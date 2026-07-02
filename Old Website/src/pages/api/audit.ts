export const prerender = false;

import type { APIRoute } from 'astro';

/* ═══════════════════════════════════════════════════════════════
   Server-Side SEO Audit API  —  v3.0 with DataForSEO authority data
   Improvements over v2:
     1. Real Domain Rating (DR) from DataForSEO backlink profile
     2. Live backlink count, referring domains, referring IPs
     3. Organic traffic estimate + top ranking keywords
     4. Authority & Backlinks scoring category (10 pts)
     5. All previous v2 features preserved
   ═══════════════════════════════════════════════════════════════ */

import { getBacklinksSummary, getRankedKeywords } from '../../lib/dataforseo';

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY || '';
const ANTHROPIC_BASE_URL = (process.env.ANTHROPIC_BASE_URL || 'https://api.anthropic.com').replace(/\/+$/, '');
const ANTHROPIC_MODEL = process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-6';

const PAGESPEED_API_KEY = process.env.PAGESPEED_API_KEY || '';

/* ── Simple in-memory LRU cache ── */
interface CacheEntry { data: AuditResult; expiresAt: number }
const cache = new Map<string, CacheEntry>();
const CACHE_TTL_MS = 60 * 60 * 1000;
const MAX_CACHE_SIZE = 100;

function getCached(domain: string): AuditResult | null {
  const entry = cache.get(domain);
  if (!entry) return null;
  if (Date.now() > entry.expiresAt) { cache.delete(domain); return null; }
  return entry.data;
}
function setCached(domain: string, data: AuditResult) {
  if (cache.size >= MAX_CACHE_SIZE) {
    const first = cache.keys().next().value;
    if (first) cache.delete(first);
  }
  cache.set(domain, { data, expiresAt: Date.now() + CACHE_TTL_MS });
}

/* ── Types ── */
interface Check {
  name: string;
  points: number;
  maxPoints: number;
  passed: boolean;
  severity: 'critical' | 'high' | 'medium' | 'low';
  detail: string;
  fix: string | null;
  staccFeature?: string;
  staccCta?: string;
  staccLink?: string;
}
interface Category {
  name: string;
  score: number;
  maxScore: number;
  checks: Check[];
}
interface Priority {
  title: string;
  impact: string;
  fix: string;
}
interface StaccRecommendation {
  finding: string;
  feature: string;
  cta: string;
  link: string;
}
interface PageData {
  url: string;
  status: number;
  title: string;
  titleLength: number;
  metaDescription: string;
  metaDescLength: number;
  h1s: string[];
  h2s: string[];
  h3s: string[];
  images: { src: string; alt: string }[];
  imageCount: number;
  altCoverage: number;
  internalLinks: number;
  externalLinks: number;
  wordCount: number;
  canonical: string;
  schemaTypes: string[];
  jsonLd: any[];
  ogTags: Record<string, string>;
  twitterCards: Record<string, string>;
  hreflang: { url: string; lang: string }[];
  viewport: string | null;
  robotsMeta: string;
  hasBreadcrumbSchema: boolean;
  hasWebsiteSchema: boolean;
  hasPersonSchema: boolean;
  hasVideoSchema: boolean;
}
interface AnalyticsResult {
  ga4: boolean;
  gtm: boolean;
  facebookPixel: boolean;
  linkedInInsight: boolean;
  hotjar: boolean;
  clarity: boolean;
  googleAds: boolean;
  details: string[];
}
interface SecurityResult {
  hsts: boolean;
  csp: boolean;
  xFrameOptions: boolean;
  xContentTypeOptions: boolean;
  strictTransportSecurity: string | null;
  details: string[];
}
interface SitewidePatterns {
  duplicateTitles: string[];
  duplicateMetaDescriptions: string[];
  pagesWithNoH1: number;
  pagesWithMultipleH1s: number;
  totalPagesCrawled: number;
  pagesWithErrors: { url: string; status: number }[];
  averageWordsPerPage: number;
  totalImagesAcrossSite: number;
  averageAltCoverage: number;
}
interface CompetitorInfo {
  name: string;
  domain: string;
  note: string;
}
interface KimiAnalysis {
  contentQualityScore: number;
  contentQualityNotes: string;
  seoGaps: string[];
  businessType: string;
  topRecommendations: string[];
  staccFeatureMatches: { feature: string; reason: string; link: string }[];
  competitors: CompetitorInfo[];
  estimatedContentGap: string;
}
interface RobotsResult {
  aiCrawlerBlocks: string[];
  crawlDelay: number | null;
  disallowedPaths: string[];
  hasSitemapRef: boolean;
}
interface CmsResult {
  cms: string | null;
  hosting: string | null;
  techStack: string[];
}
interface EeatResult {
  eeatScore: number;
  eeatDetails: string[];
  hasTestimonials: boolean;
  hasTeamPage: boolean;
  hasReviews: boolean;
}
interface LocalResult {
  localScore: number;
  localDetails: string[];
  hasGbpLink: boolean;
}
interface FreshnessResult {
  oldestDate: string | null;
  newestDate: string | null;
  averageAgeDays: number | null;
  orphanPages: string[];
  contentFreshness: 'fresh' | 'stale' | 'very-stale' | 'unknown';
}
interface SocialTagsResult {
  ogTitle: string | null;
  ogDescription: string | null;
  ogImage: string | null;
  ogType: string | null;
  ogUrl: string | null;
  twitterCard: string | null;
  twitterTitle: string | null;
  twitterDescription: string | null;
  twitterImage: string | null;
  hasAllEssential: boolean;
}
interface RedirectChainResult {
  chain: string[];
  isLoop: boolean;
  chainLength: number;
}
interface MixedContentResult {
  mixedResources: string[];
  hasMixedContent: boolean;
}
interface Soft404Result {
  soft404s: { url: string; wordCount: number; reason: string }[];
  count: number;
}
interface HreflangResult {
  tags: { url: string; lang: string }[];
  hasXDefault: boolean;
  issues: string[];
}
interface LlmsTxtResult {
  exists: boolean;
  content: string | null;
  hasNoTrain: boolean;
  hasAttribution: boolean;
}
interface PassageResult {
  avgPassageLength: number;
  hasDirectAnswers: boolean;
  directAnswerCount: number;
  questionHeadingCount: number;
  structureScore: number;
}
interface GeoAioResult {
  llmsTxt: LlmsTxtResult;
  passageStructure: PassageResult;
  brandMentions: { source: string; found: boolean }[];
  entityDensity: number;
  freshnessScore: number;
}
interface AuthorityData {
  dr: number;                    // Domain Rating 0-100
  backlinks: number;             // Total live backlinks
  refDomains: number;            // Referring domains
  refIps: number;                // Referring IPs
  brokenBacklinks: number;       // Broken backlinks
  totalKeywords: number;         // Total ranking keywords
  pos1to3: number;               // Keywords in top 3
  pos4to10: number;              // Keywords in top 10
  pos11to20: number;             // Keywords in positions 11-20
  pos21to50: number;             // Keywords in positions 21-50
  pos51to100: number;            // Keywords in positions 51-100
  estTraffic: number;            // Estimated monthly organic traffic
  topKeywords: Array<{ keyword: string; position: number; volume: number; cpc: number; url: string }>;
  dataAvailable: boolean;        // Whether DataForSEO had data
}
interface AuditResult {
  success: boolean;
  domain: string;
  url: string;
  overallScore: number;
  grade: string;
  businessType: string;
  categories: Category[];
  topPriorities: Priority[];
  staccRecommendations: StaccRecommendation[];
  serpPreview: { title: string; description: string; url: string };
  pageSpeed: { lcp?: number; cls?: number; performance?: number } | null;
  fetchTime: number;
  pagesAudited: number;
  isSPA: boolean;
  spaFramework: string | null;
  analytics: AnalyticsResult;
  security: SecurityResult;
  sitewide: SitewidePatterns;
  competitorHint: string;
  robotsTxt: RobotsResult;
  cms: CmsResult;
  eeat: EeatResult;
  local: LocalResult;
  freshness: FreshnessResult;
  socialTags: SocialTagsResult;
  redirectChain: RedirectChainResult;
  mixedContent: MixedContentResult;
  soft404s: Soft404Result;
  hreflang: HreflangResult;
  geoAio: GeoAioResult;
  authority: AuthorityData;
}

/* ── URL helpers ── */
function normalizeUrl(input: string): { url: string; domain: string } | null {
  let raw = input.trim().toLowerCase();
  if (!raw) return null;
  let domain = raw.replace(/^https?:\/\//, '').replace(/\/+$/, '');
  let url = raw;
  if (!/^https?:\/\//i.test(url)) url = 'https://' + url;
  url = url.replace(/\/+$/, '');
  try { const parsed = new URL(url); return { url: parsed.href, domain: parsed.hostname }; }
  catch { return null; }
}

/* ── Fetch helpers ── */
async function fetchWithTimeout(url: string, timeoutMs = 15000, opts?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...opts, signal: controller.signal });
  } finally { clearTimeout(timer); }
}

async function fetchHTML(url: string): Promise<{ html: string; finalUrl: string; status: number; headers: Headers }> {
  const res = await fetchWithTimeout(url, 15000, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    },
  });
  const html = await res.text();
  return { html, finalUrl: res.url || url, status: res.status, headers: res.headers };
}

async function fetchPageSpeed(url: string): Promise<any> {
  try {
    const keyParam = PAGESPEED_API_KEY ? `&key=${PAGESPEED_API_KEY}` : '';
    const apiUrl = `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${encodeURIComponent(url)}&category=PERFORMANCE&category=ACCESSIBILITY&category=BEST_PRACTICES&category=SEO&strategy=MOBILE${keyParam}`;
    const res = await fetchWithTimeout(apiUrl, 30000);
    if (!res.ok) return null;
    return await res.json();
  } catch { return null; }
}

async function checkFileExists(url: string): Promise<{ exists: boolean; content?: string; status?: number }> {
  try {
    const res = await fetchWithTimeout(url, 8000);
    const content = res.ok ? await res.text() : undefined;
    return { exists: res.ok, content, status: res.status };
  } catch { return { exists: false }; }
}

/* ── Sitemap parser ── */
async function fetchSitemapUrls(baseUrl: string): Promise<string[]> {
  const sitemapUrl = `${new URL(baseUrl).origin}/sitemap.xml`;
  const sitemapIndexUrl = `${new URL(baseUrl).origin}/sitemap_index.xml`;

  // Try sitemap.xml first
  let result = await checkFileExists(sitemapUrl);
  if (!result.exists || !result.content) {
    result = await checkFileExists(sitemapIndexUrl);
  }
  if (!result.exists || !result.content) return [];

  // Verify it's actually XML, not HTML
  const content = result.content.trim();
  if (!content.includes('<urlset') && !content.includes('<sitemapindex')) {
    // Could be an HTML fallback page
    return [];
  }

  const urls: string[] = [];
  const locRegex = /<loc>([^<]+)<\/loc>/gi;
  let match;
  while ((match = locRegex.exec(content)) !== null) {
    try {
      const u = new URL(match[1].trim());
      // Only include same-origin URLs
      if (u.origin === new URL(baseUrl).origin) {
        urls.push(u.href);
      }
    } catch { /* skip invalid URLs */ }
  }

  // Remove duplicates and return
  return [...new Set(urls)];
}

/* ── Multi-page crawler ── */
async function crawlPages(urls: string[], maxPages = 50): Promise<PageData[]> {
  const limited = urls.slice(0, maxPages);
  const promises = limited.map(async (url) => {
    try {
      const { html, status, finalUrl } = await fetchHTML(url);
      const parsed = parsePageHTML(html, finalUrl);
      return { ...parsed, url: finalUrl, status };
    } catch {
      return {
        url, status: 0, title: '', titleLength: 0, metaDescription: '', metaDescLength: 0,
        h1s: [], h2s: [], h3s: [], images: [], imageCount: 0, altCoverage: 0,
        internalLinks: 0, externalLinks: 0, wordCount: 0, canonical: '', schemaTypes: [], jsonLd: [],
        ogTags: {}, twitterCards: {}, hreflang: [], viewport: null, robotsMeta: '',
        hasBreadcrumbSchema: false, hasWebsiteSchema: false, hasPersonSchema: false, hasVideoSchema: false
      };
    }
  });
  return Promise.all(promises);
}

