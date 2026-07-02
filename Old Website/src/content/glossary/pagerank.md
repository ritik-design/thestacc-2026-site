---
term: "PageRank"
slug: "pagerank"
definition: "PageRank is Google's original algorithm for measuring the importance of web pages based on the quantity and quality of links pointing to them. Named after."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is pagerank"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "backlinks"
  - "link-building"
  - "domain-authority"
  - "link-equity"
  - "off-page-seo"
---

## What is PageRank?

PageRank is Google's foundational algorithm that scores the importance of a web page based on the number and quality of other pages linking to it.

Larry Page and Sergey Brin developed it at Stanford in 1998. The core idea was borrowed from academic citation analysis: a research paper cited by many other papers is probably important. A paper cited by *important* papers is even more important. PageRank applied that same logic to the web. Every link from Page A to Page B passes a portion of Page A's importance. What SEOs now call [link equity](/glossary/link-equity).

Google stopped publicly updating PageRank scores in 2016 and removed the toolbar that displayed them. But the algorithm itself. Or evolved versions of it. Still runs inside Google's ranking systems. A 2017 Google patent filing confirmed they continue using a "modified PageRank" as part of their link evaluation. Links still matter. The math just isn't visible anymore.

## Why Does PageRank Matter?

Even though the public toolbar is dead, the principle behind PageRank shapes modern SEO more than almost any other concept.

- **[Backlinks](/glossary/backlinks) remain a top-3 ranking factor**. Multiple correlation studies (Ahrefs, Backlinko, Semrush) consistently show that pages with more high-quality backlinks rank higher. PageRank is *why*.
- **Not all links are equal**. A single link from The New York Times passes more PageRank than 1,000 links from unknown blogs. Quality over quantity. That distinction comes directly from the PageRank model.
- **[Internal linking](/glossary/internal-link) distributes PageRank across your site**. Every internal link passes PageRank from one page to another within your domain. Strategic internal linking can boost important pages without earning a single external link.
- **PageRank decay means orphan pages starve**. Pages with no links pointing to them receive zero PageRank. [Orphan pages](/glossary/orphan-page) are effectively invisible to this system.

Understanding PageRank changes how you think about every link on your site. Inbound, outbound, and internal.

## How PageRank Works

The original algorithm uses a surprisingly elegant formula. Here's how it operates conceptually.

### The Voting Model

Imagine every page on the web starts with an equal share of importance. When Page A links to Page B, it passes a fraction of its importance to Page B. If Page A links to 5 pages, each link passes roughly 1/5 of Page A's available PageRank. Pages that receive lots of votes. Especially from pages that themselves have high scores. Accumulate more PageRank.

### The Damping Factor

The original formula includes a "damping factor" (typically set at 0.85). This models the probability that a random person clicking links will eventually stop and start over on a random page. It prevents PageRank from concentrating infinitely on pages with lots of incoming links. The damping factor is why even well-linked pages don't have unlimited authority.

### Iterative Calculation

PageRank isn't calculated once. The algorithm runs in loops. Recalculating every page's score based on updated scores from the previous round. After enough iterations, scores converge. In practice, Google recalculates continuously as it discovers new links and pages.

### Link Dilution

Here's what most people miss: a page splits its PageRank among all outgoing links. A page with 2 outgoing links passes more per link than a page with 200 outgoing links. That's why links from pages with few outbound links are more valuable. Each one carries a bigger share of PageRank.

## Types of PageRank

PageRank concepts have evolved beyond the original algorithm:

- **Classic PageRank**. The original 1998 algorithm, scored 0-10 on the Google Toolbar. Publicly visible until 2016. Simple, link-count-based.
- **Topic-Sensitive PageRank**. A Google research variant that weights links differently based on topical relevance. A link from a dental site to another dental site passes more "topical PageRank" than a link from an unrelated cooking blog. This is likely part of how Google evaluates [topical authority](/glossary/topical-authority).
- **Toolbar PageRank (deprecated)**. The 0-10 score that used to appear in Google's browser toolbar. It was a logarithmic simplification of the real PageRank value. Removed in 2016. Don't trust any tool claiming to show PageRank scores today.
- **Internal PageRank**. The concept applied within a single website. Your homepage accumulates the most internal PageRank (most internal links point to it), and you can strategically redistribute it through [internal linking](/glossary/internal-link) to boost priority pages.

The third-party metrics you see today ,  [Domain Authority](/glossary/domain-authority) from Moz, Domain Rating from Ahrefs. Are reverse-engineered approximations inspired by PageRank. They're useful. They're not the real thing.

## PageRank Examples

