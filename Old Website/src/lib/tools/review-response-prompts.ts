// src/lib/tools/review-response-prompts.ts
// Prompt templates + safety rules + scorer for the Review Response Generator.
// Tier 3 tool — full output free, no email gate.

export interface ReviewInput {
  reviewText: string;
  rating: 1 | 2 | 3 | 4 | 5;
  biz: string;
  industry: string;
  city: string;
  reviewerName?: string;
  tone: 'professional' | 'friendly' | 'empathetic' | 'brief';
}

// ─── Industry safety rules ─────────────────────────────────────
// Real legal exposure if these are violated. The model MUST follow them.

const HIPAA_INDUSTRIES = ['dental', 'orthodontic', 'medical', 'chiropract', 'physical therapy', 'mental health', 'therapy', 'counsel', 'veterinary', 'optometr', 'dermat'];
const LEGAL_PRIVILEGE_INDUSTRIES = ['legal', 'law', 'attorney', 'lawyer'];
const FINANCIAL_PRIVILEGE_INDUSTRIES = ['accounting', 'tax', 'financial', 'cpa', 'wealth', 'insurance'];

export function getIndustrySafetyRules(industry: string): string[] {
  const ind = (industry || '').toLowerCase();
  const rules: string[] = [];

  if (HIPAA_INDUSTRIES.some(k => ind.includes(k))) {
    rules.push('CRITICAL — HIPAA: NEVER reference any specific treatment, procedure, diagnosis, condition, medication, or appointment detail in your response. Even if the reviewer mentioned it. Speak only in general terms about your practice and patient experience. Saying "thanks for trusting us with your root canal" is a HIPAA violation.');
    rules.push('Do not confirm whether someone is a patient. Use phrases like "anyone who has visited our practice" instead of "you" when referencing care.');
  }

  if (LEGAL_PRIVILEGE_INDUSTRIES.some(k => ind.includes(k))) {
    rules.push('CRITICAL — Attorney-client privilege: NEVER confirm someone is a client. NEVER reference case details, outcomes, hearings, settlements, or strategy. Speak only in general terms about your firm\'s approach and values.');
    rules.push('Use language like "our firm" and "anyone who works with us" — not "your case" or "we represented you".');
  }

  if (FINANCIAL_PRIVILEGE_INDUSTRIES.some(k => ind.includes(k))) {
    rules.push('CRITICAL — Financial confidentiality: Do not reference specific account details, returns, advice given, or financial outcomes. Speak in general terms about your firm\'s approach.');
  }

  if (ind.includes('real estate') || ind.includes('realtor')) {
    rules.push('Do not reference specific property addresses, sale prices, or transaction details — even if the reviewer mentioned them.');
  }

  return rules;
}

// ─── Tone profiles ─────────────────────────────────────────────

const TONE_GUIDE: Record<ReviewInput['tone'], string> = {
  professional: 'Measured, polished, restrained. Think a senior partner at an established firm. Full sentences. No exclamation marks except in the opening line for 5-star. Words like "appreciate," "value," "thoughtful."',
  friendly: 'Warm, conversational, human. Think a trusted neighborhood business owner. Contractions ("we\'re," "that\'s"). One exclamation point per response is OK. Words like "thrilled," "glad," "love hearing this."',
  empathetic: 'Patient, validating, accountability-forward. Think a hospitality manager who genuinely listens. Acknowledges feelings before action. Words like "I hear you," "that\'s frustrating," "we should have done better."',
  brief: 'Direct, concise, no padding. Think a busy owner who replies fast. Short sentences. Active voice. Often under 60 words even on the longest variation. No fluff.',
};

// ─── Length targets per variation ──────────────────────────────
// concise = quick reply (40-80 words), balanced = standard (90-150), detailed = full acknowledgment (160-220).
// For 1-2 star reviews, the model gets nudged toward longer detailed responses.

const LENGTH_TARGETS = {
  concise: { min: 40, max: 90, words: '40-80 words' },
  balanced: { min: 80, max: 170, words: '90-150 words' },
  detailed: { min: 150, max: 240, words: '160-220 words' },
} as const;

// ─── System prompt ─────────────────────────────────────────────
// Includes 6 fully-formatted GOOD response examples (positive + negative for 3 industries).

