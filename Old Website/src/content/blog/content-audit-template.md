---
title: "Content Audit Template: The Complete 2026 Guide"
description: "Use this content audit template to inventory, score, and fix every page on your site. Includes a free spreadsheet structure, scoring rubric, and action framework."
slug: "content audit template"
keyword: "content audit template"
author: "Stacc Editorial"
date: "2026-05-26"
category: "Content Strategy"
image: "/blogs-preview-images/content-audit-template.png"
---

# Content Audit Template: The Complete 2026 Guide

Most websites sit on a graveyard of outdated blog posts, competing pages, and thin content that drags down every new article you publish.

A content audit fixes this. It is the single highest-ROI activity in SEO. Single Grain updated 42 posts over six months and saw a 96% traffic increase, according to their published case study. The posts that already had traction contributed to 85% of that gain.

This guide gives you a complete content audit template. You will learn how to build your inventory, score every page, and turn the results into a prioritized action plan. We publish 3,500+ blogs across 70+ industries. This is the exact process we use.

Here is what you will learn:

- How to build a content inventory in under 2 hours
- A 100-point scoring rubric that removes guesswork
- The 4-action decision matrix: Keep, Update, Merge, Remove
- How to prioritize fixes for maximum traffic impact
- A downloadable spreadsheet structure you can use today

---

## What Is a Content Audit Template

A content audit template is a structured spreadsheet used to inventory, evaluate, and prioritize every piece of content on a website. It turns subjective opinions about "quality" into objective scores that drive action.

Without a template, audits become chaotic. Teams argue about which posts matter. Decisions stall. Months pass with no changes. A template forces consistency. Every page gets scored against the same criteria. Every score leads to a clear action.

The template has three core components:

1. **Inventory sheet** — Every URL, title, content type, and publish date
2. **Performance data** — Traffic, rankings, backlinks, conversions
3. **Scoring and action columns** — Quality scores and recommended next steps

Most teams stop at step 2. They collect data but never turn it into decisions. The scoring and action columns are where the real value lives.

---

## Why You Need a Content Audit Now

