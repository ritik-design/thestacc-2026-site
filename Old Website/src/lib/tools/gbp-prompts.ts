// src/lib/tools/gbp-prompts.ts
// Prompt templates + industry data for the GBP Post Generator.

export const GBP_SYSTEM_PROMPT = `You are an expert Google Business Profile post writer for local US businesses.

You write posts that look like a thoughtful business owner wrote them — not an AI, not a corporate copywriter. Every post is well-formatted, scannable on mobile, and ends with a natural call-to-action.

VOICE AND STYLE:
- Active voice. Contractions ("we're", "don't", "it's", "you'll").
- Specific numbers, real names, concrete outcomes. No generic adjectives.
- Lead with a strong opener in the first 75 characters (visible before "Read more" on mobile).
- Reference the city by its short name in conversation (e.g., "Austin" not "Austin, TX") — only use the full state form once, in the FIRST mention, then use the short name.
- Vary your CTA phrasing across the 3 posts. Don't repeat the same closing line. The CTA should feel like a natural ending, not a tacked-on tagline.

FORMATTING RULES (CRITICAL):
- Use blank lines (\\n\\n) between paragraphs. EVERY post must have at least 2 paragraphs separated by a blank line.
- Short post: 1 punchy hook line + 1 short body paragraph + 1 CTA line — 3 visual chunks.
- Medium post: 1 hook line + 2-3 short body paragraphs + 1 CTA line.
- Long post: 1 hook line + 3-4 short body paragraphs + 1 CTA line.
- Keep individual paragraphs short (2-4 sentences max). Wall-of-text kills GBP engagement.
- No headings. No bullet points. No emoji clusters. At most 1 emoji total per post (and only if it fits the tone).

NEVER USE THESE PHRASES (signal AI/template):
"in today's world", "in today's fast-paced", "delve into", "dive into", "tailored to your needs",
"comprehensive solutions", "we pride ourselves", "industry-leading", "state-of-the-art", "cutting-edge",
"innovative", "look no further", "don't hesitate to reach out", "your satisfaction is our",
"leverage our", "seamless", "robust", "we are pleased to", "we are excited to"

NEVER include hashtags. NEVER include phone numbers in the body — the CTA button handles that.

GOOD POST EXAMPLES (study the FORMAT — paragraph breaks, hook, CTA variation):

EXAMPLE 1 (short, story angle, dental):
"""
Marcus chipped his front tooth biting into an apple last Friday afternoon.

He came in Monday morning embarrassed about his coworkers seeing it. We bonded a perfect color match in 45 minutes — by lunch he was back at his desk and nobody noticed.

Book online if something cracked or chipped recently. We keep emergency slots open every weekday.
"""

EXAMPLE 2 (medium, seasonal, plumbing):
"""
It's October in Austin, which means furnace season is 6 weeks away.

Our team ran 47 furnace tune-ups last winter. Every single one of those customers avoided a December emergency call. The math is simple: $89 now or $400+ when it dies on a 28-degree night.

Tune-ups take 45 minutes. We test the heat exchanger, change the filter, and check the gas pressure. We've been doing this for 18 years on the same Austin streets.

Book a tune-up before October 31st and we'll throw in a smart thermostat install for free.
"""

EXAMPLE 3 (long, story, restaurant):
"""
Last Saturday, the Patel family booked our private dining room for their daughter's high school graduation.

They wanted Southern food with Indian touches — something that felt like both halves of who Priya is. Chef Marco built a menu in 4 days: tandoori-spiced fried chicken, masala mac, and a saag-creamed greens that Priya cried over.

We watched a 17-year-old hug her grandmother across the table while her dad ran the slideshow. The grandmother flew in from Mumbai for one weekend.

Stuff like that is why we run private events. It's not catering. It's holding space for the moments your family will tell stories about for 30 years.

Book a private dinner if you've got something coming up. We do 4 of these a month and they fill up 6 weeks out.
"""

OUTPUT FORMAT:
Return ONLY valid JSON matching this exact schema. NO commentary, NO markdown fences:
{
  "posts": [
    { "id": 1, "length": "short", "text": "..." },
    { "id": 2, "length": "medium", "text": "..." },
    { "id": 3, "length": "long", "text": "..." }
  ]
}

Length targets:
- "short": 150-300 characters total (~2-3 paragraphs)
- "medium": 350-650 characters total (~3-4 paragraphs)
- "long": 750-1100 characters total (~4-5 paragraphs)

Each post must include the actual blank-line paragraph breaks (\\n\\n) inside the JSON string.`;

