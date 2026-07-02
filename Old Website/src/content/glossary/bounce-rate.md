---
term: "Bounce Rate"
slug: "bounce-rate"
definition: "Bounce rate is the percentage of visitors who leave after viewing only one page. Learn the formula, benchmarks by industry, and proven strategies to."
category: "SEO"
difficulty: "Beginner"
keyword: "what is bounce rate"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "dwell-time"
  - "click-through-rate"
  - "core-web-vitals"
  - "user-experience"
  - "google-analytics"
---

## What is Bounce Rate?

Bounce rate is the percentage of website visitors who land on a page and leave without taking any further action. No second page view, no click, no scroll event (in GA4's case, no engagement).

Put differently: someone arrives, looks at one page, and disappears. In [Google Analytics](/glossary/google-analytics), a "bounce" traditionally meant a single-page session with no interaction. GA4 changed the definition. Now it's the inverse of "engagement rate," where an engaged session lasts 10+ seconds, has 2+ page views, or triggers a conversion event. Same concept, slightly different math.

Contentsquare's 2024 Digital Experience Benchmark found that the average bounce rate across all industries is 47%. But that number varies wildly. A blog post might have a 65% bounce rate and be performing well. A product page at 65% is bleeding money.

## Why Does Bounce Rate Matter?

A high bounce rate isn't always bad. But when it's high on pages designed to convert. Landing pages, product pages, service pages. It signals a real problem.

- **Wasted traffic**. Every bounce is a visitor who came, saw nothing compelling enough to stay, and left. If you're paying for that traffic through [PPC](/glossary/pay-per-click), each bounce costs you money with zero return.
- **Conversion killer**. Visitors who bounce can't convert. If your service page has an 80% bounce rate, only 20% of visitors are even seeing your [call to action](/glossary/call-to-action). That's a leaky bucket.
- **Possible ranking signal**. Google hasn't confirmed bounce rate as a direct ranking factor. But user engagement signals (pogo-sticking, [dwell time](/glossary/dwell-time)) correlate strongly with rankings. Pages that satisfy users tend to rank better.
- **Content quality indicator**. A blog post with a 90% bounce rate might mean the content doesn't match the [search intent](/glossary/search-intent). The visitor searched for one thing, found something else, and left.

Bounce rate alone doesn't tell the full story. But combined with time on page, scroll depth, and [conversion rate](/glossary/conversion-rate), it paints a clear picture of whether your pages are working.

## How Bounce Rate Works

The metric is straightforward, but interpreting it requires context.

### The Formula

Bounce Rate = (Single-page sessions / Total sessions) x 100

If 1,000 people visit your page and 600 leave without any interaction, your bounce rate is 60%.

### GA4's Engagement Rate (The Inverse)

Google Analytics 4 flipped the script. Instead of tracking bounces, it tracks "engaged sessions." An engaged session meets at least one criterion: lasted 10+ seconds, had 2+ page views, or included a conversion event. Bounce rate in GA4 = 100% minus engagement rate. If your engagement rate is 55%, your bounce rate is 45%.

### What Counts as a "Bounce"

In Universal Analytics (legacy), any single-page session with zero interaction events counted as a bounce. Even if the user read the entire article for 10 minutes. GA4 fixed this by adding the 10-second threshold. A user who reads for 30 seconds but never clicks anything is "engaged" in GA4 but would've been a "bounce" in UA. Important distinction if you're comparing historical data.

### Benchmarks by Page Type

Not all pages should have the same bounce rate target:

| Page Type | Average Bounce Rate | Good Target |
|---|---|---|
| Blog posts | 65-80% | Under 65% |
| Landing pages | 60-70% | Under 55% |
| Service/product pages | 40-55% | Under 40% |
| Ecommerce product pages | 35-50% | Under 35% |
| Homepage | 40-60% | Under 45% |

A 70% bounce rate on a blog post can be perfectly fine. The reader got their answer and left. A 70% bounce rate on a checkout page is a crisis.

## Types of Bounce Rate

Bounce rate gets segmented differently depending on what you're analyzing:

- **Page-level bounce rate**. The bounce rate for a specific page. Most useful for diagnosing individual page performance.
- **Site-wide bounce rate**. The average across your entire site. Useful as a general health metric but masks page-level problems.
- **Source-level bounce rate**. Bounce rate broken down by traffic source (organic, paid, social, direct, email). If your paid traffic bounces at 80% but organic bounces at 45%, you have a targeting problem. Not a content problem.
- **Device-level bounce rate**. Mobile vs. desktop. Mobile bounce rates are consistently 10-20% higher than desktop across industries, often due to slower load times and poor [mobile optimization](/glossary/mobile-first-indexing).

Always analyze bounce rate in segments. Site-wide averages hide the real issues.

## Bounce Rate Examples

**Example 1: A law firm's service page losing leads**
A personal injury law firm gets 2,000 monthly visitors to their main service page. Bounce rate: 72%. Investigation reveals the page takes 6.2 seconds to load on mobile (a [Core Web Vitals](/glossary/core-web-vitals) failure). After optimizing images, enabling lazy loading, and reducing page weight, load time drops to 2.1 seconds. Bounce rate drops to 48%. Monthly form submissions increase by 35%.

**Example 2: A blog with misleading titles**
A marketing agency publishes a post titled "2026 SEO Trends That Will Double Your Traffic." The content is a generic listicle with no original data. Bounce rate: 88%. Visitors expected actionable insights and got fluff. After rewriting with original research, specific tactics, and data, bounce rate drops to 58%. The page moves from position 14 to position 5 for its target [keyword](/glossary/keyword).

**Example 3: An ecommerce store fixing its product pages**
An online retailer notices their product pages average a 62% bounce rate. Exit surveys reveal customers can't find sizing information. The team adds a sizing chart, customer photos, and a Q&A section to each product page. Bounce rate drops to 41%. Revenue per page increases 22%. Sometimes the fix isn't about [SEO](/glossary/seo). It's about answering the question the visitor actually has.

## Bounce Rate vs. Exit Rate

These metrics sound similar. They measure different things.

| | Bounce Rate | Exit Rate |
|---|---|---|
| **Measures** | Single-page sessions (no interaction) | Last page in a multi-page session |
| **Scope** | First-page visits only | All page views |
| **What it means** | Visitor arrived and left immediately | Visitor browsed other pages, then left from this one |
| **High rate signals** | Poor first impression, mismatched intent | Natural end of journey or drop-off point |
| **Example** | User lands on blog post > leaves | User visits homepage > about > pricing > leaves from pricing |

A page can have a low bounce rate but a high exit rate. That's normal for pages at the end of a user journey (thank you pages, checkout confirmation). Context matters.

## Bounce Rate Best Practices

- **Speed up your pages** ,  [Page speed](/glossary/page-speed) is the #1 bounce rate factor. Google data shows that bounce probability increases 32% as page load time goes from 1 to 3 seconds. Optimize images, minimize code, and use caching.
- **Match content to search intent**. If someone searches "how to fix a leaky faucet," they expect a how-to guide. Not a sales page for plumbing services. Mismatched [search intent](/glossary/search-intent) causes instant bounces.
- **Use internal links to create pathways**. Give visitors somewhere to go. Related articles, suggested products, next-step CTAs. Every [internal link](/glossary/internal-link) is a chance to prevent a bounce. theStacc includes strategic internal links in every article published, creating natural pathways that keep visitors moving through your site.
- **Improve above-the-fold content**. Users decide to stay or leave within 3 seconds. Your headline, opening paragraph, and visual layout need to instantly communicate relevance and value.
- **Segment and prioritize**. Don't try to fix every page. Sort pages by traffic x bounce rate. The high-traffic, high-bounce pages are where improvements will have the biggest impact on your business.

## Frequently Asked Questions

### What's a good bounce rate?

There's no universal "good" number. For most websites, 40-55% is healthy. Blog content typically runs 60-70%. Landing pages should target under 55%. The right benchmark depends on page type, industry, and traffic source.

### Does bounce rate affect SEO rankings?

Google says bounce rate isn't a direct ranking factor. But related engagement signals ,  [dwell time](/glossary/dwell-time), pogo-sticking (returning to search results immediately), and engagement metrics. Correlate with rankings. Pages that keep users engaged tend to rank better over time.

### Why is my mobile bounce rate so high?

Mobile bounce rates are typically 10-20% higher than desktop. The usual culprits: slow load speed, intrusive pop-ups, unreadable text, buttons too small to tap, and layouts that aren't mobile-optimized. Check [Core Web Vitals](/glossary/core-web-vitals) in Google Search Console for specific mobile issues.

### Is a high bounce rate always bad?

No. A blog post or FAQ page can have a high bounce rate and still be successful. The user found their answer and left satisfied. High bounce rates are problematic on conversion-focused pages (product pages, landing pages, pricing pages) where the goal is deeper engagement.

---

Want to publish content that keeps visitors engaged and moving through your site? theStacc publishes 30 SEO-optimized articles with strategic internal linking every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Analytics Help: About Bounce Rate](https://support.google.com/analytics/answer/1009409)
- [Contentsquare: Digital Experience Benchmark Report](https://contentsquare.com/insights/digital-experience-benchmark/)
- [Google: Page Speed and Bounce Rate](https://www.thinkwithgoogle.com/marketing-strategies/app-and-mobile/mobile-page-speed-data/)
- [Backlinko: Bounce Rate Study](https://backlinko.com/hub/seo/bounce-rate)
- [Semrush: Bounce Rate Guide](https://www.semrush.com/blog/bounce-rate/)
