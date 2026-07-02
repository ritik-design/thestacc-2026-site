---
term: "Content Delivery Network (CDN)"
slug: "content-delivery-network"
definition: "A Content Delivery Network (CDN) is a distributed network of servers that caches and delivers website content from locations closer to users, reducing load times and improving global performance."
category: "SEO"
difficulty: "Beginner"
keyword: "what is a content delivery network"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "page-speed"
  - "time-to-first-byte"
  - "caching"
  - "edge-computing"
  - "core-web-vitals"
---

## What Is a Content Delivery Network (CDN)?

A Content Delivery Network (CDN) is a geographically distributed network of servers that work together to deliver website content faster to users around the world.

Without a CDN, every user connects directly to your origin server — no matter where they are. A user in Tokyo loading a website hosted in New York must wait for data to travel across the Pacific Ocean. With a CDN, that same user gets content from a server in Tokyo.

**How it works:**

1. User requests your website
2. CDN routes the request to the nearest edge server
3. If the edge server has the content cached, it delivers immediately
4. If not, the edge server fetches from your origin server, caches it, and delivers it
5. Future requests for the same content are served from the cache

## Why CDNs Matter for SEO

### Faster Page Load Times

CDNs reduce the physical distance between users and your content. This directly improves:

| Metric | CDN Impact |
|---|---|
| Time to First Byte (TTFB) | 30-70% reduction |
| First Contentful Paint (FCP) | 20-50% reduction |
| Largest Contentful Paint (LCP) | 20-40% reduction |
| Overall page load time | 20-60% reduction |

### Global Reach

If your audience is international, a CDN is essential. Without one:
- Users in Europe wait for content from your U.S. server
- Users in Asia experience 2-3x slower load times
- Users in Australia face the longest delays

**Example:** A website hosted in New York might have:
- 150ms TTFB for users in New York
- 400ms TTFB for users in London
- 800ms TTFB for users in Sydney

With a CDN, all users might see 150-250ms TTFB regardless of location.

### Reduced Server Load

CDNs absorb traffic spikes and reduce the load on your origin server. During viral traffic surges, the CDN serves cached content instead of overwhelming your server.

### Improved Security

Modern CDNs provide security features:
- DDoS protection (absorbing malicious traffic)
- Web Application Firewall (WAF)
- SSL/TLS encryption at the edge
- Bot detection and mitigation

### Better Uptime

If your origin server goes down, a CDN with stale-while-revalidate caching can continue serving cached content to users.

## What CDNs Cache

### Static Assets (Always Cached)

- Images (JPEG, PNG, WebP, AVIF)
- CSS and JavaScript files
- Fonts (WOFF, WOFF2)
- Videos and media files
- PDFs and downloadable files

### Dynamic Content (Configurable)

- HTML pages (with short cache times)
- API responses
- User-specific content (with care)

### Not Cached

- Personalized user data
- Shopping cart contents
- Form submissions
- Real-time data

## Popular CDN Providers

| Provider | Best For | Starting Cost |
|---|---|---|
| Cloudflare | All-around performance + security | Free tier available |
| Amazon CloudFront | AWS ecosystem integration | Pay-per-use |
| Google Cloud CDN | GCP ecosystem integration | Pay-per-use |
| Fastly | Enterprise, real-time purging | ~$50/month |
| KeyCDN | Simple, affordable pricing | ~$4/month |
| Bunny CDN | Budget-friendly, developer-friendly | ~$1/month |
| Akamai | Enterprise, largest network | Custom pricing |

## CDN Setup Checklist

### 1. Choose a CDN Provider

Consider:
- Number and location of edge servers (PoPs)
- Pricing model (bandwidth vs. requests)
- Ease of setup and management
- Security features included
- Cache purging speed

### 2. Point Your DNS to the CDN

Change your DNS records to route traffic through the CDN:

```
www.yoursite.com CNAME yoursite.cdn-provider.net
```

### 3. Configure Cache Rules

Set appropriate cache durations:

| Asset Type | Cache Duration | Reason |
|---|---|---|
| Images | 1 year | Rarely change, can version with filenames |
| CSS/JS | 1 year | Version in filenames (style.v2.css) |
| Fonts | 1 year | Never change |
| HTML pages | Hours to days | Content updates regularly |
| API responses | Minutes to hours | Data changes frequently |

### 4. Enable Compression

Ensure your CDN serves:
- Brotli compression (modern, 15-25% smaller than Gzip)
- Gzip compression (fallback for older browsers)
- Image optimization (auto-format, quality adjustment)

### 5. Test Performance

Before and after CDN implementation:
- Test from multiple global locations
- Measure TTFB, LCP, and overall load time
- Verify all assets load correctly from CDN URLs

## CDN Best Practices

**1. Use versioned filenames for static assets.**

Instead of `styles.css`, use `styles.v2.css`. This allows you to cache forever because the filename changes when the content changes.

**2. Configure proper cache headers.**

Set `Cache-Control` headers on your origin server to tell the CDN how long to cache each resource.

**3. Enable HTTP/2 or HTTP/3.**

Modern CDNs support multiplexed connections that load multiple assets simultaneously.

**4. Use a CDN for images.**

Images are typically 50-80% of page weight. A CDN with image optimization can:
- Automatically convert to WebP/AVIF
- Resize images for different devices
- Compress images without quality loss

**5. Monitor cache hit ratio.**

Aim for 80%+ cache hit ratio. Low ratios mean the CDN is frequently fetching from origin, reducing effectiveness.

## CDN Limitations

**1. First-time visitors still hit origin.**

If content is not cached at the edge, the first visitor from a new location experiences normal (slow) load times. The CDN caches it for subsequent visitors.

**2. Cache invalidation takes time.**

When you update content, purging CDN caches globally can take seconds to minutes. Some visitors may see old content during this window.

**3. Dynamic content benefits less.**

Personalized pages, real-time data, and user-specific content cannot be heavily cached. CDNs help with the static assets on these pages but not the dynamic HTML.

**4. Adds complexity.**

Debugging issues becomes harder when traffic flows through a CDN. You need to understand both your origin and the CDN layer.

## Related Terms

- [Page Speed](/glossary/page-speed/)
- [Time to First Byte](/glossary/time-to-first-byte/)
- [Caching](/glossary/caching/)
- [Edge Computing](/glossary/edge-computing/)
- [Core Web Vitals](/glossary/core-web-vitals/)