export const REVIEW_RESPONSE_SYSTEM_PROMPT = `You are an expert local-business owner replying to Google reviews. You write responses that read as if a thoughtful, accountable owner wrote them — never AI, never corporate, never defensive.

CORE PRINCIPLES:
- Acknowledge what the reviewer specifically said. Reference one concrete detail (a name, an experience, a praise word, a complaint specifics) — proof you actually read it.
- Lead with empathy on negatives. Lead with genuine appreciation on positives.
- Active voice. Contractions ("we're", "that's", "you're", "we've", "don't"). No corporate-speak.
- Mention the business name once, the city once. Naturally placed, not stuffed.
- For 1-2 star reviews: the response is for the next 100 readers, not the angry reviewer. Stay calm, don't argue, offer offline resolution.
- For 5 star reviews: be warmly grateful without sycophancy. Vary the opening across the 3 variations — never identical.
- Keep an 8th-grade reading level. Short sentences. Short paragraphs.

PARAGRAPH STRUCTURE (CRITICAL):
- Use blank lines (\\n\\n) between paragraphs.
- Concise variation: 1-2 paragraphs.
- Balanced variation: 2-3 paragraphs.
- Detailed variation: 3-4 paragraphs.
- No wall of text. No bullet points. No headings. No emojis (one optional in detailed only, at most).

NEVER USE THESE PHRASES (signal AI/corporate template):
"in today's world", "delve into", "tailored to your needs", "we pride ourselves",
"industry-leading", "state-of-the-art", "your satisfaction is our top priority",
"we strive to", "rest assured", "we appreciate your business", "feel free to reach out",
"we are pleased to", "we are excited to", "thank you for choosing", "we value your feedback",
"on behalf of the entire team", "we are committed to", "we sincerely apologize for any inconvenience",
"please don't hesitate", "kindly", "as per your concern", "duly noted"

NEGATIVE REVIEW RULES (1-3 stars):
1. Do NOT start with "We're sorry" alone. Lead with acknowledgment of their specific experience.
2. Do NOT admit fault or guarantee specific outcomes — that's legal exposure. Use "we should have done better" not "we did wrong."
3. Do NOT argue, contradict, or "but actually" the reviewer publicly. Move the dispute offline.
4. Always offer a path off-platform: a direct number, a manager's email, or "reach out to us so we can make this right."
5. Don't promise refunds, free service, or compensation in public.
6. Sign with a real-feeling identity ("Lisa, GM" or "the team at [Biz]") — but do NOT invent a specific person's name. Use "the team at [Biz]" by default.

POSITIVE REVIEW RULES (4-5 stars):
1. Vary the opening across all 3 variations. Never repeat "Thank you so much, [Name]!" three times.
2. Reference one specific detail from their review (a praise word, an experience, a service mentioned).
3. Reinforce the city/service area subtly: "Glad we could help with your [thing] in [city]" — once per response, not three times.
4. Encourage continued engagement naturally: "see you next time," "tell a friend," "let us know how the [thing] holds up."
5. Skip generic phrases like "we appreciate your business."

GOOD RESPONSE EXAMPLES (study the FORMAT — paragraph breaks, specifics, voice):

EXAMPLE 1 (5-star, dental, friendly tone):
"""
Sarah, you just made our whole team's day.

Hearing that the cleaning felt comfortable means a lot — that's exactly what Dr. Chen and the hygienists work toward every single visit. We're glad it showed.

Glad to be part of your dental routine in Austin. See you in 6 months.
"""

EXAMPLE 2 (1-star, plumbing, empathetic tone):
"""
Marcus, this isn't the experience anyone should have when their water heater goes out.

You waited 6 hours for a callback that never came, and that's on us — not on the dispatcher, not on the technician, on the system we run. We should have done better, full stop.

I'd like to make this right directly. Please call our office at the number on our profile and ask for the GM. I'll personally pull your job ticket and we'll find a way forward.

— the team at North Austin Plumbing
"""

EXAMPLE 3 (3-star, restaurant, professional tone):
"""
Thank you for the honest feedback, Jennifer.

The wait time you described isn't what we aim for, especially on a Saturday evening. Our host team has worked through revised seating procedures over the past few weeks specifically because of this kind of feedback. The kitchen pacing is something we're still tuning.

If you give us another chance, please mention this review when you book — we'd like to seat you personally and prove the experience can be much better.

The team at Marigold Kitchen, downtown Charleston
"""

EXAMPLE 4 (5-star, legal, professional tone — note attorney privilege):
"""
Thank you for taking the time to share this, David.

We work hard to make sure anyone who walks into our firm feels heard and respected — knowing that came through is meaningful. The whole team values that kind of feedback.

If you ever need our help again, or know someone in the Denver area who might, we're here.
"""

EXAMPLE 5 (1-star, salon, friendly tone):
"""
Priya, I'm so sorry the color didn't come out the way you hoped.

I've been cutting hair in Phoenix for 14 years and I know how much it hurts to leave a chair feeling worse than when you sat down. The fact that we didn't catch this in the chair is something I need to look at with my team.

Please call the salon and ask for Lisa — that's me. I'd like to bring you back in personally for a correction, on the house, with whichever stylist you'd prefer.
"""

EXAMPLE 6 (5-star, plumbing, brief tone):
"""
Carlos, thanks. Glad we got the leak handled fast.

Call us anytime your house decides to surprise you again.
"""

OUTPUT FORMAT:
Return ONLY valid JSON matching this exact schema. NO markdown fences, NO commentary:
{
  "responses": [
    { "id": 1, "variant": "concise", "text": "..." },
    { "id": 2, "variant": "balanced", "text": "..." },
    { "id": 3, "variant": "detailed", "text": "..." }
  ],
  "flags": [
    { "type": "hipaa" | "legal" | "tone" | "unverified_claim", "message": "..." }
  ]
}

The "flags" array warns the user about anything in the original review that requires care (e.g., reviewer mentioned a specific medical procedure → HIPAA flag; reviewer mentioned a specific case → privilege flag; reviewer claimed something extreme that needs verification before responding). Empty array if nothing to flag.

Length targets:
- "concise": ${LENGTH_TARGETS.concise.words} (1-2 paragraphs)
- "balanced": ${LENGTH_TARGETS.balanced.words} (2-3 paragraphs)
- "detailed": ${LENGTH_TARGETS.detailed.words} (3-4 paragraphs)`;

