export const prerender = false;

import type { APIRoute } from 'astro';
import { getPeopleAlsoAsk } from '../../lib/dataforseo';
import { callKimiJson } from '../../lib/kimi';

interface PAAItem {
  question: string;
  answer: string;
}

interface SchemaPAAResponse {
  keyword: string;
  paaItems: PAAItem[];
  source: 'dataforseo' | 'fallback' | 'none';
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: { keyword?: string; industry?: string; businessName?: string };

  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const keyword = body.keyword?.trim();
  if (!keyword || keyword.length < 2) {
    return json({ error: 'Keyword is required (min 2 chars)' }, 400);
  }

  const industry = body.industry?.trim() || '';
  const businessName = body.businessName?.trim() || '';

  // 1. Fetch real PAA from DataForSEO
  let paaItems: PAAItem[] = [];
  let source: SchemaPAAResponse['source'] = 'none';

  try {
    const paaData = await getPeopleAlsoAsk(keyword);
    if (paaData && paaData.length > 0) {
      paaItems = paaData.map((item) => ({
        question: item.question,
        answer: item.answer || '',
      }));
      source = 'dataforseo';
    }
  } catch {
    // Fallback to Kimi-generated questions
  }

  // 2. If no PAA data, generate questions via Kimi
  if (paaItems.length === 0) {
    const fallbackItems = await generateFallbackQuestions(keyword, industry);
    if (fallbackItems && fallbackItems.length > 0) {
      paaItems = fallbackItems;
      source = 'fallback';
    }
  }

  // 3. Enhance answers with Kimi if they're empty or too short
  if (paaItems.length > 0) {
    const enhanced = await enhanceAnswers(paaItems, keyword, industry, businessName);
    paaItems = enhanced;
  }

  return json({ keyword, paaItems, source } as SchemaPAAResponse, 200);
};

async function generateFallbackQuestions(keyword: string, industry: string): Promise<PAAItem[] | null> {
  const systemPrompt = `You are an SEO expert who knows exactly what questions people search for on Google. Generate 5-8 realistic "People Also Ask" style questions for the given keyword. Return ONLY JSON.`;

  const userPrompt = `Generate 5-8 realistic "People Also Ask" questions that Google would show for the keyword: "${keyword}"
${industry ? `Industry context: ${industry}` : ''}

Return JSON only:
{
  "questions": [
    "Question 1?",
    "Question 2?",
    "Question 3?"
  ]
}`;

  const result = await callKimiJson<{ questions: string[] }>({
    systemPrompt,
    userPrompt,
    maxTokens: 1024,
    temperature: 0.5,
    timeoutMs: 20000,
  });

  if (!result?.questions) return null;
  return result.questions.map((q) => ({ question: q, answer: '' }));
}

async function enhanceAnswers(
  items: PAAItem[],
  keyword: string,
  industry: string,
  businessName: string
): Promise<PAAItem[]> {
  const systemPrompt = `You are a local business SEO copywriter. Write concise, professional FAQ answers (40-80 words each) that help businesses rank in Google's "People Also Ask" boxes. Answers should be factual, helpful, and naturally include relevant keywords. Return ONLY JSON.`;

  const contextParts: string[] = [];
  if (industry) contextParts.push(`Industry: ${industry}`);
  if (businessName) contextParts.push(`Business: ${businessName}`);
  const context = contextParts.length > 0 ? `\nContext: ${contextParts.join(', ')}` : '';

  const questionsList = items.map((item, i) => `${i + 1}. ${item.question}`).join('\n');

  const userPrompt = `Write professional FAQ answers for these questions about "${keyword}".${context}

Questions:
${questionsList}

Return JSON only:
{
  "answers": [
    { "question": "exact question text", "answer": "40-80 word professional answer" },
    ...
  ]
}`;

  const result = await callKimiJson<{ answers: { question: string; answer: string }[] }>({
    systemPrompt,
    userPrompt,
    maxTokens: 2048,
    temperature: 0.6,
    timeoutMs: 30000,
  });

  if (!result?.answers) return items;

  // Merge AI answers with original items (match by question text)
  return items.map((item) => {
    const match = result.answers.find((a) => a.question === item.question);
    return {
      question: item.question,
      answer: match?.answer || item.answer || '',
    };
  });
}
