export const prerender = false;

import type { APIRoute } from 'astro';
import { createHmac, timingSafeEqual } from 'node:crypto';
import { upsertContact, splitName, findContact, getContactById } from '../../lib/bigin';

// ─── Constants ────────────────────────────────────────────────────────────────

const DEFAULT_COUNTRY_CODE = '91';
const WATI_TIMEOUT_MS = 15_000;
const DEDUPE_TTL_MS = 24 * 60 * 60 * 1000;
const REDIS_KEY_PREFIX = 'cal_reminder:';
const REDIS_TTL_SECONDS = 8 * 24 * 60 * 60; // 8 days — covers longest meeting window
const MIN_SCHEDULE_BUFFER_MS = 90_000; // skip reminder if < 90s from now

// ─── Deduplication ────────────────────────────────────────────────────────────

const seenBookings = new Map<string, number>();

function rememberBooking(uid: string): boolean {
  const now = Date.now();
  for (const [k, t] of seenBookings) {
    if (now - t > DEDUPE_TTL_MS) seenBookings.delete(k);
  }
  if (seenBookings.has(uid)) return false;
  seenBookings.set(uid, now);
  return true;
}

// ─── Payload helpers ──────────────────────────────────────────────────────────

function esc(str: string): string {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function normalizePhone(raw: string): string {
  const trimmed = raw.trim();
  if (trimmed.startsWith('+')) return trimmed.replace(/\D/g, '');
  const digits = trimmed.replace(/\D/g, '');
  if (!digits) return '';
  if (digits.length === 10) return `${DEFAULT_COUNTRY_CODE}${digits}`;
  return digits;
}

function extractMeetingLink(payload: any): string {
  const p = payload?.payload ?? {};
  const candidates: unknown[] = [
    p.metadata?.videoCallUrl,
    p.videoCallData?.url,
    p.location,
    p.responses?.location?.value?.value,
    p.responses?.location?.value,
  ];
  for (const c of candidates) {
    if (typeof c === 'string' && /^https?:\/\//i.test(c.trim())) return c.trim();
  }
  return '';
}

function extractPhone(payload: any): string {
  const attendee = payload?.payload?.attendees?.[0] ?? {};
  const responses = payload?.payload?.responses ?? {};
  const userFieldsResponses = payload?.payload?.userFieldsResponses ?? {};
  const customInputs = payload?.payload?.customInputs ?? {};
  const candidates: unknown[] = [
    attendee.phoneNumber,
    attendee.phone,
    responses?.phone?.value,
    responses?.phoneNumber?.value,
    userFieldsResponses?.phone?.value,
    userFieldsResponses?.phoneNumber?.value,
    customInputs?.Phone,
    customInputs?.phone,
  ];
  for (const c of candidates) {
    if (typeof c === 'string' && c.trim()) return c.trim();
  }
  return '';
}

function verifySignature(rawBody: string, header: string | null, secret: string): boolean {
  if (!header) return false;
  const expectedHex = createHmac('sha256', secret).update(rawBody).digest('hex');
  const headerBuf = Buffer.from(header);
  for (const variant of [expectedHex, `sha256=${expectedHex}`]) {
    const expBuf = Buffer.from(variant);
    if (expBuf.length === headerBuf.length && timingSafeEqual(expBuf, headerBuf)) return true;
  }
  return false;
}

function extractCustomResponses(payload: any): {
  additionalNotes: string;
  seoHandling: string;
  attendanceConfirm: string;
} {
  const responses = payload?.payload?.responses ?? {};

  function findByQuestionText(...searchTerms: string[]): string {
    for (const [key, val] of Object.entries(responses)) {
      // Normalize: 'how-are-you' → 'how are you' so slugified keys match too
      const normalizedKey = key.toLowerCase().replace(/-/g, ' ');
      for (const term of searchTerms) {
        if (normalizedKey.includes(term.toLowerCase())) {
          const value = (val as any)?.value;
          if (typeof value === 'string') return value.trim();
          if (Array.isArray(value)) return value.join(', ').trim();
          if (value && typeof value === 'object' && value.value) {
            return (value.value as string).trim();
          }
        }
      }
    }
    return '';
  }

  // Additional notes — Cal.com often has this as a top-level field or in responses
  let additionalNotes = payload?.payload?.additionalNotes ?? '';
  if (!additionalNotes) {
    additionalNotes = findByQuestionText('additional notes', 'notes');
  }

  const seoHandling = findByQuestionText(
    'handling seo',
    'currently handling',
    'seo/content',
    'seo content',
  );

  const attendanceConfirm = findByQuestionText(
    'attend this demo',
    'confirm you',
    'scheduled time',
    'attendance',
  );

  return { additionalNotes, seoHandling, attendanceConfirm };
}

function buildBiginDescription(
  eventTitle: string,
  bookingDate: string,
  bookingTime: string,
  meetingLink: string,
  responses: { additionalNotes: string; seoHandling: string; attendanceConfirm: string },
): string {
  const parts: string[] = [];
  if (eventTitle) parts.push(`Event: ${eventTitle}`);
  if (bookingDate && bookingTime) parts.push(`Scheduled: ${bookingDate} at ${bookingTime}`);
  if (meetingLink) parts.push(`Meeting Link: ${meetingLink}`);
  if (responses.additionalNotes) parts.push(`\nAdditional Notes:\n${responses.additionalNotes}`);
  if (responses.seoHandling) parts.push(`\nSEO/Content Handling:\n${responses.seoHandling}`);
  if (responses.attendanceConfirm) parts.push(`\nAttendance Confirmation:\n${responses.attendanceConfirm}`);
  return parts.join('\n');
}

async function syncBookingToBigin(payload: any, bookingUid: string): Promise<void> {
  const attendee = payload?.payload?.attendees?.[0] ?? {};
  const name: string = (attendee.name ?? '').toString().trim();
  const { firstName, lastName } = splitName(name);
  const rawPhone = extractPhone(payload);
  const phone = normalizePhone(rawPhone);

  if (!attendee.email) {
    console.log('cal-webhook: skipping Bigin sync — no attendee email', { bookingUid });
    return;
  }

  const startTime: string | undefined = payload?.payload?.startTime;
  const timezone: string = payload?.payload?.organizer?.timeZone ?? 'Asia/Kolkata';
  const meetingStart = startTime ? new Date(startTime) : null;
  const bookingDate = meetingStart
    ? meetingStart.toLocaleDateString('en-IN', { dateStyle: 'long', timeZone: timezone })
    : '';
  const bookingTime = meetingStart
    ? meetingStart.toLocaleTimeString('en-IN', { timeStyle: 'short', timeZone: timezone })
    : '';
  const eventTitle: string =
    (payload?.payload?.eventType?.title ?? payload?.payload?.eventTitle ?? 'Meeting with theStacc').toString();
  const meetingLink = extractMeetingLink(payload);
  const responses = extractCustomResponses(payload);

  // Build new Cal.com booking block for Campaign_Details
  const campaignParts: string[] = [];
  campaignParts.push(`--- Cal.com Booking — ${bookingUid} ---`);
  campaignParts.push(`Event: ${eventTitle}`);
  campaignParts.push(`Scheduled: ${bookingDate} at ${bookingTime} (${timezone})`);
  if (meetingLink) campaignParts.push(`Meeting Link: ${meetingLink}`);

  const endTime: string | undefined = payload?.payload?.endTime;
  if (endTime) campaignParts.push(`End Time: ${endTime}`);

  const organizer = payload?.payload?.organizer;
  if (organizer) {
    campaignParts.push(`Organizer: ${organizer.name || ''} <${organizer.email || ''}>`);
  }

  campaignParts.push(`Attendee: ${name || ''} <${attendee.email || ''}>`);
  if (phone) campaignParts.push(`Attendee Phone: +${phone}`);

  const status: string = payload?.payload?.status || '';
  if (status) campaignParts.push(`Booking Status: ${status}`);

  const rescheduleUid: string = payload?.payload?.rescheduleUid || payload?.payload?.previousBookingUid || '';
  if (rescheduleUid) campaignParts.push(`Rescheduled From: ${rescheduleUid}`);

  if (responses.additionalNotes) campaignParts.push(`\nAdditional Notes:\n${responses.additionalNotes}`);
  if (responses.seoHandling) campaignParts.push(`\nSEO/Content Handling:\n${responses.seoHandling}`);
  if (responses.attendanceConfirm) campaignParts.push(`\nAttendance Confirmation:\n${responses.attendanceConfirm}`);

  // Include raw responses for any other custom fields
  const rawResponses = payload?.payload?.responses ?? {};
  const extraResponses: string[] = [];
  for (const [key, val] of Object.entries(rawResponses)) {
    if (key === 'name' || key === 'email' || key === 'location' || key === 'guests') continue;
    const value = (val as any)?.value;
    if (value && typeof value === 'string' && value.trim()) {
      const normalizedKey = key.toLowerCase().replace(/-/g, ' ');
      const alreadyCaptured =
        normalizedKey.includes('additional notes') && responses.additionalNotes === value.trim() ||
        (normalizedKey.includes('handling seo') || normalizedKey.includes('currently handling') || normalizedKey.includes('seo content')) && responses.seoHandling === value.trim() ||
        (normalizedKey.includes('attend this demo') || normalizedKey.includes('confirm you') || normalizedKey.includes('scheduled time') || normalizedKey.includes('attendance')) && responses.attendanceConfirm === value.trim();
      if (!alreadyCaptured) {
        extraResponses.push(`${key}: ${value.trim()}`);
      }
    }
  }
  if (extraResponses.length > 0) {
    campaignParts.push('\nOther Responses:');
    campaignParts.push(...extraResponses);
  }

  const newCampaignBlock = campaignParts.join('\n');

  try {
    // ── Deduplication: find by email, merge if exists, create if new ────────
    const email = attendee.email.trim().toLowerCase();
    const existingId = await findContact(email, undefined);

    if (existingId) {
      // Lead already exists — fetch current data and append Cal.com info
      const existing = await getContactById(existingId);
      const existingCal = typeof existing?.Cal_com_details === 'string'
        ? existing.Cal_com_details.trim()
        : '';

      const mergedCal = existingCal
        ? `${existingCal}\n\n${newCampaignBlock}`
        : newCampaignBlock;

      // Only update fields that Cal.com provides (don't overwrite form data)
      const updateResult = await upsertContact({
        Cal_com_details: mergedCal,
        // Update phone only if we got one and existing is empty
        ...(phone && !existing?.Mobile ? { Mobile: phone } : {}),
        // Update meeting link only if empty
        ...(meetingLink && !existing?.Title ? { Title: meetingLink } : {}),
      }, existingId);

      if (updateResult) {
        console.log('cal-webhook: Bigin contact updated (appended)', { bookingUid, email, existingId });
      } else {
        console.warn('cal-webhook: Bigin update returned non-ok', { bookingUid, email, existingId });
      }
      return;
    }

    // ── New lead — create with full data ────────────────────────────────────
    const description = buildBiginDescription(eventTitle, bookingDate, bookingTime, meetingLink, responses);

    const result = await upsertContact({
      First_Name: firstName || name || 'Guest',
      Last_Name: lastName,
      Email: attendee.email,
      Mobile: phone || undefined,
      Title: meetingLink || undefined,
      Lead_Source: 'Cal.com Booking',
      Description: description || undefined,
      Cal_com_details: newCampaignBlock || undefined,
    });

    if (result) {
      console.log('cal-webhook: Bigin contact created', { bookingUid, email, id: result.id, created: result.created });
    } else {
      console.error('cal-webhook: Bigin create failed', { bookingUid, email });
    }
  } catch (err) {
    console.error('[bigin] cal webhook sync failed', { bookingUid, error: String(err) });
  }
}

function extractBookingInfo(payload: any) {
  const attendee = payload?.payload?.attendees?.[0] ?? {};
  const startTime: string | undefined = payload?.payload?.startTime;
  const timezone: string = payload?.payload?.organizer?.timeZone ?? 'Asia/Kolkata';
  const meetingStart = startTime ? new Date(startTime) : null;

  const bookingDate = meetingStart
    ? meetingStart.toLocaleDateString('en-IN', { dateStyle: 'long', timeZone: timezone })
    : '';
  const bookingTime = meetingStart
    ? meetingStart.toLocaleTimeString('en-IN', { timeStyle: 'short', timeZone: timezone })
    : '';

  const eventTitle: string =
    (payload?.payload?.eventType?.title ?? payload?.payload?.eventTitle ?? 'Meeting with theStacc').toString();

  return {
    attendee,
    meetingStart,
    bookingDate,
    bookingTime,
    eventTitle,
    meetingLink: extractMeetingLink(payload),
  };
}

// ─── Upstash Redis (pipeline endpoint — handles JSON values safely) ────────────

async function redisPipeline(commands: string[][]): Promise<any[]> {
  const baseUrl = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;
  if (!baseUrl || !token) return [];
  try {
    const res = await fetch(`${baseUrl}/pipeline`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(commands),
    });
    return (await res.json()) as any[];
  } catch {
    return [];
  }
}

async function redisGet(key: string): Promise<string | null> {
  const results = await redisPipeline([['GET', key]]);
  return (results[0]?.result as string | null) ?? null;
}

async function redisSet(key: string, value: string, exSeconds: number): Promise<void> {
  await redisPipeline([['SET', key, value, 'EX', String(exSeconds)]]);
}

async function redisDel(key: string): Promise<void> {
  await redisPipeline([['DEL', key]]);
}

// ─── Email templates ──────────────────────────────────────────────────────────

type ReminderTiming = '1d' | '1h' | '10m' | 'now';

interface ReminderCtx {
  firstName: string;
  eventTitle: string;
  bookingDate: string;
  bookingTime: string;
  meetingLink: string;
}

const REMINDER_CONFIG: Record<ReminderTiming, { offsetMs: number; subject: string; intro: string }> = {
  '1d': {
    offsetMs: 24 * 60 * 60 * 1000,
    subject: 'Your meeting with theStacc is tomorrow',
    intro: "This is a friendly reminder that your meeting is scheduled for tomorrow. We're looking forward to it.",
  },
  '1h': {
    offsetMs: 60 * 60 * 1000,
    subject: 'Your theStacc meeting starts in 1 hour',
    intro: "Your meeting starts in 1 hour. Get your questions ready — we'll cover everything you need.",
  },
  '10m': {
    offsetMs: 10 * 60 * 1000,
    subject: 'Starting in 10 minutes: your theStacc meeting',
    intro: 'Your meeting starts in 10 minutes. Click the button below to join when you\'re ready.',
  },
  'now': {
    offsetMs: 0,
    subject: 'Your theStacc meeting is starting now',
    intro: 'Your meeting is starting now. Click the button below to join.',
  },
};

function buildEmailHtml(timing: ReminderTiming, ctx: ReminderCtx): string {
  const { intro } = REMINDER_CONFIG[timing];
  const joinBtn = ctx.meetingLink
    ? `<a href="${ctx.meetingLink}" style="display:inline-block;background:#4f39f6;color:#ffffff;text-decoration:none;padding:12px 28px;border-radius:6px;font-size:15px;font-weight:600;margin-top:8px">Join Meeting →</a>`
    : '';

  return `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(REMINDER_CONFIG[timing].subject)}</title></head>
<body style="margin:0;padding:0;background:#f5f5f4;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 20px">
    <tr><td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border-radius:8px;border:1px solid #e7e5e4;overflow:hidden">
        <tr>
          <td style="background:#4f39f6;padding:20px 32px">
            <span style="color:#ffffff;font-size:20px;font-weight:700;letter-spacing:-0.3px">theStacc</span>
          </td>
        </tr>
        <tr>
          <td style="padding:32px 32px 24px">
            <p style="margin:0 0 16px;font-size:16px;color:#292524;font-weight:500">Hi ${esc(ctx.firstName)},</p>
            <p style="margin:0 0 24px;font-size:15px;color:#57534e;line-height:24px">${intro}</p>
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f4;border-radius:6px;border:1px solid #e7e5e4;margin-bottom:24px">
              <tr><td style="padding:20px">
                <p style="margin:0 0 6px;font-size:11px;font-weight:600;color:#a8a29e;text-transform:uppercase;letter-spacing:0.8px">Meeting Details</p>
                <p style="margin:0 0 4px;font-size:15px;color:#292524;font-weight:600">${esc(ctx.eventTitle)}</p>
                <p style="margin:0;font-size:14px;color:#57534e">${esc(ctx.bookingDate)} &middot; ${esc(ctx.bookingTime)}</p>
              </td></tr>
            </table>
            ${joinBtn}
          </td>
        </tr>
        <tr>
          <td style="padding:16px 32px;border-top:1px solid #e7e5e4">
            <p style="margin:0;font-size:12px;color:#a8a29e">theStacc &middot; <a href="https://thestacc.com" style="color:#79716b;text-decoration:none">thestacc.com</a></p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

// ─── Resend scheduling ────────────────────────────────────────────────────────

async function scheduleReminders(
  bookingUid: string,
  attendeeEmail: string,
  ctx: ReminderCtx,
  meetingStart: Date,
): Promise<string[]> {
  const apiKey = process.env.RESEND_API_KEY;
  const fromEmail = process.env.RESEND_FROM_EMAIL ?? 'ritik@thestacc.com';
  const internalEmails = (process.env.INTERNAL_NOTIFY_EMAIL ?? '')
    .split(',')
    .map((e) => e.trim())
    .filter(Boolean);
  if (!apiKey) {
    console.warn('cal-webhook: RESEND_API_KEY not set — skipping email reminders');
    return [];
  }

  const now = Date.now();
  const emailIds: string[] = [];

  for (const timing of ['1d', '1h', '10m', 'now'] as ReminderTiming[]) {
    const { offsetMs, subject } = REMINDER_CONFIG[timing];
    const sendAt = new Date(meetingStart.getTime() - offsetMs);

    if (sendAt.getTime() <= now + MIN_SCHEDULE_BUFFER_MS) {
      console.log(`cal-webhook: skipping ${timing} reminder (send time already passed)`, { bookingUid });
      emailIds.push('');
      continue;
    }

    const body: Record<string, unknown> = {
      from: `theStacc <${fromEmail}>`,
      to: [attendeeEmail],
      subject,
      html: buildEmailHtml(timing, ctx),
      scheduledAt: sendAt.toISOString(),
      tags: [{ name: 'booking_uid', value: bookingUid }],
    };
    if (internalEmails.length > 0) body.bcc = internalEmails;

    try {
      const res = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
        body: JSON.stringify(body),
      });
      const json = (await res.json()) as { id?: string; statusCode?: number; message?: string };

      if (res.ok && json.id) {
        emailIds.push(json.id);
        console.log(`cal-webhook: scheduled ${timing} reminder`, { bookingUid, emailId: json.id, sendAt });
      } else {
        console.error(`cal-webhook: Resend rejected ${timing} reminder`, { bookingUid, status: res.status, json });
        emailIds.push('');
      }
    } catch (err) {
      console.error(`cal-webhook: Resend error for ${timing}`, { bookingUid, error: String(err) });
      emailIds.push('');
    }
  }

  return emailIds;
}

async function cancelReminders(emailIds: string[]): Promise<void> {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) return;

  await Promise.allSettled(
    emailIds.filter(Boolean).map(async (id) => {
      try {
        const res = await fetch(`https://api.resend.com/emails/${id}/cancel`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${apiKey}` },
        });
        if (!res.ok) {
          const text = await res.text();
          // "already sent" is not an error worth surfacing
          if (!text.includes('already sent') && !text.includes('not scheduled')) {
            console.warn('cal-webhook: cancel failed', { id, status: res.status, text });
          }
        } else {
          console.log('cal-webhook: cancelled scheduled email', { id });
        }
      } catch (err) {
        console.error('cal-webhook: cancel error', { id, error: String(err) });
      }
    }),
  );
}

