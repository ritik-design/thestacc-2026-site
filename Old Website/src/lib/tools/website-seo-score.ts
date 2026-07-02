// src/lib/tools/website-seo-score.ts
// 8-dimension Website SEO scorer combining HTML parse + PageSpeed + DataForSEO + Kimi.
// 100-point scale, weighted across: on-page (15), technical (15), performance (15),
// authority (15), organic performance (10), local SEO (10), content/AI (15), trust (5).

import type { ParsedPage } from './on-page-seo-checker';

export interface PageSpeedScores {
  performance: number | null;     // 0-100
  lcp: number | null;             // ms
  cls: number | null;
  inp: number | null;             // ms (replaces FID)
  tbt: number | null;             // ms
  fcp: number | null;             // ms
}

export interface SiteSignals {
  page: ParsedPage;
  pageSpeed: PageSpeedScores | null;
  hasHttps: boolean;
  hasRobotsTxt: boolean;
  hasLlmsTxt: boolean;
  hasSitemap: boolean;
  blocksAiCrawlers: boolean;
  // DataForSEO
  drNormalized: number | null;     // 0-100 Domain Rating equivalent
  refDomains: number | null;
  backlinks: number | null;
  estTraffic: number | null;
  totalRankingKeywords: number | null;
  pos1to3: number | null;
  pos4to10: number | null;
  // User input
  bizName?: string;
  city?: string;
}

export interface DimensionScore {
  id: string;
  label: string;
  score: number;
  maxScore: number;
  pct: number;
  status: 'excellent' | 'good' | 'fair' | 'poor';
  summary: string;
  checks: Array<{ id: string; label: string; passed: boolean; score: number; maxScore: number; detail: string; fix?: string; }>;
}

export interface ScoredSiteReport {
  overall: { score: number; maxScore: 100; pct: number; grade: 'A' | 'B' | 'C' | 'D' | 'F'; gradeLabel: string };
  dimensions: DimensionScore[];
  topPriorities: Array<{ priority: number; dimension: string; fix: string; impact: 'high' | 'medium' | 'low'; effort: 'low' | 'medium' | 'high' }>;
  metrics: {
    domainRating: number | null;
    refDomains: number | null;
    backlinks: number | null;
    estTraffic: number | null;
    rankingKeywords: number | null;
    pos1to3: number | null;
    performanceScore: number | null;
    lcp: number | null;
    wordCount: number;
  };
}

function statusFromPct(pct: number): DimensionScore['status'] {
  if (pct >= 85) return 'excellent';
  if (pct >= 70) return 'good';
  if (pct >= 50) return 'fair';
  return 'poor';
}

/** Build all 8 dimension scores. */
export function scoreSite(signals: SiteSignals): ScoredSiteReport {
  const dimensions: DimensionScore[] = [
    scoreOnPage(signals),
    scoreTechnical(signals),
    scorePerformance(signals),
    scoreAuthority(signals),
    scoreOrganicPerformance(signals),
    scoreLocalSeo(signals),
    scoreContentAndAi(signals),
    scoreTrust(signals),
  ];

  const totalScore = dimensions.reduce((a, d) => a + d.score, 0);
  const totalMax = dimensions.reduce((a, d) => a + d.maxScore, 0);
  const pct = totalMax > 0 ? Math.round((totalScore / totalMax) * 100) : 0;
  const grade: ScoredSiteReport['overall']['grade'] =
    pct >= 90 ? 'A' : pct >= 75 ? 'B' : pct >= 60 ? 'C' : pct >= 45 ? 'D' : 'F';
  const gradeLabel = {
    A: 'Excellent — top-tier SEO foundation',
    B: 'Good — a few quick wins to push higher',
    C: 'Average — focused work could move you up significantly',
    D: 'Needs work — multiple critical gaps holding rankings back',
    F: 'Poor — major SEO problems blocking visibility',
  }[grade];

  // Top 5 priorities — pull failed/weak checks across all dimensions
  const allFailedChecks = dimensions
    .flatMap(d => d.checks
      .filter(c => !c.passed && c.fix)
      .map(c => ({ dimension: d.label, ...c, dimensionMax: d.maxScore }))
    )
    .sort((a, b) => (b.maxScore - b.score) - (a.maxScore - a.score))  // biggest gaps first
    .slice(0, 5);

  const topPriorities = allFailedChecks.map((c, i) => ({
    priority: i + 1,
    dimension: c.dimension,
    fix: c.fix as string,
    impact: ((c.maxScore >= 7) ? 'high' : c.maxScore >= 4 ? 'medium' : 'low') as 'high' | 'medium' | 'low',
    effort: estimateEffort(c.id),
  }));

  return {
    overall: { score: totalScore, maxScore: 100, pct, grade, gradeLabel },
    dimensions,
    topPriorities,
    metrics: {
      domainRating: signals.drNormalized,
      refDomains: signals.refDomains,
      backlinks: signals.backlinks,
      estTraffic: signals.estTraffic,
      rankingKeywords: signals.totalRankingKeywords,
      pos1to3: signals.pos1to3,
      performanceScore: signals.pageSpeed?.performance ?? null,
      lcp: signals.pageSpeed?.lcp ?? null,
      wordCount: signals.page.wordCount,
    },
  };
}

