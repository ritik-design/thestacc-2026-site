// src/lib/tools/on-page-seo-checker.ts
// Deterministic on-page SEO parser + scorer (no LLM needed).
// Reusable: API endpoint calls these functions, then layers Kimi insights on top.

export interface ParsedPage {
  title: string;
  metaDescription: string;
  canonical: string;
  robotsMeta: string;
  h1s: string[];
  h2s: string[];
  h3s: string[];
  images: { src: string; alt: string }[];
  internalLinkCount: number;
  externalLinkCount: number;
  bodyText: string;
  wordCount: number;
  jsonLd: any[];
  schemaTypes: string[];
  ogImage: string;
  hasViewport: boolean;
  htmlLang: string;
  urlSlug: string;
}

/** Parse HTML server-side using regex (no DOM). */
export function parseHTML(rawHtml: string, baseUrl: string): ParsedPage {
  const html = rawHtml || '';
  let originHost = '';
  let urlSlug = '';
  try {
    const u = new URL(baseUrl);
    originHost = u.hostname;
    urlSlug = (u.pathname + u.search).toLowerCase();
  } catch {}

  // Title
  const title = (html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1] || '').replace(/\s+/g, ' ').trim();

  // Meta description
  const metaDescMatch = html.match(/<meta[^>]*name=["']description["'][^>]*>/i)
    || html.match(/<meta[^>]*property=["']og:description["'][^>]*>/i);
  let metaDescription = '';
  if (metaDescMatch) {
    const cm = metaDescMatch[0].match(/content=["']([^"]*)["']/i);
    metaDescription = cm ? cm[1].trim() : '';
  }

  // Canonical
  const canonicalMatch = html.match(/<link[^>]*rel=["']canonical["'][^>]*>/i);
  let canonical = '';
  if (canonicalMatch) {
    const cm = canonicalMatch[0].match(/href=["']([^"]*)["']/i);
    canonical = cm ? cm[1] : '';
  }

  // Robots meta
  const robotsMatch = html.match(/<meta[^>]*name=["']robots["'][^>]*>/i);
  let robotsMeta = '';
  if (robotsMatch) {
    const cm = robotsMatch[0].match(/content=["']([^"]*)["']/i);
    robotsMeta = cm ? cm[1].toLowerCase() : '';
  }

  // OG image
  const ogImageMatch = html.match(/<meta[^>]*property=["']og:image["'][^>]*>/i);
  let ogImage = '';
  if (ogImageMatch) {
    const cm = ogImageMatch[0].match(/content=["']([^"]*)["']/i);
    ogImage = cm ? cm[1] : '';
  }

  // Viewport
  const hasViewport = /<meta[^>]*name=["']viewport["'][^>]*>/i.test(html);

  // HTML lang
  const langMatch = html.match(/<html[^>]*lang=["']([^"]*)["']/i);
  const htmlLang = langMatch ? langMatch[1] : '';

  // H1, H2, H3 — strip tags inside
  const h1s = extractHeadings(html, 'h1');
  const h2s = extractHeadings(html, 'h2');
  const h3s = extractHeadings(html, 'h3');

  // Images
  const images: { src: string; alt: string }[] = [];
  const imgRe = /<img[^>]*>/gi;
  let m: RegExpExecArray | null;
  while ((m = imgRe.exec(html)) !== null) {
    const srcMatch = m[0].match(/(?:^|\s)src=["']([^"]*)["']/i);
    const altMatch = m[0].match(/(?:^|\s)alt=["']([^"]*)["']/i);
    images.push({ src: srcMatch ? srcMatch[1] : '', alt: altMatch ? altMatch[1] : '' });
  }

  // Links — internal vs external
  let internalLinkCount = 0;
  let externalLinkCount = 0;
  const linkRe = /<a[^>]*href=["']([^"]*)["'][^>]*>/gi;
  while ((m = linkRe.exec(html)) !== null) {
    const href = m[1];
    if (!href || href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) continue;
    try {
      const linkUrl = new URL(href, baseUrl);
      if (linkUrl.hostname === originHost) internalLinkCount++;
      else if (linkUrl.protocol.startsWith('http')) externalLinkCount++;
    } catch { /* invalid URL */ }
  }

  // Body text — strip script, style, nav, footer tags first; then strip all tags.
  let bodyText = html
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, ' ')
    .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, ' ')
    .replace(/<noscript\b[^<]*(?:(?!<\/noscript>)<[^<]*)*<\/noscript>/gi, ' ')
    .replace(/<svg\b[^<]*(?:(?!<\/svg>)<[^<]*)*<\/svg>/gi, ' ')
    .replace(/<header\b[^<]*(?:(?!<\/header>)<[^<]*)*<\/header>/gi, ' ')
    .replace(/<footer\b[^<]*(?:(?!<\/footer>)<[^<]*)*<\/footer>/gi, ' ')
    .replace(/<nav\b[^<]*(?:(?!<\/nav>)<[^<]*)*<\/nav>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"')
    .replace(/\s+/g, ' ')
    .trim();

  const wordCount = bodyText.split(/\s+/).filter(w => w.length > 1).length;

  // JSON-LD
  const jsonLd: any[] = [];
  const schemaTypes = new Set<string>();
  const jlRe = /<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  while ((m = jlRe.exec(html)) !== null) {
    try {
      const parsed = JSON.parse(m[1].trim());
      jsonLd.push(parsed);
      collectSchemaTypes(parsed, schemaTypes);
    } catch { /* skip */ }
  }

  return {
    title,
    metaDescription,
    canonical,
    robotsMeta,
    h1s,
    h2s,
    h3s,
    images,
    internalLinkCount,
    externalLinkCount,
    bodyText,
    wordCount,
    jsonLd,
    schemaTypes: Array.from(schemaTypes),
    ogImage,
    hasViewport,
    htmlLang,
    urlSlug,
  };
}

function extractHeadings(html: string, tag: string): string[] {
  const re = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\/${tag}>`, 'gi');
  const out: string[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(html)) !== null) {
    const stripped = m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    if (stripped) out.push(stripped);
  }
  return out;
}

function collectSchemaTypes(node: any, out: Set<string>): void {
  if (!node || typeof node !== 'object') return;
  if (Array.isArray(node)) {
    node.forEach(n => collectSchemaTypes(n, out));
    return;
  }
  const t = node['@type'];
  if (typeof t === 'string') out.add(t);
  else if (Array.isArray(t)) t.forEach(x => typeof x === 'string' && out.add(x));
  for (const k of Object.keys(node)) {
    if (k.startsWith('@')) continue;
    collectSchemaTypes(node[k], out);
  }
}

// ─── Keyword matching helpers ──────────────────────────────────

export interface KeywordMatch {
  exact: boolean;
  partial: boolean;
  position: number; // -1 if not found
}

export function matchKeyword(haystack: string, keyword: string): KeywordMatch {
  if (!haystack || !keyword) return { exact: false, partial: false, position: -1 };
  const lowerH = haystack.toLowerCase();
  const lowerK = keyword.toLowerCase().trim();
  const exactPos = lowerH.indexOf(lowerK);
  if (exactPos >= 0) return { exact: true, partial: true, position: exactPos };
  // Partial: every word from keyword appears somewhere in haystack
  const words = lowerK.split(/\s+/).filter(w => w.length > 2);
  if (words.length === 0) return { exact: false, partial: false, position: -1 };
  const allFound = words.every(w => lowerH.includes(w));
  if (allFound) {
    const firstWord = words[0];
    return { exact: false, partial: true, position: lowerH.indexOf(firstWord) };
  }
  return { exact: false, partial: false, position: -1 };
}

export function calculateKeywordDensity(bodyText: string, keyword: string): number {
  if (!bodyText || !keyword) return 0;
  const totalWords = bodyText.split(/\s+/).filter(w => w.length > 1).length || 1;
  const lowerB = bodyText.toLowerCase();
  const lowerK = keyword.toLowerCase().trim();
  const escaped = lowerK.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const matches = lowerB.match(new RegExp(`\\b${escaped}\\b`, 'g'));
  const exactCount = matches ? matches.length : 0;
  // Each phrase match counts as keyword.split(' ').length words
  const phraseWords = lowerK.split(/\s+/).filter(w => w.length > 0).length;
  return (exactCount * phraseWords) / totalWords * 100;
}

// ─── 15-rule on-page scorer ────────────────────────────────────

export interface CheckResult {
  id: string;
  group: 'placement' | 'content' | 'technical';
  label: string;
  passed: boolean;
  score: number;        // 0-points awarded
  maxScore: number;
  detail: string;       // What was checked / found
  fix?: string;         // What to do if failed
}

export interface ScoredReport {
  overall: { score: number; maxScore: number; pct: number; grade: 'A' | 'B' | 'C' | 'D' | 'F' };
  byGroup: { placement: { score: number; max: number }; content: { score: number; max: number }; technical: { score: number; max: number } };
  checks: CheckResult[];
  keywordPlacementMap: Array<{ location: string; status: 'found' | 'partial' | 'missing'; preview?: string }>;
  topIssues: CheckResult[];
  density: number;
  competitorWordCountAvg: number; // populated by API endpoint
  yourWordCount: number;
}

export function scoreOnPage(page: ParsedPage, keyword: string, baseUrl: string, competitorAvgWordCount = 0): ScoredReport {
  const checks: CheckResult[] = [];
  const lowerK = keyword.toLowerCase().trim();
  const firstParagraph = (page.bodyText || '').slice(0, 600);

  // ─── PLACEMENT (8 checks, 50 pts total) ───
  // 1. Title tag — keyword present (10 pts)
  const titleMatch = matchKeyword(page.title, keyword);
  checks.push({
    id: 'title_keyword',
    group: 'placement',
    label: 'Keyword in title tag',
    passed: titleMatch.exact,
    score: titleMatch.exact ? 10 : (titleMatch.partial ? 5 : 0),
    maxScore: 10,
    detail: page.title ? `Title: "${page.title}"` : 'Title tag is missing.',
    fix: !titleMatch.exact
      ? `Add "${keyword}" to your title tag, ideally near the beginning. Keep total length 50-60 chars.`
      : undefined,
  });

  // 2. H1 — keyword present (8 pts)
  const h1 = page.h1s[0] || '';
  const h1Match = matchKeyword(h1, keyword);
  checks.push({
    id: 'h1_keyword',
    group: 'placement',
    label: 'Keyword in H1 heading',
    passed: page.h1s.length === 1 && h1Match.exact,
    score: page.h1s.length !== 1 ? 0 : (h1Match.exact ? 8 : (h1Match.partial ? 4 : 0)),
    maxScore: 8,
    detail: page.h1s.length === 0
      ? 'No H1 heading on this page.'
      : page.h1s.length > 1
        ? `Found ${page.h1s.length} H1 headings — should be exactly 1.`
        : `H1: "${h1}"`,
    fix: page.h1s.length === 0
      ? `Add an <h1> heading containing "${keyword}".`
      : page.h1s.length > 1
        ? `Use only one H1 per page. Convert extra H1s to H2 or H3.`
        : !h1Match.exact
          ? `Add "${keyword}" to your H1 heading.`
          : undefined,
  });

  // 3. Meta description — keyword present (6 pts)
  const mdMatch = matchKeyword(page.metaDescription, keyword);
  checks.push({
    id: 'meta_keyword',
    group: 'placement',
    label: 'Keyword in meta description',
    passed: !!page.metaDescription && mdMatch.exact,
    score: !page.metaDescription ? 0 : (mdMatch.exact ? 6 : (mdMatch.partial ? 3 : 0)),
    maxScore: 6,
    detail: page.metaDescription
      ? `Meta description: "${page.metaDescription.slice(0, 120)}${page.metaDescription.length > 120 ? '…' : ''}"`
      : 'No meta description on this page.',
    fix: !page.metaDescription
      ? `Add a meta description (150-160 chars) that includes "${keyword}" and a clear value proposition.`
      : !mdMatch.exact
        ? `Rewrite the meta description to include "${keyword}".`
        : undefined,
  });

  // 4. First 100 words — keyword present (6 pts)
  const first100 = page.bodyText.split(/\s+/).slice(0, 100).join(' ');
  const f100Match = matchKeyword(first100, keyword);
  checks.push({
    id: 'first_100_words',
    group: 'placement',
    label: 'Keyword in first 100 words',
    passed: f100Match.exact,
    score: f100Match.exact ? 6 : (f100Match.partial ? 3 : 0),
    maxScore: 6,
    detail: f100Match.exact
      ? 'Keyword appears in opening content.'
      : 'Keyword does not appear in the first 100 words.',
    fix: !f100Match.exact
      ? `Mention "${keyword}" naturally in your opening paragraph — within the first 100 words.`
      : undefined,
  });

  // 5. Subheadings (H2/H3) — keyword present in at least one (5 pts)
  const subheadings = [...page.h2s, ...page.h3s];
  const subheadingMatch = subheadings.some(h => matchKeyword(h, keyword).exact);
  const subheadingPartial = !subheadingMatch && subheadings.some(h => matchKeyword(h, keyword).partial);
  checks.push({
    id: 'subheadings',
    group: 'placement',
    label: 'Keyword in subheadings',
    passed: subheadingMatch,
    score: subheadingMatch ? 5 : (subheadingPartial ? 2 : 0),
    maxScore: 5,
    detail: subheadings.length
      ? `${subheadings.length} subheadings on page; ${subheadingMatch ? 'at least one' : 'none'} contain the keyword.`
      : 'No H2 or H3 subheadings.',
    fix: !subheadingMatch
      ? `Add at least one H2 or H3 that includes "${keyword}" or a close variation.`
      : undefined,
  });

  // 6. URL slug — keyword present (5 pts)
  const slugMatch = matchKeyword(page.urlSlug.replace(/[/-]/g, ' '), keyword);
  checks.push({
    id: 'url_slug',
    group: 'placement',
    label: 'Keyword in URL slug',
    passed: slugMatch.exact || slugMatch.partial,
    score: slugMatch.exact ? 5 : (slugMatch.partial ? 3 : 0),
    maxScore: 5,
    detail: page.urlSlug ? `Slug: ${page.urlSlug}` : 'Root URL.',
    fix: !slugMatch.exact && !slugMatch.partial
      ? `Consider a URL slug containing "${keyword.replace(/\s+/g, '-')}". Note: changing existing URLs needs 301 redirects.`
      : undefined,
  });

  // 7. Image alt text — keyword present in at least one (5 pts)
  const altMatch = page.images.some(img => matchKeyword(img.alt, keyword).exact);
  const altPartial = !altMatch && page.images.some(img => matchKeyword(img.alt, keyword).partial);
  checks.push({
    id: 'image_alt_keyword',
    group: 'placement',
    label: 'Keyword in image alt text',
    passed: altMatch,
    score: altMatch ? 5 : (altPartial ? 2 : 0),
    maxScore: 5,
    detail: page.images.length === 0
      ? 'No images on the page.'
      : `${page.images.length} image${page.images.length === 1 ? '' : 's'}; ${altMatch ? 'at least one alt text contains the keyword' : 'no alt text contains the keyword'}.`,
    fix: !altMatch && page.images.length > 0
      ? `Add "${keyword}" to the alt text of your most relevant image (only where natural).`
      : undefined,
  });

  // 8. Keyword density (5 pts) — 0.5-3% sweet spot
  const density = calculateKeywordDensity(page.bodyText, keyword);
  let densityScore = 0;
  let densityDetail = '';
  if (density >= 0.5 && density <= 3) {
    densityScore = 5;
    densityDetail = `Density: ${density.toFixed(2)}% (in optimal 0.5-3% range)`;
  } else if (density > 0 && density < 0.5) {
    densityScore = 2;
    densityDetail = `Density: ${density.toFixed(2)}% (too low — under 0.5%)`;
  } else if (density > 3 && density < 5) {
    densityScore = 2;
    densityDetail = `Density: ${density.toFixed(2)}% (slightly high — risk of stuffing)`;
  } else if (density >= 5) {
    densityScore = 0;
    densityDetail = `Density: ${density.toFixed(2)}% (TOO HIGH — risk of keyword stuffing penalty)`;
  } else {
    densityScore = 0;
    densityDetail = 'Keyword does not appear in body content.';
  }
  checks.push({
    id: 'keyword_density',
    group: 'placement',
    label: 'Keyword density',
    passed: densityScore >= 3,
    score: densityScore,
    maxScore: 5,
    detail: densityDetail,
    fix: density < 0.5
      ? `Use "${keyword}" 1-2 more times naturally in your content.`
      : density >= 5
        ? `Reduce keyword frequency. Replace some instances with synonyms or related phrases.`
        : undefined,
  });

  // ─── CONTENT QUALITY (4 checks, 30 pts) ───

  // 9. Word count (10 pts) — competitor-aware if data available
  let wcScore = 0;
  let wcDetail = '';
  let wcFix: string | undefined;
  const target = competitorAvgWordCount > 0 ? competitorAvgWordCount : 800;
  if (page.wordCount >= target) {
    wcScore = 10;
    wcDetail = `Word count: ${page.wordCount} (above target of ~${target})`;
  } else if (page.wordCount >= target * 0.7) {
    wcScore = 7;
    wcDetail = `Word count: ${page.wordCount} (close to target of ~${target})`;
    wcFix = `Add ${target - page.wordCount} more words to match the depth of competing pages.`;
  } else if (page.wordCount >= 300) {
    wcScore = 4;
    wcDetail = `Word count: ${page.wordCount} (below target of ${target})`;
    wcFix = `Top-ranking pages average ${target} words. Expand content to ${Math.round(target * 0.8)}+ words.`;
  } else {
    wcScore = 0;
    wcDetail = `Word count: ${page.wordCount} (very thin — under 300 words)`;
    wcFix = `Pages under 300 words rarely rank. Expand to at least ${Math.round(target * 0.8)} words covering all relevant subtopics.`;
  }
  checks.push({
    id: 'word_count',
    group: 'content',
    label: 'Content length',
    passed: page.wordCount >= 600,
    score: wcScore,
    maxScore: 10,
    detail: wcDetail,
    fix: wcFix,
  });

  // 10. Internal links (6 pts)
  let ilScore = 0;
  let ilDetail = `${page.internalLinkCount} internal link${page.internalLinkCount === 1 ? '' : 's'}.`;
  if (page.internalLinkCount >= 5) ilScore = 6;
  else if (page.internalLinkCount >= 3) ilScore = 4;
  else if (page.internalLinkCount >= 1) ilScore = 2;
  checks.push({
    id: 'internal_links',
    group: 'content',
    label: 'Internal links',
    passed: page.internalLinkCount >= 3,
    score: ilScore,
    maxScore: 6,
    detail: ilDetail,
    fix: page.internalLinkCount < 3
      ? `Add at least 3-5 internal links to related pages on your site (use descriptive anchor text).`
      : undefined,
  });

  // 11. External links (4 pts)
  let elScore = 0;
  if (page.externalLinkCount >= 2) elScore = 4;
  else if (page.externalLinkCount >= 1) elScore = 2;
  checks.push({
    id: 'external_links',
    group: 'content',
    label: 'External links to authoritative sources',
    passed: page.externalLinkCount >= 1,
    score: elScore,
    maxScore: 4,
    detail: `${page.externalLinkCount} external link${page.externalLinkCount === 1 ? '' : 's'}.`,
    fix: page.externalLinkCount === 0
      ? `Cite at least 1-2 authoritative sources (research, .gov, .edu, industry leaders) — improves E-E-A-T signals.`
      : undefined,
  });

  // 12. Heading structure (10 pts)
  let hsScore = 0;
  const hsParts: string[] = [];
  if (page.h1s.length === 1) { hsScore += 4; hsParts.push('1 H1 ✓'); }
  else hsParts.push(page.h1s.length === 0 ? 'No H1 ✗' : `${page.h1s.length} H1s ✗`);
  if (page.h2s.length >= 3) { hsScore += 4; hsParts.push(`${page.h2s.length} H2s ✓`); }
  else if (page.h2s.length >= 1) { hsScore += 2; hsParts.push(`${page.h2s.length} H2s (light)`); }
  else hsParts.push('0 H2s ✗');
  if (page.h3s.length >= 2) { hsScore += 2; hsParts.push(`${page.h3s.length} H3s ✓`); }
  else if (page.h3s.length >= 1) { hsScore += 1; hsParts.push(`${page.h3s.length} H3 (light)`); }
  checks.push({
    id: 'heading_structure',
    group: 'content',
    label: 'Heading structure',
    passed: hsScore >= 7,
    score: hsScore,
    maxScore: 10,
    detail: hsParts.join(' · '),
    fix: hsScore < 7
      ? `Aim for 1 H1, 3+ H2s for major sections, and 2+ H3s for sub-points. Helps both SEO and readability.`
      : undefined,
  });

  // ─── TECHNICAL (3 checks, 20 pts) ───

  // 13. Image optimization (alt coverage) (8 pts)
  const imagesWithAlt = page.images.filter(img => img.alt && img.alt.trim().length > 0).length;
  const altPct = page.images.length === 0 ? 0 : imagesWithAlt / page.images.length;
  let imgScore = 0;
  let imgDetail = '';
  if (page.images.length === 0) {
    imgScore = 4;
    imgDetail = 'No images on the page.';
  } else if (altPct >= 0.95) {
    imgScore = 8;
    imgDetail = `${imagesWithAlt} of ${page.images.length} images have alt text.`;
  } else if (altPct >= 0.6) {
    imgScore = 5;
    imgDetail = `${imagesWithAlt} of ${page.images.length} images have alt text (${Math.round(altPct * 100)}%).`;
  } else {
    imgScore = 0;
    imgDetail = `Only ${imagesWithAlt} of ${page.images.length} images have alt text.`;
  }
  checks.push({
    id: 'image_alt_coverage',
    group: 'technical',
    label: 'Image alt text coverage',
    passed: imgScore >= 5,
    score: imgScore,
    maxScore: 8,
    detail: imgDetail,
    fix: page.images.length > 0 && altPct < 0.95
      ? `Add descriptive alt text to all ${page.images.length - imagesWithAlt} images without it. Required for accessibility + image search rankings.`
      : undefined,
  });

  // 14. Schema markup (7 pts)
  const hasSchema = page.schemaTypes.length > 0;
  const hasFaqSchema = page.schemaTypes.some(t => /FAQ/i.test(t));
  const hasArticleSchema = page.schemaTypes.some(t => /(Article|BlogPosting|NewsArticle)/i.test(t));
  const hasLocalBizSchema = page.schemaTypes.some(t => /LocalBusiness|Organization/i.test(t));
  let schemaScore = 0;
  if (hasSchema) schemaScore += 3;
  if (hasFaqSchema || hasArticleSchema || hasLocalBizSchema) schemaScore += 4;
  checks.push({
    id: 'schema_markup',
    group: 'technical',
    label: 'Schema.org structured data',
    passed: hasSchema,
    score: schemaScore,
    maxScore: 7,
    detail: hasSchema ? `Schema types found: ${page.schemaTypes.slice(0, 5).join(', ')}` : 'No schema markup detected.',
    fix: !hasSchema
      ? `Add JSON-LD structured data (Article, FAQ, or LocalBusiness) — try our schema markup generator.`
      : !hasFaqSchema && !hasArticleSchema && !hasLocalBizSchema
        ? `Add a content-specific schema type (FAQPage, Article, or LocalBusiness) — generic schema doesn't trigger rich results.`
        : undefined,
  });

  // 15. Mobile + canonical + indexable (5 pts)
  let techMisc = 0;
  const techParts: string[] = [];
  if (page.hasViewport) { techMisc += 2; techParts.push('viewport ✓'); }
  else techParts.push('viewport ✗');
  if (page.canonical) { techMisc += 2; techParts.push('canonical ✓'); }
  else techParts.push('canonical ✗');
  const isNoindex = /noindex/.test(page.robotsMeta);
  if (!isNoindex) { techMisc += 1; techParts.push('indexable ✓'); }
  else techParts.push('NOINDEX ✗ (page blocked from search)');
  checks.push({
    id: 'technical_misc',
    group: 'technical',
    label: 'Mobile viewport, canonical, indexable',
    passed: techMisc >= 4,
    score: techMisc,
    maxScore: 5,
    detail: techParts.join(' · '),
    fix: !page.hasViewport
      ? 'Add <meta name="viewport" content="width=device-width, initial-scale=1"> to <head>.'
      : !page.canonical
        ? 'Add a canonical link (<link rel="canonical" href="...">) to prevent duplicate content issues.'
        : isNoindex
          ? 'This page has noindex set — remove it from your robots meta if you want it to rank.'
          : undefined,
  });

  // ─── Aggregate ───
  const placementChecks = checks.filter(c => c.group === 'placement');
  const contentChecks = checks.filter(c => c.group === 'content');
  const techChecks = checks.filter(c => c.group === 'technical');

  const sum = (arr: CheckResult[], k: keyof CheckResult) => arr.reduce((a, c) => a + (c[k] as number), 0);

  const overallScore = sum(checks, 'score');
  const overallMax = sum(checks, 'maxScore');
  const pct = overallMax > 0 ? Math.round((overallScore / overallMax) * 100) : 0;
  const grade: ScoredReport['overall']['grade'] =
    pct >= 90 ? 'A' : pct >= 75 ? 'B' : pct >= 60 ? 'C' : pct >= 45 ? 'D' : 'F';

  // Top issues = failed checks ordered by maxScore (most impactful first)
  const topIssues = checks.filter(c => !c.passed).sort((a, b) => b.maxScore - a.maxScore).slice(0, 5);

  // Keyword placement map for visual rendering
  const placementMap = [
    { location: 'Title tag', status: titleMatch.exact ? 'found' : (titleMatch.partial ? 'partial' : 'missing'), preview: page.title },
    { location: 'H1 heading', status: h1Match.exact ? 'found' : (h1Match.partial ? 'partial' : 'missing'), preview: h1 },
    { location: 'Meta description', status: mdMatch.exact ? 'found' : (mdMatch.partial ? 'partial' : 'missing'), preview: page.metaDescription },
    { location: 'First 100 words', status: f100Match.exact ? 'found' : (f100Match.partial ? 'partial' : 'missing') },
    { location: 'Subheadings', status: subheadingMatch ? 'found' : (subheadingPartial ? 'partial' : 'missing') },
    { location: 'URL slug', status: slugMatch.exact ? 'found' : (slugMatch.partial ? 'partial' : 'missing'), preview: page.urlSlug },
    { location: 'Image alt text', status: altMatch ? 'found' : (altPartial ? 'partial' : 'missing') },
    { location: 'Body content', status: density >= 0.5 ? 'found' : 'missing' },
  ] as Array<{ location: string; status: 'found' | 'partial' | 'missing'; preview?: string }>;

  return {
    overall: { score: overallScore, maxScore: overallMax, pct, grade },
    byGroup: {
      placement: { score: sum(placementChecks, 'score'), max: sum(placementChecks, 'maxScore') },
      content: { score: sum(contentChecks, 'score'), max: sum(contentChecks, 'maxScore') },
      technical: { score: sum(techChecks, 'score'), max: sum(techChecks, 'maxScore') },
    },
    checks,
    keywordPlacementMap: placementMap,
    topIssues,
    density: parseFloat(density.toFixed(2)),
    competitorWordCountAvg: competitorAvgWordCount,
    yourWordCount: page.wordCount,
  };
}
