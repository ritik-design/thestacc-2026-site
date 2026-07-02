---
term: "404 Error"
slug: "404-error"
definition: "A 404 error is an HTTP status code that tells visitors and search engines a page doesn't exist at the requested URL. Fixing 404s protects your rankings."
category: "SEO"
difficulty: "Beginner"
keyword: "what is a 404 error"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "broken-link"
  - "301-redirect"
  - "crawl-budget"
  - "site-architecture"
  - "url-structure"
---

## What is a 404 Error?

A 404 error is an HTTP response code indicating that the server can't find the page a user or crawler requested. It's the internet's way of saying "this page doesn't exist here."

Every website encounters 404s at some point. Pages get deleted, URLs change, someone types in the wrong address. The problem isn't that they happen. It's what happens when you ignore them. Visitors bounce. Googlebot wastes [crawl budget](/glossary/crawl-budget). And any [link equity](/glossary/link-equity) pointing to that dead URL evaporates.

According to a Semrush study, the average website has over 300 pages returning 404 errors. Most site owners don't even know they exist until rankings start slipping.

## Why Does 404 Error Matter?

Left unchecked, 404 errors quietly erode your site's SEO performance and user trust.

- **Lost link value**. External [backlinks](/glossary/backlinks) pointing to 404 pages pass zero ranking power to your site
- **Wasted crawl budget**. Googlebot spends time on dead URLs instead of indexing your real content
- **Poor user experience**. Visitors who hit a 404 leave. Bounce rates spike, and [dwell time](/glossary/dwell-time) drops
- **Broken internal paths**. A 404 in your navigation or footer can block users from reaching key pages

Any business relying on [organic traffic](/glossary/organic-traffic) should audit for 404s at least monthly.

## How 404 Error Works

### What Triggers a 404

A server returns a 404 when it receives a request for a URL that doesn't match any existing resource. Common causes include deleted pages, changed [URL structures](/glossary/url-structure), typos in links, and expired content that was removed without a redirect.

### Soft 404 vs. Hard 404

A hard 404 returns the proper HTTP status code. A soft 404 shows a "page not found" message but returns a 200 (OK) status code. Confusing search engines into thinking the page exists. Google Search Console flags soft 404s separately because they waste crawl resources.

### How to Fix 404 Errors

The standard fix is a [301 redirect](/glossary/301-redirect) pointing the broken URL to the most relevant live page. If no relevant page exists, let the 404 stand but make sure your custom 404 page helps visitors navigate back to useful content. Tools like Google Search Console, Screaming Frog, and Ahrefs can identify 404s across your site.

## 404 Error Examples

**Example 1: A redesigned website**
A plumbing company redesigns their site and changes `/services/drain-cleaning` to `/plumbing-services/drain-cleaning`. Without a redirect, every existing link and bookmark to the old URL now hits a 404. Their top-ranking page disappears from Google within weeks.

**Example 2: A deleted blog post**
An accounting firm removes an outdated tax guide that had earned 40+ backlinks. Those links now point to nothing. A 301 redirect to the updated version would have preserved that link equity and kept the page ranking.
## Frequently Asked Questions

### Are 404 errors bad for SEO?

Individual 404s on low-value pages won't tank your rankings. But large numbers of 404s. Especially on pages with backlinks or internal links. Signal poor site maintenance to Google and waste crawl budget that could index your important pages.

### How do I find 404 errors on my site?

Google Search Console's Coverage report lists pages returning 404 codes. Third-party crawlers like Screaming Frog and Ahrefs Site Audit scan every URL on your site and flag broken pages within minutes.

### Should I redirect all 404s?

Only redirect 404s to relevant pages. Redirecting deleted pages to your homepage or unrelated content creates a bad user experience and Google may treat those redirects as soft 404s anyway. If there's no logical destination, let the 404 stand.

---

Want to keep your site's technical SEO clean without doing it manually? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Fix soft 404 errors](https://developers.google.com/search/docs/crawling-indexing/http-network-errors)
- [Semrush: Site Audit Errors Study](https://www.semrush.com/blog/site-audit-issues/)
- [Moz: HTTP Status Codes for SEO](https://moz.com/learn/seo/http-status-codes)
- [Ahrefs: How to Find and Fix Broken Links](https://ahrefs.com/blog/broken-link-building/)