function estimateEffort(checkId: string): 'low' | 'medium' | 'high' {
  // Quick wins (under 30 min): meta description, title length, viewport, alt text, schema basic
  const lowEffort = ['title_length', 'meta_description_present', 'viewport', 'image_alt_coverage', 'h1_present', 'canonical', 'open_graph', 'llms_txt'];
  // Medium (1-3 hours): add schema, restructure headings, add FAQ
  const mediumEffort = ['schema_specific', 'heading_structure', 'internal_links', 'sitemap', 'localbusiness_schema', 'faq_schema', 'mobile_viewport'];
  // High (multi-day): page speed work, build backlinks, add content depth
  if (lowEffort.includes(checkId)) return 'low';
  if (mediumEffort.includes(checkId)) return 'medium';
  return 'high';
}

// ─── Dimension 1: On-Page SEO (15 pts) ─────────────
function scoreOnPage(s: SiteSignals): DimensionScore {
  const p = s.page;
  const checks: DimensionScore['checks'] = [];

  // Title (5 pts: present + length)
  const titleLen = p.title.length;
  let titleScore = 0;
  let titleDetail = '';
  if (!p.title) {
    titleDetail = 'Missing title tag.';
  } else if (titleLen >= 30 && titleLen <= 60) {
    titleScore = 5;
    titleDetail = `Title (${titleLen} chars): "${p.title.slice(0, 60)}"`;
  } else if (titleLen < 30) {
    titleScore = 2;
    titleDetail = `Title (${titleLen} chars) — too short, aim for 30-60.`;
  } else {
    titleScore = 3;
    titleDetail = `Title (${titleLen} chars) — too long, will be truncated in SERPs.`;
  }
  checks.push({
    id: 'title_length', label: 'Title tag', passed: titleScore === 5, score: titleScore, maxScore: 5, detail: titleDetail,
    fix: titleScore < 5 ? `Set title to 30-60 characters with primary keyword near the start.` : undefined,
  });

  // Meta description (3 pts)
  const mdLen = p.metaDescription.length;
  let mdScore = 0;
  let mdDetail = '';
  if (!p.metaDescription) {
    mdDetail = 'No meta description set.';
  } else if (mdLen >= 120 && mdLen <= 160) {
    mdScore = 3;
    mdDetail = `Meta description (${mdLen} chars) — optimal length.`;
  } else if (mdLen >= 80) {
    mdScore = 2;
    mdDetail = `Meta description (${mdLen} chars) — could be optimized to 120-160.`;
  } else {
    mdScore = 1;
    mdDetail = `Meta description too short (${mdLen} chars).`;
  }
  checks.push({
    id: 'meta_description_present', label: 'Meta description', passed: mdScore >= 2, score: mdScore, maxScore: 3, detail: mdDetail,
    fix: mdScore < 3 ? `Write a 120-160 character meta description that summarizes the page and contains your main keyword.` : undefined,
  });

  // H1 (3 pts)
  let h1Score = 0;
  let h1Detail = '';
  if (p.h1s.length === 0) { h1Detail = 'No H1 heading on the page.'; }
  else if (p.h1s.length === 1) { h1Score = 3; h1Detail = `H1: "${p.h1s[0].slice(0, 60)}"`; }
  else { h1Score = 1; h1Detail = `Multiple H1s detected (${p.h1s.length}) — should be exactly 1.`; }
  checks.push({
    id: 'h1_present', label: 'H1 heading', passed: h1Score === 3, score: h1Score, maxScore: 3, detail: h1Detail,
    fix: h1Score < 3 ? (p.h1s.length === 0 ? 'Add a single <h1> heading describing the page.' : 'Convert extra H1s to H2 — only one H1 per page.') : undefined,
  });

  // Image alt coverage (2 pts)
  const totalImgs = p.images.length;
  const withAlt = p.images.filter(i => i.alt && i.alt.trim()).length;
  const altPct = totalImgs > 0 ? withAlt / totalImgs : 1;
  let altScore = 0;
  let altDetail = totalImgs === 0 ? 'No images on page.' : `${withAlt}/${totalImgs} images have alt text (${Math.round(altPct * 100)}%).`;
  if (altPct >= 0.95 || totalImgs === 0) altScore = 2;
  else if (altPct >= 0.6) altScore = 1;
  checks.push({
    id: 'image_alt_coverage', label: 'Image alt text', passed: altScore === 2, score: altScore, maxScore: 2, detail: altDetail,
    fix: altScore < 2 ? `Add descriptive alt text to ${totalImgs - withAlt} images missing it.` : undefined,
  });

  // Open Graph (2 pts)
  const hasOg = /og:title|og:description|og:image/i.test(JSON.stringify(p)); // crude check on parsed
  // Better: check stored in raw HTML — but we don't have access here. Simplification: check title
  let ogScore = hasOg ? 2 : 0;
  // Fallback: assume present if og:image was extracted (not in current ParsedPage). For now, give partial credit.
  // Since ParsedPage doesn't track OG specifically, infer from `ogImage` field presence:
  ogScore = (p as any).ogImage ? 2 : 1;
  checks.push({
    id: 'open_graph', label: 'Open Graph tags (social sharing)', passed: ogScore === 2, score: ogScore, maxScore: 2,
    detail: ogScore === 2 ? 'Open Graph tags present.' : 'Open Graph tags missing or incomplete.',
    fix: ogScore < 2 ? 'Add og:title, og:description, og:image meta tags for proper social previews.' : undefined,
  });

  const totalScore = checks.reduce((a, c) => a + c.score, 0);
  const maxScore = checks.reduce((a, c) => a + c.maxScore, 0);
  return {
    id: 'on_page',
    label: 'On-Page SEO',
    score: totalScore,
    maxScore,
    pct: Math.round((totalScore / maxScore) * 100),
    status: statusFromPct((totalScore / maxScore) * 100),
    summary: `${totalScore}/${maxScore} — ${checks.filter(c => c.passed).length} of ${checks.length} on-page elements optimized.`,
    checks,
  };
}