export interface GBPInput {
  biz: string;
  city: string;
  industry: string;
  angle: 'tip' | 'seasonal' | 'story' | 'offer' | 'bts' | 'faq';
  tone: 'professional' | 'friendly' | 'casual';
  cta: string;
  topic?: string;
  offer?: { title?: string; coupon?: string; terms?: string } | null;
}

const ANGLE_GUIDANCE: Record<GBPInput['angle'], string> = {
  tip: 'Share an industry tip or piece of advice that helps customers make a smart choice. Specific, useful, never preachy.',
  seasonal: 'Tie the post to the current season or month. Connect a real customer pain point to that timing.',
  story: 'Tell a real customer-style story: a person, a specific problem, what we did, how it ended. Use a believable name.',
  offer: 'Promote a specific offer with clear terms and a deadline. Lead with the savings, not the corporate language.',
  bts: 'Behind the scenes — show how the business actually operates. Specific details, named team members, what makes the team different.',
  faq: 'Bust a common myth or answer a question customers actually ask. Direct, useful, no hedging.',
};

const TONE_GUIDANCE: Record<GBPInput['tone'], string> = {
  professional: 'Measured, confident, polished. Think established law firm or established medical practice.',
  friendly: 'Warm, approachable, conversational. Think neighborhood salon or beloved restaurant.',
  casual: 'Laid-back, direct, punchy. Think trusted local mechanic or no-nonsense plumber.',
};

const CTA_VERBS: Record<string, string> = {
  'Book': 'book online or call to schedule',
  'Order online': 'order from our website',
  'Buy': 'shop the offer',
  'Learn more': 'see the full details',
  'Sign up': 'sign up to get started',
  'Call now': 'call us today',
  'Get offer': 'claim the offer',
};

const SEASON = (() => {
  const m = new Date().getMonth();
  if (m >= 2 && m <= 4) return 'spring';
  if (m >= 5 && m <= 7) return 'summer';
  if (m >= 8 && m <= 10) return 'fall';
  return 'winter';
})();

const MONTH = new Date().toLocaleString('en-US', { month: 'long' });

export function buildGBPUserPrompt(input: GBPInput): string {
  const angleGuide = ANGLE_GUIDANCE[input.angle] || ANGLE_GUIDANCE.tip;
  const toneGuide = TONE_GUIDANCE[input.tone] || TONE_GUIDANCE.professional;
  const ctaVerb = CTA_VERBS[input.cta] || 'take the next step';
  const cityShort = input.city.split(',')[0].trim();

  let offerBlock = '';
  if (input.angle === 'offer' && input.offer) {
    const parts = [];
    if (input.offer.title) parts.push(`Offer: ${input.offer.title}`);
    if (input.offer.coupon) parts.push(`Coupon code: ${input.offer.coupon}`);
    if (input.offer.terms) parts.push(`Terms: ${input.offer.terms}`);
    offerBlock = parts.length ? `\n\nOffer details:\n${parts.join('\n')}` : '';
  }

  const topicLine = input.topic ? `\n\nSpecific topic to weave in: ${input.topic}` : '';

  return `Write 3 distinct Google Business Profile posts for this local business.

BUSINESS:
- Name: ${input.biz}
- City: ${input.city}  (use the short form "${cityShort}" in conversation; full form OK for first mention if natural)
- Industry: ${input.industry}
- Current month: ${MONTH} (${SEASON} in the US)

POST ANGLE: ${input.angle}
${angleGuide}

TONE: ${input.tone}
${toneGuide}

CALL-TO-ACTION BUTTON: ${input.cta}
The customer will see this exact label as a button below the post. Your CTA line should flow naturally into the action of "${ctaVerb}" — but VARY THE WORDING across all 3 posts. Do not repeat the same closing line.${offerBlock}${topicLine}

REQUIREMENTS:
1. The 3 posts must be COMPLETELY DIFFERENT — different hooks, different angles within the chosen angle, different concrete details (different names, different numbers, different scenes).
2. EVERY post must use blank-line paragraph breaks (\\n\\n in the JSON string). Wall-of-text is unacceptable.
3. Reference "${cityShort}" naturally 1-2 times per post — never more than 2.
4. Include at least one specific number, time, name, or concrete detail per post.
5. Mention "${input.biz}" once per post (not in the hook line — weave it into the body).
6. Each post ends with a CTA line that flows to the "${input.cta}" button. Vary the wording — do not start every CTA with the same word.
7. Length targets: short 150-300 chars, medium 350-650 chars, long 750-1100 chars.
8. Output ONLY the JSON object — no commentary, no markdown fences, no explanation.

Remember: study the EXAMPLES in the system prompt for FORMATTING — paragraph breaks are not optional. Each post must look like 3-5 visually distinct chunks separated by blank lines.`;
}

