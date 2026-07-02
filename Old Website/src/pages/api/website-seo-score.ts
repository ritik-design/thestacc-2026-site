// src/pages/api/website-seo-score.ts
// API endpoint for the Website SEO Score tool.
// POST /api/website-seo-score/
// Combines: server-side HTML fetch + 8-dimension scorer + Google PageSpeed + DataForSEO (DR, ranked keywords) + Kimi narrative.
// Tier 1 — free preview always; full report (AI plan + comprehensive fix list) gated via /api/audit-lead.

export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimiJson } from '../../lib/kimi';
import { getCached, setCached, hashInput, checkRateLimit } from '../../lib/cache';
import {
  getBacklinksSummary,
  getRankedKeywords,
} from '../../lib/dataforseo';
import { parseHTML } from '../../lib/tools/on-page-seo-checker';
import {
  scoreSite,
  parsePageSpeedResponse,
  checkAiCrawlerBlocks,
  type SiteSignals,
  type ScoredSiteReport,
  type PageSpeedScores,
} from '../../lib/tools/website-seo-score';
import {
  WEBSITE_SEO_SYSTEM_PROMPT,
  buildSiteSummaryUserPrompt,
  type SiteSummaryContext,
} from '../../lib/tools/website-seo-prompts';

const RATE_LIMIT_DAILY = 5;
const RATE_LIMIT_TTL_SEC = 86400;
const CACHE_VERSION = 'v1';
const CACHE_TTL_SEC = 86400;
const FETCH_TIMEOUT_MS = 15000;
const ROBOTS_TIMEOUT_MS = 8000;
const PAGESPEED_TIMEOUT_MS = 35000;

interface AiNarrative {
  executiveSummary: string;
  biggestOpportunity: { headline: string; explanation: string; expectedImpact: string };
  actionPlan: Array<{ week: number; task: string; estimatedHours: number; expectedScoreLift: number }>;
  competitivePositioning: string;
}

function json(body: object, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function normalizeUrl(raw: string): string | null {
  let u = (raw || '').trim();
  if (!u) return null;
  if (!/^https?:\/\//i.test(u)) u = 'https://' + u;
  try { return new URL(u).href; } catch { return null; }
}

async function fetchWithTimeout(url: string, timeoutMs: number, opts?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...opts, signal: controller.signal });
  } finally { clearTimeout(timer); }
}

async function fetchHTML(url: string, timeoutMs = FETCH_TIMEOUT_MS): Promise<{ html: string; finalUrl: string; status: number }> {
  const res = await fetchWithTimeout(url, timeoutMs, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    },
  });
  const html = await res.text();
  return { html, finalUrl: res.url || url, status: res.status };
}

async function fetchTextFile(url: string, timeoutMs = ROBOTS_TIMEOUT_MS): Promise<string | null> {
  try {
    const res = await fetchWithTimeout(url, timeoutMs);
    if (!res.ok) return null;
    return await res.text();
  } catch { return null; }
}

async function fetchPageSpeed(url: string): Promise<PageSpeedScores | null> {
  try {
    const key = process.env.PAGESPEED_API_KEY || '';
    const keyParam = key ? `&key=${key}` : '';
    const apiUrl = `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${encodeURIComponent(url)}&category=PERFORMANCE&strategy=MOBILE${keyParam}`;
    const res = await fetchWithTimeout(apiUrl, PAGESPEED_TIMEOUT_MS);
    if (!res.ok) return null;
    const data = await res.json();
    return parsePageSpeedResponse(data);
  } catch { return null; }
}

function validateInput(body: any): { ok: true; url: string; bizName?: string; city?: string } | { ok: false; error: { field: string; message: string } } {
  if (!body || typeof body !== 'object') return { ok: false, error: { field: '_', message: 'Invalid request body' } };
  const url = normalizeUrl(String(body.url || ''));
  const bizName = body.bizName ? String(body.bizName).trim().slice(0, 100) : undefined;
  const city = body.city ? String(body.city).trim().slice(0, 80) : undefined;
  if (!url) return { ok: false, error: { field: 'url', message: 'Please enter a valid URL' } };
  return { ok: true, url, bizName, city };
}

async function generateNarrative(ctx: SiteSummaryContext): Promise<AiNarrative | null> {
  const result = await callKimiJson<AiNarrative>({
    systemPrompt: WEBSITE_SEO_SYSTEM_PROMPT,
    userPrompt: buildSiteSummaryUserPrompt(ctx),
    maxTokens: 1500,
    temperature: 0.4,
    timeoutMs: 45000,
  });
  if (!result) return null;
  // Light validation
  if (!result.executiveSummary) return null;
  if (!Array.isArray(result.actionPlan)) result.actionPlan = [];
  return result;
}

