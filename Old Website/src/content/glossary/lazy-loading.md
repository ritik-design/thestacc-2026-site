---
term: "Lazy Loading"
slug: "lazy-loading"
definition: "Lazy loading is a web performance technique that delays loading non-critical resources such as images and videos until they are about to enter the user's viewport, reducing initial page weight and improving load times."
category: "SEO"
difficulty: "Beginner"
keyword: "what is lazy loading"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "core-web-vitals"
  - "largest-contentful-paint"
  - "cumulative-layout-shift"
  - "page-speed"
  - "render-blocking"
---

## What Is Lazy Loading?

Lazy loading is a performance optimization technique that defers the loading of certain page resources until they are actually needed. Instead of downloading every image, video, and iframe when the page first loads, the browser only loads content as the user scrolls near it.

This reduces the initial page payload, lowers bandwidth usage, and improves metrics like Largest Contentful Paint and overall page speed.

## How Lazy Loading Works

When lazy loading is implemented, the browser initially loads only the content visible in the viewport. For images and videos below the fold, the browser places a lightweight placeholder. As the user scrolls down, the browser detects when these elements approach the viewport and then loads the actual media files.

Modern browsers support native lazy loading through the `loading="lazy"` attribute on images and iframes. For more advanced use cases, JavaScript libraries like Lazysizes or Intersection Observer-based scripts provide additional control.

## Native Lazy Loading Example

```html
<img src="image.jpg" alt="Description" loading="lazy" width="800" height="600">
```

The `loading` attribute accepts three values:

| Value | Behavior |
|---|---|
| `lazy` | Defers loading until the element approaches the viewport |
| `eager` | Loads the resource immediately, regardless of position |
| `auto` | Lets the browser decide whether to lazy load |

## Why Lazy Loading Matters for SEO

### Faster Initial Page Load

Pages with many images or videos can have large initial payloads. Lazy loading reduces what the browser must download upfront, improving load times and Core Web Vitals scores.

### Reduced Bandwidth Usage

Users on mobile or metered connections benefit because they only download media they actually view. This is especially important for long articles and image-heavy category pages.

### Better Crawl Efficiency

While Googlebot can scroll and execute JavaScript, reducing the number of immediate requests helps pages render faster and makes content more accessible to search engines.

### Improved User Experience

Faster perceived performance leads to lower bounce rates and longer dwell times, both of which correlate with better engagement and rankings.

## What Should Be Lazy Loaded?

| Resource Type | Lazy Load? | Notes |
|---|---|---|
| Below-the-fold images | Yes | Default candidate for lazy loading |
| Above-the-fold images | No | Load immediately to avoid LCP delays |
| Below-the-fold videos | Yes | Heavy files benefit most |
| Embedded iframes | Yes | Maps, ads, and third-party widgets |
| Comments sections | Often | Load when user scrolls to comments |
| Infinite scroll content | Yes | Load additional items on demand |
| Hero images | No | Must load immediately for LCP |

## Lazy Loading and Core Web Vitals

Lazy loading directly impacts three Core Web Vitals:

### Largest Contentful Paint (LCP)

If above-the-fold images are lazy loaded, they may delay LCP. Always mark hero images and other critical above-the-fold content with `loading="eager"` or omit the attribute entirely.

### Cumulative Layout Shift (CLS)

Lazy-loaded images must have explicit `width` and `height` attributes or CSS aspect ratios. Without dimensions, the placeholder collapses when the image loads, causing layout shifts.

### Interaction to Next Paint (INP)

By reducing main-thread work during initial load, lazy loading can improve interactivity. However, poorly implemented JavaScript-based lazy loading can itself block the main thread.

## Common Lazy Loading Mistakes

### Lazy Loading Above-the-Fold Content

Applying lazy loading to hero images or above-the-fold content delays LCP and hurts user experience. Critical content should always load immediately.

### Missing Dimensions

Images without width and height attributes cause layout shifts when they load. Always specify dimensions or use CSS to reserve space.

### Hiding Content from Search Engines

Some lazy loading implementations load content only on user interaction, which may prevent Googlebot from discovering it. Ensure important content is accessible without requiring user input.

### Overusing JavaScript Libraries

Heavy lazy loading libraries can add unnecessary JavaScript. Native lazy loading with `loading="lazy"` is supported by all modern browsers and requires no additional scripts.

## Best Practices for Lazy Loading

- Use native lazy loading with `loading="lazy"` where browser support is sufficient
- Always include width and height attributes on images
- Reserve space with CSS aspect-ratio to prevent CLS
- Use `loading="eager"` for above-the-fold and LCP images
- Test implementation using Chrome DevTools and PageSpeed Insights
- Provide meaningful alt text so content remains accessible
- Use fallback scripts only when supporting older browsers

## Frequently Asked Questions

### Does Google index lazy-loaded images?

Yes. Googlebot processes lazy-loaded content, especially when using native browser lazy loading. For JavaScript-based solutions, ensure that image URLs are present in the HTML source or accessible via rendered DOM.

### Should all images be lazy loaded?

No. Only below-the-fold images should be lazy loaded. Above-the-fold images should load immediately to support LCP and user experience.

### Is lazy loading good for SEO?

Yes, when implemented correctly. It improves page speed and bandwidth usage. Poor implementation can harm LCP and CLS, so following best practices is essential.

### What is eager loading?

Eager loading is the opposite of lazy loading. It loads resources immediately when the page loads, regardless of whether they are currently visible.

## Summary

Lazy loading is a simple but powerful performance optimization. By deferring below-the-fold media until it is needed, websites can reduce initial load times, improve Core Web Vitals, and create a better experience for users and search engines. The key is to use it strategically while protecting critical above-the-fold content.
