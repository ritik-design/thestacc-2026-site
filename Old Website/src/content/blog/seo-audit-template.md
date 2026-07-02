---
title: "SEO Audit Template: Complete Checklist (2026)"
description: "The complete SEO audit template for 2026. 70+ checklist items across technical, on-page, content, backlinks, and AI search signals. Free to copy and use."
slug: "seo-audit-template"
keyword: "seo audit template"
author: "Stacc Editorial"
date: "2026-04-17"
category: "SEO Tips"
image: "/blogs-preview-images/seo-audit-template.webp"
---

Most SEO audit templates are too vague to be useful. They tell you to "check your meta descriptions" without explaining what a good meta description looks like, what a bad one costs you, or what to do when you find a problem.

This SEO audit template covers all 8 categories of a complete audit. With 70+ actual checklist items you can work through on any site, in any industry. Every item includes what to check, what to look for, and why it matters.

We have audited sites across 70+ industries and published 3,500+ SEO articles. These are the checks that consistently separate ranking sites from stagnant ones.

In this guide, you will find:

- A complete technical SEO audit checklist
- An on-page SEO audit checklist with specific pass/fail criteria
- A content quality audit for both new and existing content
- A backlink and off-page audit checklist
- A local SEO audit section for businesses with physical locations
- An AI search visibility audit (new in 2026)
- A priority framework for fixing what you find

---

## Table of Contents

