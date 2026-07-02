export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimi } from '../../lib/kimi';

interface CrawlerRule {
  crawler: string;
  allowed: boolean;
  description: string;
  organization: string;
}

interface SiteSection {
  path: string;
  label: string;
  count: number;
  suggested: 'allow' | 'disallow' | 'review';
}

interface SiteAnalysis {
  title: string;
  metaDescription: string;
  detectedTypes: { type: string; confidence: number }[];
  sitemapFound: string | null;
  sitemapUrls: string[];
  siteSections: SiteSection[];
  robotsTxtFound: boolean;
  robotsTxtRules: { userAgent: string; allow: string[]; disallow: string[] }[];
  pageCount: number;
}

interface ValidationResult {
  status: 'valid' | 'warnings' | 'errors';
  warnings: string[];
  errors: string[];
}

interface LLMsTxtResponse {
  ok: boolean;
  data?: {
    siteAnalysis: SiteAnalysis;
    crawlerRules: CrawlerRule[];
    llmsTxt: string;
    validation: ValidationResult;
    templateUsed: string;
  };
  error?: string;
}

const AI_CRAWLERS: CrawlerRule[] = [
  { crawler: 'GPTBot', allowed: true, description: 'OpenAI GPT crawler — indexes content for ChatGPT and GPT models', organization: 'OpenAI' },
  { crawler: 'ClaudeBot', allowed: true, description: 'Anthropic Claude crawler — indexes content for Claude AI assistant', organization: 'Anthropic' },
  { crawler: 'ChatGPT-User', allowed: true, description: 'ChatGPT browser plugin — used when users browse with ChatGPT', organization: 'OpenAI' },
  { crawler: 'OAI-SearchBot', allowed: true, description: 'OpenAI Search crawler — indexes for OpenAI search products', organization: 'OpenAI' },
  { crawler: ' anthropic-ai', allowed: true, description: 'Anthropic AI crawler — general Anthropic content indexing', organization: 'Anthropic' },
  { crawler: 'PerplexityBot', allowed: true, description: 'Perplexity AI crawler — indexes for Perplexity search engine', organization: 'Perplexity' },
  { crawler: 'Google-Extended', allowed: true, description: 'Google AI crawler — indexes for Gemini and Bard', organization: 'Google' },
  { crawler: 'GoogleBot', allowed: true, description: 'Google web crawler — general search indexing (also used for AI)', organization: 'Google' },
  { crawler: 'Bingbot', allowed: true, description: 'Microsoft Bing crawler — general search indexing', organization: 'Microsoft' },
  { crawler: 'CCBot', allowed: true, description: 'Common Crawl — open web corpus used by many AI systems', organization: 'Common Crawl' },
  { crawler: 'FacebookBot', allowed: true, description: 'Meta AI crawler — indexes for Meta AI products', organization: 'Meta' },
  { crawler: 'Applebot', allowed: true, description: 'Apple Intelligence crawler — indexes for Apple AI features', organization: 'Apple' },
  { crawler: 'ImagesiftBot', allowed: true, description: 'Image search crawler — indexes images for AI training', organization: 'Imagesift' },
  { crawler: 'YouBot', allowed: true, description: 'You.com crawler — indexes for You.com AI search', organization: 'You.com' },
  { crawler: 'Cohere-ai', allowed: true, description: 'Cohere AI crawler — indexes for Cohere language models', organization: 'Cohere' },
  { crawler: 'Diffbot', allowed: true, description: 'Diffbot knowledge graph — structured data extraction', organization: 'Diffbot' },
  { crawler: 'Amazonbot', allowed: true, description: 'Amazon AI crawler — indexes for Alexa and Amazon AI', organization: 'Amazon' },
  { crawler: 'Bytespider', allowed: true, description: 'ByteDance/TikTok crawler — indexes for TikTok AI features', organization: 'ByteDance' },
  { crawler: 'Claude-Web', allowed: true, description: 'Anthropic web crawler — general web indexing for Claude', organization: 'Anthropic' },
  { crawler: 'SnapchatBot', allowed: true, description: 'Snapchat AI crawler — indexes for Snap AI features', organization: 'Snap' },
];

