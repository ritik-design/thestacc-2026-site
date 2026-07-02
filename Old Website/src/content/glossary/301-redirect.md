---
term: "301 Redirect"
slug: "301-redirect"
definition: "A 301 redirect permanently sends users and search engines from one URL to another. Learn when to use 301 redirects, how to implement them, and SEO impact."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is a 301 redirect"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "302-redirect"
  - "canonical-url"
  - "link-equity"
  - "crawling"
  - "domain-authority"
---

## What is a 301 Redirect?

A 301 redirect is an HTTP status code that permanently forwards one URL to another. Telling browsers and search engines that the original address has moved for good.

When Googlebot or a visitor hits a 301, they get automatically sent to the new URL. No broken page. No dead end. The "301" part refers to the specific HTTP response code. It's the web's way of saying "this page has permanently moved to a new location." There's a [302 redirect](/glossary/302-redirect) for temporary moves, but 301 is the one that matters for [SEO](/glossary/seo).

Here's why this is critical: Moz research shows that 301 redirects pass approximately 95-99% of [link equity](/glossary/link-equity) to the destination URL. That means the ranking power your old URL earned from [backlinks](/glossary/backlinks) doesn't disappear. It transfers to the new page. Get 301s wrong, and you're throwing away years of accumulated authority.

## Why Does a 301 Redirect Matter?

Every time a URL changes without a proper redirect, something breaks. Rankings, traffic, user experience. Pick any two.

- **Preserves search rankings**. Without a 301, Google treats the new URL as a brand new page with zero authority. Your rankings vanish overnight.
- **Transfers link equity**. Those [backlinks](/glossary/backlinks) you earned? A 301 passes their value to the new URL. Without it, that link juice evaporates.
- **Prevents 404 errors**. Users who bookmarked the old URL or click an external link get a working page instead of a [404 error](/glossary/404-error). Better experience, lower [bounce rate](/glossary/bounce-rate).
- **Consolidates duplicate content**. Multiple URLs serving the same content dilute your authority. 301s merge them into one strong page.

If you've ever moved a website, changed a URL structure, or merged two pages. You needed 301 redirects. Skipping them is one of the most common and costly [technical SEO](/glossary/technical-seo) mistakes.

## How a 301 Redirect Works

The process happens in milliseconds, but here's what's actually going on under the hood.

### The HTTP Request Cycle

A user or search engine crawler requests the old URL. The server responds with HTTP status code 301 and a "Location" header pointing to the new URL. The browser then automatically requests the new URL. The user sees the final page. They might not even notice the redirect happened.

### How Google Processes 301s

When [Googlebot](/glossary/crawling) encounters a 301, it does three things: follows the redirect to the new URL, transfers most of the old page's ranking signals to the new page, and eventually drops the old URL from its index. This process can take days to weeks depending on how frequently Google crawls your site.

### Server-Level vs. Page-Level Implementation

301 redirects are configured at the server level. Not in your HTML. The most common methods:

- **Apache (.htaccess):** `Redirect 301 /old-page https://example.com/new-page`
- **Nginx:** `rewrite ^/old-page$ /new-page permanent;`
- **WordPress plugins:** Yoast, Redirection, or Rank Math handle this through the dashboard
- **Cloudflare:** Page Rules or Bulk Redirects for domain-level changes

Page-level meta refresh redirects exist, but they're slower and don't pass link equity as reliably. Always use server-level 301s.

## Types of Redirects

Understanding the differences prevents costly mistakes:

- **301 (Permanent)**. The page has moved forever. Passes ~95-99% of link equity. Use for URL changes, domain migrations, and content consolidation.
- **[302 (Temporary)](/glossary/302-redirect)**. The page has moved temporarily. Google may or may not pass link equity. Use for A/B tests, maintenance pages, or seasonal content.
- **307 (Temporary, HTTP/1.1)**. Same as 302, but strictly preserves the request method (POST stays POST). Technical use cases only.
- **308 (Permanent, HTTP/1.1)**. Same as 301 with strict method preservation. Rarely used in SEO contexts.
- **Meta refresh**. HTML-based redirect. Slow, poor SEO value. Avoid it.

When in doubt, use a 301. It's the safe choice for permanent URL changes.

## 301 Redirect Examples

