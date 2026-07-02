// src/pages/api/website-traffic-checker.ts
// API endpoint for the Website Traffic Checker tool.
// POST /api/website-traffic-checker/
// DataForSEO: domain_rank_overview (traffic, positions, movement) + ranked_keywords (top KWs).
// Tier 1 — free preview (traffic, top 5 KWs, position dist); full report gated via /api/audit-lead.

export const prerender = false;

import type { APIRoute } from 'astro';
import {
  getDomainTrafficOverview,
  getRankedKeywords,
  getBulkKeywordDifficulty,
} from '../../lib/dataforseo';
import { getCached, setCached, hashInput, checkRateLimit } from '../../lib/cache';

const RATE_LIMIT_DAILY = 5;
const RATE_LIMIT_TTL_SEC = 86400;
const CACHE_VERSION = 'v2';
const CACHE_TTL_SEC = 86400;

function json(body: object, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function normalizeDomain(raw: string): string | null {
  let d = (raw || '').trim().toLowerCase();
  if (!d) return null;
  d = d.replace(/^https?:\/\//, '');
  d = d.replace(/^www\./, '');
  d = d.replace(/\/.*$/, '');
  if (!/^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)*$/.test(d)) return null;
  return d;
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

  const domain = normalizeDomain(body?.domain || body?.url || '');
  if (!domain) {
    return json({ success: false, error: 'invalid_input', field: 'domain', message: 'Please enter a valid domain (e.g., example.com)' }, 400);
  }

  // 2. Cache check (before rate limit — cached hits are free)
  const cacheKey = `traffic:${CACHE_VERSION}:${hashInput({ domain })}`;
  const cached = await getCached<any>(cacheKey);
  if (cached?.preview) {
    return json({
      ...cached,
      metadata: { ...cached.metadata, cached: true, ratelimitRemaining: RATE_LIMIT_DAILY },
    });
  }

  // 3. Rate limit
  const ip = clientAddress || 'unknown';
  const rl = await checkRateLimit(`traffic_rl:${ip}`, RATE_LIMIT_DAILY, RATE_LIMIT_TTL_SEC);
  if (!rl.allowed) {
    return json({
      success: false,
      error: 'rate_limit',
      message: `You've used all ${RATE_LIMIT_DAILY} free checks today. Resets in ${Math.ceil((rl.resetAt.getTime() - Date.now()) / (3600 * 1000))} hours.`,
      ctaUrl: '/demo/?source=traffic-checker-ratelimit',
    }, 429);
  }

  // 4. Fetch DataForSEO data in parallel
  const [trafficRes, rankedRes] = await Promise.allSettled([
    getDomainTrafficOverview(domain, 2840),
    getRankedKeywords(domain, 2840, 25),
  ]);

  const traffic = trafficRes.status === 'fulfilled' ? trafficRes.value : null;
  const ranked = rankedRes.status === 'fulfilled' ? rankedRes.value : null;

  if (!traffic && !ranked) {
    return json({ success: false, error: 'data_unavailable', message: 'Could not fetch traffic data for this domain. The site may be too new or have no measurable search presence.' }, 404);
  }

  // 5. Enrich top keywords with KD
  let keywordsWithKd: Array<{
    keyword: string; position: number; volume: number; cpc: number;
    url: string; kd: number | null;
  }> = [];

  if (ranked?.topKeywords?.length) {
    const topKwList = ranked.topKeywords;
    const kdMap = new Map<string, number | null>();
    try {
      const kdResults = await getBulkKeywordDifficulty(topKwList.map(k => k.keyword), 2840);
      for (const r of kdResults) kdMap.set(r.keyword, r.kd);
    } catch { /* best effort */ }

    keywordsWithKd = topKwList.map(k => ({
      ...k,
      kd: kdMap.get(k.keyword) ?? null,
    }));
  }

  // 6. Build preview + full response
  const org = traffic?.organic;
  const paid = traffic?.paid;
  const totalPositions = org
    ? org.pos1 + org.pos2to3 + org.pos4to10 + org.pos11to20 + org.pos21to50 + org.pos51to100
    : 0;

  const response = {
    success: true,
    domain,
    preview: {
      organicTraffic: org?.traffic ?? 0,
      organicTrafficFormatted: formatNumber(org?.traffic ?? 0),
      totalKeywords: org?.keywords ?? ranked?.total ?? 0,
      totalKeywordsFormatted: formatNumber(org?.keywords ?? ranked?.total ?? 0),
      paidTraffic: paid?.traffic ?? 0,
      paidKeywords: paid?.keywords ?? 0,
      hasPaidData: !!paid && paid.keywords > 0,
      trafficValue: org?.trafficValue ?? 0,
      trafficValueFormatted: '$' + formatNumber(org?.trafficValue ?? 0),
      positionDistribution: {
        top3: org ? org.pos1 + org.pos2to3 : ranked?.pos1to3 ?? 0,
        top10: org?.pos4to10 ?? ranked?.pos4to10 ?? 0,
        top20: org?.pos11to20 ?? ranked?.pos11to20 ?? 0,
        top50: org?.pos21to50 ?? ranked?.pos21to50 ?? 0,
        top100: org?.pos51to100 ?? ranked?.pos51to100 ?? 0,
        total: totalPositions,
      },
      keywordMovement: org ? {
        new: org.newKeywords,
        up: org.upKeywords,
        down: org.downKeywords,
        lost: org.lostKeywords,
      } : null,
      topKeywords: keywordsWithKd.slice(0, 5).map(k => ({
        keyword: k.keyword,
        position: k.position,
        volume: k.volume,
        volumeFormatted: formatNumber(k.volume),
        url: k.url,
      })),
    },
    full: {
      allKeywords: keywordsWithKd.slice(0, 20).map(k => ({
        keyword: k.keyword,
        position: k.position,
        volume: k.volume,
        volumeFormatted: formatNumber(k.volume),
        cpc: k.cpc,
        kd: k.kd,
        url: k.url,
      })),
      difficultyDistribution: (() => {
        const dist = { easy: 0, medium: 0, hard: 0, unknown: 0 };
        for (const k of keywordsWithKd.slice(0, 20)) {
          if (k.kd == null) dist.unknown++;
          else if (k.kd <= 30) dist.easy++;
          else if (k.kd <= 60) dist.medium++;
          else dist.hard++;
        }
        return dist;
      })(),
      topPages: (() => {
        const urlMap = new Map<string, { url: string; keywordCount: number; totalVolume: number }>();
        for (const k of keywordsWithKd) {
          if (!k.url) continue;
          const existing = urlMap.get(k.url);
          if (existing) {
            existing.keywordCount++;
            existing.totalVolume += k.volume;
          } else {
            urlMap.set(k.url, { url: k.url, keywordCount: 1, totalVolume: k.volume });
          }
        }
        return Array.from(urlMap.values())
          .sort((a, b) => b.totalVolume - a.totalVolume)
          .slice(0, 10);
      })(),
    },
    metadata: {
      ratelimitRemaining: rl.remaining,
      cached: false,
      hasDataForSeo: !!traffic,
      generatedAt: new Date().toISOString(),
    },
  };

  // 7. Cache
  await setCached(cacheKey, response, CACHE_TTL_SEC);

  return json(response, 200);
};