// ─── User prompt builder ───────────────────────────────────────

export function buildReviewResponseUserPrompt(input: ReviewInput): string {
  const cityShort = input.city.split(',')[0].trim();
  const safetyRules = getIndustrySafetyRules(input.industry);
  const safetyBlock = safetyRules.length
    ? `\n\nINDUSTRY SAFETY RULES (must follow):\n${safetyRules.map(r => '- ' + r).join('\n')}`
    : '';

  const reviewerLine = input.reviewerName
    ? `Reviewer name: ${input.reviewerName} (use the name once, naturally, in 1-2 of the 3 variations — not all three)`
    : 'Reviewer is anonymous (no name to use — open with a warm phrase, not "Hi reviewer")';

  const ratingGuide = ratingGuidance(input.rating);

  return `Write 3 distinct response variations to this Google review.

THE REVIEW:
Star rating: ${input.rating}/5
${reviewerLine}
Review text:
"""
${input.reviewText.trim()}
"""

YOUR BUSINESS:
- Name: ${input.biz}
- Industry: ${input.industry}
- City: ${input.city}  (use the short form "${cityShort}" in conversation)

TONE: ${input.tone}
${TONE_GUIDE[input.tone]}

RATING-SPECIFIC GUIDANCE:
${ratingGuide}${safetyBlock}

REQUIREMENTS:
1. The 3 variations must be DIFFERENT in approach — different opening, different specific detail referenced, different closing. Not three rephrasings of the same response.
2. Each response must reference at least ONE specific detail from the original review (a praise word, a complaint, a service mentioned, a name, a number).
3. Mention "${input.biz}" once per response (not in the very first sentence — weave it in). Mention "${cityShort}" once. No more.
4. EVERY response must use blank-line paragraph breaks (\\n\\n in the JSON string). No wall of text.
5. Tone must stay consistent with "${input.tone}" across all 3 variations.
6. NEVER fabricate details the review didn't include (no inventing names, no inventing dates, no claiming "we met your wife" if not in the review).
7. NEVER admit legal fault. Use "we should have done better" not "we were negligent / wrong / at fault."
8. For 1-3 star reviews: each response must include a clear off-platform resolution path (call us, email the manager, etc.).
9. Output ONLY the JSON object — no commentary, no markdown fences.

Remember: study the EXAMPLES in the system prompt for FORMATTING — paragraph breaks are not optional.`;
}

