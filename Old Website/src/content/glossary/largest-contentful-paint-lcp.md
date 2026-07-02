---
term: "Largest Contentful Paint (LCP)"
slug: "largest-contentful-paint-lcp"
definition: "Largest Contentful Paint (LCP) is a Core Web Vitals metric that measures how long it takes for the largest visible element on a page. Typically a hero."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is largest contentful paint lcp"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "core-web-vitals"
  - "interaction-to-next-paint-inp"
  - "cumulative-layout-shift-cls"
  - "page-speed"
  - "technical-seo"
---

## What is Largest Contentful Paint (LCP)?

Largest Contentful Paint (LCP) measures the time from when a page starts loading to when the largest content element visible in the viewport finishes rendering.

In plain terms: it's how long your visitor stares at a loading screen before seeing the main content. That hero image. The headline. The product photo. Whatever takes up the most visual space above the fold. LCP tracks when it becomes fully visible.

Google picked LCP as a [Core Web Vitals](/glossary/core-web-vitals) metric because it correlates strongly with perceived load speed. Users don't care about technical load events. They care about when the page *looks* ready. According to Google's data, 53% of mobile users abandon pages that take longer than 3 seconds to load. LCP quantifies exactly that moment of "ready."

## Why Does LCP Matter?

Slow LCP means visitors leave before they see your content. Fast LCP means they stay and engage.

- **Direct ranking signal**. LCP is one of three Core Web Vitals in Google's page experience system. Pages with poor LCP (over 4 seconds) face a measurable ranking penalty.
- **53% of mobile visitors bounce** after 3 seconds of load time (Google). If your LCP is 4+ seconds, you're losing over half your mobile audience before they read a single word.
- **Conversion rate impact**. Vodafone improved LCP by 31% and saw an 8% increase in sales. Shopify found that every 100ms of LCP improvement increased conversion by 1.3%.
- **[Organic traffic](/glossary/organic-traffic) compounds the effect**. A slow page ranks lower, gets fewer clicks, earns fewer [backlinks](/glossary/backlinks), and drops further. A fast page does the opposite. LCP creates a flywheel in both directions.

Every page on your site has an LCP score. Not just the homepage. Blog posts, product pages, landing pages. They all get measured independently.

## How LCP Works

LCP measurement involves the browser tracking candidate elements as the page renders.

### Identifying the LCP Element

The browser watches for the largest content element in the viewport during page load. Eligible elements include `<img>` tags, `<video>` poster images, elements with CSS `background-image`, and block-level text elements (`<h1>`, `<p>`, `<div>` with text). The "largest" is measured by visible area. The element that covers the most pixels in the viewport.

### Continuous Measurement

LCP isn't a single measurement. The browser continuously updates the LCP candidate as new elements render. If your headline text renders first (becoming the temporary LCP element), then a hero image loads 2 seconds later and takes up more space. The hero image becomes the new LCP element. The final LCP score is the render time of the last largest element before the user first interacts with the page.

### What Triggers Poor LCP

Four categories of issues account for nearly all LCP problems:

| Cause | What Happens | Common Culprit |
|---|---|---|
| Slow server response | The HTML itself takes too long to arrive | Shared hosting, no CDN, database bottlenecks |
| Render-blocking resources | CSS and JavaScript block the browser from painting | Large CSS files, undeferred JS in the `<head>` |
| Slow resource load | The LCP element (image/video) downloads slowly | Unoptimized images, no lazy loading, distant server |
| Client-side rendering | Content renders via JavaScript after the page loads | Single-page apps (React, Vue) without SSR |

Google Search Console's Core Web Vitals report flags pages with poor LCP and groups them by issue type. A good starting point for fixes.

## Types of LCP Elements

Different page types have different LCP elements. Knowing yours is step one to optimizing it.

- **Hero images**. The most common LCP element on marketing pages, blog posts, and e-commerce sites. Large above-the-fold images dominate the viewport.
- **Background images via CSS**. Full-bleed background images on hero sections. These are trickier because the browser discovers them later than inline `<img>` tags.
- **Video poster images**. For pages with above-the-fold video, the poster frame often serves as the LCP element.
- **Large text blocks**. On text-heavy pages without large images (documentation, articles, search results), the main heading or first paragraph can be the LCP element. These typically have excellent LCP scores since text renders fast.
- **Carousel first slides**. On pages with an image carousel above the fold, the first visible slide is usually the LCP element.

Check which element is *your* LCP using Chrome DevTools → Performance panel → hover over the LCP marker. You might be surprised.

