export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimiJson } from '../../lib/kimi';

interface VisibilityCheck {
  name: string;
  status: 'pass' | 'warn' | 'fail';
  score: number; // 0-10
  description: string;
  recommendation: string;
}

interface VisibilityCategory {
  name: string;
  score: number; // 0-100
  maxScore: number;
  checks: VisibilityCheck[];
}

interface AIVisibilityResponse {
  url: string;
  domain: string;
  overallScore: number; // 0-100
  grade: string; // A+, A, B, C, D, F
  categories: VisibilityCategory[];
  summary: string;
  topRecommendations: string[];
  aiCrawlerAccess: {
    name: string;
    allowed: boolean;
    detail: string;
  }[];
  llmsTxt: {
    exists: boolean;
    url: string;
    preview?: string;
  };
  source: 'ai' | 'fallback';
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: { url?: string };

  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  let url = body.url?.trim() || '';

  // Normalize URL
  if (!url) {
    return json({ error: 'URL is required' }, 400);
  }

  if (!/^https?:\/\//i.test(url)) {
    url = 'https://' + url;
  }

  let parsedUrl: URL;
  try {
    parsedUrl = new URL(url);
  } catch {
    return json({ error: 'Invalid URL format' }, 400);
  }

  const domain = parsedUrl.hostname;
  const origin = parsedUrl.origin;

  // ── Parallel data collection ───────────────────────────────
  const [homepageResult, robotsResult, llmsResult] = await Promise.all([
    fetchHomepage(origin),
    fetchRobotsTxt(origin),
    fetchLlmsTxt(origin),
  ]);

  // ── Build signal report for Kimi ───────────────────────────
  const signals = buildSignalReport(homepageResult, robotsResult, llmsResult, domain);

  // ── Call Kimi for analysis ─────────────────────────────────
  const analysis = await analyzeWithKimi(signals, domain);

  if (analysis) {
    return json({
      url: origin,
      domain,
      ...analysis,
      aiCrawlerAccess: signals.aiCrawlerAccess,
      llmsTxt: {
        exists: llmsResult.ok,
        url: `${origin}/llms.txt`,
        preview: llmsResult.text?.slice(0, 300),
      },
      source: 'ai',
    } as AIVisibilityResponse, 200);
  }

  // ── Fallback: rule-based scoring ───────────────────────────
  const fallback = buildFallbackReport(signals, domain);
  return json({
    url: origin,
    domain,
    ...fallback,
    aiCrawlerAccess: signals.aiCrawlerAccess,
    llmsTxt: {
      exists: llmsResult.ok,
      url: `${origin}/llms.txt`,
      preview: llmsResult.text?.slice(0, 300),
    },
    source: 'fallback',
  } as AIVisibilityResponse, 200);
};

// ── Fetch helpers ──────────────────────────────────────────────

async function fetchHomepage(origin: string): Promise<{
  ok: boolean;
  html: string;
  headers: Record<string, string>;
}> {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    const res = await fetch(origin, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; theStaccBot/1.0; +https://thestacc.com)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      },
    });
    clearTimeout(timer);

    if (!res.ok) return { ok: false, html: '', headers: {} };

    const headers: Record<string, string> = {};
    res.headers.forEach((v, k) => { headers[k.toLowerCase()] = v; });
    const html = await res.text();
    return { ok: true, html, headers };
  } catch {
    return { ok: false, html: '', headers: {} };
  }
}

async function fetchRobotsTxt(origin: string): Promise<{
  ok: boolean;
  text: string;
}> {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 10000);
    const res = await fetch(`${origin}/robots.txt`, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; theStaccBot/1.0; +https://thestacc.com)',
      },
    });
    clearTimeout(timer);

    if (!res.ok) return { ok: false, text: '' };
    const text = await res.text();
    return { ok: true, text };
  } catch {
    return { ok: false, text: '' };
  }
}

async function fetchLlmsTxt(origin: string): Promise<{
  ok: boolean;
  text: string;
}> {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 8000);
    const res = await fetch(`${origin}/llms.txt`, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; theStaccBot/1.0; +https://thestacc.com)',
      },
    });
    clearTimeout(timer);

    if (!res.ok) return { ok: false, text: '' };
    const text = await res.text();
    return { ok: text.length > 0, text };
  } catch {
    return { ok: false, text: '' };
  }
}

// ── Signal extraction ──────────────────────────────────────────