function ratingGuidance(rating: number): string {
  if (rating === 5) return 'This is a 5-star review. Lead with genuine appreciation, reference what they specifically loved, and close with a warm invitation to return or refer. Avoid sycophancy. Vary the opening across the 3 variations.';
  if (rating === 4) return 'This is a 4-star review. Show appreciation, then ask (gently, without begging) what would have made it 5 stars. Or, if they mentioned a specific issue, address it concretely without being defensive.';
  if (rating === 3) return 'This is a 3-star (mixed) review. Acknowledge both what worked and what didn\'t. Show that you\'re taking the criticism seriously. Offer a clear path to make the next visit better.';
  if (rating === 2) return 'This is a 2-star review. Lead with empathy. Acknowledge their specific frustration. Take quiet ownership ("we should have done better") without legal admission. Always include an off-platform resolution path.';
  return 'This is a 1-star review. The response is for the NEXT 100 readers, not the angry reviewer. Stay calm. Don\'t argue. Don\'t list excuses. Acknowledge their specific experience, accept ownership of the system failure (not personal blame), and offer a clear off-platform path. NEVER promise compensation publicly. NEVER admit legal fault.';
}

// ─── Anti-pattern detection (shared with GBP — review-specific additions) ──

const ANTI_PATTERNS = [
  /your satisfaction is our/i, /we pride ourselves/i, /thank you for choosing/i,
  /we value your (business|feedback)/i, /we sincerely apologize for any inconvenience/i,
  /rest assured/i, /please feel free/i, /please don['']?t hesitate/i, /kindly/i,
  /on behalf of the entire team/i, /we are committed to/i, /we strive to/i,
  /we are pleased to/i, /we are excited to/i, /duly noted/i, /as per your/i,
  /tailored to your needs/i, /comprehensive (services|solutions|care)/i,
  /industry[- ]leading/i, /state[- ]of[- ]the[- ]art/i, /cutting[- ]edge/i,
  /delve into/i, /in today['']?s .* world/i,
];

export function hasAntiPattern(text: string): boolean {
  return ANTI_PATTERNS.some(rx => rx.test(text));
}

export function cleanAntiPatterns(text: string): string {
  let t = text;
  t = t.replace(/Your satisfaction is our top priority\.?\s*/gi, '');
  t = t.replace(/We pride ourselves on/gi, 'We focus on');
  t = t.replace(/We sincerely apologize for any inconvenience\.?/gi, 'That isn\'t the experience we want anyone to have.');
  t = t.replace(/We strive to/gi, 'We aim to');
  t = t.replace(/Rest assured(?:,)?\s*/gi, '');
  t = t.replace(/Please feel free to/gi, 'You can');
  t = t.replace(/Please don['']?t hesitate to/gi, 'Just');
  t = t.replace(/Thank you for choosing /gi, 'Thanks for picking ');
  t = t.replace(/On behalf of the entire team,?\s*/gi, '');
  t = t.replace(/We are committed to/gi, 'We work hard to');
  return t.trim();
}

// ─── HIPAA / privilege guardrail check ─────────────────────────
// Scans generated text for tell-tale violations. Used both as a scoring penalty
// and as a regenerate trigger if score is low.

const HIPAA_VIOLATION_PATTERNS = [
  /your (root canal|filling|crown|extraction|cleaning|implant|whitening|braces|invisalign|veneer|botox|injection|prescription|surgery|procedure|biopsy|diagnosis|condition|medication|treatment|therapy session)/i,
  /your (heart|knee|back|shoulder|hip|spine|nerve|joint) (issue|pain|problem|condition)/i,
  /thanks for trusting us with your/i,
];

const LEGAL_VIOLATION_PATTERNS = [
  /your case (was|went|outcome|settlement)/i,
  /we (won|lost|settled) your/i,
  /your (custody|divorce|criminal|trial|hearing|deposition)/i,
  /the (court|judge|jury) ruled/i,
];

