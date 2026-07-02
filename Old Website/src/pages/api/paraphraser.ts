// src/pages/api/paraphraser.ts
// API endpoint for the Paraphraser / Rewriter tool.
// POST /api/paraphraser/
// Kimi-only: rewrites text in 5 modes. Tier 3 — full output free.

export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimi } from '../../lib/kimi';

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

const modeGuide: Record<string, string> = {
  standard: 'Reword sentences while preserving meaning. Natural, balanced vocabulary changes. Good for general rewriting.',
  fluent: 'Smooth, polished rewrite. Fixes awkward phrasing and improves flow. Best for making text read better.',
  formal: 'Professional, academic tone. Removes contractions and colloquialisms. Uses precise vocabulary. Ideal for business and academic writing.',
  simple: 'Easier to read. Shorter sentences, common words, clear structure. Targets 8th-grade reading level. Great for broad audiences.',
  creative: 'More expressive and varied. Uses vivid language, metaphors, and unexpected word choices. Best for storytelling and marketing copy.',
};

export const POST: APIRoute = async ({ request }) => {
  let body: { text?: string; mode?: string };

  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const text = body.text?.trim() || '';
  if (!text || text.length < 10) {
    return json({ error: 'Please enter at least 10 characters of text' }, 400);
  }
  if (text.length > 2000) {
    return json({ error: 'Text exceeds 2000 character limit' }, 400);
  }

  const mode = body.mode || 'standard';
  if (!modeGuide[mode]) {
    return json({ error: 'Invalid mode. Choose: standard, fluent, formal, simple, creative' }, 400);
  }

  const systemPrompt = `You are a professional paraphrasing editor. You rewrite text to express the same meaning using different words and sentence structures. You preserve all factual claims, data, names, and technical terms exactly. You never add new information. Return ONLY the rewritten text with no preamble, no quotes around the output, and no explanations.`;

  const userPrompt = `Rewrite the following text using the "${mode}" style.

MODE: ${mode} — ${modeGuide[mode]}

REWRITING RULES:
- Preserve every factual claim, number, date, name, and technical term exactly
- Do NOT add new information, examples, or arguments not in the original
- Change sentence structure and vocabulary significantly (at least 60% of words should differ)
- Maintain the same approximate length (±15% word count)
- Keep paragraph breaks in the same positions
- For "formal" mode: no contractions, no slang, precise vocabulary
- For "simple" mode: short sentences, common words, clear structure
- For "creative" mode: vivid language, varied sentence rhythm, expressive word choices
- For "fluent" mode: fix awkward phrasing, improve transitions, smooth reading flow
- For "standard" mode: balanced rewrite, natural synonyms, clear meaning

ORIGINAL TEXT:
${text}

Return ONLY the rewritten text. No quotes around the output. No "Here is the rewrite:" preamble. No markdown formatting. Just the plain rewritten text.`;

  const rewritten = await callKimi({
    systemPrompt,
    userPrompt,
    maxTokens: 4000,
    temperature: 0.7,
    timeoutMs: 30000,
  });

  if (!rewritten) {
    return json({ error: 'AI rewrite failed. Please try again.' }, 500);
  }

  return json({
    original: text,
    rewritten: rewritten.trim(),
    mode,
  }, 200);
};