const TEMPLATE_PRESETS: Record<string, { allow: string[]; disallow: string[]; attribution: string; label: string }> = {
  'allow-all': { allow: ['/'], disallow: [], attribution: 'optional', label: 'Allow All AI Crawlers' },
  'block-all': { allow: [], disallow: ['/'], attribution: 'required', label: 'Block All AI Crawlers' },
  'allow-blog-only': { allow: ['/blog/', '/articles/', '/guides/', '/resources/'], disallow: ['/admin/', '/private/', '/account/', '/checkout/', '/cart/'], attribution: 'required', label: 'Allow Blog Content Only' },
  'allow-public-only': { allow: ['/'], disallow: ['/admin/', '/private/', '/account/', '/checkout/', '/cart/', '/api/'], attribution: 'optional', label: 'Allow Public Pages Only' },
  'custom': { allow: ['/'], disallow: [], attribution: 'optional', label: 'Custom — Full Control' },
};

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: {
    url?: string;
    template?: string;
    email?: string;
    companyName?: string;
    description?: string;
    contentTypes?: string[];
    attribution?: string;
    includePolicy?: boolean;
    includeRateLimit?: boolean;
    customAllowPaths?: string[];
    customDisallowPaths?: string[];
  };

  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: 'Invalid request body' }, 400);
  }

  let url = body.url?.trim() || '';
  const template = body.template || 'allow-public-only';
  const email = body.email?.trim() || '';
  const companyName = body.companyName?.trim() || '';
  const description = body.description?.trim() || '';
  const contentTypes = body.contentTypes || [];
  const attribution = body.attribution || 'optional';
  const includePolicy = body.includePolicy ?? false;
  const includeRateLimit = body.includeRateLimit ?? false;
  const customAllowPaths = body.customAllowPaths || [];
  const customDisallowPaths = body.customDisallowPaths || [];

  if (!url) {
    return json({ ok: false, error: 'URL is required' }, 400);
  }

  // Normalize URL
  if (!/^https?:\/\//i.test(url)) {
    url = 'https://' + url;
  }

  let parsedUrl: URL;
  try {
    parsedUrl = new URL(url);
  } catch {
    return json({ ok: false, error: 'Invalid URL format' }, 400);
  }

  const origin = parsedUrl.origin;
  const domain = parsedUrl.hostname;

  // ── Parallel data collection ───────────────────────────────
  const [homepageResult, sitemapResult, robotsResult] = await Promise.all([
    fetchHomepage(origin),
    fetchAndParseSitemap(origin),
    fetchRobotsTxt(origin),
  ]);

  // ── Build site analysis ────────────────────────────────────
  const siteAnalysis = buildSiteAnalysis(homepageResult, sitemapResult, robotsResult, domain);

  // ── Generate llms.txt ──────────────────────────────────────
  const llmsTxt = await generateLLMsTxt({
    origin,
    domain,
    siteAnalysis,
    template,
    homepageResult,
    email,
    companyName,
    description,
    contentTypes,
    attribution,
    includePolicy,
    includeRateLimit,
    customAllowPaths,
    customDisallowPaths,
  });

  // ── Validate ───────────────────────────────────────────────
  const validation = validateLLMsTxt(llmsTxt, email);

  // ── Build crawler rules ────────────────────────────────────
  const crawlerRules = buildCrawlerRules(template);

  return json({
    ok: true,
    data: {
      siteAnalysis,
      crawlerRules,
      llmsTxt,
      validation,
      templateUsed: template,
    },
  } as LLMsTxtResponse, 200);
};

// ── Fetch helpers ──────────────────────────────────────────────

