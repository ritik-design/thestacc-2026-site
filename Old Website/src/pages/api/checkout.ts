export const prerender = false;

import type { APIRoute } from 'astro';
import { Resend } from 'resend';
import { upsertContact } from '../../lib/bigin';

interface CheckoutBody {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  website?: string;
  business?: string;
  goal?: string;
  booking_date?: string;
  booking_time?: string;
  selected_modules?: string;
  billing?: string;
  page_url?: string;
}

const MODULE_LABELS: Record<string, string> = {
  blog: 'Blog SEO',
  local: 'Local SEO',
  social: 'Social Media',
};

export const POST: APIRoute = async ({ request }) => {
  const resendKey = process.env.RESEND_API_KEY;
  if (!resendKey) {
    return json({ error: 'Email service not configured' }, 500);
  }

  let body: CheckoutBody;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const { first_name, last_name, email, phone, website, business, goal, booking_date, booking_time, selected_modules, billing } = body;
  const pageUrl = body.page_url || request.headers.get('referer') || 'Unknown';

  if (!first_name?.trim() || !last_name?.trim() || !email?.trim() || !phone?.trim()) {
    return json({ error: 'First name, last name, email, and phone are required.' }, 400);
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ error: 'Invalid email address.' }, 400);
  }

  const modulesText = selected_modules
    ? selected_modules.split(',').map(m => MODULE_LABELS[m.trim()] ?? m).join(', ')
    : 'Not specified';

  const billingLabel = billing === 'monthly' ? 'Monthly' : 'Annual';

  const resend = new Resend(resendKey);

  // ── Team notification ──
  const { error: teamError } = await resend.emails.send({
    from: 'theStacc Bookings <team@mail.thestacc.com>',
    to: ['ritik@thestacc.com', 'hello@thestacc.com', 'udit@thestacc.com'],
    replyTo: email,
    subject: `New booking: ${first_name} ${last_name}${business ? ` — ${business}` : ''}${booking_date ? ` · ${booking_date} ${booking_time}` : ''}`,
    html: `
      <h2 style="margin-bottom:16px;">New Strategy Call Booking</h2>
      <table style="border-collapse:collapse;width:100%;max-width:480px;">
        <tr><td style="padding:6px 0;color:#6b7280;width:140px;">Name</td><td style="padding:6px 0;font-weight:600;">${first_name} ${last_name}</td></tr>
        <tr><td style="padding:6px 0;color:#6b7280;">Email</td><td style="padding:6px 0;"><a href="mailto:${email}">${email}</a></td></tr>
        <tr><td style="padding:6px 0;color:#6b7280;">Phone</td><td style="padding:6px 0;">${phone}</td></tr>
        ${website ? `<tr><td style="padding:6px 0;color:#6b7280;">Website</td><td style="padding:6px 0;"><a href="${website}">${website}</a></td></tr>` : ''}
        ${business ? `<tr><td style="padding:6px 0;color:#6b7280;">Business</td><td style="padding:6px 0;">${business}</td></tr>` : ''}
        ${booking_date ? `<tr><td style="padding:6px 0;color:#6b7280;">Call date</td><td style="padding:6px 0;font-weight:600;color:#4f39f6;">${booking_date} at ${booking_time} ET</td></tr>` : ''}
        <tr><td style="padding:6px 0;color:#6b7280;">Modules</td><td style="padding:6px 0;">${modulesText}</td></tr>
        <tr><td style="padding:6px 0;color:#6b7280;">Billing</td><td style="padding:6px 0;">${billingLabel}</td></tr>
        <tr><td style="padding:6px 0;color:#6b7280;">Submitted from</td><td style="padding:6px 0;"><a href="${pageUrl}">${pageUrl}</a></td></tr>
      </table>
      ${goal ? `<div style="margin-top:16px;"><strong>Marketing challenge:</strong><p style="margin-top:6px;color:#374151;">${goal.replace(/\n/g, '<br>')}</p></div>` : ''}
    `,
  });

  if (teamError) {
    console.error('Resend team error:', teamError);
    return json({ error: 'Failed to submit. Please try again.' }, 500);
  }

  // ── Confirmation to lead ──
  const { error: confirmError } = await resend.emails.send({
    from: 'theStacc <team@mail.thestacc.com>',
    to: [email],
    subject: `Your strategy call is confirmed${booking_date ? ` — ${booking_date} at ${booking_time} ET` : ''}`,
    html: `
      <p>Hi ${first_name},</p>
      <p>Your strategy call is confirmed${booking_date ? ` for <strong>${booking_date} at ${booking_time} Eastern Time</strong>` : ''}.</p>
      <p>Before the call, our team will review your website and current search presence so we can come prepared with specific recommendations — not a generic pitch.</p>
      ${modulesText !== 'Not specified' ? `<p>You selected: <strong>${modulesText}</strong>. We'll focus the conversation on how these modules will work for your business specifically.</p>` : ''}
      <p>If you need to reschedule or have questions, just reply to this email.</p>
      <p>Talk soon,<br>The theStacc Team</p>
    `,
  });

  if (confirmError) {
    console.error('Resend confirm error:', confirmError);
    // Don't fail — team was notified
  }

  // ── Sync to Bigin CRM — await so it doesn't get killed when the response returns ──
  const descParts: string[] = [];
  if (booking_date) descParts.push(`Booking: ${booking_date} at ${booking_time} ET`);
  if (modulesText !== 'Not specified') descParts.push(`Modules: ${modulesText}`);
  descParts.push(`Billing: ${billingLabel}`);
  descParts.push(`Submitted from: ${pageUrl}`);
  if (goal) descParts.push(`\nMarketing challenge:\n${goal}`);

  try {
    await upsertContact({
      First_Name: first_name,
      Last_Name: last_name,
      Email: email,
      Mobile: phone,
      Account_Name: business || undefined,
      Company: business || undefined,
      Title: website || undefined,
      Lead_Source: 'Website Checkout',
      Description: descParts.join('\n'),
    });
  } catch (err) {
    console.error('[bigin] checkout sync failed', err);
  }

  return json({ success: true }, 200);
};

function json(body: object, status: number) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