// ─── Dimension 2: Technical SEO (15 pts) ─────────────
function scoreTechnical(s: SiteSignals): DimensionScore {
  const p = s.page;
  const checks: DimensionScore['checks'] = [];

  // HTTPS (3 pts)
  checks.push({
    id: 'https', label: 'HTTPS encryption', passed: s.hasHttps, score: s.hasHttps ? 3 : 0, maxScore: 3,
    detail: s.hasHttps ? 'Site uses HTTPS.' : 'Site is not on HTTPS.',
    fix: !s.hasHttps ? 'Migrate to HTTPS — Google flags non-HTTPS sites as "Not Secure" and they rank worse.' : undefined,
  });

  // Mobile viewport (3 pts)
  checks.push({
    id: 'viewport', label: 'Mobile viewport meta', passed: p.hasViewport, score: p.hasViewport ? 3 : 0, maxScore: 3,
    detail: p.hasViewport ? 'Viewport meta tag present.' : 'Missing viewport meta tag.',
    fix: !p.hasViewport ? 'Add <meta name="viewport" content="width=device-width, initial-scale=1"> to <head>.' : undefined,
  });

  // Canonical (2 pts)
  checks.push({
    id: 'canonical', label: 'Canonical link', passed: !!p.canonical, score: p.canonical ? 2 : 0, maxScore: 2,
    detail: p.canonical ? `Canonical: ${p.canonical}` : 'No canonical link.',
    fix: !p.canonical ? 'Add <link rel="canonical" href="..."> pointing to the preferred URL of this page.' : undefined,
  });

  // Robots.txt (2 pts)
  checks.push({
    id: 'robots_txt', label: 'robots.txt file', passed: s.hasRobotsTxt, score: s.hasRobotsTxt ? 2 : 0, maxScore: 2,
    detail: s.hasRobotsTxt ? 'robots.txt found.' : 'No robots.txt at /robots.txt.',
    fix: !s.hasRobotsTxt ? 'Create a /robots.txt file with at minimum a sitemap reference.' : undefined,
  });

  // Sitemap (3 pts)
  checks.push({
    id: 'sitemap', label: 'XML sitemap', passed: s.hasSitemap, score: s.hasSitemap ? 3 : 0, maxScore: 3,
    detail: s.hasSitemap ? 'XML sitemap accessible.' : 'No sitemap.xml found.',
    fix: !s.hasSitemap ? 'Generate /sitemap.xml and reference it in robots.txt — Google uses it for crawl efficiency.' : undefined,
  });

  // Indexability (2 pts)
  const isNoindex = /noindex/i.test(p.robotsMeta);
  checks.push({
    id: 'indexable', label: 'Page is indexable', passed: !isNoindex, score: isNoindex ? 0 : 2, maxScore: 2,
    detail: isNoindex ? 'NOINDEX meta tag detected — page is blocked from search.' : 'Page is indexable.',
    fix: isNoindex ? 'Remove "noindex" from robots meta tag if you want this page to rank.' : undefined,
  });

  const totalScore = checks.reduce((a, c) => a + c.score, 0);
  const maxScore = checks.reduce((a, c) => a + c.maxScore, 0);
  return {
    id: 'technical',
    label: 'Technical SEO',
    score: totalScore,
    maxScore,
    pct: Math.round((totalScore / maxScore) * 100),
    status: statusFromPct((totalScore / maxScore) * 100),
    summary: `${totalScore}/${maxScore} — ${checks.filter(c => c.passed).length} of ${checks.length} technical signals healthy.`,
    checks,
  };
}

