---
term: "Page Speed"
slug: "page-speed"
definition: "Page speed is how fast the content on a web page loads and becomes interactive for users. It's a confirmed Google ranking factor that directly affects."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is page speed"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "core-web-vitals"
  - "largest-contentful-paint-lcp"
  - "technical-seo"
  - "bounce-rate"
  - "mobile-first-indexing"
---

## What is Page Speed?

Page speed is the measurement of how quickly a web page's content loads and becomes usable. From the moment a user clicks a link to the moment they can read, scroll, and interact with the page.

Don't confuse it with "site speed," which is an average across your whole site. Page speed is per-page. A blazing fast homepage means nothing if your blog posts take 8 seconds to load. And load time isn't binary. It's a spectrum of metrics. How fast does the first piece of content appear? How fast does the largest element render? When can the user actually interact? Each stage matters.

Google made page speed an official ranking factor in 2018 for mobile searches. Then in 2021, [Core Web Vitals](/glossary/core-web-vitals) made it more specific. Measuring [Largest Contentful Paint](/glossary/largest-contentful-paint-lcp) (loading), Interaction to Next Paint (interactivity), and [Cumulative Layout Shift](/glossary/cumulative-layout-shift-cls) (visual stability). A Google study found that as page load time increases from 1 second to 3 seconds, the probability of bounce increases by 32%. At 5 seconds, it jumps to 90%.

## Why Does Page Speed Matter?

Slow pages kill rankings, kill conversions, and kill user trust. The impact is measurable across every metric that matters.

- **Google confirmed it's a ranking factor**. Slow pages get penalized in rankings. Google prioritizes fast, mobile-friendly pages, especially after the [mobile-first indexing](/glossary/mobile-first-indexing) shift.
- **Every second costs you money**. Amazon famously calculated that a 1-second delay in page load could cost $1.6 billion per year in lost sales. For smaller businesses, the proportional impact is the same.
- **Bounce rates spike with load time**. Google's data: 1 to 3 second load time increases bounce probability 32%. 1 to 5 seconds: 90%. 1 to 10 seconds: 123%. Users won't wait.
- **Mobile users are less patient**. Over 60% of searches happen on mobile. Mobile connections are often slower. Pages that load fine on desktop broadband can be painfully slow on a 4G connection.
- **[Core Web Vitals](/glossary/core-web-vitals) affect search visibility**. Google uses CWV data directly in ranking. Pages failing CWV thresholds are at a disadvantage against competitors who pass.

A slow website is like a store with a locked door. People show up, can't get in, and leave.

## How Page Speed Works

Page speed involves multiple technical factors. From server response time to how browsers render your page.

### Server Response Time (TTFB)

Time to First Byte. The time between a browser requesting your page and receiving the first byte of data from your server. A TTFB over 600ms signals a slow server. Causes include cheap hosting, database bottlenecks, no caching, and servers geographically far from your users. A [Content Delivery Network (CDN)](/glossary/content-delivery-network-cdn) can fix the geography problem.

### Resource Loading

After the browser gets the HTML, it starts loading everything the page needs: CSS files, JavaScript files, images, fonts, videos. Each file requires a network request. More requests mean more time. Large files mean more data to download. Unoptimized images are the #1 culprit. A single 5MB hero image can add 3-4 seconds to load time on mobile.

### Rendering and Interactivity

The browser processes HTML, applies CSS, and executes JavaScript to render the visible page. Heavy JavaScript. Especially render-blocking scripts. Delays when the page becomes visually complete and interactive. [Largest Contentful Paint](/glossary/largest-contentful-paint-lcp) measures when the main content finishes loading. [Interaction to Next Paint (INP)](/glossary/interaction-to-next-paint-inp) measures how quickly the page responds when users click or tap.

### Layout Stability

[Cumulative Layout Shift](/glossary/cumulative-layout-shift-cls) tracks how much the page content moves around while loading. If text jumps, buttons shift, or images push content down, that's layout shift. It's frustrating for users and Google penalizes it.

## Types of Page Speed Metrics

Page speed isn't one number. It's a collection of metrics, each measuring a different aspect of the loading experience.

- **[Largest Contentful Paint (LCP)](/glossary/largest-contentful-paint-lcp)**. How long until the main content element is visible. Good: under 2.5 seconds. The most important Core Web Vital for perceived speed.
- **[First Contentful Paint (FCP)](/glossary/first-contentful-paint-fcp)**. When the first piece of content appears on screen. Good: under 1.8 seconds. Gives users confidence the page is loading.
- **[Interaction to Next Paint (INP)](/glossary/interaction-to-next-paint-inp)**. How fast the page responds to user interactions. Good: under 200ms. Replaced First Input Delay in 2024.
- **Time to First Byte (TTFB)**. Server response speed. Good: under 600ms. A server-side issue, not a front-end one.
- **[Cumulative Layout Shift (CLS)](/glossary/cumulative-layout-shift-cls)**. Visual stability score. Good: under 0.1. Lower means content doesn't jump around while loading.

Google PageSpeed Insights, Lighthouse, and Chrome DevTools all measure these metrics. Google Search Console's Core Web Vitals report shows your site-wide performance.

## Page Speed Examples

