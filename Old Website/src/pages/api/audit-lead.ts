export const prerender = false;

import type { APIRoute } from 'astro';
import { Resend } from 'resend';
import { upsertContact } from '../../lib/bigin';

/* ═══════════════════════════════════════════════════════════════
   Audit Lead Capture API
   Captures name/email/phone from audit users, sends notification
   + confirmation emails, syncs to Bigin CRM.
   ═══════════════════════════════════════════════════════════════ */

function json(body: object, status: number) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request }) => {
  const env = (import.meta as any).env || {};
  const resendKey = env.RESEND_API_KEY || process.env.RESEND_API_KEY || '';
  const fromEmail = env.RESEND_FROM_EMAIL || process.env.RESEND_FROM_EMAIL || 'team@mail.thestacc.com';
  if (!resendKey) {
    return json({ error: 'Email service not configured' }, 500);
  }

  let body: {
    domain?: string;
    first_name?: string;
    last_name?: string;
    email?: string;
    phone?: string;
    audit_score?: number;
    audit_grade?: string;
    top_issues?: string[];
    page_url?: string;
  };

  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request body' }, 400);
  }

  const {
    domain,
    first_name,
    last_name,
    email,
    phone,
    audit_score,
    audit_grade,
    top_issues,
  } = body;
  const pageUrl = body.page_url || request.headers.get('referer') || 'Unknown';

  if (!first_name?.trim() || !last_name?.trim() || !email?.trim() || !phone?.trim()) {
    return json({ error: 'First name, last name, email, and phone are required' }, 400);
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return json({ error: 'Invalid email address' }, 400);
  }

  const resend = new Resend(resendKey);

  // Build issues list for email
  const issuesList = top_issues?.length
    ? top_issues.map((issue, i) => `<li>${i + 1}. ${issue}</li>`).join('')
    : '<li>No specific issues flagged</li>';

  // ── Team notification (best effort — don't block user if email fails) ──
  const teamResult = await resend.emails.send({
    from: `theStacc Audit <${fromEmail}>`,
    to: ['ritik@thestacc.com', 'hello@thestacc.com'],
    replyTo: email,
    subject: `New SEO Audit Lead: ${first_name} ${last_name} — ${domain || 'No domain'}`,
    html: `
      <h2>New SEO Audit Lead</h2>
      <p><strong>Name:</strong> ${first_name} ${last_name}</p>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Phone:</strong> ${phone}</p>
      <p><strong>Domain:</strong> ${domain || 'Not provided'}</p>
      <p><strong>Audit Score:</strong> ${audit_score ?? 'N/A'}/100 (Grade ${audit_grade ?? 'N/A'})</p>
      <p><strong>Top Issues:</strong></p>
      <ul>${issuesList}</ul>
      <p><strong>Audit URL:</strong> ${domain ? `https://thestacc.com/audit/${domain}/` : 'N/A'}</p>
      <p><strong>Submitted from:</strong> ${pageUrl}</p>
    `,
  });

  if (teamResult.error) {
    console.error('[audit-lead] Team email failed:', teamResult.error);
  }

  // ── Confirmation email to lead (best effort) ──
  const confirmResult = await resend.emails.send({
    from: `theStacc <${fromEmail}>`,
    to: [email],
    subject: `${first_name}, here's your full SEO audit report`,
    html: `
      <p>Hi ${first_name},</p>
      <p>Thanks for running a free SEO audit with theStacc. Your full report is now unlocked and ready.</p>
      <p><strong>Your website scored ${audit_score ?? 'N/A'}/100 (Grade ${audit_grade ?? 'N/A'})</strong></p>
      <p>We've identified the top issues holding your site back, along with specific fixes you can implement right away.</p>
      <p><a href="${domain ? `https://thestacc.com/audit/${domain}/` : 'https://thestacc.com/tools/seo-audit/'}" style="display:inline-block;padding:12px 24px;background:#4f39f6;color:white;text-decoration:none;border-radius:8px;font-weight:600;">View Full Report</a></p>
      <p>Want us to handle the fixes automatically? TheStacc publishes 30+ SEO-optimized articles, manages your Google Business Profile, and handles social media — all on autopilot.</p>
      <p><a href="https://thestacc.com/demo/" style="color:#4f39f6;">Book a free 30-minute strategy call →</a></p>
      <p>Talk soon,<br>The theStacc Team</p>
    `,
  });

  if (confirmResult.error) {
    console.error('[audit-lead] Confirmation email failed:', confirmResult.error);
  }

  // ── Bigin CRM sync — await so it doesn't get killed when the response returns ──
  const descParts: string[] = [];
  if (domain) descParts.push(`Audit Domain: ${domain}`);
  if (audit_score !== undefined) descParts.push(`Audit Score: ${audit_score}/100`);
  if (audit_grade) descParts.push(`Audit Grade: ${audit_grade}`);
  if (top_issues?.length) descParts.push(`Top Issues:\n${top_issues.join('\n')}`);
  if (domain) descParts.push(`Audit Report: https://thestacc.com/audit/${domain}/`);
  descParts.push(`Submitted from: ${pageUrl}`);

  try {
    await upsertContact({
      First_Name: first_name.trim(),
      Last_Name: last_name.trim(),
      Email: email.trim(),
      Mobile: phone.trim() || undefined,
      Account_Name: domain || undefined,
      Company: domain || undefined,
      Lead_Source: 'SEO Audit Tool',
      Description: descParts.join('\n') || undefined,
    });
  } catch (err) {
    console.error('[bigin] audit lead sync failed', err);
  }

  return json({ success: true }, 200);
};