export const POST: APIRoute = async ({ request, clientAddress }) => {
  // 1. Validate
  let body: any;
  try { body = await request.json(); }
  catch { return json({ success: false, error: 'invalid_json', message: 'Request body must be JSON' }, 400); }

  const validation = validateInput(body);
  if (!validation.ok) {
    return json({ success: false, error: 'invalid_input', field: validation.error.field, message: validation.error.message }, 400);
  }
  const { url, bizName, city } = validation;

  // 2. Rate limit
  const ip = clientAddress || 'unknown';
  const rl = await checkRateLimit(`wss_rl:${ip}`, RATE_LIMIT_DAILY, RATE_LIMIT_TTL_SEC);
  if (!rl.allowed) {
    return json({
      success: false,
      error: 'rate_limit',
      message: `You've used all ${RATE_LIMIT_DAILY} free analyses today. Resets in ${Math.ceil((rl.resetAt.getTime() - Date.now()) / (3600 * 1000))} hours.`,
      ctaUrl: '/demo/?source=site-score-ratelimit',
    }, 429);
  }

  // 3. Cache check
  const cacheKey = `wss:${CACHE_VERSION}:${hashInput({ url, bizName, city })}`;
  const cached = await getCached<any>(cacheKey);
  if (cached?.report) {
    return json({
      ...cached,
      metadata: { ...cached.metadata, cached: true, ratelimitRemaining: rl.remaining },
    });
  }

  // 4. Parse domain from URL
  let domain = '';
  let origin = '';
  let hasHttps = false;
  try {
    const u = new URL(url);
    domain = u.hostname.replace(/^www\./, '');
    origin = u.origin;
    hasHttps = u.protocol === 'https:';
  } catch {}

  // 5. Fire all parallel fetches
  const [
    htmlRes,
    psRes,
    robotsRes,
    llmsRes,
    sitemapRes,
    sitemapAltRes,
    backlinksRes,
    rankedKwRes,
  ] = await Promise.allSettled([
    fetchHTML(url),
    fetchPageSpeed(url),
    fetchTextFile(`${origin}/robots.txt`),
    fetchTextFile(`${origin}/llms.txt`),
    fetchTextFile(`${origin}/sitemap.xml`),
    fetchTextFile(`${origin}/sitemap_index.xml`),
    getBacklinksSummary(domain),
    getRankedKeywords(domain, 2840, 15),
  ]);

  // 6. Process page fetch
  if (htmlRes.status !== 'fulfilled') {
    return json({
      success: false,
      error: 'page_fetch_failed',
      message: 'Could not reach the website. Check the URL and try again — or the site may be blocking automated requests.',
    }, 400);
  }
  const { html, status: pageStatus } = htmlRes.value;
  if (pageStatus >= 400 || !html || html.length < 100) {
    return json({
      success: false,
      error: 'page_fetch_failed',
      message: pageStatus >= 400 ? `Site returned HTTP ${pageStatus}. Make sure the URL is publicly accessible.` : 'Site returned no usable HTML. May be entirely client-rendered.',
    }, 400);
  }
  const parsedPage = parseHTML(html, url);

  // 7. Process other fetches
  const pageSpeed = psRes.status === 'fulfilled' ? psRes.value : null;
  const robotsContent = robotsRes.status === 'fulfilled' ? robotsRes.value : null;
  const hasLlmsTxt = llmsRes.status === 'fulfilled' && !!llmsRes.value && llmsRes.value.length > 10;
  const sitemapContent = (sitemapRes.status === 'fulfilled' && sitemapRes.value) ? sitemapRes.value : (sitemapAltRes.status === 'fulfilled' ? sitemapAltRes.value : null);
  const hasSitemap = !!sitemapContent && (sitemapContent.includes('<urlset') || sitemapContent.includes('<sitemapindex'));
  const blocksAiCrawlers = robotsContent ? checkAiCrawlerBlocks(robotsContent) : false;
  const backlinks = backlinksRes.status === 'fulfilled' ? backlinksRes.value : null;
  const rankedKw = rankedKwRes.status === 'fulfilled' ? rankedKwRes.value : null;

  // 8. Build signals
  const signals: SiteSignals = {
    page: parsedPage,
    pageSpeed,
    hasHttps,
    hasRobotsTxt: !!robotsContent && robotsContent.length > 0,
    hasLlmsTxt,
    hasSitemap,
    blocksAiCrawlers,
    drNormalized: backlinks?.drNormalized ?? null,
    refDomains: backlinks?.refDomains ?? null,
    backlinks: backlinks?.backlinks ?? null,
    estTraffic: rankedKw?.estTraffic ?? null,
    totalRankingKeywords: rankedKw?.total ?? null,
    pos1to3: rankedKw?.pos1to3 ?? null,
    pos4to10: rankedKw?.pos4to10 ?? null,
    bizName,
    city,
  };

  // 9. Score
  const report: ScoredSiteReport = scoreSite(signals);

  // 10. Kimi narrative
  let narrative: AiNarrative | null = null;
  {
    try {
      const hasFaqSchema = parsedPage.schemaTypes.some(t => /FAQPage|QAPage/i.test(t));
      const hasLocalBizSchema = parsedPage.schemaTypes.some(t => /LocalBusiness|Dentist|Restaurant|Plumber|Electrician|MedicalBusiness|LegalService|Attorney/i.test(t));
      const failedChecks = report.dimensions
        .flatMap(d => d.checks.filter(c => !c.passed && c.fix).map(c => ({ label: c.label, fix: c.fix as string })))
        .slice(0, 8);

      narrative = await generateNarrative({
        url,
        domain,
        bizName,
        city,
        overallScore: report.overall.pct,
        grade: report.overall.grade,
        drNormalized: signals.drNormalized,
        refDomains: signals.refDomains,
        estTraffic: signals.estTraffic,
        totalRankingKeywords: signals.totalRankingKeywords,
        pos1to3: signals.pos1to3,
        performanceScore: pageSpeed?.performance ?? null,
        title: parsedPage.title,
        metaDescription: parsedPage.metaDescription,
        h1: parsedPage.h1s[0] || '',
        wordCount: parsedPage.wordCount,
        hasFaqSchema,
        hasLocalBizSchema,
        hasLlmsTxt,
        topRankingKeywords: rankedKw?.topKeywords?.slice(0, 5).map(k => ({ keyword: k.keyword, position: k.position, volume: k.volume })) || [],
        dimensionScores: report.dimensions.map(d => ({ label: d.label, score: d.score, max: d.maxScore, status: d.status })),
        topFailedChecks: failedChecks,
      });
    } catch (err) {
      console.error('[wss] AI narrative failed:', err instanceof Error ? err.message : err);
    }
  }

  // 11. Build response
  const response = {
    success: true,
    url,
    domain,
    report,
    page: {
      title: parsedPage.title,
      titleLength: parsedPage.title.length,
      metaDescription: parsedPage.metaDescription,
      metaDescLength: parsedPage.metaDescription.length,
      h1: parsedPage.h1s[0] || '',
      h1Count: parsedPage.h1s.length,
      h2Count: parsedPage.h2s.length,
      h3Count: parsedPage.h3s.length,
      imageCount: parsedPage.images.length,
      imagesWithAlt: parsedPage.images.filter(i => i.alt && i.alt.trim()).length,
      internalLinkCount: parsedPage.internalLinkCount,
      externalLinkCount: parsedPage.externalLinkCount,
      wordCount: parsedPage.wordCount,
      schemaTypes: parsedPage.schemaTypes,
      canonical: parsedPage.canonical,
      hasViewport: parsedPage.hasViewport,
    },
    pageSpeed,
    backlinks,
    rankedKeywords: rankedKw ? {
      total: rankedKw.total,
      pos1to3: rankedKw.pos1to3,
      pos4to10: rankedKw.pos4to10,
      pos11to20: rankedKw.pos11to20,
      estTraffic: rankedKw.estTraffic,
      topKeywords: rankedKw.topKeywords.slice(0, 10),
    } : null,
    technical: {
      hasHttps,
      hasRobotsTxt: !!robotsContent && robotsContent.length > 0,
      hasLlmsTxt,
      hasSitemap,
      blocksAiCrawlers,
    },
    aiNarrative: narrative,
    metadata: {
      ratelimitRemaining: rl.remaining,
      cached: false,
      hasDataForSeo: !!backlinks,
      hasPageSpeed: !!pageSpeed,
      hasAi: !!narrative,
      generatedAt: new Date().toISOString(),
    },
  };

  // 12. Cache
  await setCached(cacheKey, response, CACHE_TTL_SEC);

  return json(response, 200);
};