- [Chapter 1: When to Run an SEO Audit](#ch1)
- [Chapter 2: Technical SEO Audit Checklist](#ch2)
- [Chapter 3: On-Page SEO Audit Checklist](#ch3)
- [Chapter 4: Content Quality Audit](#ch4)
- [Chapter 5: Backlink and Off-Page Audit](#ch5)
- [Chapter 6: Local SEO Audit](#ch6)
- [Chapter 7: AI Search Visibility Audit](#ch7)
- [Chapter 8: How to Prioritize Your Fixes](#ch8)

---

## Chapter 1: When to Run an SEO Audit {#ch1}

An SEO audit is not a once-a-year calendar event. Run one reactively or it will miss issues that are actively costing you traffic right now.

### Scheduled Audits

| Site Type | Recommended Frequency |
|---|---|
| Small site (under 100 pages) | Every 6 months |
| Medium site (100-1,000 pages) | Quarterly |
| Large site (1,000+ pages) | Monthly (automated) + quarterly (manual) |
| E-commerce | Monthly minimum |

### Trigger-Based Audits

Run an immediate audit when any of these occur:

- [ ] Organic traffic drops more than 20% week-over-week
- [ ] A major Google algorithm update rolls out
- [ ] You complete a site redesign or CMS migration
- [ ] You add more than 50 new pages in a month
- [ ] A new competitor appears in your top 5 rankings
- [ ] You merge two websites or change domain names

The [how to do an SEO audit step-by-step guide](/blog/how-to-do-seo-audit) covers the full process if you are running your first one. This checklist assumes you already know the process and need a reference sheet.

### Tools Required

You do not need to pay for tools to complete this audit. Here is the free and paid breakdown:

| Task | Free Tool | Paid Option |
|---|---|---|
| Crawl analysis | Google Search Console | Screaming Frog, Sitebulb |
| Keyword rankings | Google Search Console | Ahrefs, Semrush |
| Backlink analysis | Google Search Console | Ahrefs, Majestic |
| Page speed | PageSpeed Insights | GTmetrix Pro |
| Technical issues | [Website SEO Score checker](/tools/website-seo-score) | DeepCrawl |
| On-page analysis | [On-Page SEO Checker](/tools/on-page-seo-checker) | Surfer SEO |

---

## Chapter 2: Technical SEO Audit Checklist {#ch2}

Technical SEO is the foundation. No amount of good content or backlinks overcomes a site that search engines cannot crawl, index, or render properly.

### Crawlability

- [ ] `robots.txt` file exists at domain.com/robots.txt
- [ ] `robots.txt` does not block any key pages or directories
- [ ] No important pages have `noindex` directives left from staging or development
- [ ] XML sitemap exists and is submitted to Google Search Console
- [ ] Sitemap only contains indexable pages (no 404s, noindex, or redirects)
- [ ] Sitemap is updated automatically when new pages are published
- [ ] Internal links use absolute URLs, not relative paths

**Why it matters:** Google cannot rank what it cannot crawl. Blocked pages or missing sitemaps mean your most important content may never enter the index.

### Indexation

- [ ] Open `site:yourdomain.com` in Google. Indexed pages match expected count
- [ ] No significant indexation gaps (1,000 pages published but only 200 indexed)
- [ ] Duplicate content handled via canonical tags, not just similar pages
- [ ] `www` vs. non-`www` redirects to a single canonical version
- [ ] HTTP redirects to HTTPS for all pages
- [ ] No soft 404 pages (pages returning 200 status with thin/empty content)
- [ ] Check Google Search Console > Pages > Crawled, Not Indexed for patterns

**Common trap:** Staging URLs left indexed after launch. Always block staging environments via `robots.txt` or basic authentication.

---

![Technical SEO audit checklist. Crawlability, indexation, and Core Web Vitals checks for 2026](/images/blog/seo-audit-technical-checklist.png)

---

### Site Speed and Core Web Vitals

- [ ] Run PageSpeed Insights on homepage, category page, and a content page
- [ ] Largest Contentful Paint (LCP): target under 2.5 seconds
- [ ] Cumulative Layout Shift (CLS): target under 0.1
- [ ] Interaction to Next Paint (INP): target under 200ms
- [ ] No render-blocking JavaScript files in `<head>` without `defer` or `async`
- [ ] Images have explicit width and height attributes (prevents CLS)
- [ ] Hero images are preloaded with `<link rel="preload">`
- [ ] Web fonts use `font-display: swap` to prevent invisible text

> According to [Google's PageSpeed Insights data](https://developers.google.com/speed/pagespeed/insights/), pages in the top SERP positions have an average LCP under 2.5s. Pages above 4s face a measurable ranking disadvantage.

### Security and HTTPS

- [ ] SSL certificate is valid and not expiring within 30 days
- [ ] HTTPS enforced on all pages (not just homepage)
- [ ] No mixed content warnings (HTTP resources loaded on HTTPS pages)
- [ ] HSTS header present on server responses
- [ ] No malware or security warnings in Google Search Console

### Mobile and Rendering

- [ ] Site passes Google Mobile-Friendly Test
- [ ] No Flash, iframes, or plugins that do not render on mobile
- [ ] Touch targets are at least 44×44px
- [ ] No horizontal scrolling on mobile viewport
- [ ] JavaScript-dependent content is visible to Googlebot (test via Google's URL Inspection tool)

The [technical SEO checklist](/blog/technical-seo-checklist) covers every item in this section in more detail with tool-by-tool instructions.

> **Stop writing. Start ranking.** Stacc publishes 30 SEO-optimized articles per month. So your content section of every future audit is already handled.
> [Start for $1 →](/pricing)

---

## Chapter 3: On-Page SEO Audit Checklist {#ch3}

On-page SEO determines whether a page is relevant to the queries it needs to rank for. Run this audit on every high-priority page. Homepage, service pages, top-traffic content.

### Title Tags

- [ ] Every page has a unique title tag
- [ ] No title tags truncated in SERP (under 60 characters)
- [ ] Primary keyword appears in title tag, ideally in first 4 words
- [ ] No keyword stuffing (title reads naturally)
- [ ] Branded homepage titles follow format: [Brand Name] – [Primary Value Prop]

### Meta Descriptions

- [ ] Every page has a unique meta description
- [ ] Meta descriptions are 145-155 characters
- [ ] Primary keyword appears in meta description
- [ ] Meta descriptions include a call to action or benefit statement
- [ ] No auto-generated or duplicate meta descriptions

**Note:** Meta descriptions do not directly affect rankings. They affect click-through rate. Which affects rankings indirectly. Treat every meta description as ad copy.

### Header Tags

- [ ] Every page has exactly one H1 tag
- [ ] H1 includes the primary keyword
- [ ] H2s structure the content logically (section titles, not decorative phrases)
- [ ] H3s exist under relevant H2s (not used as standalone subsections)
- [ ] No heading levels skipped (H1 → H2 → H3, not H1 → H3)

### URL Structure

- [ ] URLs are lowercase with hyphens (no underscores, no spaces)
- [ ] URLs are descriptive and include the primary keyword
- [ ] No URLs longer than 75 characters
- [ ] No duplicate content at different URL paths
- [ ] Canonical tag on each page points to the preferred URL

### Internal Linking

- [ ] Every page has at least 2-3 internal links to topically related content
- [ ] Every piece of new content links back to the main category or hub page
- [ ] No orphan pages (pages with zero internal links pointing to them)
- [ ] Anchor text is descriptive (not "click here" or "read more")
- [ ] No more than 1 internal link per anchor text phrase across the site

The [on-page SEO checklist](/blog/on-page-seo-checklist) goes deeper on each of these 32 items.

### Image Optimization

- [ ] All images have descriptive alt text including relevant keywords
- [ ] Alt text describes the image content accurately (not keyword-stuffed)
- [ ] Images use next-gen formats (WebP preferred)
- [ ] No images with file sizes above 200KB on content pages
- [ ] Large images use lazy loading (`loading="lazy"`)

---

## Chapter 4: Content Quality Audit {#ch4}

Google's March 2026 Core Update affected 55% of monitored sites and penalized thin AI content, weak E-E-A-T signals, and pages without verifiable author credentials. Content quality is now an active ranking factor, not just a best practice.

### Content Inventory

- [ ] Identify all pages with fewer than 400 words (flag for consolidation or improvement)
- [ ] Identify all pages with duplicate or near-duplicate content
- [ ] Identify pages that have not been updated in 18+ months
- [ ] Check for cannibalizing content (2+ pages targeting the same keyword)
- [ ] Pages generating traffic that have declining rankings in the last 90 days

### Content Quality Signals

- [ ] Author attribution is present on all content (name, credentials, bio)
- [ ] Factual claims include sources or citations
- [ ] Content covers the topic to the same depth or greater than page-1 competitors
- [ ] No AI-generated boilerplate visible to readers (generic intros, filler summaries)
- [ ] First-hand experience or expertise is demonstrated in the content
- [ ] Content answers the full search intent (not just the head keyword)

**The content audit in depth:** The [how to do a content audit guide](/blog/how-to-content-audit) covers the full 8-step process for inventorying, scoring, and fixing existing content.

### Search Intent Match

- [ ] The page format matches search intent (guide for informational, product page for transactional)
- [ ] The page answers the featured snippet query format (paragraph for "what is", list for "how to", table for "best X")
- [ ] People Also Ask questions are addressed within the content body

### Freshness

- [ ] Date-sensitive content (statistics, prices, tools) has been updated this year
- [ ] Last-updated date is visible to users and accurate
- [ ] Outdated stats or references have been replaced with 2025/2026 data

> **3,500+ blogs published. 92% average SEO score.** Stacc handles the ongoing content production that makes every future content audit clean.
> [See what Stacc does →](/modules/content-seo)

---

## Chapter 5: Backlink and Off-Page Audit {#ch5}

Backlinks remain one of Google's top 3 ranking signals. A backlink audit identifies both opportunities (underused equity, missing links) and risks (toxic links, anchor text patterns that trigger spam filters).

### Backlink Profile Health

- [ ] Run a full backlink export from Google Search Console or Ahrefs
- [ ] Calculate ratio of dofollow to nofollow links (target: 70/30 or higher dofollow)
- [ ] Identify referring domains in your top 20 by domain authority
- [ ] Flag any links from clearly irrelevant or low-quality domains
- [ ] Check for sudden spikes in link acquisition (can signal negative SEO)
- [ ] Verify that your most linked-to pages are your highest-priority pages

### Toxic Link Review

- [ ] Identify links from penalized domains or known link farms
- [ ] Look for patterns in toxic anchors (over-optimized exact match anchors)
- [ ] Disavow confirmed toxic links using Google's Disavow Tool
- [ ] Do NOT disavow links you are unsure about. Disavow should be used conservatively

**Context on disavow:** Most sites do not need to disavow anything. Disavowing healthy links can harm rankings. Only disavow links you are confident are toxic or that Google has flagged explicitly.

The full [backlink audit guide](/blog/backlink-audit-guide) covers the 7-step process for cleaning up a compromised link profile.

### Anchor Text Distribution

- [ ] Check anchor text distribution in your backlink profile
- [ ] Exact match keyword anchors should be under 5% of total anchor text
- [ ] Branded anchors (your domain name or brand name) should be 30-50%
- [ ] Generic anchors ("click here", "this site") are natural. Do not disavow these
- [ ] Phrase-match anchors (partial keyword + filler words) are ideal for the bulk

### Link Acquisition Opportunities

- [ ] Identify competitor backlinks you do not have (Ahrefs Link Intersect)
- [ ] Find unlinked brand mentions across the web
- [ ] Flag broken external links on your site that pointed to high-authority sources
- [ ] Identify content earning links at scale (candidate for republishing/updating)

---

![SEO audit checklist sections. On-page, content, backlinks, local, and AI visibility](/images/blog/seo-audit-sections-overview.png)

---

## Chapter 6: Local SEO Audit {#ch6}

This section applies to any business with a physical location, service area, or Google Business Profile. Skip this chapter if you are a purely national or international brand with no local component.

### Google Business Profile

- [ ] GBP is claimed and verified
- [ ] Business name matches exactly what appears on your website
- [ ] Business category is set to the most specific applicable primary category
- [ ] Secondary categories are added for all relevant service types
- [ ] Business hours are current and reflect holiday schedules
- [ ] Phone number matches the number on your website exactly
- [ ] Website URL links to the correct location page (not just the homepage)
- [ ] 5+ photos of the business exterior, interior, team, and products/services
- [ ] Business description is 750 characters, includes primary keyword naturally

### Citations and NAP Consistency

- [ ] NAP (Name, Address, Phone) is identical across all directories
- [ ] Check top 10 directories: Google, Yelp, Facebook, Bing Places, Apple Maps, YellowPages
- [ ] No duplicate GBP listings for the same location
- [ ] Any outdated citations have been corrected or removed

### Local Reviews

- [ ] Review count meets or exceeds local competitors
- [ ] Average star rating is 4.0 or higher
- [ ] Owner responds to reviews within 72 hours (positive and negative)
- [ ] Reviews mention relevant keywords organically (do not prompt for this)

The complete [local SEO audit guide](/blog/local-seo-audit-guide) covers GBP, citations, on-page local signals, and competitor benchmarking across all 10 steps.

---

## Chapter 7: AI Search Visibility Audit {#ch7}

AI Overviews, Perplexity, ChatGPT web search, and other AI-powered search experiences now account for a growing share of queries that would previously generate a standard SERP click. A 2026 audit that does not check AI visibility is incomplete.

### Featured Snippet Optimization

- [ ] Search your target keywords and check if a featured snippet exists
- [ ] If a snippet exists but belongs to a competitor, analyze its format (paragraph, list, table)
- [ ] Restructure your page to directly answer the query in the snippet format
- [ ] Add a concise definition or direct answer in the first 100 words of the page
- [ ] Use H2/H3 headings that match question-format queries exactly

### Schema Markup

- [ ] Homepage has `Organization` or `LocalBusiness` schema
- [ ] Blog posts have `Article` or `BlogPosting` schema
- [ ] FAQ sections use `FAQPage` schema
- [ ] How-to content uses `HowTo` schema
- [ ] Product or service pages use `Product` or `Service` schema
- [ ] Breadcrumb schema is implemented on all non-homepage pages
- [ ] Validate all schema at schema.org/validator. Zero errors

### AI Crawl Access

- [ ] `robots.txt` does not block GPTBot, ClaudeBot, PerplexityBot, or Google-Extended
- [ ] `llms.txt` file exists at domain.com/llms.txt (emerging standard)
- [ ] Core content is server-rendered (not JavaScript-dependent) for AI crawler access
- [ ] Page structure uses semantic HTML5 elements (`<article>`, `<section>`, `<nav>`)

### E-E-A-T Signals

- [ ] Author pages exist with credentials, expertise indicators, and social profiles
- [ ] About page includes real team information with verifiable credentials
- [ ] Contact information is visible and functional
- [ ] Privacy policy and terms of service are accessible from every page
- [ ] Site earns brand mentions or citations on authoritative third-party sites

> **Rank everywhere. Do nothing.** Blog SEO, Local SEO, and Social on autopilot. Stacc is the content engine behind rankings across 70+ industries.
> [Start for $1 →](/pricing)

---

## Chapter 8: How to Prioritize Your Fixes {#ch8}

Running the audit is straightforward. Knowing what to fix first is where most people get stuck.

Every issue found falls into one of three priority tiers:

### Tier 1: Fix Immediately (this week)

These issues actively prevent ranking or actively lose rankings:

- Pages with `noindex` that should be indexed
- Key pages blocked in `robots.txt`
- Broken internal links on top-traffic pages
- Expired SSL certificate or HTTPS errors
- Google Search Console manual actions (penalties)
- 404 errors on pages with existing backlinks

**Impact:** Fixing Tier 1 issues often produces immediate, measurable ranking recovery.

### Tier 2: Fix This Month

These issues suppress rankings without preventing indexation:

- Missing or duplicate title tags and meta descriptions
- Pages below 400 words that target competitive keywords
- Core Web Vitals failures on key pages
- Toxic backlinks confirmed via manual review
- GBP listing with incorrect information
- Orphan pages with no internal links

**Impact:** Tier 2 fixes produce gradual ranking improvement over 30-90 days.

### Tier 3: Ongoing Optimization

These are improvements that compound over time rather than fix acute problems:

- Building new internal links to underperforming content
- Updating content to include 2026 statistics and examples
- Adding schema markup to existing pages
- Acquiring new referring domains to high-priority pages
- Expanding thin content that ranks on page 2

### The Fix Tracking Template

Document every issue found in this format:

| Issue | URL(s) Affected | Priority | Estimated Fix Time | Status |
|---|---|---|---|---|
| Noindex on /services page | /services | Tier 1 | 5 min | To do |
| Missing title tag | /blog/12-posts | Tier 2 | 2 hrs | In progress |
| Thin content | /blog/old-post | Tier 3 | 4 hrs | Backlog |

Track fixes the same way you track the issues. Improvement is invisible without a before/after benchmark.

For the content side of your Tier 3 fixes. Publishing 30 SEO-optimized articles per month ,  [see the SEO ROI data](/blog/seo-roi-statistics) behind consistent content output at scale.

---

## FAQ

**How long does an SEO audit take?**

A complete audit on a small site (under 100 pages) takes 4-8 hours using this template. A medium site (100-1,000 pages) takes 2-3 days for a thorough manual review. Large sites use automated crawl tools to surface issues, then spend 1-2 days interpreting and prioritizing findings. Your first audit always takes longer than subsequent ones as you learn the site's patterns.

**What is the most important part of an SEO audit?**

Technical crawlability comes first. If Google cannot access and index your pages, no other audit work matters. After technical, on-page fundamentals (title tags, meta descriptions, header structure) affect ranking for every page simultaneously. Content quality and backlinks matter most for competitive keywords where technical and on-page are already solid.

**Do I need paid tools to run an SEO audit?**

No. Google Search Console covers crawl data, indexation issues, keyword rankings, and backlink information for free. Google PageSpeed Insights covers Core Web Vitals. The [free SEO audit tool](/tools/seo-audit) covers on-page and technical surface issues. Paid tools like Ahrefs or Semrush add depth and speed but are not required to complete a thorough audit.

**How often should I run a full SEO audit?**

Quarterly for most sites. Monthly for large sites, e-commerce, or highly competitive industries. Always run an audit immediately after a major algorithm update, a site migration, or a traffic drop above 20%. The items under Chapter 1 of this template cover all the trigger scenarios.

**What is an SEO audit template vs. an SEO audit tool?**

A template is a structured checklist you work through manually or semi-manually. A tool automates the detection of technical issues (crawl errors, broken links, missing tags). The two complement each other. Tools surface issues quickly, templates ensure you cover areas tools miss (content quality, AI visibility, strategy-level gaps). Use both.

**How is this SEO audit different from a content audit?**

An SEO audit covers all ranking factors: technical, on-page, content, backlinks, and local signals. A [content audit](/blog/how-to-content-audit) focuses specifically on your existing content. Scoring every page for performance, intent match, and update priority. A full SEO audit includes a content audit as one chapter.

---

A good SEO audit does not produce a 200-item fix list. It produces a clear Tier 1/2/3 action plan where the highest-impact items are tackled first.

Run through this template quarterly. Track your fixes in the documentation table. The sites that compound rankings consistently are the ones running audits on a schedule. Not just when traffic drops.

The content production side of the audit. Tier 3 ongoing publishing. Is where [Stacc handles the execution](/modules/content-seo). 30 articles per month, fully optimized, automatically delivered.

## Related Tools & Resources

**Free SEO Tools:**
- [Free SEO Audit](/tools/seo-audit/)
- [On-Page SEO Checker](/tools/on-page-seo-checker/)
- [Website SEO Score](/tools/website-seo-score/)

**Best Lists:**
- [Best AI SEO Tools](/best/ai-seo-tools/)
- [Best SEO Automation Tools](/best/seo-automation-tools/)
