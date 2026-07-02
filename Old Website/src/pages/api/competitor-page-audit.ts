export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimi } from '../../lib/kimi';

interface PageAnalysis {
  url: string;
  title: string;
  metaDescription: string;
  h1: string[];
  h2: string[];
  h3: string[];
  wordCount: number;
  imageCount: number;
  imagesWithAlt: number;
  internalLinks: number;
  externalLinks: number;
  hasSchema: boolean;
  schemaTypes: string[];
  hasCanonical: boolean;
  canonicalUrl: string | null;
  hasOpenGraph: boolean;
  ogTags: Record<string, string>;
  loadTimeMs: number | null;
}

interface ComparisonResult {
  category: string;
  winner: 'a' | 'b' | 'tie';
  scoreA: number;
  scoreB: number;
  details: string;
}

interface AuditResponse {
  ok: boolean;
  data?: {
    pageA: PageAnalysis;
    pageB: PageAnalysis;
    comparisons: ComparisonResult[];
    recommendations: string[];
    overallScoreA: number;
    overallScoreB: number;
  };
  error?: string;
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: { urlA?: string; urlB?: string };

  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: 'Invalid request body' }, 400);
  }

  let urlA = body.urlA?.trim() || '';
  let urlB = body.urlB?.trim() || '';

  if (!urlA || !urlB) {
    return json({ ok: false, error: 'Both URLs are required' }, 400);
  }

  // Normalize URLs
  for (const url of [urlA, urlB]) {
    if (!/^https?:\/\//i.test(url)) {
      url = 'https://' + url;
    }
  }

  try {
    new URL(urlA);
    new URL(urlB);
  } catch {
    return json({ ok: false, error: 'Invalid URL format' }, 400);
  }

  // Fetch both pages in parallel
  const [analysisA, analysisB] = await Promise.all([
    analyzePage(urlA),
    analyzePage(urlB),
  ]);

  // Run comparisons
  const comparisons = runComparisons(analysisA, analysisB);

  // Calculate overall scores
  const overallScoreA = Math.round(comparisons.reduce((sum, c) => sum + c.scoreA, 0) / comparisons.length);
  const overallScoreB = Math.round(comparisons.reduce((sum, c) => sum + c.scoreB, 0) / comparisons.length);

  // Generate AI recommendations
  const recommendations = await generateRecommendations(analysisA, analysisB, comparisons);

  return json({
    ok: true,
    data: {
      pageA: analysisA,
      pageB: analysisB,
      comparisons,
      recommendations,
      overallScoreA,
      overallScoreB,
    },
  } as AuditResponse, 200);
};

