// Zoho Bigin CRM — create/update contacts from website form submissions.
// Never throws — Bigin failures are logged and silently dropped so they
// never break the user-facing form submit path.

/* ── Env helpers (Astro SSR uses import.meta.env; process.env is fallback) ── */
const _env = (import.meta as any).env || {};
const _getEnv = (key: string): string | undefined => _env[key] || process.env[key];

export interface BiginContact {
  First_Name?: string;
  Last_Name?: string;
  Email?: string;
  Mobile?: string;
  Phone?: string;
  Account_Name?: string;
  Company?: string;
  Title?: string;        // stores website URL — Bigin Contact has no native Website field
  Lead_Source?: string;
  Description?: string;
  Campaign_Details?: string;
  Cal_com_details?: string;
  Owner?: { id: string };
  [key: string]: unknown;
}

// ── Module-level cache (lives for the life of the Node process) ───────────────

let _token: { value: string; expiresAt: number } | null = null;
let _ownerId: string | null = null;

function dc(): string {
  return (_getEnv('ZOHO_DC') || 'in').toLowerCase();
}

function apiBase(): string {
  return `https://www.zohoapis.${dc()}/bigin/v2`;
}

async function refreshToken(): Promise<string | null> {
  const clientId = _getEnv('ZOHO_CLIENT_ID');
  const clientSecret = _getEnv('ZOHO_CLIENT_SECRET');
  const refreshTok = _getEnv('ZOHO_REFRESH_TOKEN');

  if (!clientId || !clientSecret || !refreshTok) {
    console.warn('[bigin] ZOHO_CLIENT_ID / SECRET / REFRESH_TOKEN not set — skipping CRM sync');
    return null;
  }

  try {
    const res = await fetch(`https://accounts.zoho.${dc()}/oauth/v2/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: refreshTok,
        client_id: clientId,
        client_secret: clientSecret,
      }).toString(),
    });
    const data = await res.json() as { access_token?: string; expires_in?: number };
    if (!data.access_token) {
      console.error('[bigin] token refresh failed', data);
      return null;
    }
    const ttl = data.expires_in ? (data.expires_in - 60) * 1000 : 3_240_000; // 54 min
    _token = { value: data.access_token, expiresAt: Date.now() + ttl };
    return _token.value;
  } catch (err) {
    console.error('[bigin] token refresh threw', err);
    return null;
  }
}

async function getToken(): Promise<string | null> {
  if (_token && Date.now() < _token.expiresAt) return _token.value;
  return refreshToken();
}

async function biginRequest(
  path: string,
  opts: RequestInit = {},
  retry = true,
): Promise<{ ok: boolean; status: number; data: unknown }> {
  const token = await getToken();
  if (!token) return { ok: false, status: 0, data: null };

  const res = await fetch(`${apiBase()}${path}`, {
    ...opts,
    headers: {
      'Content-Type': 'application/json',
      ...(opts.headers as Record<string, string> || {}),
      Authorization: `Zoho-oauthtoken ${token}`,
    },
  });

  if (res.status === 401 && retry) {
    _token = null;
    return biginRequest(path, opts, false);
  }

  let data: unknown = null;
  if (res.status !== 204) {
    try { data = await res.json(); } catch { /* ignore */ }
  }
  return { ok: res.ok || res.status === 204, status: res.status, data };
}

// ── Owner ID ──────────────────────────────────────────────────────────────────

async function getOwnerId(): Promise<string | undefined> {
  if (_ownerId) return _ownerId;

  const ownerEmail = (_getEnv('BIGIN_OWNER_EMAIL') || '').trim().toLowerCase();
  if (!ownerEmail) return undefined;

  const { ok, data } = await biginRequest('/users?type=ActiveUsers');
  if (!ok || !data) return undefined;

  const users = (data as { users?: { id: string; email: string }[] }).users || [];
  const match = users.find(u => u.email.toLowerCase() === ownerEmail);
  if (match) {
    _ownerId = match.id;
    return match.id;
  }
  return undefined;
}

// ── Contact search ────────────────────────────────────────────────────────────

export async function findContact(email?: string, phone?: string): Promise<string | null> {
  const queries: string[] = [];
  if (email) queries.push(`(Email:equals:${email})`);
  if (phone) queries.push(`(Mobile:equals:${phone})`, `(Phone:equals:${phone})`);

  for (const criteria of queries) {
    const { ok, status, data } = await biginRequest(
      `/Contacts/search?criteria=${encodeURIComponent(criteria)}`,
    );
    if (!ok || status === 204) continue;
    const records = (data as { data?: { id: string }[] })?.data;
    if (records?.[0]?.id) return records[0].id;
  }
  return null;
}

/** Fetch a single contact by ID. Returns null on failure. */
export async function getContactById(id: string): Promise<BiginContact | null> {
  const { ok, data } = await biginRequest(`/Contacts/${id}`);
  if (!ok || !data) return null;
  const records = (data as { data?: BiginContact[] })?.data;
  return records?.[0] ?? null;
}

// ── Public API ────────────────────────────────────────────────────────────────

/**
 * Create or update a Bigin Contact. Deduplicates on Email + Mobile.
 * If `existingId` is provided, skips the search and updates that record directly.
 * Returns the Bigin record ID, or null if the sync was skipped/failed.
 */
export async function upsertContact(
  contact: BiginContact,
  existingId?: string,
): Promise<{ id: string; created: boolean } | null> {
  try {
    const email = typeof contact.Email === 'string'
      ? contact.Email.trim().toLowerCase()
      : undefined;
    const phone = typeof contact.Mobile === 'string'
      ? contact.Mobile.trim()
      : undefined;

    const _existingId = existingId || await findContact(email, phone);

    if (_existingId) {
      const { Owner: _owner, ...updateFields } = contact;
      const { ok } = await biginRequest('/Contacts', {
        method: 'PUT',
        body: JSON.stringify({
          data: [{ ...updateFields, id: _existingId }],
          trigger: ['workflow'],
        }),
      });
      if (!ok) console.warn('[bigin] contact update returned non-ok status');
      return { id: _existingId, created: false };
    }

    const ownerId = await getOwnerId();
    const payload: BiginContact = { ...contact };
    if (ownerId) payload.Owner = { id: ownerId };

    const { ok, data } = await biginRequest('/Contacts', {
      method: 'POST',
      body: JSON.stringify({ data: [payload], trigger: ['workflow'] }),
    });
    if (!ok || !data) {
      console.error('[bigin] create failed', data);
      return null;
    }
    const record = (data as { data?: { code: string; details?: { id: string } }[] })?.data?.[0];
    if (record?.code !== 'SUCCESS' || !record.details?.id) {
      console.error('[bigin] create returned non-SUCCESS', record);
      return null;
    }
    return { id: record.details.id, created: true };
  } catch (err) {
    console.error('[bigin] upsertContact threw', err);
    return null;
  }
}

// ── Name splitter (used by forms that only capture full name) ─────────────────

export function splitName(fullName: string): { firstName: string; lastName: string } {
  const parts = fullName.trim().split(/\s+/);
  if (parts.length === 1) return { firstName: parts[0], lastName: '' };
  return { firstName: parts[0], lastName: parts.slice(1).join(' ') };
}
