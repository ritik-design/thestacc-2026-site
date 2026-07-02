export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimi } from '../../lib/kimi';

interface ContentGap {
  topic: string;
  priority: 'High' | 'Medium' | 'Low';
  reason: string;
  format: string;
  estimatedWords: string;
}

interface GapResult {
  keyword: string;
  totalGaps: number;
  highPriority: number;
  mediumPriority: number;
  lowPriority: number;
  gaps: ContentGap[];
  summary: string;
}

interface GapResponse {
  ok: boolean;
  data?: GapResult;
  error?: string;
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: { keyword?: string; competitorUrl?: string };

  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: 'Invalid request body' }, 400);
  }

  const keyword = body.keyword?.trim() || '';
  const competitorUrl = body.competitorUrl?.trim() || '';

  if (!keyword) {
    return json({ ok: false, error: 'Keyword is required' }, 400);
  }

  if (keyword.length > 200) {
    return json({ ok: false, error: 'Keyword too long (max 200 chars)' }, 400);
  }

  const competitorContext = competitorUrl
    ? `Also analyze the competitor URL: ${competitorUrl} for additional gap insights.`
    : '';

  const prompt = `Analyze the keyword "${keyword}" and identify 6 content gaps — subtopics missing from existing content.

${competitorContext}

Return ONLY JSON:
{
  "summary": "2 sentences on the biggest opportunity",
  "gaps": [
    {
      "topic": "specific subtopic",
      "priority": "High" | "Medium" | "Low",
      "reason": "why this gap matters",
      "format": "e.g., guide, comparison, case study, checklist",
      "estimatedWords": "e.g., 800-1,200 words"
    }
  ]
}

Rules: distinct topics, no duplicates, actionable for writers, varied formats.`;

  const result = await callKimi({
    systemPrompt: 'You are an expert content strategist. Find content gaps. Return ONLY valid JSON.',
    userPrompt: prompt,
    maxTokens: 1500,
    temperature: 0.5,
    timeoutMs: 30000,
  });

  if (!result) {
    return json({ ok: false, error: 'AI analysis failed. Please try again.' }, 500);
  }

  let data: GapResult;
  try {
    const jsonMatch = result.match(/\{[\s\S]*\}/);
    const parsed = JSON.parse(jsonMatch ? jsonMatch[0] : result);

    const gaps: ContentGap[] = (parsed.gaps || [])
      .map((g: any) => ({
        topic: String(g.topic || '').trim(),
        priority: ['High', 'Medium', 'Low'].includes(g.priority) ? g.priority : 'Medium',
        reason: String(g.reason || '').trim(),
        format: String(g.format || 'Blog post').trim(),
        estimatedWords: String(g.estimatedWords || '1,000-1,500 words').trim(),
      }))
      .filter((g: ContentGap) => g.topic.length > 3)
      .slice(0, 12);

    const high = gaps.filter((g: ContentGap) => g.priority === 'High').length;
    const medium = gaps.filter((g: ContentGap) => g.priority === 'Medium').length;
    const low = gaps.filter((g: ContentGap) => g.priority === 'Low').length;

    data = {
      keyword,
      totalGaps: gaps.length,
      highPriority: high,
      mediumPriority: medium,
      lowPriority: low,
      gaps,
      summary: String(parsed.summary || `Found ${gaps.length} content gaps for "${keyword}".`).trim(),
    };
  } catch {
    return json({ ok: false, error: 'Could not parse analysis. Try a different keyword.' }, 500);
  }

  return json({
    ok: true,
    data,
  } as GapResponse, 200);
};
