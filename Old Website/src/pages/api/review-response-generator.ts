// src/pages/api/review-response-generator.ts
// API endpoint for the Review Response Generator tool.
// POST /api/review-response-generator/
// Returns 3 ready-to-post Google review responses using Kimi LLM with quality scoring + fallback.
// Tier 3 — full output free, no email gate.

export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimiJson } from '../../lib/kimi';
import { getCached, setCached, hashInput, checkRateLimit } from '../../lib/cache';
import {
  REVIEW_RESPONSE_SYSTEM_PROMPT,
  buildReviewResponseUserPrompt,
  scoreReviewResponse,
  cleanAntiPatterns,
  hasAntiPattern,
  checkPrivilegedContentViolation,
  getResponseTimeHint,
  getResponseTip,
  getIndustrySafetyRules,
  type ReviewInput,
} from '../../lib/tools/review-response-prompts';

const VALID_TONES = ['professional', 'friendly', 'empathetic', 'brief'] as const;

const RATE_LIMIT_DAILY = 15;
const RATE_LIMIT_TTL_SEC = 86400;
const CACHE_VERSION = 'v1';
const CACHE_TTL_SEC = 86400;
const MIN_AVG_SCORE = 60;
const MAX_REGEN_ATTEMPTS = 2;

interface RawResponse {
  id?: number;
  variant: 'concise' | 'balanced' | 'detailed';
  text: string;
}

interface RawFlag {
  type: 'hipaa' | 'legal' | 'tone' | 'unverified_claim';
  message: string;
}

interface DecoratedResponse {
  id: number;
  variant: 'concise' | 'balanced' | 'detailed';
  label: string;
  text: string;
  score: number;
  wordCount: number;
  characterCount: number;
  warnings: string[];
  tip: string;
}

const VARIANT_LABELS: Record<RawResponse['variant'], string> = {
  concise: 'Concise',
  balanced: 'Balanced',
  detailed: 'Detailed',
};

