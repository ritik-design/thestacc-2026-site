export const prerender = false;

import type { APIRoute } from 'astro';
import { getSerpOrganic } from '../../lib/dataforseo';
import { callKimiJson } from '../../lib/kimi';

interface SerpComparisonItem {
  rank: number;
  domain: string;
  title: string;
  titleLen: number;
  description: string;
  descLen: number;
}

interface MetaRewrite {
  type: 'title' | 'description';
  original: string;
  rewritten: string;
  reason: string;
  score: number;
}

interface MetaAnalysisResponse {
  keyword: string;
  serpItems: SerpComparisonItem[];
  rewrites: MetaRewrite[];
  critique: string;
  titlePatterns: string[];
  descPatterns: string[];
  avgTitleLen: number;
  avgDescLen: number;
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: { url?: string; keyword?: string; currentTitle?: string; currentDesc?: string };

  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const keyword = body.keyword?.trim() || '';
  const currentTitle = body.currentTitle?.trim() || '';
  const currentDesc = body.currentDesc?.trim() || '';

  if (!keyword || keyword.length < 2) {
    return json({ error: 'Target keyword is required (min 2 chars)' }, 400);
  }

  // 1. Fetch SERP data
  let serpItems: SerpComparisonItem[] = [];
  try {
    const organic = await getSerpOrganic(keyword, 2840);
    serpItems = organic.slice(0, 10).map((it) => ({
      rank: it.rank,
      domain: it.domain,
      title: it.title || '',
      titleLen: (it.title || '').length,
      description: it.description || '',
      descLen: (it.description || '').length,
    }));
  } catch {
    // Continue without SERP data
  }

  // 2. Call Kimi for rewrites + critique
  const aiResult = await generateRewrites(currentTitle, currentDesc, keyword, serpItems);

  // 3. Calculate averages
  const avgTitleLen = serpItems.length > 0
    ? Math.round(serpItems.reduce((s, it) => s + it.titleLen, 0) / serpItems.length)
    : 50;
  const avgDescLen = serpItems.length > 0
    ? Math.round(serpItems.reduce((s, it) => s + it.descLen, 0) / serpItems.length)
    : 145;

  // 4. Extract patterns from SERP titles/descriptions
  const titlePatterns = extractPatterns(serpItems.map((it) => it.title));
  const descPatterns = extractPatterns(serpItems.map((it) => it.description));

  return json({
    keyword,
    serpItems: serpItems.slice(0, 10),
    rewrites: aiResult?.rewrites || [],
    critique: aiResult?.critique || '',
    titlePatterns: titlePatterns.slice(0, 5),
    descPatterns: descPatterns.slice(0, 5),
    avgTitleLen,
    avgDescLen,
  } as MetaAnalysisResponse, 200);
};

async function generateRewrites(
  currentTitle: string,
  currentDesc: string,
  keyword: string,
  serpItems: SerpComparisonItem[]
): Promise<{ rewrites: MetaRewrite[]; critique: string } | null> {
  const serpContext = serpItems.slice(0, 5).map((it) =>
    `Rank ${it.rank}: "${it.title}" | "${it.description}"`
  ).join('\n');

  const systemPrompt = `You are an expert SEO copywriter who specializes in writing high-converting title tags and meta descriptions. You analyze competing SERP results and write better versions that stand out. Return ONLY valid JSON.`;

  const userPrompt = `Analyze the following title tag and meta description for the keyword "${keyword}". Compare against the top 5 SERP results and provide improved rewrites.

CURRENT TAGS:
Title: "${currentTitle || '(missing)'}")
Description: "${currentDesc || '(missing)'}")

TOP 5 SERP RESULTS:
${serpContext}

Return JSON only:
{
  "rewrites": [
    {
      "type": "title",
      "original": "${currentTitle || ''}",
      "rewritten": "Improved title here",
      "reason": "Why this version is better",
      "score": 85
    },
    {
      "type": "title",
      "original": "${currentTitle || ''}",
      "rewritten": "Alternative improved title",
      "reason": "Why this version works",
      "score": 82
    },
    {
      "type": "description",
      "original": "${currentDesc || ''}",
      "rewritten": "Improved description here",
      "reason": "Why this converts better",
      "score": 88
    },
    {
      "type": "description",
      "original": "${currentDesc || ''}",
      "rewritten": "Alternative improved description",
      "reason": "Why this stands out in SERP",
      "score": 85
    }
  ],
  "critique": "2-3 sentences analyzing the current title/description against SERP competition. Be specific about what's weak and what the top performers do better."
}`;

  const result = await callKimiJson<{ rewrites: MetaRewrite[]; critique: string }>({
    systemPrompt,
    userPrompt,
    maxTokens: 2048,
    temperature: 0.6,
    timeoutMs: 30000,
  });

  if (!result?.rewrites) return null;

  return {
    rewrites: result.rewrites.slice(0, 4),
    critique: result.critique || '',
  };
}

function extractPatterns(texts: string[]): string[] {
  const patterns: string[] = [];
  const joined = texts.join(' ').toLowerCase();

  if (/\d{4}/.test(joined)) patterns.push('Uses year numbers');
  if (/(best|top|ultimate|complete|definitive|guide)/.test(joined)) patterns.push('Superlative adjectives (best, top, ultimate)');
  if (/(how to|step by step|tutorial)/.test(joined)) patterns.push('How-to / instructional framing');
  if (/(\?|what|why|how)/.test(joined)) patterns.push('Question-based titles');
  if (/(free|tool|generator|checker|analyzer)/.test(joined)) patterns.push('Tool-type keywords');
  if (/(202[4-9]|20[3-9][0-9])/.test(joined)) patterns.push('Current year references');
  if (/(learn|discover|find out|see)/.test(joined)) patterns.push('Action verbs (learn, discover)');
  if (/(\||–|-|:)/.test(joined)) patterns.push('Separator characters (pipe, dash)');
  if (/(seo|ranking|traffic|google)/.test(joined)) patterns.push('SEO/power keywords');

  return patterns.length > 0 ? patterns : ['Descriptive titles', 'Brand mentions'];
}
