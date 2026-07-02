export const prerender = false;

import type { APIRoute } from 'astro';
import { Resend } from 'resend';
import { upsertContact } from '../../lib/bigin';

export const POST: APIRoute = async ({ request }) => {
  const resendKey = process.env.RESEND_API_KEY;
  if (!resendKey) {
    return new Response(
      JSON.stringify({ error: 'Email service not configured' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }

  let body: {
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
    website?: string;
    business?: string;
    business_type?: string;
    plan?: string;
    interest?: string;
    software_interest?: string;
    services_interest?: string;
    goal?: string;
    page_url?: string;
  };

  try {
    body = await request.json();
  } catch {
    return new Response(
      JSON.stringify({ error: 'Invalid request body' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const { first_name, last_name, email, phone, website, business, business_type, plan, interest, software_interest, services_interest, goal } = body;
  const pageUrl = body.page_url || request.headers.get('referer') || 'Unknown';

  if (!first_name?.trim() || !last_name?.trim() || !email?.trim() || !phone?.trim()) {
    return new Response(
      JSON.stringify({ error: 'First name, last name, email, and phone are required' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return new Response(
      JSON.stringify({ error: 'Invalid email address' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const planLabels: Record<string, string> = {
    'local-growth': 'Local Growth — $749/mo',
    'growth-pro': 'Growth Pro — $999/mo',
    'growth-complete': 'Growth Complete — $1,299/mo',
  };
  const planLabel = plan ? (planLabels[plan] ?? plan) : 'Not selected';

  const resend = new Resend(resendKey);

  const isLpLead = /\/lp(\/|$|\?|#)/.test(pageUrl);
  const subject = isLpLead
    ? `Google Ads lead: ${first_name} ${last_name}${business ? ` — ${business}` : ''} (${pageUrl})`
    : `New strategy call request: ${first_name} ${last_name}${business ? ` — ${business}` : ''}`;

  const { error: teamError } = await resend.emails.send({
    from: 'theStacc Demo <team@mail.thestacc.com>',
    to: ['ritik@thestacc.com', 'hello@thestacc.com', 'udit@thestacc.com'],
    replyTo: email,
    subject,
    html: `
      <h2>New Strategy Call Request</h2>
      <p><strong>Name:</strong> ${first_name} ${last_name}</p>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Phone:</strong> ${phone}</p>
      ${website ? `<p><strong>Website:</strong> ${website}</p>` : ''}
      ${business ? `<p><strong>Business:</strong> ${business}</p>` : ''}
      ${business_type ? `<p><strong>Business type:</strong> ${business_type}</p>` : ''}
      <p><strong>Plan of Interest:</strong> ${planLabel}</p>
      ${goal ? `<p><strong>Biggest marketing challenge:</strong></p><p>${goal.replace(/\n/g, '<br>')}</p>` : ''}
      <p><strong>Submitted from:</strong> ${pageUrl}</p>
    `,
  });

  if (teamError) {
    console.error('Resend error (team):', teamError);
    return new Response(
      JSON.stringify({ error: 'Failed to submit request. Please try again.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Confirmation email to the prospect
  const { error: confirmError } = await resend.emails.send({
    from: 'theStacc <team@mail.thestacc.com>',
    to: [email],
    subject: `We got your request, ${first_name} — we'll be in touch within 1 business day`,
    html: `
      <p>Hi ${first_name},</p>
      <p>Thanks for reaching out. We've received your strategy call request and will confirm your slot within 1 business day.</p>
      <p>Before the call, our team will review your website and current local search presence so you're not starting from zero.</p>
      <p>If you have any questions in the meantime, just reply to this email.</p>
      <p>Talk soon,<br>The theStacc Team</p>
    `,
  });

  if (confirmError) {
    // Don't fail the request — team was already notified
    console.error('Resend error (confirmation):', confirmError);
  }

  // Sync to Bigin CRM — await so it doesn't get killed when the response returns
  const descParts: string[] = [];
  if (business_type) descParts.push(`Business type: ${business_type}`);
  if (interest) descParts.push(`Interest: ${interest}`);
  if (software_interest) descParts.push(`Software interest: ${software_interest}`);
  if (services_interest) descParts.push(`Services interest: ${services_interest}`);
  if (planLabel !== 'Not selected') descParts.push(`Plan of interest: ${planLabel}`);
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
      Lead_Source: 'Website Demo Request',
      Description: descParts.join('\n') || undefined,
    });
  } catch (err) {
    console.error('[bigin] demo form sync failed', err);
  }

  return new Response(
    JSON.stringify({ success: true }),
    { status: 200, headers: { 'Content-Type': 'application/json' } }
  );
};
