---
term: "Canonical URL / Canonicalization"
slug: "canonical-url"
definition: "A canonical URL tells search engines which version of a page is the master copy. Learn how canonicalization prevents duplicate content issues and how to."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is a canonical url"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "duplicate-content"
  - "301-redirect"
  - "indexing"
  - "crawl-budget"
  - "technical-seo"
---

## What is a Canonical URL?

A canonical URL is an HTML element that tells search engines which version of a page is the preferred, authoritative copy when multiple URLs serve the same or very similar content.

It looks like this in the `<head>` of a page: `<link rel="canonical" href="https://example.com/preferred-page">`. Why does this exist? Because on the modern web, a single piece of content often lives at multiple URLs. Same product page accessible with and without www, with and without trailing slashes, with tracking parameters, through filtered navigation. Google sees each URL as a separate page. Without a canonical tag, Google has to guess which one to index. And it often guesses wrong.

Semrush data from a study of 150,000 websites found that 65% of domains have some form of [duplicate content](/glossary/duplicate-content) issue. Canonical tags are the primary tool for solving this at scale without restructuring your entire site.

## Why Does Canonicalization Matter?

Duplicate content isn't a penalty. Google has stated this clearly. But it creates real SEO problems that cost you traffic and rankings.

- **Link equity gets split**. If 30 sites link to your page but half link to `example.com/page` and half to `example.com/page/`, the authority is divided. A canonical consolidates all signals to one URL, making it stronger.
- **[Crawl budget](/glossary/crawl-budget) gets wasted**. Googlebot has a finite crawl budget for your site. Every duplicate URL it crawls is a page it didn't crawl. For large sites with thousands of pages, this directly impacts how quickly new content gets [indexed](/glossary/indexing).
- **The wrong page might rank**. Without canonicalization, Google picks the version it thinks is best. That might be your mobile URL, a parameter-heavy URL, or a filtered category page. Not the clean, optimized version you want ranking.
- **Analytics get fragmented**. Traffic and engagement data spread across multiple URLs. Your actual performance looks weaker than it is because the metrics are split.

If your site has more than a handful of pages, you almost certainly have duplicate content that canonicalization would fix.

## How Canonicalization Works

The canonical tag is a suggestion, not a directive. Google usually respects it. But not always.

### Self-Referencing Canonicals

Every page on your site should point its canonical tag to itself. This is called a self-referencing canonical. It tells Google: "This is the preferred URL for this content, even if you discover it through a different path." Most [CMS platforms](/glossary/content-management-system) and [technical SEO](/glossary/technical-seo) plugins handle this automatically.

### Cross-Domain Canonicals

If you syndicate content. Publishing the same article on your blog and on Medium or LinkedIn. You can set a cross-domain canonical pointing from the syndicated version back to your original. This tells Google to credit the [link equity](/glossary/link-equity) and ranking signals to your domain, not the syndicated copy.

### Canonical vs. Google's Choice

Google treats canonical tags as a strong hint, not a command. If the canonical tag conflicts with other signals (sitemaps, internal links, redirect patterns), Google may override your preference. This is why consistency matters. Your canonical, your [internal links](/glossary/internal-link), your sitemap, and your [301 redirects](/glossary/301-redirect) should all point to the same preferred URL.

### Common Canonical URL Variations

These are the most frequent duplicate content scenarios canonicalization solves:

- `http://` vs `https://`
- `www.example.com` vs `example.com`
- `/page` vs `/page/` (trailing slash)
- `/page` vs `/page?utm_source=google&utm_medium=cpc`
- `/page` vs `/page?ref=homepage`
- Mobile URLs (`m.example.com`) vs desktop URLs

Each variation is a separate URL to Google. Canonical tags merge them into one.

## Types of Canonicalization

There are multiple ways to signal your preferred URL. The canonical tag is the most common, but not the only option.

- **HTML canonical tag**. The `<link rel="canonical">` tag in the page's `<head>`. Most flexible, works on any page, easy to implement.
- **HTTP header canonical**. Sent as a `Link:` header in the HTTP response. Used for non-HTML files (PDFs, images) where you can't add HTML tags.
- **[301 redirect](/glossary/301-redirect)**. Permanently redirects duplicate URLs to the preferred version. Stronger than a canonical tag because users and bots can only access the preferred URL.
- **[XML sitemap](/glossary/xml-sitemap) signals**. Including only canonical URLs in your sitemap reinforces which versions you prefer. Not a direct canonicalization method, but a supporting signal.
- **Internal linking consistency**. Always linking to the same version of a URL across your site sends Google a clear signal about your preferred version.

For most sites, the HTML canonical tag combined with consistent internal linking handles 90%+ of cases.

