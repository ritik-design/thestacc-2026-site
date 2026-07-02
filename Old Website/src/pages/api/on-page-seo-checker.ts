// src/pages/api/on-page-seo-checker.ts
// API endpoint for the On-Page SEO Checker.
// POST /api/on-page-seo-checker/
// Combines: server-side HTML fetch + 15-rule scorer + DataForSEO SERP/KD + Kimi content analysis.
// Tier 1 — free preview always; full report (AI rewrites + competitor analysis) gated via /api/audit-lead.

export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimiJson } from '../../lib/kimi';
import { getCached, setCached, hashInput, checkRateLimit } from '../../lib/cache';
import {
  getSerpOrganic,
  getKeywordOverview,
  getRelatedKeywords,
  getPeopleAlsoAsk,
  type SerpItem,
  type KeywordOverview,
} from '../../lib/dataforseo';
import {
  parseHTML,
  scoreOnPage,
  type ScoredReport,
  type ParsedPage,
} from '../../lib/tools/on-page-seo-checker';
import {
  ON_PAGE_SEO_SYSTEM_PROMPT,
  buildOnPageUserPrompt,
  type OnPageContext,
} from '../../lib/tools/on-page-seo-prompts';

const RATE_LIMIT_DAILY = 5;            // Tier 1 — heavy data, low daily cap
const RATE_LIMIT_TTL_SEC = 86400;
const CACHE_VERSION = 'v1';
const CACHE_TTL_SEC = 86400;
const FETCH_TIMEOUT_MS = 15000;
const COMPETITOR_FETCH_TIMEOUT_MS = 8000;
const COMPETITORS_TO_FETCH = 3;

interface AiInsights {
  topicalDepthScore: number;
  contentQualityScore: number;
  competitorComparison: string;
  missingSubtopics: Array<{ topic: string; why: string }>;
  missingPaaCoverage: Array<{ question: string; suggestion: string }>;
  rewrites: {
    titleTag: { current: string; suggested: string; reasoning: string };
    metaDescription: { current: string; suggested: string; reasoning: string };
    openingParagraph: { current: string; suggested: string; reasoning: string };
  };
  topPriorityFixes: Array<{ priority: number; fix: string; impact: string; effort: string }>;
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

function validateInput(body: any): { ok: true; url: string; keyword: string } | { ok: false; error: { field: string; message: string } } {
  if (!body || typeof body !== 'object') return { ok: false, error: { field: '_', message: 'Invalid request body' } };
  const url = normalizeUrl(String(body.url || ''));
  const keyword = String(body.keyword || '').trim();
  if (!url) return { ok: false, error: { field: 'url', message: 'Please enter a valid URL' } };
  if (!keyword) return { ok: false, error: { field: 'keyword', message: 'Please enter your target keyword' } };
  if (keyword.length > 100) return { ok: false, error: { field: 'keyword', message: 'Keyword too long (max 100 chars)' } };
  if (keyword.length < 2) return { ok: false, error: { field: 'keyword', message: 'Keyword too short (min 2 chars)' } };
  return { ok: true, url, keyword };
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
      'Accept-Language': 'en-US,en;q=0.9',
    },
  });
  const html = await res.text();
  return { html, finalUrl: res.url || url, status: res.status };
}

/** Fetch + parse competitor pages in parallel to compute avg word count. */
async function fetchCompetitorWordCounts(serpItems: SerpItem[], skipDomain: string): Promise<{ avgWordCount: number; perCompetitor: Array<{ url: string; wordCount: number; title: string }> }> {
  const targets = serpItems
    .filter(s => s.domain && !s.domain.toLowerCase().includes(skipDomain.toLowerCase()))
    .slice(0, COMPETITORS_TO_FETCH);

  const results = await Promise.allSettled(
    targets.map(async (item) => {
      const { html } = await fetchHTML(item.url, COMPETITOR_FETCH_TIMEOUT_MS);
      const parsed = parseHTML(html, item.url);
      return { url: item.url, wordCount: parsed.wordCount, title: item.title };
    })
  );

  const successful = results
    .filter((r): r is PromiseFulfilledResult<{ url: string; wordCount: number; title: string }> => r.status === 'fulfilled')
    .map(r => r.value)
    .filter(r => r.wordCount > 100); // ignore failed-fetch results

  const avg = successful.length
    ? Math.round(successful.reduce((a, c) => a + c.wordCount, 0) / successful.length)
    : 0;

  return { avgWordCount: avg, perCompetitor: successful };
}

