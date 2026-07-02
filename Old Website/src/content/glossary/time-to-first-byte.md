---
term: "Time to First Byte (TTFB)"
slug: "time-to-first-byte"
definition: "Time to First Byte (TTFB) is a speed metric that measures how long it takes for a browser to receive the first byte of data from the server after requesting a web page."
category: "SEO"
difficulty: "Beginner"
keyword: "what is time to first byte"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "page-speed"
  - "core-web-vitals"
  - "largest-contentful-paint"
  - "server-response-time"
  - "content-delivery-network"
---

## What Is Time to First Byte (TTFB)?

Time to First Byte (TTFB) measures the duration from when a browser makes an HTTP request to when it receives the first byte of the server's response. It captures the server's responsiveness before any content actually starts loading on the page.

**TTFB includes three phases:**

1. **Request travel time** — The browser sends the request to the server
2. **Server processing time** — The server processes the request, queries databases, runs application code
3. **Response travel time** — The server sends the first byte back to the browser

**TTFB does NOT include:**
- DNS lookup time (though some tools measure this separately)
- SSL/TLS handshake time (also measured separately)
- Time to download the full page
- Time to render the page

## Why TTFB Matters

TTFB is the foundation of page speed. Every other speed metric depends on it. If TTFB is slow, even the most optimized frontend cannot achieve good performance.

**The cascading effect:**

| Metric | Depends On |
|---|---|
| TTFB | Server response time |
| First Contentful Paint (FCP) | TTFB + render-blocking resources |
| Largest Contentful Paint (LCP) | TTFB + resource load times |
| Total Page Load Time | TTFB + all resource downloads |

**Example:** If TTFB is 2 seconds, even with perfect frontend optimization, LCP cannot be faster than 2 seconds plus the time to load the largest content element.

## TTFB Scoring Thresholds

| Rating | Time | Impact |
|---|---|---|
| Good | ≤ 600 milliseconds | Fast server response, quick page starts |
| Needs Improvement | 600 - 1800 milliseconds | Noticeable delay before content appears |
| Poor | > 1800 milliseconds | Users perceive the site as very slow |

**Target:** Keep TTFB under 600ms for the best user experience.

## What Causes Slow TTFB

### 1. Slow Hosting

Budget shared hosting plans often have slow server response times due to overcrowded servers.

**Fix:** Upgrade to VPS, dedicated, or cloud hosting. Use hosting near your target audience.

### 2. Database Queries

Complex or unoptimized database queries can take seconds to execute.

**Fix:**
- Add database indexes
- Optimize slow queries
- Use query caching
- Implement object caching (Redis, Memcached)

### 3. Server-Side Code

Heavy server-side processing — PHP, Python, Node.js — delays the response.

**Fix:**
- Profile and optimize application code
- Use opcode caching (OPcache for PHP)
- Minimize server-side rendering complexity

### 4. No Caching

Without caching, every request regenerates the entire page from scratch.

**Fix:**
- Implement page caching (Varnish, Nginx FastCGI cache)
- Use CDN edge caching
- Enable browser caching

### 5. Network Latency

Physical distance between the user and server affects TTFB.

**Fix:** Use a Content Delivery Network (CDN) to serve content from edge locations near users.

## How to Measure TTFB

### Browser DevTools

In Chrome DevTools Network tab:
1. Open DevTools (F12)
2. Go to Network tab
3. Reload the page
4. Click the first request (the document)
5. Look at "Waiting for server response" in the Timing tab

### WebPageTest

WebPageTest provides detailed TTFB measurements from multiple global locations:
- First View TTFB
- Repeat View TTFB
- TTFB by location

### Google Search Console

Core Web Vitals report shows TTFB data from real Chrome users (field data).

### Command Line

```bash
curl -o /dev/null -s -w "TTFB: %{time_starttransfer}\n" https://example.com
```

## How to Improve TTFB

### Hosting Optimizations

| Tactic | Expected Improvement | Effort |
|---|---|---|
| Upgrade hosting plan | 200-1000ms | Low |
| Use hosting near your audience | 50-300ms | Low |
| Enable HTTP/2 or HTTP/3 | 50-200ms | Low |
| Use a CDN | 100-500ms | Low |

### Application Optimizations

| Tactic | Expected Improvement | Effort |
|---|---|---|
| Implement page caching | 300-2000ms | Medium |
| Optimize database queries | 100-1000ms | Medium |
| Use opcode caching | 50-200ms | Low |
| Reduce server-side rendering | 100-500ms | Medium |
| Enable compression (Brotli/Gzip) | 20-50ms | Low |

### Code Optimizations

| Tactic | Expected Improvement | Effort |
|---|---|---|
| Minimize plugins/modules | 50-300ms | Medium |
| Lazy load non-critical resources | 20-100ms | Low |
| Remove unused code | 20-100ms | Medium |
| Optimize autoloaders | 10-50ms | Low |

## TTFB by Platform

| Platform | Typical TTFB | Optimization Potential |
|---|---|---|
| Static HTML (CDN) | 50-150ms | Already optimal |
| WordPress (cached) | 100-300ms | Good with caching |
| WordPress (uncached) | 500-2000ms | High — implement caching |
| Shopify | 200-500ms | Limited — platform-controlled |
| Custom application | 100-1000ms | Depends on code quality |

## TTFB Myths

**Myth: TTFB is the most important speed metric.**

TTFB is important but not sufficient. A page with 200ms TTFB but 10-second LCP is still slow. Optimize TTFB first, then focus on other metrics.

**Myth: You need perfect TTFB to rank well.**

Google considers TTFB as part of Page Experience, but content relevance and quality remain the primary ranking factors. A page with 800ms TTFB and excellent content can outrank a page with 200ms TTFB and mediocre content.

**Myth: TTFB only matters for the homepage.**

Every page has its own TTFB. Product pages, category pages, and blog posts all need fast server responses. Test TTFB for your highest-traffic page templates.

## Related Terms

- [Page Speed](/glossary/page-speed/)
- [Core Web Vitals](/glossary/core-web-vitals/)
- [Largest Contentful Paint](/glossary/largest-contentful-paint/)
- [Server Response Time](/glossary/server-response-time/)
- [Content Delivery Network](/glossary/content-delivery-network/)