## LCP Examples

**A law firm's homepage.** Their hero section has a 4MB background image of a skyline at sunset. No compression, no next-gen format, no CDN. LCP: 6.2 seconds on mobile. They switch to a WebP image at 200KB, add a CDN, and preload it with `<link rel="preload">`. New LCP: 1.8 seconds. Rankings improve within 6 weeks.

**A dentist's blog powered by theStacc.** The 30 articles published monthly use optimized featured images under 100KB, served through a CDN with responsive `srcset` attributes. Average LCP across all blog pages: 1.4 seconds. Google Search Console shows zero LCP issues. The [technical SEO](/glossary/technical-seo) foundation is solid from day one. No cleanup needed.

**An e-commerce product page.** The main product image loads from a third-party image host without a CDN. The page also has 2MB of render-blocking JavaScript from various widgets. LCP: 5.1 seconds. Mobile [bounce rate](/glossary/bounce-rate) is 72%. Fixing the image delivery alone drops LCP to 3.2 seconds. Deferring non-critical JavaScript brings it down to 2.1 seconds.

## LCP vs. First Contentful Paint (FCP)

These two metrics sound similar but measure different things.

| | LCP | FCP |
|---|---|---|
| **What it measures** | When the *largest* visible element renders | When *any* content first appears on screen |
| **What it reflects** | Perceived page readiness | Initial visual response |
| **Good threshold** | Under 2.5 seconds | Under 1.8 seconds |
| **Core Web Vital?** | Yes | No (it's a supplemental metric) |
| **Typical gap** | FCP happens first, LCP follows | LCP is always equal to or after FCP |

FCP tells you when the page starts showing something. LCP tells you when it finishes showing the main content. Both matter for user experience, but LCP is the one Google uses for ranking.

## LCP Best Practices

- **Preload your LCP image**. Add `<link rel="preload" as="image" href="hero.webp">` in the `<head>`. This tells the browser to start downloading the image immediately, before it discovers it in the HTML. Single biggest LCP improvement for most sites.
- **Use next-gen image formats**. WebP and AVIF compress 25-50% smaller than JPEG at equivalent quality. Smaller files download faster. Period.
- **Eliminate render-blocking resources**. Inline critical CSS, defer non-critical CSS with `media="print"` swapping, and move JavaScript to the end of the body or add `defer`/`async` attributes.
- **Use a CDN for static assets**. Serving images from a server 50ms away instead of 500ms away directly reduces LCP. Cloudflare, Fastly, and CloudFront all work. Sites running large content operations. Like those using theStacc to publish 30 articles/month. Should ensure their CDN covers all blog images.
- **Set explicit width and height on images**. This prevents layout recalculation during load, which delays rendering. Also helps avoid [Cumulative Layout Shift](/glossary/cumulative-layout-shift-cls) issues.

## Frequently Asked Questions

### What's a good LCP score?

Under 2.5 seconds is "good." Between 2.5 and 4.0 seconds "needs improvement." Over 4.0 seconds is "poor." Google uses real-user data (field data) from Chrome browsers to assess your score. Not lab tests.

### Does LCP affect SEO rankings?

Yes. LCP is one of three [Core Web Vitals](/glossary/core-web-vitals) and feeds directly into Google's page experience ranking signal. Poor LCP won't tank a page with great content, but it creates a measurable disadvantage against equally relevant competitors.

### How do I find my LCP score?

[Google Search Console](/glossary/google-search-console) → Core Web Vitals report shows site-wide data. PageSpeed Insights gives per-page scores. Chrome DevTools → Performance panel shows the exact LCP element and timing for debugging.

### Can text be the LCP element?

Yes. If the largest visible element in the viewport is a text block (heading or paragraph), that becomes the LCP element. Text-only LCP pages typically score very well since text renders almost instantly once CSS loads.

---

Want fast-loading, SEO-optimized content published to your site automatically? theStacc publishes 30 articles per month. Built for performance and rankings. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google: Largest Contentful Paint Documentation](https://web.dev/articles/lcp)
- [Google Search Central: Core Web Vitals Report](https://support.google.com/webmasters/answer/9205520)
- [Google: Why Speed Matters ,  53% Mobile Bounce Study](https://www.thinkwithgoogle.com/marketing-strategies/app-and-mobile/mobile-page-speed-new-industry-benchmarks/)
- [Web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp)
- [Vodafone: Web Performance Case Study](https://web.dev/case-studies/vodafone)