function json(body: object, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function validateInput(body: any): { ok: true; data: ReviewInput } | { ok: false; error: { field: string; message: string } } {
  if (!body || typeof body !== 'object') return { ok: false, error: { field: '_', message: 'Invalid request body' } };

  const reviewText = String(body.reviewText || '').trim();
  const ratingNum = Number(body.rating);
  const biz = String(body.biz || '').trim();
  const industry = String(body.industry || '').trim();
  const city = String(body.city || '').trim();
  const reviewerName = body.reviewerName ? String(body.reviewerName).trim().slice(0, 50) : undefined;
  const tone = String(body.tone || 'professional').trim();

  if (!reviewText) return { ok: false, error: { field: 'reviewText', message: 'Please paste the review you want to respond to' } };
  if (reviewText.length < 10) return { ok: false, error: { field: 'reviewText', message: 'Review is too short — paste the full review (at least 10 characters)' } };
  if (reviewText.length > 2000) return { ok: false, error: { field: 'reviewText', message: 'Review is too long (max 2,000 characters)' } };

  if (!Number.isFinite(ratingNum) || ratingNum < 1 || ratingNum > 5 || !Number.isInteger(ratingNum)) {
    return { ok: false, error: { field: 'rating', message: 'Please pick the star rating (1-5)' } };
  }

  if (!biz) return { ok: false, error: { field: 'biz', message: 'Please enter your business name' } };
  if (biz.length > 100) return { ok: false, error: { field: 'biz', message: 'Business name too long (max 100 chars)' } };

  if (!industry) return { ok: false, error: { field: 'industry', message: 'Please select your industry' } };
  if (industry.length > 80) return { ok: false, error: { field: 'industry', message: 'Industry name too long' } };

  if (!city) return { ok: false, error: { field: 'city', message: 'Please enter your city' } };
  if (city.length > 80) return { ok: false, error: { field: 'city', message: 'City name too long (max 80 chars)' } };

  if (!VALID_TONES.includes(tone as any)) return { ok: false, error: { field: 'tone', message: 'Invalid tone' } };

  return {
    ok: true,
    data: {
      reviewText,
      rating: ratingNum as ReviewInput['rating'],
      biz,
      industry,
      city,
      reviewerName,
      tone: tone as ReviewInput['tone'],
    },
  };
}

function decorateResponse(resp: RawResponse, index: number, input: ReviewInput): DecoratedResponse {
  const variant: 'concise' | 'balanced' | 'detailed' = (resp.variant as any) || (['concise', 'balanced', 'detailed'][index] as any);
  let text = cleanAntiPatterns(resp.text || '');
  const score = scoreReviewResponse(text, input, variant);
  const wordCount = text.trim().split(/\s+/).length;
  const characterCount = text.length;

  const warnings: string[] = [];

  // Anti-pattern check
  if (hasAntiPattern(text)) warnings.push('Contains AI-sounding phrases — consider editing');

  // Privilege violation check
  const priv = checkPrivilegedContentViolation(text, input.industry);
  if (priv.violation) {
    if (priv.type === 'hipaa') warnings.push('HIPAA risk: response references specific treatment — edit before posting');
    if (priv.type === 'legal') warnings.push('Privilege risk: response references case details — edit before posting');
  }

  // Length warnings
  if (variant === 'concise' && wordCount > 100) warnings.push(`A bit long for "concise" (${wordCount} words) — Google truncates at ~80 in mobile preview`);
  if (variant === 'detailed' && wordCount > 240) warnings.push(`Above 240 words — readers skim long replies; consider trimming`);

  // Mention checks
  const cityShort = input.city.split(',')[0].trim().toLowerCase();
  if (!text.toLowerCase().includes(cityShort)) warnings.push(`City "${cityShort}" not mentioned — naturally fitting it once helps local SEO`);

  // Resolution path check for negative reviews
  const hasResolutionPath = /(call|email|reach out|contact|direct)/i.test(text);
  if (input.rating <= 2 && !hasResolutionPath) warnings.push('No off-platform path — add a phone number or "ask for the manager"');

  const tip = getResponseTip(input.rating, hasResolutionPath);

  return {
    id: index + 1,
    variant,
    label: VARIANT_LABELS[variant],
    text,
    score,
    wordCount,
    characterCount,
    warnings,
    tip,
  };
}

async function generateWithKimi(input: ReviewInput): Promise<{ responses: RawResponse[]; flags: RawFlag[] } | null> {
  const userPrompt = buildReviewResponseUserPrompt(input);
  let bestResult: { responses: RawResponse[]; flags: RawFlag[] } | null = null;
  let bestAvg = 0;

  for (let attempt = 0; attempt < MAX_REGEN_ATTEMPTS; attempt++) {
    const result = await callKimiJson<{ responses?: RawResponse[]; flags?: RawFlag[] }>({
      systemPrompt: attempt === 0 ? REVIEW_RESPONSE_SYSTEM_PROMPT : REVIEW_RESPONSE_SYSTEM_PROMPT + '\n\nIMPORTANT: previous attempt was generic or contained AI-sounding phrases. Use SPECIFIC details from the review, vary the openings, and lead with empathy (negatives) or genuine appreciation (positives). NO corporate-speak.',
      userPrompt,
      maxTokens: 2048,
      temperature: 0.75,
      timeoutMs: 45000,
    });

    if (!result?.responses || result.responses.length !== 3) {
      console.warn(`[review-response] Kimi attempt ${attempt + 1} returned invalid structure`);
      continue;
    }

    // Validate quality
    const variants: Array<'concise' | 'balanced' | 'detailed'> = ['concise', 'balanced', 'detailed'];
    const scores = result.responses.map((r, i) => {
      const v = (r.variant || variants[i]) as 'concise' | 'balanced' | 'detailed';
      return scoreReviewResponse(cleanAntiPatterns(r.text || ''), input, v);
    });
    const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
    console.log(`[review-response] Kimi attempt ${attempt + 1}: avg score ${avg.toFixed(1)}`);

    if (avg > bestAvg) {
      bestAvg = avg;
      bestResult = { responses: result.responses, flags: result.flags || [] };
    }

    if (avg >= MIN_AVG_SCORE) return { responses: result.responses, flags: result.flags || [] };
  }
  return bestResult;
}

// Tiny template fallback (used if Kimi unavailable). Intentionally minimal.
function generateTemplateFallback(input: ReviewInput): { responses: RawResponse[]; flags: RawFlag[] } {
  const cityShort = input.city.split(',')[0].trim();
  const name = input.reviewerName || 'there';
  const isPositive = input.rating >= 4;
  const isMixed = input.rating === 3;

  if (isPositive) {
    return {
      responses: [
        {
          id: 1,
          variant: 'concise',
          text: `Thanks, ${name}.\n\nGlad we could help. Looking forward to seeing you again at ${input.biz}.`,
        },
        {
          id: 2,
          variant: 'balanced',
          text: `Thanks for taking the time to share this, ${name}.\n\nReviews like yours mean a lot to our team — they remind us why we do what we do. Glad to be part of your day in ${cityShort}.\n\nSee you next time at ${input.biz}.`,
        },
        {
          id: 3,
          variant: 'detailed',
          text: `${name}, thank you so much.\n\nWe work hard to make every visit feel exactly the way you described it, and hearing it landed for you is the best feedback our team can get. The whole crew at ${input.biz} appreciates you taking the time to share this.\n\nIf you know anyone in ${cityShort} who could use what we do, please send them our way. And we'll see you next time.`,
        },
      ],
      flags: [],
    };
  }

  if (isMixed) {
    return {
      responses: [
        {
          id: 1,
          variant: 'concise',
          text: `Thanks for the honest feedback, ${name}.\n\nWe hear you and we'll work on it. Please give ${input.biz} another shot in ${cityShort}.`,
        },
        {
          id: 2,
          variant: 'balanced',
          text: `Thank you for sharing this, ${name}.\n\nMixed feedback is the most useful kind — it tells us what's working and where we have room to grow. Our team is talking through what you described.\n\nIf you come back to ${input.biz}, please mention this review at the front and we'll make it right.`,
        },
        {
          id: 3,
          variant: 'detailed',
          text: `Thanks for the honest review, ${name}.\n\nWe take feedback like yours seriously — it's how every business in ${cityShort} actually improves. The parts of your visit that worked, we'll keep doing. The parts that didn't, our team is reviewing this week.\n\nPlease come back to ${input.biz} and ask for the manager when you arrive. We'd like to take care of you personally and prove the experience can be much better.`,
        },
      ],
      flags: [],
    };
  }

  // Negative
  return {
    responses: [
      {
        id: 1,
        variant: 'concise',
        text: `${name}, this isn't the experience anyone should have at ${input.biz}.\n\nPlease call our office and ask for the manager so we can make this right.`,
      },
      {
        id: 2,
        variant: 'balanced',
        text: `${name}, I'm sorry — this isn't the experience we want anyone to have.\n\nWhat you described isn't acceptable, and that's on us. We should have done better.\n\nPlease call ${input.biz} directly and ask for the manager. I'd like to make this right.`,
      },
      {
        id: 3,
        variant: 'detailed',
        text: `${name}, I want to start by saying I hear you, and I'm sorry.\n\nThe experience you described isn't what we aim for, and the fact that it happened tells me we have work to do. We should have done better — full stop, no excuses.\n\nI'd like to take care of this directly. Please call our office in ${cityShort} and ask for the manager. I'll personally pull your file and we'll find a way forward.\n\n— the team at ${input.biz}`,
      },
    ],
    flags: [],
  };
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
  const rl = await checkRateLimit(`rrg_rl:${ip}`, RATE_LIMIT_DAILY, RATE_LIMIT_TTL_SEC);
  if (!rl.allowed) {
    return json({
      success: false,
      error: 'rate_limit',
      message: `You've used all ${RATE_LIMIT_DAILY} free generations today. Resets in ${Math.ceil((rl.resetAt.getTime() - Date.now()) / (3600 * 1000))} hours.`,
      ratelimitResetAt: rl.resetAt.toISOString(),
      ctaUrl: '/demo/?source=review-response-tool-ratelimit',
    }, 429);
  }

  // 3. Cache check
  const cacheKey = `rrg:${CACHE_VERSION}:${hashInput(input)}`;
  const cached = await getCached<any>(cacheKey);
  if (cached?.responses) {
    return json({
      ...cached,
      metadata: {
        ...cached.metadata,
        cached: true,
        ratelimitRemaining: rl.remaining,
      },
    });
  }

  // 4. Generate
  let raw: { responses: RawResponse[]; flags: RawFlag[] } | null = null;
  let fallback = false;

  raw = await generateWithKimi(input);
  if (!raw || raw.responses.length !== 3) {
    raw = generateTemplateFallback(input);
    fallback = true;
  }

  // 5. Decorate
  const responses = raw.responses.map((r, i) => decorateResponse(r, i, input));

  // 6. Aggregate flags
  const flags = [...(raw.flags || [])];
  // Add a top-level flag if any response had a privilege warning
  const anyPrivWarning = responses.some(r => r.warnings.some(w => w.includes('HIPAA') || w.includes('Privilege')));
  if (anyPrivWarning && !flags.some(f => f.type === 'hipaa' || f.type === 'legal')) {
    flags.push({
      type: 'tone',
      message: 'One or more responses references specifics that may need editing — review the warning labels before posting.',
    });
  }

  // 7. Build response
  const response = {
    success: true,
    responses,
    flags,
    metadata: {
      industry: input.industry,
      rating: input.rating,
      tone: input.tone,
      avgScore: Math.round(responses.reduce((a, r) => a + r.score, 0) / responses.length),
      responseTimeHint: getResponseTimeHint(input.rating),
      industrySafetyNotes: getIndustrySafetyRules(input.industry),
      ratelimitRemaining: rl.remaining,
      cached: false,
      fallback,
      generatedAt: new Date().toISOString(),
    },
  };

  // 8. Cache
  await setCached(cacheKey, response, CACHE_TTL_SEC);

  return json(response, 200);
};
