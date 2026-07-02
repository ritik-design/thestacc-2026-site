export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimiJson } from '../../lib/kimi';

interface LinkSuggestion {
  id: number;
  context: string;
  anchorText: string;
  targetTopic: string;
  targetUrlHint: string;
  priority: 'high' | 'medium' | 'low';
  reasoning: string;
}

interface InternalLinkResponse {
  url: string;
  keyword: string;
  pageTitle: string;
  suggestions: LinkSuggestion[];
  summary: string;
  totalOpportunities: number;
  source: 'ai' | 'fallback';
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

/** Strip HTML tags and extract readable text. */
function extractText(html: string): { title: string; text: string } {
  // Extract title
  const titleMatch = html.match(/<title[^>]*>([^<]*)<\/title>/i);
  const title = titleMatch ? titleMatch[1].trim() : '';

  // Remove script, style, nav, footer, header tags and their contents
  let cleaned = html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, ' ')
    .replace(/<nav[^>]*>[\s\S]*?<\/nav>/gi, ' ')
    .replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, ' ')
    .replace(/<header[^>]*>[\s\S]*?<\/header>/gi, ' ')
    .replace(/<aside[^>]*>[\s\S]*?<\/aside>/gi, ' ')
    .replace(/<noscript[^>]*>[\s\S]*?<\/noscript>/gi, ' ')
    .replace(/<!--[\s\S]*?-->/g, ' ');

  // Extract main content if available
  const mainMatch = cleaned.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
  const articleMatch = cleaned.match(/<article[^>]*>([\s\S]*?)<\/article>/i);
  const content = mainMatch ? mainMatch[1] : articleMatch ? articleMatch[1] : cleaned;

  // Strip remaining HTML tags
  const text = content
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  return { title, text };
}

export const POST: APIRoute = async ({ request }) => {
  let body: { url?: string; keyword?: string };

  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const url = body.url?.trim() || '';
  const keyword = body.keyword?.trim() || '';

  // Validate URL
  if (!url || !/^https?:\/\//i.test(url)) {
    return json({ error: 'A valid URL starting with http:// or https:// is required' }, 400);
  }

  try {
    new URL(url);
  } catch {
    return json({ error: 'Invalid URL format' }, 400);
  }

  if (!keyword || keyword.length < 2) {
    return json({ error: 'Target keyword is required (min 2 chars)' }, 400);
  }

  // 1. Fetch page content
  let pageText: string;
  let pageTitle: string;

  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    const res = await fetch(url, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; theStaccBot/1.0; +https://thestacc.com)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
      },
    });
    clearTimeout(timer);

    if (!res.ok) {
      return json({ error: `Could not fetch the page (HTTP ${res.status}). Make sure the URL is accessible.` }, 400);
    }

    const html = await res.text();
    const extracted = extractText(html);
    pageTitle = extracted.title;
    pageText = extracted.text;

    if (pageText.length < 100) {
      return json({ error: 'Page has too little content to analyze. Try a different URL with more text.' }, 400);
    }
  } catch (err) {
    const msg = err instanceof Error ? err.message : 'Unknown error';
    if (msg.includes('abort')) {
      return json({ error: 'Page took too long to load. The site may be blocking automated requests.' }, 400);
    }
    return json({ error: `Could not fetch the page: ${msg}` }, 400);
  }

  // 2. Truncate text for Kimi (keep first ~10K chars which is usually enough)
  const truncatedText = pageText.slice(0, 10000);

  // 3. Call Kimi to analyze internal link opportunities
  const suggestions = await analyzeWithKimi(truncatedText, pageTitle, keyword, url);

  if (!suggestions || suggestions.length === 0) {
    // Fallback: generate generic suggestions
    const fallback = generateFallbackSuggestions(keyword, url);
    return json({
      url,
      keyword,
      pageTitle,
      suggestions: fallback,
      summary: `Found ${fallback.length} general internal linking opportunities for "${keyword}". The page content could not be deeply analyzed, but these suggestions follow SEO best practices.`,
      totalOpportunities: fallback.length,
      source: 'fallback',
    } as InternalLinkResponse, 200);
  }

  return json({
    url,
    keyword,
    pageTitle,
    suggestions,
    summary: `Found ${suggestions.length} internal linking opportunity${suggestions.length === 1 ? '' : 'ies'} on "${pageTitle || url}" for the keyword "${keyword}". High-priority links should be implemented first for maximum SEO impact.`,
    totalOpportunities: suggestions.length,
    source: 'ai',
  } as InternalLinkResponse, 200);
};

