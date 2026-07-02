export const prerender = false;

import type { APIRoute } from 'astro';

interface CrawledPage {
  url: string;
  title: string;
  pageType: string;
  changefreq: string;
  priority: number;
  lastmod: string;
  depth: number;
  internalLinks: number;
  status: number;
  statusText: string;
  noindex: boolean;
  canonical: string | null;
}

interface CrawlIssue {
  type: 'broken_link' | 'redirect' | 'noindex' | 'timeout' | 'error';
  url: string;
  status?: number;
  message?: string;
  foundOn?: string;
}

interface CrawlStats {
  totalPages: number;
  crawlTimeMs: number;
  brokenLinks: number;
  redirects: number;
  noindexPages: number;
  maxDepthReached: number;
}

interface TreeNode {
  name: string;
  url: string;
  type: string;
  priority: number;
  children: TreeNode[];
}

interface ValidationResult {
  status: 'valid' | 'warnings' | 'errors';
  warnings: string[];
  errors: string[];
}

interface SitemapResponse {
  ok: boolean;
  data?: {
    crawlStats: CrawlStats;
    pages: CrawledPage[];
    issues: CrawlIssue[];
    xmlSitemap: string;
    validation: ValidationResult;
    treeData: TreeNode;
  };
  error?: string;
}

const USER_AGENT = 'Mozilla/5.0 (compatible; theStaccBot/1.0; +https://thestacc.com)';
const MAX_BODY_SIZE = 2 * 1024 * 1024; // 2MB
const FETCH_TIMEOUT = 5000; // 5s per page

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  const startTime = Date.now();
  let body: { url?: string; maxDepth?: number; maxPages?: number };

  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: 'Invalid request body' }, 400);
  }

  let url = body.url?.trim() || '';
  const maxDepth = Math.min(Math.max(body.maxPages || 3, 1), 5);
  const maxPages = Math.min(Math.max(body.maxPages || 100, 10), 500);

  if (!url) {
    return json({ ok: false, error: 'URL is required' }, 400);
  }

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

  // ── Check robots.txt ─────────────────────────────────────────
  let robotsDisallowed: string[] = [];
  try {
    robotsDisallowed = await fetchRobotsDisallowed(origin);
  } catch {
    // Continue without robots.txt
  }

  // ── BFS Crawl (with concurrency) ─────────────────────────────
  const visited = new Set<string>();
  const queue: { url: string; depth: number }[] = [{ url: origin + '/', depth: 0 }];
  const pages: CrawledPage[] = [];
  const issues: CrawlIssue[] = [];
  let maxDepthReached = 0;
  const MAX_CRAWL_TIME = 15000; // 15 seconds max
  const CONCURRENCY = 5;

  while (queue.length > 0 && pages.length < maxPages) {
    // Stop if we've exceeded max crawl time
    if (Date.now() - startTime > MAX_CRAWL_TIME) {
      issues.push({ type: 'timeout', url: origin, message: 'Crawl stopped after 25 seconds to keep response fast' });
      break;
    }

    // Process up to CONCURRENCY pages in parallel
    const batch: { url: string; depth: number }[] = [];
    while (batch.length < CONCURRENCY && queue.length > 0) {
      const item = queue.shift()!;
      if (visited.has(item.url) || item.depth > maxDepth) continue;

      const normalized = normalizeUrl(item.url);
      if (visited.has(normalized)) continue;

      if (isDisallowedByRobots(item.url, robotsDisallowed)) continue;

      visited.add(normalized);
      visited.add(item.url);
      batch.push(item);
    }

    if (batch.length === 0) continue;

    // Crawl batch in parallel
    const results = await Promise.all(
      batch.map((item) => crawlPage(item.url, item.depth, origin))
    );

    for (let i = 0; i < batch.length; i++) {
      const item = batch[i];
      const result = results[i];

      if (result.page) {
        pages.push(result.page);
        maxDepthReached = Math.max(maxDepthReached, item.depth);

        // Add internal links to queue
        if (item.depth < maxDepth) {
          for (const link of result.links) {
            const normLink = normalizeUrl(link);
            if (!visited.has(normLink) && !visited.has(link)) {
              queue.push({ url: link, depth: item.depth + 1 });
            }
          }
        }
      }

      issues.push(...result.issues);
    }
  }

  // ── Sort and dedupe ──────────────────────────────────────────
  const uniquePages = dedupePages(pages);
  uniquePages.sort((a, b) => b.priority - a.priority || a.url.localeCompare(b.url));

  // ── Generate XML ─────────────────────────────────────────────
  const xmlSitemap = generateXML(uniquePages, origin);

  // ── Validate ─────────────────────────────────────────────────
  const validation = validateSitemap(xmlSitemap, uniquePages);

  // ── Build tree ───────────────────────────────────────────────
  const treeData = buildTree(uniquePages, domain);

  // ── Stats ────────────────────────────────────────────────────
  const crawlTimeMs = Date.now() - startTime;
  const stats: CrawlStats = {
    totalPages: uniquePages.length,
    crawlTimeMs,
    brokenLinks: issues.filter(i => i.type === 'broken_link').length,
    redirects: issues.filter(i => i.type === 'redirect').length,
    noindexPages: uniquePages.filter(p => p.noindex).length,
    maxDepthReached,
  };

  return json({
    ok: true,
    data: {
      crawlStats: stats,
      pages: uniquePages,
      issues,
      xmlSitemap,
      validation,
      treeData,
    },
  } as SitemapResponse, 200);
};