export function checkPrivilegedContentViolation(text: string, industry: string): { violation: boolean; type?: string } {
  const ind = (industry || '').toLowerCase();
  if (HIPAA_INDUSTRIES.some(k => ind.includes(k))) {
    if (HIPAA_VIOLATION_PATTERNS.some(rx => rx.test(text))) {
      return { violation: true, type: 'hipaa' };
    }
  }
  if (LEGAL_PRIVILEGE_INDUSTRIES.some(k => ind.includes(k))) {
    if (LEGAL_VIOLATION_PATTERNS.some(rx => rx.test(text))) {
      return { violation: true, type: 'legal' };
    }
  }
  return { violation: false };
}

// ─── 100-point quality scorer ──────────────────────────────────
// 10 rules tailored to review responses (different from GBP scorer).

export function scoreReviewResponse(
  text: string,
  input: ReviewInput,
  variant: 'concise' | 'balanced' | 'detailed',
): number {
  let score = 0;
  const wc = text.trim().split(/\s+/).length;
  const paragraphs = text.split(/\n\s*\n/).map(p => p.trim()).filter(Boolean);
  const lower = text.toLowerCase();
  const review = input.reviewText.toLowerCase();
  const cityShort = input.city.split(',')[0].trim().toLowerCase();
  const bizName = input.biz.toLowerCase();
  const escCity = cityShort.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const escBiz = bizName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  // Rule 1: Acknowledgment of specific detail (15 pts)
  // Look for words that appear in BOTH review and response — proves real reading.
  const reviewWords = review
    .split(/[^a-z0-9]+/)
    .filter(w => w.length > 4 && !STOP_WORDS.has(w));
  const overlap = reviewWords.filter(w => lower.includes(w));
  // De-dupe overlap
  const uniqueOverlap = Array.from(new Set(overlap));
  if (uniqueOverlap.length >= 3) score += 15;
  else if (uniqueOverlap.length === 2) score += 10;
  else if (uniqueOverlap.length === 1) score += 5;

  // Rule 2: Empathy / gratitude alignment with rating (15 pts)
  if (input.rating <= 2) {
    // Negative review — empathy phrases
    const empathyHits = [
      /sorry/i, /should have/i, /that['']?s on us/i, /we hear you/i,
      /we let you down/i, /didn['']?t live up/i, /that isn['']?t the experience/i,
      /we understand/i, /that['']?s frustrating/i, /right (about|to)/i,
    ].filter(rx => rx.test(text)).length;
    score += Math.min(empathyHits * 5, 15);
  } else if (input.rating === 3) {
    const mixedHits = [
      /thank you/i, /honest feedback/i, /both/i, /aim to/i, /take.*seriously/i,
      /next time/i, /better/i, /fair/i, /appreciate/i,
    ].filter(rx => rx.test(text)).length;
    score += Math.min(mixedHits * 4, 15);
  } else {
    // Positive — gratitude, but not generic
    const gratitudeHits = [
      /thank/i, /glad/i, /thrilled/i, /means a lot/i, /grateful/i,
      /honored/i, /made (our|my) (day|week)/i, /love hearing/i, /happy/i,
    ].filter(rx => rx.test(text)).length;
    score += Math.min(gratitudeHits * 4, 15);
  }

  // Rule 3: Business name + city placement (10 pts)
  const bizHits = (text.match(new RegExp('\\b' + escBiz + '\\b', 'gi')) || []).length;
  const cityHits = (text.match(new RegExp('\\b' + escCity + '\\b', 'gi')) || []).length;
  if (bizHits === 1) score += 5;
  else if (bizHits === 2) score += 3;
  if (cityHits >= 1 && cityHits <= 2) score += 5;
  else if (cityHits === 0) score += 0;

  // Rule 4: Length fit per variant (10 pts)
  const target = LENGTH_TARGETS[variant];
  if (wc >= target.min && wc <= target.max) score += 10;
  else if (wc >= target.min * 0.75 && wc <= target.max * 1.3) score += 5;

  // Rule 5: Active voice + contractions (10 pts)
  const contractionHits = (text.match(/\b(we['']?re|don['']?t|can['']?t|won['']?t|it['']?s|that['']?s|you['']?re|we['']?ve|isn['']?t|here['']?s|what['']?s|i['']?m|i['']?ve|you['']?ll|we['']?ll|let['']?s)\b/gi) || []).length;
  if (contractionHits >= 2) score += 6;
  else if (contractionHits === 1) score += 3;
  if (/\b(we|our|us|i)\b/i.test(text)) score += 4;

  // Rule 6: Anti-pattern absence (10 pts)
  if (!hasAntiPattern(text)) score += 10;
  else score += 0;

  // Rule 7: Resolution path for negative reviews (10 pts)
  if (input.rating <= 3) {
    const resHits = [
      /call (us|the (office|store|salon|shop))/i, /email/i, /reach out/i, /contact/i,
      /direct(ly)?/i, /our (number|line|office)/i, /please .* (call|reach|contact)/i,
      /pick up/i, /the manager/i, /the gm/i, /the owner/i, /come back/i, /(come|stop) by/i,
    ].filter(rx => rx.test(text)).length;
    if (resHits >= 2) score += 10;
    else if (resHits === 1) score += 6;
  } else {
    // For positives — invitation to return / next-step counts here
    const inviteHits = [
      /see you (soon|next|in)/i, /come back/i, /next visit/i, /next time/i,
      /tell .* friend/i, /referr/i, /share/i, /let us know how/i, /call us anytime/i,
    ].filter(rx => rx.test(text)).length;
    if (inviteHits >= 1) score += 10;
  }

  // Rule 8: Privilege violation penalty (10 pts)
  // Full points if NO violation; zero if HIPAA / legal violation found.
  const priv = checkPrivilegedContentViolation(text, input.industry);
  if (!priv.violation) score += 10;

  // Rule 9: CTA / next step direction (5 pts)
  if (/(book|call|schedule|return|come|reach|email|stop by|see you)/i.test(text)) score += 5;

  // Rule 10: Formatting quality (15 pts)
  const expectedParagraphs = variant === 'concise' ? 1 : variant === 'balanced' ? 2 : 3;
  if (paragraphs.length >= expectedParagraphs) score += 8;
  else if (paragraphs.length >= 1) score += 4;
  if (paragraphs.every(p => p.length <= 350)) score += 4;
  else if (paragraphs.every(p => p.length <= 500)) score += 2;
  // No sign-offs that fabricate identity
  if (!/(— [A-Z][a-z]+ [A-Z][a-z]+,)|(— Dr\. [A-Z])/i.test(text)) score += 3;

  return Math.min(score, 100);
}

