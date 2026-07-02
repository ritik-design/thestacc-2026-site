---
term: "Core Web Vitals"
slug: "core-web-vitals"
definition: "Core Web Vitals are Google's metrics for measuring page experience: LCP, INP, and CLS. Learn what each metric means, how to measure them, and improvement."
category: "SEO"
difficulty: "Intermediate"
keyword: "what are core web vitals"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "page-speed"
  - "technical-seo"
  - "google-search-console"
  - "largest-contentful-paint-lcp"
  - "cumulative-layout-shift-cls"
---

## What Are Core Web Vitals?

Core Web Vitals are a set of three specific metrics Google uses to measure how fast, responsive, and visually stable a web page feels to real users.

Google introduced them in 2020 and made them an official ranking signal in 2021. They're part of the broader [page speed](/glossary/page-speed) conversation, but more specific. Instead of a single "speed score," Core Web Vitals break the user experience into three measurable components. Loading, interactivity, and visual stability.

According to Google's own data, pages meeting all three Core Web Vitals thresholds see 24% fewer page abandonments. That's not a minor UX improvement. It's a direct line to more conversions and better [organic traffic](/glossary/organic-traffic).

## Why Do Core Web Vitals Matter?

Ignoring Core Web Vitals won't tank your rankings overnight. But all else being equal, Google will favor pages that pass these benchmarks over pages that don't.

- **Ranking factor since 2021**. Google confirmed Core Web Vitals as part of its page experience signals, meaning they directly influence where you appear in [search results](/glossary/serp)
- **24% fewer abandonments**. Pages passing all three thresholds keep users on the page significantly longer (Google, 2021)
- **Mobile-first impact**. With [mobile-first indexing](/glossary/mobile-first-indexing) as the default, slow mobile pages get hit hardest
- **Ad revenue correlation**. Publishers who improved CWV scores saw up to 15% more ad revenue from longer session durations

If you're running a local business or small company, this matters because your competitors probably aren't optimizing for CWV either. Getting a passing score when they don't is a real advantage.

## How Core Web Vitals Work

Google collects Core Web Vitals data from real Chrome users through the Chrome User Experience Report (CrUX). That means your scores come from actual visitors. Not a lab simulation.

### Largest Contentful Paint (LCP)

[LCP](/glossary/largest-contentful-paint-lcp) measures how long it takes for the biggest visible element on your page to load. Think: the hero image, a large text block, or a video thumbnail. Google wants this under 2.5 seconds. Anything over 4 seconds is rated "poor."

The fix is usually straightforward: compress images, use a [CDN](/glossary/content-delivery-network-cdn), defer offscreen resources, and improve server response time.

### Interaction to Next Paint (INP)

INP replaced First Input Delay (FID) in March 2024. It measures how quickly your page responds to user interactions. Clicks, taps, and key presses. Throughout the entire visit, not just the first interaction.

Good INP is under 200 milliseconds. If your page freezes for half a second when someone clicks a button, that's a failing score. Heavy JavaScript is the usual culprit.

### Cumulative Layout Shift (CLS)

[CLS](/glossary/cumulative-layout-shift-cls) measures visual stability. Ever tried to tap a button on a page, only to have it jump because an ad or image loaded late? That's layout shift.

Google wants a CLS score under 0.1. The most common causes: images without defined dimensions, ads injected above content, and web fonts that swap sizes during load.

## Types of Core Web Vitals Assessments

Core Web Vitals data comes in two flavors, and they often tell different stories:

- **Field data (RUM)**. Real User Metrics collected from actual visitors via CrUX. This is what Google uses for ranking decisions. You can see it in [Google Search Console](/glossary/google-search-console) and PageSpeed Insights.
- **Lab data**. Simulated performance tests from tools like Lighthouse, WebPageTest, and Chrome DevTools. Useful for debugging but not used directly for rankings.
- **Origin-level vs. URL-level**. Google evaluates CWV at both the full domain level and individual page level. If your site overall passes but a key landing page fails, that page can still be affected.
- **Mobile vs. Desktop**. Scores are measured separately for mobile and desktop. Most sites perform worse on mobile, which is the version Google prioritizes.

