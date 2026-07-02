// src/pages/api/serp-checker.ts
// API endpoint for the SERP Checker tool.
// POST /api/serp-checker/
// DataForSEO: /serp/google/organic/live/regular (depth 100) + keyword_overview.
// Tier 2 — free: top 10 organic + SERP features + keyword stats.
//          gated: top 100 organic + full feature breakdown + domain analysis.

export const prerender = false;

import type { APIRoute } from 'astro';
import { getSerpResults, getKeywordOverview } from '../../lib/dataforseo';
import { getCached, setCached, hashInput, checkRateLimit } from '../../lib/cache';

const RATE_LIMIT_DAILY = 5;
const RATE_LIMIT_TTL_SEC = 86400;
const CACHE_VERSION = 'v2';
const CACHE_TTL_SEC = 86400;

const LOCATION_MAP: Record<string, { code: number; label: string }> = {
  us: { code: 2840, label: 'United States' },
  uk: { code: 2826, label: 'United Kingdom' },
  ca: { code: 2124, label: 'Canada' },
  au: { code: 2036, label: 'Australia' },
  in: { code: 3560, label: 'India' },
};

function json(body: object, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function formatNumber(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
  if (n >= 1_000) return (n / 1_000).toFixed(1) + 'K';
  return String(n);
}

export const POST: APIRoute = async ({ request, clientAddress }) => {
  // 1. Parse + validate
  let body: any;
  try { body = await request.json(); }
  catch { return json({ success: false, error: 'invalid_json', message: 'Invalid request body' }, 400); }

  const keyword = (body?.keyword || '').trim();
  if (!keyword || keyword.length < 2) {
    return json({ success: false, error: 'invalid_input', field: 'keyword', message: 'Please enter a keyword (min 2 characters)' }, 400);
  }

  const locationKey = (body?.location || 'us').toLowerCase();
  const location = LOCATION_MAP[locationKey] || LOCATION_MAP.us;

  // 2. Cache check (before rate limit)
  const cacheKey = `serp:${CACHE_VERSION}:${hashInput({ keyword, location: location.code })}`;
  const cached = await getCached<any>(cacheKey);
  if (cached?.preview) {
    return json({
      ...cached,
      metadata: { ...cached.metadata, cached: true, ratelimitRemaining: RATE_LIMIT_DAILY },
    });
  }

  // 3. Rate limit
  const ip = clientAddress || 'unknown';
  const rl = await checkRateLimit(`serp_rl:${ip}`, RATE_LIMIT_DAILY, RATE_LIMIT_TTL_SEC);
  if (!rl.allowed) {
    return json({
      success: false,
      error: 'rate_limit',
      message: `You've used all ${RATE_LIMIT_DAILY} free checks today. Resets in ${Math.ceil((rl.resetAt.getTime() - Date.now()) / (3600 * 1000))} hours.`,
      ctaUrl: '/demo/?source=serp-checker-ratelimit',
    }, 429);
  }

  // 4. Fetch DataForSEO data in parallel
  const [serpRes, overviewRes] = await Promise.allSettled([
    getSerpResults(keyword, location.code),
    getKeywordOverview(keyword, location.code),
  ]);

  const serp = serpRes.status === 'fulfilled' ? serpRes.value : null;
  const overview = overviewRes.status === 'fulfilled' ? overviewRes.value : null;

  if (!serp) {
    return json({ success: false, error: 'data_unavailable', message: 'Could not fetch SERP data for this keyword. Please try a different keyword.' }, 404);
  }

  // 5. Build domain frequency analysis (top 100)
  const domainFreq: Record<string, { domain: string; count: number; positions: number[] }> = {};
  for (const r of serp.organic) {
    if (!domainFreq[r.domain]) {
      domainFreq[r.domain] = { domain: r.domain, count: 0, positions: [] };
    }
    domainFreq[r.domain].count++;
    domainFreq[r.domain].positions.push(r.position);
  }
  const domainAnalysis = Object.values(domainFreq)
    .sort((a, b) => b.count - a.count)
    .slice(0, 10)
    .map(d => ({
      domain: d.domain,
      count: d.count,
      bestPosition: Math.min(...d.positions),
      avgPosition: Math.round(d.positions.reduce((s, p) => s + p, 0) / d.positions.length),
    }));

  // 6. Count SERP features
  const f = serp.features;
  const featureCount = [
    f.featuredSnippet, f.peopleAlsoAsk, f.localPack,
    f.images, f.videos, f.knowledgeGraph,
    f.relatedSearches, f.topStories, f.shopping,
  ].filter(Boolean).length;

  // 7. Build response
  const response = {
    success: true,
    keyword: serp.keyword,
    location: { code: location.code, label: location.label, key: locationKey },
    keywordStats: overview ? {
      volume: overview.volume,
      volumeFormatted: formatNumber(overview.volume),
      kd: overview.kd,
      cpc: overview.cpc,
      cpcFormatted: overview.cpc > 0 ? '$' + overview.cpc.toFixed(2) : '$0.00',
      intent: overview.intent || 'unknown',
    } : {
      volume: null,
      volumeFormatted: null,
      kd: null,
      cpc: null,
      cpcFormatted: null,
      intent: null,
    },
    serpFeatures: {
      count: featureCount,
      featuredSnippet: f.featuredSnippet,
      peopleAlsoAsk: f.peopleAlsoAsk,
      localPack: f.localPack,
      images: f.images,
      videos: f.videos,
      knowledgeGraph: f.knowledgeGraph,
      relatedSearches: f.relatedSearches,
      topStories: f.topStories,
      shopping: f.shopping,
    },
    preview: {
      organicTop10: serp.organic.slice(0, 10).map(r => ({
        position: r.position,
        title: r.title,
        url: r.url,
        domain: r.domain,
        description: r.description,
        breadcrumb: r.breadcrumb,
      })),
    },
    full: {
      organicTop100: serp.organic.slice(0, 100).map(r => ({
        position: r.position,
        title: r.title,
        url: r.url,
        domain: r.domain,
        description: r.description,
        breadcrumb: r.breadcrumb,
      })),
      domainAnalysis,
      totalOrganicResults: serp.organic.length,
    },
    metadata: {
      ratelimitRemaining: rl.remaining,
      cached: false,
      hasDataForSeo: true,
      generatedAt: new Date().toISOString(),
    },
  };

  // 8. Cache
  await setCached(cacheKey, response, CACHE_TTL_SEC);

  return json(response, 200);
};
