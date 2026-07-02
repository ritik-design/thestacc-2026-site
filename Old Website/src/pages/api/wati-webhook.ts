export const prerender = false;

import type { APIRoute } from 'astro';
import { sendSessionMessage, sendInteractiveButtons } from '../../lib/wati';

// Wati posts incoming-message events here. We respond by sending follow-up
// messages back through the Wati API. Both happen inside the 24h "service
// window" Meta opens when a user replies to us.

const BUTTON_BOOK_DEMO = 'Book a demo';
const BUTTON_SEE_PRICING = 'See pricing';

const MENU_BODY =
  'Great! What would you like to do?';
const MENU_FOOTER = 'theStacc';

const DEMO_REPLY =
  "Awesome — here's the link to grab a demo slot 👇\n\n📅 https://thestacc.com/demo/\n\nPick a time that works for you and we'll see you on the call.";

const PRICING_REPLY =
  "Here's our pricing 👇\n\n💰 https://thestacc.com/pricing/\n\nLet me know if you'd like a quick walkthrough — I can connect you with the team.";

async function sendMenu(phone: string): Promise<void> {
  await sendInteractiveButtons(
    phone,
    MENU_BODY,
    [BUTTON_BOOK_DEMO, BUTTON_SEE_PRICING],
    undefined,
    MENU_FOOTER,
  );
}

// Wati's incoming webhook payload is loosely typed and varies by event. We
// only care about user-sent messages (text or button reply).
type WatiIncoming = {
  eventType?: string;
  type?: string;
  text?: string;
  data?: string;
  waId?: string;
  owner?: boolean;
  buttonReply?: { text?: string };
  listReply?: { title?: string };
};

function extractMessage(payload: WatiIncoming): { text: string; phone: string } | null {
  if (payload.owner === true) return null; // outbound — ignore our own messages
  const phone = payload.waId;
  if (!phone) return null;

  // Buttons can arrive as type=button with `data` set to button text, or as
  // a buttonReply object on newer Wati versions. Try both.
  const text =
    payload.buttonReply?.text ??
    payload.listReply?.title ??
    payload.data ??
    payload.text ??
    '';
  const trimmed = text.trim();
  if (!trimmed) return null;
  return { text: trimmed, phone };
}

export const POST: APIRoute = async ({ request }) => {
  // Optional shared-secret check. Configure the same value in Wati dashboard
  // → Webhooks → "Secret" so impostors can't trigger replies on your behalf.
  const expected = process.env.WATI_WEBHOOK_SECRET;
  if (expected) {
    const auth = request.headers.get('authorization') ?? '';
    const provided = auth.replace(/^Bearer\s+/i, '');
    if (provided !== expected) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      });
    }
  }

  let payload: WatiIncoming;
  try {
    payload = (await request.json()) as WatiIncoming;
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Only react to inbound user messages
  const msg = extractMessage(payload);
  if (!msg) {
    return new Response(JSON.stringify({ received: true, ignored: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const lower = msg.text.toLowerCase();

  if (lower === BUTTON_BOOK_DEMO.toLowerCase() || lower.includes('demo')) {
    await sendSessionMessage(msg.phone, DEMO_REPLY);
  } else if (lower === BUTTON_SEE_PRICING.toLowerCase() || lower.includes('pricing') || lower.includes('price')) {
    await sendSessionMessage(msg.phone, PRICING_REPLY);
  } else if (lower === 'tell me more' || lower === 'menu' || lower === 'help' || lower === 'hi' || lower === 'hello') {
    await sendMenu(msg.phone);
  } else {
    // Unrecognized — show the menu so the user has a clear next step
    await sendMenu(msg.phone);
  }

  return new Response(JSON.stringify({ received: true }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};