async function fetchHomepage(origin: string): Promise<{
  ok: boolean;
  html: string;
  title: string;
  metaDescription: string;
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

    if (!res.ok) return { ok: false, html: '', title: '', metaDescription: '' };

    const html = await res.text();
    const titleMatch = html.match(/<title[^>]*>([^<]*)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : '';

    const metaDescMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']*)["'][^>]*>/i)
      || html.match(/<meta[^>]*content=["']([^"']*)["'][^>]*name=["']description["'][^>]*>/i)
      || html.match(/<meta[^>]*property=["']og:description["'][^>]*content=["']([^"']*)["'][^>]*>/i);
    const metaDescription = metaDescMatch ? metaDescMatch[1].trim() : '';

    return { ok: true, html, title, metaDescription };
  } catch {
    return { ok: false, html: '', title: '', metaDescription: '' };
  }
}

async function fetchAndParseSitemap(origin: string): Promise<{
  ok: boolean;
  url: string;
  urls: string[];
}> {
  const sitemapUrls = [
    `${origin}/sitemap.xml`,
    `${origin}/sitemap_index.xml`,
    `${origin}/sitemap-index.xml`,
  ];

  for (const url of sitemapUrls) {
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 10000);
      const res = await fetch(url, {
        signal: controller.signal,
        headers: { 'User-Agent': 'Mozilla/5.0 (compatible; theStaccBot/1.0)' },
      });
      clearTimeout(timer);

      if (res.ok) {
        const text = await res.text();
        if (text.includes('<urlset') || text.includes('<sitemapindex')) {
          // Extract URLs from sitemap
          const urlMatches = text.match(/<loc>([^<]+)<\/loc>/g);
          const urls = urlMatches
            ? urlMatches.map(m => m.replace(/<\/?loc>/g, '')).filter(u => u.startsWith('http'))
            : [];
          return { ok: true, url, urls };
        }
      }
    } catch {
      // Try next
    }
  }

  return { ok: false, url: '', urls: [] };
}

async function fetchRobotsTxt(origin: string): Promise<{
  ok: boolean;
  content: string;
  rules: { userAgent: string; allow: string[]; disallow: string[] }[];
}> {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 10000);
    const res = await fetch(`${origin}/robots.txt`, {
      signal: controller.signal,
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; theStaccBot/1.0)' },
    });
    clearTimeout(timer);

    if (!res.ok) return { ok: false, content: '', rules: [] };

    const content = await res.text();
    const rules = parseRobotsTxt(content);
    return { ok: true, content, rules };
  } catch {
    return { ok: false, content: '', rules: [] };
  }
}

function parseRobotsTxt(content: string): { userAgent: string; allow: string[]; disallow: string[] }[] {
  const rules: { userAgent: string; allow: string[]; disallow: string[] }[] = [];
  const lines = content.split('\n');
  let currentRule: { userAgent: string; allow: string[]; disallow: string[] } | null = null;

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;

    const lower = line.toLowerCase();
    if (lower.startsWith('user-agent:')) {
      const ua = line.substring(lower.indexOf(':') + 1).trim();
      currentRule = { userAgent: ua, allow: [], disallow: [] };
      rules.push(currentRule);
    } else if (lower.startsWith('allow:') && currentRule) {
      currentRule.allow.push(line.substring(lower.indexOf(':') + 1).trim());
    } else if (lower.startsWith('disallow:') && currentRule) {
      currentRule.disallow.push(line.substring(lower.indexOf(':') + 1).trim());
    }
  }

  return rules;
}

// ── Site analysis ──────────────────────────────────────────────