**A local HVAC company's blog.** They publish 30 articles per month using theStacc. Over 6 months, they've built 180 interlinked pages on heating, cooling, and air quality topics. Even without many external backlinks, the internal linking structure distributes PageRank efficiently across the site. Google sees a well-connected topical cluster, not 180 isolated pages. Several articles start ranking on page 1 for local keywords purely from internal PageRank flow.

**A guest post on a high-authority site.** An accounting firm writes an article for Forbes' contributor network. That single [backlink](/glossary/backlinks) from Forbes (with its massive PageRank) passes more authority than dozens of links from small directories. The firm's service page. Which the Forbes article links to. Jumps from position 14 to position 6 within 8 weeks.

**A page buried 5 clicks deep.** A real estate agency has a detailed neighborhood guide. Great content, zero internal links pointing to it. No external links either. PageRank: effectively zero. The page doesn't rank for anything. They add internal links from 10 relevant blog posts and the homepage. Rankings appear within a month. Same content, totally different result. Just because PageRank could finally flow to it.

## PageRank vs. Domain Authority

People use these terms interchangeably. They shouldn't.

| | PageRank | [Domain Authority](/glossary/domain-authority) (DA) |
|---|---|---|
| **Created by** | Google (Larry Page, Sergey Brin) | Moz |
| **Scope** | Per-page metric | Per-domain metric |
| **Scale** | Originally 0-10 (logarithmic) | 0-100 (logarithmic) |
| **Publicly visible** | No (since 2016) | Yes (via Moz tools) |
| **Used by Google** | Yes (internally, evolved form) | No. It's a third-party estimate |
| **What it measures** | Link-based page importance | Predicted ranking strength of a domain |

DA is a useful proxy for estimating a site's authority. But Google doesn't use DA. Google uses its own link evaluation systems. Which descend from PageRank.

## PageRank Best Practices

- **Earn links from high-authority pages, not just high-authority domains**. A link from a page with its own strong backlink profile passes more PageRank than a link from a low-traffic page on a big domain. Check the linking *page*, not just the site.
- **Build a flat site architecture**. Keep important pages within 3 clicks of the homepage. The more clicks deep a page is, the less PageRank flows to it. [Site architecture](/glossary/site-architecture) directly controls internal PageRank distribution.
- **Link strategically from high-PageRank pages to priority pages**. Your homepage has the most internal PageRank. Link from it to your most important service or product pages. Don't waste homepage links on low-priority pages.
- **Avoid [nofollow](/glossary/nofollow-link) on internal links**. Nofollow tells Google not to pass PageRank through a link. Using it on internal links wastes your own authority. Reserve nofollow for external links where appropriate.
- **Publish content consistently to create link-worthy assets**. More pages means more opportunities to earn external links and more nodes in your internal linking graph. Services like theStacc publish 30 articles/month, giving your site 30 new PageRank recipients. And 30 new pages to link from to your key commercial pages.

## Frequently Asked Questions

### Is PageRank still used by Google?

Yes. Google confirmed in patent filings and engineer statements that evolved versions of PageRank remain part of their ranking systems. The public toolbar score is gone, but the underlying algorithm lives on.

### Can I check my PageRank?

Not the real one. Google stopped publishing PageRank scores in 2016. Tools showing "PageRank" today are using third-party estimates. Moz's Page Authority and Ahrefs' URL Rating are the closest available proxies.

### Do nofollow links pass PageRank?

Officially, no. Google treats nofollow as a "hint" since 2019, meaning they *might* count the link in some cases. But for practical purposes, [dofollow links](/glossary/dofollow-link) are what pass PageRank reliably.

### Does internal linking affect PageRank?

Absolutely. Internal links pass PageRank just like external links do. A thoughtful [internal linking](/glossary/internal-link) strategy can significantly boost the PageRank flowing to your most important pages. Without earning a single backlink.

---

Want to build a site structure that compounds PageRank automatically? theStacc publishes 30 interlinked SEO articles to your site every month. Building internal authority while you focus on your business. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Stanford: The PageRank Citation Ranking (Original Paper)](http://ilpubs.stanford.edu:8090/422/1/1999-66.pdf)
- [Google Search Central: How Search Works. Ranking](https://developers.google.com/search/docs/fundamentals/how-search-works)
- [Ahrefs: Do Backlinks Still Matter? (Study)](https://ahrefs.com/blog/search-traffic-study/)
- [Moz: What Is Domain Authority?](https://moz.com/learn/seo/domain-authority)
- [Search Engine Journal: Is PageRank Still Used?](https://www.searchenginejournal.com/google-pagerank/367875/)
