/**
 * Central internal linking configuration for theStacc.com
 * Maps page types, categories, and tools to their cross-link targets
 */

// ─── Tool name normalization for review ↔ alternatives cross-linking ───
// Maps slug patterns found in reviews/alternatives to canonical slugs
export const toolSlugs = [
  'semrush', 'ahrefs', 'surfer-seo', 'jasper', 'copy-ai', 'writesonic',
  'frase', 'clearscope', 'scalenut', 'koala-ai', 'junia-ai', 'neuronwriter',
  'grammarly', 'quillbot', 'aiseo', 'brandwell', 'marketmuse', 'outrank',
  'seo-ai', 'mangools', 'se-ranking', 'rank-math',
] as const;

/**
 * Extract the core tool name from a review/alternatives slug.
 * e.g. "semrush-review" → "semrush", "jasper-alternatives" → "jasper"
 */
export function extractToolSlug(slug: string): string | null {
  // Try direct match first
  for (const tool of toolSlugs) {
    if (slug === tool || slug.startsWith(tool + '-')) {
      return tool;
    }
  }
  // Try matching after removing common suffixes
  const cleaned = slug
    .replace(/-review$/, '')
    .replace(/-alternatives$/, '')
    .replace(/-alternative$/, '');
  for (const tool of toolSlugs) {
    if (cleaned === tool) return tool;
  }
  return null;
}

// ─── Category → Module page mapping ───
export const categoryToModule: Record<string, { url: string; label: string; anchor: string }> = {
  'Content Strategy': {
    url: '/modules/content-seo',
    label: 'Blog SEO Module',
    anchor: 'AI blog writing tool',
  },
  'SEO Tools': {
    url: '/modules/content-seo',
    label: 'Blog SEO Module',
    anchor: 'SEO automation platform',
  },
  'Local SEO': {
    url: '/modules/local-seo',
    label: 'Local SEO Module',
    anchor: 'local SEO automation',
  },
  'SEO Tips': {
    url: '/modules/content-seo',
    label: 'Blog SEO Module',
    anchor: 'automated SEO tool',
  },
};

// ─── Category → Related free tools ───
export const categoryToTools: Record<string, { url: string; label: string }[]> = {
  'Content Strategy': [
    { url: '/tools/headline-analyzer', label: 'Headline Analyzer' },
    { url: '/tools/meta-tag-analyzer', label: 'Meta Tag Analyzer' },
    { url: '/tools/seo-audit', label: 'Free SEO Audit' },
  ],
  'SEO Tools': [
    { url: '/tools/on-page-seo-checker', label: 'On-Page SEO Checker' },
    { url: '/tools/schema-markup-generator', label: 'Schema Markup Generator' },
    { url: '/tools/website-seo-score', label: 'Website SEO Score' },
  ],
  'Local SEO': [
    { url: '/tools/gbp-post-generator', label: 'GBP Post Generator' },
    { url: '/tools/review-response-generator', label: 'Review Response Generator' },
    { url: '/tools/review-qr-code-generator', label: 'Review QR Code Generator' },
  ],
  'SEO Tips': [
    { url: '/tools/seo-audit', label: 'Free SEO Audit' },
    { url: '/tools/on-page-seo-checker', label: 'On-Page SEO Checker' },
    { url: '/tools/seo-roi-calculator', label: 'SEO ROI Calculator' },
  ],
};

