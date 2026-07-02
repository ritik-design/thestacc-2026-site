---
term: "Robots.txt"
slug: "robots-txt"
definition: "Robots.txt is a plain-text file at your website's root that instructs search engine crawlers which URLs they can and can't access. Controlling how."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is robots.txt"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "crawling"
  - "indexing"
  - "technical-seo"
  - "xml-sitemap"
  - "meta-robots-tag"
---

## What is Robots.txt?

**Robots.txt is a text file placed at your domain's root directory (yoursite.com/robots.txt) that tells search engine crawlers which pages or sections of your site they're allowed to access.**

Every major search engine. Google, Bing, Yahoo. Checks this file before [crawling](/glossary/crawling) your site. Think of it as a bouncer's list. Not a lock on the door, but a clear set of instructions that well-behaved bots follow.

According to Google's own documentation, Googlebot checks robots.txt before making any request to your server. For sites with thousands of pages, that file becomes one of the most important pieces of your [technical SEO](/glossary/technical-seo) setup.

## Why Does Robots.txt Matter?

Getting your robots.txt wrong can tank your rankings overnight. One misplaced directive and Google can't see your most important pages.

- **Crawl budget protection**. Large sites have limited [crawl budget](/glossary/crawl-budget). Blocking low-value pages (admin panels, staging areas, duplicate filters) keeps Googlebot focused on what matters.
- **Prevents indexing of sensitive areas**. Internal search results, login pages, and cart pages don't belong in the [SERP](/glossary/serp). Robots.txt keeps bots away.
- **Faster discovery of new content**. When crawlers aren't wasting requests on junk pages, they find your new blog posts and product pages faster.
- **Server load management**. Aggressive bots can strain small servers. Blocking unnecessary crawling reduces resource consumption.

If you're publishing content regularly. Whether that's 5 pages or 30 articles a month. You need crawlers spending their time on the right URLs.

## How Robots.txt Works

The file uses a simple syntax. Three core directives handle most use cases.

### User-Agent

This line specifies which crawler the rule applies to. `User-agent: *` targets all bots. `User-agent: Googlebot` targets only Google's crawler. You can stack multiple rules for different bots in the same file.

### Disallow

The `Disallow` directive blocks a specific path. `Disallow: /admin/` prevents crawlers from accessing anything under the /admin/ directory. Leave it blank (`Disallow:`) and you're allowing everything. A single forward slash (`Disallow: /`) blocks the entire site.

### Allow and Sitemap

`Allow` overrides a broader Disallow rule for specific paths. Useful when you block a directory but want one page inside it crawled. The `Sitemap` directive points crawlers to your [XML sitemap](/glossary/xml-sitemap), helping them discover all your important URLs without guessing.

### How Google Processes It

Googlebot fetches your robots.txt before crawling anything else. If the file returns a 200 status, Google follows the rules. A 404 means "no restrictions". Everything gets crawled. A 5xx error makes Google temporarily cautious and limits crawling until the file becomes accessible again.

## Types of Robots.txt Directives

Robots.txt directives fall into 4 main categories:

- **Access directives (Allow/Disallow)**. Control which paths bots can visit. The foundation of every robots.txt file.
- **User-agent directives**. Target rules at specific bots. You might block SEMrushBot while allowing Googlebot full access.
- **Crawl-delay directives**. Tell bots to wait between requests. Google ignores this (use Google Search Console instead), but Bing and Yandex respect it.
- **Sitemap directives**. Point to your sitemap file. Not technically a "rule," but a discovery mechanism bots rely on.

Most small-to-medium sites only need access directives and a sitemap reference. Crawl-delay matters more for large-scale sites with server constraints.

## Robots.txt Examples

**Example 1: Local plumbing company**
A plumber in Austin has a WordPress site with /wp-admin/, /cart/, and /internal-pricing/ directories. Their robots.txt blocks all three and includes a sitemap reference. Result: Googlebot spends its time on service pages and blog posts. Not admin panels.

**Example 2: eCommerce store with filtered pages**
An online retailer has 50 products but 3,000 filter combinations (size + color + price). Without robots.txt blocking `/products?filter=`, Googlebot wastes [crawl budget](/glossary/crawl-budget) on duplicate filtered pages. One Disallow line fixes it.

**Example 3: Accidentally blocking the entire site**
A marketing agency moved from staging to production and left `Disallow: /` in robots.txt. For 3 weeks, nothing got [indexed](/glossary/indexing). Traffic dropped to zero. One character caused it. The forward slash after Disallow.

## Robots.txt vs Meta Robots Tag

These two do different jobs at different stages. Robots.txt stops crawlers before they reach a page. The [meta robots tag](/glossary/meta-robots-tag) gives instructions after a crawler has already accessed it.

| | Robots.txt | Meta Robots Tag |
|---|---|---|
| **Where it lives** | Root directory file | HTML `<head>` of individual pages |
| **When it acts** | Before crawling | After crawling |
| **Scope** | Entire directories or paths | Individual pages |
| **Can prevent indexing?** | No. Only prevents crawling | Yes ,  `noindex` removes from search |
| **Best for** | Blocking sections of a site | Removing specific pages from search |

Here's the catch: if you block a page with robots.txt, Google can't see a noindex tag on that page. So the page might still appear in search results (with no snippet) because Google found a link to it elsewhere. To truly remove a page from search, use the meta robots tag. Not robots.txt.

## Robots.txt Best Practices

- **Always include a Sitemap directive**. Point to your [XML sitemap](/glossary/xml-sitemap) so crawlers have a complete map of your site. One line: `Sitemap: https://yoursite.com/sitemap.xml`.
- **Never block CSS or JavaScript files**. Google needs to render your pages to understand them. Blocking these resources hurts your [on-page SEO](/glossary/on-page-seo).
- **Test before deploying**. Use Google Search Console's robots.txt tester to check your rules. A typo can block your entire site.
- **Review quarterly**. As your site grows, new directories appear. What made sense 6 months ago might be blocking important content today.
- **Pair with a content strategy**. Robots.txt manages what gets crawled, but you still need pages worth crawling. Services like theStacc publish 30 SEO-optimized articles per month, giving Googlebot fresh content to discover on every visit.

## Frequently Asked Questions

### Does robots.txt stop pages from appearing in Google?

Not directly. Robots.txt prevents crawling, not [indexing](/glossary/indexing). If other sites link to a blocked page, Google may still show it in results. Just without a description snippet. Use a noindex meta tag to fully remove a page from search.

### Where do I put my robots.txt file?

Place it at your domain's root: `https://yoursite.com/robots.txt`. Subdirectory placement doesn't work. Each subdomain needs its own robots.txt file.

### Can robots.txt improve my rankings?

Indirectly, yes. Blocking low-value pages preserves crawl budget for your important content. On large sites, this means faster discovery and indexing of new pages. Which can speed up ranking improvements.

### Do all bots follow robots.txt rules?

Legitimate search engine bots (Googlebot, Bingbot) respect robots.txt. Malicious bots and scrapers typically ignore it. Don't rely on robots.txt for security. It's a guideline, not a firewall.

---

Want to make sure your SEO content actually gets crawled and ranked? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Robots.txt Specifications](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [Google Search Central: How Google Interprets Robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt)
- [Moz: Robots.txt. Learn SEO](https://moz.com/learn/seo/robotstxt)
- [Ahrefs: Robots.txt. The Ultimate Guide](https://ahrefs.com/blog/robots-txt/)