async function analyzePage(url: string): Promise<PageAnalysis> {
  const startTime = Date.now();
  const result: PageAnalysis = {
    url,
    title: '',
    metaDescription: '',
    h1: [],
    h2: [],
    h3: [],
    wordCount: 0,
    imageCount: 0,
    imagesWithAlt: 0,
    internalLinks: 0,
    externalLinks: 0,
    hasSchema: false,
    schemaTypes: [],
    hasCanonical: false,
    canonicalUrl: null,
    hasOpenGraph: false,
    ogTags: {},
    loadTimeMs: null,
  };

  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 10000);
    const res = await fetch(url, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; theStaccBot/1.0; +https://thestacc.com)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      },
    });
    clearTimeout(timer);

    if (!res.ok) {
      result.title = `Error: ${res.status}`;
      return result;
    }

    const html = await res.text();
    result.loadTimeMs = Date.now() - startTime;

    // Title
    const titleMatch = html.match(/<title[^>]*>([^<]*)<\/title>/i);
    result.title = titleMatch ? titleMatch[1].trim() : '';

    // Meta description
    const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']*)["'][^>]*>/i)
      || html.match(/<meta[^>]*content=["']([^"']*)["'][^>]*name=["']description["'][^>]*>/i);
    result.metaDescription = descMatch ? descMatch[1].trim() : '';

    // Headings
    result.h1 = extractTags(html, 'h1');
    result.h2 = extractTags(html, 'h2');
    result.h3 = extractTags(html, 'h3');

    // Word count (rough estimate from body text)
    const bodyText = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    result.wordCount = bodyText.split(/\s+/).length;

    // Images
    const imgMatches = html.match(/<img[^>]*>/gi) || [];
    result.imageCount = imgMatches.length;
    result.imagesWithAlt = imgMatches.filter(img => /alt=["'][^"']+["']/.test(img)).length;

    // Links
    const linkMatches = html.match(/<a[^>]*href=["']([^"']+)["'][^>]*>/gi) || [];
    const origin = new URL(url).origin;
    linkMatches.forEach(link => {
      const hrefMatch = link.match(/href=["']([^"']+)["']/);
      if (hrefMatch) {
        try {
          const resolved = new URL(hrefMatch[1], url).origin;
          if (resolved === origin) result.internalLinks++;
          else result.externalLinks++;
        } catch {
          // Invalid URL
        }
      }
    });

    // Schema markup
    const schemaMatches = html.match(/<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi) || [];
    result.hasSchema = schemaMatches.length > 0;
    result.schemaTypes = schemaMatches.map(s => {
      const typeMatch = s.match(/"@type"\s*:\s*"([^"]+)"/);
      return typeMatch ? typeMatch[1] : 'Unknown';
    }).filter((v, i, a) => a.indexOf(v) === i);

    // Canonical
    const canonMatch = html.match(/<link[^>]*rel=["']canonical["'][^>]*href=["']([^"']*)["'][^>]*>/i)
      || html.match(/<link[^>]*href=["']([^"']*)["'][^>]*rel=["']canonical["'][^>]*>/i);
    if (canonMatch) {
      result.hasCanonical = true;
      result.canonicalUrl = canonMatch[1];
    }

    // Open Graph
    const ogMatches = html.match(/<meta[^>]*property=["']og:([^"']*)["'][^>]*content=["']([^"']*)["'][^>]*>/gi) || [];
    result.hasOpenGraph = ogMatches.length > 0;
    ogMatches.forEach(og => {
      const match = og.match(/property=["']og:([^"']*)["'].*content=["']([^"']*)["']/);
      if (match) result.ogTags[match[1]] = match[2];
    });

  } catch {
    result.title = 'Failed to fetch page';
  }

  return result;
}

function extractTags(html: string, tag: string): string[] {
  const regex = new RegExp(`<${tag}[^>]*>([^<]*)<\/${tag}>`, 'gi');
  const matches: string[] = [];
  let match;
  while ((match = regex.exec(html)) !== null) {
    matches.push(match[1].trim());
  }
  return matches;
}

function runComparisons(a: PageAnalysis, b: PageAnalysis): ComparisonResult[] {
  const comparisons: ComparisonResult[] = [];

  // Title comparison
  const titleScoreA = scoreTextLength(a.title, 30, 60);
  const titleScoreB = scoreTextLength(b.title, 30, 60);
  comparisons.push({
    category: 'Title Tag',
    winner: titleScoreA > titleScoreB ? 'a' : titleScoreB > titleScoreA ? 'b' : 'tie',
    scoreA: titleScoreA,
    scoreB: titleScoreB,
    details: `Length: ${a.title.length} vs ${b.title.length} chars`,
  });

  // Meta description
  const descScoreA = scoreTextLength(a.metaDescription, 120, 160);
  const descScoreB = scoreTextLength(b.metaDescription, 120, 160);
  comparisons.push({
    category: 'Meta Description',
    winner: descScoreA > descScoreB ? 'a' : descScoreB > descScoreA ? 'b' : 'tie',
    scoreA: descScoreA,
    scoreB: descScoreB,
    details: `Length: ${a.metaDescription.length} vs ${b.metaDescription.length} chars`,
  });

  // H1 tags
  const h1ScoreA = a.h1.length === 1 ? 100 : a.h1.length === 0 ? 0 : 50;
  const h1ScoreB = b.h1.length === 1 ? 100 : b.h1.length === 0 ? 0 : 50;
  comparisons.push({
    category: 'H1 Tag',
    winner: h1ScoreA > h1ScoreB ? 'a' : h1ScoreB > h1ScoreA ? 'b' : 'tie',
    scoreA: h1ScoreA,
    scoreB: h1ScoreB,
    details: `${a.h1.length} H1(s) vs ${b.h1.length} H1(s)`,
  });

  // Content depth (H2s)
  const h2ScoreA = Math.min(a.h2.length * 10, 100);
  const h2ScoreB = Math.min(b.h2.length * 10, 100);
  comparisons.push({
    category: 'Content Structure (H2s)',
    winner: h2ScoreA > h2ScoreB ? 'a' : h2ScoreB > h2ScoreA ? 'b' : 'tie',
    scoreA: h2ScoreA,
    scoreB: h2ScoreB,
    details: `${a.h2.length} H2s vs ${b.h2.length} H2s`,
  });

  // Word count
  const wordScoreA = Math.min(a.wordCount / 10, 100);
  const wordScoreB = Math.min(b.wordCount / 10, 100);
  comparisons.push({
    category: 'Content Length',
    winner: wordScoreA > wordScoreB ? 'a' : wordScoreB > wordScoreA ? 'b' : 'tie',
    scoreA: Math.round(wordScoreA),
    scoreB: Math.round(wordScoreB),
    details: `${a.wordCount.toLocaleString()} vs ${b.wordCount.toLocaleString()} words`,
  });

  // Images with alt text
  const altRatioA = a.imageCount > 0 ? (a.imagesWithAlt / a.imageCount) * 100 : 100;
  const altRatioB = b.imageCount > 0 ? (b.imagesWithAlt / b.imageCount) * 100 : 100;
  comparisons.push({
    category: 'Image Accessibility',
    winner: altRatioA > altRatioB ? 'a' : altRatioB > altRatioA ? 'b' : 'tie',
    scoreA: Math.round(altRatioA),
    scoreB: Math.round(altRatioB),
    details: `${a.imagesWithAlt}/${a.imageCount} vs ${b.imagesWithAlt}/${b.imageCount} with alt text`,
  });

  // Internal links
  const linkScoreA = Math.min(a.internalLinks * 5, 100);
  const linkScoreB = Math.min(b.internalLinks * 5, 100);
  comparisons.push({
    category: 'Internal Links',
    winner: linkScoreA > linkScoreB ? 'a' : linkScoreB > linkScoreA ? 'b' : 'tie',
    scoreA: linkScoreA,
    scoreB: linkScoreB,
    details: `${a.internalLinks} vs ${b.internalLinks} internal links`,
  });

  // Schema markup
  const schemaScoreA = a.hasSchema ? (a.schemaTypes.length * 20) : 0;
  const schemaScoreB = b.hasSchema ? (b.schemaTypes.length * 20) : 0;
  comparisons.push({
    category: 'Schema Markup',
    winner: schemaScoreA > schemaScoreB ? 'a' : schemaScoreB > schemaScoreA ? 'b' : 'tie',
    scoreA: Math.min(schemaScoreA, 100),
    scoreB: Math.min(schemaScoreB, 100),
    details: `${a.schemaTypes.join(', ') || 'None'} vs ${b.schemaTypes.join(', ') || 'None'}`,
  });

  // Open Graph
  const ogScoreA = Object.keys(a.ogTags).length * 20;
  const ogScoreB = Object.keys(b.ogTags).length * 20;
  comparisons.push({
    category: 'Social Sharing (OG)',
    winner: ogScoreA > ogScoreB ? 'a' : ogScoreB > ogScoreA ? 'b' : 'tie',
    scoreA: Math.min(ogScoreA, 100),
    scoreB: Math.min(ogScoreB, 100),
    details: `${Object.keys(a.ogTags).length} vs ${Object.keys(b.ogTags).length} OG tags`,
  });

  return comparisons;
}

function scoreTextLength(text: string, min: number, max: number): number {
  const len = text.length;
  if (len === 0) return 0;
  if (len >= min && len <= max) return 100;
  if (len < min) return Math.round((len / min) * 100);
  return Math.round(Math.max(0, 100 - ((len - max) / max) * 50));
}

async function generateRecommendations(
  a: PageAnalysis,
  b: PageAnalysis,
  comparisons: ComparisonResult[]
): Promise<string[]> {
  const prompt = `Compare these two pages and give 5 specific, actionable SEO recommendations for the weaker page.

Page A: ${a.url}
- Title: ${a.title} (${a.title.length} chars)
- Meta: ${a.metaDescription.substring(0, 100)} (${a.metaDescription.length} chars)
- Word count: ${a.wordCount}
- H1s: ${a.h1.join(', ')}
- H2s: ${a.h2.length}
- Images: ${a.imageCount} (${a.imagesWithAlt} with alt)
- Internal links: ${a.internalLinks}
- Schema: ${a.schemaTypes.join(', ') || 'None'}
- OG tags: ${Object.keys(a.ogTags).length}

Page B: ${b.url}
- Title: ${b.title} (${b.title.length} chars)
- Meta: ${b.metaDescription.substring(0, 100)} (${b.metaDescription.length} chars)
- Word count: ${b.wordCount}
- H1s: ${b.h1.join(', ')}
- H2s: ${b.h2.length}
- Images: ${b.imageCount} (${b.imagesWithAlt} with alt)
- Internal links: ${b.internalLinks}
- Schema: ${b.schemaTypes.join(', ') || 'None'}
- OG tags: ${Object.keys(b.ogTags).length}

Comparison scores (0-100):
${comparisons.map(c => `- ${c.category}: A=${c.scoreA}, B=${c.scoreB}`).join('\n')}

Give exactly 5 concise, actionable recommendations (1 sentence each). Focus on the biggest gaps. No explanations, just the recommendations. Number them 1-5.`;

  const result = await callKimi({
    systemPrompt: 'You are an expert SEO analyst. Give concise, actionable recommendations. One sentence per recommendation. No fluff.',
    userPrompt: prompt,
    maxTokens: 800,
    temperature: 0.3,
    timeoutMs: 15000,
  });

  if (!result) return [];

  return result
    .split('\n')
    .map(line => line.replace(/^\d+\.\s*/, '').trim())
    .filter(line => line.length > 10)
    .slice(0, 5);
}