// Stopwords to exclude from "review-overlap" scoring (rule 1).
const STOP_WORDS = new Set([
  'about', 'after', 'again', 'against', 'because', 'before', 'being', 'below',
  'between', 'could', 'doing', 'during', 'every', 'first', 'their', 'there',
  'these', 'those', 'through', 'under', 'until', 'while', 'would', 'really',
  'still', 'going', 'never', 'always', 'thank', 'thanks', 'review', 'visit',
  'place', 'people', 'great', 'service', 'staff', 'that', 'this', 'them', 'they',
  'with', 'have', 'were', 'will', 'just', 'when', 'from', 'your', 'you', 'and',
  'but', 'the',
]);

// ─── Industry-aware response time hint ─────────────────────────

export function getResponseTimeHint(rating: number): string {
  if (rating <= 2) return 'Respond within 4 hours. Negative reviews accumulate views fast — every hour after publication, your response carries less weight.';
  if (rating === 3) return 'Respond within 24 hours. Mixed reviews are an opportunity to show responsiveness publicly.';
  return 'Respond within 48 hours. Even quick "thanks" replies keep your response rate high — Google rewards 80%+ response rates.';
}

// ─── Pre-built tips per response (added at decoration time) ────

export function getResponseTip(rating: number, hasResolutionPath: boolean): string {
  if (rating <= 2 && !hasResolutionPath) return 'Add a phone number or "ask for the manager" to move this off-platform — public negotiations rarely end well.';
  if (rating <= 2) return 'After posting, also send an internal note to your team to log this complaint — patterns matter more than single reviews.';
  if (rating === 3) return 'Consider what specific change you\'ll make based on this feedback. Mixed reviews are operational gold.';
  if (rating === 4) return 'Want the 5th star? Reply, then follow up via email/text after a week — most reviewers will update their rating once.';
  return 'Bonus: ask if they\'d share their experience on Yelp / Facebook too. 10-15% of respondents say yes.';
}