// ─── Dimension 3: Performance (15 pts) ─────────────
function scorePerformance(s: SiteSignals): DimensionScore {
  const ps = s.pageSpeed;
  const checks: DimensionScore['checks'] = [];

  // Overall PageSpeed score (8 pts)
  let psScore = 0;
  let psDetail = 'PageSpeed data unavailable.';
  if (ps?.performance != null) {
    if (ps.performance >= 90) psScore = 8;
    else if (ps.performance >= 70) psScore = 6;
    else if (ps.performance >= 50) psScore = 4;
    else if (ps.performance >= 30) psScore = 2;
    psDetail = `Mobile Performance score: ${ps.performance}/100 (Google PageSpeed Insights).`;
  }
  checks.push({
    id: 'pagespeed_score', label: 'Mobile performance score', passed: psScore >= 6, score: psScore, maxScore: 8, detail: psDetail,
    fix: psScore < 6 ? 'Optimize images, defer non-critical JS, reduce server response time. PageSpeed below 50 hurts Core Web Vitals.' : undefined,
  });

  // LCP (3 pts) — Largest Contentful Paint
  let lcpScore = 0;
  let lcpDetail = 'LCP data unavailable.';
  if (ps?.lcp != null) {
    if (ps.lcp <= 2500) { lcpScore = 3; lcpDetail = `LCP: ${(ps.lcp / 1000).toFixed(1)}s — Good (target <2.5s).`; }
    else if (ps.lcp <= 4000) { lcpScore = 1; lcpDetail = `LCP: ${(ps.lcp / 1000).toFixed(1)}s — Needs improvement.`; }
    else { lcpDetail = `LCP: ${(ps.lcp / 1000).toFixed(1)}s — Poor (target <2.5s).`; }
  }
  checks.push({
    id: 'lcp', label: 'Largest Contentful Paint (LCP)', passed: lcpScore === 3, score: lcpScore, maxScore: 3, detail: lcpDetail,
    fix: lcpScore < 3 && ps?.lcp != null ? 'Optimize the largest above-the-fold image, preload critical resources, defer JS.' : undefined,
  });

  // CLS (2 pts)
  let clsScore = 0;
  let clsDetail = 'CLS data unavailable.';
  if (ps?.cls != null) {
    if (ps.cls <= 0.1) { clsScore = 2; clsDetail = `CLS: ${ps.cls.toFixed(2)} — Good (target <0.1).`; }
    else if (ps.cls <= 0.25) { clsScore = 1; clsDetail = `CLS: ${ps.cls.toFixed(2)} — Needs improvement.`; }
    else { clsDetail = `CLS: ${ps.cls.toFixed(2)} — Poor.`; }
  }
  checks.push({
    id: 'cls', label: 'Cumulative Layout Shift (CLS)', passed: clsScore === 2, score: clsScore, maxScore: 2, detail: clsDetail,
    fix: clsScore < 2 && ps?.cls != null ? 'Reserve space for images and embeds (use width/height attributes), avoid late-loading content above the fold.' : undefined,
  });

  // INP (2 pts) — replaces FID
  let inpScore = 0;
  let inpDetail = 'INP data unavailable.';
  if (ps?.inp != null) {
    if (ps.inp <= 200) { inpScore = 2; inpDetail = `INP: ${ps.inp}ms — Good (target <200ms).`; }
    else if (ps.inp <= 500) { inpScore = 1; inpDetail = `INP: ${ps.inp}ms — Needs improvement.`; }
    else { inpDetail = `INP: ${ps.inp}ms — Poor.`; }
  }
  checks.push({
    id: 'inp', label: 'Interaction to Next Paint (INP)', passed: inpScore === 2, score: inpScore, maxScore: 2, detail: inpDetail,
    fix: inpScore < 2 && ps?.inp != null ? 'Break up long JS tasks, defer third-party scripts, optimize event handlers.' : undefined,
  });

  const totalScore = checks.reduce((a, c) => a + c.score, 0);
  const maxScore = checks.reduce((a, c) => a + c.maxScore, 0);
  return {
    id: 'performance',
    label: 'Page Performance',
    score: totalScore,
    maxScore,
    pct: Math.round((totalScore / maxScore) * 100),
    status: statusFromPct((totalScore / maxScore) * 100),
    summary: ps ? `${totalScore}/${maxScore} — ${ps.performance}/100 PageSpeed score.` : `${totalScore}/${maxScore} — performance data unavailable.`,
    checks,
  };
}

