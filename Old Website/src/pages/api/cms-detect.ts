export const prerender = false;

import type { APIRoute } from 'astro';
import {
  SIGNATURES,
  SIGNATURE_MAP,
  CATEGORY_META,
  type Category,
  type Signature,
} from '../../lib/cms-signatures';

/* ════════════════════════════════════════════════════════════════
   CMS Detector API — v1
   ----------------------------------------------------------------
   POST /api/cms-detect
   Body: { "url": "example.com" }
   ════════════════════════════════════════════════════════════════ */

const FETCH_TIMEOUT_MS = 12_000;
const MAX_BODY_BYTES = 2 * 1024 * 1024; // 2 MB
const USER_AGENT =
  'Mozilla/5.0 (compatible; theStacc-CMS-Detector/1.0; +https://thestacc.com/tools/cms-detector/)';

/* ── In-memory LRU cache (1h TTL, 200 entries) ─────────────── */
interface CacheEntry {
  data: DetectionResult;
  expiresAt: number;
}
const CACHE_TTL_MS = 60 * 60 * 1000;
const MAX_CACHE = 200;
const cache = new Map<string, CacheEntry>();

function cacheGet(key: string): DetectionResult | null {
  const e = cache.get(key);
  if (!e) return null;
  if (Date.now() > e.expiresAt) {
    cache.delete(key);
    return null;
  }
  return e.data;
}
function cacheSet(key: string, data: DetectionResult) {
  if (cache.size >= MAX_CACHE) {
    const first = cache.keys().next().value;
    if (first) cache.delete(first);
  }
  cache.set(key, { data, expiresAt: Date.now() + CACHE_TTL_MS });
}

/* ── Result types ──────────────────────────────────────────── */
type Confidence = 'high' | 'medium' | 'low';

interface DetectedTech {
  name: string;
  category: Category;
  categoryLabel: string;
  version: string | null;
  confidence: Confidence;
  score: number;
  icon: string | null;
  url: string | null;
  description: string | null;
  signals: string[];
}

interface DetectionResult {
  ok: true;
  url: string;
  finalUrl: string;
  fetchedAt: number;
  responseStatus: number;
  responseTimeMs: number;
  primary: { name: string; category: Category; version: string | null; confidence: Confidence } | null;
  technologies: DetectedTech[];
  byCategory: Record<string, DetectedTech[]>;
  totalDetected: number;
  insights: {
    isStaticSite: boolean;
    isJsHeavy: boolean;
    hasEcommerce: boolean;
    securityHeaders: { name: string; present: boolean }[];
  };
  redirected: boolean;
  fromCache: boolean;
}

interface DetectionError {
  ok: false;
  error: string;
  message: string;
  url?: string;
}