interface SignalReport {
  hasTitle: boolean;
  hasDescription: boolean;
  hasCanonical: boolean;
  hasSchema: boolean;
  schemaTypes: string[];
  hasAuthorInfo: boolean;
  hasDates: boolean;
  hasAboutPage: boolean;
  hasContactInfo: boolean;
  hasFaqSchema: boolean;
  hasArticleSchema: boolean;
  hasOrganizationSchema: boolean;
  hasBreadcrumbSchema: boolean;
  wordCount: number;
  headingCount: number;
  hasSocialProfiles: boolean;
  aiCrawlerAccess: {
    name: string;
    allowed: boolean;
    detail: string;
  }[];
  robotsTxtPresent: boolean;
  llmsTxtPresent: boolean;
  sitemapPresent: boolean;
}

function buildSignalReport(
  home: { ok: boolean; html: string; headers: Record<string, string> },
  robots: { ok: boolean; text: string },
  llms: { ok: boolean; text: string },
  domain: string
): SignalReport {
  const html = home.html.toLowerCase();
  const htmlOriginal = home.html;

  // Schema detection
  const schemaMatches = htmlOriginal.match(/"@type"\s*:\s*"([^"]+)"/gi) || [];
  const schemaTypes = schemaMatches.map(m => m.replace(/"@type"\s*:\s*"/i, '').replace(/"$/, ''));

  // Social profile links
  const socialPatterns = [
    /href="https?:\/\/twitter\.com\/[^"]+"/i,
    /href="https?:\/\/x\.com\/[^"]+"/i,
    /href="https?:\/\/linkedin\.com\/company\/[^"]+"/i,
    /href="https?:\/\/facebook\.com\/[^"]+"/i,
    /href="https?:\/\/instagram\.com\/[^"]+"/i,
    /href="https?:\/\/youtube\.com\/[^"]+"/i,
  ];
  const hasSocialProfiles = socialPatterns.some(p => p.test(htmlOriginal));

  // Heading count
  const headingCount = (htmlOriginal.match(/<h[1-6][^>]*>/gi) || []).length;

  // Word count (rough estimate from body text)
  const bodyMatch = htmlOriginal.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
  const bodyText = bodyMatch ? bodyMatch[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : '';
  const wordCount = bodyText.split(/\s+/).filter(w => w.length > 0).length;

  // AI crawler access analysis from robots.txt
  const robotsText = robots.text;
  const aiCrawlers = [
    { name: 'GPTBot', pattern: /gptbot/i },
    { name: 'ClaudeBot', pattern: /claudebot/i },
    { name: 'PerplexityBot', pattern: /perplexitybot/i },
    { name: 'Google-Extended', pattern: /google-extended/i },
    { name: 'CCBot', pattern: /ccbot/i },
    { name: 'ChatGPT-User', pattern: /chatgpt-user/i },
  ];

  const aiCrawlerAccess = aiCrawlers.map(crawler => {
    const hasRule = crawler.pattern.test(robotsText);
    const hasDisallow = robotsText.includes('disallow');

    if (!robots.ok) {
      return { name: crawler.name, allowed: true, detail: 'No robots.txt found — crawler access is unrestricted' };
    }

    if (!hasRule) {
      return { name: crawler.name, allowed: true, detail: 'No specific rule found — allowed by default' };
    }

    // Simple heuristic: if crawler name appears near "disallow: /" it's blocked
    const lines = robotsText.split('\n');
    let inCrawlerBlock = false;
    let blocked = false;

    for (const line of lines) {
      const lower = line.toLowerCase().trim();
      if (lower.startsWith('user-agent:')) {
        inCrawlerBlock = crawler.pattern.test(line) || /\*/.test(line);
      }
      if (inCrawlerBlock && lower.startsWith('disallow:') && lower.includes('/')) {
        blocked = true;
      }
      if (inCrawlerBlock && lower.startsWith('allow:')) {
        // More nuanced: allow after disallow might override
        blocked = false;
      }
    }

    return {
      name: crawler.name,
      allowed: !blocked,
      detail: blocked ? 'Explicitly disallowed in robots.txt' : 'Allowed or no restriction found',
    };
  });

  // Check sitemap reference in robots.txt
  const sitemapPresent = /sitemap/i.test(robotsText);

  return {
    hasTitle: /<title[^>]*>[^<]+<\/title>/i.test(htmlOriginal),
    hasDescription: /<meta[^>]*name="description"[^>]*>/i.test(htmlOriginal),
    hasCanonical: /<link[^>]*rel="canonical"[^>]*>/i.test(htmlOriginal),
    hasSchema: schemaTypes.length > 0,
    schemaTypes,
    hasAuthorInfo: /author|byline|"person"|"author"/i.test(htmlOriginal),
    hasDates: /published|modified|datepublished|datemodified/i.test(htmlOriginal),
    hasAboutPage: /href="[^"]*about[^"]*"/i.test(htmlOriginal),
    hasContactInfo: /href="[^"]*contact[^"]*"|tel:|mailto:/i.test(htmlOriginal),
    hasFaqSchema: schemaTypes.some(t => /faq/i.test(t)),
    hasArticleSchema: schemaTypes.some(t => /article|blogposting|newsarticle/i.test(t)),
    hasOrganizationSchema: schemaTypes.some(t => /organization|localbusiness/i.test(t)),
    hasBreadcrumbSchema: schemaTypes.some(t => /breadcrumb/i.test(t)),
    wordCount,
    headingCount,
    hasSocialProfiles,
    aiCrawlerAccess,
    robotsTxtPresent: robots.ok,
    llmsTxtPresent: llms.ok,
    sitemapPresent,
  };
}