async function generateAiInsights(ctx: OnPageContext): Promise<AiInsights | null> {
  const result = await callKimiJson<AiInsights>({
    systemPrompt: ON_PAGE_SEO_SYSTEM_PROMPT,
    userPrompt: buildOnPageUserPrompt(ctx),
    maxTokens: 2500,
    temperature: 0.4,
    timeoutMs: 45000,
  });
  if (!result) return null;
  // Light validation
  if (typeof result.topicalDepthScore !== 'number') result.topicalDepthScore = 50;
  if (typeof result.contentQualityScore !== 'number') result.contentQualityScore = 50;
  if (!Array.isArray(result.missingSubtopics)) result.missingSubtopics = [];
  if (!Array.isArray(result.missingPaaCoverage)) result.missingPaaCoverage = [];
  if (!Array.isArray(result.topPriorityFixes)) result.topPriorityFixes = [];
  if (!result.rewrites) {
    result.rewrites = {
      titleTag: { current: ctx.title, suggested: ctx.title, reasoning: '' },
      metaDescription: { current: ctx.metaDescription, suggested: ctx.metaDescription, reasoning: '' },
      openingParagraph: { current: ctx.bodyExcerpt.slice(0, 200), suggested: '', reasoning: '' },
    };
  }
  return result;
}