function buildSiteAnalysis(
  homepage: { ok: boolean; html: string; title: string; metaDescription: string },
  sitemap: { ok: boolean; url: string; urls: string[] },
  robots: { ok: boolean; content: string; rules: { userAgent: string; allow: string[]; disallow: string[] }[] },
  domain: string
): SiteAnalysis {
  const detectedTypes: { type: string; confidence: number }[] = [];
  const html = homepage.html.toLowerCase();
  const meta = (homepage.metaDescription || '').toLowerCase();

  // Detect site type from sitemap URL patterns (most reliable)
  const urlPatterns: Record<string, { patterns: RegExp[]; keywords: string[] }> = {
    blog: { patterns: [/(?:^|\/)(?:blog|articles?|posts?|news|stories)(?:\/|$)/i], keywords: ['blog', 'article', 'post', 'newsletter'] },
    ecommerce: { patterns: [/(?:^|\/)(?:product|shop|store|cart|checkout|catalog)(?:\/|$)/i], keywords: ['product', 'shop', 'buy', 'price', 'cart', 'store'] },
    saas: { patterns: [/(?:^|\/)(?:pricing|features|api|docs|documentation|app|dashboard)(?:\/|$)/i], keywords: ['saas', 'software', 'platform', 'pricing', 'signup', 'trial'] },
    portfolio: { patterns: [/(?:^|\/)(?:portfolio|work|projects?|gallery|case-studies)(?:\/|$)/i], keywords: ['portfolio', 'work', 'project', 'gallery'] },
    documentation: { patterns: [/(?:^|\/)(?:docs|documentation|guides?|tutorials?|api|reference)(?:\/|$)/i], keywords: ['documentation', 'guide', 'tutorial', 'api reference'] },
    news: { patterns: [/(?:^|\/)(?:news|press|media|category)(?:\/|$)/i], keywords: ['news', 'media', 'press'] },
  };

  // Count URLs matching each pattern
  const patternCounts: Record<string, number> = {};
  for (const sitemapUrl of sitemap.urls) {
    for (const [type, config] of Object.entries(urlPatterns)) {
      for (const pattern of config.patterns) {
        if (pattern.test(sitemapUrl)) {
          patternCounts[type] = (patternCounts[type] || 0) + 1;
        }
      }
    }
  }

  // Score each type based on URL patterns + HTML content + meta description
  const scores: Record<string, number> = {};
  for (const [type, config] of Object.entries(urlPatterns)) {
    let score = 0;
    // URL pattern matches (up to 5 points)
    score += Math.min((patternCounts[type] || 0) * 0.5, 5);
    // HTML keyword matches (up to 3 points)
    for (const kw of config.keywords) {
      if (html.includes(kw)) score += 0.5;
    }
    score = Math.min(score, 3);
    // Meta description matches (up to 2 points)
    for (const kw of config.keywords) {
      if (meta.includes(kw)) score += 0.3;
    }
    score = Math.min(score, 2);
    scores[type] = score;
  }

  // Sort by score and only include types with reasonable confidence
  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  for (const [type, score] of sorted) {
    if (score >= 1.5) {
      detectedTypes.push({ type, confidence: Math.min(score / 5, 0.99) });
    }
  }

  // Default if nothing detected
  if (detectedTypes.length === 0) {
    detectedTypes.push({ type: 'website', confidence: 0.5 });
  }

  // Detect site sections from sitemap URLs
  const siteSections = detectSiteSections(sitemap.urls, detectedTypes.map(d => d.type));

  return {
    title: homepage.title || domain,
    metaDescription: homepage.metaDescription,
    detectedTypes,
    sitemapFound: sitemap.ok ? sitemap.url : null,
    sitemapUrls: sitemap.urls.slice(0, 50), // Limit for response size
    siteSections,
    robotsTxtFound: robots.ok,
    robotsTxtRules: robots.rules.slice(0, 10),
    pageCount: sitemap.ok ? sitemap.urls.length : null,
  };
}

function detectSiteSections(urls: string[], detectedTypes: string[]): SiteSection[] {
  const sections: Record<string, { label: string; count: number; paths: Set<string> }> = {};

  const sectionPatterns: Record<string, { label: string; patterns: RegExp[] }> = {
    blog: { label: 'Blog / Articles', patterns: [/(?:^|\/)(?:blog|articles?|posts?|stories)(?:\/|$)/i] },
    products: { label: 'Products / Shop', patterns: [/(?:^|\/)(?:product|shop|store|catalog)(?:\/|$)/i] },
    docs: { label: 'Documentation', patterns: [/(?:^|\/)(?:docs|documentation|guides?|tutorials?)(?:\/|$)/i] },
    about: { label: 'About / Company', patterns: [/(?:^|\/)(?:about|company|team|careers?)(?:\/|$)/i] },
    contact: { label: 'Contact', patterns: [/(?:^|\/)(?:contact|support|help)(?:\/|$)/i] },
    resources: { label: 'Resources', patterns: [/(?:^|\/)(?:resources|tools|downloads|whitepapers?)(?:\/|$)/i] },
    api: { label: 'API / Developer', patterns: [/(?:^|\/)(?:api|developers?|swagger|openapi)(?:\/|$)/i] },
    pricing: { label: 'Pricing', patterns: [/(?:^|\/)(?:pricing|plans?|packages?)(?:\/|$)/i] },
    portfolio: { label: 'Portfolio / Work', patterns: [/(?:^|\/)(?:portfolio|work|projects?|gallery)(?:\/|$)/i] },
    news: { label: 'News / Press', patterns: [/(?:^|\/)(?:news|press|media)(?:\/|$)/i] },
  };

  for (const url of urls) {
    try {
      const path = new URL(url).pathname;
      for (const [key, config] of Object.entries(sectionPatterns)) {
        for (const pattern of config.patterns) {
          if (pattern.test(path)) {
            if (!sections[key]) {
              sections[key] = { label: config.label, count: 0, paths: new Set() };
            }
            // Extract the base path
            const match = path.match(new RegExp(`^(.+?)(?:${pattern.source.replace(/\(\?:|\)/g, '').split('|')[0]})/?`));
            const basePath = match ? match[0] : path;
            sections[key].paths.add(basePath);
            sections[key].count++;
            break;
          }
        }
      }
    } catch {
      // Skip invalid URLs
    }
  }

  const result: SiteSection[] = [];
  for (const [key, data] of Object.entries(sections)) {
    const paths = Array.from(data.paths);
    const suggestedPath = paths.sort((a, b) => b.length - a.length)[0] || `/${key}/`;
    const isBlogOrDocs = ['blog', 'docs', 'resources', 'portfolio', 'news'].includes(key);
    const isPrivate = ['admin', 'login', 'account', 'checkout', 'cart'].includes(key);

    result.push({
      path: suggestedPath,
      label: data.label,
      count: data.count,
      suggested: isPrivate ? 'disallow' : isBlogOrDocs ? 'allow' : 'review',
    });
  }

  return result.sort((a, b) => b.count - a.count);
}

