---
term: "Sitemap (XML)"
slug: "xml-sitemap"
definition: "An XML sitemap is a file that lists all the important URLs on your website, helping search engines like Google discover, crawl, and index your pages more."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is an xml sitemap"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "crawling"
  - "indexing"
  - "robots-txt"
  - "technical-seo"
  - "google-search-console"
---

## What is an XML Sitemap?

**An XML sitemap is a structured file (formatted in XML) that provides search engines with a complete list of URLs on your site that you want crawled and indexed.**

It's basically a roadmap for [crawlers](/glossary/crawling). Without it, Googlebot has to discover your pages by following links. Which works, but it's slow and incomplete. Orphan pages (pages with no internal links pointing to them) might never get found.

Google's own documentation states that sitemaps are "especially helpful" for large sites, new sites with few external links, and sites with rich media content. A study by Oncrawl found that pages listed in an XML sitemap get indexed 8-10x faster on average than pages that aren't included.

## Why Does an XML Sitemap Matter?

If Google can't find your pages, they can't rank them. An XML sitemap removes the guesswork.

- **Faster indexing of new content**. When you publish a new blog post or landing page, the sitemap tells Google it exists immediately. No waiting for Googlebot to stumble across it through link discovery.
- **Coverage for orphan pages**. Pages without internal links are invisible to crawlers. The sitemap catches them. This is common on large eCommerce sites with filter-generated pages.
- **Priority and freshness signals**. Sitemaps include `<lastmod>` tags that tell Google when a page was last updated. Fresh content gets recrawled faster.
- **Diagnostic value**. Submitting your sitemap to [Google Search Console](/glossary/google-search-console) gives you an indexation report. You can see exactly which pages Google has indexed and which ones it rejected. And why.

For any site publishing content regularly, an XML sitemap is non-negotiable.

## How an XML Sitemap Works

The process is straightforward. Create the file, tell Google where it is, and keep it updated.

### File Structure

An XML sitemap is a list of `<url>` entries wrapped in a `<urlset>` tag. Each entry includes the URL (`<loc>`), last modification date (`<lastmod>`), change frequency (`<changefreq>`), and priority (`<priority>`). Google officially ignores `changefreq` and `priority`. The URL and `lastmod` date are what matter.

### Submission Methods

Three ways to get your sitemap to Google. First, submit it directly through [Google Search Console](/glossary/google-search-console). Second, reference it in your [robots.txt](/glossary/robots-txt) file with `Sitemap: https://yoursite.com/sitemap.xml`. Third, use the Ping API to notify Google of updates. Most sites use the first two methods.

### Sitemap Index Files

Individual sitemaps max out at 50,000 URLs or 50MB (uncompressed). Larger sites use a sitemap index file. A sitemap that points to other sitemaps. A site with 200,000 pages might have a sitemap index pointing to 4 individual sitemaps of 50,000 URLs each.

### Auto-Generation

Most CMS platforms (WordPress, Webflow, Shopify) generate XML sitemaps automatically. WordPress creates one at `/wp-sitemap.xml` by default. SEO plugins like Yoast and RankMath offer more control over which pages appear.

## Types of XML Sitemaps

Not all sitemaps serve the same purpose:

- **Standard XML sitemap**. Lists your HTML pages. The most common type and the one most people mean when they say "sitemap."
- **Image sitemap**. Lists images on your site for Google Images discovery. Useful for photographers, eCommerce, and visual-heavy sites.
- **Video sitemap**. Provides metadata about video content (title, description, thumbnail, duration). Helps content appear in Google's video carousels.
- **News sitemap**. Specifically for Google News publishers. Includes publication date, title, and language. Only for sites approved as news sources.
- **Sitemap index**. A master file that links to multiple sitemaps. Required for large sites exceeding the 50,000-URL limit.

Most small-to-medium businesses only need a standard XML sitemap. Add image or video sitemaps if visual content is a significant part of your strategy.

## XML Sitemap Examples

**Example 1: New local business website**
A newly launched plumbing company has 15 pages and zero [backlinks](/glossary/backlinks). Without a sitemap, Google might take weeks to discover all pages through link crawling alone. After submitting a sitemap to Google Search Console, all 15 pages get indexed within 5 days.

**Example 2: eCommerce store with 10,000 products**
An online retailer adds 50 new products weekly. Their sitemap auto-generates through Shopify, updating `<lastmod>` dates with each product addition. Google recrawls the sitemap regularly and discovers new products within days. Not weeks.

**Example 3: Blog publishing 30 posts per month**
A company using theStacc publishes 30 SEO-optimized articles monthly. Each new post automatically appears in the XML sitemap. Google Search Console's index coverage report shows consistent growth in indexed pages. No manual sitemap updates needed.

## XML Sitemap vs HTML Sitemap

Different files for different audiences.

| | XML Sitemap | HTML Sitemap |
|---|---|---|
| **Audience** | Search engine crawlers | Human visitors |
| **Format** | XML code | Regular web page with links |
| **Location** | `/sitemap.xml` | Usually `/sitemap` or linked in footer |
| **Purpose** | Help crawlers discover all pages | Help users navigate the site |
| **SEO impact** | Directly improves crawl efficiency | Minor. Mostly a UX feature |
| **Required?** | Strongly recommended | Optional, nice to have |

Both are useful, but the XML sitemap is the one that impacts [SEO](/glossary/seo) directly. If you only implement one, make it the XML version.

## XML Sitemap Best Practices

- **Only include indexable pages**. Don't list pages with [noindex](/glossary/noindex) tags, redirected URLs, or pages blocked by robots.txt. A clean sitemap builds trust with Google.
- **Keep `<lastmod>` dates accurate**. Only update the lastmod date when page content actually changes. Faking freshness by updating dates without content changes erodes Google's trust in your sitemap signals.
- **Submit through Google Search Console**. Manual submission gives you access to indexation reports showing exactly how Google processes your sitemap. Check it monthly.
- **Limit to 50,000 URLs per file**. Use a sitemap index if you exceed this. Large sitemaps that fail to load are worse than no sitemap at all.
- **Pair with consistent publishing**. A sitemap is most valuable when your site regularly adds new content worth [indexing](/glossary/indexing). theStacc publishes 30 SEO articles per month, giving Google a reason to recrawl your sitemap frequently and discover fresh pages.

## Frequently Asked Questions

### Does every website need an XML sitemap?

Not technically. Small sites with strong [internal linking](/glossary/internal-link) can get by without one. But there's no downside to having a sitemap, and the benefits for indexing speed and diagnostic data make it worth the minimal effort for any site.

### How do I create an XML sitemap?

Most CMS platforms generate one automatically. WordPress, Webflow, and Shopify all create sitemaps by default. For custom sites, tools like Screaming Frog or XML-Sitemaps.com can generate the file. Then submit it through Google Search Console.

### How often should I update my sitemap?

Ideally, your sitemap updates automatically when you publish or modify content. CMS-generated sitemaps handle this. If you maintain a manual sitemap, update it whenever you add, remove, or significantly change pages.

### Can a bad sitemap hurt my SEO?

A sitemap with broken URLs, noindexed pages, or incorrect lastmod dates sends confusing signals to Google. It won't trigger a penalty, but it wastes [crawl budget](/glossary/crawl-budget) and slows down indexing of your important pages.

---

Want fresh content that Google actually indexes? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Learn About Sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
- [Google Search Central: Build and Submit a Sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Ahrefs: XML Sitemaps. The Complete Guide](https://ahrefs.com/blog/xml-sitemap/)
- [Moz: XML Sitemaps](https://moz.com/learn/seo/xml-sitemaps)