export const POST: APIRoute = async ({ request, clientAddress }) => {
  // 1. Parse + validate
  let body: any;
  try {
    body = await request.json();
  } catch {
    return json({ success: false, error: 'invalid_json', message: 'Request body must be JSON' }, 400);
  }

  const validation = validateInput(body);
  if (!validation.ok) {
    return json({ success: false, error: 'invalid_input', field: validation.error.field, message: validation.error.message }, 400);
  }

  const { url, keyword } = validation;

  // 2. Rate limit
  const ip = clientAddress || 'unknown';
  const rl = await checkRateLimit(`onpage_rl:${ip}`, RATE_LIMIT_DAILY, RATE_LIMIT_TTL_SEC);
  if (!rl.allowed) {
    return json({
      success: false,
      error: 'rate_limit',
      message: `You've used all ${RATE_LIMIT_DAILY} free analyses today. Resets in ${Math.ceil((rl.resetAt.getTime() - Date.now()) / (3600 * 1000))} hours.`,
      ratelimitResetAt: rl.resetAt.toISOString(),
      ctaUrl: '/demo/?source=onpage-tool-ratelimit',
    }, 429);
  }

  // 3. Cache check
  const cacheKey = `onpage:${CACHE_VERSION}:${hashInput({ url, keyword })}`;
  const cached = await getCached<any>(cacheKey);
  if (cached?.report) {
    return json({
      ...cached,
      metadata: {
        ...cached.metadata,
        cached: true,
        ratelimitRemaining: rl.remaining,
      },
    });
  }

  // 4. Fetch the user's URL
  let parsed: ParsedPage;
  let finalUrl = url;
  try {
    const fetched = await fetchHTML(url);
    if (fetched.status >= 400) {
      return json({
        success: false,
        error: 'page_fetch_failed',
        message: `Could not fetch the page (HTTP ${fetched.status}). Make sure the URL is publicly accessible.`,
      }, 400);
    }
    if (!fetched.html || fetched.html.length < 100) {
      return json({
        success: false,
        error: 'page_fetch_failed',
        message: 'The page returned no HTML. The site may be blocking bots or rendering entirely client-side.',
      }, 400);
    }
    finalUrl = fetched.finalUrl;
    parsed = parseHTML(fetched.html, finalUrl);
  } catch (err) {
    return json({
      success: false,
      error: 'page_fetch_failed',
      message: 'Could not reach the page. Check the URL and try again — or the site may be blocking automated requests.',
    }, 400);
  }

  // 5. Run SERP + keyword data calls in parallel
  let serpTop10: SerpItem[] = [];
  let kwOverview: KeywordOverview | null = null;
  let relatedKws: Array<{ keyword: string; volume: number }> = [];
  let paa: Array<{ question: string; answer: string }> = [];

  {
    const [serpRes, kwRes, relRes, paaRes] = await Promise.allSettled([
      getSerpOrganic(keyword),
      getKeywordOverview(keyword),
      getRelatedKeywords(keyword, 2840, 15),
      getPeopleAlsoAsk(keyword),
    ]);
    if (serpRes.status === 'fulfilled') serpTop10 = serpRes.value;
    if (kwRes.status === 'fulfilled') kwOverview = kwRes.value;
    if (relRes.status === 'fulfilled') relatedKws = relRes.value;
    if (paaRes.status === 'fulfilled') paa = paaRes.value;
  }

  // 6. Fetch top 3 competitor pages for word count benchmarking (parallel)
  let userDomain = '';
  try { userDomain = new URL(finalUrl).hostname; } catch {}

  const compResults = serpTop10.length
    ? await fetchCompetitorWordCounts(serpTop10, userDomain)
    : { avgWordCount: 0, perCompetitor: [] };

  // 7. Score the page
  const report = scoreOnPage(parsed, keyword, finalUrl, compResults.avgWordCount);

  // 8. Kimi content analysis (in parallel-ready position; runs after scoring so we have wordCount)
  let aiInsights: AiInsights | null = null;
  if (parsed.wordCount >= 50) {
    try {
      aiInsights = await generateAiInsights({
        url: finalUrl,
        keyword,
        title: parsed.title,
        metaDescription: parsed.metaDescription,
        h1: parsed.h1s[0] || '',
        h2s: parsed.h2s,
        h3s: parsed.h3s,
        bodyExcerpt: parsed.bodyText,
        wordCount: parsed.wordCount,
        competitorAvgWordCount: compResults.avgWordCount,
        competitorTitles: serpTop10.slice(0, 5).map(s => s.title).filter(Boolean),
        paaQuestions: paa.slice(0, 6).map(p => p.question),
        relatedKeywords: relatedKws.slice(0, 10).map(r => r.keyword),
      });
    } catch (err) {
      console.error('[onpage] AI insights failed:', err instanceof Error ? err.message : err);
    }
  }

  // 9. Build response
  const response = {
    success: true,
    url: finalUrl,
    keyword,
    report,
    page: {
      title: parsed.title,
      metaDescription: parsed.metaDescription,
      h1: parsed.h1s[0] || '',
      h1Count: parsed.h1s.length,
      h2Count: parsed.h2s.length,
      h3Count: parsed.h3s.length,
      imageCount: parsed.images.length,
      imagesWithAlt: parsed.images.filter(i => i.alt && i.alt.trim()).length,
      internalLinkCount: parsed.internalLinkCount,
      externalLinkCount: parsed.externalLinkCount,
      wordCount: parsed.wordCount,
      schemaTypes: parsed.schemaTypes,
      canonical: parsed.canonical,
      hasViewport: parsed.hasViewport,
    },
    keywordData: kwOverview ? {
      keyword: kwOverview.keyword,
      volume: kwOverview.volume,
      kd: kwOverview.kd,
      cpc: kwOverview.cpc,
      intent: kwOverview.intent,
    } : null,
    serp: {
      top10: serpTop10.map(s => ({ rank: s.rank, domain: s.domain, title: s.title, url: s.url })),
      avgWordCount: compResults.avgWordCount,
      competitors: compResults.perCompetitor,
    },
    paa: paa.slice(0, 8),
    relatedKeywords: relatedKws.slice(0, 10),
    aiInsights,
    metadata: {
      ratelimitRemaining: rl.remaining,
      cached: false,
      hasDataForSeo: serpTop10.length > 0,
      hasAi: !!aiInsights,
      generatedAt: new Date().toISOString(),
    },
  };

  // 10. Cache (24h)
  await setCached(cacheKey, response, CACHE_TTL_SEC);

  return json(response, 200);
};
