---
term: "Cumulative Layout Shift (CLS)"
slug: "cumulative-layout-shift"
definition: "Cumulative Layout Shift (CLS) is a Core Web Vitals metric that measures visual stability by tracking how much page elements unexpectedly move around during loading, scoring the total of all individual layout shifts."
category: "SEO"
difficulty: "Beginner"
keyword: "what is cumulative layout shift"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "core-web-vitals"
  - "page-speed"
  - "largest-contentful-paint"
  - "interaction-to-next-paint"
  - "page-experience"
---

## What Is Cumulative Layout Shift (CLS)?

Cumulative Layout Shift (CLS) is a Core Web Vitals metric that measures visual stability. It quantifies how much page elements move around unexpectedly while the page is loading.

**A layout shift occurs when:**
- A visible element changes its position on the page
- The change was not caused by user interaction
- The change affects content the user is already viewing

**Common causes of layout shifts:**
- Images without width and height attributes
- Ads or embeds that load after surrounding content
- Web fonts that cause text to reflow
- Content injected dynamically above existing content
- Cookie banners or pop-ups that push content down

## Why CLS Matters

Layout shifts create poor user experiences. A user reading an article might have the text jump down when an ad loads, causing them to lose their place. Someone about to click a button might have it shift at the last moment, causing them to click the wrong element.

**Real-world impact:**
- Users are 3x more likely to abandon a page with high CLS
- E-commerce sites with high CLS see 10-15% lower conversion rates
- News sites with unstable layouts have 20% higher bounce rates
- Accidental clicks on shifted elements lead to user frustration

## How CLS Is Calculated

CLS is calculated using a formula that considers both the distance an element moves and the size of the viewport affected:

**Impact fraction** × **Distance fraction** = **Layout shift score**

### Impact Fraction

The percentage of the viewport that is affected by the layout shift.

**Example:** If an element shifts and affects 50% of the viewport height, the impact fraction is 0.5.

### Distance Fraction

The distance the element moved relative to the viewport size.

**Example:** If an element moves down by 25% of the viewport height, the distance fraction is 0.25.

**Layout shift score:** 0.5 × 0.25 = 0.125

### Cumulative Score

CLS is the sum of all individual layout shift scores that occur during the entire lifespan of the page.

**Important change in 2021:** CLS is now calculated as the maximum session window of 5 seconds, rather than the entire page lifetime. This means brief shifts early in loading do not continue to accumulate as the user scrolls.

## CLS Scoring Thresholds

| Rating | Score | User Experience |
|---|---|---|
| Good | ≤ 0.1 | Elements stay where users expect them |
| Needs Improvement | 0.1 - 0.25 | Occasional shifts that cause minor annoyance |
| Poor | > 0.25 | Frequent or large shifts that disrupt reading and interaction |

**Target:** Keep CLS below 0.1 for at least 75% of page loads.

## Common Causes of Layout Shifts

### Images Without Dimensions

When an image loads without predefined width and height, the browser does not know how much space to reserve. The image pushes content down as it loads.

**Fix:** Always include width and height attributes on images and video elements.

```html
<!-- Bad -->
<img src="hero.jpg" alt="Hero image">

<!-- Good -->
<img src="hero.jpg" alt="Hero image" width="1200" height="600">
```

### Ads and Embeds

Advertisements, iframes, and embeds often load after the surrounding content, causing shifts.

**Fix:** Reserve space for ads and embeds using placeholder containers with fixed dimensions.

```css
.ad-container {
  min-height: 250px;
  width: 300px;
}
```

### Web Fonts

When a web font loads, it often has different dimensions than the fallback font, causing text to reflow.

**Fix:**
- Use `font-display: optional` or `font-display: swap`
- Preload critical fonts
- Use system fonts as fallbacks with similar dimensions

### Dynamic Content

Content injected above existing content — like cookie banners, newsletter sign-up forms, or "related article" widgets — pushes everything down.

**Fix:**
- Reserve space for dynamic content in the initial layout
- Use overlays instead of inline banners when possible
- Inject content at the bottom of the viewport, not the top

## How to Fix CLS Issues

### For Images

| Fix | Implementation |
|---|---|
| Add width and height attributes | `<img src="photo.jpg" width="800" height="600">` |
| Use aspect-ratio CSS | `img { aspect-ratio: 16 / 9; }` |
| Use responsive images with srcset | Specify dimensions for each image size |

### For Ads

| Fix | Implementation |
|---|---|
| Reserve ad space | Set min-height on ad containers |
| Collapse empty ad slots | Use `data-ad-status` to hide unfilled slots |
| Avoid placing ads near the top | Top-of-page ads cause the most disruptive shifts |

### For Fonts

| Fix | Implementation |
|---|---|
| Preload fonts | `<link rel="preload" href="font.woff2" as="font">` |
| Use font-display: optional | `font-display: optional` shows fallback first |
| Match fallback font metrics | Choose a fallback font with similar sizing |

### For Dynamic Content

| Fix | Implementation |
|---|---|
| Reserve space | Include placeholder elements in initial HTML |
| Use skeleton screens | Show loading states that match final dimensions |
| Avoid top-of-page injections | Place dynamic content below the fold |

## CLS Testing Tools

| Tool | What It Shows | Cost |
|---|---|---|
| Chrome DevTools | Individual layout shifts in Performance panel | Free |
| Lighthouse | CLS score and specific elements causing shifts | Free |
| PageSpeed Insights | Field and lab CLS data | Free |
| Web Vitals Chrome Extension | Real-time CLS as you browse | Free |
| Google Search Console | CLS issues across your entire site | Free |

## CLS Myths

**Myth: CLS only matters during initial page load.**

CLS measures shifts throughout the entire page session. Scrolling, lazy loading images, and dynamic content can all cause shifts after the initial load.

**Myth: Animations and transitions hurt CLS.**

CLS only counts unexpected shifts. Animations that users trigger (like expanding an accordion) or transitions that are part of the design do not count.

**Myth: CLS is less important than LCP.**

Google considers all three Core Web Vitals equally important for Page Experience. Poor CLS can hurt rankings just as much as poor LCP.

## Related Terms

- [Core Web Vitals](/glossary/core-web-vitals/)
- [Page Speed](/glossary/page-speed/)
- [Largest Contentful Paint](/glossary/largest-contentful-paint/)
- [Interaction to Next Paint](/glossary/interaction-to-next-paint/)
- [Page Experience](/glossary/page-experience/)