async function analyzeWithKimi(
  text: string,
  pageTitle: string,
  keyword: string,
  pageUrl: string
): Promise<LinkSuggestion[] | null> {
  const systemPrompt = `You are an expert SEO content strategist specializing in internal linking. You analyze webpage content and identify the best opportunities to add internal links that improve SEO, user experience, and topical authority.

Rules:
- Identify specific sentences or paragraphs where a natural internal link can be added
- Suggest anchor text that is descriptive and keyword-rich (avoid "click here" or "read more")
- Suggest what topic/page the link should point toward
- Assign priority (high/medium/low) based on SEO impact and natural fit
- Each suggestion must include a brief reasoning explaining the SEO benefit
- Focus on contextual links within body content, not navigation
- Suggest 5-8 opportunities maximum
- The suggestions must feel natural — no forced or awkward placements
- Return ONLY valid JSON, no markdown formatting`;

  const domain = new URL(pageUrl).hostname;

  const userPrompt = `Analyze the following webpage content and identify internal linking opportunities for the target keyword "${keyword}".

Page title: ${pageTitle || 'N/A'}
Page URL: ${pageUrl}
Domain: ${domain}

Content:
---
${text}
---

Return JSON only:
{
  "suggestions": [
    {
      "id": 1,
      "context": "The surrounding sentence or paragraph where the link should be added (30-80 words)",
      "anchorText": "The exact words that should become the clickable link",
      "targetTopic": "What topic or page type this link should point to (e.g., 'Service page about teeth whitening')",
      "targetUrlHint": "A suggested URL path like /services/teeth-whitening/",
      "priority": "high",
      "reasoning": "1-2 sentences explaining why this link helps SEO and user experience"
    }
  ]
}`;

  const result = await callKimiJson<{ suggestions: LinkSuggestion[] }>({
    systemPrompt,
    userPrompt,
    maxTokens: 4096,
    temperature: 0.5,
    timeoutMs: 45000,
  });

  if (!result?.suggestions || !Array.isArray(result.suggestions)) return null;

  // Validate and clean suggestions
  return result.suggestions
    .filter((s) => s.context && s.anchorText)
    .map((s, i) => ({
      id: s.id || i + 1,
      context: s.context.slice(0, 300),
      anchorText: s.anchorText.slice(0, 100),
      targetTopic: (s.targetTopic || 'Related page').slice(0, 100),
      targetUrlHint: (s.targetUrlHint || '/').slice(0, 200),
      priority: ['high', 'medium', 'low'].includes(s.priority) ? s.priority : 'medium',
      reasoning: (s.reasoning || '').slice(0, 250),
    }));
}

function generateFallbackSuggestions(keyword: string, pageUrl: string): LinkSuggestion[] {
  const domain = new URL(pageUrl).hostname;
  const kwSlug = keyword.toLowerCase().replace(/\s+/g, '-');

  return [
    {
      id: 1,
      context: `At the beginning of your article or page, introduce the topic of ${keyword} and link to your main pillar or service page that covers this topic in depth.`,
      anchorText: keyword,
      targetTopic: `Main pillar page about ${keyword}`,
      targetUrlHint: `/${kwSlug}/`,
      priority: 'high',
      reasoning: 'Linking your target keyword early in the content signals topical relevance to search engines and helps users find comprehensive information.',
    },
    {
      id: 2,
      context: `In a section discussing related services or products, mention ${keyword} and link to the dedicated page.`,
      anchorText: `learn more about ${keyword}`,
      targetTopic: `Service or product page for ${keyword}`,
      targetUrlHint: `/services/${kwSlug}/`,
      priority: 'high',
      reasoning: 'Contextual links from related content pass topical authority and help users navigate to conversion pages.',
    },
    {
      id: 3,
      context: `When mentioning how your business helps customers with ${keyword}, link to a case study or results page.`,
      anchorText: `our ${keyword} solutions`,
      targetTopic: 'Case study or results page',
      targetUrlHint: `/case-studies/${kwSlug}/`,
      priority: 'medium',
      reasoning: 'Case study links build trust with readers while distributing link equity to important conversion pages.',
    },
    {
      id: 4,
      context: `In a FAQ section or conclusion, reference ${keyword} and link to a detailed guide or resource page.`,
      anchorText: `complete guide to ${keyword}`,
      targetTopic: 'Comprehensive guide or resource page',
      targetUrlHint: `/guides/${kwSlug}/`,
      priority: 'medium',
      reasoning: 'FAQ and conclusion links capture users who have read through the content and want deeper information.',
    },
    {
      id: 5,
      context: `If you mention pricing, packages, or plans related to ${keyword}, link to your pricing page with descriptive anchor text.`,
      anchorText: `${keyword} pricing and packages`,
      targetTopic: 'Pricing page',
      targetUrlHint: '/pricing/',
      priority: 'low',
      reasoning: 'Pricing links convert interested readers into leads, but should only appear when pricing is contextually relevant.',
    },
  ];
}
