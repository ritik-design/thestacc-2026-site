export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimi } from '../../lib/kimi';

interface PAAItem {
  question: string;
  answer: string;
  intent: 'informational' | 'comparison' | 'how-to' | 'transactional' | 'navigational';
}

interface PAAResponse {
  ok: boolean;
  data?: {
    keyword: string;
    items: PAAItem[];
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

  const prompt = `For the keyword "${keyword}", generate 6 realistic "People Also Ask" questions that appear in Google search results.

Return ONLY a JSON array like this:
[
  {"question":"...","answer":"...","intent":"informational"},
  ...
]

Intents: informational, comparison, how-to, transactional, navigational.
Answers: 2 sentences max, factual and helpful.`;

  const result = await callKimi({
    systemPrompt: 'You are an SEO researcher. Return ONLY valid JSON arrays. No markdown, no explanations.',
    userPrompt: prompt,
    maxTokens: 1500,
    temperature: 0.4,
    timeoutMs: 30000,
  });

  if (!result) {
    return json({ ok: false, error: 'AI generation failed. Please try again.' }, 500);
  }

  // Extract JSON from response
  let items: PAAItem[] = [];
  try {
    const jsonMatch = result.match(/\[[\s\S]*\]/);
    if (jsonMatch) {
      items = JSON.parse(jsonMatch[0]);
    } else {
      // Try parsing the whole response
      items = JSON.parse(result);
    }

    // Validate and filter
    items = items
      .filter((item: any) => item.question && item.answer)
      .map((item: any) => ({
        question: String(item.question).trim(),
        answer: String(item.answer).trim(),
        intent: (['informational', 'comparison', 'how-to', 'transactional', 'navigational'].includes(item.intent)
          ? item.intent
          : 'informational') as PAAItem['intent'],
      }))
      .slice(0, 12);
  } catch {
    // Fallback: parse line by line
    items = parseFallback(result, keyword);
  }

  if (items.length === 0) {
    return json({ ok: false, error: 'Could not generate questions. Try a different keyword.' }, 500);
  }

  return json({
    ok: true,
    data: { keyword, items },
  } as PAAResponse, 200);
};

function parseFallback(text: string, keyword: string): PAAItem[] {
  const items: PAAItem[] = [];
  const lines = text.split('\n');
  let current: Partial<PAAItem> = {};

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    if (trimmed.match(/^\d+[:.\)]/)) {
      if (current.question) {
        items.push({
          question: current.question,
          answer: current.answer || 'No answer provided.',
          intent: current.intent || 'informational',
        });
      }
      current = {
        question: trimmed.replace(/^\d+[:.\)]\s*/, '').trim(),
      };
    } else if (trimmed.toLowerCase().startsWith('answer:') || trimmed.toLowerCase().startsWith('a:')) {
      current.answer = trimmed.replace(/^[^:]*:\s*/, '').trim();
    } else if (trimmed.toLowerCase().startsWith('intent:') || trimmed.toLowerCase().startsWith('type:')) {
      const intentVal = trimmed.replace(/^[^:]*:\s*/, '').trim().toLowerCase();
      current.intent = ['informational', 'comparison', 'how-to', 'transactional', 'navigational'].includes(intentVal)
        ? intentVal as PAAItem['intent']
        : 'informational';
    } else if (current.question && !current.answer) {
      current.answer = trimmed;
    }
  }

  if (current.question) {
    items.push({
      question: current.question,
      answer: current.answer || 'No answer provided.',
      intent: current.intent || 'informational',
    });
  }

  return items;
}