// ── Kimi analysis ──────────────────────────────────────────────

async function analyzeWithKimi(signals: SignalReport, domain: string): Promise<{
  overallScore: number;
  grade: string;
  categories: VisibilityCategory[];
  summary: string;
  topRecommendations: string[];
} | null> {
  const systemPrompt = `You are an expert in Generative Engine Optimization (GEO) and AI search visibility. You analyze websites for how likely they are to be discovered, cited, and recommended by AI systems like ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews.

Scoring rules:
- Overall score is 0-100
- Grade: A+ (97-100), A (90-96), B (80-89), C (70-79), D (60-69), F (<60)
- Each category has a max score and individual checks scored 0-10
- Be honest and critical — most sites score C or D
- Base scores ONLY on the signals provided, do not hallucinate

Categories:
1. AI Crawler Access (max 20 pts) — can AI crawlers access the site?
2. Structured Data & Schema (max 20 pts) — schema.org markup quality
3. Content Quality Signals (max 20 pts) — depth, structure, freshness signals
4. E-E-A-T Signals (max 20 pts) — experience, expertise, authoritativeness, trust
5. AI-Specific Readiness (max 20 pts) — llms.txt, sitemap, canonical, etc.

Return ONLY valid JSON. No markdown.`;

  const userPrompt = `Analyze the following website signals for AI visibility and return a JSON report.

Domain: ${domain}

Signals:
${JSON.stringify(signals, null, 2)}

Return JSON in this exact structure:
{
  "overallScore": 72,
  "grade": "C",
  "summary": "2-3 sentence overview of the site's AI visibility strengths and weaknesses",
  "topRecommendations": [
    "Specific actionable recommendation 1",
    "Specific actionable recommendation 2",
    "Specific actionable recommendation 3",
    "Specific actionable recommendation 4",
    "Specific actionable recommendation 5"
  ],
  "categories": [
    {
      "name": "AI Crawler Access",
      "score": 15,
      "maxScore": 20,
      "checks": [
        {
          "name": "Check name",
          "status": "pass|warn|fail",
          "score": 8,
          "description": "What this check evaluates",
          "recommendation": "What to do to improve"
        }
      ]
    }
  ]
}`;

  const result = await callKimiJson<{
    overallScore: number;
    grade: string;
    summary: string;
    topRecommendations: string[];
    categories: VisibilityCategory[];
  }>({
    systemPrompt,
    userPrompt,
    maxTokens: 4096,
    temperature: 0.3,
    timeoutMs: 45000,
  });

  if (!result || typeof result.overallScore !== 'number') return null;

  // Clamp score
  result.overallScore = Math.max(0, Math.min(100, Math.round(result.overallScore)));

  // Validate categories
  if (!Array.isArray(result.categories)) return null;

  return result;
}

// ── Fallback rule-based report ─────────────────────────────────

