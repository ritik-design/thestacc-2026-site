export const prerender = false;

import type { APIRoute } from 'astro';

/**
 * Bigin health check — verifies env vars are loaded and the Zoho OAuth flow works.
 * Returns 200 with non-sensitive diagnostic info. Does NOT expose secrets.
 *
 * GET /api/bigin-health/?key=<HEALTH_CHECK_KEY>
 *
 * Set HEALTH_CHECK_KEY env var to a random string to gate access.
 */
export const GET: APIRoute = async ({ url }) => {
  const env = (import.meta as any).env || {};
  const getEnv = (key: string): string | undefined => env[key] || process.env[key];

  // Simple auth: require ?key=<HEALTH_CHECK_KEY> param
  const expectedKey = getEnv('HEALTH_CHECK_KEY');
  const providedKey = url.searchParams.get('key');
  if (!expectedKey || providedKey !== expectedKey) {
    return new Response(JSON.stringify({ error: 'Forbidden' }), {
      status: 403,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const dc = (getEnv('ZOHO_DC') || 'in').toLowerCase();
  const clientId = getEnv('ZOHO_CLIENT_ID');
  const clientSecret = getEnv('ZOHO_CLIENT_SECRET');
  const refreshTok = getEnv('ZOHO_REFRESH_TOKEN');
  const ownerEmail = getEnv('BIGIN_OWNER_EMAIL');

  const envCheck = {
    ZOHO_DC: dc,
    ZOHO_CLIENT_ID: clientId ? `${clientId.slice(0, 8)}...` : 'MISSING',
    ZOHO_CLIENT_SECRET: clientSecret ? `set (${clientSecret.length} chars)` : 'MISSING',
    ZOHO_REFRESH_TOKEN: refreshTok ? `${refreshTok.slice(0, 8)}...` : 'MISSING',
    BIGIN_OWNER_EMAIL: ownerEmail || 'MISSING',
  };

  if (!clientId || !clientSecret || !refreshTok) {
    return new Response(
      JSON.stringify({
        ok: false,
        stage: 'env',
        message: 'Required Zoho env vars are missing on the server',
        env: envCheck,
      }, null, 2),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Try OAuth refresh
  let tokenResp: { ok: boolean; status: number; data: any };
  try {
    const r = await fetch(`https://accounts.zoho.${dc}/oauth/v2/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: refreshTok,
        client_id: clientId,
        client_secret: clientSecret,
      }).toString(),
    });
    tokenResp = { ok: r.ok, status: r.status, data: await r.json() };
  } catch (err) {
    return new Response(
      JSON.stringify({
        ok: false,
        stage: 'token-fetch',
        message: 'Network error fetching token',
        error: String(err),
        env: envCheck,
      }, null, 2),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  }

  if (!tokenResp.ok || !tokenResp.data?.access_token) {
    return new Response(
      JSON.stringify({
        ok: false,
        stage: 'token-refresh',
        message: 'Zoho token refresh failed',
        zohoStatus: tokenResp.status,
        zohoError: tokenResp.data,
        env: envCheck,
      }, null, 2),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Try Bigin API call
  const accessToken = tokenResp.data.access_token;
  let usersResp: { ok: boolean; status: number; data: any };
  try {
    const r = await fetch(`https://www.zohoapis.${dc}/bigin/v2/users?type=ActiveUsers`, {
      headers: { Authorization: `Zoho-oauthtoken ${accessToken}` },
    });
    usersResp = { ok: r.ok, status: r.status, data: await r.json() };
  } catch (err) {
    return new Response(
      JSON.stringify({
        ok: false,
        stage: 'bigin-api',
        message: 'Network error calling Bigin API',
        error: String(err),
        env: envCheck,
      }, null, 2),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const users = usersResp.data?.users || [];
  const ownerMatch = ownerEmail
    ? users.find((u: any) => u.email?.toLowerCase() === ownerEmail.toLowerCase())
    : null;

  // Test creating a contact via the actual upsertContact function
  let upsertResult: any = null;
  let upsertError: string | null = null;
  if (url.searchParams.get('upsert') === '1') {
    try {
      const { upsertContact } = await import('../../lib/bigin');
      const testEmail = `bigin-health-${Date.now()}@thestacc-test.com`;
      upsertResult = await upsertContact({
        First_Name: 'Health',
        Last_Name: 'Check',
        Email: testEmail,
        Lead_Source: 'Health Check',
        Description: `Test contact from /api/bigin-health at ${new Date().toISOString()}`,
      });
      upsertResult = { ...upsertResult, testEmail };
    } catch (err) {
      upsertError = err instanceof Error ? `${err.name}: ${err.message}\n${err.stack}` : String(err);
    }
  }

  return new Response(
    JSON.stringify({
      ok: true,
      stage: 'all-good',
      message: 'Bigin connection healthy',
      env: envCheck,
      bigin: {
        users_found: users.length,
        owner_match: ownerMatch ? `${ownerMatch.full_name} (${ownerMatch.id})` : 'NOT FOUND',
      },
      upsertTest: url.searchParams.get('upsert') === '1' ? {
        result: upsertResult,
        error: upsertError,
      } : 'pass ?upsert=1 to test contact creation',
    }, null, 2),
    { status: 200, headers: { 'Content-Type': 'application/json' } }
  );
};
