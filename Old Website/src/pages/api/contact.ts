export const prerender = false;

import type { APIRoute } from 'astro';
import { Resend } from 'resend';
import { upsertContact, splitName } from '../../lib/bigin';

export const POST: APIRoute = async ({ request }) => {
  const resendKey = process.env.RESEND_API_KEY;
  if (!resendKey) {
    return new Response(
      JSON.stringify({ error: 'Email service not configured' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }

  let body: { name: string; email: string; company?: string; module?: string; message: string; phone?: string; page_url?: string };
  try {
    body = await request.json();
  } catch {
    return new Response(
      JSON.stringify({ error: 'Invalid request body' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const { name, email, company, module: areaOfInterest, message } = body;
  const pageUrl = body.page_url || request.headers.get('referer') || 'Unknown';

  if (!name?.trim() || !email?.trim() || !message?.trim()) {
    return new Response(
      JSON.stringify({ error: 'Name, email, and message are required' }),
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

  const resend = new Resend(resendKey);

  const { data, error } = await resend.emails.send({
    from: 'theStacc Contact Form <team@mail.thestacc.com>',
    to: ['ritik@thestacc.com', 'hello@thestacc.com', 'udit@thestacc.com', 'rn@thestacc.com', 'sg@thestacc.com'],
    replyTo: email,
    subject: `Contact form: ${name}${areaOfInterest ? ` — ${areaOfInterest}` : ''}`,
    html: `
      <h2>New contact form submission</h2>
      <p><strong>Name:</strong> ${name}</p>
      <p><strong>Email:</strong> ${email}</p>
      ${company ? `<p><strong>Company:</strong> ${company}</p>` : ''}
      ${areaOfInterest ? `<p><strong>Area of Interest:</strong> ${areaOfInterest}</p>` : ''}
      <p><strong>Message:</strong></p>
      <p>${message.replace(/\n/g, '<br>')}</p>
      <p><strong>Submitted from:</strong> ${pageUrl}</p>
    `,
  });

  if (error) {
    console.error('Resend error:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to send message. Please try again.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Sync to Bigin CRM — await so it doesn't get killed when the response returns
  const { firstName, lastName } = splitName(name);
  const descParts: string[] = [];
  if (areaOfInterest) descParts.push(`Area of interest: ${areaOfInterest}`);
  descParts.push(`Submitted from: ${pageUrl}`);
  if (message) descParts.push(`\nMessage:\n${message}`);

  try {
    await upsertContact({
      First_Name: firstName || name,
      Last_Name: lastName,
      Email: email,
      Mobile: body.phone?.trim() || undefined,
      Account_Name: company || undefined,
      Company: company || undefined,
      Lead_Source: 'Website Contact Form',
      Description: descParts.join('\n') || undefined,
    });
  } catch (err) {
    console.error('[bigin] contact form sync failed', err);
  }

  return new Response(
    JSON.stringify({ success: true }),
    { status: 200, headers: { 'Content-Type': 'application/json' } }
  );
};
