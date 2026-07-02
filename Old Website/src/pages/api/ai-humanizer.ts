export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimi } from '../../lib/kimi';

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: { text?: string; tone?: string; platform?: string };

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

  const tone = body.tone || 'conversational';
  const platform = body.platform || 'general';

  const toneGuide: Record<string, string> = {
    casual: 'Relaxed, friendly, uses slang and colloquialisms where appropriate. Sounds like a friend explaining something.',
    professional: 'Polished and authoritative but not stiff. Confident expert tone with clear structure.',
    academic: 'Formal, precise, well-structured arguments. Appropriate for research papers and educational content.',
    conversational: 'Natural speech patterns, asks rhetorical questions, uses "you" and "I". Sounds like a podcast or blog post.',
  };

  const platformGuide: Record<string, string> = {
    blog: 'Written for web readers who scan. Use subheadings, short paragraphs, and engaging hooks.',
    linkedin: 'Professional network tone. Blend expertise with personal insight. Use first-person storytelling.',
    email: 'Direct, scannable, single-CTA focused. Friendly but concise. Good subject line energy in the opening.',
    social: 'Short punchy sentences. Emoji-appropriate. Hook in the first line. Designed to stop the scroll.',
    general: 'Versatile tone that works across platforms. Clear, engaging, and natural.',
  };

  const systemPrompt = `You are a professional editor who rewrites AI-generated text to sound natural and human-written. You vary sentence structure, add contractions and natural transitions, remove robotic patterns, and match the requested tone and platform. Return ONLY the rewritten text. No markdown, no explanation, no preamble.`;

  const userPrompt = `Rewrite the following text to sound more natural and human-written.

TONE: ${tone} — ${toneGuide[tone] || toneGuide.conversational}
PLATFORM: ${platform} — ${platformGuide[platform] || platformGuide.general}

REWRITING GUIDELINES:
- Vary sentence length and structure (mix short punchy sentences with longer flowing ones)
- Use contractions (don't, can't, it's, we're) where they sound natural
- Add natural transitions ("Here's the thing", "Honestly", "Look", "The truth is")
- Remove repetitive sentence starters ("Furthermore", "Moreover", "In conclusion" — unless academic)
- Replace passive voice with active voice where possible
- Add occasional rhetorical questions or parenthetical asides
- Break up overly long sentences into 2-3 shorter ones
- Use specific, concrete language instead of vague abstractions
- Match the energy level to the platform (LinkedIn = thoughtful, Social = punchy, Blog = engaging)
- Keep all factual claims and data points exactly as stated
- Do NOT add new facts, statistics, or claims not in the original
- Maintain the original length — aim for roughly the same word count (±15%)

ORIGINAL TEXT:
${text}

Return ONLY the rewritten text. No markdown formatting, no explanations, no "Here is the rewritten text:" preamble.`;

  const humanized = await callKimi({
    systemPrompt,
    userPrompt,
    maxTokens: 4000,
    temperature: 0.8,
    timeoutMs: 30000,
  });

  if (!humanized) {
    return json({ error: 'AI rewrite failed. Please try again.' }, 500);
  }

  return json({
    original: text,
    humanized: humanized.trim(),
    tone,
    platform,
  }, 200);
};
