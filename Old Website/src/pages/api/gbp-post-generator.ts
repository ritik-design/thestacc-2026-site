// src/pages/api/gbp-post-generator.ts
// API endpoint for the GBP Post Generator tool.
// POST /api/gbp-post-generator/
// Returns 3 ready-to-publish GBP posts using Kimi LLM with quality scoring + fallback.

export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimiJson } from '../../lib/kimi';
import { getCached, setCached, hashInput, checkRateLimit } from '../../lib/cache';
import {
  GBP_SYSTEM_PROMPT,
  buildGBPUserPrompt,
  getBestTimeToPost,
  scoreGBPPost,
  cleanAntiPatterns,
  hasAntiPattern,
  type GBPInput,
} from '../../lib/tools/gbp-prompts';

const VALID_ANGLES = ['tip', 'seasonal', 'story', 'offer', 'bts', 'faq'] as const;
const VALID_TONES = ['professional', 'friendly', 'casual'] as const;
const VALID_CTAS = ['Book', 'Order online', 'Buy', 'Learn more', 'Sign up', 'Call now', 'Get offer'];

const RATE_LIMIT_DAILY = 10;
const RATE_LIMIT_TTL_SEC = 86400;
const CACHE_VERSION = 'v3';
const CACHE_TTL_SEC = 86400;
const MIN_AVG_SCORE = 60;
const MAX_REGEN_ATTEMPTS = 2;

interface RawPost { id?: number; length: 'short' | 'medium' | 'long'; text: string; }

interface DecoratedPost {
  id: number;
  length: 'short' | 'medium' | 'long';
  text: string;
  score: number;
  characterCount: number;
  previewText: string;
  imagePrompt: string;
  warnings: string[];
}

