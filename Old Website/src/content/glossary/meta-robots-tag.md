---
term: "Meta Robots Tag"
slug: "meta-robots-tag"
definition: "The meta robots tag is an HTML element that instructs search engines how to crawl, index, and display a specific page. Directives include noindex."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is meta robots tag"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "noindex"
  - "nofollow-link"
  - "robots-txt"
  - "crawling"
  - "indexing"
---

## What is the Meta Robots Tag?

The meta robots tag is an HTML meta element placed in a page's `<head>` section that gives search engines page-level instructions about [crawling](/glossary/crawling), [indexing](/glossary/indexing), and content display in search results.

Unlike [robots.txt](/glossary/robots-txt) (which controls access at the crawl stage), meta robots tags work at the page level after Google has already fetched the page. This gives you granular control over individual pages. Telling Google to index or not index, follow links or not, show snippets or not.

Google processes an estimated 400 billion pages in its index. Meta robots tags are how site owners communicate page-level preferences at scale. Ahrefs found that 5.3% of pages across the web use a [noindex](/glossary/noindex) directive. Showing how widely this tag is deployed.

## Why Does Meta Robots Tag Matter?

Meta robots tags give you precise control over what appears in Google's index.

- **Index management**. Keep internal pages (login, thank you, staging) out of search results without blocking them from crawlers
- **Link equity control**. The nofollow directive prevents equity from flowing through specific links on a page
- **Snippet control**. Directives like nosnippet and max-snippet control how Google displays your content in search results
- **Duplicate prevention**. Noindexing thin or [duplicate pages](/glossary/duplicate-content) prevents them from diluting your site's overall quality signals

Any site with pages that shouldn't appear in search results needs meta robots tags.

## How Meta Robots Tag Works

### Common Directives

`noindex` tells Google not to include the page in search results. `nofollow` tells Google not to follow any links on the page. `nosnippet` prevents text snippets from appearing. `max-snippet:[number]` limits snippet length. `noarchive` prevents Google from showing a cached copy. You can combine directives: `<meta name="robots" content="noindex, nofollow">`.

### Meta Robots vs. X-Robots-Tag

The meta robots tag works in HTML. The X-Robots-Tag works via HTTP headers. Useful for non-HTML files like PDFs and images that don't have a `<head>` section. Both accept the same directives. Use whichever is easier to implement for your specific use case.

### Common Mistakes

The biggest mistake: adding noindex to pages you actually want indexed, usually through misconfigured CMS settings or a staging environment directive that carries over to production. Second: using robots.txt to block a page AND adding noindex. If robots.txt blocks the crawl, Google never sees the noindex tag, so the page might stay indexed.

## Meta Robots Tag Examples

**Example 1: Blocking internal pages**
An ecommerce store has 500 filter combination pages that create [thin content](/glossary/thin-content). They add `<meta name="robots" content="noindex, follow">` to filter pages. Google stops indexing the thin pages but still follows links on them, keeping the internal linking structure intact.

**Example 2: Controlling search snippets**
A news publisher doesn't want Google showing full paragraphs in search results (driving zero-click behavior). They add `<meta name="robots" content="max-snippet:50">` to article pages, limiting snippets to 50 characters. This forces users to click through for the full story.
### Tools and Resources

| Tool | Purpose | Price |
|---|---|---|
| **[Google Search Console](/glossary/google-search-console)** | Search performance data | Free |
| **Ahrefs** | Backlinks, keywords, site audit | From $99/month |
| **Semrush** | All-in-one SEO platform | From $130/month |
| **Screaming Frog** | Technical crawl analysis | Free (500 URLs) |
| **theStacc** | Automated SEO content publishing | From $99/month |

## Frequently Asked Questions

### What's the difference between noindex and robots.txt disallow?

Robots.txt blocks the crawl. Google never fetches the page. [Noindex](/glossary/noindex) lets Google crawl the page but tells it not to include the page in search results. Use noindex when you want Google to see the page (and follow its links) but not show it in search. Use robots.txt when you want to save [crawl budget](/glossary/crawl-budget).

### Does noindex remove a page from Google immediately?

No. Google needs to recrawl the page and find the noindex tag before removing it from the index. This can take days to weeks. For urgent removals, use Google Search Console's URL Removal tool for temporary removal while the noindex tag takes effect.

### Can I use meta robots to noindex specific search engines?

Yes. Replace `name="robots"` with a specific bot name: `name="googlebot"` for Google only, or `name="bingbot"` for Bing only. This lets you appear in one search engine but not another. Though it's rarely needed outside of specific licensing situations.

---

Want your site's technical SEO handled while you focus on growth? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Robots Meta Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)
- [Google Search Central: X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag#xrobotstag)
- [Moz: Robots Meta Directives](https://moz.com/learn/seo/robots-meta-directives)