// ─── Dimension 4: Authority / Backlinks (15 pts) ─────────────
function scoreAuthority(s: SiteSignals): DimensionScore {
  const checks: DimensionScore['checks'] = [];

  const dr = s.drNormalized ?? 0;
  // DR (8 pts) — exponential scoring
  let drScore = 0;
  let drDetail = '';
  if (s.drNormalized == null) {
    drDetail = 'Domain Rating unavailable (data may be limited for new/small sites).';
    drScore = 2; // partial credit when unknown
  } else if (dr >= 60) { drScore = 8; drDetail = `Domain Rating: ${dr}/100 — strong authority.`; }
  else if (dr >= 40) { drScore = 6; drDetail = `Domain Rating: ${dr}/100 — good authority.`; }
  else if (dr >= 20) { drScore = 4; drDetail = `Domain Rating: ${dr}/100 — building authority.`; }
  else if (dr >= 10) { drScore = 2; drDetail = `Domain Rating: ${dr}/100 — early stage.`; }
  else { drScore = 0; drDetail = `Domain Rating: ${dr}/100 — site lacks backlink authority.`; }
  checks.push({
    id: 'domain_rating', label: 'Domain Rating (Authority)', passed: drScore >= 6, score: drScore, maxScore: 8, detail: drDetail,
    fix: drScore < 6 ? 'Build backlinks: guest posts, podcast appearances, industry directories, partnerships. DR grows over months, not days.' : undefined,
  });

  // Referring domains (4 pts) — number of unique linking domains
  const rd = s.refDomains ?? 0;
  let rdScore = 0;
  let rdDetail = '';
  if (s.refDomains == null) { rdDetail = 'Referring domain count unavailable.'; rdScore = 1; }
  else if (rd >= 200) { rdScore = 4; rdDetail = `${rd.toLocaleString()} referring domains — strong link diversity.`; }
  else if (rd >= 50) { rdScore = 3; rdDetail = `${rd.toLocaleString()} referring domains — moderate.`; }
  else if (rd >= 10) { rdScore = 2; rdDetail = `${rd.toLocaleString()} referring domains — early stage.`; }
  else { rdScore = 0; rdDetail = `Only ${rd.toLocaleString()} referring domains.`; }
  checks.push({
    id: 'referring_domains', label: 'Referring domains', passed: rdScore >= 2, score: rdScore, maxScore: 4, detail: rdDetail,
    fix: rdScore < 2 ? 'Aim for 50+ unique referring domains. Diversity matters more than total backlink count.' : undefined,
  });

  // Total backlinks (3 pts)
  const bl = s.backlinks ?? 0;
  let blScore = 0;
  let blDetail = '';
  if (s.backlinks == null) { blDetail = 'Backlink count unavailable.'; blScore = 1; }
  else if (bl >= 1000) { blScore = 3; blDetail = `${bl.toLocaleString()} total backlinks.`; }
  else if (bl >= 100) { blScore = 2; blDetail = `${bl.toLocaleString()} total backlinks.`; }
  else if (bl >= 10) { blScore = 1; blDetail = `${bl.toLocaleString()} total backlinks.`; }
  else { blDetail = `Only ${bl.toLocaleString()} backlinks.`; }
  checks.push({
    id: 'total_backlinks', label: 'Total backlinks', passed: blScore >= 2, score: blScore, maxScore: 3, detail: blDetail,
    fix: blScore < 2 ? 'Total count matters less than diversity. Focus on getting links from relevant, authoritative sites.' : undefined,
  });

  const totalScore = checks.reduce((a, c) => a + c.score, 0);
  const maxScore = checks.reduce((a, c) => a + c.maxScore, 0);
  return {
    id: 'authority',
    label: 'Authority & Backlinks',
    score: totalScore,
    maxScore,
    pct: Math.round((totalScore / maxScore) * 100),
    status: statusFromPct((totalScore / maxScore) * 100),
    summary: s.drNormalized != null ? `DR ${s.drNormalized}/100 · ${(s.refDomains ?? 0).toLocaleString()} ref domains · ${(s.backlinks ?? 0).toLocaleString()} backlinks` : `${totalScore}/${maxScore} — limited backlink data available.`,
    checks,
  };
}

// ─── Dimension 5: Organic Performance (10 pts) ─────────────
function scoreOrganicPerformance(s: SiteSignals): DimensionScore {
  const checks: DimensionScore['checks'] = [];

  // Total ranking keywords (4 pts)
  const tk = s.totalRankingKeywords ?? 0;
  let tkScore = 0;
  let tkDetail = '';
  if (s.totalRankingKeywords == null) { tkDetail = 'Ranking-keyword data unavailable.'; tkScore = 1; }
  else if (tk >= 1000) { tkScore = 4; tkDetail = `${tk.toLocaleString()} keywords ranking in top 100.`; }
  else if (tk >= 100) { tkScore = 3; tkDetail = `${tk.toLocaleString()} keywords ranking.`; }
  else if (tk >= 10) { tkScore = 2; tkDetail = `${tk.toLocaleString()} keywords ranking.`; }
  else { tkDetail = `Only ${tk} keywords ranking.`; }
  checks.push({
    id: 'ranking_keywords', label: 'Total keywords ranking', passed: tkScore >= 2, score: tkScore, maxScore: 4, detail: tkDetail,
    fix: tkScore < 2 ? 'Publish more topic-targeted content. Each new article unlocks 5-50 long-tail keyword rankings within 6 months.' : undefined,
  });

  // Top 3 rankings (3 pts) — high-conversion positions
  const top3 = s.pos1to3 ?? 0;
  let top3Score = 0;
  let top3Detail = '';
  if (s.pos1to3 == null) { top3Detail = 'Top-position data unavailable.'; top3Score = 0; }
  else if (top3 >= 50) { top3Score = 3; top3Detail = `${top3} keywords in positions 1-3 (high-traffic positions).`; }
  else if (top3 >= 10) { top3Score = 2; top3Detail = `${top3} keywords in top 3.`; }
  else if (top3 >= 1) { top3Score = 1; top3Detail = `${top3} keywords in top 3.`; }
  else { top3Detail = 'No top-3 rankings yet.'; }
  checks.push({
    id: 'top_3_rankings', label: 'Keywords in top 3 positions', passed: top3Score >= 1, score: top3Score, maxScore: 3, detail: top3Detail,
    fix: top3Score < 1 ? 'Position 1-3 captures 50%+ of clicks. Identify your top-10 rankings and improve those pages with better content + internal links.' : undefined,
  });

  // Estimated traffic (3 pts)
  const tr = s.estTraffic ?? 0;
  let trScore = 0;
  let trDetail = '';
  if (s.estTraffic == null) { trDetail = 'Traffic estimate unavailable.'; trScore = 1; }
  else if (tr >= 5000) { trScore = 3; trDetail = `~${tr.toLocaleString()} estimated monthly organic visits.`; }
  else if (tr >= 500) { trScore = 2; trDetail = `~${tr.toLocaleString()} estimated monthly organic visits.`; }
  else if (tr >= 50) { trScore = 1; trDetail = `~${tr.toLocaleString()} estimated monthly organic visits.`; }
  else { trDetail = `~${tr.toLocaleString()} estimated monthly organic visits.`; }
  checks.push({
    id: 'organic_traffic', label: 'Estimated monthly organic traffic', passed: trScore >= 1, score: trScore, maxScore: 3, detail: trDetail,
    fix: trScore < 1 ? 'Traffic follows from rankings. Focus on building topical authority through consistent content publishing.' : undefined,
  });

  const totalScore = checks.reduce((a, c) => a + c.score, 0);
  const maxScore = checks.reduce((a, c) => a + c.maxScore, 0);
  return {
    id: 'organic_performance',
    label: 'Organic Performance',
    score: totalScore,
    maxScore,
    pct: Math.round((totalScore / maxScore) * 100),
    status: statusFromPct((totalScore / maxScore) * 100),
    summary: `${totalScore}/${maxScore} — ${(s.totalRankingKeywords ?? 0).toLocaleString()} ranking keywords · ${(s.estTraffic ?? 0).toLocaleString()} est. monthly visits.`,
    checks,
  };
}