function buildFallbackReport(signals: SignalReport, domain: string): {
  overallScore: number;
  grade: string;
  categories: VisibilityCategory[];
  summary: string;
  topRecommendations: string[];
} {
  const categories: VisibilityCategory[] = [];

  // 1. AI Crawler Access (max 20)
  const allowedCrawlers = signals.aiCrawlerAccess.filter(c => c.allowed).length;
  const totalCrawlers = signals.aiCrawlerAccess.length;
  const crawlerScore = Math.round((allowedCrawlers / totalCrawlers) * 20);
  categories.push({
    name: 'AI Crawler Access',
    score: crawlerScore,
    maxScore: 20,
    checks: signals.aiCrawlerAccess.map(c => ({
      name: c.name,
      status: c.allowed ? 'pass' : 'fail' as 'pass' | 'warn' | 'fail',
      score: c.allowed ? 3 : 0,
      description: c.detail,
      recommendation: c.allowed
        ? `${c.name} can access your site. Maintain good content to be cited.`
        : `Consider allowing ${c.name} in robots.txt if you want AI systems to discover your content.`,
    })),
  });

  // 2. Structured Data & Schema (max 20)
  let schemaScore = 0;
  const schemaChecks: VisibilityCheck[] = [];

  schemaChecks.push({
    name: 'Schema.org markup present',
    status: signals.hasSchema ? 'pass' : 'fail',
    score: signals.hasSchema ? 4 : 0,
    description: 'Structured data helps AI systems understand your content context',
    recommendation: signals.hasSchema
      ? 'Good — schema is present. Ensure it validates with Google\'s Rich Results Test.'
      : 'Add Schema.org JSON-LD markup to key pages. Start with Organization and WebPage.',
  });
  if (signals.hasSchema) schemaScore += 4;

  schemaChecks.push({
    name: 'Article or BlogPosting schema',
    status: signals.hasArticleSchema ? 'pass' : 'warn',
    score: signals.hasArticleSchema ? 4 : 1,
    description: 'Article schema signals high-quality editorial content',
    recommendation: signals.hasArticleSchema
      ? 'Article schema detected — excellent for AI citation.'
      : 'Add Article or BlogPosting schema to blog posts and content pages.',
  });
  if (signals.hasArticleSchema) schemaScore += 4; else schemaScore += 1;

  schemaChecks.push({
    name: 'FAQ schema',
    status: signals.hasFaqSchema ? 'pass' : 'warn',
    score: signals.hasFaqSchema ? 4 : 1,
    description: 'FAQ schema is frequently cited by AI systems for direct answers',
    recommendation: signals.hasFaqSchema
      ? 'FAQ schema present — AI systems love structured Q&A content.'
      : 'Add FAQPage schema to pages with Q&A content. High citation potential.',
  });
  if (signals.hasFaqSchema) schemaScore += 4; else schemaScore += 1;

  schemaChecks.push({
    name: 'Organization or LocalBusiness schema',
    status: signals.hasOrganizationSchema ? 'pass' : 'warn',
    score: signals.hasOrganizationSchema ? 4 : 2,
    description: 'Organization schema builds entity recognition in AI systems',
    recommendation: signals.hasOrganizationSchema
      ? 'Organization schema detected — builds brand entity recognition.'
      : 'Add Organization schema with name, URL, logo, and sameAs links.',
  });
  if (signals.hasOrganizationSchema) schemaScore += 4; else schemaScore += 2;

  schemaChecks.push({
    name: 'Breadcrumb schema',
    status: signals.hasBreadcrumbSchema ? 'pass' : 'warn',
    score: signals.hasBreadcrumbSchema ? 4 : 1,
    description: 'Breadcrumbs help AI understand site structure',
    recommendation: signals.hasBreadcrumbSchema
      ? 'Breadcrumb schema present — helps AI map your site hierarchy.'
      : 'Add BreadcrumbList schema to improve site structure understanding.',
  });
  if (signals.hasBreadcrumbSchema) schemaScore += 4; else schemaScore += 1;

  categories.push({ name: 'Structured Data & Schema', score: schemaScore, maxScore: 20, checks: schemaChecks });

  // 3. Content Quality Signals (max 20)
  let contentScore = 0;
  const contentChecks: VisibilityCheck[] = [];

  const wordCountStatus = signals.wordCount > 1000 ? 'pass' : signals.wordCount > 300 ? 'warn' : 'fail';
  const wordCountScore = signals.wordCount > 1000 ? 5 : signals.wordCount > 300 ? 3 : 1;
  contentChecks.push({
    name: 'Content depth',
    status: wordCountStatus,
    score: wordCountScore,
    description: `Approximately ${signals.wordCount} words detected on homepage`,
    recommendation: signals.wordCount > 1000
      ? 'Good content depth — AI systems prefer substantive pages.'
      : 'Add more comprehensive content. AI systems favor pages with 1000+ words.',
  });
  contentScore += wordCountScore;

  const headingStatus = signals.headingCount >= 3 ? 'pass' : signals.headingCount > 0 ? 'warn' : 'fail';
  const headingScore = signals.headingCount >= 3 ? 5 : signals.headingCount > 0 ? 2 : 0;
  contentChecks.push({
    name: 'Heading structure',
    status: headingStatus,
    score: headingScore,
    description: `${signals.headingCount} headings detected`,
    recommendation: signals.headingCount >= 3
      ? 'Good heading structure — helps AI parse content hierarchy.'
      : 'Use H1-H6 headings to structure content logically.',
  });
  contentScore += headingScore;

  contentChecks.push({
    name: 'Title tag present',
    status: signals.hasTitle ? 'pass' : 'fail',
    score: signals.hasTitle ? 3 : 0,
    description: 'Title tags are critical for AI understanding page topic',
    recommendation: signals.hasTitle
      ? 'Title tag present.'
      : 'Add a descriptive title tag to every page.',
  });
  contentScore += signals.hasTitle ? 3 : 0;

  contentChecks.push({
    name: 'Meta description present',
    status: signals.hasDescription ? 'pass' : 'warn',
    score: signals.hasDescription ? 3 : 1,
    description: 'Meta descriptions often appear in AI citations',
    recommendation: signals.hasDescription
      ? 'Meta description present.'
      : 'Add compelling meta descriptions — AI systems sometimes use them in summaries.',
  });
  contentScore += signals.hasDescription ? 3 : 1;

  contentChecks.push({
    name: 'Canonical tag',
    status: signals.hasCanonical ? 'pass' : 'warn',
    score: signals.hasCanonical ? 4 : 1,
    description: 'Canonical tags prevent duplicate content confusion',
    recommendation: signals.hasCanonical
      ? 'Canonical tag present — helps AI identify the primary version of content.'
      : 'Add canonical tags to prevent AI systems from indexing duplicate versions.',
  });
  contentScore += signals.hasCanonical ? 4 : 1;

  categories.push({ name: 'Content Quality Signals', score: contentScore, maxScore: 20, checks: contentChecks });

  // 4. E-E-A-T Signals (max 20)
  let eeatScore = 0;
  const eeatChecks: VisibilityCheck[] = [];

  eeatChecks.push({
    name: 'Author information',
    status: signals.hasAuthorInfo ? 'pass' : 'warn',
    score: signals.hasAuthorInfo ? 5 : 1,
    description: 'Author attribution builds expertise signals',
    recommendation: signals.hasAuthorInfo
      ? 'Author information detected — good for expertise signaling.'
      : 'Add author bylines with bios and links to author pages.',
  });
  eeatScore += signals.hasAuthorInfo ? 5 : 1;

  eeatChecks.push({
    name: 'Publication dates',
    status: signals.hasDates ? 'pass' : 'warn',
    score: signals.hasDates ? 4 : 1,
    description: 'Dates signal content freshness',
    recommendation: signals.hasDates
      ? 'Publication dates detected — freshness is a ranking signal for AI.'
      : 'Add publishedDate and modifiedDate to content.',
  });
  eeatScore += signals.hasDates ? 4 : 1;

  eeatChecks.push({
    name: 'About page',
    status: signals.hasAboutPage ? 'pass' : 'warn',
    score: signals.hasAboutPage ? 4 : 1,
    description: 'About pages establish brand authority',
    recommendation: signals.hasAboutPage
      ? 'About page detected — builds brand entity recognition.'
      : 'Create an About page that explains who you are and why you\'re credible.',
  });
  eeatScore += signals.hasAboutPage ? 4 : 1;

  eeatChecks.push({
    name: 'Contact information',
    status: signals.hasContactInfo ? 'pass' : 'warn',
    score: signals.hasContactInfo ? 4 : 1,
    description: 'Contact info signals trustworthiness',
    recommendation: signals.hasContactInfo
      ? 'Contact information detected — builds trust signals.'
      : 'Add contact details (email, phone, address) to build trust.',
  });
  eeatScore += signals.hasContactInfo ? 4 : 1;

  eeatChecks.push({
    name: 'Social media presence',
    status: signals.hasSocialProfiles ? 'pass' : 'warn',
    score: signals.hasSocialProfiles ? 3 : 1,
    description: 'Social profiles build authoritativeness',
    recommendation: signals.hasSocialProfiles
      ? 'Social media links detected — helps AI verify brand identity.'
      : 'Link to official social media profiles to build brand authority.',
  });
  eeatScore += signals.hasSocialProfiles ? 3 : 1;

  categories.push({ name: 'E-E-A-T Signals', score: eeatScore, maxScore: 20, checks: eeatChecks });

  // 5. AI-Specific Readiness (max 20)
  let aiReadyScore = 0;
  const aiReadyChecks: VisibilityCheck[] = [];

  aiReadyChecks.push({
    name: 'llms.txt file',
    status: signals.llmsTxtPresent ? 'pass' : 'warn',
    score: signals.llmsTxtPresent ? 6 : 1,
    description: 'llms.txt helps AI systems understand your site structure',
    recommendation: signals.llmsTxtPresent
      ? 'llms.txt detected — excellent AI-search readiness.'
      : 'Create an llms.txt file at your domain root. It tells AI crawlers what your site is about.',
  });
  aiReadyScore += signals.llmsTxtPresent ? 6 : 1;

  aiReadyChecks.push({
    name: 'robots.txt present',
    status: signals.robotsTxtPresent ? 'pass' : 'warn',
    score: signals.robotsTxtPresent ? 4 : 1,
    description: 'robots.txt guides all crawlers including AI bots',
    recommendation: signals.robotsTxtPresent
      ? 'robots.txt detected.'
      : 'Create a robots.txt file to guide crawler behavior.',
  });
  aiReadyScore += signals.robotsTxtPresent ? 4 : 1;

  aiReadyChecks.push({
    name: 'Sitemap referenced',
    status: signals.sitemapPresent ? 'pass' : 'warn',
    score: signals.sitemapPresent ? 5 : 1,
    description: 'Sitemaps help AI crawlers discover all pages',
    recommendation: signals.sitemapPresent
      ? 'Sitemap referenced in robots.txt — good discoverability.'
      : 'Add a sitemap URL to your robots.txt file.',
  });
  aiReadyScore += signals.sitemapPresent ? 5 : 1;

  aiReadyChecks.push({
    name: 'Schema diversity',
    status: signals.schemaTypes.length >= 3 ? 'pass' : signals.schemaTypes.length > 0 ? 'warn' : 'fail',
    score: signals.schemaTypes.length >= 3 ? 5 : signals.schemaTypes.length > 0 ? 2 : 0,
    description: `${signals.schemaTypes.length} schema type(s) detected: ${signals.schemaTypes.slice(0, 5).join(', ') || 'none'}`,
    recommendation: signals.schemaTypes.length >= 3
      ? 'Good schema diversity — AI systems can understand multiple content types.'
      : 'Add more schema types (Article, FAQ, HowTo, Product, Review) for richer AI understanding.',
  });
  aiReadyScore += signals.schemaTypes.length >= 3 ? 5 : signals.schemaTypes.length > 0 ? 2 : 0;

  categories.push({ name: 'AI-Specific Readiness', score: aiReadyScore, maxScore: 20, checks: aiReadyChecks });

  // Calculate overall
  const overallScore = Math.round(
    (categories.reduce((sum, c) => sum + c.score, 0) /
     categories.reduce((sum, c) => sum + c.maxScore, 0)) * 100
  );

  const grade = overallScore >= 97 ? 'A+' :
    overallScore >= 90 ? 'A' :
    overallScore >= 80 ? 'B' :
    overallScore >= 70 ? 'C' :
    overallScore >= 60 ? 'D' : 'F';

  // Generate recommendations
  const allChecks = categories.flatMap(c => c.checks);
  const failRecs = allChecks
    .filter(c => c.status === 'fail')
    .map(c => c.recommendation);
  const warnRecs = allChecks
    .filter(c => c.status === 'warn')
    .map(c => c.recommendation);
  const topRecommendations = [...failRecs, ...warnRecs].slice(0, 5);

  // Pad if needed
  while (topRecommendations.length < 3) {
    topRecommendations.push('Continue publishing high-quality, original content on a consistent schedule.');
  }

  const summary = overallScore >= 80
    ? `${domain} shows strong AI visibility foundations with a score of ${overallScore}/100. The site has good crawler access and structured data, positioning it well for AI search citations.`
    : overallScore >= 60
      ? `${domain} has moderate AI visibility (${overallScore}/100). Some important signals are present but there are gaps in structured data, E-E-A-T, or AI-specific readiness that should be addressed.`
      : `${domain} has weak AI visibility (${overallScore}/100). The site lacks key signals that AI systems use to discover, understand, and cite content. Significant improvements are recommended.`;

  return { overallScore, grade, categories, summary, topRecommendations };
}
