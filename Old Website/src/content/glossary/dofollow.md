---
term: "Dofollow Link"
slug: "dofollow"
definition: "A dofollow link is a standard hyperlink that passes SEO authority (link equity) from one webpage to another, telling search engines to count it as a ranking signal."
category: "SEO"
difficulty: "Beginner"
keyword: "what is a dofollow link"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "nofollow"
  - "backlinks"
  - "link-building"
  - "link-equity"
  - "anchor-text"
---

## What Is a Dofollow Link?

A dofollow link is the default state of any hyperlink on the web. When you create a link without adding any special attributes, search engines treat it as dofollow — meaning they follow it, crawl the destination page, and pass ranking authority (also called "link equity" or "link juice") from the source page to the target page.

Dofollow links are the backbone of Google's original PageRank algorithm. They are how Google discovers new pages, understands relationships between websites, and determines which pages deserve to rank higher in search results.

**The technical reality:** There is no actual `rel="dofollow"` attribute in HTML. Dofollow is simply the absence of `rel="nofollow"`, `rel="sponsored"`, or `rel="ugc"`. If a link has no `rel` attribute, it is dofollow by default.

## Why Dofollow Links Matter

Dofollow links are the single most important off-page ranking factor in SEO. Google's algorithm was built on the principle that a link from one page to another is a vote of trust, authority, and relevance.

**Key statistics:**
- Pages in Google's top 10 results have 3.8x more dofollow backlinks than pages ranking on page 2 (Ahrefs)
- 96.55% of pages on the internet have zero or fewer than 10 dofollow backlinks (Ahrefs, 1B+ page study)
- The average page ranking #1 has 3.5x more dofollow referring domains than the page ranking #10
- A single dofollow link from a high-authority domain can be worth more than 1,000 links from low-quality sites

**What dofollow links actually do:**

1. **Pass ranking authority.** When page A links to page B with a dofollow link, a portion of page A's authority flows to page B. The more authoritative page A is, the more authority is passed.

2. **Help Google discover content.** Google's crawlers follow dofollow links to find new pages. Without dofollow links pointing to your content, Google may never find it — even if you submit a sitemap.

3. **Establish topical relevance.** A dofollow link from a cooking blog to a recipe page tells Google the recipe page is relevant to cooking. A dofollow link from a finance site to the same recipe page sends a weaker relevance signal.

4. **Drive referral traffic.** Dofollow links appear as clickable links on real websites. Real users click them. A dofollow link from a high-traffic blog can send hundreds or thousands of visitors directly to your site.

## How Dofollow Links Work

### The Link Equity Flow

Not all dofollow links pass the same amount of authority. Several factors determine how much equity flows through a link:

| Factor | Impact on Link Value |
|---|---|
| Source domain authority | Higher DA = more equity passed |
| Source page authority | Higher PA = more equity passed |
| Number of outbound links on source page | More links = equity is split (diluted) |
| Link placement | Editorial body content > sidebar/footer |
| Topical relevance | Relevant niche link > irrelevant link |
| Link age | Older, established links often carry more weight |
| Anchor text | Descriptive anchor > generic "click here" |

### PageRank Distribution

Google's original PageRank algorithm worked like this: if a page has a certain amount of authority and links to 10 other pages with dofollow links, each target page receives roughly 1/10th of that authority. If the same page links to 100 pages, each receives roughly 1/100th.

This is why a dofollow link from a page with few outbound links is more valuable than one from a page with hundreds of outbound links.

### Dofollow vs. Nofollow vs. Sponsored vs. UGC

Google introduced additional link attributes in 2019 to better classify links:

| Attribute | Purpose | Passes Authority? |
|---|---|---|
| No `rel` attribute (default) | Standard editorial link | Yes |
| `rel="nofollow"` | Untrusted or unendorsed links | No (since March 2020, treated as a hint) |
| `rel="sponsored"` | Paid or compensated links | No |
| `rel="ugc"` | User-generated content links | No |
| `rel="nofollow sponsored"` | Paid links you don't endorse | No |

**Important change:** Since March 2020, Google treats nofollow as a "hint" rather than a directive. This means Google *may* choose to count some nofollow links for ranking purposes, especially if they appear editorial and high-quality. However, for practical SEO purposes, dofollow links remain the primary source of ranking authority.

## How to Get Dofollow Links

### White-Hat Strategies

**Content that earns links naturally:**
- Original research and data studies
- Comprehensive guides and tutorials
- Free tools and calculators
- Industry benchmarks and reports
- Infographics and visual data

**Proactive link building:**
- Guest posting on relevant blogs (with dofollow author bio links)
- Digital PR and press outreach
- Broken link building
- Resource page link building
- Skyscraper technique (creating better content than competitors)
- HARO (Help A Reporter Out) responses
- Podcast appearances with show notes links

### What to Avoid

- Buying dofollow links from link farms or PBNs
- Excessive link exchanges ("you link to me, I link to you")
- Dofollow links from irrelevant or low-quality sites
- Sitewide footer/sidebar links
- Automated link building tools
- Comment spam with dofollow links

These tactics can trigger Google penalties, including manual actions and algorithmic demotions.

## Common Dofollow Link Mistakes

**Mistake 1: Obsessing over dofollow ratio.**

A natural backlink profile includes a mix of dofollow and nofollow links. Google's John Mueller has stated that a "perfect" ratio does not exist. Focus on earning high-quality links of any type, not just dofollow.

**Mistake 2: Ignoring nofollow links entirely.**

Nofollow links from major publications (Wikipedia, Forbes, NYT) drive referral traffic, build brand authority, and can indirectly improve rankings even without passing direct link equity.

**Mistake 3: Building only homepage links.**

Dofollow links to your homepage help domain authority. But deep links to specific pages (blog posts, product pages, service pages) help those individual pages rank for their target keywords.

**Mistake 4: Over-optimized anchor text.**

If 90% of your dofollow links use exact-match anchor text like "best SEO tools," Google sees this as manipulation. Use natural, varied anchor text: branded anchors, partial match, generic text, and naked URLs.

## How to Check If a Link Is Dofollow

**Method 1: Browser Inspect**
Right-click the link → Inspect Element → Look at the HTML. If there is no `rel` attribute, or if `rel` does not include "nofollow," "sponsored," or "ugc," the link is dofollow.

**Method 2: SEO Browser Extensions**
Tools like MozBar, Ahrefs SEO Toolbar, and SEOquake highlight dofollow vs. nofollow links with different colors.

**Method 3: Crawl Your Backlinks**
Use Ahrefs, Semrush, or Moz to analyze your backlink profile. These tools label each link as dofollow or nofollow and show the ratio in your overall profile.

## Related Terms

- [Nofollow](/glossary/nofollow/)
- [Backlinks](/glossary/backlinks/)
- [Link Building](/glossary/link-building/)
- [Anchor Text](/glossary/anchor-text/)
- [Domain Authority](/glossary/domain-authority/)
