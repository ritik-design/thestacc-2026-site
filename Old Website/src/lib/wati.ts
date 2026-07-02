// Wati WhatsApp Business API client.
//
// Used by src/pages/api/wati-webhook.ts to reply to inbound WhatsApp
// messages inside the 24h Meta service window. This file was missing
// from the original commit that added the webhook route — without it
// the production build fails with `Could not resolve "../../lib/wati"`.
//
// Required env vars (set in Coolify → Environment):
//   WATI_API_URL   — e.g. https://live-mt-server.wati.io/<tenantId>
//   WATI_API_TOKEN — Bearer token from Wati dashboard → API Docs
//
// If either env var is unset the helpers no-op (and log) so the webhook
// doesn't 500 — it just won't reply. The webhook still 200s, which is
// what Wati expects.

const API_URL = process.env.WATI_API_URL;
const API_TOKEN = process.env.WATI_API_TOKEN;

function authHeaders(): Record<string, string> {
  return {
    Authorization: API_TOKEN!.startsWith('Bearer ') ? API_TOKEN! : `Bearer ${API_TOKEN}`,
    'Content-Type': 'application/json-patch+json',
  };
}

function configured(): boolean {
  if (!API_URL || !API_TOKEN) {
    console.warn('[wati] WATI_API_URL or WATI_API_TOKEN missing — skipping send');
    return false;
  }
  return true;
}

// Strips a leading `+` and any whitespace. Wati's path params want digits only.
function normalizePhone(phone: string): string {
  return phone.replace(/[^\d]/g, '');
}

export async function sendSessionMessage(phone: string, message: string): Promise<void> {
  if (!configured()) return;
  const wa = normalizePhone(phone);
  const url = `${API_URL}/api/v1/sendSessionMessage/${wa}?messageText=${encodeURIComponent(message)}`;
  try {
    const res = await fetch(url, { method: 'POST', headers: authHeaders() });
    if (!res.ok) {
      const body = await res.text().catch(() => '');
      console.error(`[wati] sendSessionMessage ${res.status}: ${body.slice(0, 300)}`);
    }
  } catch (err) {
    console.error('[wati] sendSessionMessage threw', err);
  }
}

export async function sendInteractiveButtons(
  phone: string,
  body: string,
  buttons: string[],
  header?: string,
  footer?: string,
): Promise<void> {
  if (!configured()) return;
  const wa = normalizePhone(phone);
  const url = `${API_URL}/api/v1/sendInteractiveButtonsMessage?whatsappNumber=${wa}`;
  const payload = {
    header: header ? { type: 'Text', text: header } : undefined,
    body,
    footer,
    buttons: buttons.map(text => ({ text })),
  };
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const text = await res.text().catch(() => '');
      console.error(`[wati] sendInteractiveButtons ${res.status}: ${text.slice(0, 300)}`);
    }
  } catch (err) {
    console.error('[wati] sendInteractiveButtons threw', err);
  }
}