**Example 1: A local business redesigning its website**
A law firm redesigns their website and changes their URL structure from `/services/personal-injury-attorney` to `/practice-areas/personal-injury`. Without a 301, the old page. Which ranked #3 for "personal injury attorney [city]". Would return a 404. With the redirect, the new URL inherits the ranking position and the 47 [backlinks](/glossary/backlinks) pointing to the old page keep working.

**Example 2: Merging two blog posts into one stronger page**
A plumbing company has two thin articles: "How to Fix a Leaky Faucet" and "Leaky Faucet Repair Guide." Neither ranks well. They merge both into one detailed guide on the stronger URL and 301 the weaker one. The combined [domain authority](/glossary/domain-authority) signals push the merged page from position 12 to position 4 within 6 weeks.

**Example 3: Domain migration gone wrong**
An ecommerce store moves from olddomain.com to newdomain.com but only redirects the homepage. The 2,400 product pages and 180 blog posts all return 404s. [Organic traffic](/glossary/organic-traffic) drops 78% in 2 weeks. Every single URL needed a 1-to-1 301 redirect. This mistake costs months to recover from. If it's caught quickly.

## 301 Redirect vs. Canonical URL

Both deal with duplicate content, but they work differently.

| | 301 Redirect | [Canonical URL](/glossary/canonical-url) |
|---|---|---|
| **What it does** | Sends users and bots to a new URL | Tells Google which URL is the "master" copy |
| **User experience** | User sees the new page (automatic redirect) | User can still access the original page |
| **When to use** | Old page should no longer exist | Both pages should remain accessible |
| **Link equity** | Passes ~95-99% | Consolidates signals to canonical |
| **Example** | Old blog URL moved to new URL structure | Product page accessible via 3 different URLs |

Use 301s when the old page is dead. Use canonicals when both pages need to exist but you want Google to prioritize one.

## 301 Redirect Best Practices

- **Map every old URL to a relevant new URL**. Don't redirect everything to the homepage. Redirect each old page to its closest equivalent. Google treats mass-redirects to the homepage as soft 404s.
- **Implement 1-to-1 redirects during site migrations**. Before launching a new site, crawl the old one, export every URL, and create a redirect map. Miss this step and you'll watch [organic traffic](/glossary/organic-traffic) crater.
- **Avoid redirect chains**. A > B > C > D slows down the user, wastes [crawl budget](/glossary/crawl-budget), and can lose link equity at each hop. Each redirect should point directly to the final destination.
- **Monitor with Google Search Console**. Check the Coverage report for crawl errors after implementing redirects. [Google Search Console](/glossary/google-search-console) shows which pages are returning 404s so you can catch missed redirects fast.
- **Audit redirects quarterly**. Old redirects pointing to pages that no longer exist create chains. Services like theStacc include proper URL structures in every article they publish, but if you're migrating or reorganizing content, schedule regular redirect audits to keep things clean.

## Frequently Asked Questions

### Do 301 redirects hurt SEO?

Not when used correctly. A properly implemented 301 passes nearly all link equity to the new URL. Google's John Mueller has confirmed that 301s don't cause ranking loss. The risk comes from implementing them incorrectly. Redirect chains, mass redirects to the homepage, or missing pages entirely.

### How long should you keep a 301 redirect?

Indefinitely, or at least one year. Google needs time to recrawl the old URL, process the redirect, and update its index. Removing a 301 too early means external links to the old URL will hit 404s again.

### Can too many 301 redirects slow down a site?

Individual redirects add milliseconds. But redirect chains (page A > B > C) compound that delay. Keep redirects to one hop maximum. A site with thousands of clean 301s is fine. It's chains and loops that cause problems.

### What's the difference between a 301 and a 302?

A [301 is permanent](/glossary/301-redirect); a [302 is temporary](/glossary/302-redirect). Use 301 when the old URL is gone for good. Use 302 when the original page will come back (seasonal content, temporary maintenance). Google passes link equity more reliably through 301s.

---

Want a site architecture built for SEO from day one? theStacc publishes 30 SEO-optimized articles to your site every month with clean URL structures and proper internal linking. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Moz: Redirection Guide](https://moz.com/learn/seo/redirection)
- [Ahrefs: 301 Redirects for SEO](https://ahrefs.com/blog/301-redirects/)
- [Search Engine Journal: 301 vs 302 Redirects](https://www.searchenginejournal.com/301-vs-302-redirects/299843/)
- [Google Search Console Help: Fix Crawl Errors](https://support.google.com/webmasters/answer/7440203)
