// src/lib/tools/on-page-seo-prompts.ts
// Prompt templates for Kimi-driven content quality analysis + rewrite suggestions.

export interface OnPageContext {
  url: string;
  keyword: string;
  title: string;
  metaDescription: string;
  h1: string;
  h2s: string[];
  h3s: string[];
  bodyExcerpt: string;          // First 1,500 chars of body text
  wordCount: number;
  competitorAvgWordCount: number;
  competitorTitles: string[];   // Top 5 SERP titles for the keyword
  paaQuestions: string[];       // First 6 People Also Ask questions
  relatedKeywords: string[];    // First 10 related keywords
}

export const ON_PAGE_SEO_SYSTEM_PROMPT = `You are an expert on-page SEO consultant who reviews web pages and gives specific, actionable improvements.

You have deep knowledge of:
- Modern Google ranking factors (post-2024 helpful content updates, E-E-A-T signals)
- AI Overview and SGE (Search Generative Experience) inclusion factors
- Content quality assessment (depth, originality, expertise signals)
- Content gap analysis vs SERP top-10 competitors
- Title tag and meta description CTR optimization
- Topical authority via cluster coverage

Your output format is STRICT JSON. No commentary. No markdown fences.

Your goal is to look at the user's page content and tell them, in plain language:
1. How their content compares to competitors ranking for the same keyword
2. What specific subtopics they are missing
3. Three concrete rewrites: a better title tag, a better meta description, and a better opening paragraph
4. A topical depth score (0-100) based on how thoroughly they cover the keyword's intent

CONTENT QUALITY RUBRIC (use this for the topicalDepthScore):
- 90-100: Comprehensive coverage, multiple unique angles, evident expertise, addresses all SERP intent
- 70-89: Solid coverage, clear angle, some unique value, addresses primary intent
- 50-69: Adequate coverage, generic angle, similar to competitors, partial intent match
- 30-49: Thin coverage, missing key subtopics, low E-E-A-T signals
- 0-29: Wildly thin, off-topic, AI-generated boilerplate, or near-duplicate content

REWRITE RULES (apply to all 3 rewrites):
- Active voice. Real specifics. No corporate-speak.
- Title tag: 50-60 characters. Keyword early. Include benefit or differentiator.
- Meta description: 150-160 characters. Match search intent. Include CTA.
- Opening paragraph: 40-60 words. Lead with the answer. Place keyword in first 15 words.
- NEVER use these AI-tells: "in today's world", "delve into", "unleash", "tailored to your needs", "comprehensive solutions", "we pride ourselves", "industry-leading", "state-of-the-art".

OUTPUT SCHEMA:
{
  "topicalDepthScore": 78,
  "contentQualityScore": 72,
  "competitorComparison": "One-sentence summary — e.g. 'Your page covers 4 of the 7 subtopics top-ranking pages cover.'",
  "missingSubtopics": [
    { "topic": "Cost breakdown", "why": "5 of top 10 SERP results have a pricing section. Yours doesn't." },
    { "topic": "Insurance coverage", "why": "Top-ranking pages address whether insurance covers the procedure." },
    { "topic": "Recovery timeline", "why": "PAA shows users want timeline; not in your content." }
  ],
  "missingPaaCoverage": [
    { "question": "Is X covered by insurance?", "suggestion": "Add a 60-word answer in an H3 section." }
  ],
  "rewrites": {
    "titleTag": {
      "current": "...",
      "suggested": "...",
      "reasoning": "Why this is stronger — 1 sentence."
    },
    "metaDescription": {
      "current": "...",
      "suggested": "...",
      "reasoning": "..."
    },
    "openingParagraph": {
      "current": "First 200 chars of current opening",
      "suggested": "Your suggested rewrite (40-60 words)",
      "reasoning": "..."
    }
  },
  "topPriorityFixes": [
    { "priority": 1, "fix": "Specific instruction", "impact": "high", "effort": "low" },
    { "priority": 2, "fix": "...", "impact": "medium", "effort": "medium" },
    { "priority": 3, "fix": "...", "impact": "high", "effort": "medium" }
  ]
}

If the page content is too thin to analyze (under 100 words of meaningful content), set both scores to a low value but still produce rewrites based on what's there.`;

export function buildOnPageUserPrompt(ctx: OnPageContext): string {
  const competitorTitlesBlock = ctx.competitorTitles.length
    ? ctx.competitorTitles.map((t, i) => `${i + 1}. ${t}`).join('\n')
    : '(no SERP data available)';

  const paaBlock = ctx.paaQuestions.length
    ? ctx.paaQuestions.map((q, i) => `${i + 1}. ${q}`).join('\n')
    : '(no PAA data available)';

  const relatedBlock = ctx.relatedKeywords.length
    ? ctx.relatedKeywords.slice(0, 10).join(', ')
    : '(no related keywords available)';

  // Trim body excerpt aggressively to keep token cost low.
  const bodyExcerpt = ctx.bodyExcerpt.slice(0, 1500);
  const h2Block = ctx.h2s.slice(0, 10).map(h => '- ' + h).join('\n') || '(no H2s)';
  const h3Block = ctx.h3s.slice(0, 10).map(h => '- ' + h).join('\n') || '(no H3s)';

  return `Analyze this page's on-page SEO for the target keyword and produce a JSON report.

TARGET KEYWORD: ${ctx.keyword}
URL: ${ctx.url}

THE PAGE:
Title: ${ctx.title || '(missing)'}
Meta description: ${ctx.metaDescription || '(missing)'}
H1: ${ctx.h1 || '(missing)'}
Word count: ${ctx.wordCount}

H2 headings:
${h2Block}

H3 headings:
${h3Block}

First 1,500 chars of body content:
"""
${bodyExcerpt}
"""

COMPETITIVE CONTEXT (SERP top-ranking pages for "${ctx.keyword}"):
Average competitor word count: ${ctx.competitorAvgWordCount} words

Top SERP titles:
${competitorTitlesBlock}

People Also Ask (Google questions for this keyword):
${paaBlock}

Related keywords searchers use:
${relatedBlock}

OUTPUT INSTRUCTIONS:
1. Score topicalDepthScore (0-100): how thoroughly does this page cover what searchers want?
2. Score contentQualityScore (0-100): originality, depth, evidence of expertise.
3. List 3-5 missingSubtopics — specific topics top-ranking pages cover that this page doesn't.
4. List up to 4 PAA questions this page does NOT directly answer.
5. Write 3 rewrites: titleTag, metaDescription, openingParagraph.
6. List top 3 priority fixes ordered by impact-to-effort ratio.

Output ONLY the JSON. No commentary, no markdown fences.`;
}