// Industry-aware best-time-to-post hints
export function getBestTimeToPost(industry: string): string {
  const ind = industry.toLowerCase();
  if (ind.includes('dental') || ind.includes('orthodontic')) return 'Monday-Wednesday 7-9am (when parents check phones before school drop-off)';
  if (ind.includes('plumb') || ind.includes('hvac') || ind.includes('electric')) return 'Tuesday 8-10am (after morning emergency calls slow down)';
  if (ind.includes('legal') || ind.includes('law') || ind.includes('attorney')) return 'Tuesday-Thursday 9-11am (when professionals start their day)';
  if (ind.includes('restaurant') || ind.includes('cafe')) return 'Thursday-Friday 4-6pm (planning weekend dining)';
  if (ind.includes('salon') || ind.includes('spa') || ind.includes('beauty')) return 'Wednesday 11am-1pm (lunch-break booking peak)';
  if (ind.includes('auto') || ind.includes('mechanic')) return 'Tuesday 8-10am (after morning commute issues)';
  if (ind.includes('real estate') || ind.includes('realtor')) return 'Sunday 6-8pm (when buyers plan the week)';
  if (ind.includes('chiropract') || ind.includes('physical therapy')) return 'Monday 6-8am (when back/neck pain peaks)';
  if (ind.includes('roofing') || ind.includes('construction')) return 'Saturday 9-11am (homeowners reviewing projects)';
  if (ind.includes('cleaning')) return 'Sunday 7-9pm (planning the week ahead)';
  if (ind.includes('vet') || ind.includes('pet')) return 'Saturday 8-10am (pet-owner peak)';
  if (ind.includes('fitness') || ind.includes('gym') || ind.includes('yoga')) return 'Sunday 6-8pm (week-ahead planning) or Monday 5-7am';
  return 'Tuesday 8-10am (general best window for local businesses)';
}

// Anti-pattern detection (existing pattern from v1 engine)
const ANTI_PATTERNS = [
  /in today's .* world/i, /it's important to note/i, /whether you're .* or /i,
  /is not just .* — it's/i, /delve into/i, /dive into/i, /we pride ourselves/i,
  /look no further/i, /don't hesitate to/i, /your satisfaction is/i,
  /state-of-the-art/i, /cutting-edge/i, /industry-leading/i,
  /we go above and beyond/i, /quality you can count on/i, /experience the difference/i,
  /comprehensive .* (services|solutions|care)/i, /tailored to your needs/i,
  /leverage our/i, /seamless(ly)?/i, /innovative/i, /robust/i,
  /at \w+, we believe/i, /we are pleased to/i, /we are excited to/i,
];

export function hasAntiPattern(text: string): boolean {
  return ANTI_PATTERNS.some(rx => rx.test(text));
}

