// Minimal Cloudflare Worker for thestacc-2026-site
// Serves static assets uploaded via Workers Static Assets.
// Handles legacy /api/demo/ form submission from the /lp/ page.

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Legacy demo form handler used by the static /lp/ snapshot
    if (url.pathname === '/api/demo/' && request.method === 'POST') {
      try {
        const body = await request.json();
        const firstName = (body.first_name || '').trim();
        const lastName = (body.last_name || '').trim();
        const email = (body.email || '').trim();
        const phone = (body.phone || '').trim();

        const params = new URLSearchParams();
        params.set('name', `${firstName} ${lastName}`.trim());
        params.set('email', email);
        if (phone) params.set('smsReminderNumber', phone);

        return new Response(null, {
          status: 302,
          headers: {
            Location: `/lp/thankyou/?${params.toString()}`,
          },
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: 'Invalid submission' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' },
        });
      }
    }

    // Everything else is served by Workers Static Assets
    return env.ASSETS.fetch(request);
  },
};
