---
term: "Orphan Page"
slug: "orphan-page"
definition: "An orphan page is a page on your website that has no internal links pointing to it from any other page. Making it nearly invisible to search engine."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is orphan page"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "internal-link"
  - "crawl-budget"
  - "site-architecture"
  - "indexing"
  - "technical-seo"
---

## What is an Orphan Page?

An orphan page is a live page on your website that no other page links to internally. It exists in isolation, disconnected from your site's navigation and link structure.

Googlebot discovers pages by following links. If no [internal link](/glossary/internal-link) points to a page, crawlers may never find it. Even if it appears in your [XML sitemap](/glossary/xml-sitemap). It's like having a room in a building with no doors. The content might be excellent, but nobody can reach it.

Orphan pages are surprisingly common. A Botify study found that 26% of pages on large websites are orphan pages. On sites publishing content at high volume without proper internal linking strategies, the percentage can be even higher.

## Why Do Orphan Pages Matter?

Orphan pages waste your content investment. You created them, but they can't perform.

- **Can't be crawled efficiently**. Googlebot relies on internal links for discovery, and orphan pages get skipped or crawled much less frequently
- **Receive zero [link equity](/glossary/link-equity)**. Internal links pass authority between pages, and orphan pages get none of it
- **Hurt [site architecture](/glossary/site-architecture)**. They represent gaps in your content structure where topical connections should exist
- **Waste content budget**. If you're paying for blog posts that nobody can find through your site's navigation, that's money lost

Finding and fixing orphan pages is one of the fastest wins in [technical SEO](/glossary/technical-seo).

## How Orphan Pages Work

### How They're Created

Most orphan pages happen accidentally. A blog post gets published but never linked from other articles. A product page gets created without being added to category navigation. An old landing page survives a site redesign but loses all its inbound internal links. CMS migrations are a common culprit. URLs change and internal links break.

### Finding Them

Compare your site's crawl data (from Screaming Frog or a similar crawler) against your server logs or sitemap. Pages that appear in your CMS but don't show up in a crawl. Because the crawler couldn't reach them through links. Are orphans. Google Search Console's coverage report may also flag indexed pages that have no incoming internal links.

### Fixing Them

Add contextual [internal links](/glossary/internal-link) from related pages. If a blog post about "email marketing tips" is orphaned, link to it from your email marketing category page, from related blog posts, and from any relevant resource page. If the orphan page is outdated or irrelevant, consider redirecting or removing it instead.

## Orphan Page Examples

**A law firm** publishes 200 blog posts over 3 years. An audit reveals 47 are orphan pages. Never linked from any other post or page. After adding internal links from related articles and the practice area pages, those 47 posts see a combined 340% increase in organic impressions within 2 months.

**A local business** using theStacc to publish 30 articles per month ensures every new post links to at least 3 existing posts, and existing cornerstone pages link back. Zero orphan pages. Every article starts ranking faster because Googlebot discovers it through multiple paths.
## Frequently Asked Questions

### How do I find orphan pages on my site?

Run a full site crawl with Screaming Frog or Sitebulb, then compare the crawled pages against your [XML sitemap](/glossary/xml-sitemap) or CMS page list. Any page in your CMS that the crawler didn't discover through links is likely an orphan.

### Are orphan pages bad for SEO?

Yes. They waste [crawl budget](/glossary/crawl-budget), miss out on internal link equity, and often go unindexed. Even if Google finds them through your sitemap, they'll rank poorly without internal link support.

### How many internal links should each page have?

There's no exact rule, but every page should receive at least 2-3 contextual internal links from related content. Hub pages and important money pages should have more. The goal is that every page is reachable within 3 clicks from your homepage.

---

Want zero orphan pages and a fully connected content library? theStacc publishes 30 SEO-optimized articles to your site every month. Each one internally linked to your existing content. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Botify: The Problem of Orphan Pages](https://www.botify.com/blog/orphan-pages)
- [Google Search Central: Site Architecture](https://developers.google.com/search/docs/crawling-indexing/site-hierarchy)
- [Ahrefs: How to Find and Fix Orphan Pages](https://ahrefs.com/blog/orphan-pages/)
- [Screaming Frog: Crawl Audit Guide](https://www.screamingfrog.co.uk/seo-spider/)