function json(body: object, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function validateInput(body: any): { ok: true; data: GBPInput } | { ok: false; error: { field: string; message: string } } {
  if (!body || typeof body !== 'object') return { ok: false, error: { field: '_', message: 'Invalid request body' } };
  const biz = String(body.biz || '').trim();
  const city = String(body.city || '').trim();
  const industry = String(body.industry || '').trim();
  const angle = String(body.angle || '').trim();
  const tone = String(body.tone || 'professional').trim();
  const cta = String(body.cta || 'Learn more').trim();

  if (!biz) return { ok: false, error: { field: 'biz', message: 'Please enter your business name' } };
  if (biz.length > 100) return { ok: false, error: { field: 'biz', message: 'Business name too long (max 100 chars)' } };
  if (!city) return { ok: false, error: { field: 'city', message: 'Please enter your city' } };
  if (city.length > 60) return { ok: false, error: { field: 'city', message: 'City name too long (max 60 chars)' } };
  if (!industry) return { ok: false, error: { field: 'industry', message: 'Please select your industry' } };
  if (industry.length > 80) return { ok: false, error: { field: 'industry', message: 'Industry name too long' } };
  if (!VALID_ANGLES.includes(angle as any)) return { ok: false, error: { field: 'angle', message: 'Invalid post angle' } };
  if (!VALID_TONES.includes(tone as any)) return { ok: false, error: { field: 'tone', message: 'Invalid tone' } };
  if (!VALID_CTAS.includes(cta)) return { ok: false, error: { field: 'cta', message: 'Invalid CTA button' } };

  const topic = body.topic ? String(body.topic).trim().slice(0, 200) : undefined;
  let offer: GBPInput['offer'] = null;
  if (angle === 'offer' && body.offer && typeof body.offer === 'object') {
    offer = {
      title: body.offer.title ? String(body.offer.title).trim().slice(0, 80) : undefined,
      coupon: body.offer.coupon ? String(body.offer.coupon).trim().slice(0, 30) : undefined,
      terms: body.offer.terms ? String(body.offer.terms).trim().slice(0, 200) : undefined,
    };
  }

  return {
    ok: true,
    data: { biz, city, industry, angle: angle as GBPInput['angle'], tone: tone as GBPInput['tone'], cta, topic, offer },
  };
}

function decoratePost(post: RawPost, index: number, input: GBPInput): DecoratedPost {
  const length: 'short' | 'medium' | 'long' = (post.length as any) || (['short', 'medium', 'long'][index] as any);
  let text = cleanAntiPatterns(post.text || '');

  const score = scoreGBPPost(text, input.city, input.industry, input.cta, length);
  const characterCount = text.length;
  const previewText = text.slice(0, 80);

  const warnings: string[] = [];
  if (characterCount > 300 && length === 'short') warnings.push('Truncated in Google preview — keep under 80 chars before "...read more"');
  if (characterCount > 1500) warnings.push('Above Google\'s 1500-character display limit');
  if (hasAntiPattern(text)) warnings.push('Contains AI-sounding phrases — consider rewriting');
  if (!text.toLowerCase().includes(input.city.split(',')[0].toLowerCase())) warnings.push(`City "${input.city}" not mentioned`);

  const imagePrompt = generateImagePrompt(input);

  return {
    id: index + 1,
    length,
    text,
    score,
    characterCount,
    previewText,
    imagePrompt,
    warnings,
  };
}

function generateImagePrompt(input: GBPInput): string {
  const ind = input.industry.toLowerCase();
  let scenario = 'a real photo of your team or workspace';
  if (ind.includes('dental')) scenario = 'a real photo of your dental team, treatment room, or patient smile (with permission)';
  else if (ind.includes('plumb') || ind.includes('hvac')) scenario = 'a real photo of your truck, tools, or a recent install';
  else if (ind.includes('legal') || ind.includes('law')) scenario = 'a real photo of your office, your team, or local courthouse';
  else if (ind.includes('restaurant') || ind.includes('cafe')) scenario = 'a real photo of a signature dish, your kitchen, or your dining room';
  else if (ind.includes('salon') || ind.includes('beauty')) scenario = 'a real photo of a recent transformation (client permission), your stylist, or your space';
  else if (ind.includes('auto') || ind.includes('mechanic')) scenario = 'a real photo of your shop, a recent repair, or your team';
  else if (ind.includes('real estate')) scenario = 'a real photo of a recent listing, an open house, or your local market';
  return `${scenario}. Size: 1200×900px, real photo only (Google deprioritizes stock images).`;
}

async function generateWithKimi(input: GBPInput): Promise<RawPost[] | null> {
  const userPrompt = buildGBPUserPrompt(input);
  let bestPosts: RawPost[] | null = null;
  let bestAvg = 0;

  for (let attempt = 0; attempt < MAX_REGEN_ATTEMPTS; attempt++) {
    const result = await callKimiJson<{ posts?: RawPost[] }>({
      systemPrompt: attempt === 0 ? GBP_SYSTEM_PROMPT : GBP_SYSTEM_PROMPT + '\n\nIMPORTANT: previous attempt produced low-quality output. Use SPECIFIC numbers, named scenarios, and active voice. NO generic phrases.',
      userPrompt,
      maxTokens: 2048,
      temperature: 0.7,
      timeoutMs: 45000,
    });

    if (!result?.posts || result.posts.length !== 3) {
      console.warn(`[gbp] Kimi attempt ${attempt + 1} returned invalid structure`);
      continue;
    }

    // Validate quality
    const lengths: Array<'short' | 'medium' | 'long'> = ['short', 'medium', 'long'];
    const scores = result.posts.map((p, i) => {
      const len = (p.length || lengths[i]) as 'short' | 'medium' | 'long';
      return scoreGBPPost(cleanAntiPatterns(p.text || ''), input.city, input.industry, input.cta, len);
    });
    const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
    console.log(`[gbp] Kimi attempt ${attempt + 1}: avg score ${avg.toFixed(1)}`);

    // Track best attempt
    if (avg > bestAvg) {
      bestAvg = avg;
      bestPosts = result.posts;
    }

    if (avg >= MIN_AVG_SCORE) return result.posts;
  }
  // Return best attempt even if below threshold (better than template)
  return bestPosts;
}

// Tiny template fallback (used if Kimi unavailable). Intentionally minimal —
// quality bar is met by Kimi; fallback just guarantees non-empty output.
function generateTemplateFallback(input: GBPInput): RawPost[] {
  const cityName = input.city.split(',')[0].trim();
  const ind = input.industry.split('/')[0].trim();
  return [
    {
      id: 1,
      length: 'short',
      text: `Looking for ${ind.toLowerCase()} in ${cityName}? ${input.biz} has been helping locals for years. ${input.cta === 'Call now' ? 'Call us today.' : input.cta + ' to get started.'}`,
    },
    {
      id: 2,
      length: 'medium',
      text: `${input.biz} works with ${cityName} customers every week. We focus on doing the job right the first time — no surprises, no upsells. Recent customers have saved time and money by calling early instead of waiting for problems to grow.\n\n${input.cta} to see how we can help.`,
    },
    {
      id: 3,
      length: 'long',
      text: `Here's what we tell every new customer at ${input.biz}: don't wait. Most ${ind.toLowerCase()} situations are easier and cheaper to solve early than late.\n\nWe've been serving ${cityName} for years, and the pattern is consistent. Customers who call at the first sign of an issue spend less and get back to normal faster.\n\nIf you've been putting something off, this is your sign. ${input.cta} and we'll take a look.`,
    },
  ];
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

  const input = validation.data;

  // 2. Rate limit
  const ip = clientAddress || 'unknown';
  const rl = await checkRateLimit(`gbp_rl:${ip}`, RATE_LIMIT_DAILY, RATE_LIMIT_TTL_SEC);
  if (!rl.allowed) {
    return json({
      success: false,
      error: 'rate_limit',
      message: `You've used all ${RATE_LIMIT_DAILY} free generations today. Resets in ${Math.ceil((rl.resetAt.getTime() - Date.now()) / (3600 * 1000))} hours.`,
      ratelimitResetAt: rl.resetAt.toISOString(),
      ctaUrl: '/demo/?source=gbp-tool-ratelimit',
    }, 429);
  }

  // 3. Cache check
  const cacheKey = `gbp:${CACHE_VERSION}:${hashInput(input)}`;
  const cached = await getCached<any>(cacheKey);
  if (cached?.posts) {
    return json({
      ...cached,
      metadata: {
        ...cached.metadata,
        cached: true,
        ratelimitRemaining: rl.remaining,
        bestTimeToPost: getBestTimeToPost(input.industry),
      },
    });
  }

  // 4. Generate
  let rawPosts: RawPost[] | null = null;
  let fallback = false;

  rawPosts = await generateWithKimi(input);
  if (!rawPosts || rawPosts.length !== 3) {
    rawPosts = generateTemplateFallback(input);
    fallback = true;
  }

  // 5. Decorate (score, character count, warnings, image prompt)
  const posts = rawPosts.map((p, i) => decoratePost(p, i, input));

  // 6. Build response
  const response = {
    success: true,
    posts,
    metadata: {
      industry: input.industry,
      angle: input.angle,
      bestTimeToPost: getBestTimeToPost(input.industry),
      ratelimitRemaining: rl.remaining,
      cached: false,
      fallback,
      generatedAt: new Date().toISOString(),
    },
  };

  // 7. Cache
  await setCached(cacheKey, response, CACHE_TTL_SEC);

  return json(response, 200);
};
