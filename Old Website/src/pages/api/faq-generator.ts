export const prerender = false;

import type { APIRoute } from 'astro';
import { callKimiJson } from '../../lib/kimi';

interface FAQPair {
  question: string;
  answer: string;
}

interface FAQGeneratorResponse {
  faqs: FAQPair[];
  schema: Record<string, unknown>;
  topic: string;
  industry: string;
  tone: string;
}

const VALID_TONES = ['professional', 'friendly', 'casual', 'authoritative'] as const;
const VALID_COUNTS = [5, 8, 10];

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  let body: {
    topic?: string;
    industry?: string;
    tone?: string;
    count?: number;
  };

  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const topic = body.topic?.trim();
  if (!topic || topic.length < 3) {
    return json({ error: 'Topic is required (min 3 chars)' }, 400);
  }
  if (topic.length > 200) {
    return json({ error: 'Topic too long (max 200 chars)' }, 400);
  }

  const industry = (body.industry || 'general').trim();
  const tone = (body.tone || 'professional').trim();
  const count = VALID_COUNTS.includes(body.count as any) ? body.count : 8;

  if (!VALID_TONES.includes(tone as any)) {
    return json({ error: 'Invalid tone' }, 400);
  }

  // Generate FAQ pairs via Kimi
  const faqs = await generateFAQs(topic, industry, tone, count);
  if (!faqs || faqs.length === 0) {
    return json({ error: 'Failed to generate FAQs. Please try again.' }, 500);
  }

  // Build FAQPage JSON-LD schema
  const schema = buildFAQSchema(faqs, topic);

  return json({
    faqs,
    schema,
    topic,
    industry,
    tone,
  } as FAQGeneratorResponse, 200);
};

async function generateFAQs(
  topic: string,
  industry: string,
  tone: string,
  count: number
): Promise<FAQPair[] | null> {
  const toneDesc: Record<string, string> = {
    professional: 'Formal, clear, and business-appropriate. Use industry terminology.',
    friendly: 'Warm, approachable, conversational. Use "you" and "we".',
    casual: 'Relaxed, simple language. Short sentences. Like talking to a friend.',
    authoritative: 'Expert, confident, data-backed. Cite specifics where relevant.',
  };

  const systemPrompt = `You are an expert SEO copywriter who specializes in writing FAQ sections that rank in Google's "People Also Ask" boxes and earn featured snippets.

Rules:
- Each question should be a real question that actual customers/prospects ask
- Answers should be 40-80 words — long enough to be helpful, short enough to be scannable
- Use the specified tone consistently
- Include the topic keyword naturally in 2-3 questions
- Order questions by importance (most common first)
- Make answers self-contained (reader shouldn't need to visit another page)
- Avoid fluff, generic statements, and corporate buzzwords

Return ONLY valid JSON. No markdown, no explanation outside JSON.`;

  const userPrompt = `Generate ${count} FAQ question-and-answer pairs for a business or website about: "${topic}"

Context:
- Industry: ${industry}
- Tone: ${toneDesc[tone] || toneDesc.professional}
- Target: Local business website FAQ section

Return JSON only:
{
  "faqs": [
    { "question": "First question?", "answer": "40-80 word answer here." },
    { "question": "Second question?", "answer": "40-80 word answer here." }
  ]
}`;

  const result = await callKimiJson<{ faqs: FAQPair[] }>({
    systemPrompt,
    userPrompt,
    maxTokens: 3000,
    temperature: 0.7,
    timeoutMs: 35000,
  });

  if (!result?.faqs || !Array.isArray(result.faqs)) return null;

  // Validate and clean
  return result.faqs
    .filter((f) => f.question?.trim() && f.answer?.trim())
    .map((f) => ({
      question: f.question.trim(),
      answer: f.answer.trim(),
    }))
    .slice(0, count);
}

function buildFAQSchema(faqs: FAQPair[], topic: string): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map((f) => ({
      '@type': 'Question',
      name: f.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: f.answer,
      },
    })),
    about: {
      '@type': 'Thing',
      name: topic,
    },
  };
}
