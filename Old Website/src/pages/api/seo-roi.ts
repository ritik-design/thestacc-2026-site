export const prerender = false;

import type { APIRoute } from 'astro';
import { getKeywordOverview } from '../../lib/dataforseo';

interface ROIVolumeResponse {
  keyword: string;
  volume: number;
  cpc: number;
  kd: number | null;
  intent: string;
  source: 'api' | 'fallback';
}

const INDUSTRY_KEYWORDS: Record<string, string> = {
  dentist: 'dentist',
  plumber: 'plumber',
  lawyer: 'lawyer',
  realtor: 'real estate agent',
  restaurant: 'restaurant',
  auto: 'auto repair',
  chiro: 'chiropractor',
  salon: 'salon',
};

const FALLBACK_VOLUME: Record<string, number> = {
  dentist: 1200,
  plumber: 900,
  lawyer: 600,
  realtor: 800,
  restaurant: 1500,
  auto: 700,
  chiro: 500,
  salon: 800,
};

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: { industry?: string; city?: string };

  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const industry = (body.industry || '').trim().toLowerCase();
  const city = (body.city || '').trim();

  if (!industry || !INDUSTRY_KEYWORDS[industry]) {
    return json({ error: 'Invalid industry' }, 400);
  }

  const baseKeyword = INDUSTRY_KEYWORDS[industry];
  const keyword = city ? `${baseKeyword} ${city}` : baseKeyword;

  // Fetch real data from DataForSEO
  let overview = null;
  try {
    overview = await getKeywordOverview(keyword, 2840);
  } catch {
    // Continue with fallback
  }

  // If API returned no volume, try the base keyword without city
  if (!overview || overview.volume === 0) {
    try {
      overview = await getKeywordOverview(baseKeyword, 2840);
    } catch {
      // Use fallback
    }
  }

  const volume = overview && overview.volume > 0 ? overview.volume : (FALLBACK_VOLUME[industry] || 800);
  const cpc = overview && overview.cpc > 0 ? overview.cpc : 10;
  const kd = overview?.kd ?? null;
  const intent = overview?.intent || 'unknown';
  const source = overview && overview.volume > 0 ? 'api' : 'fallback';

  return json({
    keyword,
    volume,
    cpc,
    kd,
    intent,
    source,
  } as ROIVolumeResponse, 200);
};