// ── LLMs.txt generation ────────────────────────────────────────

interface GenerateOptions {
  origin: string;
  domain: string;
  siteAnalysis: SiteAnalysis;
  template: string;
  homepageResult: { ok: boolean; html: string; title: string; metaDescription: string };
  email: string;
  companyName: string;
  description: string;
  contentTypes: string[];
  attribution: string;
  includePolicy: boolean;
  includeRateLimit: boolean;
  customAllowPaths: string[];
  customDisallowPaths: string[];
}

async function generateLLMsTxt(options: GenerateOptions): Promise<string> {
  // Try Kimi first for smart generation
  const kimiResult = await generateWithKimi(options);
  if (kimiResult) return kimiResult;

  // Fallback to template-based generation
  return generateWithTemplate(options);
}

async function generateWithKimi(options: GenerateOptions): Promise<string | null> {
  const { origin, domain, siteAnalysis, template, email, companyName, description, contentTypes, attribution, includePolicy, includeRateLimit, customAllowPaths, customDisallowPaths } = options;

  const preset = TEMPLATE_PRESETS[template] || TEMPLATE_PRESETS['allow-public-only'];

  // Build detected sections info
  const sectionsInfo = siteAnalysis.siteSections.map(s =>
    `- ${s.label}: ${s.count} pages at ${s.path} (suggest: ${s.suggested})`
  ).join('\n');

  // Build detected types info
  const typesInfo = siteAnalysis.detectedTypes.map(t =>
    `- ${t.type} (confidence: ${Math.round(t.confidence * 100)}%)`
  ).join('\n');

  // Build content types from user
  const userContentTypes = contentTypes.length > 0
    ? contentTypes.join(', ')
    : siteAnalysis.detectedTypes.map(t => t.type).join(', ');

  // Build allow/disallow from template + custom + sections
  const allowPaths = [...new Set([...preset.allow, ...customAllowPaths, ...siteAnalysis.siteSections.filter(s => s.suggested === 'allow').map(s => s.path)])];
  const disallowPaths = [...new Set([...preset.disallow, ...customDisallowPaths])];

  // Add common private paths if not already there
  const commonPrivate = ['/admin/', '/wp-admin/', '/login/', '/account/', '/checkout/', '/cart/', '/api/private/', '/.env', '/config/'];
  for (const p of commonPrivate) {
    if (!allowPaths.some(a => p.startsWith(a)) && !disallowPaths.includes(p)) {
      disallowPaths.push(p);
    }
  }

  const systemPrompt = `You are an expert in AI crawler control and web standards. Generate a professional, comprehensive llms.txt file.

The llms.txt format rules:
- Start with a clear header: # llms.txt for [Site Name]
- Include a generated-by line with timestamp
- Include a Description section explaining what the site is
- Include Content Policy section describing what content is available
- User-agent rules for each major AI crawler (specific rules, not just wildcard)
- Allow/Disallow rules that are specific and meaningful
- Attribution directive
- Sitemap URL
- Contact email (real email, never a placeholder)
- Optional: Rate Limiting notes, Content Policy details
- Use clear section comments
- Keep formatting clean and professional
- Do NOT use placeholder emails like admin@example.com or admin@domain
- If no real email is provided, omit the Contact line entirely rather than use a placeholder`;

  const userPrompt = `Generate a comprehensive llms.txt file for ${domain}.

SITE INFORMATION:
- Domain: ${domain}
- Origin: ${origin}
${companyName ? `- Company/Organization: ${companyName}` : ''}
${description ? `- Description: ${description}` : ''}
- Site Title: ${siteAnalysis.title}
${siteAnalysis.metaDescription ? `- Meta Description: ${siteAnalysis.metaDescription}` : ''}

DETECTED SITE TYPES:
${typesInfo || '- General website'}

DETECTED SITE SECTIONS (from sitemap analysis):
${sectionsInfo || '- No sections detected from sitemap'}

CONTENT TYPES ON THIS SITE: ${userContentTypes}

TEMPLATE: ${preset.label}
Allow paths: ${allowPaths.join(', ') || 'All pages'}
Disallow paths: ${disallowPaths.join(', ') || 'None'}
Attribution: ${attribution}

${email ? `- Contact email: ${email}` : '- No contact email provided — omit Contact line'}
${includePolicy ? '- Include detailed Content Policy section' : ''}
${includeRateLimit ? '- Include Rate Limiting guidance section' : ''}

SITEMAP: ${siteAnalysis.sitemapFound || 'Not found'}
ROBOTS.TXT: ${siteAnalysis.robotsTxtFound ? 'Found' : 'Not found'}

Generate a professional llms.txt file. Make it detailed and specific — not a generic template. Include:
1. Header with site name and generation info
2. Description of what the site offers
3. Content sections with descriptions of what's in each allowed path
4. Specific User-agent rules for each major crawler (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot, Bingbot, etc.)
5. Allow/Disallow rules that reference actual site sections
6. Attribution directive
7. Sitemap URL
8. ${email ? `Contact: ${email}` : 'No contact line (email not provided)'}
${includePolicy ? '9. Content Policy section explaining how AI systems may use the content' : ''}
${includeRateLimit ? `${includePolicy ? '10' : '9'}. Rate Limiting guidance` : ''}

Output ONLY the raw llms.txt content. No markdown code fences. No explanations. Just the file content.`;

  const result = await callKimi({
    systemPrompt,
    userPrompt,
    maxTokens: 2500,
    temperature: 0.3,
    timeoutMs: 30000,
  });

  if (!result) return null;

  // Clean up the result
  let cleaned = result
    .replace(/```[\w]*\n?/g, '')
    .replace(/```\n?/g, '')
    .trim();

  // Replace any placeholder emails if user provided a real one
  if (email) {
    cleaned = cleaned.replace(/admin@(?:example\.com|domain\.com|domain)/g, email);
  }

  return cleaned;
}