For [technical SEO](/glossary/technical-seo) audits, always start with field data. Lab data helps you find the problem, but field data tells you whether the problem is actually hurting real visitors.

## Core Web Vitals Examples

**Example 1: A plumbing company's slow homepage**
A local plumber has a homepage with a 4.8-second LCP because of an uncompressed hero image (3.2 MB). After converting it to WebP and resizing to the correct dimensions, LCP drops to 1.9 seconds. Their bounce rate falls 18% over the next month.

**Example 2: An ecommerce store with layout shift**
A Shopify store selling pet supplies has a CLS score of 0.34 because product images load without width/height attributes. Adding explicit dimensions to every image tag brings CLS to 0.04. No more accidental "Add to Cart" clicks from frustrated shoppers.

**Example 3: A blog with heavy JavaScript**
A marketing agency's blog uses 14 third-party scripts. Analytics, chat widgets, social embeds, ad trackers. INP sits at 480ms. After auditing and removing 6 unused scripts, INP drops to 160ms. Pages built and published through theStacc already ship with clean, optimized code. No bloated scripts.

## Core Web Vitals vs. Page Speed

People use these interchangeably. They shouldn't.

| | Core Web Vitals | Page Speed |
|---|---|---|
| **What it measures** | 3 specific user experience metrics (LCP, INP, CLS) | Overall load time and performance score |
| **Data source** | Real user data (CrUX) | Lab simulations (Lighthouse) |
| **Google ranking signal** | Yes, directly | Indirectly (through CWV) |
| **Scope** | Focused on perceived experience | Broader performance umbrella |
| **Example metric** | LCP: 2.1s | PageSpeed Score: 74/100 |

[Page speed](/glossary/page-speed) is the broader concept. Core Web Vitals are the specific metrics Google actually uses.

## Core Web Vitals Best Practices

- **Compress and properly size all images**. Use WebP or AVIF formats, and always set explicit width and height attributes to prevent layout shift
- **Minimize third-party scripts**. Every external script (chat widgets, analytics, ad trackers) adds to INP. Audit ruthlessly and remove what you don't need.
- **Use a CDN for static assets**. Serving images and CSS from edge servers close to your visitors dramatically reduces LCP
- **Defer non-critical JavaScript**. Load above-the-fold content first, then let secondary scripts load after the page is interactive
- **Monitor field data monthly in Google Search Console**. Lab scores fluctuate, but field data shows whether real visitors are getting a good experience. Services like theStacc automatically publish content that follows clean HTML best practices, reducing CWV issues from the start.

## Frequently Asked Questions

### Are Core Web Vitals a ranking factor?

Google confirmed Core Web Vitals as a ranking signal in June 2021. They're part of the page experience system. The impact is real but secondary to content relevance and [backlinks](/glossary/backlinks). Think tiebreaker, not dealbreaker.

### What replaced First Input Delay?

Interaction to Next Paint (INP) officially replaced FID as a Core Web Vital in March 2024. INP measures responsiveness across all interactions during a visit, not just the first click.

### How do I check my Core Web Vitals?

Use Google Search Console's Core Web Vitals report for field data. PageSpeed Insights gives you both field and lab data for any URL. Chrome DevTools and Lighthouse work for local testing during development.

### What's a good LCP score?

Google rates LCP under 2.5 seconds as "good," between 2.5 and 4 seconds as "needs improvement," and over 4 seconds as "poor." Most sites struggle with LCP because of unoptimized images and slow server response.

---

Want your content to load fast and rank well without managing technical details? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google: Web Vitals](https://web.dev/vitals/)
- [Google Search Central: Page Experience](https://developers.google.com/search/docs/appearance/page-experience)
- [Chrome UX Report (CrUX)](https://developer.chrome.com/docs/crux/)
- [Web.dev: Interaction to Next Paint (INP)](https://web.dev/inp/)
- [Ahrefs: Core Web Vitals and SEO](https://ahrefs.com/blog/core-web-vitals/)
