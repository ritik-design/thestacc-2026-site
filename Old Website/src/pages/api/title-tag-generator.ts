export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimi } from '../../lib/kimi';

interface TitleSuggestion {
  title: string;
  length: number;
  score: number;
  reason: string;
}

interface TitleTagResponse {
  ok: boolean;
  data?: {
    keyword: string;
    pageType: string;
    suggestions: TitleSuggestion[];
  };
  error?: string;
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: { keyword?: string; pageType?: string };

  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: 'Invalid request body' }, 400);
  }

  const keyword = body.keyword?.trim() || '';
  const pageType = body.pageType?.trim() || 'blog post';

  if (!keyword) {
    return json({ ok: false, error: 'Keyword is required' }, 400);
  }

  if (keyword.length > 200) {
    return json({ ok: false, error: 'Keyword too long (max 200 chars)' }, 400);
  }

  const prompt = `Generate 8 optimized title tags for a ${pageType} targeting the keyword: "${keyword}".

For each title tag, provide:
1. The complete title tag text
2. Character count
3. Score from 0-100 (based on SEO best practices: keyword placement, length 50-60 chars, click-worthiness, uniqueness)
4. One-line reason explaining the score

Rules:
- Mix of styles: some front-load the keyword, some use power words, some use numbers, some use questions
- Keep titles between 40-65 characters for optimal display
- Make them compelling and click-worthy
- Format as JSON array with fields: title, length, score, reason

Return ONLY valid JSON array. No markdown, no explanations.`;

  const result = await callKimi({
    systemPrompt: 'You are an expert SEO copywriter who specializes in title tag optimization. You write compelling, keyword-rich titles that earn clicks. Always return valid JSON arrays. No markdown.',
    userPrompt: prompt,
    maxTokens: 1500,
    temperature: 0.6,
    timeoutMs: 30000,
  });

  if (!result) {
    return json({ ok: false, error: 'AI generation failed. Please try again.' }, 500);
  }

  let suggestions: TitleSuggestion[] = [];
  try {
    const jsonMatch = result.match(/\[[\s\S]*\]/);
    if (jsonMatch) {
      suggestions = JSON.parse(jsonMatch[0]);
    } else {
      suggestions = JSON.parse(result);
    }

    suggestions = suggestions
      .filter((s: any) => s.title)
      .map((s: any) => ({
        title: String(s.title).trim(),
        length: Number(s.length) || String(s.title).length,
        score: Math.min(100, Math.max(0, Number(s.score) || 70)),
        reason: String(s.reason || 'Good title tag').trim(),
      }))
      .slice(0, 10)
      .sort((a, b) => b.score - a.score);
  } catch {
    suggestions = parseFallback(result, keyword);
  }

  if (suggestions.length === 0) {
    return json({ ok: false, error: 'Could not generate titles. Try a different keyword.' }, 500);
  }

  return json({
    ok: true,
    data: { keyword, pageType, suggestions },
  } as TitleTagResponse, 200);
};

function parseFallback(text: string, keyword: string): TitleSuggestion[] {
  const suggestions: TitleSuggestion[] = [];
  const lines = text.split('\n');

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    // Match numbered lines like "1. Title text (55 chars) - Score: 85"
    const match = trimmed.match(/^\d+[:.)\s]+(.+?)(?:\s*\(|\s*-|\s*\|)/);
    if (match) {
      const title = match[1].trim();
      const len = title.length;
      const scoreMatch = trimmed.match(/score[:\s]*(\d+)/i);
      const score = scoreMatch ? parseInt(scoreMatch[1], 10) : Math.round(Math.max(0, 100 - Math.abs(len - 55) * 3));

      suggestions.push({
        title,
        length: len,
        score: Math.min(100, Math.max(0, score)),
        reason: len >= 50 && len <= 60 ? 'Optimal length for SERP display' : len < 50 ? 'Could be more descriptive' : 'May be truncated in SERP',
      });
    }
  }

  return suggestions.slice(0, 10);
}