function generateWithTemplate(options: GenerateOptions): string {
  const { origin, domain, siteAnalysis, template, email, companyName, description, contentTypes, attribution, includePolicy, includeRateLimit } = options;
  const preset = TEMPLATE_PRESETS[template] || TEMPLATE_PRESETS['allow-public-only'];

  const siteName = companyName || siteAnalysis.title || domain;
  const today = new Date().toISOString().split('T')[0];

  // Build allow/disallow from sections + template
  const allowPaths = [...new Set([...preset.allow, ...siteAnalysis.siteSections.filter(s => s.suggested === 'allow').map(s => s.path)])];
  const disallowPaths = [...new Set([...preset.disallow])];

  // Add common private paths
  const commonPrivate = ['/admin/', '/wp-admin/', '/login/', '/account/', '/checkout/', '/cart/', '/api/private/', '/.env'];
  for (const p of commonPrivate) {
    if (!allowPaths.some(a => p.startsWith(a)) && !disallowPaths.includes(p)) {
      disallowPaths.push(p);
    }
  }

  const lines: string[] = [
    `# llms.txt for ${siteName}`,
    `# ${domain}`,
    `# Generated by theStacc LLMs.txt Generator — ${origin}`,
    `# Last updated: ${today}`,
    `# Standard: llms.txt (AI Crawler Control)`,
    '',
    `################################################################################`,
    `# DESCRIPTION`,
    `################################################################################`,
    '',
  ];

  const siteDesc = description || siteAnalysis.metaDescription || `${siteName} is a ${siteAnalysis.detectedTypes.map(t => t.type).join(', ')} website.`;
  lines.push(`# ${siteDesc}`);

  if (siteAnalysis.pageCount) {
    lines.push(`# Total pages indexed: ${siteAnalysis.pageCount}`);
  }

  const primaryTypes = siteAnalysis.detectedTypes.filter(t => t.confidence >= 0.5).map(t => t.type);
  if (primaryTypes.length > 0) {
    lines.push(`# Primary content: ${primaryTypes.join(', ')}`);
  }

  lines.push('');

  // Content sections
  if (siteAnalysis.siteSections.length > 0) {
    lines.push(`################################################################################`);
    lines.push(`# CONTENT SECTIONS`);
    lines.push(`################################################################################`);
    lines.push('');

    for (const section of siteAnalysis.siteSections) {
      const status = section.suggested === 'allow' ? 'Available' : section.suggested === 'disallow' ? 'Restricted' : 'Review';
      lines.push(`# ${section.label}: ${section.count} pages at ${section.path} [${status}]`);
    }
    lines.push('');
  }

  // Content Policy
  if (includePolicy) {
    lines.push(`################################################################################`);
    lines.push(`# CONTENT POLICY`);
    lines.push(`################################################################################`);
    lines.push('');
    lines.push('# This website contains the following types of content:');
    const allTypes = contentTypes.length > 0 ? contentTypes : primaryTypes;
    for (const type of allTypes) {
      lines.push(`# - ${capitalize(type)} content`);
    }
    lines.push(`# AI systems may use this content for training and indexing purposes.`);
    if (attribution === 'required') {
      lines.push(`# Attribution is REQUIRED when using this content in AI-generated responses.`);
    } else if (attribution === 'optional') {
      lines.push(`# Attribution is appreciated but not required.`);
    }
    lines.push('');
  }

  // General rules
  if (allowPaths.length > 0 || disallowPaths.length > 0) {
    lines.push(`################################################################################`);
    lines.push(`# GENERAL CRAWLER RULES`);
    lines.push(`################################################################################`);
    lines.push('');
    lines.push('User-agent: *');
    for (const path of allowPaths) {
      lines.push(`Allow: ${path}`);
    }
    for (const path of disallowPaths) {
      lines.push(`Disallow: ${path}`);
    }
    lines.push('');
  }

  // Specific AI crawler rules
  lines.push(`################################################################################`);
  lines.push(`# AI CRAWLER-SPECIFIC RULES`);
  lines.push(`################################################################################`);
  lines.push('');

  const importantCrawlers = [
    { name: 'GPTBot', org: 'OpenAI', desc: 'OpenAI GPT models and ChatGPT' },
    { name: 'ClaudeBot', org: 'Anthropic', desc: 'Claude AI assistant' },
    { name: 'PerplexityBot', org: 'Perplexity', desc: 'Perplexity AI search engine' },
    { name: 'Google-Extended', org: 'Google', desc: 'Google AI and Gemini' },
    { name: 'GoogleBot', org: 'Google', desc: 'Google Search' },
    { name: 'Bingbot', org: 'Microsoft', desc: 'Bing Search' },
    { name: 'CCBot', org: 'Common Crawl', desc: 'Open web corpus for AI training' },
    { name: 'FacebookBot', org: 'Meta', desc: 'Meta AI products' },
    { name: 'Applebot', org: 'Apple', desc: 'Apple Intelligence' },
  ];

  for (const crawler of importantCrawlers) {
    lines.push(`# ${crawler.name} — ${crawler.desc} (${crawler.org})`);
    lines.push(`User-agent: ${crawler.name}`);
    for (const path of allowPaths) {
      lines.push(`Allow: ${path}`);
    }
    for (const path of disallowPaths) {
      lines.push(`Disallow: ${path}`);
    }
    lines.push('');
  }

  // Rate limiting
  if (includeRateLimit) {
    lines.push(`################################################################################`);
    lines.push(`# RATE LIMITING`);
    lines.push(`################################################################################`);
    lines.push('');
    lines.push('# Please respect the following crawl rate limits:');
    lines.push('# - Maximum 1 request per second per crawler');
    lines.push('# - Crawl-delay: 1 second between requests');
    lines.push('# - For high-volume crawling, contact the site owner');
    lines.push('Crawl-delay: 1');
    lines.push('');
  }

  // Attribution
  lines.push(`################################################################################`);
  lines.push(`# ATTRIBUTION`);
  lines.push(`################################################################################`);
  lines.push('');
  if (attribution === 'required') {
    lines.push('Attribution: required');
    lines.push('# Please cite this website when using our content in AI-generated responses');
    lines.push('# Include the site name, URL, and date of access');
  } else if (attribution === 'none') {
    lines.push('Attribution: none');
    lines.push('# No attribution required');
  } else {
    lines.push('Attribution: optional');
    lines.push('# Attribution is appreciated but not required');
  }
  lines.push('');

  // Sitemap
  if (siteAnalysis.sitemapFound) {
    lines.push(`################################################################################`);
    lines.push(`# SITEMAP`);
    lines.push(`################################################################################`);
    lines.push('');
    lines.push(`Sitemap: ${siteAnalysis.sitemapFound}`);
    lines.push('');
  }

  // Contact
  if (email && !email.includes('example.com') && !email.includes('domain.com')) {
    lines.push(`################################################################################`);
    lines.push(`# CONTACT`);
    lines.push(`################################################################################`);
    lines.push('');
    lines.push(`# For questions about crawler access or content usage:`);
    lines.push(`Contact: ${email}`);
    lines.push('');
  }

  // Footer
  lines.push(`################################################################################`);
  lines.push(`# END OF llms.txt`);
  lines.push(`################################################################################`);

  return lines.join('\n');
}