**A local restaurant's website.** Their homepage has 12 uncompressed photos (average 4MB each), 3 embedded Google Maps iframes, and a Facebook widget. Total page weight: 52MB. Load time on mobile: 14 seconds. Google PageSpeed Insights score: 18/100. Potential customers searching "pizza near me" click, wait 5 seconds, leave, and click the next result. After compressing images, lazy-loading below-fold content, and removing unused widgets: 2.8 second load, score jumps to 82. Bounce rate drops 40%.

**An ecommerce site losing sales.** Their product pages load in 6.2 seconds. Analytics shows 73% of mobile visitors leave before the page finishes loading. A speed audit reveals the culprit: a render-blocking JavaScript bundle (1.2MB) that could be deferred. After code splitting, image optimization, and implementing a CDN, load time drops to 2.1 seconds. Mobile conversion rate doubles in the first month.

**A content-heavy blog.** They publish 30 articles per month through theStacc. Each article loads in under 2 seconds because the site uses a static site generator with optimized images and minimal JavaScript. Fast pages mean Google crawls and indexes their content quickly, and visitors stay to read. Their [organic traffic](/glossary/organic-traffic) compounds faster because speed amplifies every other [SEO](/glossary/seo) effort.

## Page Speed vs. Core Web Vitals

People use these terms interchangeably, but they're not the same thing.

| | Page Speed | [Core Web Vitals](/glossary/core-web-vitals) |
|---|---|---|
| **What it is** | General concept of how fast a page loads | Specific set of 3 metrics defined by Google |
| **Metrics** | Many (TTFB, FCP, LCP, Speed Index, etc.) | LCP, INP, CLS only |
| **Scope** | Full loading performance picture | Focused on user-perceived experience |
| **Ranking impact** | Indirect. Many metrics, varying influence | Direct. Google uses CWV as ranking signals |
| **How to measure** | PageSpeed Insights, Lighthouse, WebPageTest | Google Search Console, PageSpeed Insights |

Core Web Vitals are a subset of page speed. Passing CWV is the minimum bar Google sets. Optimizing page speed more broadly improves everything. User experience, [bounce rate](/glossary/bounce-rate), conversions, and crawl efficiency.

## Page Speed Best Practices

- **Compress and resize images**. Images are the #1 page weight offender. Use modern formats (WebP, AVIF), resize to actual display dimensions, and compress aggressively. A hero image doesn't need to be 4000px wide.
- **Implement lazy loading**. Only load images and embeds when they're about to scroll into view. This slashes initial load time for content-heavy pages. Most modern browsers support native lazy loading with the `loading="lazy"` attribute.
- **Minimize render-blocking resources**. Defer non-critical JavaScript. Inline critical CSS. Move third-party scripts (analytics, chat widgets, social embeds) to load after the main content.
- **Use a CDN**. A [Content Delivery Network](/glossary/content-delivery-network-cdn) serves your pages from servers close to the user's location. Reduces TTFB dramatically for visitors far from your origin server.
- **Monitor with real data, not just lab data**. PageSpeed Insights shows both lab scores (simulated) and field data (real user measurements). Field data from [Google Search Console](/glossary/google-search-console) is what Google actually uses for ranking. theStacc sites are built on fast, optimized infrastructure so every article loads quickly. Because speed affects how well all 30 monthly articles perform in search.

## Frequently Asked Questions

### What's a good page speed score?

A Google PageSpeed Insights score of 90-100 is excellent, 50-89 is average, and below 50 needs work. But the score is a summary. Focus on the individual metrics, especially LCP (under 2.5s) and INP (under 200ms), since those directly affect rankings.

### Does page speed affect SEO directly?

Yes. Google confirmed page speed as a ranking factor in 2018, and [Core Web Vitals](/glossary/core-web-vitals) became explicit ranking signals in 2021. Slow pages rank lower, especially on mobile. The impact is most noticeable when two pages are otherwise similar in content quality and authority.

### How do I test my page speed?

Google PageSpeed Insights (free) is the starting point. It shows both lab and field data. For deeper analysis, use Chrome DevTools Lighthouse, WebPageTest.org, or GTmetrix. Google Search Console's Core Web Vitals report shows site-wide performance trends.

### What slows down a page the most?

Large uncompressed images, render-blocking JavaScript, slow server response times, and too many third-party scripts (analytics trackers, chat widgets, ad scripts). Images are almost always the biggest offender. And the easiest to fix.

---

Want fast-loading, SEO-optimized content published to your site automatically? theStacc publishes 30 articles per month with built-in [on-page SEO](/glossary/on-page-seo) optimization. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Page Experience Ranking Signals](https://developers.google.com/search/docs/appearance/page-experience)
- [Google: Find Out How You Stack Up to New Industry Benchmarks for Mobile Page Speed](https://www.thinkwithgoogle.com/marketing-strategies/app-and-mobile/mobile-page-speed-new-industry-benchmarks/)
- [Web.dev: Core Web Vitals](https://web.dev/vitals/)
- [Google PageSpeed Insights Tool](https://pagespeed.web.dev/)
- [Ahrefs: Page Speed and SEO. Does Site Speed Affect Rankings?](https://ahrefs.com/blog/page-speed/)