export function cleanAntiPatterns(text: string): string {
  let t = text;
  t = t.replace(/In today's .* world,?\s*/gi, '');
  t = t.replace(/It's important to note that\s+/gi, '');
  t = t.replace(/Don't hesitate to reach out/gi, 'Give us a call');
  t = t.replace(/We pride ourselves on/gi, 'We focus on');
  t = t.replace(/comprehensive\s+/gi, '');
  t = t.replace(/\s+solutions/gi, ' services');
  t = t.replace(/tailored to your needs/gi, 'built around what you actually need');
  t = t.replace(/Experience the difference/gi, 'See what we mean');
  return t.trim();
}

// Quality scorer (100-point scale, 10 rules) — used for retry gating
export function scoreGBPPost(text: string, city: string, industry: string, ctaButton: string, length: 'short' | 'medium' | 'long'): number {
  let score = 0;
  const paragraphs = text.split(/\n\s*\n/).map(p => p.trim()).filter(Boolean);
  const lines = text.split('\n').filter(l => l.trim());
  const hook = lines[0] || '';
  const escCity = city.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const cityShort = city.split(',')[0].trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  // Rule 1: Hook quality (15 pts) — first 75 chars must hook
  if (hook.length <= 75) score += 6;
  else if (hook.length <= 100) score += 3;
  if (/\d/.test(hook)) score += 3;
  if (/\?/.test(hook)) score += 2;
  if (!/^(We |Our |The |At |Welcome|Here at)/.test(hook)) score += 4;

  // Rule 2: City placement (10 pts) — short form preferred
  const cityShortMatches = (text.match(new RegExp('\\b' + cityShort + '\\b', 'gi')) || []).length;
  const fullCityMatches = (text.match(new RegExp(escCity, 'gi')) || []).length;
  if (cityShortMatches >= 1 && cityShortMatches <= 2) score += 10;
  else if (cityShortMatches > 0 || fullCityMatches > 0) score += 5;

  // Rule 3: Specificity (12 pts)
  const hasPrice = /\$\d/.test(text);
  const hasTime = /\d+\s*(minute|hour|day|week|month|year|am|pm)/i.test(text);
  const hasQty = /\d+\s*(patient|customer|client|home|job|call|review)/i.test(text);
  const hasPct = /\d+%/.test(text);
  const specifics = [hasPrice, hasTime, hasQty, hasPct].filter(Boolean).length;
  score += Math.min(specifics * 4, 12);

  // Rule 4: CTA presence (10 pts)
  const ctaLower = (ctaButton || '').toLowerCase();
  const hasCta = /(call|book|order|sign up|get offer|learn more|schedule|visit|stop by|reserve)/i.test(text);
  if (hasCta) score += 7;
  if (ctaLower && text.toLowerCase().includes(ctaLower)) score += 3;

  // Rule 5: Human voice (10 pts)
  if (/(we're|don't|can't|won't|it's|that's|you're|we've|isn't|here's|what's|i'm|i've|you'll)/i.test(text)) score += 3;
  if (/\b(we|our|us)\b/i.test(text)) score += 2;
  if (!hasAntiPattern(text)) score += 5;

  // Rule 6: Length fit (8 pts)
  const len = text.length;
  if (length === 'short' && len >= 120 && len <= 350) score += 8;
  else if (length === 'medium' && len >= 300 && len <= 800) score += 8;
  else if (length === 'long' && len >= 600 && len <= 1500) score += 8;
  else if (len >= 120 && len <= 1500) score += 4;

  // Rule 7: Industry language (7 pts)
  const indWords = (industry || '').toLowerCase().split(/[\s/]+/).filter(w => w.length > 3);
  const matches = indWords.filter(w => text.toLowerCase().includes(w)).length;
  score += Math.min(matches * 3, 7);

  // Rule 8: Proof over claims (6 pts)
  if (/\d+\+?\s*(years?|reviews?|patients?|clients?|jobs?|customers?|installs?|repairs?)/i.test(text)) score += 3;
  if (/(saved|fixed|replaced|installed|completed|resolved|recovered|booked|served|delivered)/i.test(text)) score += 3;

  // Rule 9: Urgency (5 pts)
  const monthName = new Date().toLocaleString('en-US', { month: 'long' });
  const urgRe = new RegExp(`(${SEASON}|${monthName}|this week|this month|limited|ends? (soon|friday|sunday)|before|deadline|spots? open|booked? out)`, 'i');
  if (urgRe.test(text)) score += 5;

  // Rule 10: Formatting quality (12 pts) — paragraph breaks are critical for GBP
  const expectedParagraphs = length === 'short' ? 2 : length === 'medium' ? 3 : 3;
  if (paragraphs.length >= expectedParagraphs) score += 8;
  else if (paragraphs.length >= 2) score += 4;
  // No paragraph that's a wall of text (>400 chars)
  if (paragraphs.every(p => p.length <= 400)) score += 4;
  else if (paragraphs.every(p => p.length <= 600)) score += 2;

  return Math.min(score, 100);
}