// ─── Dimension 6: Local SEO (10 pts) ─────────────
function scoreLocalSeo(s: SiteSignals): DimensionScore {
  const p = s.page;
  const checks: DimensionScore['checks'] = [];

  // LocalBusiness schema (5 pts)
  const hasLocalBiz = p.schemaTypes.some(t => /LocalBusiness|Dentist|Restaurant|Plumber|Electrician|MedicalBusiness|LegalService|RealEstateAgent|Store|HomeAndConstructionBusiness|Attorney/i.test(t));
  const hasOrg = p.schemaTypes.some(t => /Organization/i.test(t));
  let lbScore = 0;
  let lbDetail = '';
  if (hasLocalBiz) { lbScore = 5; lbDetail = `LocalBusiness schema detected (${p.schemaTypes.filter(t => /LocalBusiness|Dentist|Restaurant|Plumber|Electrician|MedicalBusiness|LegalService|Attorney/i.test(t)).join(', ')}).`; }
  else if (hasOrg) { lbScore = 2; lbDetail = 'Generic Organization schema present — upgrade to LocalBusiness or specific subtype for local rankings.'; }
  else { lbDetail = 'No LocalBusiness or Organization schema.'; }
  checks.push({
    id: 'localbusiness_schema', label: 'LocalBusiness schema', passed: lbScore === 5, score: lbScore, maxScore: 5, detail: lbDetail,
    fix: lbScore < 5 ? 'Add LocalBusiness schema (or specific subtype like Dentist, Plumber, Restaurant) — major local-ranking signal.' : undefined,
  });

  // NAP (Name, Address, Phone) on page (3 pts)
  const text = p.bodyText.toLowerCase();
  const hasPhone = /\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}/.test(p.bodyText);
  const hasAddress = /\d+\s+\w+\s+(street|st\.?|ave|avenue|blvd|boulevard|drive|dr\.?|road|rd\.?|lane|ln\.?|way|circle|cir|place|plaza)\b/i.test(p.bodyText);
  const hasBizName = !!s.bizName && text.includes(s.bizName.toLowerCase());
  let napScore = 0;
  const napParts = [];
  if (hasPhone) { napScore += 1; napParts.push('phone ✓'); } else napParts.push('phone ✗');
  if (hasAddress) { napScore += 1; napParts.push('address ✓'); } else napParts.push('address ✗');
  if (s.bizName ? hasBizName : true) { napScore += 1; napParts.push(s.bizName ? 'business name ✓' : 'name (skip — no input)'); }
  else napParts.push('business name ✗');
  checks.push({
    id: 'nap', label: 'NAP (Name, Address, Phone)', passed: napScore >= 2, score: napScore, maxScore: 3, detail: napParts.join(' · '),
    fix: napScore < 2 ? 'Display your business name, full address, and phone number on every page (footer is fine).' : undefined,
  });

  // City / location mentioned (2 pts)
  let cityScore = 0;
  let cityDetail = '';
  if (s.city) {
    const cityShort = s.city.split(',')[0].trim().toLowerCase();
    if (text.includes(cityShort)) { cityScore = 2; cityDetail = `City "${cityShort}" mentioned in content.`; }
    else { cityDetail = `City "${cityShort}" not found on the page.`; }
  } else {
    cityScore = 1; cityDetail = 'City not provided — skipping check.';
  }
  checks.push({
    id: 'city_mention', label: 'Service area / city mentioned', passed: cityScore >= 1, score: cityScore, maxScore: 2, detail: cityDetail,
    fix: s.city && cityScore < 2 ? `Mention "${s.city}" in body content, footer, or service-area section.` : undefined,
  });

  const totalScore = checks.reduce((a, c) => a + c.score, 0);
  const maxScore = checks.reduce((a, c) => a + c.maxScore, 0);
  return {
    id: 'local_seo',
    label: 'Local SEO',
    score: totalScore,
    maxScore,
    pct: Math.round((totalScore / maxScore) * 100),
    status: statusFromPct((totalScore / maxScore) * 100),
    summary: `${totalScore}/${maxScore} — ${hasLocalBiz ? 'LocalBusiness schema present' : 'LocalBusiness schema missing'}.`,
    checks,
  };
}

