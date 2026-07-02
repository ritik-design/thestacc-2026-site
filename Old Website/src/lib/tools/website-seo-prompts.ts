// src/lib/tools/website-seo-prompts.ts
// Kimi prompt for narrative SEO summary + strategic recommendations.

export interface SiteSummaryContext {
  url: string;
  domain: string;
  bizName?: string;
  city?: string;
  industry?: string;
  overallScore: number;
  grade: string;
  // Real metrics
  drNormalized: number | null;
  refDomains: number | null;
  estTraffic: number | null;
  totalRankingKeywords: number | null;
  pos1to3: number | null;
  performanceScore: number | null;
  // Page signals
  title: string;
  metaDescription: string;
  h1: string;
  wordCount: number;
  hasFaqSchema: boolean;
  hasLocalBizSchema: boolean;
  hasLlmsTxt: boolean;
  // Top keywords ranking
  topRankingKeywords: Array<{ keyword: string; position: number; volume: number }>;
  // Dimension scores
  dimensionScores: Array<{ label: string; score: number; max: number; status: string }>;
  // Already-identified failed checks
  topFailedChecks: Array<{ label: string; fix: string }>;
}

export const WEBSITE_SEO_SYSTEM_PROMPT = `You are an expert SEO consultant who reviews a website's complete SEO health and writes plain-language strategic recommendations for the business owner.

You produce three things:
1. A 2-3 sentence executive summary in plain English (no jargon)
2. The single biggest SEO opportunity for this site (one specific, actionable thing)
3. A 60-day action plan with 5 specific tasks ordered by ROI

VOICE:
- Direct. No corporate-speak. No "in today's digital landscape."
- Specific numbers. "Add 600 words" beats "expand your content."
- Real recommendations. "Add LocalBusiness schema with type Dentist" beats "improve your schema."
- Honest. If the site is already strong in a dimension, say so. If it's a disaster, say so without hedging.

NEVER USE:
"in today's world", "delve into", "tailored to your needs", "comprehensive solutions",
"we pride ourselves", "industry-leading", "state-of-the-art", "leverage", "synergies",
"unlock the full potential", "best-in-class".

OUTPUT SCHEMA (strict JSON, no commentary, no markdown fences):
{
  "executiveSummary": "2-3 sentences, plain English. Reference the score and grade. Mention the strongest and weakest dimension by name.",
  "biggestOpportunity": {
    "headline": "Short headline (8-15 words) describing the #1 lever",
    "explanation": "1 paragraph (50-80 words) explaining what to do and why",
    "expectedImpact": "Concrete impact statement — e.g. 'Could move 5-15 ranking keywords into top-10 positions within 60 days.'"
  },
  "actionPlan": [
    { "week": 1, "task": "Specific, named task", "estimatedHours": 2, "expectedScoreLift": 5 },
    { "week": 1, "task": "...", "estimatedHours": 1, "expectedScoreLift": 3 },
    { "week": 2, "task": "...", "estimatedHours": 4, "expectedScoreLift": 6 },
    { "week": 4, "task": "...", "estimatedHours": 8, "expectedScoreLift": 8 },
    { "week": 8, "task": "...", "estimatedHours": 20, "expectedScoreLift": 12 }
  ],
  "competitivePositioning": "1 sentence comparing this site's authority + traffic to typical industry benchmarks. Honest, not flattering."
}

Use the actual numbers in the summary. If DR is 12, say "DR 12 — early stage." If 70, say "DR 70 — strong authority."`;

export function buildSiteSummaryUserPrompt(ctx: SiteSummaryContext): string {
  const dimBlock = ctx.dimensionScores.map(d => `  - ${d.label}: ${d.score}/${d.max} (${d.status})`).join('\n');
  const topKwBlock = ctx.topRankingKeywords.length
    ? ctx.topRankingKeywords.slice(0, 5).map(k => `  - "${k.keyword}" — pos ${k.position}, vol ${k.volume.toLocaleString()}`).join('\n')
    : '  (no top ranking keywords found)';
  const failedBlock = ctx.topFailedChecks.length
    ? ctx.topFailedChecks.slice(0, 8).map(c => `  - ${c.label}: ${c.fix}`).join('\n')
    : '  (no failed checks)';

  const bizContext = ctx.bizName ? `Business: ${ctx.bizName}` : 'Business name: (not provided)';
  const cityContext = ctx.city ? `City/area: ${ctx.city}` : 'City: (not provided)';

  return `Analyze this website's complete SEO health and produce a strategic summary.

THE SITE:
URL: ${ctx.url}
Domain: ${ctx.domain}
${bizContext}
${cityContext}
Industry hint: ${ctx.industry || 'unknown'}

OVERALL SCORE: ${ctx.overallScore}/100 · Grade ${ctx.grade}

REAL METRICS (from DataForSEO + Google PageSpeed):
- Domain Rating: ${ctx.drNormalized != null ? `${ctx.drNormalized}/100` : 'unavailable'}
- Referring domains: ${ctx.refDomains != null ? ctx.refDomains.toLocaleString() : 'unavailable'}
- Estimated monthly organic traffic: ${ctx.estTraffic != null ? ctx.estTraffic.toLocaleString() : 'unavailable'}
- Total ranking keywords: ${ctx.totalRankingKeywords != null ? ctx.totalRankingKeywords.toLocaleString() : 'unavailable'}
- Keywords in top-3 positions: ${ctx.pos1to3 != null ? ctx.pos1to3 : 'unavailable'}
- Mobile PageSpeed score: ${ctx.performanceScore != null ? `${ctx.performanceScore}/100` : 'unavailable'}

TOP RANKING KEYWORDS:
${topKwBlock}

PAGE SIGNALS:
- Title: ${ctx.title || '(missing)'}
- H1: ${ctx.h1 || '(missing)'}
- Word count: ${ctx.wordCount}
- FAQ schema: ${ctx.hasFaqSchema ? 'present' : 'missing'}
- LocalBusiness schema: ${ctx.hasLocalBizSchema ? 'present' : 'missing'}
- llms.txt: ${ctx.hasLlmsTxt ? 'present' : 'missing'}

DIMENSION SCORES (out of 100 total):
${dimBlock}

FAILED / WEAK CHECKS NEEDING FIXES:
${failedBlock}

INSTRUCTIONS:
1. Write executiveSummary (2-3 sentences, plain English, reference the score and biggest weakness)
2. biggestOpportunity — pick the single highest-ROI lever based on the data
3. actionPlan — 5 tasks across weeks 1-8, ordered by ROI
4. competitivePositioning — 1 honest sentence

Output ONLY the JSON. No commentary, no markdown.`;
}