## Canonical URL Examples

**Example 1: An ecommerce site with parameter-heavy URLs**
A clothing store's product page lives at `/blue-running-shoes`. But filtering by size generates `/blue-running-shoes?size=10`, and tracking codes add `/blue-running-shoes?utm_source=email`. All three show the same product. Without canonical tags, Google might index the parameter URL instead of the clean one. Adding `<link rel="canonical" href="/blue-running-shoes">` to all three versions solves it instantly.

**Example 2: A multi-location business with duplicate service pages**
A plumbing franchise has service pages for each city: `/austin/drain-cleaning`, `/dallas/drain-cleaning`, `/houston/drain-cleaning`. The content is 90% identical with only the city name swapped. These pages shouldn't canonicalize to each other (they target different [local keywords](/glossary/local-keywords)), but they should each self-reference. The real fix is making each page genuinely unique with city-specific content. Something theStacc handles by generating location-specific articles automatically.

**Example 3: A blog syndicating content to Medium**
A B2B company republishes their blog posts on Medium for extra exposure. Without a canonical tag, Google might rank the Medium version instead of the original. By adding a canonical URL pointing back to the company blog on each Medium post (Medium supports this in settings), all ranking signals flow to the original domain. [Organic traffic](/glossary/organic-traffic) goes to your site, not Medium's.

## Canonical URL vs. 301 Redirect

Both solve duplicate content problems. The right choice depends on whether the duplicate page should remain accessible.

| | Canonical URL | [301 Redirect](/glossary/301-redirect) |
|---|---|---|
| **User sees** | Both pages are accessible | User is sent to the preferred page |
| **Signal strength** | Strong hint (Google may override) | Definitive (forced redirect) |
| **Use when** | Both URLs need to exist (parameters, syndication) | Old URL should no longer be visited |
| **Link equity** | Consolidated to canonical URL | Passes ~95-99% to destination |
| **Example** | Product page with filter parameters | Old blog URL moved to new URL structure |

When the duplicate page must remain accessible (tracked URLs, filtered results, syndicated content), use a canonical. When the old URL is dead and gone, use a 301.

## Canonical URL Best Practices

- **Self-reference every page**. Even pages without duplicates should have a self-referencing canonical tag. It's a safety net against unexpected duplicate URLs from parameters, session IDs, or CMS quirks.
- **Use absolute URLs, not relative**. Always write the full URL: `https://example.com/page`. Not `/page`. Relative canonicals can cause issues with protocol and domain resolution.
- **Point canonicals to indexable pages**. Never set a canonical to a page that's [noindexed](/glossary/noindex), redirected, or returns a [404](/glossary/404-error). That confuses Google and defeats the purpose.
- **Audit canonicals after site migrations**. CMS changes, domain moves, and redesigns frequently break canonical tags. Run a crawl with Screaming Frog or Sitebulb post-launch to verify every page points to the right canonical.
- **Keep your signals consistent**. Your canonical tag, sitemap, internal links, and hreflang (for international sites) should all agree on the preferred URL. When signals conflict, Google makes its own choice. And it might not be the one you want. theStacc publishes all articles with proper canonical tags and clean URL structures built in.

## Frequently Asked Questions

### Do canonical tags pass link equity?

Yes. Google consolidates ranking signals from duplicate pages to the canonical URL. If 10 sites link to a parameter version of your page and the canonical points to the clean version, the clean version gets the benefit of those links.

### Can I canonical to a different domain?

Yes. Cross-domain canonicals tell Google that the original content lives on a different domain. Common use case: syndicating content to Medium, LinkedIn, or partner sites while keeping your domain as the canonical source.

### What happens if my canonical tag is wrong?

Google may ignore it. If the canonical points to a page with completely different content, Google recognizes the mismatch and will index the URLs independently. Canonical tags only work when the pages have substantially similar content.

### How do I check my canonical tags?

View page source and search for `rel="canonical"`. Or use [Google Search Console](/glossary/google-search-console). The URL Inspection tool shows which canonical Google selected for any page. If Google's chosen canonical differs from yours, there's a conflict in your signals.

---

Want every article published with proper canonical tags, clean URLs, and [technical SEO](/glossary/technical-seo) handled automatically? theStacc publishes 30 SEO-optimized articles to your site every month. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Consolidate Duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Moz: Canonical URL Tag Guide](https://moz.com/learn/seo/canonicalization)
- [Ahrefs: Canonical Tags for SEO](https://ahrefs.com/blog/canonical-tags/)
- [Semrush: Duplicate Content Study](https://www.semrush.com/blog/duplicate-content/)
- [Google Search Console: URL Inspection Tool](https://support.google.com/webmasters/answer/9012289)