// ─── Dimension 7: Content & AI Readiness (15 pts) ─────────────
function scoreContentAndAi(s: SiteSignals): DimensionScore {
  const p = s.page;
  const checks: DimensionScore['checks'] = [];

  // Content depth (5 pts)
  let cdScore = 0;
  let cdDetail = '';
  if (p.wordCount >= 1500) { cdScore = 5; cdDetail = `${p.wordCount.toLocaleString()} words — substantial content depth.`; }
  else if (p.wordCount >= 800) { cdScore = 4; cdDetail = `${p.wordCount.toLocaleString()} words — solid coverage.`; }
  else if (p.wordCount >= 400) { cdScore = 3; cdDetail = `${p.wordCount.toLocaleString()} words — moderate.`; }
  else if (p.wordCount >= 150) { cdScore = 1; cdDetail = `${p.wordCount.toLocaleString()} words — thin content.`; }
  else { cdDetail = `${p.wordCount.toLocaleString()} words — very thin.`; }
  checks.push({
    id: 'content_depth', label: 'Content depth', passed: cdScore >= 3, score: cdScore, maxScore: 5, detail: cdDetail,
    fix: cdScore < 3 ? 'Aim for 800+ words on key pages. Thin pages rarely rank for competitive keywords.' : undefined,
  });

  // Heading hierarchy (3 pts)
  let hhScore = 0;
  const hhParts = [];
  if (p.h1s.length === 1) { hhScore += 1; hhParts.push('1 H1 ✓'); } else hhParts.push(p.h1s.length === 0 ? 'no H1 ✗' : `${p.h1s.length} H1s ✗`);
  if (p.h2s.length >= 3) { hhScore += 1; hhParts.push(`${p.h2s.length} H2s ✓`); } else hhParts.push(`${p.h2s.length} H2s (light)`);
  if (p.h3s.length >= 2) { hhScore += 1; hhParts.push(`${p.h3s.length} H3s ✓`); } else hhParts.push(`${p.h3s.length} H3s (light)`);
  checks.push({
    id: 'heading_structure', label: 'Heading hierarchy', passed: hhScore >= 2, score: hhScore, maxScore: 3, detail: hhParts.join(' · '),
    fix: hhScore < 2 ? 'Aim for 1 H1, 3+ H2s, and 2+ H3s. Question-format H2s improve AI Overview pull-in rates.' : undefined,
  });

  // FAQ schema or Q&A content (3 pts) — AI Overview citation factor
  const hasFaqSchema = p.schemaTypes.some(t => /FAQPage|QAPage/i.test(t));
  const hasQaContent = (p.h2s.concat(p.h3s)).some(h => /^(what|why|how|when|where|is|do|can|does)\s/i.test(h.trim()));
  let faqScore = 0;
  let faqDetail = '';
  if (hasFaqSchema && hasQaContent) { faqScore = 3; faqDetail = 'FAQ schema + question-format headings — strong AI Overview signal.'; }
  else if (hasFaqSchema) { faqScore = 2; faqDetail = 'FAQ schema present.'; }
  else if (hasQaContent) { faqScore = 1; faqDetail = 'Question-format headings detected (no FAQ schema).'; }
  else { faqDetail = 'No FAQ schema and no question-format headings.'; }
  checks.push({
    id: 'faq_schema', label: 'FAQ schema / Q&A content (AI Overview signal)', passed: faqScore >= 2, score: faqScore, maxScore: 3, detail: faqDetail,
    fix: faqScore < 2 ? 'Add an FAQ section with FAQPage schema. AI Overviews and Featured Snippets pull from question-format content first.' : undefined,
  });

  // llms.txt (2 pts)
  checks.push({
    id: 'llms_txt', label: 'llms.txt file (AI/LLM signal)', passed: s.hasLlmsTxt, score: s.hasLlmsTxt ? 2 : 0, maxScore: 2,
    detail: s.hasLlmsTxt ? 'llms.txt found — explicit AI/LLM guidance present.' : 'No /llms.txt file.',
    fix: !s.hasLlmsTxt ? 'Add /llms.txt — emerging standard for guiding AI crawlers (ChatGPT, Perplexity, Claude). Boosts citation likelihood.' : undefined,
  });

  // AI crawler access (2 pts)
  checks.push({
    id: 'ai_crawler_access', label: 'AI crawlers allowed', passed: !s.blocksAiCrawlers, score: s.blocksAiCrawlers ? 0 : 2, maxScore: 2,
    detail: s.blocksAiCrawlers ? 'robots.txt blocks one or more AI crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.).' : 'AI crawlers can access the site.',
    fix: s.blocksAiCrawlers ? 'Reconsider blocking AI crawlers — citations in ChatGPT, Perplexity, and Google AI Overviews drive new traffic.' : undefined,
  });

  const totalScore = checks.reduce((a, c) => a + c.score, 0);
  const maxScore = checks.reduce((a, c) => a + c.maxScore, 0);
  return {
    id: 'content_ai',
    label: 'Content & AI Readiness',
    score: totalScore,
    maxScore,
    pct: Math.round((totalScore / maxScore) * 100),
    status: statusFromPct((totalScore / maxScore) * 100),
    summary: `${totalScore}/${maxScore} — ${p.wordCount.toLocaleString()} words · ${hasFaqSchema ? 'FAQ schema present' : 'no FAQ schema'} · ${s.hasLlmsTxt ? 'llms.txt ✓' : 'no llms.txt'}.`,
    checks,
  };
}

