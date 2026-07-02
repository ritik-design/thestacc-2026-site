---
term: "Noindex"
slug: "noindex"
definition: "Noindex is a directive that tells search engines not to include a specific page in their search index. It keeps pages accessible to visitors while hiding."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is noindex"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "meta-robots-tag"
  - "robots-txt"
  - "indexing"
  - "crawl-budget"
  - "thin-content"
---

## What is Noindex?

Noindex is a page-level directive. Delivered via a [meta robots tag](/glossary/meta-robots-tag) or X-Robots-Tag HTTP header. That instructs search engines to exclude a specific URL from their search index.

It's not a block. Google still crawls the page (unlike a robots.txt disallow). It just won't show the page in search results. That's a critical distinction. Noindex lets you keep pages live and accessible to visitors while preventing them from appearing in Google, Bing, or other search engines.

Google processes noindex at the page level, making it more precise than robots.txt. According to Ahrefs' web crawl data, approximately 5.3% of all web pages use noindex. Mostly for admin pages, tag archives, staging environments, and [thin content](/glossary/thin-content) pages that would hurt overall site quality.

## Why Does Noindex Matter?

Noindex is your primary tool for managing what Google considers your "indexable" site.

- **Quality control**. Preventing thin or [duplicate pages](/glossary/duplicate-content) from entering the index protects your site's overall quality signal
- **[Crawl budget](/glossary/crawl-budget) savings**. While Google still crawls noindexed pages, over time it crawls them less frequently, freeing budget for important pages
- **Helpful Content protection**. Google's [Helpful Content system](/glossary/helpful-content-update) evaluates your site holistically. Noindexing weak pages prevents them from dragging down your domain
- **Staging and internal pages**. Login pages, thank-you pages, and staging environments shouldn't appear in search results

Any site with more than 50 pages should audit which pages deserve indexation and which don't.

## How Noindex Works

### Implementation Methods

Add `<meta name="robots" content="noindex">` in the page's `<head>` section. For non-HTML files (PDFs, images), use the X-Robots-Tag HTTP header: `X-Robots-Tag: noindex`. Both methods tell all search engines. Replace "robots" with "googlebot" to target Google specifically.

### Noindex with Follow

Using `noindex, follow` tells Google: "Don't show this page in results, but do follow the links on it." This is useful for archive pages or tag pages that link to valuable content but shouldn't rank themselves. The link equity flows through even though the page itself stays out of the index.

### Common Noindex Mistakes

The most dangerous mistake: accidentally noindexing your entire site. This happens when developers forget to remove `noindex` directives from a staging environment after migrating to production. Another common error: blocking a page with robots.txt AND adding noindex. If robots.txt blocks the crawl, Google never sees the noindex tag.

## Noindex Examples

**Example 1: Cleaning up tag page bloat**
A WordPress blog has 400 tag pages, most with only 1-2 posts. These thin pages add no value to search. Adding noindex to all tag pages removes them from Google's index while keeping them functional for site navigation. The blog's overall quality signal improves.

**Example 2: Protecting staging from accidental indexing**
A web development agency adds `<meta name="robots" content="noindex, nofollow">` to every staging site by default. When one client's staging URL accidentally gets linked from an external source, Google crawls it but doesn't index it. Preventing embarrassing unfinished pages from appearing in search results.
## Frequently Asked Questions

### How long does it take for noindex to remove a page from Google?

Google needs to recrawl the page to see the noindex directive. For frequently crawled pages, this can happen within days. For rarely crawled pages, it may take weeks. Use Google Search Console's URL Removal tool if you need faster temporary removal.

### Does noindex waste crawl budget?

Initially, Google still crawls noindexed pages. Over time, it reduces crawl frequency for consistently noindexed URLs. For large-scale exclusions (thousands of pages), using [robots.txt](/glossary/robots-txt) to prevent the crawl entirely is more efficient for crawl budget.

### Should I noindex or delete low-quality pages?

If the page might have value in the future, noindex it. If it's permanently worthless, delete it and return a proper 404. Don't noindex pages indefinitely as a substitute for proper content cleanup. Review noindexed pages quarterly and decide whether to improve, redirect, or remove them.

---

Want your site's index filled with high-quality pages? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Noindex Tag](https://developers.google.com/search/docs/crawling-indexing/block-indexing)
- [Google Search Central: Remove URLs](https://support.google.com/webmasters/answer/9689846)
- [Ahrefs: Noindex Guide](https://ahrefs.com/blog/noindex/)
- [Moz: Robots Meta Directives](https://moz.com/learn/seo/robots-meta-directives)
