export const prerender = false;

import type { APIRoute } from 'astro';
import { Resend } from 'resend';
import { upsertContact, splitName } from '../../lib/bigin';

function generateAffiliateCode(name: string): string {
  const slug = name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '')
    .slice(0, 10);
  const random = Math.random().toString(36).slice(2, 8);
  return `${slug}-${random}`;
}

export const POST: APIRoute = async ({ request }) => {
  const resendKey = process.env.RESEND_API_KEY;
  if (!resendKey) {
    return new Response(
      JSON.stringify({ error: 'Email service not configured' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }

  let body: {
    name: string;
    email: string;
    website?: string;
    audience?: string;
    channel: string;
    message?: string;
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

  const { name, email, website, audience, channel, message } = body;
  const pageUrl = body.page_url || request.headers.get('referer') || 'Unknown';

  if (!name?.trim() || !email?.trim() || !channel?.trim()) {
    return new Response(
      JSON.stringify({ error: 'Name, email, and promotion channel are required' }),
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

  const affiliateCode = generateAffiliateCode(name);
  const affiliateLink = `https://thestacc.com/?ref=${affiliateCode}`;

  const resend = new Resend(resendKey);

  // Notify the team
  const { error: teamError } = await resend.emails.send({
    from: 'theStacc Affiliates <team@mail.thestacc.com>',
    to: ['sidgangal@gmail.com'],
    replyTo: email,
    subject: `New affiliate signup: ${name}`,
    html: `
      <h2>New Affiliate Application</h2>
      <p><strong>Name:</strong> ${name}</p>
      <p><strong>Email:</strong> ${email}</p>
      ${website ? `<p><strong>Website:</strong> ${website}</p>` : ''}
      ${audience ? `<p><strong>Audience Size:</strong> ${audience}</p>` : ''}
      <p><strong>Promotion Channel:</strong> ${channel}</p>
      ${message ? `<p><strong>About their audience:</strong></p><p>${message.replace(/\n/g, '<br>')}</p>` : ''}
      <hr>
      <p><strong>Generated Affiliate Code:</strong> ${affiliateCode}</p>
      <p><strong>Affiliate Link:</strong> ${affiliateLink}</p>
      <p><strong>Submitted from:</strong> ${pageUrl}</p>
    `,
  });

  if (teamError) {
    console.error('Resend error (team):', teamError);
    return new Response(
      JSON.stringify({ error: 'Failed to process application. Please try again.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Send welcome email to the affiliate
  const { error: affiliateError } = await resend.emails.send({
    from: 'theStacc Affiliates <team@mail.thestacc.com>',
    to: [email],
    subject: `Welcome to the theStacc Affiliate Program`,
    html: `
      <h2>Welcome to the theStacc Affiliate Program!</h2>
      <p>Hi ${name},</p>
      <p>Thanks for joining our affiliate program. Here are your details:</p>
      <div style="background:#f5f3ff;border:1px solid #e7e5e4;border-radius:12px;padding:20px;margin:20px 0;">
        <p style="margin:0 0 8px;font-size:14px;color:#79716b;">Your Affiliate Link</p>
        <p style="margin:0;font-size:18px;font-weight:600;color:#4f39f6;">${affiliateLink}</p>
        <p style="margin:12px 0 0;font-size:14px;color:#79716b;">Your Affiliate Code</p>
        <p style="margin:0;font-size:18px;font-weight:600;color:#292524;">${affiliateCode}</p>
      </div>
      <h3>Commission Structure</h3>
      <ul>
        <li><strong>25% recurring commission</strong> on direct sales (customer signs up through your link)</li>
        <li><strong>15% recurring commission</strong> on sales-assisted deals (you generate the lead, our team closes)</li>
        <li><strong>90-day cookie window</strong></li>
        <li><strong>Lifetime recurring</strong> — earn for as long as your referral stays a customer</li>
      </ul>
      <h3>How It Works</h3>
      <ol>
        <li>Share your unique affiliate link with your audience</li>
        <li>When someone signs up through your link, they're tagged as your referral</li>
        <li>You earn commission on every payment they make</li>
        <li>Payouts are monthly via PayPal or bank transfer (minimum $50)</li>
      </ol>
      <p>We'll be in touch soon with marketing assets, tips, and your affiliate dashboard access.</p>
      <p>Questions? Reply to this email anytime.</p>
      <p>Best,<br>The theStacc Team</p>
    `,
  });

  if (affiliateError) {
    console.error('Resend error (affiliate):', affiliateError);
    // Don't fail the request — team was already notified
  }

  // Sync to Bigin CRM — await so it doesn't get killed when the response returns
  const { firstName, lastName } = splitName(name);
  const descParts: string[] = [];
  descParts.push(`Affiliate code: ${affiliateCode}`);
  descParts.push(`Affiliate link: ${affiliateLink}`);
  descParts.push(`Promotion channel: ${channel}`);
  if (audience) descParts.push(`Audience size: ${audience}`);
  descParts.push(`Submitted from: ${pageUrl}`);
  if (message) descParts.push(`\nAbout their audience:\n${message}`);

  try {
    await upsertContact({
      First_Name: firstName || name,
      Last_Name: lastName,
      Email: email,
      Title: website || undefined,
      Lead_Source: 'Website Affiliate Signup',
      Description: descParts.join('\n'),
    });
  } catch (err) {
    console.error('[bigin] affiliate sync failed', err);
  }

  return new Response(
    JSON.stringify({
      success: true,
      affiliateCode,
      affiliateLink,
    }),
    { status: 200, headers: { 'Content-Type': 'application/json' } }
  );
};