// ── Validation ─────────────────────────────────────────────────

function validateLLMsTxt(content: string, email: string): ValidationResult {
  const warnings: string[] = [];
  const errors: string[] = [];

  if (!content.includes('User-agent:')) {
    errors.push('Missing User-agent directive');
  }

  if (!content.includes('Allow:') && !content.includes('Disallow:')) {
    warnings.push('No Allow or Disallow rules found');
  }

  if (!content.includes('Sitemap:')) {
    warnings.push('Sitemap URL not included — add your sitemap for better crawlability');
  }

  // Check for placeholder emails
  if (content.includes('admin@example.com') || content.includes('admin@domain.com') || content.includes('admin@domain')) {
    errors.push('Placeholder email detected — replace with your actual contact email');
  }

  // Check if contact email is provided
  const hasContact = content.match(/Contact:\s*\S+@\S+/);
  if (!hasContact && email) {
    warnings.push('Your email was provided but not included in the file — check the output');
  } else if (!hasContact && !email) {
    warnings.push('No contact email included — consider adding one for crawler communication');
  }

  // Check for description
  if (!content.toLowerCase().includes('description') && !content.match(/^# .+/m)) {
    warnings.push('No site description found — add a brief description of your site');
  }

  // Check file length
  if (content.length < 200) {
    warnings.push('File is very short — consider adding more detail about your content and policies');
  }

  // Check for multiple User-agent blocks
  const uaBlocks = (content.match(/User-agent:/g) || []).length;
  if (uaBlocks < 2) {
    warnings.push('Only one User-agent block found — consider adding specific rules for major AI crawlers');
  }

  // Check for attribution
  if (!content.toLowerCase().includes('attribution')) {
    warnings.push('No attribution directive found — consider specifying your attribution preferences');
  }

  const status = errors.length > 0 ? 'errors' : warnings.length > 0 ? 'warnings' : 'valid';

  return { status, warnings, errors };
}

// ── Crawler rules builder ──────────────────────────────────────

function buildCrawlerRules(template: string): CrawlerRule[] {
  const preset = TEMPLATE_PRESETS[template];
  const isBlocking = preset && preset.disallow.includes('/');

  return AI_CRAWLERS.map(c => ({
    ...c,
    allowed: !isBlocking,
  }));
}

// ── Helpers ────────────────────────────────────────────────────

function capitalize(str: string): string {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}
