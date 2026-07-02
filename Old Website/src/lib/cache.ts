// src/lib/cache.ts
// Upstash Redis-backed cache for API responses + ratelimit counters.
// Uses Upstash REST API (no extra package needed).

import { createHash } from 'node:crypto';

const env = (import.meta as any).env || {};
const REDIS_URL = (env.UPSTASH_REDIS_REST_URL || process.env.UPSTASH_REDIS_REST_URL || '').replace(/\/+$/, '');
const REDIS_TOKEN = env.UPSTASH_REDIS_REST_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN || '';

async function redis(args: string[]): Promise<any | null> {
  if (!REDIS_URL || !REDIS_TOKEN) return null;
  try {
    const res = await fetch(REDIS_URL, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${REDIS_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(args),
    });
    if (!res.ok) {
      console.error('[cache] redis non-ok', res.status);
      return null;
    }
    const data = await res.json();
    return data.result;
  } catch (err) {
    console.error('[cache] redis error', err instanceof Error ? err.message : err);
    return null;
  }
}

/** Get a cached JSON value by key. Returns null on miss/error. */
export async function getCached<T = unknown>(key: string): Promise<T | null> {
  const v = await redis(['GET', key]);
  if (!v) return null;
  try {
    return JSON.parse(v) as T;
  } catch {
    return null;
  }
}

/** Set a cached JSON value with TTL in seconds. */
export async function setCached<T = unknown>(key: string, value: T, ttlSec: number): Promise<void> {
  await redis(['SET', key, JSON.stringify(value), 'EX', String(ttlSec)]);
}

/** Hash an input object/string deterministically (used for cache keys). */
export function hashInput(input: object | string): string {
  const json = typeof input === 'string' ? input : JSON.stringify(sortObjectKeys(input));
  return createHash('sha256').update(json).digest('hex').slice(0, 16);
}

function sortObjectKeys(obj: any): any {
  if (obj === null || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(sortObjectKeys);
  return Object.keys(obj).sort().reduce((acc: any, k) => { acc[k] = sortObjectKeys(obj[k]); return acc; }, {});
}

export const cacheConfigured = !!REDIS_URL && !!REDIS_TOKEN;

// ─── Ratelimit (uses same Redis) ───────────────────────────────

export interface RateLimitResult { remaining: number; resetAt: Date; allowed: boolean; }

/**
 * Atomically increment a counter, set TTL on first hit, and check against limit.
 * Fail-open: if Redis is unavailable, all requests are allowed.
 */
export async function checkRateLimit(key: string, limit: number, ttlSec: number): Promise<RateLimitResult> {
  if (!REDIS_URL || !REDIS_TOKEN) {
    return { remaining: limit, resetAt: new Date(Date.now() + ttlSec * 1000), allowed: true };
  }
  const count = await redis(['INCR', key]);
  if (count === 1) await redis(['EXPIRE', key, String(ttlSec)]);
  const ttl = await redis(['TTL', key]);
  const resetAt = new Date(Date.now() + (ttl > 0 ? ttl * 1000 : ttlSec * 1000));
  return {
    remaining: Math.max(0, limit - (count || 0)),
    resetAt,
    allowed: (count || 0) <= limit,
  };
}
