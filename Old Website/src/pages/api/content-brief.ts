export const prerender = false;

import type { APIRoute } from 'astro';
import {
  getSerpOrganic,
  getPeopleAlsoAsk,
  getKeywordOverview,
  getRelatedKeywords,
} from '../../lib/dataforseo';
import { callKimiJson } from '../../lib/kimi';

interface CompetitorItem {
  domain: string;
  title: string;
  description: string;
  wordCount: number | null;
}

interface BriefKeyword {
  keyword: string;
  volume: number;
  kd: number | null;
  intent: string;
}

interface HeadingItem {
  level: number;
  text: string;
}

interface ContentBriefResponse {
  keyword: string;
  contentType: string;
  mainKeyword: {
    volume: number;
    kd: number | null;
    cpc: number;
    intent: string;
  };
  titles: string[];
  outline: HeadingItem[];
  targetWordCount: { min: number; max: number; rationale: string };
  keywords: BriefKeyword[];
  questions: string[];
  competitors: CompetitorItem[];
  contentAngle: string;
  searchIntent: string;
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: { keyword?: string; contentType?: string };

  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const keyword = body.keyword?.trim();
  if (!keyword || keyword.length < 2) {
    return json({ error: 'Target keyword is required (min 2 chars)' }, 400);
  }

  const contentType = body.contentType || 'blog';

  // 1. Fetch all data in parallel
  const [serpItems, paaItems, overview, related] = await Promise.all([
    getSerpOrganic(keyword, 2840).catch(() => []),
    getPeopleAlsoAsk(keyword, 2840).catch(() => []),
    getKeywordOverview(keyword, 2840).catch(() => null),
    getRelatedKeywords(keyword, 2840, 15).catch(() => []),
  ]);

  // 2. Build competitor data from SERP
  const competitors: CompetitorItem[] = serpItems.slice(0, 10).map((it) => ({
    domain: it.domain,
    title: it.title || '',
    description: it.description || '',
    wordCount: it.wordCount || null,
  }));

  // 3. Build keyword data
  const briefKeywords: BriefKeyword[] = [
    { keyword, volume: overview?.volume || 0, kd: overview?.kd, intent: overview?.intent || 'unknown' },
    ...related.slice(0, 14).map((r) => ({
      keyword: r.keyword,
      volume: r.volume || 0,
      kd: r.kd,
      intent: 'related',
    })),
  ];

  // 4. Build questions from PAA
  const questions = paaItems.map((p) => p.question).filter(Boolean);

  // 5. Call Kimi for AI-generated brief components
  const aiBrief = await generateBriefWithKimi(keyword, contentType, competitors, questions, briefKeywords);

  const response: ContentBriefResponse = {
    keyword,
    contentType,
    mainKeyword: {
      volume: overview?.volume || 0,
      kd: overview?.kd,
      cpc: overview?.cpc || 0,
      intent: overview?.intent || 'unknown',
    },
    titles: aiBrief?.titles || [],
    outline: aiBrief?.outline || [],
    targetWordCount: aiBrief?.targetWordCount || { min: 1500, max: 2500, rationale: 'Standard length for this content type' },
    keywords: briefKeywords,
    questions: questions.length > 0 ? questions : (aiBrief?.questions || []),
    competitors,
    contentAngle: aiBrief?.contentAngle || '',
    searchIntent: aiBrief?.searchIntent || (overview?.intent || 'unknown'),
  };

  return json(response, 200);
};

async function generateBriefWithKimi(
  keyword: string,
  contentType: string,
  competitors: CompetitorItem[],
  questions: string[],
  keywords: BriefKeyword[]
): Promise<{
  titles: string[];
  outline: HeadingItem[];
  targetWordCount: { min: number; max: number; rationale: string };
  questions: string[];
  contentAngle: string;
  searchIntent: string;
} | null> {
  const competitorContext = competitors.slice(0, 5).map((c, i) =>
    `Rank ${i + 1}: ${c.domain} — "${c.title}"`
  ).join('\n');

  const questionContext = questions.slice(0, 8).join('\n');
  const keywordContext = keywords.slice(0, 10).map((k) =>
    `- ${k.keyword} (vol: ${k.volume}${k.kd ? `, KD: ${k.kd}` : ''})`
  ).join('\n');

  const systemPrompt = `You are a senior SEO content strategist who creates detailed content briefs. You analyze SERP competition and write actionable briefs that help writers create content that ranks. Return ONLY valid JSON. No markdown, no explanation outside JSON.`;

  const userPrompt = `Create a content brief for the keyword "${keyword}" as a ${contentType}.

TOP 5 COMPETITORS:
${competitorContext}

PEOPLE ALSO ASK QUESTIONS:
${questionContext || 'No PAA data available'}

RELEVANT KEYWORDS:
${keywordContext}

Return JSON with this exact structure:
{
  "titles": ["5 suggested title tags, optimized for CTR"],
  "outline": [
    { "level": 1, "text": "H1: Main heading" },
    { "level": 2, "text": "H2: Section heading" },
    { "level": 3, "text": "H3: Subsection" }
  ],
  "targetWordCount": { "min": 1500, "max": 2500, "rationale": "Why this length based on competitors" },
  "questions": ["5-8 additional questions the content should answer"],
  "contentAngle": "1-2 sentence recommendation for the unique angle that will differentiate this content",
  "searchIntent": "informational|transactional|navigational|commercial"
}

Rules:
- Outline should have 1 H1, 4-6 H2s, and 2-3 H3s under each H2
- Titles should be 50-60 characters and include the target keyword
- Target word count should be based on competitor analysis (aim for top 25% length)
- Content angle must be differentiated from what's already ranking
- Questions should cover gaps competitors miss`;

  const result = await callKimiJson<{
    titles: string[];
    outline: HeadingItem[];
    targetWordCount: { min: number; max: number; rationale: string };
    questions: string[];
    contentAngle: string;
    searchIntent: string;
  }>({
    systemPrompt,
    userPrompt,
    maxTokens: 3000,
    temperature: 0.65,
    timeoutMs: 35000,
  });

  return result;
}
