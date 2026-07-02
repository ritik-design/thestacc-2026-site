// src/lib/kimi.ts
// Reusable Kimi (Anthropic-compatible) LLM client for all theStacc tools.
// Reads ANTHROPIC_BASE_URL, ANTHROPIC_API_KEY, ANTHROPIC_MODEL from env.

const API_KEY = process.env.ANTHROPIC_API_KEY;
const BASE_URL = (process.env.ANTHROPIC_BASE_URL || 'https://api.kimi.com/coding/').replace(/\/+$/, '');
const MODEL = process.env.ANTHROPIC_MODEL || 'kimi-for-coding';

export interface KimiOptions {
  systemPrompt: string;
  userPrompt: string;
  maxTokens?: number;
  temperature?: number;
  timeoutMs?: number;
}

async function fetchWithTimeout(url: string, timeoutMs: number, opts?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...opts, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Call Kimi/Anthropic. Returns the text content or null on any failure.
 * Designed for graceful degradation — caller handles fallback.
 */
export async function callKimi(opts: KimiOptions): Promise<string | null> {
  if (!API_KEY) {
    console.warn('[kimi] No ANTHROPIC_API_KEY configured — skipping LLM call');
    return null;
  }

  try {
    const res = await fetchWithTimeout(`${BASE_URL}/v1/messages`, opts.timeoutMs ?? 45000, {
      method: 'POST',
      headers: {
        'x-api-key': API_KEY,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: opts.maxTokens ?? 4096,
        temperature: opts.temperature ?? 0.7,
        system: opts.systemPrompt,
        messages: [{ role: 'user', content: opts.userPrompt }],
      }),
    });

    if (!res.ok) {
      const errText = await res.text();
      console.error('[kimi] API error:', res.status, errText.substring(0, 500));
      return null;
    }

    const data = await res.json();
    const content = data.content?.[0]?.text;
    if (!content) {
      console.error('[kimi] Empty content in response:', JSON.stringify(data).substring(0, 500));
      return null;
    }
    return content;
  } catch (err) {
    console.error('[kimi] Call failed:', err instanceof Error ? err.message : err);
    return null;
  }
}

/**
 * Call Kimi expecting JSON output. Strips ```json fences.
 * Returns parsed object or null on any failure.
 */
export async function callKimiJson<T = unknown>(opts: KimiOptions): Promise<T | null> {
  const text = await callKimi(opts);
  if (!text) return null;

  try {
    const cleaned = text
      .replace(/```json\s*/gi, '')
      .replace(/```\s*$/g, '')
      .trim();
    return JSON.parse(cleaned) as T;
  } catch (err) {
    console.error('[kimi] JSON parse failed:', err instanceof Error ? err.message : err, 'raw:', text.substring(0, 300));
    return null;
  }
}

/** Runtime check — returns true if API_KEY is configured. Using a function prevents build-time dead-code elimination. */
export function isKimiConfigured(): boolean {
  return !!API_KEY;
}
