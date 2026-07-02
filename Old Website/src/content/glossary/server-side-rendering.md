---
term: "Server-Side Rendering (SSR)"
slug: "server-side-rendering"
definition: "Server-Side Rendering (SSR) is a web development technique where HTML is generated on the server for each request, delivering fully rendered pages to browsers rather than empty containers that rely on JavaScript to load content."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is server side rendering"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "client-side-rendering"
  - "dynamic-rendering"
  - "prerendering"
  - "javascript-seo"
  - "core-web-vitals"
---

## What Is Server-Side Rendering (SSR)?

Server-Side Rendering (SSR) is a web architecture where the server generates the complete HTML for a page before sending it to the user's browser. When a user requests a page, they receive fully rendered content that can be immediately displayed — not an empty shell that needs JavaScript to populate.

**The SSR process:**

1. User requests a page
2. Server receives the request
3. Server fetches data from databases/APIs
4. Server renders the HTML with all content included
5. Browser receives complete HTML and displays it immediately
6. JavaScript hydrates the page to add interactivity

**Contrast with Client-Side Rendering (CSR):**

| Aspect | SSR | CSR |
|---|---|---|
| Initial HTML | Complete, with content | Empty container (often just `<div id="root"></div>`) |
| First meaningful paint | Immediate | After JavaScript loads and executes |
| JavaScript requirement | Works without JS (progressive enhancement) | Requires JS to display any content |
| Server load | Higher (rendering on every request) | Lower (just serves static files) |
| Interactivity | Requires hydration step | Already interactive after JS loads |

## Why SSR Matters for SEO

### Google Can Crawl the Content

Googlebot has improved at executing JavaScript, but it is not perfect. With CSR:
- Googlebot may not wait for all JavaScript to execute
- Dynamic content loaded after initial render might be missed
- Crawl budget is wasted rendering pages instead of discovering content

With SSR, Googlebot receives the fully rendered HTML immediately. Every piece of content is visible and indexable from the first crawl.

### Faster Core Web Vitals

SSR significantly improves Core Web Vitals metrics:

| Metric | SSR Impact |
|---|---|
| Largest Contentful Paint (LCP) | Faster — content is in the initial HTML |
| First Contentful Paint (FCP) | Faster — first paint happens immediately |
| Cumulative Layout Shift (CLS) | Better — content dimensions known upfront |
| Time to First Byte (TTFB) | Slightly slower — server needs time to render |

**Important trade-off:** SSR improves most metrics but can increase TTFB because the server must render before responding.

### Social Sharing

When someone shares a link on Twitter, Facebook, or LinkedIn, these platforms fetch the page to generate preview cards. Their bots do not execute JavaScript. SSR ensures they see the correct title, description, and images.

### Accessibility

Screen readers and users with JavaScript disabled can access SSR content immediately. CSR pages are blank or broken without JavaScript.

## SSR Implementation Approaches

### Framework-Based SSR

Modern frameworks support SSR natively:

| Framework | SSR Approach | Notes |
|---|---|---|
| Next.js (React) | `getServerSideProps` or App Router | Automatic SSR with React |
| Nuxt.js (Vue) | `asyncData` or `fetch` hooks | Vue-based SSR framework |
| SvelteKit | Server routes and page endpoints | Built-in SSR for Svelte |
| Angular Universal | Server-side rendering module | Google's official Angular SSR |
| Astro | Server-first architecture | Ships zero JS by default |

### Static Site Generation (SSG)

A hybrid approach where pages are rendered at build time, not on each request:

**SSG process:**
1. Build the site (render all pages to HTML)
2. Deploy static files to CDN
3. Users receive pre-rendered HTML instantly

**When to use SSG vs. SSR:**

| Factor | SSG | SSR |
|---|---|---|
| Content updates | Infrequent | Frequent |
| Number of pages | Small to medium | Large or dynamic |
| Personalization | None | User-specific content |
| Build time | Acceptable (seconds to minutes) | Not applicable (renders on request) |
| Hosting | Any static host | Requires server |

**Examples:**
- Blog posts → SSG (content rarely changes)
- E-commerce product pages → SSR (prices/inventory change constantly)
- User dashboards → SSR (personalized content)

### Dynamic Rendering

A hybrid approach where:
- Normal users get the regular JavaScript application (CSR)
- Search engine crawlers get a pre-rendered version (SSR)

**Implementation:** Use a service like Prerender.io, or tools like Puppeteer to render pages for bots.

**Google's stance:** Dynamic rendering is a workaround, not a long-term solution. Google recommends SSR or hydration instead.

## SSR Challenges

### Increased Server Load

Rendering HTML on every request requires more server resources than serving static files. During traffic spikes, SSR servers can become overwhelmed.

**Mitigation:**
- Implement caching at the CDN edge
- Use stale-while-revalidate strategies
- Scale server resources dynamically

### Hydration Complexity

After the server sends HTML, the client-side JavaScript must "hydrate" the page — attaching event listeners and making it interactive. If the hydrated state does not match the server-rendered HTML, users see errors or flickering.

### Waterfall Data Fetching

If a page needs data from multiple sources, SSR can create request waterfalls where each data dependency waits for the previous one to complete.

**Solution:** Use parallel data fetching, Suspense boundaries, or streaming SSR.

### TTFB Trade-Off

SSR increases Time to First Byte because the server must render before responding. For complex pages, this can add 200-500ms to TTFB.

**Solution:**
- Optimize server rendering performance
- Use edge rendering (render at CDN edge locations)
- Implement streaming SSR (send HTML as it is generated)

## SSR Best Practices

**1. Cache rendered pages.**
Cache SSR output at the CDN or server level to avoid re-rendering unchanged pages on every request.

**2. Use streaming SSR.**
Send the HTML `<head>` and layout immediately, then stream content as it renders. Users see the page skeleton instantly while content loads.

**3. Implement stale-while-revalidate.**
Serve cached HTML immediately, then re-render in the background and update the cache. Users always get fast responses.

**4. Minimize server-side JavaScript.**
Server rendering should be fast. Avoid heavy computations, complex loops, or synchronous API calls during render.

**5. Test with JavaScript disabled.**
Disable JavaScript in your browser and verify the page is usable. This simulates what search engines and screen readers experience.

## SSR vs. CSR vs. SSG: When to Use Each

| Scenario | Best Approach | Why |
|---|---|---|
| Blog or marketing site | SSG | Content rarely changes, fastest performance |
| E-commerce product pages | SSR | Prices, inventory change frequently |
| User dashboards | SSR | Personalized, dynamic content |
| Single-page application (SPA) | CSR + SSR for SEO | Complex interactivity, but SSR for crawlers |
| News site with breaking updates | SSR | Content changes by the minute |
| Documentation site | SSG | Content stable, speed is priority |

## Related Terms

- [Client-Side Rendering](/glossary/client-side-rendering/)
- [Dynamic Rendering](/glossary/dynamic-rendering/)
- [Prerendering](/glossary/prerendering/)
- [JavaScript SEO](/glossary/javascript-seo/)
- [Core Web Vitals](/glossary/core-web-vitals/)