Google released four core updates in the first five months of 2026. The March update hit 55% of tracked domains, according to data from [Digital Applied](https://www.digitalapplied.com/blog/google-march-2026-core-update-impact-analysis-recovery). Sites with thin AI-generated content saw 60% to 80% traffic drops. Sites with strong E-E-A-T signals gained 23% visibility.

The rules have changed. Content that ranked in 2024 may be a liability today. Our [content refresh strategy guide](/blog/content-refresh-strategy/) covers how to systematically update aging posts before they become problems.

Here are the signals that you need an audit:

- Organic traffic has plateaued or declined for 3+ months
- Multiple pages target the same keyword
- Conversion pages get traffic but few conversions
- Your blog has posts older than 18 months with no updates
- New content takes months to rank

The cost of inaction is compounding. Every weak page dilutes your site's authority. Every outdated post trains Google to crawl your site less often. Every competing page splits the ranking potential that one strong page could capture.

---

## The Content Audit Template Structure

This is the exact spreadsheet structure we use at Stacc. It works for sites with 50 pages or 50,000.

### Master Inventory Columns

| Column | What to Enter | Data Source |
|---|---|---|
| URL | Full canonical URL, no parameters | Screaming Frog, sitemap |
| Page Title | H1 or title tag | Screaming Frog, manual |
| Content Type | Blog, landing page, product, guide | Manual |
| Primary Keyword | Main query the page targets | Ahrefs, Semrush, GSC |
| Search Intent | Informational, commercial, transactional, navigational | Manual |
| Publish Date | Original publication date | CMS export |
| Last Updated | Most recent meaningful revision | CMS export |
| Organic Sessions (90d) | Clicks from organic search | Google Analytics 4 |
| Pageviews (90d) | Total page views | Google Analytics 4 |
| Avg. Time on Page | Average engagement time | Google Analytics 4 |
| Bounce Rate | Percentage of single-page sessions | Google Analytics 4 |
| Impressions (90d) | Search appearances | Google Search Console |
| Clicks (90d) | Search clicks | Google Search Console |
| Avg. Position | Average ranking position | Google Search Console |
| CTR | Click-through rate from search | Google Search Console |
| Backlinks | Total referring links | Ahrefs, Semrush |
| Referring Domains | Unique linking domains | Ahrefs, Semrush |
| Conversions (90d) | Goal completions or events | Google Analytics 4 |

### Scoring Columns

| Column | Scale | How to Score |
|---|---|---|
| Intent Match | 0-20 | Does the content match what searchers want? |
| Topical Depth | 0-20 | Does it cover subtopics, examples, and details? |
| Freshness and Accuracy | 0-15 | Are claims, stats, and screenshots current? |
| On-Page SEO Quality | 0-15 | Strong title alignment, clear headings, internal links? |
| Conversion Clarity | 0-15 | Is the CTA specific and relevant to intent? |
| Effort-to-Impact | 0-15 | Are clear, realistic improvements possible? |
| **Total Score** | **0-100** | **Sum of all dimensions** |

### Action Columns

| Column | Options | When to Use |
|---|---|---|
| Recommended Action | Keep, Update, Merge, Remove | Based on total score and traffic data |
| Target URL (if merging) | Canonical destination page | When consolidating competing pages |
| Internal Links to Add | Related page URLs | Cross-link opportunities identified |
| Owner | Team member name | Who implements the fix |
| Due Date | Specific date | When the fix must be complete |
| Notes | Specific edit instructions | What exactly needs to change |

### Score-to-Action Thresholds

| Total Score | Action | Timeline |
|---|---|---|
| 80-100 | Keep and monitor | Review quarterly |
| 60-79 | Update this quarter | 30-60 days |
| 40-59 | Merge or major rewrite | 60-90 days |
| 0-39 | Remove or redirect | 30 days |

The exception is pages with high backlink counts. A page scoring 35 but with 50+ referring domains should be merged, not deleted. The link equity matters.

---

## How to Build Your Content Inventory

### Step 1: Export Every Indexable URL

Start with a complete list of every page Google can crawl. Do not guess. Do not use your CMS post list alone. That misses orphan pages, old redirects, and technical edge cases.

Use one of these methods:

**Option A: [Screaming Frog](https://www.screamingfrog.co.uk/seo-spider/) (most thorough)**

- Crawl your site with Screaming Frog SEO Spider
- Filter to HTML pages with 200 status codes
- Export the URL, title, meta description, and word count columns
- The free version handles up to 500 URLs

**Option B: XML Sitemap**

- Download your sitemap from `/sitemap.xml`
- Parse the URL list with a spreadsheet formula or script
- Cross-reference with Google Search Console coverage report
- Add any indexed pages missing from the sitemap

**Option C: Google Search Console**

- Go to Performance > Search Results
- Set date range to last 16 months
- Export the query report with page URLs
- This captures only pages with impressions, but that is your starting priority

### Step 2: Pull Performance Data

Import metrics from three sources. Use VLOOKUP or INDEX/MATCH to populate your template automatically.

**[Google Analytics 4](https://analytics.google.com/):**

- Go to Engagement > Pages and Screens
- Set date range to last 90 days
- Export: page path, sessions, users, average engagement time, bounce rate

**[Google Search Console](https://search.google.com/search-console):**

- Go to Performance > Search Results
- Set date range to last 90 days
- Filter by page and export: impressions, clicks, CTR, average position

**[Ahrefs](https://ahrefs.com/) or [Semrush](https://www.semrush.com/):**

- Enter your domain in Site Explorer
- Go to Organic Search > Top Pages
- Export: URL, traffic, keywords, backlinks, referring domains

### Step 3: Categorize Content by Type and Intent

Add two manual columns: Content Type and Search Intent. This step takes 30 minutes but transforms how you prioritize.

**Content types to track:**

- Blog post
- Landing page
- Product page
- Category page
- Guide or resource
- Case study
- About or team page
- Contact page

**Search intent categories:**

- **Informational** — "how to," "what is," "guide"
- **Commercial** — "best," "top," "vs," "review"
- **Transactional** — "buy," "price," "discount," "free trial"
- **Navigational** — brand names, specific page searches

Intent mismatch is the most common content problem we see. A transactional query served by an informational blog post will not convert. A commercial query served by a product page with no comparison data will not rank. Our guide on [how to write blog posts that rank](/blog/write-blog-post-ranks/) explains how to align content structure with search intent from the start.

---

## How to Score Content Quality

Scoring removes opinion from the audit. Two team members should score the same page within 10 points of each other. If they do not, your rubric is too vague.

### Dimension 1: Intent Match (0-20 points)

Does the content match what the searcher wants?

| Score | Criteria |
|---|---|
| 16-20 | The page perfectly matches search intent. A searcher would find exactly what they expected. |
| 11-15 | The page mostly matches intent but misses one key element. |
| 6-10 | The page partially matches intent. The searcher would need to visit another page. |
| 0-5 | The page mismatches intent entirely. The searcher would bounce immediately. |

**Example:** A page targeting "best CRM for small business" should compare options, list pros and cons, and include pricing. A 2,000-word guide about "what is a CRM" would score 0-5 for intent match. The searcher wants a comparison, not a definition.

### Dimension 2: Topical Depth (0-20 points)

Does the content cover the topic thoroughly?

| Score | Criteria |
|---|---|
| 16-20 | Covers all major subtopics with specific examples, data, and implementation details. |
| 11-15 | Covers most subtopics but lacks depth in one or two areas. |
| 6-10 | Covers surface-level information only. No examples or specifics. |
| 0-5 | Extremely thin. Could be replaced by a 3-sentence AI summary. |

**Example:** A page about "content audit template" should cover inventory building, scoring rubrics, action frameworks, and tool recommendations. A page that only defines what a content audit is would score 0-5. Our guide on [building topical authority](/blog/build-topical-authority/) explains how to create content that covers a subject in depth.

### Dimension 3: Freshness and Accuracy (0-15 points)

Are claims, statistics, screenshots, and examples current?

| Score | Criteria |
|---|---|
| 13-15 | All stats are from the last 12 months. All screenshots match current interfaces. All links work. |
| 9-12 | Most stats are current. One or two outdated references. |
| 5-8 | Several outdated stats or broken links. Screenshots from old product versions. |
| 0-4 | Heavily outdated. References tools that no longer exist. Stats from 3+ years ago. |

### Dimension 4: On-Page SEO Quality (0-15 points)

Is the page technically optimized?

Check these elements:

- [ ] Title tag includes primary keyword and stays under 60 characters
- [ ] Meta description includes keyword and stays under 155 characters
- [ ] H1 matches or closely aligns with the title tag
- [ ] URL is short, descriptive, and includes the keyword
- [ ] Heading structure uses H2s and H3s logically
- [ ] Images have descriptive alt text
- [ ] Internal links point to relevant related pages
- [ ] Page loads in under 3 seconds
- [ ] Mobile formatting is clean with no horizontal scrolling
- [ ] Schema markup is present and valid

Score 1.5 points per checked item. For a deeper technical review, use our [blog SEO audit checklist](/blog/blog-seo-audit-checklist/).

### Dimension 5: Conversion Clarity (0-15 points)

Does the page guide the reader toward a specific next step?

| Score | Criteria |
|---|---|
| 13-15 | Clear CTA relevant to the page intent. Multiple conversion paths. Social proof near CTA. |
| 9-12 | One clear CTA. Relevant to intent but no supporting proof. |
| 5-8 | Weak or generic CTA. "Contact us" on an informational post. |
| 0-4 | No CTA. The reader has nowhere to go. |

### Dimension 6: Effort-to-Impact (0-15 points)

How much improvement can realistic edits produce?

| Score | Criteria |
|---|---|
| 13-15 | Small edits would produce large gains. Missing one subtopic. Weak title only. |
| 9-12 | Moderate edits would produce moderate gains. Needs expansion and updates. |
| 5-8 | Major rewrite required. Thin foundation with little to build on. |
| 0-4 | No amount of editing would save this page. Start from scratch or remove. |

---

## The 4-Action Decision Matrix

Every page gets one of four actions. No maybes. No "review later." Decide now.

### Action 1: Keep

Pages scoring 80+ with stable or growing traffic. These are your winners. Monitor them quarterly but do not touch them unless something changes.

**Criteria for Keep:**

- Total score: 80-100
- Organic traffic: Stable or growing over 90 days
- Rankings: Position 1-10 for primary keyword
- Backlinks: 10+ referring domains
- Conversions: Above site average for content type

**What to do:**

- Add to a "watch list" spreadsheet
- Set a calendar reminder to review in 90 days
- Note any seasonal trends that might affect future performance

### Action 2: Update

Pages scoring 60-79 with existing traffic or ranking potential. These are your highest-ROI fixes. Small improvements produce measurable gains because the page already has authority.

**Criteria for Update:**

- Total score: 60-79
- Organic traffic: Declining or plateaued
- Rankings: Position 4-20 for primary keyword
- Backlinks: 5+ referring domains
- Age: Last updated 6+ months ago

**What to do:**

- Refresh all statistics and examples
- Expand thin sections with new subtopics
- Improve the title and meta description
- Add internal links to newer related content
- Update or add schema markup
- Set a 30-60 day deadline

### Action 3: Merge

Pages scoring 40-59 that target the same keyword as another page. These create [keyword cannibalization](/blog/what-is-keyword-cannibalization/). Two mediocre pages competing for the same query will not outrank one strong page. Our [content pruning guide](/blog/content-pruning-guide/) walks through the merge process in detail.

**Criteria for Merge:**

- Total score: 40-59
- Keyword overlap: Another page on your site targets the same term
- Traffic: Low but not zero
- Backlinks: Some referring domains worth preserving

**What to do:**

- Identify the stronger page (higher score, more traffic, more backlinks)
- Move the best content from the weaker page into the stronger one
- Add a 301 redirect from the weaker URL to the stronger one
- Update internal links that pointed to the old URL
- Set a 60-90 day deadline

### Action 4: Remove

Pages scoring 0-39 with no traffic, no backlinks, and no path to improvement. These drag down your site quality signals. Google crawls them, finds nothing valuable, and reduces crawl budget for the rest of your site.

**Criteria for Remove:**

- Total score: 0-39
- Organic traffic: Under 10 sessions in 90 days
- Backlinks: 0-2 referring domains
- Age: Published 12+ months ago with no updates
- Effort-to-impact: 0-4

**Critical exception:** Never delete a page with meaningful backlinks. Even 5 referring domains from decent sites are worth preserving. Merge those pages instead. Only remove pages with zero or near-zero link equity. Our [backlink audit guide](/blog/backlink-audit-guide/) explains how to evaluate which links are worth preserving.

**What to do:**

- Export the content before deleting (some teams repurpose it later)
- Implement a [301 redirect](/blog/301-redirects-guide/) to the most relevant remaining page
- Remove internal links pointing to the deleted URL
- Submit the updated [sitemap](/blog/create-xml-sitemap/) to Google Search Console
- Set a 30-day deadline

---

## How to Prioritize Your Fixes

You will not fix everything at once. A site with 500 pages might have 80 Update actions, 40 Merge actions, and 30 Remove actions. That is months of work. Prioritize by impact.

### Priority 1: Revenue-Adjacent Pages

Start with pages that directly drive leads, sales, or conversions. A landing page with 1,000 monthly sessions and a 0.5% conversion rate produces 5 conversions. Improving that to 1.5% triples output without adding traffic.

**Filter your template:**

- Content type = Landing page or Product page
- Conversions (90d) = Greater than 0
- Recommended action = Update

### Priority 2: Pages in Positions 4-10

Pages ranking on page 1 but not in the top 3 have the easiest path to more traffic. A move from position 8 to position 3 can increase clicks by 300% or more.

**Filter your template:**

- Avg. position = 4.0 to 10.0
- Organic sessions = Greater than 50 in 90 days
- Recommended action = Update

### Priority 3: Pages with Backlinks but Low Scores

Pages with 10+ referring domains but scores under 60 are wasted assets. The links say the page matters. The content says it does not. A rewrite on this foundation outperforms a new post every time.

**Filter your template:**

- Referring domains = 10+
- Total score = Under 60
- Recommended action = Update or Merge

### Priority 4: Keyword Cannibalization Clusters

When three blog posts target "content marketing strategy," none of them rank well. Consolidating into one definitive guide almost always produces a ranking jump within 60 days.

**Filter your template:**

- Primary keyword = Duplicate entries
- Recommended action = Merge

---

## Sample Content Audit Template Spreadsheet

Here is a concrete example with real data patterns. Use this as your starting format.

| URL | Type | Primary Keyword | Intent | Organic Sessions | Avg. Position | Backlinks | Score | Action | Due Date |
|---|---|---|---|---|---|---|---|---|---|
| /blog/content-marketing-strategy/ | Blog | content marketing strategy | Informational | 1,240 | 5.2 | 34 | 78 | Update | 2026-06-15 |
| /blog/content-marketing-tips/ | Blog | content marketing strategy | Informational | 89 | 18.4 | 3 | 42 | Merge | 2026-07-01 |
| /blog/what-is-content-marketing/ | Blog | what is content marketing | Informational | 2,100 | 3.1 | 56 | 88 | Keep | Quarterly |
| /services/seo/ | Landing | seo services | Commercial | 340 | 8.7 | 12 | 65 | Update | 2026-06-30 |
| /blog/old-post-2019/ | Blog | outdated topic | Informational | 3 | 45.0 | 0 | 22 | Remove | 2026-06-10 |
| /blog/content-audit-guide/ | Blog | content audit | Informational | 567 | 6.8 | 19 | 72 | Update | 2026-06-20 |

Notice how the two posts targeting "content marketing strategy" have very different scores and traffic. The Merge action for the weaker post is obvious once the data is visible.

---

## Tools to Speed Up Your Audit

You do not need expensive software to run an effective audit. Here is what we recommend at each budget level.

### Free Tool Stack

| Tool | Purpose | Cost |
|---|---|---|
| [Google Search Console](https://search.google.com/search-console) | Rankings, impressions, CTR, indexing status | Free |
| [Google Analytics 4](https://analytics.google.com/) | Traffic, engagement, conversions | Free |
| [Screaming Frog](https://www.screamingfrog.co.uk/seo-spider/) | URL crawling, technical data | Free (500 URLs) |
| Google Sheets | Template and scoring | Free |
| [PageSpeed Insights](https://pagespeed.web.dev/) | Core Web Vitals, load speed | Free |

### Paid Tool Stack

| Tool | Purpose | Cost |
|---|---|---|
| [Ahrefs](https://ahrefs.com/) | Backlinks, keyword rankings, traffic estimates | From $99/mo |
| [Semrush](https://www.semrush.com/) | Keyword tracking, site audits, content analysis | From $129/mo |
| [Screaming Frog](https://www.screamingfrog.co.uk/seo-spider/) | Full-site crawling, unlimited URLs | From $259/year |
| [Surfer SEO](https://surferseo.com/) | Content scoring, optimization suggestions | From $89/mo |

For a detailed comparison of SEO platforms, see our [Ahrefs vs Semrush analysis](/compare/ahrefs-vs-semrush/).

### Stacc Alternative

If you do not have time to run audits manually, [Stacc handles this for you](/pricing). We publish optimized blog posts, local SEO content, and social media updates on a fixed monthly schedule. Your content stays fresh without the audit overhead. Our [content calendar template](/blog/content-calendar-template/) shows how we plan publication schedules that prevent content decay before it starts.

---

## Measuring Results After Your Audit

An audit without follow-up measurement is just data collection. Track these metrics at 30, 60, and 90 days after implementation.

### Traffic Metrics

- **Organic sessions** — Total visits from search
- **Organic users** — Unique visitors from search
- **Pages per session** — Are visitors exploring more content?
- **Average engagement time** — Are visitors staying longer?

### Ranking Metrics

- **Average position** — Overall ranking trend across all tracked keywords
- **Keywords in positions 1-3** — Your money positions
- **Keywords in positions 4-10** — Your quick-win positions
- **Total ranking keywords** — Is your footprint expanding?

### Conversion Metrics

- **Goal completions** — Form fills, sign-ups, purchases
- **Conversion rate by page** — Which updated pages converted best?
- **Revenue per visitor** — Is traffic quality improving?

### Content Health Metrics

- **Pages with scores under 60** — Should trend toward zero
- **Average content score** — Should trend upward
- **Pages updated in last 90 days** — Should be 20% or more of your library

---

## Common Content Audit Mistakes

Even experienced SEOs make these errors. Avoid them.

### Mistake 1: Auditing Without a Goal

"Fix our content" is not a goal. "Increase organic traffic by 25% in 90 days by updating pages scoring 60-79 that rank in positions 4-15" is a goal. Every decision in your audit should connect to a specific outcome.

### Mistake 2: Scoring Based on Gut Feel

"This post feels thin" is not a score. Use the rubric. If two team members score the same page more than 10 points apart, your criteria are too vague. Refine them.

### Mistake 3: Ignoring Search Intent

A 5,000-word guide about "what is a CRM" will not rank for "best CRM for small business." Intent mismatch kills more content than thinness. Check intent before you check word count. Our [blog post structure guide](/blog/blog-post-structure-seo/) shows how to build content that matches what searchers actually want.

### Mistake 4: Deleting Pages with Backlinks

This is the most expensive mistake in content auditing. A page with 20 referring domains has link equity that took months or years to build. Merge it. Never delete it. See our [backlink audit guide](/blog/backlink-audit-guide/) for evaluating link quality before making removal decisions.

### Mistake 5: Updating Without Redirecting Old URLs

When you merge two posts, the old URL must [301 redirect](/blog/301-redirects-guide/) to the new one. If you simply unpublish the old post, you lose the link equity and create [404 errors](/blog/404-error-seo/) that waste crawl budget.

### Mistake 6: Stopping After One Audit

Content audits are not one-time projects. They are a recurring discipline. We recommend:

- **Full audit:** Quarterly
- **Quick traffic review:** Monthly
- **Post-algorithm update:** Immediate
- **After major site changes:** Immediate

---

## Content Audit Checklist

Use this checklist to run your audit from start to finish.

### Phase 1: Preparation

- [ ] Define your audit goal (traffic, conversions, rankings)
- [ ] Choose your tool stack
- [ ] Create the spreadsheet template
- [ ] Set a deadline for completion

### Phase 2: Data Collection

- [ ] Export all indexable URLs
- [ ] Pull GA4 traffic data (90 days)
- [ ] Pull GSC ranking data (90 days)
- [ ] Pull backlink data from Ahrefs or Semrush
- [ ] Categorize each page by type and intent

### Phase 3: Scoring

- [ ] Score every page on Intent Match (0-20)
- [ ] Score every page on Topical Depth (0-20)
- [ ] Score every page on Freshness (0-15)
- [ ] Score every page on On-Page SEO (0-15)
- [ ] Score every page on Conversion Clarity (0-15)
- [ ] Score every page on Effort-to-Impact (0-15)
- [ ] Calculate total scores

### Phase 4: Action Planning

- [ ] Assign Keep/Update/Merge/Remove to every page
- [ ] Prioritize by revenue impact and ranking potential
- [ ] Assign owners and due dates
- [ ] Identify internal link opportunities
- [ ] Plan [301 redirects](/blog/301-redirects-guide/) for merged and removed pages

### Phase 5: Implementation

- [ ] Update Priority 1 pages first
- [ ] Merge competing pages with 301 redirects
- [ ] Remove low-value pages with 301 redirects
- [ ] Add internal links between related content
- [ ] Submit updated sitemap to Google Search Console

### Phase 6: Measurement

- [ ] Record baseline metrics before changes
- [ ] Check metrics at 30, 60, and 90 days
- [ ] Compare actual results to your goal
- [ ] Document lessons for the next audit

---

## Frequently Asked Questions

**How often should I run a content audit?**

Run a full audit quarterly. Run a quick traffic review monthly. Run an immediate audit after any Google core update or major site change. Sites publishing 10+ posts per month may need monthly full audits.

**How long does a content audit take?**

A 100-page site takes 4-6 hours to audit. A 1,000-page site takes 2-3 days. A 10,000+ page site requires automation tools and may take 1-2 weeks. The scoring phase takes the most time. Data collection is mostly automated.

**What is the difference between a content audit and a content inventory?**

An inventory is a list of what you have. An audit evaluates what you have and decides what to do with it. You cannot audit without inventorying first, but inventorying without auditing is just data collection.

**Should I audit my entire site or focus on one section?**

Start with your highest-traffic section. If your blog drives 80% of organic traffic, audit the blog first. If your product pages drive conversions, audit those first. A partial audit that produces action beats a full audit that never gets finished.

**Can I use AI to speed up content auditing?**

Yes, but with limits. AI can help categorize content, suggest internal links, and draft update briefs. AI cannot accurately score intent match or conversion clarity without deep knowledge of your audience and business. Use AI for data processing, not for final scoring decisions. Our [AI content audit fix guide](/blog/ai-content-audit-fix/) covers how to use AI tools responsibly as part of your audit workflow.

**What should I do with pages that have zero traffic but high backlinks?**

Merge them. Move the content into a stronger page on a related topic. Implement a 301 redirect. The backlinks pass their equity to the destination page. Never delete a page with meaningful backlinks.

**How do I handle pages with seasonal traffic?**

Flag them in your template with a "Seasonal" note. Score them based on their peak performance period, not their current traffic. A holiday gift guide with zero traffic in June may be your top performer in November. Do not remove seasonal content during its off-season.

**What metrics matter most for a content audit?**

Organic traffic, average position, and conversions matter most. Backlinks matter for deciding between Merge and Remove. Engagement time and bounce rate matter for identifying Update candidates. Ignore vanity metrics like total word count or number of images. For more on tracking the right metrics, see our [content marketing KPIs guide](/blog/content-marketing-kpis/).

---

## Key Takeaways

- A content audit template turns subjective opinions into objective scores
- The 100-point rubric covers intent, depth, freshness, SEO, conversions, and effort
- Every page gets one of four actions: Keep, Update, Merge, or Remove
- Prioritize by revenue impact and ranking potential, not by personal preference
- Never delete pages with backlinks. Merge them instead.
- Run full audits quarterly and quick reviews monthly

Content audits are not glamorous. They are work. But they produce results that new content creation cannot match. Updated posts with existing authority outrank new posts 9 times out of 10. For a data-backed look at how updates affect rankings, read our [content updates and rankings study](/blog/content-updates-rankings-study/).

> **Stop letting old content drag down your rankings.** Stacc publishes fresh, optimized content across blog, local SEO, and social channels — so your site stays current without the manual audit overhead.
> [Start for $1 →](/pricing)
