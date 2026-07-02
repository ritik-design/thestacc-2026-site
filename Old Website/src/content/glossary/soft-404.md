---
term: "Soft 404"
slug: "soft-404"
definition: "A soft 404 is a page that displays a 'not found' or empty message to users but returns an HTTP 200 (OK) status code to search engines. Confusing crawlers."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is soft 404"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "404-error"
  - "crawl-budget"
  - "technical-seo"
  - "google-search-console"
  - "indexing"
---

## What is a Soft 404?

A soft 404 is a page that tells visitors "this content doesn't exist" but tells Googlebot "everything's fine". A mismatch between user experience and HTTP response code that wastes [crawl budget](/glossary/crawl-budget) and confuses indexing.

A real [404 error](/glossary/404-error) returns a 404 status code, and Google knows to skip it. A soft 404 returns a 200 status code (the "OK" response), so Google tries to index a page with no real content. It's like sending someone to a store that's closed but has the "Open" sign on.

Google Search Console specifically flags soft 404s as a coverage issue. According to Google's documentation, they process soft 404s differently once detected. But detection isn't instant, and the pages can waste crawl resources for weeks before being identified.

## Why Do Soft 404s Matter?

Soft 404s silently drain your [technical SEO](/glossary/technical-seo) health.

- **Waste crawl budget**. Googlebot tries to process pages that contain nothing useful, diverting crawl resources from your real content
- **Confuse indexing**. Google may attempt to index empty or error pages, diluting your site's quality signals
- **Create poor user experience**. Visitors land on a page that looks broken but technically loaded "successfully"
- **Accumulate over time**. Ecommerce sites with expired products, blogs with deleted posts, and any CMS generating dynamic pages are prone to soft 404 buildup

On sites with thousands of pages, hundreds of soft 404s can accumulate without anyone noticing. Until Google Search Console flags them.

## How Soft 404s Work

### Common Causes

A product page gets discontinued but the CMS shows a "product unavailable" message with a 200 status code instead of returning a proper 404. An internal search page returns zero results but still loads the full template. A blog post gets unpublished but the URL serves an empty shell.

### Detection

Check [Google Search Console](/glossary/google-search-console) under the Pages report. Soft 404s appear as a specific issue type. Google identifies them by analyzing page content. If a 200 response contains thin, error-like, or empty content, Google reclassifies it as a soft 404.

### Fixing Them

The fix depends on the cause. For genuinely missing content, return a proper 404 status code or redirect to a relevant page with a [301 redirect](/glossary/301-redirect). For temporarily unavailable products, use a 503 status code. For empty search results pages, add a [noindex](/glossary/noindex) tag or block them via [robots.txt](/glossary/robots-txt).

## Soft 404 Examples

**An online retailer** has 3,000 seasonal products that rotate yearly. Old product URLs display "this item is no longer available" but return a 200 status code. Google Search Console flags 2,800 soft 404s. After updating the CMS to return proper 404 codes for discontinued products, Googlebot refocuses its crawl on current product pages. New products get indexed 60% faster.

**A content publisher** using theStacc to publish 30 articles per month notices 45 soft 404s in Search Console. Investigation reveals old draft URLs that were published accidentally then unpublished. But the CMS served a blank template with a 200 code. Setting up proper 404 responses and 301 redirects to related content clears the issue within one crawl cycle.
## Frequently Asked Questions

### How are soft 404s different from regular 404s?

A regular [404 error](/glossary/404-error) returns the correct HTTP 404 status code, telling Google the page doesn't exist. A soft 404 returns a misleading 200 status code while showing error-like content. Google handles regular 404s correctly by default. Soft 404s require manual fixes.

### Are soft 404s bad for SEO?

They waste crawl budget and can confuse indexing, which indirectly hurts SEO. They're not as damaging as a [manual action](/glossary/manual-action), but they signal technical sloppiness that accumulates over time. Fix them as part of regular technical audits.

### How do I prevent soft 404s?

Configure your CMS to return proper HTTP status codes. Pages that don't exist should return 404. Pages temporarily down should return 503. Redirected pages should return 301 or 302. Test after any CMS update or site migration.

---

Want a technically clean site with fresh content? theStacc publishes 30 SEO-optimized articles to your site every month. No soft 404s, no junk pages. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Soft 404 Errors](https://developers.google.com/search/docs/crawling-indexing/http-network-errors)
- [Google Search Central: Page Indexing Report](https://support.google.com/webmasters/answer/7440203)
- [Ahrefs: How to Find and Fix Soft 404s](https://ahrefs.com/blog/soft-404/)
- [Screaming Frog: HTTP Status Codes Guide](https://www.screamingfrog.co.uk/seo-spider/)