// ── Crawl a single page ────────────────────────────────────────

async function crawlPage(
  url: string,
  depth: number,
  origin: string
): Promise<{ page: CrawledPage | null; links: string[]; issues: CrawlIssue[] }> {
  const issues: CrawlIssue[] = [];

  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT);

    const res = await fetch(url, {
      signal: controller.signal,
      headers: {
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      },
      redirect: 'follow',
    });
    clearTimeout(timer);

    if (!res.ok) {
      issues.push({ type: 'broken_link', url, status: res.status, message: res.statusText });
      return { page: null, links: [], issues };
    }

    const contentType = res.headers.get('content-type') || '';
    if (!contentType.includes('text/html')) {
      return { page: null, links: [], issues };
    }

    // Limit body size
    const body = await res.text();
    const truncated = body.length > MAX_BODY_SIZE ? body.slice(0, MAX_BODY_SIZE) : body;

    // Extract data
    const title = extractTitle(truncated);
    const metaRobots = extractMetaRobots(truncated);
    const canonical = extractCanonical(truncated, origin);
    const noindex = metaRobots.includes('noindex');
    const lastmod = extractLastMod(res.headers.get('last-modified'));

    // Extract links
    const links = extractLinks(truncated, origin, url);

    // Classify page type
    const pageType = classifyPageType(url, title);

    // Calculate priority and changefreq
    const priority = calculatePriority(depth, links.length, pageType);
    const changefreq = detectChangefreq(pageType, lastmod);

    const page: CrawledPage = {
      url,
      title,
      pageType,
      changefreq,
      priority: Math.round(priority * 10) / 10,
      lastmod,
      depth,
      internalLinks: links.length,
      status: res.status,
      statusText: res.statusText,
      noindex,
      canonical,
    };

    return { page: noindex ? null : page, links: noindex ? [] : links, issues };
  } catch (err: any) {
    if (err.name === 'AbortError') {
      issues.push({ type: 'timeout', url, message: 'Request timed out' });
    } else {
      issues.push({ type: 'error', url, message: err.message });
    }
    return { page: null, links: [], issues };
  }
}

// ── HTML extraction ────────────────────────────────────────────

function extractTitle(html: string): string {
  const match = html.match(/<title[^>]*>([^<]*)<\/title>/i);
  return match ? match[1].trim() : '';
}