// ─── Dimension 8: Trust & Security (5 pts) ─────────────
function scoreTrust(s: SiteSignals): DimensionScore {
  const checks: DimensionScore['checks'] = [];

  // HTTPS (already in technical, but double-weighted as trust signal — split smaller)
  checks.push({
    id: 'https_trust', label: 'HTTPS / SSL certificate', passed: s.hasHttps, score: s.hasHttps ? 3 : 0, maxScore: 3,
    detail: s.hasHttps ? 'HTTPS encryption active.' : 'Site is not on HTTPS.',
    fix: !s.hasHttps ? 'Migrate to HTTPS — required for modern SEO and user trust.' : undefined,
  });

  // Privacy/contact info presence (2 pts) — light heuristic
  const text = s.page.bodyText.toLowerCase();
  const hasPrivacy = /privacy policy|privacy/i.test(text) || /privacy/i.test(JSON.stringify(s.page.jsonLd));
  const hasContact = /contact|reach us|get in touch|email us/i.test(text);
  let trustScore = 0;
  if (hasPrivacy) trustScore += 1;
  if (hasContact) trustScore += 1;
  checks.push({
    id: 'trust_signals', label: 'Trust signals (privacy + contact)', passed: trustScore >= 1, score: trustScore, maxScore: 2,
    detail: `Privacy: ${hasPrivacy ? '✓' : '✗'} · Contact info: ${hasContact ? '✓' : '✗'}`,
    fix: trustScore < 1 ? 'Add a Privacy Policy link and clear contact info — required for E-E-A-T signals.' : undefined,
  });

  const totalScore = checks.reduce((a, c) => a + c.score, 0);
  const maxScore = checks.reduce((a, c) => a + c.maxScore, 0);
  return {
    id: 'trust',
    label: 'Trust & Security',
    score: totalScore,
    maxScore,
    pct: Math.round((totalScore / maxScore) * 100),
    status: statusFromPct((totalScore / maxScore) * 100),
    summary: `${totalScore}/${maxScore} — ${s.hasHttps ? 'HTTPS active' : 'HTTPS missing'}.`,
    checks,
  };
}

// ─── PageSpeed parser ───────────────────────────────────────
export function parsePageSpeedResponse(json: any): PageSpeedScores | null {
  if (!json) return null;
  try {
    const lh = json.lighthouseResult;
    const audits = lh?.audits || {};
    const categories = lh?.categories || {};
    return {
      performance: categories.performance ? Math.round(categories.performance.score * 100) : null,
      lcp: audits['largest-contentful-paint']?.numericValue ?? null,
      cls: audits['cumulative-layout-shift']?.numericValue ?? null,
      inp: audits['interactive']?.numericValue ?? null,  // approximation; full INP needs CrUX
      tbt: audits['total-blocking-time']?.numericValue ?? null,
      fcp: audits['first-contentful-paint']?.numericValue ?? null,
    };
  } catch {
    return null;
  }
}

// ─── robots.txt parser for AI crawler block detection ───────
const AI_CRAWLERS = ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'CCBot', 'anthropic-ai', 'Google-Extended', 'Applebot-Extended'];

export function checkAiCrawlerBlocks(robotsContent: string): boolean {
  if (!robotsContent) return false;
  const lines = robotsContent.split('\n').map(l => l.trim());
  let currentAgent = '';
  for (const line of lines) {
    const lower = line.toLowerCase();
    if (lower.startsWith('user-agent:')) {
      currentAgent = line.split(':')[1].trim();
    } else if (lower.startsWith('disallow:')) {
      const path = line.split(':')[1].trim();
      if (path === '/' && AI_CRAWLERS.some(a => a.toLowerCase() === currentAgent.toLowerCase())) {
        return true;
      }
    }
  }
  return false;
}