// ─── Module pages → Related resources ───
export const moduleResources: Record<string, {
  blogs: { url: string; label: string }[];
  bestLists: { url: string; label: string }[];
  tools: { url: string; label: string }[];
}> = {
  'content-seo': {
    blogs: [
      { url: '/blog/seo-content-strategy', label: 'SEO Content Strategy Guide' },
      { url: '/blog/ai-content-writing-tools', label: 'AI Content Writing Tools' },
      { url: '/blog/blog-seo-checklist', label: 'Blog SEO Checklist' },
      { url: '/blog/keyword-research-guide', label: 'Keyword Research Guide' },
      { url: '/blog/on-page-seo-guide', label: 'On-Page SEO Guide' },
    ],
    bestLists: [
      { url: '/best/ai-blog-writing-tools', label: 'Best AI Blog Writing Tools' },
      { url: '/best/ai-seo-tools', label: 'Best AI SEO Tools' },
      { url: '/best/seo-automation-tools', label: 'Best SEO Automation Tools' },
    ],
    tools: [
      { url: '/tools/headline-analyzer', label: 'Headline Analyzer' },
      { url: '/tools/meta-tag-analyzer', label: 'Meta Tag Analyzer' },
      { url: '/tools/on-page-seo-checker', label: 'On-Page SEO Checker' },
    ],
  },
  'local-seo': {
    blogs: [
      { url: '/blog/google-business-profile-optimization-complete-guide', label: 'Google Business Profile Optimization Guide' },
      { url: '/blog/local-seo-guide', label: 'Complete Local SEO Guide' },
      { url: '/blog/local-seo-for-small-business', label: 'Local SEO for Small Business' },
      { url: '/blog/google-maps-seo', label: 'Google Maps SEO Guide' },
      { url: '/blog/local-seo-checklist', label: 'Local SEO Checklist' },
    ],
    bestLists: [
      { url: '/best/local-seo-tools', label: 'Best Local SEO Tools' },
      { url: '/best/google-business-profile-management-tools', label: 'Best GBP Management Tools' },
      { url: '/best/affordable-local-seo-tools', label: 'Best Affordable Local SEO Tools' },
    ],
    tools: [
      { url: '/tools/gbp-post-generator', label: 'GBP Post Generator' },
      { url: '/tools/review-response-generator', label: 'Review Response Generator' },
      { url: '/tools/review-qr-code-generator', label: 'Review QR Code Generator' },
    ],
  },
  'social-media': {
    blogs: [
      { url: '/blog/social-media-seo', label: 'Social Media SEO Guide' },
      { url: '/blog/social-media-automation', label: 'Social Media Automation Guide' },
      { url: '/blog/social-media-marketing-strategy', label: 'Social Media Marketing Strategy' },
      { url: '/blog/social-media-content-calendar', label: 'Content Calendar Guide' },
      { url: '/blog/social-media-for-seo', label: 'Social Media for SEO' },
    ],
    bestLists: [
      { url: '/best/social-media-management-tools', label: 'Best Social Media Tools' },
      { url: '/best/social-media-scheduling-tools', label: 'Best Scheduling Tools' },
      { url: '/best/social-media-automation-tools', label: 'Best Automation Tools' },
    ],
    tools: [
      { url: '/tools/headline-analyzer', label: 'Headline Analyzer' },
      { url: '/tools/meta-tag-analyzer', label: 'Meta Tag Analyzer' },
    ],
  },
};

// ─── Homepage anchor text variations for internal links from content pages ───
export const homepageAnchors = [
  'AI SEO automation platform',
  'SEO automation tool',
  'theStacc',
  'automated SEO platform',
  'AI-powered SEO tool',
] as const;

// ─── Glossary category → relevant best-list pages ───
export const glossaryCategoryLinks: Record<string, { url: string; label: string }[]> = {
  'SEO': [
    { url: '/best/ai-seo-tools', label: 'Best AI SEO Tools' },
    { url: '/modules/content-seo', label: 'Blog SEO Module' },
  ],
  'Local SEO': [
    { url: '/best/local-seo-tools', label: 'Best Local SEO Tools' },
    { url: '/modules/local-seo', label: 'Local SEO Module' },
  ],
  'Marketing': [
    { url: '/best/ai-content-writing-tools-for-seo', label: 'Best AI Writing Tools' },
    { url: '/modules/content-seo', label: 'Blog SEO Module' },
  ],
  'Social Media': [
    { url: '/best/social-media-management-tools', label: 'Best Social Media Tools' },
    { url: '/modules/social-media', label: 'Social Media Module' },
  ],
  'AI & Emerging': [
    { url: '/best/ai-seo-tools', label: 'Best AI SEO Tools' },
    { url: '/modules/content-seo', label: 'Blog SEO Module' },
  ],
};

// ─── All modules for cross-linking ───
export const allModules = [
  { url: '/modules/content-seo', label: 'Blog SEO', anchor: 'AI blog writing' },
  { url: '/modules/local-seo', label: 'Local SEO', anchor: 'local SEO automation' },
  { url: '/modules/social-media', label: 'Social Media', anchor: 'social media automation' },
] as const;