function extractMetaRobots(html: string): string {
  const match = html.match(/<meta[^>]*name=["']robots["'][^>]*content=["']([^"']*)["'][^>]*>/i)
    || html.match(/<meta[^>]*content=["']([^"']*)["'][^>]*name=["']robots["'][^>]*>/i);
  return match ? match[1].toLowerCase() : '';
}

function extractCanonical(html: string, origin: string): string | null {
  const match = html.match(/<link[^>]*rel=["']canonical["'][^>]*href=["']([^"']*)["'][^>]*>/i)
    || html.match(/<link[^>]*href=["']([^"']*)["'][^>]*rel=["']canonical["'][^>]*>/i);
  return match ? resolveUrl(match[1], origin) : null;
}

function extractLinks(html: string, origin: string, baseUrl: string): string[] {
  const links: string[] = [];
  const seen = new Set<string>();
  const regex = /<a[^>]*href=["']([^"']+)["'][^>]*>/gi;
  let match;

  while ((match = regex.exec(html)) !== null) {
    const href = match[1].trim();
    if (!href || href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) continue;

    const resolved = resolveUrl(href, baseUrl);
    if (!resolved) continue;

    const parsed = new URL(resolved);
    if (parsed.origin !== origin) continue;
    if (isAssetUrl(parsed.pathname)) continue;

    const normalized = normalizeUrl(resolved);
    if (!seen.has(normalized)) {
      seen.add(normalized);
      links.push(normalized);
    }
  }

  return links;
}

function isAssetUrl(path: string): boolean {
  const ext = path.split('.').pop()?.toLowerCase();
  return ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp', 'css', 'js', 'pdf', 'zip', 'mp4', 'mp3', 'woff', 'woff2', 'ttf', 'ico'].includes(ext || '');
}

// ── URL utilities ──────────────────────────────────────────────

function resolveUrl(href: string, base: string): string | null {
  try {
    return new URL(href, base).href;
  } catch {
    return null;
  }
}

function normalizeUrl(url: string): string {
  try {
    const parsed = new URL(url);
    parsed.hash = '';
    // Remove trailing slash for consistency, except root
    if (parsed.pathname.length > 1 && parsed.pathname.endsWith('/')) {
      parsed.pathname = parsed.pathname.slice(0, -1);
    }
    return parsed.href;
  } catch {
    return url;
  }
}

function isDisallowedByRobots(url: string, disallowed: string[]): boolean {
  const pathname = new URL(url).pathname;
  return disallowed.some(d => pathname.startsWith(d));
}

// ── robots.txt ─────────────────────────────────────────────────

async function fetchRobotsDisallowed(origin: string): Promise<string[]> {
  try {
    const res = await fetch(`${origin}/robots.txt`, {
      headers: { 'User-Agent': USER_AGENT },
      signal: AbortSignal.timeout(5000),
    });
    if (!res.ok) return [];

    const text = await res.text();
    const disallowed: string[] = [];
    let inOurBlock = false;

    for (const line of text.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;

      const lower = trimmed.toLowerCase();
      if (lower.startsWith('user-agent:')) {
        const ua = lower.split(':')[1]?.trim() || '';
        // Only match wildcard (*) or our specific bot name
        inOurBlock = ua === '*' || ua.includes('stacc');
      } else if (inOurBlock && lower.startsWith('disallow:')) {
        const path = trimmed.split(':').slice(1).join(':').trim();
        if (path) disallowed.push(path);
      }
    }

    return disallowed;
  } catch {
    return [];
  }
}

// ── Page classification ────────────────────────────────────────

function classifyPageType(url: string, title: string): string {
  const path = new URL(url).pathname.toLowerCase();
  const tl = title.toLowerCase();

  if (path === '/' || path === '') return 'homepage';
  if (path.includes('/blog/') || path.includes('/article') || path.includes('/post')) return 'blog_post';
  if (path.includes('/product') || path.includes('/shop/') || path.includes('/item/')) return 'product';
  if (path.includes('/category') || path.includes('/tag/') || path.includes('/topic/')) return 'category';
  if (path.includes('/about')) return 'about';
  if (path.includes('/contact')) return 'contact';
  if (path.includes('/faq') || path.includes('/help')) return 'faq';
  if (path.includes('/pricing') || path.includes('/plan')) return 'pricing';
  if (path.includes('/docs') || path.includes('/documentation') || path.includes('/guide')) return 'documentation';
  if (path.includes('/portfolio') || path.includes('/work') || path.includes('/project')) return 'portfolio';
  if (path.includes('/service')) return 'service';
  if (path.includes('/testimonial') || path.includes('/review')) return 'testimonial';
  if (path.includes('/team') || path.includes('/career')) return 'team';
  if (path.includes('/news') || path.includes('/press')) return 'news';
  if (tl.includes('home')) return 'homepage';
  if (tl.includes('blog') || tl.includes('article') || tl.includes('post')) return 'blog_post';

  return 'page';
}

// ── Priority scoring ───────────────────────────────────────────

function calculatePriority(depth: number, linkCount: number, pageType: string): number {
  // Base by page type
  const typeScores: Record<string, number> = {
    homepage: 1.0,
    product: 0.8,
    blog_post: 0.7,
    category: 0.8,
    documentation: 0.7,
    about: 0.6,
    contact: 0.6,
    pricing: 0.7,
    service: 0.7,
    portfolio: 0.6,
    faq: 0.5,
    news: 0.6,
    team: 0.4,
    testimonial: 0.4,
    page: 0.5,
  };

  let score = typeScores[pageType] || 0.5;

  // Depth penalty (closer to homepage = higher)
  score -= depth * 0.05;

  // Link count bonus
  if (linkCount > 10) score += 0.05;
  if (linkCount > 20) score += 0.05;

  return Math.min(Math.max(score, 0.1), 1.0);
}

// ── Changefreq detection ───────────────────────────────────────

function detectChangefreq(pageType: string, lastmod: string): string {
  const freqMap: Record<string, string> = {
    homepage: 'daily',
    news: 'daily',
    blog_post: 'weekly',
    product: 'weekly',
    category: 'weekly',
    documentation: 'weekly',
    pricing: 'monthly',
    about: 'monthly',
    contact: 'monthly',
    service: 'monthly',
    portfolio: 'monthly',
    faq: 'monthly',
    team: 'monthly',
    testimonial: 'yearly',
    page: 'monthly',
  };

  return freqMap[pageType] || 'monthly';
}

function extractLastMod(headerValue: string | null): string {
  if (headerValue) {
    const date = new Date(headerValue);
    if (!isNaN(date.getTime())) {
      return date.toISOString().split('T')[0];
    }
  }
  return new Date().toISOString().split('T')[0];
}

// ── Deduplication ──────────────────────────────────────────────

function dedupePages(pages: CrawledPage[]): CrawledPage[] {
  const seen = new Set<string>();
  const result: CrawledPage[] = [];

  for (const page of pages) {
    const key = normalizeUrl(page.url);
    if (!seen.has(key)) {
      seen.add(key);
      result.push(page);
    }
  }

  return result;
}

// ── XML generation ─────────────────────────────────────────────

function generateXML(pages: CrawledPage[], origin: string): string {
  const today = new Date().toISOString().split('T')[0];

  const lines: string[] = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    '  <!-- Generated by theStacc Sitemap Generator -->',
    `  <!-- ${origin} -->`,
    `  <!-- ${today} -->`,
  ];

  for (const page of pages) {
    lines.push('  <url>');
    lines.push(`    <loc>${escapeXml(page.url)}</loc>`);
    lines.push(`    <lastmod>${page.lastmod}</lastmod>`);
    lines.push(`    <changefreq>${page.changefreq}</changefreq>`);
    lines.push(`    <priority>${page.priority.toFixed(1)}</priority>`);
    lines.push('  </url>');
  }

  lines.push('</urlset>');
  return lines.join('\n');
}

// ── Tree building ──────────────────────────────────────────────

function buildTree(pages: CrawledPage[], domain: string): TreeNode {
  const root: TreeNode = {
    name: domain,
    url: '',
    type: 'homepage',
    priority: 1.0,
    children: [],
  };

  // Group pages by path segments
  const pathMap = new Map<string, TreeNode>();
  pathMap.set('/', root);

  for (const page of pages) {
    const parsed = new URL(page.url);
    const segments = parsed.pathname.split('/').filter(Boolean);

    let parent = root;
    let currentPath = '';

    for (let i = 0; i < segments.length; i++) {
      const segment = segments[i];
      currentPath += '/' + segment;

      if (!pathMap.has(currentPath)) {
        const node: TreeNode = {
          name: segment,
          url: '',
          type: 'page',
          priority: 0.5,
          children: [],
        };
        pathMap.set(currentPath, node);
        parent.children.push(node);
      }

      parent = pathMap.get(currentPath)!;
    }

    // Update leaf node with actual page data
    const leaf = pathMap.get(parsed.pathname) || parent;
    leaf.url = page.url;
    leaf.type = page.pageType;
    leaf.priority = page.priority;
  }

  // Sort children by priority
  sortTree(root);
  return root;
}

function sortTree(node: TreeNode) {
  node.children.sort((a, b) => b.priority - a.priority);
  node.children.forEach(sortTree);
}

// ── Validation ─────────────────────────────────────────────────

function validateSitemap(xml: string, pages: CrawledPage[]): ValidationResult {
  const warnings: string[] = [];
  const errors: string[] = [];

  if (!xml.includes('<?xml version="1.0"')) {
    errors.push('Missing XML declaration');
  }

  if (!xml.includes('<urlset')) {
    errors.push('Missing urlset element');
  }

  if (!xml.includes('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')) {
    errors.push('Missing sitemap.org namespace');
  }

  if (pages.length === 0) {
    errors.push('No URLs in sitemap');
  }

  if (pages.length > 50000) {
    errors.push('Sitemap exceeds 50,000 URL limit');
  }

  const sizeInBytes = new Blob([xml]).size;
  if (sizeInBytes > 50 * 1024 * 1024) {
    errors.push('Sitemap exceeds 50MB size limit');
  }

  // Check for duplicate URLs
  const urls = pages.map(p => p.url);
  const duplicates = urls.filter((item, index) => urls.indexOf(item) !== index);
  if (duplicates.length > 0) {
    warnings.push(`${new Set(duplicates).size} duplicate URL(s) found`);
  }

  // Check for invalid URLs
  const invalidUrls = pages.filter(p => {
    try { new URL(p.url); return false; } catch { return true; }
  });
  if (invalidUrls.length > 0) {
    warnings.push(`${invalidUrls.length} invalid URL(s) found`);
  }

  // Check for noindex pages in sitemap
  const noindexInSitemap = pages.filter(p => p.noindex);
  if (noindexInSitemap.length > 0) {
    warnings.push(`${noindexInSitemap.length} noindex page(s) included in sitemap`);
  }

  const status = errors.length > 0 ? 'errors' : warnings.length > 0 ? 'warnings' : 'valid';
  return { status, warnings, errors };
}

// ── Helpers ────────────────────────────────────────────────────

function escapeXml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}