/* ── Per-page HTML parser ── */
function parsePageHTML(rawHtml: string, baseUrl: string): Omit<PageData, 'url' | 'status'> {
  const html = rawHtml;
  const title = (html.match(/<title[^>]*>([^<]*)<\/title>/i)?.[1] || '').trim();
  const metaDescMatch = html.match(/<meta[^>]*name=["']description["'][^>]*>/i);
  let metaDescription = '';
  if (metaDescMatch) { const cm = metaDescMatch[0].match(/content=["']([^"]*)["']/i); metaDescription = cm ? cm[1].trim() : ''; }
  const robotsMetaMatch = html.match(/<meta[^>]*name=["']robots["'][^>]*>/i);
  let robotsMeta = ''; if (robotsMetaMatch) { const cm = robotsMetaMatch[0].match(/content=["']([^"]*)["']/i); robotsMeta = cm ? cm[1].toLowerCase() : ''; }
  const canonicalMatch = html.match(/<link[^>]*rel=["']canonical["'][^>]*>/i);
  let canonical = ''; if (canonicalMatch) { const cm = canonicalMatch[0].match(/href=["']([^"]*)["']/i); canonical = cm ? cm[1] : ''; }

  const h1s: string[] = []; let m;
  const h1r = /<h1[^>]*>([\s\S]*?)<\/h1>/gi;
  while ((m = h1r.exec(html)) !== null) {
    const t = m[1].replace(/<[^>]+>/g, '').trim();
    if (t) h1s.push(t);
  }

  const h2s: string[] = [];
  const h2r = /<h2[^>]*>([\s\S]*?)<\/h2>/gi;
  while ((m = h2r.exec(html)) !== null) {
    const t = m[1].replace(/<[^>]+>/g, '').trim();
    if (t) h2s.push(t);
  }

  const h3s: string[] = [];
  const h3r = /<h3[^>]*>([\s\S]*?)<\/h3>/gi;
  while ((m = h3r.exec(html)) !== null) {
    const t = m[1].replace(/<[^>]+>/g, '').trim();
    if (t) h3s.push(t);
  }

  const imgs: { src: string; alt: string }[] = []; const ir = /<img[^>]*>/gi;
  while ((m = ir.exec(html)) !== null) { const s = m[0].match(/src=["']([^"]*)["']/i); const a = m[0].match(/alt=["']([^"]*)["']/i); imgs.push({ src: s ? s[1] : '', alt: a ? a[1] : '' }); }

  const links: string[] = []; const lr = /<a[^>]*href=["']([^"]*)["'][^>]*>/gi;
  while ((m = lr.exec(html)) !== null) links.push(m[1]);

  const jlr = /<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  const jsonLd: any[] = [];
  while ((m = jlr.exec(html)) !== null) { try { jsonLd.push(JSON.parse(m[1].trim())); } catch { /* skip */ } }

  // Open Graph tags
  const ogTags: Record<string, string> = {};
  const ogR = /<meta[^>]*property=["']og:([^"']*)["'][^>]*>/gi;
  while ((m = ogR.exec(html)) !== null) {
    const contentMatch = m[0].match(/content=["']([^"]*)["']/i);
    if (contentMatch) ogTags[m[1]] = contentMatch[1];
  }

  // Twitter Card tags
  const twitterCards: Record<string, string> = {};
  const twR = /<meta[^>]*name=["']twitter:([^"']*)["'][^>]*>/gi;
  while ((m = twR.exec(html)) !== null) {
    const contentMatch = m[0].match(/content=["']([^"]*)["']/i);
    if (contentMatch) twitterCards[m[1]] = contentMatch[1];
  }

  // Hreflang
  const hreflang: { url: string; lang: string }[] = [];
  const hlR = /<link[^>]*rel=["']alternate["'][^>]*hreflang=["']([^"']*)["'][^>]*>/gi;
  while ((m = hlR.exec(html)) !== null) {
    const hrefMatch = m[0].match(/href=["']([^"]*)["']/i);
    if (hrefMatch) hreflang.push({ lang: m[1], url: hrefMatch[1] });
  }

  // Viewport
  const viewportMatch = html.match(/<meta[^>]*name=["']viewport["'][^>]*>/i);
  let viewport: string | null = null;
  if (viewportMatch) {
    const cm = viewportMatch[0].match(/content=["']([^"]*)["']/i);
    viewport = cm ? cm[1] : null;
  }

  // Schema-specific detection
  let hasBreadcrumbSchema = false;
  let hasWebsiteSchema = false;
  let hasPersonSchema = false;
  let hasVideoSchema = false;
  for (const s of jsonLd) {
    const types = extractSchemaTypes(s);
    if (types.some((t: string) => t.toLowerCase().includes('breadcrumb'))) hasBreadcrumbSchema = true;
    if (types.some((t: string) => t.toLowerCase().includes('website'))) hasWebsiteSchema = true;
    if (types.some((t: string) => t.toLowerCase().includes('person'))) hasPersonSchema = true;
    if (types.some((t: string) => t.toLowerCase().includes('video'))) hasVideoSchema = true;
  }

  function extractSchemaTypes(val: any): string[] {
    const types: string[] = [];
    if (typeof val === 'string') types.push(val);
    else if (Array.isArray(val)) val.forEach(extractSchemaTypes);
    else if (val && typeof val === 'object') {
      if (val['@type']) types.push(val['@type']);
      if (val['@graph']) val['@graph'].forEach(extractSchemaTypes);
    }
    return types;
  }

  const bodyM = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  let bodyText = '', wordCount = 0;
  if (bodyM) {
    bodyText = bodyM[1].replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    wordCount = bodyText.split(/\s+/).filter(w => w.length > 1).length;
  }

  const schemaTypes: string[] = [];
  function collectTypes(val: any) {
    if (typeof val === 'string') schemaTypes.push(val);
    else if (Array.isArray(val)) val.forEach(collectTypes);
  }
  jsonLd.forEach(s => { collectTypes(s['@type']); if (s['@graph']) s['@graph'].forEach((i: any) => collectTypes(i['@type'])); });

  const origin = new URL(baseUrl).origin;
  let internalLinks = 0, externalLinks = 0;
  links.forEach(l => { try { const u = new URL(l, baseUrl); if (u.origin === origin) internalLinks++; else externalLinks++; } catch { internalLinks++; } });

  const imagesWithAlt = imgs.filter(i => i.alt.trim().length > 0).length;
  const altCoverage = imgs.length > 0 ? Math.round((imagesWithAlt / imgs.length) * 100) : 0;

  return {
    title, titleLength: title.length, metaDescription, metaDescLength: metaDescription.length,
    h1s, h2s, h3s, images: imgs, imageCount: imgs.length, altCoverage,
    internalLinks, externalLinks, wordCount, canonical, schemaTypes, jsonLd,
    ogTags, twitterCards, hreflang, viewport, robotsMeta,
    hasBreadcrumbSchema, hasWebsiteSchema, hasPersonSchema, hasVideoSchema
  };
}

/* ── SPA Detection ── */
function detectSPA(html: string): { isSPA: boolean; framework: string | null } {
  const checks = [
    { pattern: /<div\s+id=["']root["']/i, name: 'React/Vite' },
    { pattern: /<div\s+id=["']__next["']/i, name: 'Next.js' },
    { pattern: /<div\s+id=["']__nuxt["']/i, name: 'Nuxt.js' },
    { pattern: /<div\s+id=["']app["']/i, name: 'Vue/Angular' },
    { pattern: /ng-app=/i, name: 'AngularJS' },
    { pattern: /data-reactroot/i, name: 'React' },
    { pattern: /__NEXT_DATA__/i, name: 'Next.js' },
    { pattern: /window\.__NUXT__/i, name: 'Nuxt.js' },
    { pattern: /_nuxt\//i, name: 'Nuxt.js' },
    { pattern: /vite/i, name: 'Vite' },
    { pattern: /manuscdn\.com|manus-analytics|manus-space-dispatcher/i, name: 'Manus AI' },
    { pattern: /wixsite\.com|static\.wixstatic\.com|wix-bolt/i, name: 'Wix' },
    { pattern: /squarespace-cdn\.com|static1\.squarespace\.com/i, name: 'Squarespace' },
    { pattern: /webflow\.io|assets\.website-files\.com/i, name: 'Webflow' },
  ];

  for (const check of checks) {
    if (check.pattern.test(html)) return { isSPA: true, framework: check.name };
  }

  // Check if body has very little content (potential SPA shell)
  const bodyM = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  if (bodyM) {
    const textContent = bodyM[1].replace(/<script[\s\S]*?<\/script>/gi, '').replace(/<style[\s\S]*?<\/style>/gi, '').replace(/<[^>]+>/g, '').replace(/\s+/g, '').trim();
    if (textContent.length < 100) return { isSPA: true, framework: 'Unknown SPA' };
  }

  return { isSPA: false, framework: null };
}

/* ── robots.txt Parser ── */
function parseRobotsTxt(content: string): { aiCrawlerBlocks: string[]; crawlDelay: number | null; disallowedPaths: string[]; hasSitemapRef: boolean } {
  const aiCrawlers = ['GPTBot', 'ChatGPT-User', 'anthropic-ai', 'Claude-Web', 'ClaudeBot', 'PerplexityBot', 'Google-Extended', 'CCBot', 'Bytespider', 'Amazonbot', 'meta-externalagent', 'Applebot-Extended'];
  const aiCrawlerBlocks: string[] = [];
  let crawlDelay: number | null = null;
  const disallowedPaths: string[] = [];
  let hasSitemapRef = false;

  const lines = content.split('\n');
  let currentUserAgent = '*';

  for (const rawLine of lines) {
    const line = rawLine.trim().toLowerCase();
    if (line.startsWith('user-agent:')) {
      currentUserAgent = rawLine.split(':')[1]?.trim().toLowerCase() || '*';
    }
    if (line.startsWith('disallow:')) {
      const path = rawLine.split(':')[1]?.trim() || '';
      if (path) disallowedPaths.push(path);
      // Check if this disallow is for an AI crawler
      const ua = currentUserAgent.toLowerCase();
      for (const crawler of aiCrawlers) {
        if (ua.includes(crawler.toLowerCase()) && path === '/') {
          aiCrawlerBlocks.push(crawler);
        }
      }
    }
    if (line.startsWith('crawl-delay:')) {
      const delay = parseFloat(rawLine.split(':')[1]?.trim() || '0');
      if (!isNaN(delay)) crawlDelay = delay;
    }
    if (line.startsWith('sitemap:')) {
      hasSitemapRef = true;
    }
  }

  return { aiCrawlerBlocks: [...new Set(aiCrawlerBlocks)], crawlDelay, disallowedPaths: [...new Set(disallowedPaths)], hasSitemapRef };
}

/* ── CMS / Technology Detection ── */
function detectCMS(html: string): { cms: string | null; hosting: string | null; techStack: string[] } {
  const techStack: string[] = [];
  let cms: string | null = null;
  let hosting: string | null = null;

  const lower = html.toLowerCase();

  // CMS Detection
  if (lower.includes('wp-content') || lower.includes('wp-json') || lower.includes('/wp-includes/')) {
    cms = 'WordPress';
    techStack.push('WordPress');
  }
  if (lower.includes('wixsite.com') || lower.includes('static.wixstatic.com') || lower.includes('wix-bolt')) {
    cms = 'Wix';
    techStack.push('Wix');
  }
  if (lower.includes('squarespace-cdn.com') || lower.includes('static1.squarespace.com')) {
    cms = 'Squarespace';
    techStack.push('Squarespace');
  }
  if (lower.includes('webflow.io') || lower.includes('assets.website-files.com')) {
    cms = 'Webflow';
    techStack.push('Webflow');
  }
  if (lower.includes('shopify') || lower.includes('cdn.shopify.com') || lower.includes('myshopify.com')) {
    cms = 'Shopify';
    techStack.push('Shopify');
  }
  if (lower.includes('laravel') || lower.includes('csrf-token')) {
    cms = 'Laravel';
    techStack.push('Laravel');
  }
  if (lower.includes('next.js') || lower.includes('__next') || lower.includes('_next/static')) {
    techStack.push('Next.js');
  }
  if (lower.includes('nuxt') || lower.includes('__nuxt') || lower.includes('_nuxt/')) {
    techStack.push('Nuxt.js');
  }
  if (lower.includes('vite') || lower.includes('/@vite/')) {
    techStack.push('Vite');
  }
  if (lower.includes('react') || lower.includes('data-reactroot')) {
    techStack.push('React');
  }
  if (lower.includes('vue') || lower.includes('data-v-')) {
    techStack.push('Vue');
  }
  if (lower.includes('jquery')) {
    techStack.push('jQuery');
  }
  if (lower.includes('bootstrap')) {
    techStack.push('Bootstrap');
  }

  // Hosting Detection
  if (lower.includes('cloudflare')) {
    hosting = 'Cloudflare';
    techStack.push('Cloudflare');
  }
  if (lower.includes('hostinger')) {
    hosting = 'Hostinger';
    techStack.push('Hostinger');
  }
  if (lower.includes('aws') || lower.includes('amazonaws.com')) {
    hosting = 'AWS';
    techStack.push('AWS');
  }
  if (lower.includes('vercel')) {
    hosting = 'Vercel';
    techStack.push('Vercel');
  }
  if (lower.includes('netlify')) {
    hosting = 'Netlify';
    techStack.push('Netlify');
  }

  return { cms, hosting, techStack: [...new Set(techStack)] };
}

/* ── E-E-A-T + Local SEO Detection ── */
function detectEeatAndLocal(html: string, schemaTypes: string[], pages: PageData[]): { eeatScore: number; eeatDetails: string[]; localScore: number; localDetails: string[]; hasTestimonials: boolean; hasTeamPage: boolean; hasReviews: boolean; hasGbpLink: boolean } {
  const lower = html.toLowerCase();
  const eeatDetails: string[] = [];
  const localDetails: string[] = [];

  // E-E-A-T Detection
  const hasTestimonials = lower.includes('testimonial') || lower.includes('what our clients say') || lower.includes('customer reviews');
  const hasTeamPage = pages.some(p => p.url.includes('/team') || p.url.includes('/about'));
  const hasReviews = lower.includes('review') || lower.includes('rating') || lower.includes('stars');
  const hasCaseStudies = lower.includes('case study') || lower.includes('case-study');
  const hasCertifications = lower.includes('certified') || lower.includes('certification') || lower.includes('accredited');
  const hasAuthorBios = lower.includes('author') || lower.includes('written by') || lower.includes('expert');
  const hasSocialProof = lower.includes('trusted by') || lower.includes('as seen on') || lower.includes('featured in');
  const hasContactInfo = lower.includes('phone') || lower.includes('email') || lower.includes('address');

  // Review widget detection
  const hasReviewWidget = lower.includes('trustpilot') || lower.includes('yotpo') || lower.includes('birdeye') || lower.includes('reviews.io') || lower.includes('google reviews');

  // AggregateRating schema
  const hasAggregateRating = schemaTypes.some(t => t.toLowerCase().includes('aggregaterating'));
  const hasReviewSchema = schemaTypes.some(t => t.toLowerCase().includes('review'));

  if (hasTestimonials) eeatDetails.push('Testimonials present');
  if (hasTeamPage) eeatDetails.push('Team/About page found');
  if (hasReviews) eeatDetails.push('Review mentions found');
  if (hasCaseStudies) eeatDetails.push('Case studies present');
  if (hasCertifications) eeatDetails.push('Certifications mentioned');
  if (hasAuthorBios) eeatDetails.push('Author bylines detected');
  if (hasSocialProof) eeatDetails.push('Social proof ("trusted by") found');
  if (hasReviewWidget) eeatDetails.push('Review widget integrated');
  if (hasAggregateRating) eeatDetails.push('AggregateRating schema');
  if (hasReviewSchema) eeatDetails.push('Review schema present');

  let eeatScore = Math.min(100, eeatDetails.length * 12);
  if (eeatDetails.length === 0) eeatDetails.push('Minimal E-E-A-T signals detected');

  // Local SEO Detection
  const hasLocalBusiness = schemaTypes.some(t => t.toLowerCase().includes('localbusiness'));
  const hasPostalAddress = schemaTypes.some(t => t.toLowerCase().includes('postaladdress'));
  const hasGeo = schemaTypes.some(t => t.toLowerCase().includes('geocoordinates'));
  const hasOpeningHours = schemaTypes.some(t => t.toLowerCase().includes('openinghoursspecification'));
  const hasGbpLink = lower.includes('g.page') || lower.includes('business.google.com') || lower.includes('goo.gl/maps') || lower.includes('google.com/maps');

  // Check for location pages
  const hasLocationPages = pages.some(p => p.url.includes('/location') || p.url.includes('/locations'));

  // Check for city/state mentions in titles
  const cityMentions = pages.filter(p => /\b[A-Z][a-z]+,\s*[A-Z]{2}\b/.test(p.title)).length;

  if (hasLocalBusiness) localDetails.push('LocalBusiness schema present');
  if (hasPostalAddress) localDetails.push('PostalAddress in schema');
  if (hasGeo) localDetails.push('GeoCoordinates in schema');
  if (hasOpeningHours) localDetails.push('OpeningHoursSpecification schema');
  if (hasGbpLink) localDetails.push('Google Business Profile link found');
  if (hasLocationPages) localDetails.push('Location pages detected');
  if (cityMentions > 0) localDetails.push(`City mentions in ${cityMentions} page titles`);

  let localScore = Math.min(100, localDetails.length * 15);
  if (localDetails.length === 0) localDetails.push('No local SEO signals detected');

  return { eeatScore, eeatDetails, localScore, localDetails, hasTestimonials, hasTeamPage, hasReviews, hasGbpLink };
}

/* ── Content Freshness + Orphan Detection ── */
function analyzeFreshnessAndOrphans(sitemapContent: string | undefined, pages: PageData[], homepageUrl: string): { lastmodDates: string[]; oldestDate: string | null; newestDate: string | null; orphanPages: string[]; averageAgeDays: number | null } {
  const lastmodDates: string[] = [];
  let oldestDate: string | null = null;
  let newestDate: string | null = null;
  let averageAgeDays: number | null = null;

  if (sitemapContent) {
    const lastmodRegex = /<lastmod>([^<]+)<\/lastmod>/gi;
    let match;
    while ((match = lastmodRegex.exec(sitemapContent)) !== null) {
      const date = match[1].trim();
      lastmodDates.push(date);
    }
  }

  if (lastmodDates.length > 0) {
    const dates = lastmodDates.map(d => new Date(d)).filter(d => !isNaN(d.getTime()));
    if (dates.length > 0) {
      dates.sort((a, b) => a.getTime() - b.getTime());
      oldestDate = dates[0].toISOString().split('T')[0];
      newestDate = dates[dates.length - 1].toISOString().split('T')[0];
      const now = new Date().getTime();
      const totalAge = dates.reduce((sum, d) => sum + (now - d.getTime()), 0);
      averageAgeDays = Math.round(totalAge / dates.length / (1000 * 60 * 60 * 24));
    }
  }

  // Orphan pages: pages in sitemap but not linked from homepage
  const homepageLinks = pages.find(p => p.url.replace(/\/+$/, '') === homepageUrl.replace(/\/+$/, ''))?.internalLinks || 0;
  const orphanPages: string[] = [];
  // Simple heuristic: if a page has 0 internal links (other than self), it's potentially orphaned
  for (const page of pages) {
    if (page.status < 400 && page.internalLinks <= 1 && page.url !== homepageUrl) {
      orphanPages.push(page.url);
    }
  }

  return { lastmodDates, oldestDate, newestDate, orphanPages: orphanPages.slice(0, 10), averageAgeDays };
}

/* ── Analytics Detection ── */
function detectAnalytics(html: string): AnalyticsResult {
  const result: AnalyticsResult = {
    ga4: false, gtm: false, facebookPixel: false, linkedInInsight: false,
    hotjar: false, clarity: false, googleAds: false, details: []
  };

  const lower = html.toLowerCase();

  // GA4 / Google Analytics
  if (lower.includes('gtag') || lower.includes('google-analytics.com/g/') || /G-[A-Z0-9]{10,}/i.test(html)) {
    result.ga4 = true;
    const match = html.match(/G-[A-Z0-9]{8,}/i);
    result.details.push(`GA4 detected${match ? ` (${match[0]})` : ''}`);
  }

  // GTM
  if (lower.includes('googletagmanager.com/gtm.js') || /GTM-[A-Z0-9]{4,}/i.test(html)) {
    result.gtm = true;
    const match = html.match(/GTM-[A-Z0-9]{4,}/i);
    result.details.push(`GTM detected${match ? ` (${match[0]})` : ''}`);
  }

  // Facebook Pixel
  if (lower.includes('fbq(') || lower.includes('facebook.com/tr') || lower.includes('connect.facebook.net')) {
    result.facebookPixel = true;
    result.details.push('Facebook Pixel detected');
  }

  // LinkedIn Insight
  if (lower.includes('snap.licdn.com') || lower.includes('linkedin.com/insight') || /insight\.linkedin\.com/i.test(html)) {
    result.linkedInInsight = true;
    result.details.push('LinkedIn Insight Tag detected');
  }

  // Hotjar
  if (lower.includes('hotjar.com') || lower.includes('hj(')) {
    result.hotjar = true;
    result.details.push('Hotjar detected');
  }

  // Microsoft Clarity
  if (lower.includes('clarity.ms')) {
    result.clarity = true;
    result.details.push('Microsoft Clarity detected');
  }

  // Google Ads
  if (lower.includes('googleads.g.doubleclick.net') || lower.includes('conversion.js')) {
    result.googleAds = true;
    result.details.push('Google Ads tracking detected');
  }

  if (result.details.length === 0) {
    result.details.push('No analytics detected');
  }

  return result;
}

/* ── Security Headers ── */
function checkSecurityHeaders(headers: Headers): SecurityResult {
  const result: SecurityResult = {
    hsts: false, csp: false, xFrameOptions: false, xContentTypeOptions: false,
    strictTransportSecurity: null, details: []
  };

  const hsts = headers.get('strict-transport-security');
  if (hsts) {
    result.hsts = true;
    result.strictTransportSecurity = hsts;
    result.details.push(`HSTS: ${hsts}`);
  } else {
    result.details.push('Missing HSTS header');
  }

  const csp = headers.get('content-security-policy');
  if (csp) {
    result.csp = true;
    result.details.push('CSP present');
  } else {
    result.details.push('Missing CSP header');
  }

  const xfo = headers.get('x-frame-options');
  if (xfo) {
    result.xFrameOptions = true;
    result.details.push(`X-Frame-Options: ${xfo}`);
  } else {
    result.details.push('Missing X-Frame-Options');
  }

  const xcto = headers.get('x-content-type-options');
  if (xcto) {
    result.xContentTypeOptions = true;
    result.details.push(`X-Content-Type-Options: ${xcto}`);
  } else {
    result.details.push('Missing X-Content-Type-Options');
  }

  return result;
}

/* ── Sitewide Pattern Analysis ── */
function analyzeSitewidePatterns(pages: PageData[]): SitewidePatterns {
  const titleMap = new Map<string, string[]>();
  const metaMap = new Map<string, string[]>();
  let pagesWithNoH1 = 0;
  let pagesWithMultipleH1s = 0;
  let totalWords = 0;
  let totalImages = 0;
  let totalAltCoverage = 0;
  const pagesWithErrors: { url: string; status: number }[] = [];

  for (const page of pages) {
    if (page.status >= 400) {
      pagesWithErrors.push({ url: page.url, status: page.status });
      continue;
    }

    // Track duplicate titles
    if (page.title) {
      const existing = titleMap.get(page.title) || [];
      existing.push(page.url);
      titleMap.set(page.title, existing);
    }

    // Track duplicate meta descriptions
    if (page.metaDescription) {
      const existing = metaMap.get(page.metaDescription) || [];
      existing.push(page.url);
      metaMap.set(page.metaDescription, existing);
    }

    // H1 analysis
    if (page.h1s.length === 0) pagesWithNoH1++;
    else if (page.h1s.length > 1) pagesWithMultipleH1s++;

    totalWords += page.wordCount;
    totalImages += page.imageCount;
    totalAltCoverage += page.altCoverage;
  }

  const validPages = pages.filter(p => p.status < 400);
  const duplicateTitles = [...titleMap.entries()].filter(([, urls]) => urls.length > 1).map(([title, urls]) => `"${title.substring(0, 50)}" on ${urls.length} pages`);
  const duplicateMetaDescriptions = [...metaMap.entries()].filter(([, urls]) => urls.length > 1).map(([desc, urls]) => `"${desc.substring(0, 50)}..." on ${urls.length} pages`);

  return {
    duplicateTitles,
    duplicateMetaDescriptions,
    pagesWithNoH1,
    pagesWithMultipleH1s,
    totalPagesCrawled: pages.length,
    pagesWithErrors,
    averageWordsPerPage: validPages.length > 0 ? Math.round(totalWords / validPages.length) : 0,
    totalImagesAcrossSite: totalImages,
    averageAltCoverage: validPages.length > 0 ? Math.round(totalAltCoverage / validPages.length) : 0,
  };
}

/* ── Redirect Chain Detection ── */
async function detectRedirectChain(url: string): Promise<RedirectChainResult> {
  const chain: string[] = [];
  let current = url;
  const seen = new Set<string>();
  let chainLength = 0;
  try {
    while (chainLength < 10) {
      if (seen.has(current)) return { chain, isLoop: true, chainLength };
      seen.add(current);
      chain.push(current);
      const res = await fetchWithTimeout(current, 10000, { method: 'HEAD', redirect: 'manual' });
      if (res.status >= 300 && res.status < 400) {
        const loc = res.headers.get('location');
        if (!loc) break;
        current = new URL(loc, current).href;
        chainLength++;
      } else {
        break;
      }
    }
  } catch { /* ignore */ }
  return { chain, isLoop: false, chainLength };
}

/* ── Mixed Content Detection ── */
function detectMixedContent(html: string, baseUrl: string): MixedContentResult {
  if (!baseUrl.startsWith('https://')) return { mixedResources: [], hasMixedContent: false };
  const mixed: string[] = [];
  // Check for HTTP resources on HTTPS page
  const httpResourcePattern = /(?:src|href)=["'](http:\/\/[^"']*)["']/gi;
  let m;
  while ((m = httpResourcePattern.exec(html)) !== null) {
    mixed.push(m[1]);
  }
  return { mixedResources: mixed.slice(0, 20), hasMixedContent: mixed.length > 0 };
}

/* ── Soft 404 Detection ── */
function detectSoft404s(pages: PageData[]): Soft404Result {
  const soft404s: { url: string; wordCount: number; reason: string }[] = [];
  for (const page of pages) {
    if (page.status >= 400) continue;
    // Soft 404 indicators
    const hasNotFoundText = page.title.toLowerCase().includes('not found') || page.title.toLowerCase().includes('404');
    const isThin = page.wordCount < 50;
    const hasNoH1 = page.h1s.length === 0;
    if (hasNotFoundText || (isThin && hasNoH1)) {
      const reason = hasNotFoundText ? 'Page title suggests 404' : isThin ? 'Very thin content (<50 words)' : 'Missing H1 on thin page';
      soft404s.push({ url: page.url, wordCount: page.wordCount, reason });
    }
  }
  return { soft404s: soft404s.slice(0, 10), count: soft404s.length };
}

/* ── Social Tags Analysis ── */
function analyzeSocialTags(homepage: PageData): SocialTagsResult {
  const og = homepage.ogTags;
  const tw = homepage.twitterCards;
  const hasAllEssential = !!(og['title'] && og['description'] && og['image'] && og['type'] && og['url']);
  return {
    ogTitle: og['title'] || null,
    ogDescription: og['description'] || null,
    ogImage: og['image'] || null,
    ogType: og['type'] || null,
    ogUrl: og['url'] || null,
    twitterCard: tw['card'] || null,
    twitterTitle: tw['title'] || null,
    twitterDescription: tw['description'] || null,
    twitterImage: tw['image'] || null,
    hasAllEssential,
  };
}

/* ── Hreflang Analysis ── */
function analyzeHreflang(homepage: PageData): HreflangResult {
  const tags = homepage.hreflang;
  const hasXDefault = tags.some(t => t.lang === 'x-default');
  const issues: string[] = [];
  if (tags.length > 0 && !hasXDefault) issues.push('Missing x-default fallback');
  // Check for self-referencing
  const selfRef = tags.find(t => t.url === homepage.url);
  if (tags.length > 0 && !selfRef) issues.push('Missing self-referencing hreflang');
  return { tags, hasXDefault, issues };
}

/* ── llms.txt Check ── */
async function checkLlmsTxt(domain: string): Promise<LlmsTxtResult> {
  try {
    const res = await fetchWithTimeout(`https://${domain}/llms.txt`, 8000);
    if (!res.ok) return { exists: false, content: null, hasNoTrain: false, hasAttribution: false };
    const content = await res.text();
    const lower = content.toLowerCase();
    return {
      exists: true,
      content: content.substring(0, 500),
      hasNoTrain: lower.includes('no-train') || lower.includes('do not train'),
      hasAttribution: lower.includes('attribution') || lower.includes('cite'),
    };
  } catch {
    return { exists: false, content: null, hasNoTrain: false, hasAttribution: false };
  }
}

/* ── Passage Structure Analysis ── */
function analyzePassageStructure(pages: PageData[]): PassageResult {
  let totalPassageLength = 0;
  let passageCount = 0;
  let directAnswerCount = 0;
  let questionHeadingCount = 0;

  for (const page of pages) {
    // Estimate passage length from paragraph text between headings
    const allHeadings = [...page.h2s, ...page.h3s];
    questionHeadingCount += allHeadings.filter(h => /\?/.test(h)).length;

    // Direct answers: headings that look like FAQs
    for (const h2 of page.h2s) {
      const wordCount = h2.split(/\s+/).length;
      if (wordCount >= 3 && wordCount <= 15) {
        passageCount++;
        totalPassageLength += wordCount;
      }
    }

    // Check for FAQ or Q&A patterns
    if (page.h2s.some(h => h.toLowerCase().includes('faq') || h.toLowerCase().includes('frequently asked'))) {
      directAnswerCount++;
    }
  }

  const avgPassageLength = passageCount > 0 ? Math.round(totalPassageLength / passageCount) : 0;
  const structureScore = Math.min(100, (directAnswerCount * 20) + (questionHeadingCount * 5) + (avgPassageLength >= 3 ? 20 : 0));

  return {
    avgPassageLength,
    hasDirectAnswers: directAnswerCount > 0,
    directAnswerCount,
    questionHeadingCount,
    structureScore,
  };
}

/* ── Content Duplication (Jaccard Similarity) ── */
function detectContentDuplication(pages: PageData[]): { duplicates: { url1: string; url2: string; similarity: number }[]; hasDuplicates: boolean } {
  const duplicates: { url1: string; url2: string; similarity: number }[] = [];
  const validPages = pages.filter(p => p.status < 400 && p.wordCount > 50);

  function getWordSet(text: string): Set<string> {
    const words = text.toLowerCase().split(/\s+/).filter(w => w.length > 3);
    return new Set(words);
  }

  for (let i = 0; i < validPages.length; i++) {
    for (let j = i + 1; j < validPages.length; j++) {
      const set1 = getWordSet(validPages[i].title + ' ' + validPages[i].h1s.join(' ') + ' ' + validPages[i].h2s.join(' '));
      const set2 = getWordSet(validPages[j].title + ' ' + validPages[j].h1s.join(' ') + ' ' + validPages[j].h2s.join(' '));
      const intersection = new Set([...set1].filter(x => set2.has(x)));
      const union = new Set([...set1, ...set2]);
      if (union.size === 0) continue;
      const similarity = intersection.size / union.size;
      if (similarity > 0.7) {
        duplicates.push({ url1: validPages[i].url, url2: validPages[j].url, similarity: Math.round(similarity * 100) });
      }
    }
  }

  return { duplicates: duplicates.slice(0, 10), hasDuplicates: duplicates.length > 0 };
}

/* ── AI Analysis ── */
async function callAI(systemPrompt: string, userPrompt: string): Promise<KimiAnalysis | null> {
  if (!ANTHROPIC_API_KEY) {
    console.warn('[audit] No ANTHROPIC_API_KEY configured — skipping AI analysis');
    return null;
  }
  return callAnthropic(systemPrompt, userPrompt);
}

async function callAnthropic(systemPrompt: string, userPrompt: string): Promise<KimiAnalysis | null> {
  try {
    const res = await fetchWithTimeout(`${ANTHROPIC_BASE_URL}/v1/messages`, 45000, {
      method: 'POST',
      headers: {
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: ANTHROPIC_MODEL,
        max_tokens: 4096,
        temperature: 0.3,
        system: systemPrompt,
        messages: [{ role: 'user', content: userPrompt }],
      }),
    });
    if (!res.ok) {
      const errText = await res.text();
      console.error('[audit] Anthropic API error:', res.status, errText.substring(0, 500));
      return null;
    }
    const data = await res.json();
    const content = data.content?.[0]?.text;
    if (!content) {
      console.error('[audit] Anthropic returned empty content:', JSON.stringify(data).substring(0, 500));
      return null;
    }
    const jsonText = content.replace(/```json\s*/g, '').replace(/```\s*$/g, '').trim();
    return JSON.parse(jsonText) as KimiAnalysis;
  } catch (err) {
    console.error('[audit] Anthropic call failed:', err instanceof Error ? err.message : err);
    return null;
  }
}

function buildKimiPrompt(
  homepage: PageData,
  pages: PageData[],
  patterns: SitewidePatterns,
  analytics: AnalyticsResult,
  security: SecurityResult,
  spa: { isSPA: boolean; framework: string | null },
  pageSpeed: any,
  domain: string,
  robots: RobotsResult,
  cms: CmsResult,
  eeatLocal: ReturnType<typeof detectEeatAndLocal>,
  freshness: FreshnessResult,
  authority?: AuthorityData
): string {
  const ps = pageSpeed?.lighthouseResult;
  const perf = ps?.categories?.performance?.score;
  const errorPages = patterns.pagesWithErrors.length > 0
    ? patterns.pagesWithErrors.map(e => `- ${e.url} (HTTP ${e.status})`).join('\n')
    : 'None detected';

  const allH1s = pages.map(p => ({ url: p.url, h1s: p.h1s }));
  const h1Issues = allH1s.filter(p => p.h1s.length === 0 || p.h1s.length > 1);

  return `You are an expert SEO analyst for theStacc, an AI SEO automation platform. Analyze this website's signals and return ONLY a JSON object.

WEBSITE: ${domain}
PLATFORM: ${spa.isSPA ? `SPA (${spa.framework})` : 'Server-rendered or static'}
PAGES AUDITED: ${patterns.totalPagesCrawled} (${pages.filter(p => p.status < 400).length} successful)

HOMEPAGE SIGNALS:
- Title (${homepage.titleLength} chars): "${homepage.title}"
- Meta description (${homepage.metaDescLength} chars): "${homepage.metaDescription}"
- H1s (${homepage.h1s.length}): ${JSON.stringify(homepage.h1s)}
- H2s (${homepage.h2s.length}): ${JSON.stringify(homepage.h2s.slice(0, 5))}
- Word count: ${homepage.wordCount}
- Images: ${homepage.imageCount} (${homepage.altCoverage}% with alt text)
- Internal links: ${homepage.internalLinks}
- Schema types: ${JSON.stringify(homepage.schemaTypes)}
- Has blog section: ${pages.some(p => p.url.includes('/blog')) || homepage.url.includes('/blog')}

SITEWIDE PATTERNS:
- Duplicate titles: ${patterns.duplicateTitles.length > 0 ? patterns.duplicateTitles.join('; ') : 'None'}
- Duplicate meta descriptions: ${patterns.duplicateMetaDescriptions.length > 0 ? patterns.duplicateMetaDescriptions.join('; ') : 'None'}
- Pages with NO H1: ${patterns.pagesWithNoH1} of ${patterns.totalPagesCrawled}
- Pages with multiple H1s: ${patterns.pagesWithMultipleH1s} of ${patterns.totalPagesCrawled}
- Average words per page: ${patterns.averageWordsPerPage}
- Total images across site: ${patterns.totalImagesAcrossSite}
- Pages with errors:\n${errorPages}

ANALYTICS STACK:
${analytics.details.join('\n')}

SECURITY HEADERS:
${security.details.join('\n')}

PERFORMANCE: ${perf ? Math.round(perf * 100) : 'N/A'}/100

TECHNOLOGY STACK:
- CMS: ${cms.cms || 'Unknown'}
- Hosting: ${cms.hosting || 'Unknown'}
- Stack: ${cms.techStack.join(', ') || 'Not detected'}

ROBOTS.TXT ANALYSIS:
- AI crawlers blocked: ${robots.aiCrawlerBlocks.length > 0 ? robots.aiCrawlerBlocks.join(', ') : 'None'}
- Disallowed paths: ${robots.disallowedPaths.length}
- Has sitemap reference: ${robots.hasSitemapRef}

E-E-A-T SIGNALS:
${eeatLocal.eeatDetails.join('\n')}

LOCAL SEO:
${eeatLocal.localDetails.join('\n')}

CONTENT FRESHNESS:
- Oldest content: ${freshness.oldestDate || 'Unknown'}
- Newest content: ${freshness.newestDate || 'Unknown'}
- Average age: ${freshness.averageAgeDays !== null ? freshness.averageAgeDays + ' days' : 'Unknown'}
- Freshness status: ${freshness.contentFreshness}
- Orphan pages: ${freshness.orphanPages.length}

AUTHORITY & BACKLINK DATA (from live SEO database):
${authority?.dataAvailable ? `- Domain Rating: ${authority.dr}/100
- Backlinks: ${authority.backlinks.toLocaleString()} live
- Referring domains: ${authority.refDomains.toLocaleString()} (from ${authority.refIps} IPs)
- Ranking keywords: ${authority.totalKeywords.toLocaleString()} (${authority.pos1to3} in top 3, ${authority.pos4to10} in top 10)
- Estimated organic traffic: ~${authority.estTraffic.toLocaleString()}/mo
- Top keyword: ${authority.topKeywords[0]?.keyword || 'N/A'} (position ${authority.topKeywords[0]?.position || 'N/A'})` : '- No authority data available (site may be too new)'}

IMPORTANT CONTEXT:
${spa.isSPA ? `This is a ${spa.framework} SPA. Content, headings, and links may only exist after JavaScript execution. Googlebot and AI crawlers see the static HTML shell first.` : ''}
${patterns.pagesWithErrors.length > 0 ? `CRITICAL: ${patterns.pagesWithErrors.length} pages return HTTP errors. This severely impacts crawlability and user experience.` : ''}
${robots.aiCrawlerBlocks.length > 0 ? `WARNING: AI crawlers are blocked — ${robots.aiCrawlerBlocks.join(', ')} cannot access this site.` : ''}
${freshness.orphanPages.length > 0 ? `NOTE: ${freshness.orphanPages.length} pages are orphaned (not linked from homepage).` : ''}

Return ONLY this JSON structure (no markdown, no explanation):
{
  "contentQualityScore": number 0-20,
  "contentQualityNotes": "2-3 sentences on content quality — mention sitewide patterns, word count averages, and content gaps vs. what a competitive site would have",
  "seoGaps": ["specific gap 1", "specific gap 2", "specific gap 3", "specific gap 4", "specific gap 5"],
  "businessType": "detected business type with specificity — e.g. 'B2B SaaS — LinkedIn automation' not just 'SaaS'",
  "topRecommendations": ["specific action 1 with effort estimate", "specific action 2", "specific action 3", "specific action 4", "specific action 5"],
  "staccFeatureMatches": [
    { "feature": "Blog SEO Engine", "reason": "why this feature helps", "link": "/modules/content-seo/" }
  ],
  "competitors": [
    { "name": "Competitor Name", "domain": "competitor.com", "note": "why they're a competitor" }
  ],
  "estimatedContentGap": "e.g. 'Competitors in this space typically publish 50-200 blog posts; this site has X'"
}`;
}

/* ── Severity-Weighted Scoring ── */
function scoreAudit(
  homepage: PageData,
  pages: PageData[],
  patterns: SitewidePatterns,
  analytics: AnalyticsResult,
  security: SecurityResult,
  spa: { isSPA: boolean; framework: string | null },
  pageSpeed: any,
  robotsTxt: boolean,
  sitemap: boolean,
  kimi: KimiAnalysis | null,
  finalUrl: string,
  robots: RobotsResult,
  redirectChain: RedirectChainResult,
  mixedContent: MixedContentResult,
  soft404s: Soft404Result,
  socialTags: SocialTagsResult,
  hreflang: HreflangResult,
  geoAio: GeoAioResult,
  authority: AuthorityData
): { categories: Category[]; overallScore: number; grade: string; pageSpeedMetrics: any; businessType: string } {
  const categories: Category[] = [];

  // Helper to create a check
  const mkCheck = (name: string, points: number, maxPoints: number, passed: boolean, severity: Check['severity'], detail: string, fix: string | null, extra?: Partial<Check>): Check => ({
    name, points, maxPoints, passed, severity, detail, fix,
    staccFeature: extra?.staccFeature,
    staccCta: extra?.staccCta,
    staccLink: extra?.staccLink,
  });

  /* ── Technical SEO (25) ── */
  const tech: Category = { name: 'Technical SEO', score: 0, maxScore: 25, checks: [] };
  const isHttps = finalUrl.startsWith('https://');

  tech.checks.push(mkCheck('HTTPS enabled', isHttps ? 5 : 0, 5, isHttps, 'critical',
    isHttps ? 'Site uses HTTPS' : 'No HTTPS',
    isHttps ? null : 'Enable SSL via your hosting provider'));

  // Sitemap health: verify it actually contains URLs, not just returns 200
  const sitemapHealthy = sitemap && patterns.totalPagesCrawled > 0;
  tech.checks.push(mkCheck('XML sitemap healthy', sitemapHealthy ? 4 : 0, 4, sitemapHealthy, 'high',
    sitemapHealthy ? `Sitemap with ${patterns.totalPagesCrawled} URLs found` : (sitemap ? 'Sitemap returns non-XML content' : 'No sitemap.xml'),
    sitemapHealthy ? null : 'Create a proper XML sitemap'));

  tech.checks.push(mkCheck('robots.txt exists', robotsTxt ? 3 : 0, 3, robotsTxt, 'medium',
    robotsTxt ? 'robots.txt found' : 'No robots.txt',
    robotsTxt ? null : 'Create robots.txt at domain root'));

  const hasViewport = !!homepage.viewport;
  const viewportHasWidth = hasViewport && homepage.viewport!.includes('width=device-width');
  tech.checks.push(mkCheck('Mobile viewport', hasViewport && viewportHasWidth ? 3 : hasViewport ? 1 : 0, 3, hasViewport && viewportHasWidth, 'medium',
    hasViewport ? `Viewport: ${homepage.viewport}` : 'No viewport meta tag',
    !hasViewport ? 'Add <meta name="viewport" content="width=device-width, initial-scale=1">' : null));

  const hasCanonical = !!homepage.canonical;
  // Check for canonical bugs (canonical pointing to wrong page)
  let canonicalBug = false;
  for (const p of pages) {
    if (p.canonical && p.canonical !== p.url && !p.canonical.includes(p.url.replace(/\/+$/, ''))) {
      canonicalBug = true;
      break;
    }
  }
  tech.checks.push(mkCheck('Canonical tags', hasCanonical && !canonicalBug ? 4 : canonicalBug ? 1 : 0, 4, hasCanonical && !canonicalBug, 'high',
    canonicalBug ? 'Canonical points to wrong URL on some pages' : (hasCanonical ? 'Canonical present' : 'No canonical tag'),
    canonicalBug ? 'Fix canonical URLs to self-reference each page' : (hasCanonical ? null : 'Add self-referencing canonical tags')));

  // HTTP errors check
  const hasErrors = patterns.pagesWithErrors.length > 0;
  tech.checks.push(mkCheck('No critical HTTP errors', hasErrors ? 0 : 3, 3, !hasErrors, 'critical',
    hasErrors ? `${patterns.pagesWithErrors.length} pages return errors (e.g. HTTP ${patterns.pagesWithErrors[0]?.status})` : 'All pages load successfully',
    hasErrors ? `Fix ${patterns.pagesWithErrors.length} broken pages immediately` : null));

  // Redirect chain
  const redirectOk = redirectChain.chainLength <= 1 && !redirectChain.isLoop;
  tech.checks.push(mkCheck('Redirect chains', redirectOk ? 2 : 0, 2, redirectOk, 'medium',
    redirectChain.isLoop ? 'Redirect loop detected!' : redirectChain.chainLength > 1 ? `Redirect chain: ${redirectChain.chainLength} hops` : 'No redirect chains',
    redirectChain.chainLength > 1 ? 'Minimize redirect chains to 1 hop' : null));

  // Mixed content
  tech.checks.push(mkCheck('Mixed content', !mixedContent.hasMixedContent ? 2 : 0, 2, !mixedContent.hasMixedContent, 'high',
    mixedContent.hasMixedContent ? `${mixedContent.mixedResources.length} HTTP resources on HTTPS page` : 'No mixed content',
    mixedContent.hasMixedContent ? 'Serve all resources over HTTPS' : null));

  // Soft 404s
  tech.checks.push(mkCheck('Soft 404s', soft404s.count === 0 ? 2 : 0, 2, soft404s.count === 0, 'high',
    soft404s.count > 0 ? `${soft404s.count} soft 404s detected` : 'No soft 404s',
    soft404s.count > 0 ? 'Return proper 404 status for missing pages' : null));

  // Hreflang
  const hasHreflang = hreflang.tags.length > 0;
  const hreflangOk = hasHreflang && hreflang.issues.length === 0;
  tech.checks.push(mkCheck('Hreflang tags', hreflangOk ? 2 : hasHreflang ? 1 : 0, 2, hreflangOk, 'medium',
    hasHreflang ? `${hreflang.tags.length} hreflang tags (${hreflang.issues.join(', ') || 'no issues'})` : 'No hreflang tags',
    hreflang.issues.length > 0 ? hreflang.issues.join('; ') : null));

  tech.maxScore = 25;

  // SPA penalty reduction
  if (spa.isSPA) {
    tech.checks.push(mkCheck('SPA pre-rendering', 0, 3, false, 'high',
      `${spa.framework} SPA detected — content requires JS execution`,
      'Pre-render or SSR key pages for search crawlers'));
    tech.maxScore += 3;
  }

  tech.score = Math.min(tech.maxScore, tech.checks.reduce((s, c) => s + c.points, 0));
  categories.push(tech);

  /* ── On-Page SEO (20) ── */
  const onp: Category = { name: 'On-Page SEO', score: 0, maxScore: 20, checks: [] };

  // Title quality: check for duplicates and length
  const titleIssues: string[] = [];
  if (patterns.duplicateTitles.length > 0) titleIssues.push(`${patterns.duplicateTitles.length} duplicate titles`);
  if (homepage.titleLength < 10) titleIssues.push('title too short');
  if (homepage.titleLength > 70) titleIssues.push('title too long');
  const titleScore = titleIssues.length === 0 ? 4 : titleIssues.length === 1 ? 2 : 0;
  onp.checks.push(mkCheck('Title tags', titleScore, 4, titleScore >= 2, titleIssues.length > 0 ? 'high' : 'low',
    titleIssues.length > 0 ? `Issues: ${titleIssues.join(', ')}` : `Title: "${homepage.title.substring(0, 50)}" (${homepage.titleLength} chars)`,
    titleIssues.length > 0 ? 'Write unique, keyword-rich titles (50-60 chars) for every page' : null,
    { staccFeature: 'Blog SEO Engine', staccCta: 'Stacc auto-optimizes every title tag', staccLink: '/modules/content-seo/' }));

  // Meta description quality
  const metaIssues: string[] = [];
  if (patterns.duplicateMetaDescriptions.length > 0) metaIssues.push(`${patterns.duplicateMetaDescriptions.length} duplicates`);
  if (homepage.metaDescLength === 0) metaIssues.push('missing');
  else if (homepage.metaDescLength > 170) metaIssues.push('too long');
  else if (homepage.metaDescLength < 50) metaIssues.push('too short');
  const metaScore = metaIssues.length === 0 ? 4 : metaIssues.length === 1 ? 2 : 0;
  onp.checks.push(mkCheck('Meta descriptions', metaScore, 4, metaScore >= 2, metaIssues.length > 0 ? 'high' : 'low',
    metaIssues.length > 0 ? `Issues: ${metaIssues.join(', ')}` : `Meta desc: ${homepage.metaDescLength} chars`,
    metaIssues.length > 0 ? 'Write unique, compelling meta descriptions (120-160 chars) per page' : null,
    { staccFeature: 'Blog SEO Engine', staccCta: 'Stacc writes click-worthy meta descriptions', staccLink: '/modules/content-seo/' }));

  // Heading structure — now sitewide
  const h1Severity = patterns.pagesWithNoH1 > 0 || patterns.pagesWithMultipleH1s > 2 ? 'critical' : 'high';
  const h1Score = patterns.pagesWithNoH1 === 0 && patterns.pagesWithMultipleH1s === 0 ? 4
    : patterns.pagesWithNoH1 <= 1 && patterns.pagesWithMultipleH1s <= 1 ? 2
    : 0;
  onp.checks.push(mkCheck('Heading structure', h1Score, 4, h1Score >= 2, h1Severity,
    `${patterns.pagesWithNoH1} pages with no H1, ${patterns.pagesWithMultipleH1s} with multiple H1s`,
    patterns.pagesWithNoH1 > 0 || patterns.pagesWithMultipleH1s > 0 ? 'Ensure exactly one H1 per page; use H2-H6 for subsections' : null,
    { staccFeature: 'Blog SEO Engine', staccCta: 'Stacc structures proper heading hierarchy', staccLink: '/modules/content-seo/' }));

  // H2 presence
  const h2Pages = pages.filter(p => p.h2s.length >= 2).length;
  const h2Score = h2Pages >= Math.ceil(pages.length / 2) ? 3 : h2Pages > 0 ? 1 : 0;
  onp.checks.push(mkCheck('H2 subheadings', h2Score, 3, h2Score >= 1, 'medium',
    `${h2Pages}/${pages.length} pages have 2+ H2s`,
    h2Pages < pages.length / 2 ? 'Add H2s for scannable sections on more pages' : null));

  // Internal links
  const avgInternalLinks = pages.length > 0 ? pages.reduce((s, p) => s + p.internalLinks, 0) / pages.length : 0;
  const liScore = avgInternalLinks >= 3 ? 3 : avgInternalLinks >= 1 ? 1 : 0;
  onp.checks.push(mkCheck('Internal links', liScore, 3, liScore >= 1, 'medium',
    `~${Math.round(avgInternalLinks)} internal links/page`,
    avgInternalLinks < 3 ? 'Add more contextual internal links' : null,
    { staccFeature: 'Link Building', staccCta: "Stacc's link network places you in relevant articles", staccLink: '/modules/content-seo/' }));

  // Open Graph
  const ogScore = socialTags.hasAllEssential ? 2 : socialTags.ogTitle ? 1 : 0;
  onp.checks.push(mkCheck('Open Graph tags', ogScore, 2, ogScore >= 1, 'low',
    socialTags.hasAllEssential ? `OG: title, desc, image, type, URL` : socialTags.ogTitle ? `Partial OG: ${Object.keys(homepage.ogTags).join(', ')}` : 'No Open Graph tags',
    !socialTags.hasAllEssential ? 'Add og:title, og:description, og:image, og:type, og:url' : null));

  // Twitter Cards
  const twScore = socialTags.twitterCard && socialTags.twitterTitle ? 2 : socialTags.twitterCard ? 1 : 0;
  onp.checks.push(mkCheck('Twitter Cards', twScore, 2, twScore >= 1, 'low',
    socialTags.twitterCard ? `Twitter ${socialTags.twitterCard} card` : 'No Twitter Card tags',
    !socialTags.twitterCard ? 'Add twitter:card, twitter:title, twitter:description, twitter:image' : null));

  onp.score = Math.min(onp.maxScore, onp.checks.reduce((s, c) => s + c.points, 0));
  categories.push(onp);

  /* ── Content Quality (22) ── */
  const cont: Category = { name: 'Content Quality', score: 0, maxScore: 22, checks: [] };
  const avgWords = patterns.averageWordsPerPage;
  const w300 = avgWords >= 300;
  const w600 = avgWords >= 600;
  cont.checks.push(mkCheck('Content depth (300+ words/page)', w300 ? 5 : avgWords >= 100 ? 2 : 0, 5, w300, 'high',
    `~${avgWords} words/page average`,
    avgWords < 300 ? 'Expand thin pages to 300+ words minimum' : null,
    { staccFeature: 'Blog SEO Engine', staccCta: 'Stacc publishes 30+ in-depth articles monthly', staccLink: '/modules/content-seo/' }));

  cont.checks.push(mkCheck('Content depth bonus (600+)', w600 ? 3 : 0, 3, w600, 'medium',
    w600 ? 'Deep content detected' : '<600 words/page', null,
    { staccFeature: 'Blog SEO Engine', staccCta: 'Stacc writes 1,000+ word articles that rank', staccLink: '/modules/content-seo/' }));

  // Check for placeholder text
  const hasPlaceholder = pages.some(p => ['lorem ipsum', 'coming soon', 'under construction', 'placeholder'].some(ph => p.title.toLowerCase().includes(ph)));
  cont.checks.push(mkCheck('No placeholder text', !hasPlaceholder ? 3 : 0, 3, !hasPlaceholder, 'high',
    hasPlaceholder ? 'Placeholder text detected' : 'Clean content', hasPlaceholder ? 'Replace placeholder text with real content' : null));

  // Blog presence
  const hasBlog = pages.some(p => p.url.includes('/blog')) || pages.some(p => p.h2s.some(h => h.toLowerCase().includes('blog')));
  cont.checks.push(mkCheck('Blog section', hasBlog ? 3 : 0, 3, hasBlog, 'high',
    hasBlog ? 'Blog section detected' : 'No blog section',
    !hasBlog ? 'Start a blog — content is the #1 ranking factor' : null,
    { staccFeature: 'Blog SEO Engine', staccCta: 'Stacc builds your content calendar from scratch', staccLink: '/modules/content-seo/' }));

  // Content volume
  const contentVolumeScore = pages.length >= 10 ? 3 : pages.length >= 5 ? 2 : pages.length >= 2 ? 1 : 0;
  cont.checks.push(mkCheck('Content volume', contentVolumeScore, 3, contentVolumeScore >= 2, 'high',
    `${pages.length} indexable pages`,
    pages.length < 10 ? 'Build out more landing pages, service pages, and blog posts' : null));

  // Content duplication
  const dupes = detectContentDuplication(pages);
  cont.checks.push(mkCheck('Content duplication', !dupes.hasDuplicates ? 3 : 0, 3, !dupes.hasDuplicates, 'high',
    dupes.hasDuplicates ? `${dupes.duplicates.length} near-duplicate page pairs (>>70% similarity)` : 'No content duplication',
    dupes.hasDuplicates ? 'Consolidate or differentiate near-duplicate pages' : null));

  // Passage structure for AI
  cont.checks.push(mkCheck('Passage structure', geoAio.passageStructure.structureScore >= 40 ? 2 : geoAio.passageStructure.structureScore >= 20 ? 1 : 0, 2,
    geoAio.passageStructure.structureScore >= 40, 'medium',
    `${geoAio.passageStructure.questionHeadingCount} question-based headings, ${geoAio.passageStructure.directAnswerCount} FAQ sections`,
    geoAio.passageStructure.structureScore < 40 ? 'Use question-based H2s and direct 40-60 word answers' : null));

  cont.score = cont.checks.reduce((s, c) => s + c.points, 0);
  if (kimi?.contentQualityScore !== undefined) {
    cont.score = Math.round((cont.score + kimi.contentQualityScore) / 2);
  }
  categories.push(cont);

  /* ── Performance (15) ── */
  const perf: Category = { name: 'Performance', score: 0, maxScore: 15, checks: [] };
  let pageSpeedMetrics: { lcp?: number; cls?: number; inp?: number; ttfb?: number; performance?: number } | null = null;

  if (pageSpeed?.lighthouseResult?.audits) {
    const a = pageSpeed.lighthouseResult.audits;
    const c = pageSpeed.lighthouseResult.categories;
    const lcpV = a['largest-contentful-paint']?.numericValue;
    const lcpS = a['largest-contentful-paint']?.score;
    const clsV = a['cumulative-layout-shift']?.numericValue;
    const clsS = a['cumulative-layout-shift']?.score;
    const pS = c?.performance?.score;
    pageSpeedMetrics = { lcp: lcpV ? Math.round(lcpV / 10) / 100 : undefined, cls: clsV, performance: pS ? Math.round(pS * 100) : undefined };

    // Updated LCP threshold: 2.0s (March 2026 Google update)
    const lcpOk = lcpS !== undefined && lcpS >= 0.9;
    perf.checks.push(mkCheck('LCP ≤ 2.0s', lcpOk ? 4 : lcpS !== undefined && lcpS >= 0.5 ? 2 : 0, 4, lcpOk, 'critical',
      lcpV ? `LCP: ${(lcpV / 1000).toFixed(1)}s` : 'N/A',
      lcpV && lcpV > 2000 ? 'Optimize images, enable caching, reduce TTFB' : null));

    const clsOk = clsS !== undefined && clsS >= 0.9;
    perf.checks.push(mkCheck('CLS < 0.1', clsOk ? 3 : clsS !== undefined && clsS >= 0.5 ? 1 : 0, 3, clsOk, 'medium',
      clsV !== undefined ? `CLS: ${clsV.toFixed(3)}` : 'N/A',
      clsV && clsV > 0.1 ? 'Set explicit dimensions on images' : null));

    // INP — New Core Web Vital (replaced FID)
    const inpV = a['interaction-to-next-paint']?.numericValue;
    const inpS = a['interaction-to-next-paint']?.score;
    const inpOk = inpS !== undefined && inpS >= 0.9;
    perf.checks.push(mkCheck('INP ≤ 200ms', inpOk ? 3 : inpS !== undefined && inpS >= 0.5 ? 1 : 0, 3, inpOk, 'high',
      inpV !== undefined ? `INP: ${Math.round(inpV)}ms` : 'N/A',
      inpV && inpV > 200 ? 'Reduce JavaScript execution, break up long tasks' : null));

    // TTFB
    const ttfbV = a['server-response-time']?.numericValue;
    const ttfbOk = ttfbV !== undefined && ttfbV <= 800;
    perf.checks.push(mkCheck('TTFB ≤ 800ms', ttfbOk ? 2 : ttfbV !== undefined && ttfbV <= 1800 ? 1 : 0, 2, ttfbOk, 'high',
      ttfbV !== undefined ? `TTFB: ${Math.round(ttfbV)}ms` : 'N/A',
      ttfbV && ttfbV > 800 ? 'Use CDN, optimize server response, enable caching' : null));

    const pOk = pS !== undefined && pS >= 0.5;
    perf.checks.push(mkCheck('Performance score', pOk ? 3 : pS !== undefined ? Math.round(pS * 3) : 0, 3, pOk, 'high',
      pS !== undefined ? `Performance: ${Math.round(pS * 100)}/100` : 'N/A',
      pS !== undefined && pS < 0.5 ? 'Compress assets and enable caching' : null));

    pageSpeedMetrics = {
      lcp: lcpV ? Math.round(lcpV / 10) / 100 : undefined,
      cls: clsV,
      inp: inpV ? Math.round(inpV) : undefined,
      ttfb: ttfbV ? Math.round(ttfbV) : undefined,
      performance: pS ? Math.round(pS * 100) : undefined
    };
  } else {
    // PageSpeed failed — award ZERO points, not sympathy points
    perf.checks.push(mkCheck('LCP', 0, 4, false, 'high', 'PageSpeed unavailable', 'Run Lighthouse locally or provide a PageSpeed API key'));
    perf.checks.push(mkCheck('CLS', 0, 3, false, 'medium', 'PageSpeed unavailable', null));
    perf.checks.push(mkCheck('INP', 0, 3, false, 'high', 'PageSpeed unavailable', null));
    perf.checks.push(mkCheck('TTFB', 0, 2, false, 'high', 'PageSpeed unavailable', null));
    perf.checks.push(mkCheck('Performance', 0, 3, false, 'high', 'PageSpeed unavailable', null));
  }
  perf.score = perf.checks.reduce((s, c) => s + c.points, 0);
  categories.push(perf);

  /* ── Schema Markup (12) ── */
  const sch: Category = { name: 'Schema Markup', score: 0, maxScore: 12, checks: [] };
  const allSchemaTypes = [...new Set(pages.flatMap(p => p.schemaTypes))];
  const hasLd = allSchemaTypes.length > 0;

  sch.checks.push(mkCheck('JSON-LD present', hasLd ? 2 : 0, 2, hasLd, 'high',
    hasLd ? `${allSchemaTypes.length} schema type(s): ${allSchemaTypes.join(', ')}` : 'No structured data',
    !hasLd ? 'Add JSON-LD schema' : null,
    { staccFeature: 'Schema Generator', staccCta: 'Stacc auto-generates LocalBusiness schema', staccLink: '/tools/schema-markup-generator/' }));

  const hasBusinessSchema = allSchemaTypes.some(t =>
    t.toLowerCase().includes('localbusiness') ||
    t.toLowerCase().includes('organization') ||
    t.toLowerCase().includes('roofingcontractor') ||
    t.toLowerCase().includes('professional service')
  );
  sch.checks.push(mkCheck('Business schema', hasBusinessSchema ? 2 : 0, 2, hasBusinessSchema, 'high',
    hasBusinessSchema ? `Business schema found: ${allSchemaTypes.find(t => t.toLowerCase().includes('business') || t.toLowerCase().includes('organization') || t.toLowerCase().includes('contractor'))}` : 'Missing business schema',
    !hasBusinessSchema ? 'Add Organization or LocalBusiness schema with NAP' : null,
    { staccFeature: 'Local SEO', staccCta: 'Stacc generates and validates business schema', staccLink: '/modules/local-seo/' }));

  // BreadcrumbList
  const hasBreadcrumb = pages.some(p => p.hasBreadcrumbSchema);
  sch.checks.push(mkCheck('BreadcrumbList schema', hasBreadcrumb ? 2 : 0, 2, hasBreadcrumb, 'high',
    hasBreadcrumb ? 'BreadcrumbList schema detected' : 'Missing BreadcrumbList schema',
    !hasBreadcrumb ? 'Add BreadcrumbList schema for rich results' : null));

  // WebSite schema with SearchAction
  const hasWebsite = pages.some(p => p.hasWebsiteSchema);
  sch.checks.push(mkCheck('WebSite schema', hasWebsite ? 2 : 0, 2, hasWebsite, 'medium',
    hasWebsite ? 'WebSite schema detected' : 'Missing WebSite schema',
    !hasWebsite ? 'Add WebSite schema with SearchAction for sitelinks searchbox' : null));

  // Person schema (E-E-A-T)
  const hasPerson = pages.some(p => p.hasPersonSchema);
  sch.checks.push(mkCheck('Person/Author schema', hasPerson ? 2 : 0, 2, hasPerson, 'medium',
    hasPerson ? 'Person schema detected' : 'Missing Person/Author schema',
    !hasPerson ? 'Add Person schema with SameAs links for author E-E-A-T' : null));

  // VideoObject
  const hasVideo = pages.some(p => p.hasVideoSchema);
  sch.checks.push(mkCheck('VideoObject schema', hasVideo ? 2 : 0, 2, hasVideo, 'low',
    hasVideo ? 'VideoObject schema detected' : 'No VideoObject schema',
    !hasVideo ? 'Add VideoObject schema for video content' : null));

  sch.score = sch.checks.reduce((s, c) => s + c.points, 0);
  categories.push(sch);

  /* ── AI Search Readiness (5) ── */
  const ai: Category = { name: 'AI Search Readiness', score: 0, maxScore: 5, checks: [] };
  const hasFaqContent = pages.some(p => p.h2s.some(h => h.toLowerCase().includes('frequently asked') || h.toLowerCase().includes('faq')));
  const hasQAPattern = pages.some(p => p.h2s.some(h => /\?/.test(h)));

  ai.checks.push(mkCheck('FAQ content', hasFaqContent ? 2 : 0, 2, hasFaqContent, 'medium',
    hasFaqContent ? 'FAQ section detected' : 'No FAQ section',
    !hasFaqContent ? 'Add FAQ section for AI search' : null,
    { staccFeature: 'AI Search Optimization', staccCta: 'Stacc structures content for ChatGPT & Perplexity', staccLink: '/blog/ai-search-optimization/' }));

  // Check robots.txt for AI crawler blocks
  const aiCrawlerBlocked = robots.aiCrawlerBlocks.length > 0;
  ai.checks.push(mkCheck('AI crawler access', aiCrawlerBlocked ? 0 : 2, 2, !aiCrawlerBlocked, 'high',
    aiCrawlerBlocked ? `Blocked: ${robots.aiCrawlerBlocks.join(', ')}` : 'AI crawlers can access site',
    aiCrawlerBlocked ? 'Consider allowing AI crawlers in robots.txt for AEO visibility' : null));

  ai.checks.push(mkCheck('Q&A patterns', hasQAPattern ? 1 : 0, 1, hasQAPattern, 'low',
    hasQAPattern ? 'Q&A patterns detected' : 'None',
    !hasQAPattern ? 'Structure content around customer questions' : null,
    { staccFeature: 'Blog SEO Engine', staccCta: 'Stacc answers real customer questions', staccLink: '/modules/content-seo/' }));

  ai.score = ai.checks.reduce((s, c) => s + c.points, 0);
  categories.push(ai);

  /* ── GEO / AIO Optimization (NEW — 5 points) ── */
  const geo: Category = { name: 'GEO / AIO', score: 0, maxScore: 5, checks: [] };

  geo.checks.push(mkCheck('llms.txt', geoAio.llmsTxt.exists ? 2 : 0, 2, geoAio.llmsTxt.exists, 'medium',
    geoAio.llmsTxt.exists ? 'llms.txt found' : 'No llms.txt',
    !geoAio.llmsTxt.exists ? 'Create /llms.txt to control AI training access' : null));

  geo.checks.push(mkCheck('Passage structure', geoAio.passageStructure.structureScore >= 40 ? 2 : geoAio.passageStructure.structureScore >= 20 ? 1 : 0, 2,
    geoAio.passageStructure.structureScore >= 40, 'medium',
    `${geoAio.passageStructure.questionHeadingCount} question headings, ${geoAio.passageStructure.directAnswerCount} FAQ sections`,
    geoAio.passageStructure.structureScore < 40 ? 'Structure content in 150-300 word passages with direct answers' : null));

  geo.checks.push(mkCheck('Content freshness', geoAio.freshnessScore >= 60 ? 1 : geoAio.freshnessScore >= 30 ? 0 : 0, 1,
    geoAio.freshnessScore >= 60, 'medium',
    `Freshness score: ${geoAio.freshnessScore}/100`,
    geoAio.freshnessScore < 60 ? 'Update content regularly for Perplexity citations' : null));

  geo.score = geo.checks.reduce((s, c) => s + c.points, 0);
  categories.push(geo);

  /* ── Images (5) ── */
  const img: Category = { name: 'Images', score: 0, maxScore: 5, checks: [] };
  const avgAlt = patterns.averageAltCoverage;
  const altOk = avgAlt >= 80;
  img.checks.push(mkCheck('Alt text (80%+)', altOk ? 3 : avgAlt >= 50 ? 2 : avgAlt > 0 ? 1 : 0, 3, altOk, 'medium',
    patterns.totalImagesAcrossSite > 0 ? `${avgAlt}% of ${patterns.totalImagesAcrossSite} images` : 'No images detected',
    patterns.totalImagesAcrossSite > 0 && avgAlt < 80 ? `Add alt text to ${Math.round(patterns.totalImagesAcrossSite * (1 - avgAlt / 100))} images` : null,
    { staccFeature: 'Image SEO', staccCta: 'Stacc auto-generates descriptive alt text', staccLink: '/modules/content-seo/' }));

  // Check for modern image formats across all pages
  const hasModernFormat = pages.some(p => p.images.some(i => i.src.includes('webp') || i.src.includes('avif')));
  img.checks.push(mkCheck('Image optimization', hasModernFormat || patterns.totalImagesAcrossSite === 0 ? 2 : 1, 2, hasModernFormat || patterns.totalImagesAcrossSite === 0, 'low',
    hasModernFormat ? 'Modern formats detected' : patterns.totalImagesAcrossSite === 0 ? 'No images' : 'No WebP/AVIF detected',
    !hasModernFormat && patterns.totalImagesAcrossSite > 0 ? 'Convert to WebP, add lazy loading' : null,
    { staccFeature: 'Content Optimization', staccCta: 'Stacc serves optimized images', staccLink: '/demo/' }));

  img.score = img.checks.reduce((s, c) => s + c.points, 0);
  categories.push(img);

  /* ── Analytics & Tracking (NEW — 5 points) ── */
  const track: Category = { name: 'Analytics', score: 0, maxScore: 5, checks: [] };
  const analyticsCount = [analytics.ga4, analytics.gtm, analytics.facebookPixel, analytics.linkedInInsight].filter(Boolean).length;
  track.checks.push(mkCheck('Analytics stack', analyticsCount >= 3 ? 3 : analyticsCount >= 1 ? 2 : 0, 3, analyticsCount >= 1, 'high',
    analytics.details.join('; ') || 'No analytics detected',
    analyticsCount < 3 ? 'Add Google Tag Manager + conversion tracking pixels' : null));

  track.checks.push(mkCheck('Multi-platform tracking', analyticsCount >= 2 ? 2 : 0, 2, analyticsCount >= 2, 'medium',
    `${analyticsCount} platform(s) detected`,
    analyticsCount < 2 ? 'Add Meta Pixel or LinkedIn Insight for retargeting' : null));

  track.score = track.checks.reduce((s, c) => s + c.points, 0);
  categories.push(track);

  /* ── Security (NEW — 5 points) ── */
  const sec: Category = { name: 'Security', score: 0, maxScore: 5, checks: [] };
  const secScore = [security.hsts, security.csp, security.xFrameOptions, security.xContentTypeOptions].filter(Boolean).length;
  sec.checks.push(mkCheck('Security headers', secScore >= 3 ? 3 : secScore >= 1 ? 1 : 0, 3, secScore >= 2, 'high',
    security.details.join('; '),
    secScore < 3 ? 'Add HSTS, X-Frame-Options, and X-Content-Type-Options headers' : null));

  sec.checks.push(mkCheck('HTTPS enforcement', isHttps ? 2 : 0, 2, isHttps, 'critical',
    isHttps ? 'HTTPS enforced' : 'No HTTPS',
    !isHttps ? 'Enable SSL immediately' : null));

  sec.score = sec.checks.reduce((s, c) => s + c.points, 0);
  categories.push(sec);

  /* ── Authority & Backlinks (10) — DataForSEO data ── */
  const auth: Category = { name: 'Authority & Backlinks', score: 0, maxScore: 10, checks: [] };
  if (authority.dataAvailable) {
    const dr = authority.dr;
    const drScore = dr >= 60 ? 3 : dr >= 40 ? 2 : dr >= 20 ? 1 : dr >= 1 ? 0 : 0;
    auth.checks.push(mkCheck('Domain Rating', drScore, 3, drScore >= 1, dr >= 40 ? 'low' : 'high',
      `DR ${dr}/100 — ${dr >= 60 ? 'Strong authority' : dr >= 40 ? 'Good authority' : dr >= 20 ? 'Building authority' : dr >= 1 ? 'Low authority' : 'No authority data'}`,
      dr < 40 ? 'Build backlinks through guest posts, PR, and partnerships' : null,
      { staccFeature: 'Link Building', staccCta: 'Stacc places you in relevant articles', staccLink: '/modules/content-seo/' }));

    const blScore = authority.backlinks >= 1000 ? 2 : authority.backlinks >= 100 ? 1 : authority.backlinks >= 1 ? 0 : 0;
    auth.checks.push(mkCheck('Total backlinks', blScore, 2, blScore >= 1, authority.backlinks >= 100 ? 'low' : 'medium',
      `${authority.backlinks.toLocaleString()} live backlinks`,
      authority.backlinks < 100 ? 'Start a link-building campaign' : null));

    const rdScore = authority.refDomains >= 100 ? 2 : authority.refDomains >= 20 ? 1 : authority.refDomains >= 1 ? 0 : 0;
    auth.checks.push(mkCheck('Referring domains', rdScore, 2, rdScore >= 1, authority.refDomains >= 20 ? 'low' : 'medium',
      `${authority.refDomains.toLocaleString()} referring domains from ${authority.refIps.toLocaleString()} IPs`,
      authority.refDomains < 20 ? 'Diversify your backlink sources' : null));

    const kwScore = authority.totalKeywords >= 100 ? 2 : authority.totalKeywords >= 10 ? 1 : authority.totalKeywords >= 1 ? 0 : 0;
    auth.checks.push(mkCheck('Ranking keywords', kwScore, 2, kwScore >= 1, authority.totalKeywords >= 10 ? 'low' : 'medium',
      `${authority.totalKeywords.toLocaleString()} keywords ranking (${authority.pos1to3} in top 3, ${authority.pos4to10} in top 10)`,
      authority.totalKeywords < 10 ? 'Publish more targeted content' : null,
      { staccFeature: 'Blog SEO Engine', staccCta: 'Stacc targets 30+ keywords monthly', staccLink: '/modules/content-seo/' }));

    const trafficScore = authority.estTraffic >= 1000 ? 1 : authority.estTraffic >= 100 ? 0 : 0;
    auth.checks.push(mkCheck('Organic traffic', trafficScore, 1, trafficScore >= 0, 'low',
      `~${authority.estTraffic.toLocaleString()} visits/mo estimated`,
      authority.estTraffic < 100 ? 'Organic traffic is low — focus on content + links' : null));
  } else {
    // DataForSEO had no data for this domain
    auth.checks.push(mkCheck('Domain Rating', 0, 3, false, 'medium', 'No authority data available (site may be too new or not yet crawled)', 'Continue building content and links'));
    auth.checks.push(mkCheck('Total backlinks', 0, 2, false, 'medium', 'No backlink data available', null));
    auth.checks.push(mkCheck('Referring domains', 0, 2, false, 'medium', 'No referring domain data available', null));
    auth.checks.push(mkCheck('Ranking keywords', 0, 2, false, 'medium', 'No ranking keyword data available', 'Publish more content to start ranking'));
    auth.checks.push(mkCheck('Organic traffic', 0, 1, false, 'low', 'No traffic estimate available', null));
  }
  auth.score = auth.checks.reduce((s, c) => s + c.points, 0);
  categories.push(auth);

  /* ── Calculate overall score with severity penalties ── */
  let rawScore = categories.reduce((s, c) => s + c.score, 0);
  const maxPossible = categories.reduce((s, c) => s + c.maxScore, 0);

  // Severity penalties: critical failures severely reduce the overall score
  let criticalPenalty = 0;
  let criticalFailures = 0;
  for (const cat of categories) {
    for (const check of cat.checks) {
      if (check.severity === 'critical' && !check.passed) {
        criticalPenalty += check.maxPoints; // 100% penalty for each critical failure
        criticalFailures++;
      }
    }
  }

  // Broken site penalty: multiple HTTP 500 errors are devastating
  const brokenPageCount = patterns.pagesWithErrors.filter(e => e.status >= 500).length;
  if (brokenPageCount >= 3) {
    criticalPenalty += maxPossible * 0.15; // Additional 15% penalty for 3+ server errors
  } else if (brokenPageCount >= 1) {
    criticalPenalty += maxPossible * 0.08; // 8% penalty for 1-2 server errors
  }

  // Cap penalty at 50% of total (was 30%)
  criticalPenalty = Math.min(criticalPenalty, maxPossible * 0.5);
  let overallScore = Math.max(0, Math.round(rawScore - criticalPenalty));

  // Normalize to 0-100
  overallScore = Math.round((overallScore / maxPossible) * 100);

  // Tighter grade boundaries to match reference report calibration
  let grade = 'F';
  if (overallScore >= 90) grade = 'A';
  else if (overallScore >= 75) grade = 'B';
  else if (overallScore >= 50) grade = 'C';
  else if (overallScore >= 30) grade = 'D';

  const businessType = kimi?.businessType || 'business';

  return { categories, overallScore, grade, pageSpeedMetrics, businessType };
}

function generatePriorities(categories: Category[]): Priority[] {
  const all: (Check & { category: string })[] = [];
  categories.forEach(c => c.checks.forEach(ch => all.push({ ...ch, category: c.name })));
  // Sort by severity first, then by maxPoints
  return all
    .filter(c => !c.passed && c.fix)
    .sort((a, b) => {
      const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
      const sevDiff = severityOrder[a.severity] - severityOrder[b.severity];
      if (sevDiff !== 0) return sevDiff;
      return b.maxPoints - a.maxPoints;
    })
    .slice(0, 5)
    .map(c => ({ title: c.name, impact: `${c.category} — ${c.severity}`, fix: c.fix || '' }));
}

function generateStaccRecs(categories: Category[], kimi: KimiAnalysis | null): StaccRecommendation[] {
  const recs: StaccRecommendation[] = [];
  const seen = new Set<string>();
  categories.forEach(cat => cat.checks.forEach(ch => {
    if (!ch.passed && ch.staccFeature && ch.staccCta && !seen.has(ch.staccFeature)) {
      seen.add(ch.staccFeature);
      recs.push({ finding: ch.detail, feature: ch.staccFeature, cta: ch.staccCta, link: ch.staccLink || '/demo/' });
    }
  }));
  if (kimi?.staccFeatureMatches) {
    kimi.staccFeatureMatches.forEach(m => {
      if (!seen.has(m.feature)) {
        seen.add(m.feature);
        recs.push({ finding: m.reason, feature: m.feature, cta: m.reason, link: m.link });
      }
    });
  }
  return recs.slice(0, 6);
}

/* ── Main handler ── */
export const POST: APIRoute = async ({ request }) => {
  let body: { url?: string };
  try { body = await request.json(); } catch { return json({ error: 'Invalid request body' }, 400); }

  const rawUrl = body.url?.trim();
  if (!rawUrl) return json({ error: 'URL is required' }, 400);

  const normalized = normalizeUrl(rawUrl);
  if (!normalized) return json({ error: 'Invalid URL format' }, 400);
  const { url, domain } = normalized;

  const cached = getCached(domain);
  if (cached) return json(cached, 200);

  try {
    const startTime = Date.now();

    // 1. Fetch homepage + PageSpeed in parallel
    const [{ html, finalUrl, status, headers }, pageSpeed] = await Promise.all([
      fetchHTML(url),
      fetchPageSpeed(url),
    ]);

    if (status >= 400) return json({ error: `Could not fetch website (HTTP ${status})` }, 502);
    if (html.length < 200) return json({ error: 'Website returned empty or blocked response' }, 502);

    // 2. Detect SPA
    const spa = detectSPA(html);

    // 3. Detect analytics from homepage
    const analytics = detectAnalytics(html);

    // 4. Check security headers
    const security = checkSecurityHeaders(headers);

    // 5. Detect CMS/Technology
    const cms = detectCMS(html);

    // 6. Parse sitemap and crawl pages
    const sitemapUrls = await fetchSitemapUrls(finalUrl);
    const pagesToCrawl = sitemapUrls.length > 0 ? sitemapUrls : [finalUrl];
    const pages = await crawlPages(pagesToCrawl, 50);

    // Ensure homepage is included even if not in sitemap
    const homepageInPages = pages.some(p => p.url.replace(/\/+$/, '') === finalUrl.replace(/\/+$/, ''));
    let allPages = pages;
    if (!homepageInPages) {
      const homepageParsed = parsePageHTML(html, finalUrl);
      allPages = [{ ...homepageParsed, url: finalUrl, status }, ...pages];
    }

    // 7. Analyze sitewide patterns
    const patterns = analyzeSitewidePatterns(allPages);

    // 8. Check robots.txt and sitemap existence
    const [robotsTxtResult, sitemapResult] = await Promise.all([
      checkFileExists(`${new URL(finalUrl).origin}/robots.txt`),
      checkFileExists(`${new URL(finalUrl).origin}/sitemap.xml`),
    ]);

    // 9. Parse robots.txt content
    const robotsParsed = robotsTxtResult.exists && robotsTxtResult.content
      ? parseRobotsTxt(robotsTxtResult.content)
      : { aiCrawlerBlocks: [], crawlDelay: null, disallowedPaths: [], hasSitemapRef: false };

    // 10. Detect E-E-A-T and Local SEO
    const allSchemaTypes = [...new Set(allPages.flatMap(p => p.schemaTypes))];
    const eeatLocal = detectEeatAndLocal(html, allSchemaTypes, allPages);

    // 11. Content freshness and orphan detection
    const sitemapContent = sitemapResult.exists ? sitemapResult.content : undefined;
    const freshness = analyzeFreshnessAndOrphans(sitemapContent, allPages, finalUrl);

    const homepage = allPages.find(p => p.url.replace(/\/+$/, '') === finalUrl.replace(/\/+$/, '')) || allPages[0];

    // 12. New detections
    const redirectChain = await detectRedirectChain(finalUrl);
    const mixedContent = detectMixedContent(html, finalUrl);
    const soft404s = detectSoft404s(allPages);
    const socialTags = analyzeSocialTags(homepage);
    const hreflangData = analyzeHreflang(homepage);
    const llmsTxt = await checkLlmsTxt(domain);
    const passageStructure = analyzePassageStructure(allPages);
    const freshnessScore = freshness.averageAgeDays !== null
      ? Math.max(0, 100 - Math.round(freshness.averageAgeDays / 3))
      : 50;
    const geoAioData: GeoAioResult = {
      llmsTxt,
      passageStructure,
      brandMentions: [],
      entityDensity: 0,
      freshnessScore,
    };

    // 13. DataForSEO authority data (parallel with AI)
    const [backlinksData, rankedKeywordsData] = await Promise.all([
      getBacklinksSummary(domain).catch(() => null),
      getRankedKeywords(domain).catch(() => null),
    ]);

    const authorityData: AuthorityData = {
      dr: backlinksData?.drNormalized ?? 0,
      backlinks: backlinksData?.backlinks ?? 0,
      refDomains: backlinksData?.refDomains ?? 0,
      refIps: backlinksData?.refIps ?? 0,
      brokenBacklinks: backlinksData?.brokenBacklinks ?? 0,
      totalKeywords: rankedKeywordsData?.total ?? 0,
      pos1to3: rankedKeywordsData?.pos1to3 ?? 0,
      pos4to10: rankedKeywordsData?.pos4to10 ?? 0,
      pos11to20: rankedKeywordsData?.pos11to20 ?? 0,
      pos21to50: rankedKeywordsData?.pos21to50 ?? 0,
      pos51to100: rankedKeywordsData?.pos51to100 ?? 0,
      estTraffic: rankedKeywordsData?.estTraffic ?? 0,
      topKeywords: rankedKeywordsData?.topKeywords ?? [],
      dataAvailable: !!(backlinksData || rankedKeywordsData),
    };

    // 14. AI deep analysis
    const kimiPromise = callAI(
      'You are an expert SEO analyst. Return ONLY valid JSON. Be specific about competitors and content gaps.',
      buildKimiPrompt(homepage, allPages, patterns, analytics, security, spa, pageSpeed, domain, robotsParsed, cms, eeatLocal, freshness, authorityData)
    );

    let kimiResult: KimiAnalysis | null = null;
    try { kimiResult = await kimiPromise; } catch { /* Kimi is optional */ }

    // 15. Score with multi-page data + authority
    const { categories, overallScore, grade, pageSpeedMetrics, businessType } = scoreAudit(
      homepage, allPages, patterns, analytics, security, spa,
      pageSpeed, robotsTxtResult.exists, sitemapResult.exists, kimiResult, finalUrl, robotsParsed,
      redirectChain, mixedContent, soft404s, socialTags, hreflangData, geoAioData, authorityData
    );

    const topPriorities = generatePriorities(categories);
    if (kimiResult?.topRecommendations && topPriorities.length < 3) {
      kimiResult.topRecommendations.slice(0, 3 - topPriorities.length).forEach(r => {
        topPriorities.push({ title: r, impact: 'AI Analysis', fix: 'See full report for details' });
      });
    }

    const staccRecommendations = generateStaccRecs(categories, kimiResult);

    const result: AuditResult = {
      success: true,
      domain,
      url: finalUrl,
      overallScore,
      grade,
      businessType,
      categories,
      topPriorities,
      staccRecommendations,
      serpPreview: { title: homepage.title || domain, description: homepage.metaDescription || `Learn more about ${domain}`, url: finalUrl },
      pageSpeed: pageSpeedMetrics,
      fetchTime: Date.now() - startTime,
      pagesAudited: allPages.length,
      isSPA: spa.isSPA,
      spaFramework: spa.framework,
      analytics,
      security,
      sitewide: patterns,
      competitorHint: kimiResult?.estimatedContentGap || 'Competitive analysis requires manual research',
      robotsTxt: robotsParsed,
      cms,
      eeat: { eeatScore: eeatLocal.eeatScore, eeatDetails: eeatLocal.eeatDetails, hasTestimonials: eeatLocal.hasTestimonials, hasTeamPage: eeatLocal.hasTeamPage, hasReviews: eeatLocal.hasReviews },
      local: { localScore: eeatLocal.localScore, localDetails: eeatLocal.localDetails, hasGbpLink: eeatLocal.hasGbpLink },
      freshness,
      socialTags,
      redirectChain,
      mixedContent,
      soft404s,
      hreflang: hreflangData,
      geoAio: geoAioData,
      authority: authorityData,
    };

    setCached(domain, result);
    return json(result, 200);

  } catch (err) {
    console.error('[audit]', err);
    return json({ error: 'Failed to analyze website. Please try again.' }, 500);
  }
};

function json(body: object, status: number) {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
}
