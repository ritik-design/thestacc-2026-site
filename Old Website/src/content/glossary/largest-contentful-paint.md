---
term: "Largest Contentful Paint (LCP)"
slug: "largest-contentful-paint"
definition: "Largest Contentful Paint (LCP) is a Core Web Vitals metric that measures how long it takes for the largest visible content element on a page to load and render, indicating perceived load speed."
category: "SEO"
difficulty: "Beginner"
keyword: "what is largest contentful paint"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "core-web-vitals"
  - "page-speed"
  - "interaction-to-next-paint"
  - "cumulative-layout-shift"
  - "page-experience"
---

## What Is Largest Contentful Paint (LCP)?

Largest Contentful Paint (LCP) is one of Google's three Core Web Vitals metrics. It measures the time from when the page starts loading to when the largest visible content element is fully rendered on the screen.

LCP answers a simple question: **How fast does the main content appear?**

Users do not care when the last pixel loads. They care when they can see and interact with the page's primary content. LCP measures that moment.

## What Elements Count for LCP?

The "largest contentful element" is typically one of these:

- **Image elements** (<img> tags, including those inside <svg>)
- **Image background** (CSS background images loaded via url())
- **Video elements** (the poster image or the video itself)
- **Block-level text elements** (<p>, <h1>, <div> with text content)

**What does NOT count:**
- Elements in the overflow (below the fold)
- Background patterns or gradients
- Icons and small decorative images
- Elements hidden with opacity: 0

## LCP Scoring Thresholds

| Rating | Time | User Experience |
|---|---|---|
| Good | ≤ 2.5 seconds | Content appears quickly, user feels the site is fast |
| Needs Improvement | 2.5 - 4.0 seconds | User notices a delay, may become impatient |
| Poor | > 4.0 seconds | User perceives the site as slow, likely to leave |

**Key statistic:** Pages with LCP under 2.5 seconds have 24% lower bounce rates than pages with LCP over 4 seconds (Google).

## How to Measure LCP

### Field Data (Real Users)

**Chrome User Experience Report (CrUX):** Real-world LCP data from Chrome users, available in Google Search Console and PageSpeed Insights.

**JavaScript API:**
```javascript
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP:', lastEntry.startTime);
}).observe({ entryTypes: ['largest-contentful-paint'] });
```

### Lab Data (Simulated)

**Lighthouse:** Simulates page load on a mid-tier mobile device and reports LCP.

**WebPageTest:** Tests from multiple locations and connection speeds.

**Important:** Field data is what Google uses for ranking. Lab data helps you debug but may not match real-world performance.

## What Causes Poor LCP

### 1. Slow Server Response Times

If your server takes 2 seconds to respond, LCP cannot be faster than 2 seconds.

**Fix:** Upgrade hosting, use caching, optimize database queries, enable keep-alive connections.

### 2. Render-Blocking Resources

CSS and JavaScript files that prevent the browser from rendering content until they are fully loaded.

**Fix:**
- Inline critical CSS
- Defer non-critical JavaScript
- Remove unused CSS and JS

### 3. Slow Resource Load Times

Large images, unoptimized videos, or slow-loading fonts delay LCP.

**Fix:**
- Compress images (WebP format, responsive images)
- Preload critical resources
- Use a Content Delivery Network (CDN)

### 4. Client-Side Rendering

Pages built entirely with JavaScript must download, parse, and execute JS before content appears.

**Fix:** Use server-side rendering (SSR) or static site generation (SSG) for critical content.

## How to Improve LCP

### Optimize Your Server

| Tactic | Impact | Effort |
|---|---|---|
| Enable caching | High | Low |
| Use a CDN | High | Low |
| Upgrade hosting | High | Medium |
| Optimize database queries | Medium | Medium |
| Enable HTTP/2 or HTTP/3 | Medium | Low |

### Optimize Images

| Tactic | Impact | Effort |
|---|---|---|
| Compress images | High | Low |
| Convert to WebP/AVIF | High | Low |
| Use responsive images | High | Medium |
| Set explicit width and height | Medium | Low |
| Preload hero images | High | Low |

### Optimize CSS

| Tactic | Impact | Effort |
|---|---|---|
| Inline critical CSS | High | Medium |
| Defer non-critical CSS | Medium | Medium |
| Remove unused CSS | Medium | Medium |
| Minify CSS files | Low | Low |

### Optimize JavaScript

| Tactic | Impact | Effort |
|---|---|---|
| Defer non-critical JS | High | Low |
| Code splitting | Medium | Medium |
| Remove unused JS | Medium | Medium |
| Minify JS files | Low | Low |

## LCP Optimization Checklist

**Quick wins (under 1 hour):**
- [ ] Compress and convert hero images to WebP
- [ ] Preload the LCP image with <link rel="preload">
- [ ] Set explicit width and height on images
- [ ] Enable browser caching

**Medium effort (1-4 hours):**
- [ ] Implement a CDN
- [ ] Inline critical CSS
- [ ] Defer non-critical JavaScript
- [ ] Upgrade to HTTP/2

**High effort (4+ hours):**
- [ ] Implement server-side rendering
- [ ] Optimize database and API responses
- [ ] Implement edge caching
- [ ] Migrate to faster hosting

## LCP Myths

**Myth: LCP is the same as page load time.**

LCP measures when the largest visible element renders. Page load time measures when every resource finishes loading. A page can have good LCP (2 seconds) but slow total load time (8 seconds).

**Myth: LCP only matters for mobile.**

Google measures LCP separately for mobile and desktop. Both matter for rankings. Mobile LCP is typically worse due to slower connections and less processing power.

**Myth: You need perfect LCP to rank.**

LCP is one of hundreds of ranking factors. A page with LCP of 3 seconds but excellent content can outrank a page with LCP of 1.5 seconds and mediocre content. LCP is a tiebreaker, not a primary ranking signal.

## Related Terms

- [Core Web Vitals](/glossary/core-web-vitals/)
- [Page Speed](/glossary/page-speed/)
- [Interaction to Next Paint](/glossary/interaction-to-next-paint/)
- [Cumulative Layout Shift](/glossary/cumulative-layout-shift/)
- [Page Experience](/glossary/page-experience/)
