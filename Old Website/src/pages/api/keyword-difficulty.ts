export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimi } from '../../lib/kimi';

interface DifficultyFactor {
  name: string;
  score: number;
  description: string;
}

interface DifficultyResult {
  keyword: string;
  overallScore: number;
  level: 'Easy' | 'Medium' | 'Hard' | 'Very Hard';
  searchVolume: string;
  timeToRank: string;
  contentDepth: string;
  factors: DifficultyFactor[];
  tips: string[];
}

interface DifficultyResponse {
  ok: boolean;
  data?: DifficultyResult;
  error?: string;
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: { keyword?: string };

  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: 'Invalid request body' }, 400);
  }

  const keyword = body.keyword?.trim() || '';

  if (!keyword) {
    return json({ ok: false, error: 'Keyword is required' }, 400);
  }

  if (keyword.length > 200) {
    return json({ ok: false, error: 'Keyword too long (max 200 chars)' }, 400);
  }

  const prompt = `Analyze the SEO difficulty for the keyword: "${keyword}".

Return ONLY a JSON object with this exact structure:
{
  "overallScore": 0-100,
  "level": "Easy" | "Medium" | "Hard" | "Very Hard",
  "searchVolume": "estimated monthly searches (e.g., 1K-10K or 10K-100K)",
  "timeToRank": "realistic months (e.g., 2-4 months)",
  "contentDepth": "word count recommendation (e.g., 1,500-2,500 words)",
  "factors": [
    { "name": "Competition", "score": 0-100, "description": "..." },
    { "name": "SERP Features", "score": 0-100, "description": "..." },
    { "name": "Content Quality", "score": 0-100, "description": "..." },
    { "name": "Backlinks Needed", "score": 0-100, "description": "..." },
    { "name": "Domain Authority", "score": 0-100, "description": "..." }
  ],
  "tips": ["tip 1", "tip 2", "tip 3"]
}

Rules:
- overallScore: 0-30 = Easy, 31-55 = Medium, 56-75 = Hard, 76-100 = Very Hard
- Be realistic — broad terms like "SEO" should score 80+, long-tail like "best CRM for dentists" should score 30-50
- Factors should reflect genuine SEO analysis patterns
- Tips must be actionable and specific to this keyword
- No markdown, no explanations outside the JSON`;

  const result = await callKimi({
    systemPrompt: 'You are an expert SEO analyst specializing in keyword difficulty assessment. You analyze keywords and provide realistic difficulty scores based on search patterns, competition, and ranking requirements. Always return valid JSON only.',
    userPrompt: prompt,
    maxTokens: 1500,
    temperature: 0.4,
    timeoutMs: 30000,
  });

  if (!result) {
    return json({ ok: false, error: 'AI analysis failed. Please try again.' }, 500);
  }

  let data: DifficultyResult;
  try {
    const jsonMatch = result.match(/\{[\s\S]*\}/);
    const parsed = JSON.parse(jsonMatch ? jsonMatch[0] : result);

    data = {
      keyword,
      overallScore: Math.min(100, Math.max(0, Number(parsed.overallScore) || 50)),
      level: ['Easy', 'Medium', 'Hard', 'Very Hard'].includes(parsed.level) ? parsed.level : 'Medium',
      searchVolume: String(parsed.searchVolume || 'Unknown'),
      timeToRank: String(parsed.timeToRank || '3-6 months'),
      contentDepth: String(parsed.contentDepth || '1,500-2,500 words'),
      factors: (parsed.factors || []).map((f: any) => ({
        name: String(f.name || 'Factor'),
        score: Math.min(100, Math.max(0, Number(f.score) || 50)),
        description: String(f.description || '').trim(),
      })).slice(0, 5),
      tips: (parsed.tips || []).map((t: any) => String(t)).filter((t: string) => t.length > 5).slice(0, 5),
    };
  } catch {
    return json({ ok: false, error: 'Could not parse analysis. Try a different keyword.' }, 500);
  }

  return json({
    ok: true,
    data,
  } as DifficultyResponse, 200);
};
