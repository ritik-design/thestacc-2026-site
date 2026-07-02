export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimiJson } from '../../lib/kimi';
import { getSerpOrganic } from '../../lib/dataforseo';

interface RewriteResult {
  headline: string;
  why: string;
  predictedScore: number;
}

interface HeadlineAnalysisResponse {
  rewrites: RewriteResult[];
  critique: string;
  improvementTips: string[];
  serpHeadlines: string[] | null;
}

/* ── Helpers ── */
function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

/* ── Main handler ── */
export const POST: APIRoute = async ({ request }) => {
  let body: {
    headline?: string;
    contentType?: string;
    industry?: string;
    city?: string;
    targetKeyword?: string;
  };

  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const headline = body.headline?.trim();
  if (!headline || headline.length < 3) {
    return json({ error: 'Headline is required (min 3 chars)' }, 400);
  }

  const contentType = body.contentType || 'blog';
  const industry = body.industry || '';
  const city = body.city || '';
  const targetKeyword = body.targetKeyword?.trim() || '';

  // Parallel: Kimi rewrites + DataForSEO SERP
  const [kimiResult, serpItems] = await Promise.all([
    fetchKimiAnalysis(headline, contentType, industry, city),
    targetKeyword ? getSerpOrganic(targetKeyword).catch(() => []) : Promise.resolve([]),
  ]);

  const serpHeadlines = serpItems.length > 0
    ? serpItems.map((it: any) => it.title).filter(Boolean).slice(0, 10)
    : null;

  const response: HeadlineAnalysisResponse = {
    rewrites: kimiResult?.rewrites || [],
    critique: kimiResult?.critique || '',
    improvementTips: kimiResult?.improvementTips || [],
    serpHeadlines,
  };

  return json(response, 200);
};

/* ── Kimi Analysis ── */
async function fetchKimiAnalysis(
  headline: string,
  contentType: string,
  industry: string,
  city: string
): Promise<{ rewrites: RewriteResult[]; critique: string; improvementTips: string[] } | null> {
  const contextParts: string[] = [];
  if (contentType) contextParts.push(`Content type: ${contentType}`);
  if (industry) contextParts.push(`Industry: ${industry}`);
  if (city) contextParts.push(`Target city: ${city}`);
  const context = contextParts.length > 0 ? `\n\nContext: ${contextParts.join(', ')}` : '';

  const systemPrompt = `You are an expert copywriter and headline analyst for theStacc, an AI SEO automation platform. You specialize in writing high-performing headlines for local businesses.

Analyze the user's headline and provide:
1. A qualitative critique (2-3 sentences)
2. 5 rewritten alternatives, each with a brief explanation of why it works better
3. 3-5 specific improvement tips

Rules for rewrites:
- Keep them realistic and relevant to the original topic
- Match the content type (blog title, GBP post, page H1, or email subject)
- For local businesses, include city/industry keywords when relevant
- Use proven headline formulas: numbers, questions, how-to, lists, urgency, curiosity gaps
- Aim for 50-60 characters for blog/page titles, 30-50 for email subjects, 40-80 for GBP posts
- Each rewrite should feel different (don't just swap one word)

Return ONLY valid JSON. No markdown, no explanation outside JSON.`;

  const userPrompt = `Analyze this headline and provide alternatives:\n\nOriginal: "${headline}"${context}

Return JSON with this exact structure:
{
  "critique": "2-3 sentence qualitative analysis of what's working and what's missing in the original headline",
  "rewrites": [
    { "headline": " rewritten version 1", "why": "1-sentence explanation of why this works", "predictedScore": 85 },
    { "headline": " rewritten version 2", "why": "1-sentence explanation", "predictedScore": 82 },
    { "headline": " rewritten version 3", "why": "1-sentence explanation", "predictedScore": 80 },
    { "headline": " rewritten version 4", "why": "1-sentence explanation", "predictedScore": 78 },
    { "headline": " rewritten version 5", "why": "1-sentence explanation", "predictedScore": 75 }
  ],
  "improvementTips": [
    "Specific tip 1",
    "Specific tip 2",
    "Specific tip 3"
  ]
}`;

  return callKimiJson<{
    critique: string;
    rewrites: RewriteResult[];
    improvementTips: string[];
  }>({
    systemPrompt,
    userPrompt,
    maxTokens: 2048,
    temperature: 0.7,
    timeoutMs: 30000,
  });
}