// ─── Route handler ────────────────────────────────────────────────────────────

export const POST: APIRoute = async ({ request }) => {
  const secret = process.env.CAL_WEBHOOK_SECRET;
  if (!secret) {
    console.error('cal-webhook: missing CAL_WEBHOOK_SECRET');
    return new Response('Server not configured', { status: 500 });
  }

  const rawBody = await request.text();
  const signature = request.headers.get('x-cal-signature-256');

  if (!verifySignature(rawBody, signature, secret)) {
    console.error('cal-webhook: invalid signature', { signatureHeader: signature });
    return new Response('Unauthorized', { status: 401 });
  }

  let payload: any;
  try {
    payload = JSON.parse(rawBody);
  } catch {
    return new Response('Invalid JSON', { status: 400 });
  }

  const triggerEvent: string = payload?.triggerEvent ?? '';
  const bookingUid: string =
    payload?.payload?.uid ?? payload?.payload?.bookingId?.toString() ?? '';

  console.log('cal-webhook: received', {
    triggerEvent,
    bookingUid,
    eventType: payload?.payload?.eventType?.title ?? payload?.payload?.eventTitle,
  });

  // ── BOOKING_CANCELLED ──────────────────────────────────────────────────────
  if (triggerEvent === 'BOOKING_CANCELLED') {
    if (bookingUid) {
      const stored = await redisGet(`${REDIS_KEY_PREFIX}${bookingUid}`);
      if (stored) {
        const emailIds: string[] = JSON.parse(stored);
        await cancelReminders(emailIds);
        await redisDel(`${REDIS_KEY_PREFIX}${bookingUid}`);
        console.log('cal-webhook: cancelled all reminders for booking', { bookingUid });
      } else {
        console.log('cal-webhook: no stored reminders found for cancelled booking', { bookingUid });
      }
    }
    return new Response('Cancelled', { status: 200 });
  }

  // ── BOOKING_RESCHEDULED ────────────────────────────────────────────────────
  if (triggerEvent === 'BOOKING_RESCHEDULED') {
    // Cal.com puts the previous booking UID in rescheduleUid
    const prevUid: string =
      payload?.payload?.rescheduleUid ?? payload?.payload?.previousBookingUid ?? '';

    if (prevUid) {
      const stored = await redisGet(`${REDIS_KEY_PREFIX}${prevUid}`);
      if (stored) {
        const oldIds: string[] = JSON.parse(stored);
        await cancelReminders(oldIds);
        await redisDel(`${REDIS_KEY_PREFIX}${prevUid}`);
        console.log('cal-webhook: cancelled old reminders', { prevUid });
      }
    }

    const { attendee, meetingStart, bookingDate, bookingTime, eventTitle, meetingLink } =
      extractBookingInfo(payload);

    if (!attendee.email || !meetingStart) {
      console.error('cal-webhook: missing email or start time on rescheduled booking', { bookingUid });
      return new Response('Missing data', { status: 200 });
    }

    const firstName = ((attendee.name ?? '').toString().trim().split(/\s+/)[0]) || 'there';
    const ctx: ReminderCtx = { firstName, eventTitle, bookingDate, bookingTime, meetingLink };
    const emailIds = await scheduleReminders(bookingUid, attendee.email, ctx, meetingStart);

    const validCount = emailIds.filter(Boolean).length;
    if (validCount > 0 && bookingUid) {
      await redisSet(`${REDIS_KEY_PREFIX}${bookingUid}`, JSON.stringify(emailIds), REDIS_TTL_SECONDS);
    }

    console.log('cal-webhook: rescheduled reminders', { bookingUid, scheduled: validCount });

    // Update Bigin contact with new meeting details
    await syncBookingToBigin(payload, bookingUid);

    return new Response('Rescheduled', { status: 200 });
  }

  // ── BOOKING_CREATED ────────────────────────────────────────────────────────
  if (triggerEvent !== 'BOOKING_CREATED') {
    return new Response('Ignored', { status: 200 });
  }

  if (bookingUid && !rememberBooking(bookingUid)) {
    console.log('cal-webhook: duplicate booking, skipping', { bookingUid });
    return new Response('Duplicate', { status: 200 });
  }

  const { attendee, meetingStart, bookingDate, bookingTime, eventTitle, meetingLink } =
    extractBookingInfo(payload);

  if (!attendee) {
    console.error('cal-webhook: no attendee in payload', { bookingUid });
    return new Response('No attendee', { status: 200 });
  }

  const name: string = (attendee.name ?? '').toString().trim();
  const firstName = name.split(/\s+/)[0] || 'there';
  const timezone = payload?.payload?.organizer?.timeZone ?? 'Asia/Kolkata';

  // ── WATI WhatsApp ─────────────────────────────────────────────────────────
  const watiUrlBase = process.env.WATI_API_URL;
  const watiToken = process.env.WATI_API_TOKEN;

  if (watiUrlBase && watiToken) {
    const rawPhone = extractPhone(payload);
    const phone = normalizePhone(rawPhone);

    if (phone && meetingLink) {
      const watiUrl = `${watiUrlBase.replace(/\/$/, '')}/api/v1/sendTemplateMessage?whatsappNumber=${encodeURIComponent(phone)}`;
      const watiBody = {
        template_name: 'booking_confirmation',
        broadcast_name: `booking_${bookingUid || Date.now()}`,
        parameters: [
          { name: '1', value: firstName },
          { name: '2', value: bookingDate },
          { name: '3', value: bookingTime },
          { name: '4', value: meetingLink },
        ],
      };

      try {
        const watiRes = await fetch(watiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: watiToken.startsWith('Bearer ') ? watiToken : `Bearer ${watiToken}`,
          },
          body: JSON.stringify(watiBody),
          signal: AbortSignal.timeout(WATI_TIMEOUT_MS),
        });
        const watiText = await watiRes.text();
        let watiJson: any = null;
        try { watiJson = JSON.parse(watiText); } catch { /* non-JSON */ }

        if (watiRes.ok && watiJson?.result !== false) {
          console.log('cal-webhook: WATI success', { bookingUid, phone, firstName, meetingLink });
        } else {
          console.error('cal-webhook: WATI rejected', { bookingUid, phone, status: watiRes.status, body: watiText });
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        console.error('cal-webhook: WATI fetch failed', { bookingUid, phone, error: message });
        if (bookingUid) seenBookings.delete(bookingUid);
        return new Response('WATI unreachable', { status: 502 });
      }
    } else {
      console.log('cal-webhook: skipping WATI — no phone or meeting link', {
        bookingUid,
        hasPhone: !!extractPhone(payload),
        hasMeetingLink: !!meetingLink,
      });
    }
  }

  // ── Resend email reminders ────────────────────────────────────────────────
  if (attendee.email && meetingStart) {
    const ctx: ReminderCtx = { firstName, eventTitle, bookingDate, bookingTime, meetingLink };
    const emailIds = await scheduleReminders(bookingUid, attendee.email, ctx, meetingStart);

    const validCount = emailIds.filter(Boolean).length;
    if (validCount > 0 && bookingUid) {
      await redisSet(`${REDIS_KEY_PREFIX}${bookingUid}`, JSON.stringify(emailIds), REDIS_TTL_SECONDS);
      console.log('cal-webhook: email reminders scheduled', { bookingUid, count: validCount });
    }
  } else {
    console.log('cal-webhook: skipping email reminders — no attendee email or start time', { bookingUid });
  }

  // Sync booking to Bigin CRM (includes custom Cal.com question responses)
  await syncBookingToBigin(payload, bookingUid);

  return new Response('OK', { status: 200 });
};
