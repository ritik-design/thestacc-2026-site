/**
 * Centralized noindex list for content-collection-driven pages.
 *
 * Maintained set of URL paths that should emit `<meta name="robots" content="noindex,follow">`
 * even though they otherwise build normally. Used by the dynamic [slug].astro
 * templates (/blog, /glossary, /best, /alternatives, /reviews, /compare and
 * locale variants) to soft-kill specific pages without touching every markdown
 * file's frontmatter.
 *
 * Source: Phase 7 SEO audit (2026-05-07). Tier 2 = 5–50 imp at pos 60+, no
 * backlinks, no clicks in the 16-month GSC window. Soft-killed; revisit in
 * 90 days. If a page recovers organic traffic during the noindex period,
 * remove it from this list.
 *
 * Adding a URL here:
 *   - Use the URL path with leading + trailing slash (matches Astro.url.pathname).
 *   - For locale paths, include the locale prefix (e.g. /es/glosario/...).
 *
 * Removing a URL: just delete the entry. Build will regenerate without noindex
 * on next deploy.
 */

export const NOINDEX_PATHS = new Set<string>([
  // Glossary (English)
  '/glossary/broken-link/',
  '/glossary/crm-customer-relationship-management/',
  '/glossary/analytics/',
  '/glossary/unsubscribe-rate/',
  '/glossary/messaging-framework/',
  '/glossary/ai-agent/',
  '/glossary/link-velocity/',
  '/glossary/dwell-time/',
  '/glossary/customer-satisfaction-csat/',
  '/glossary/direct-message-dm/',
  '/glossary/navigational-query/',
  '/glossary/double-opt-in/',
  '/glossary/event-marketing/',
  '/glossary/churn-prediction/',
  '/glossary/crawling/',
  '/glossary/psychographics/',
  '/glossary/schema-markup/',
  '/glossary/lead-nurturing/',
  '/glossary/local-schema-markup/',
  '/glossary/product-led-growth/',
  '/glossary/organic-search/',
  '/glossary/sponsored-content/',
  '/glossary/progressive-profiling/',
  '/glossary/google-trends/',
  '/glossary/target-audience/',
  '/glossary/link-reclamation/',
  '/glossary/mobile-first-indexing/',
  '/glossary/time-to-value-ttv/',
  '/glossary/instagram-reels/',
  '/glossary/contextual-marketing/',
  '/glossary/voice-search-optimization/',
  '/glossary/customer-onboarding/',
  '/glossary/multi-location-seo/',
  '/glossary/organic-traffic/',
  '/glossary/title-tag/',
  '/glossary/positioning-statement/',
  '/glossary/sales-cycle/',
  '/glossary/drip-campaign/',
  '/glossary/holistic-seo/',
  // Blog posts
  '/blog/http-status-codes-seo/',
  '/blog/what-is-keyword-cannibalization/',
  '/blog/seo-proposal-template/',
  '/blog/off-page-seo-guide/',
  '/blog/technical-seo-checklist/',
  // Locale glossaries (PT-BR, ES, DE)
  '/es/glosario/conversion-rate/',
  '/pt-br/glossario/keyword/',
  '/de/glossar/301-redirect/',
  '/pt-br/glossario/backlinks/',
  '/de/glossar/title-tag/',
  '/pt-br/glossario/seo/',
]);

/**
 * Helper: does this URL path appear in the noindex list?
 * Normalizes to ensure leading + trailing slash before lookup.
 */
export function isNoindexed(path: string): boolean {
  if (!path) return false;
  let p = path;
  if (!p.startsWith('/')) p = '/' + p;
  if (!p.endsWith('/')) p = p + '/';
  return NOINDEX_PATHS.has(p);
}
