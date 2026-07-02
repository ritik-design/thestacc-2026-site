export const prerender = false;

import type { APIRoute } from 'astro';
import { upsertContact } from '../../lib/bigin';

export const POST: APIRoute = async ({ request }) => {
  let body: { email: string; website?: string };
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const { email, website } = body;

  if (!email?.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ error: 'Valid email is required' }, 400);
  }

  // Await the Bigin sync — fire-and-forget gets killed by Astro's Node adapter
  // after the response is returned, causing leads to be lost.
  try {
    await upsertContact({
      Email: email.trim().toLowerCase(),
      Title: website?.trim() || undefined,
      Lead_Source: 'Website Exit Intent',
      Description: 'Source: Website exit intent modal',
    });
  } catch (err) {
    console.error('[bigin] exit-intent sync failed', err);
  }

  return json({ success: true }, 200);
};

function json(body: object, status: number) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