/* ── URL validation & SSRF guard ───────────────────────────── */
function normalizeUrl(input: string): string {
  let url = input.trim();
  if (!url) throw new Error('Empty URL');
  if (!/^https?:\/\//i.test(url)) url = 'https://' + url;
  // Strip trailing slash for cache key consistency
  return url.replace(/\/+$/, '');
}

function isPrivateHost(hostname: string): boolean {
  const h = hostname.toLowerCase();
  if (h === 'localhost' || h === '0.0.0.0' || h.endsWith('.local') || h.endsWith('.localhost')) return true;
  // IPv4 private ranges
  const v4 = h.match(/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/);
  if (v4) {
    const [, a, b] = v4.map(Number);
    if (a === 10) return true;
    if (a === 127) return true;
    if (a === 172 && b >= 16 && b <= 31) return true;
    if (a === 192 && b === 168) return true;
    if (a === 169 && b === 254) return true; // link-local
    if (a === 0) return true;
  }
  // IPv6 loopback / link-local / unique-local
  if (h === '::1' || h.startsWith('fe80:') || h.startsWith('fc') || h.startsWith('fd')) return true;
  return false;
}

/* ── Fetch with timeout & size cap ─────────────────────────── */
interface FetchOutcome {
  finalUrl: string;
  status: number;
  headers: Record<string, string>;
  rawSetCookie: string[];
  body: string;
  responseTimeMs: number;
}

async function fetchSite(url: string): Promise<FetchOutcome> {
  const start = Date.now();
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

  try {
    const res = await fetch(url, {
      method: 'GET',
      headers: {
        'User-Agent': USER_AGENT,
        Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
      },
      signal: controller.signal,
      redirect: 'follow',
    });

    // Headers — Header keys are lowercased
    const headers: Record<string, string> = {};
    res.headers.forEach((v, k) => {
      headers[k.toLowerCase()] = v;
    });

    // Set-Cookie can have multiple values
    const rawSetCookie: string[] = [];
    if (typeof (res.headers as any).getSetCookie === 'function') {
      rawSetCookie.push(...(res.headers as any).getSetCookie());
    } else if (headers['set-cookie']) {
      rawSetCookie.push(headers['set-cookie']);
    }

    // Read body up to MAX_BODY_BYTES
    const reader = res.body?.getReader();
    let received = 0;
    const chunks: Uint8Array[] = [];
    if (reader) {
      while (received < MAX_BODY_BYTES) {
        const { done, value } = await reader.read();
        if (done) break;
        if (value) {
          chunks.push(value);
          received += value.length;
          if (received >= MAX_BODY_BYTES) {
            try {
              await reader.cancel();
            } catch {}
            break;
          }
        }
      }
    }
    const merged = new Uint8Array(received);
    let off = 0;
    for (const c of chunks) {
      merged.set(c.subarray(0, Math.min(c.length, received - off)), off);
      off += c.length;
      if (off >= received) break;
    }
    const body = new TextDecoder('utf-8').decode(merged);

    return {
      finalUrl: res.url || url,
      status: res.status,
      headers,
      rawSetCookie,
      body,
      responseTimeMs: Date.now() - start,
    };
  } finally {
    clearTimeout(timer);
  }
}

/* ── Signal evaluation ─────────────────────────────────────── */
interface MatchAccumulator {
  scoreByName: Map<string, number>;
  signalsByName: Map<string, Set<string>>;
  versionByName: Map<string, string>;
}

function setVersion(acc: MatchAccumulator, name: string, version: string | undefined) {
  if (!version) return;
  const cleaned = version.trim();
  if (!cleaned) return;
  if (!acc.versionByName.has(name)) acc.versionByName.set(name, cleaned);
}

function addSignal(acc: MatchAccumulator, name: string, signal: string, score: number) {
  acc.scoreByName.set(name, (acc.scoreByName.get(name) || 0) + score);
  if (!acc.signalsByName.has(name)) acc.signalsByName.set(name, new Set());
  acc.signalsByName.get(name)!.add(signal);
}

function evaluateSignature(sig: Signature, fetched: FetchOutcome, hostname: string, acc: MatchAccumulator) {
  const s = sig.signals;

  // Headers
  if (s.headers) {
    for (const h of s.headers) {
      const val = fetched.headers[h.name.toLowerCase()];
      if (!val) continue;
      const m = val.match(h.pattern);
      if (m) {
        addSignal(acc, sig.name, `header:${h.name}=${truncate(val, 80)}`, 3);
        if (h.versionGroup && m[h.versionGroup]) {
          setVersion(acc, sig.name, m[h.versionGroup]);
        }
      }
    }
  }

  // Cookies (from Set-Cookie headers)
  if (s.cookies) {
    for (const c of s.cookies) {
      const hit = fetched.rawSetCookie.find((sc) => c.pattern.test(sc));
      if (hit) {
        addSignal(acc, sig.name, `cookie:${truncate(hit, 60)}`, 3);
      }
    }
  }

  // Meta generator
  if (s.metaGenerator) {
    // Find <meta name="generator" content="...">
    const re = /<meta[^>]+name=["']generator["'][^>]+content=["']([^"']+)["']/gi;
    let mg: RegExpExecArray | null;
    while ((mg = re.exec(fetched.body)) !== null) {
      const content = mg[1];
      const m = content.match(s.metaGenerator.pattern);
      if (m) {
        addSignal(acc, sig.name, `meta-generator:${truncate(content, 80)}`, 3);
        if (s.metaGenerator.versionGroup && m[s.metaGenerator.versionGroup]) {
          setVersion(acc, sig.name, m[s.metaGenerator.versionGroup]);
        }
        break;
      }
    }
  }

  // HTML patterns
  if (s.html) {
    for (const h of s.html) {
      const m = fetched.body.match(h.pattern);
      if (m) {
        const w = h.weight ?? 2;
        if (w > 0) addSignal(acc, sig.name, `html:${truncate(m[0], 60)}`, w);
        if (h.versionGroup && m[h.versionGroup]) {
          setVersion(acc, sig.name, m[h.versionGroup]);
        }
      }
    }
  }

  // Script src — find all script tags first, then test
  if (s.scriptSrc) {
    const scriptRe = /<script[^>]+src=["']([^"']+)["']/gi;
    const sources: string[] = [];
    let m: RegExpExecArray | null;
    while ((m = scriptRe.exec(fetched.body)) !== null) {
      sources.push(m[1]);
    }
    for (const ss of s.scriptSrc) {
      for (const src of sources) {
        const sm = src.match(ss.pattern);
        if (sm) {
          addSignal(acc, sig.name, `script:${truncate(src, 80)}`, 1);
          if (ss.versionGroup && sm[ss.versionGroup]) {
            setVersion(acc, sig.name, sm[ss.versionGroup]);
          }
          break;
        }
      }
    }
  }

  // Domain pattern
  if (s.domain) {
    if (s.domain.pattern.test(hostname)) {
      addSignal(acc, sig.name, `domain:${hostname}`, 3);
    }
  }
}

function truncate(str: string, n: number): string {
  if (str.length <= n) return str;
  return str.slice(0, n - 1) + '…';
}

/* ── Confidence calculation ────────────────────────────────── */
function scoreToConfidence(score: number): Confidence {
  if (score >= 5) return 'high';
  if (score >= 3) return 'medium';
  return 'low';
}

/* ── Apply implies relationships ───────────────────────────── */
function applyImplies(acc: MatchAccumulator) {
  // Multiple passes in case A implies B implies C
  for (let pass = 0; pass < 3; pass++) {
    const detectedNames = new Set(acc.scoreByName.keys());
    let added = false;
    for (const name of detectedNames) {
      const sig = SIGNATURE_MAP.get(name);
      if (!sig?.implies) continue;
      for (const impliedName of sig.implies) {
        if (!acc.scoreByName.has(impliedName) && SIGNATURE_MAP.has(impliedName)) {
          addSignal(acc, impliedName, `implied-by:${name}`, 3);
          added = true;
        }
      }
    }
    if (!added) break;
  }
}

/* ── Main detection ────────────────────────────────────────── */
function detect(fetched: FetchOutcome, hostname: string): DetectionResult['technologies'] {
  const acc: MatchAccumulator = {
    scoreByName: new Map(),
    signalsByName: new Map(),
    versionByName: new Map(),
  };

  for (const sig of SIGNATURES) {
    evaluateSignature(sig, fetched, hostname, acc);
  }

  applyImplies(acc);

  const techs: DetectedTech[] = [];
  for (const [name, score] of acc.scoreByName.entries()) {
    const sig = SIGNATURE_MAP.get(name);
    if (!sig) continue;
    if ((sig.minScore ?? 1) > score) continue;
    techs.push({
      name,
      category: sig.category,
      categoryLabel: CATEGORY_META[sig.category].label,
      version: acc.versionByName.get(name) || null,
      confidence: scoreToConfidence(score),
      score,
      icon: sig.icon || null,
      url: sig.url || null,
      description: sig.description || null,
      signals: Array.from(acc.signalsByName.get(name) || []).slice(0, 5),
    });
  }

  // Sort by category order, then score desc, then name
  techs.sort((a, b) => {
    const oa = CATEGORY_META[a.category].order;
    const ob = CATEGORY_META[b.category].order;
    if (oa !== ob) return oa - ob;
    if (a.score !== b.score) return b.score - a.score;
    return a.name.localeCompare(b.name);
  });

  return techs;
}

/* ── Insights post-processing ──────────────────────────────── */
function buildInsights(
  techs: DetectedTech[],
  fetched: FetchOutcome
): DetectionResult['insights'] {
  const names = new Set(techs.map((t) => t.name));
  const isJsHeavy = names.has('React') || names.has('Vue.js') || names.has('Angular') || names.has('Next.js') || names.has('Nuxt') || names.has('Remix') || names.has('SvelteKit');
  const ssgMarkers = ['Astro', 'Hugo', 'Jekyll', 'Eleventy', 'Gatsby', 'Docusaurus'];
  const isStaticSite = ssgMarkers.some((n) => names.has(n));
  const ecommNames = ['Shopify', 'WooCommerce', 'Magento', 'BigCommerce', 'PrestaShop', 'OpenCart', 'Square Online'];
  const hasEcommerce = ecommNames.some((n) => names.has(n));

  const securityHeaders = [
    { name: 'Strict-Transport-Security', key: 'strict-transport-security' },
    { name: 'Content-Security-Policy', key: 'content-security-policy' },
    { name: 'X-Frame-Options', key: 'x-frame-options' },
    { name: 'X-Content-Type-Options', key: 'x-content-type-options' },
    { name: 'Referrer-Policy', key: 'referrer-policy' },
    { name: 'Permissions-Policy', key: 'permissions-policy' },
  ].map((h) => ({ name: h.name, present: !!fetched.headers[h.key] }));

  return { isJsHeavy, isStaticSite, hasEcommerce, securityHeaders };
}

/* ── Pick a primary technology ─────────────────────────────── */
function pickPrimary(techs: DetectedTech[]): DetectionResult['primary'] {
  // Prefer CMS, then ecommerce, then framework
  const order: Category[] = ['cms', 'ecommerce', 'framework'];
  for (const cat of order) {
    const cands = techs.filter((t) => t.category === cat);
    if (cands.length === 0) continue;
    const top = cands[0];
    return {
      name: top.name,
      category: top.category,
      version: top.version,
      confidence: top.confidence,
    };
  }
  return null;
}

/* ── Group by category for the response ────────────────────── */
function groupByCategory(techs: DetectedTech[]): Record<string, DetectedTech[]> {
  const out: Record<string, DetectedTech[]> = {};
  for (const t of techs) {
    if (!out[t.category]) out[t.category] = [];
    out[t.category].push(t);
  }
  return out;
}

/* ════════════════════════════════════════════════════════════════
   Main API handler
   ════════════════════════════════════════════════════════════════ */

export const POST: APIRoute = async ({ request }) => {
  let body: any = null;
  try {
    body = await request.json();
  } catch {
    return jsonError('invalid_request', 'Request body must be valid JSON.', 400);
  }

  const rawUrl = typeof body?.url === 'string' ? body.url : '';
  if (!rawUrl) {
    return jsonError('missing_url', 'Please provide a URL to detect.', 400);
  }
  if (rawUrl.length > 2048) {
    return jsonError('url_too_long', 'URL is too long.', 400);
  }

  let normalized: string;
  let parsed: URL;
  try {
    normalized = normalizeUrl(rawUrl);
    parsed = new URL(normalized);
  } catch {
    return jsonError('invalid_url', 'Please enter a valid URL like https://example.com.', 400);
  }

  if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
    return jsonError('invalid_protocol', 'Only http and https URLs are supported.', 400);
  }

  if (isPrivateHost(parsed.hostname)) {
    return jsonError('blocked_host', 'Private and loopback addresses are not allowed.', 400);
  }

  // Cache lookup
  const cacheKey = parsed.protocol + '//' + parsed.hostname.toLowerCase() + parsed.pathname;
  const cached = cacheGet(cacheKey);
  if (cached) {
    return jsonOk({ ...cached, fromCache: true });
  }

  let fetched: FetchOutcome;
  try {
    fetched = await fetchSite(normalized);
  } catch (err: any) {
    const msg =
      err?.name === 'AbortError'
        ? 'The site took too long to respond. Try again or use a different URL.'
        : 'Could not fetch the URL. The site may be blocking external requests, behind login, or temporarily down.';
    return jsonError('fetch_failed', msg, 502, normalized);
  }

  if (fetched.status >= 400) {
    return jsonError(
      'http_error',
      `The site returned HTTP ${fetched.status}. We couldn't analyze it.`,
      502,
      normalized
    );
  }

  const finalUrlObj = (() => {
    try {
      return new URL(fetched.finalUrl);
    } catch {
      return parsed;
    }
  })();

  const techs = detect(fetched, finalUrlObj.hostname.toLowerCase());
  const insights = buildInsights(techs, fetched);
  const primary = pickPrimary(techs);

  const result: DetectionResult = {
    ok: true,
    url: normalized,
    finalUrl: fetched.finalUrl,
    fetchedAt: Math.floor(Date.now() / 1000),
    responseStatus: fetched.status,
    responseTimeMs: fetched.responseTimeMs,
    primary,
    technologies: techs,
    byCategory: groupByCategory(techs),
    totalDetected: techs.length,
    insights,
    redirected: fetched.finalUrl !== normalized && !fetched.finalUrl.startsWith(normalized),
    fromCache: false,
  };

  cacheSet(cacheKey, result);
  return jsonOk(result);
};

// Allow GET as a convenience (?url=...)
export const GET: APIRoute = async ({ url }) => {
  const target = url.searchParams.get('url');
  if (!target) {
    return jsonError('missing_url', 'Add ?url=example.com to your request.', 400);
  }
  const fakeReq = new Request(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: target }),
  });
  return POST({ request: fakeReq } as any);
};

/* ── Response helpers ──────────────────────────────────────── */
function jsonOk(data: any): Response {
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
function jsonError(code: string, message: string, status = 400, url?: string): Response {
  const body: DetectionError = { ok: false, error: code, message };
  if (url) body.url = url;
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
