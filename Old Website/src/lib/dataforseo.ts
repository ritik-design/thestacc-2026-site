// src/lib/dataforseo.ts
// Reusable DataForSEO client for all theStacc tools.
// Auth: HTTP Basic via DATAFORSEO_AUTH_BASE64.
// All functions return null/empty on failure (graceful degradation).

const AUTH = process.env.DATAFORSEO_AUTH_BASE64;

const BASE = 'https://api.dataforseo.com/v3';

async function fetchWithTimeout(url: string, timeoutMs: number, opts?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...opts, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

async function call<T>(path: string, body: object[], timeoutMs = 30000): Promise<T | null> {
  if (!AUTH) {
    console.warn('[dataforseo] No DATAFORSEO_AUTH_BASE64 configured');
    return null;
  }
  try {
    const res = await fetchWithTimeout(`${BASE}${path}`, timeoutMs, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${AUTH}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      console.error('[dataforseo]', res.status, await res.text().then(t => t.substring(0, 300)));
      return null;
    }
    const data = await res.json();
    if (data.status_code !== 20000) {
      console.error('[dataforseo] non-20000 status:', data.status_code, data.status_message);
      return null;
    }
    return data as T;
  } catch (err) {
    console.error('[dataforseo] error:', err instanceof Error ? err.message : err);
    return null;
  }
}

export interface SerpItem { domain: string; title: string; url: string; rank: number; description?: string; }
export interface PaaItem { question: string; answer: string; }
export interface KeywordOverview { keyword: string; volume: number; kd: number | null; cpc: number; intent: string; }
export interface RelatedKeyword { keyword: string; volume: number; kd: number | null; }

/** Get top organic results for a keyword. */
export async function getSerpOrganic(keyword: string, locationCode = 2840): Promise<SerpItem[]> {
  const data = await call<any>('/serp/google/organic/live/regular', [{
    keyword, language_code: 'en', location_code: locationCode, depth: 10,
  }]);
  if (!data) return [];
  const items = data.tasks?.[0]?.result?.[0]?.items || [];
  return items
    .filter((it: any) => it.type === 'organic')
    .map((it: any) => ({
      domain: it.domain || '',
      title: it.title || '',
      url: it.url || '',
      rank: it.rank_absolute || 0,
      description: it.description,
    }));
}

/** Get People Also Ask questions for a keyword. */
export async function getPeopleAlsoAsk(keyword: string, locationCode = 2840): Promise<PaaItem[]> {
  const data = await call<any>('/serp/google/organic/live/advanced', [{
    keyword, language_code: 'en', location_code: locationCode, depth: 10,
    people_also_ask_click_depth: 1,
  }]);
  if (!data) return [];
  const items = data.tasks?.[0]?.result?.[0]?.items || [];
  const paa: PaaItem[] = [];
  for (const item of items) {
    if (item.type === 'people_also_ask') {
      for (const q of (item.items || [])) {
        const ans = q.expanded_element?.[0]?.description || '';
        paa.push({ question: q.title || '', answer: ans });
      }
    }
  }
  return paa;
}

/** Get search volume + KD + CPC + intent for a keyword. */
export async function getKeywordOverview(keyword: string, locationCode = 2840): Promise<KeywordOverview | null> {
  const data = await call<any>('/dataforseo_labs/google/keyword_overview/live', [{
    keywords: [keyword], language_code: 'en', location_code: locationCode,
  }]);
  if (!data) return null;
  const result = data.tasks?.[0]?.result?.[0];
  const item = result?.items?.[0];
  if (!item) return null;
  return {
    keyword: item.keyword || keyword,
    volume: item.keyword_info?.search_volume ?? 0,
    kd: item.keyword_properties?.keyword_difficulty ?? null,
    cpc: item.keyword_info?.cpc ?? 0,
    intent: item.search_intent_info?.main_intent ?? 'unknown',
  };
}

/** Get related keywords for a seed. */
export async function getRelatedKeywords(seed: string, locationCode = 2840, limit = 30): Promise<RelatedKeyword[]> {
  const data = await call<any>('/dataforseo_labs/google/related_keywords/live', [{
    keyword: seed, language_code: 'en', location_code: locationCode, depth: 1, limit,
  }]);
  if (!data) return [];
  const items = data.tasks?.[0]?.result?.[0]?.items || [];
  return items.map((it: any) => ({
    keyword: it.keyword_data?.keyword || '',
    volume: it.keyword_data?.keyword_info?.search_volume ?? 0,
    kd: it.keyword_data?.keyword_properties?.keyword_difficulty ?? null,
  }));
}

/** Get domain rank overview (DR-equivalent + backlinks count). */
export async function getDomainRankOverview(domain: string, locationCode = 2840): Promise<{ rank: number; orgTraffic: number; backlinks: number; refDomains: number; } | null> {
  const data = await call<any>('/dataforseo_labs/google/domain_rank_overview/live', [{
    target: domain, language_code: 'en', location_code: locationCode,
  }]);
  if (!data) return null;
  const result = data.tasks?.[0]?.result?.[0];
  const item = result?.items?.[0];
  if (!item) return null;
  return {
    rank: item.metrics?.organic?.pos_1 ?? 0,
    orgTraffic: item.metrics?.organic?.etv ?? 0,
    backlinks: item.metrics?.organic?.count ?? 0,
    refDomains: 0,
  };
}

/** Get bulk keyword difficulty for many keywords (cheap — $0.01/100). */
export async function getBulkKeywordDifficulty(keywords: string[], locationCode = 2840): Promise<Array<{ keyword: string; kd: number | null; }>> {
  const data = await call<any>('/dataforseo_labs/google/bulk_keyword_difficulty/live', [{
    keywords, language_code: 'en', location_code: locationCode,
  }]);
  if (!data) return keywords.map(k => ({ keyword: k, kd: null }));
  const items = data.tasks?.[0]?.result?.[0]?.items || [];
  return items.map((it: any) => ({ keyword: it.keyword || '', kd: it.keyword_difficulty ?? null }));
}

export interface BacklinksSummary {
  rank: number;          // Domain rank (DR equivalent, 0-1000)
  drNormalized: number;  // 0-100 scale (rank / 10)
  backlinks: number;
  refDomains: number;
  refMainDomains: number;
  refIps: number;
  brokenBacklinks: number;
  spamScore: number | null;
  firstSeen: string | null;
}

/** Get full backlinks profile (DR, ref domains, total backlinks, broken). */
export async function getBacklinksSummary(target: string): Promise<BacklinksSummary | null> {
  // target = domain (e.g., "example.com")
  const data = await call<any>('/backlinks/summary/live', [{
    target,
    internal_list_limit: 10,
    backlinks_status_type: 'live',
    include_subdomains: true,
  }]);
  if (!data) return null;
  const item = data.tasks?.[0]?.result?.[0];
  if (!item) return null;
  const rank = item.rank ?? 0;  // DataForSEO returns 0-1000
  return {
    rank,
    drNormalized: Math.round(rank / 10),  // 0-100 scale matches Ahrefs DR
    backlinks: item.backlinks ?? 0,
    refDomains: item.referring_domains ?? 0,
    refMainDomains: item.referring_main_domains ?? 0,
    refIps: item.referring_ips ?? 0,
    brokenBacklinks: item.broken_backlinks ?? 0,
    spamScore: item.crawled_pages ? null : null, // not always in summary
    firstSeen: item.first_seen ?? null,
  };
}

export interface RankedKeywordsSummary {
  total: number;          // Total keywords ranking
  pos1to3: number;        // Top 3 rankings
  pos4to10: number;       // Top 10 rankings
  pos11to20: number;
  pos21to50: number;
  pos51to100: number;
  estTraffic: number;     // Estimated monthly organic traffic
  topKeywords: Array<{ keyword: string; position: number; volume: number; cpc: number; url: string; }>;
}

/** Get summary of all keywords a domain ranks for, plus top examples. */
export async function getRankedKeywords(target: string, locationCode = 2840, limit = 20): Promise<RankedKeywordsSummary | null> {
  const data = await call<any>('/dataforseo_labs/google/ranked_keywords/live', [{
    target,
    language_code: 'en',
    location_code: locationCode,
    limit,
    order_by: ['ranked_serp_element.serp_item.etv,desc'],
    filters: [['ranked_serp_element.serp_item.rank_group', '<=', 100]],
  }], 30000);
  if (!data) return null;
  const result = data.tasks?.[0]?.result?.[0];
  if (!result) return null;

  const items = result.items || [];
  const metrics = result.metrics?.organic;

  const topKeywords = items.slice(0, limit).map((it: any) => ({
    keyword: it.keyword_data?.keyword || '',
    position: it.ranked_serp_element?.serp_item?.rank_group || 0,
    volume: it.keyword_data?.keyword_info?.search_volume || 0,
    cpc: it.keyword_data?.keyword_info?.cpc || 0,
    url: it.ranked_serp_element?.serp_item?.url || '',
  }));

  return {
    total: metrics?.count ?? items.length,
    pos1to3: (metrics?.pos_1 ?? 0) + (metrics?.pos_2_3 ?? 0),
    pos4to10: metrics?.pos_4_10 ?? 0,
    pos11to20: metrics?.pos_11_20 ?? 0,
    pos21to50: metrics?.pos_21_50 ?? 0,
    pos51to100: metrics?.pos_51_100 ?? 0,
    estTraffic: Math.round(metrics?.etv ?? 0),
    topKeywords,
  };
}

export interface DomainTrafficOverview {
  domain: string;
  organic: {
    traffic: number;
    keywords: number;
    pos1: number; pos2to3: number; pos4to10: number;
    pos11to20: number; pos21to50: number; pos51to100: number;
    newKeywords: number; upKeywords: number; downKeywords: number; lostKeywords: number;
    trafficValue: number;
  };
  paid: {
    traffic: number;
    keywords: number;
    trafficValue: number;
  } | null;
}

/** Get full domain traffic overview — organic + paid metrics, position distribution, keyword movement. */
export async function getDomainTrafficOverview(domain: string, locationCode = 2840): Promise<DomainTrafficOverview | null> {
  const data = await call<any>('/dataforseo_labs/google/domain_rank_overview/live', [{
    target: domain, language_code: 'en', location_code: locationCode,
  }]);
  if (!data) return null;
  const result = data.tasks?.[0]?.result?.[0];
  const item = result?.items?.[0];
  if (!item) return null;
  const organic = item.metrics?.organic || {};
  const paid = item.metrics?.paid || {};
  return {
    domain: result?.target || domain,
    organic: {
      traffic: Math.round(organic.etv ?? 0),
      keywords: organic.count ?? 0,
      pos1: organic.pos_1 ?? 0,
      pos2to3: organic.pos_2_3 ?? 0,
      pos4to10: organic.pos_4_10 ?? 0,
      pos11to20: organic.pos_11_20 ?? 0,
      pos21to50: (organic.pos_21_30 ?? 0) + (organic.pos_31_40 ?? 0) + (organic.pos_41_50 ?? 0),
      pos51to100: (organic.pos_51_60 ?? 0) + (organic.pos_61_70 ?? 0) + (organic.pos_71_80 ?? 0) + (organic.pos_81_90 ?? 0) + (organic.pos_91_100 ?? 0),
      newKeywords: organic.is_new ?? 0,
      upKeywords: organic.is_up ?? 0,
      downKeywords: organic.is_down ?? 0,
      lostKeywords: organic.is_lost ?? 0,
      trafficValue: Math.round(organic.estimated_paid_traffic_cost ?? 0),
    },
    paid: paid.count > 0 ? {
      traffic: Math.round(paid.etv ?? 0),
      keywords: paid.count ?? 0,
      trafficValue: Math.round(paid.estimated_paid_traffic_cost ?? 0),
    } : null,
  };
}

export interface SerpResult {
  keyword: string;
  locationCode: number;
  organic: Array<{
    position: number;
    title: string;
    url: string;
    domain: string;
    description: string;
    breadcrumb?: string;
  }>;
  features: {
    featuredSnippet: { present: boolean; title?: string; description?: string; url?: string } | null;
    peopleAlsoAsk: { count: number; items: Array<{ question: string; answer?: string }> } | null;
    localPack: { present: boolean; places?: Array<{ title: string; rating?: number; reviews?: number }> } | null;
    images: boolean;
    videos: boolean;
    knowledgeGraph: boolean;
    relatedSearches: { count: number; terms: string[] } | null;
    topStories: boolean;
    shopping: boolean;
  };
}

/** Get full SERP results for a keyword — organic + all feature types, depth 100. */
export async function getSerpResults(keyword: string, locationCode = 2840): Promise<SerpResult | null> {
  const data = await call<any>('/serp/google/organic/live/regular', [{
    keyword, language_code: 'en', location_code: locationCode, depth: 100,
  }]);
  if (!data) return null;

  const taskResult = data.tasks?.[0]?.result?.[0];
  const items = taskResult?.items || [];

  // Extract organic results
  const organic = items
    .filter((it: any) => it.type === 'organic')
    .map((it: any) => ({
      position: it.rank_group || it.rank_absolute || 0,
      title: it.title || '',
      url: it.url || '',
      domain: it.domain || '',
      description: it.description || '',
      breadcrumb: it.breadcrumb || '',
    }));

  // Detect SERP features
  const featuredSnippetItem = items.find((it: any) => it.type === 'featured_snippet');
  const paaItem = items.find((it: any) => it.type === 'people_also_ask');
  const localPackItem = items.find((it: any) => it.type === 'local_pack');
  const relatedItem = items.find((it: any) => it.type === 'related_searches');

  const features = {
    featuredSnippet: featuredSnippetItem ? {
      present: true,
      title: featuredSnippetItem.title || '',
      description: featuredSnippetItem.description || '',
      url: featuredSnippetItem.url || '',
    } : null,
    peopleAlsoAsk: paaItem ? {
      count: (paaItem.items || []).length,
      items: (paaItem.items || []).map((q: any) => ({
        question: q.title || '',
        answer: q.expanded_element?.[0]?.description || '',
      })),
    } : null,
    localPack: localPackItem ? {
      present: true,
      places: (localPackItem.items || []).map((p: any) => ({
        title: p.title || '',
        rating: p.rating?.value,
        reviews: p.rating?.votes_count,
      })),
    } : null,
    images: items.some((it: any) => it.type === 'images'),
    videos: items.some((it: any) => it.type === 'video'),
    knowledgeGraph: items.some((it: any) => it.type === 'knowledge_graph'),
    relatedSearches: relatedItem ? {
      count: (relatedItem.items || []).length,
      terms: (relatedItem.items || []).map((r: any) => r.title || '').filter(Boolean),
    } : null,
    topStories: items.some((it: any) => it.type === 'top_stories'),
    shopping: items.some((it: any) => it.type === 'shopping'),
  };

  return {
    keyword: taskResult?.keyword || keyword,
    locationCode,
    organic,
    features,
  };
}

/** Runtime check — returns true if AUTH is configured. Using a function prevents build-time dead-code elimination. */
export function isDataforseoConfigured(): boolean {
  return !!AUTH;
}
