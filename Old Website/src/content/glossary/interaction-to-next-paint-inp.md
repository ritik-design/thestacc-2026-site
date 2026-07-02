---
term: "Interaction to Next Paint (INP)"
slug: "interaction-to-next-paint-inp"
definition: "Interaction to Next Paint (INP) is a Core Web Vitals metric that measures how quickly a page visually responds to user interactions like clicks, taps, and."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is interaction to next paint inp"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "core-web-vitals"
  - "largest-contentful-paint-lcp"
  - "cumulative-layout-shift-cls"
  - "page-speed"
  - "technical-seo"
---

## What is Interaction to Next Paint (INP)?

Interaction to Next Paint (INP) measures the time between a user interacting with your page. A click, tap, or key press. And the browser displaying the next visual update in response.

It's Google's way of quantifying how "snappy" a page feels. Not just the first interaction, like the old First Input Delay (FID) metric tracked. INP considers *every* interaction during a user's visit and reports the worst one (with some statistical smoothing for outliers). If your page responds instantly to a button click but freezes for 400ms when someone opens a dropdown menu. INP catches that.

Google officially replaced FID with INP as a [Core Web Vitals](/glossary/core-web-vitals) metric in March 2024. The bar: pages should respond to interactions in under 200 milliseconds. According to Chrome UX Report data, roughly 65% of websites met that threshold at launch. The rest have work to do.

## Why Does INP Matter?

A slow-responding page frustrates users. That frustration has measurable consequences.

- **It's a direct Google ranking signal**. INP is one of three [Core Web Vitals](/glossary/core-web-vitals) that feed into Google's page experience ranking system. Failing INP can suppress your rankings.
- **Users abandon unresponsive pages**. Research from Google shows a 100ms increase in interaction latency reduces conversion rates by up to 7%. Users don't wait for sluggish interfaces.
- **It captures the full session, not just the first click**. FID only measured the *first* interaction. INP measures responsiveness throughout the entire visit, making it a much more accurate reflection of real user experience.
- **Mobile impact is amplified**. Lower-powered mobile devices struggle more with heavy JavaScript. Since Google uses [mobile-first indexing](/glossary/mobile-first-indexing), INP problems on mobile directly affect your rankings.

Any site with interactive elements. Forms, menus, accordions, filters, carousels. Needs to pay attention to INP. Static content pages usually pass without issues.

## How INP Works

INP breaks each interaction into three phases. Understanding them is key to fixing problems.

### Input Delay

The time between when the user interacts (clicks a button, presses a key) and when the browser starts running the event handler code. Long input delays happen when the main thread is busy executing other JavaScript. If a third-party analytics script is running a heavy computation when someone clicks your "Add to Cart" button. That's input delay.

### Processing Time

The actual time spent running your event handler code. If clicking a filter triggers a complex function that recalculates and re-renders a product list, that processing time counts toward INP. Inefficient JavaScript, DOM manipulation, and synchronous API calls are the usual culprits.

### Presentation Delay

The time from when event handlers finish to when the browser paints the next frame. The browser needs to recalculate styles, update layout, composite layers, and render pixels. Heavy CSS, large DOM trees, and expensive paint operations slow this phase down.

Google measures INP as the sum of all three phases for each interaction, then reports the interaction at the 98th percentile (the worst interaction, ignoring extreme outliers). Your INP score is only as good as your slowest meaningful interaction.

## Types of Interactions INP Tracks

INP doesn't track every user action. Only discrete interactions that expect a visual response:

- **Clicks**. Mouse clicks and trackpad taps on buttons, links, checkboxes, and other interactive elements
- **Taps**. Touch interactions on mobile devices. Tap to open a menu, tap to submit a form, tap to expand an accordion.
- **Key presses**. Typing in form fields, pressing Enter to submit, keyboard navigation. Each keystroke is a measured interaction.
- **Not tracked: scrolling**. Scroll is continuous, not discrete, so it's excluded from INP. Scroll performance has its own metrics.
- **Not tracked: hover**. Mouse hover doesn't count as an interaction for INP purposes.

For most sites, the worst INP interactions happen on complex elements: dropdown menus, filter systems, image carousels, and form submissions.

## INP Examples

**An e-commerce product page.** A user taps the "Size" dropdown on mobile. The page has 14 third-party scripts running. Analytics, chat widgets, recommendation engines. The main thread is blocked for 380ms before the dropdown even starts to open. INP score: 420ms. Poor. The fix: defer non-critical scripts, move heavy computations to web workers, and lazy-load third-party tools.

**A local restaurant's reservation form.** Someone fills out the form and taps "Submit." The page runs client-side validation, sends the request, and shows a confirmation. All within 120ms. INP score: 120ms. Good. Simple pages with minimal JavaScript naturally perform well on INP.

**A real estate listing site built with theStacc's content.** The blog section ,  30 articles published monthly. Runs on a lightweight [CMS](/glossary/content-management-system) with minimal JavaScript. INP scores consistently under 100ms. But the property search page, with its complex filter system and map integration, scores 350ms. Same site, very different INP performance. The lesson: INP is measured per page, not per site.

## INP vs. First Input Delay (FID)

FID measured only the first interaction. INP replaced it because a page that responds quickly to the first click but chokes on the fifth isn't actually responsive.

| | INP | FID (deprecated) |
|---|---|---|
| **What it measures** | Responsiveness across ALL interactions | Only the FIRST interaction |
| **Score reported** | 98th percentile of all interactions | Single first-interaction delay |
| **Includes processing time** | Yes. Input delay + processing + presentation | No. Only input delay |
| **Became Core Web Vital** | March 2024 | 2020-2024 |
| **Good threshold** | Under 200ms | Under 100ms |

INP is a harder bar to clear than FID was. Many sites that passed FID comfortably fail INP because their later interactions (not just the first one) are slow.

## INP Best Practices

- **Audit your worst interactions first**. Use Chrome DevTools' Performance panel or the Web Vitals Chrome extension to identify which specific interactions have the highest latency. Fix the worst offender before optimizing everything else.
- **Reduce JavaScript execution on the main thread**. Break up long tasks (anything over 50ms) using `requestIdleCallback`, `setTimeout`, or the newer `scheduler.yield()` API. The main thread needs to stay free to respond to user input.
- **Defer third-party scripts**. Analytics, chat widgets, and ad scripts are the most common INP killers. Load them with `defer` or `async`, or delay them until after the page becomes interactive.
- **Minimize DOM size**. Pages with 3,000+ DOM elements take longer to re-render after interactions. Simplify your HTML structure. [Technical SEO](/glossary/technical-seo) audits should flag excessive DOM depth.
- **Use `content-visibility: auto` for off-screen content**. This CSS property tells the browser to skip rendering elements not visible in the viewport, dramatically reducing presentation delay. Sites publishing high volumes of content. Like those using theStacc for 30 articles/month. Benefit from efficient page templates that keep DOM size in check.

## Frequently Asked Questions

### What's a good INP score?

Under 200ms is "good" by Google's standards. Between 200-500ms is "needs improvement." Over 500ms is "poor." Most sites should aim for under 150ms to stay safely in the green.

### Does INP affect rankings?

Yes. INP is one of three [Core Web Vitals](/glossary/core-web-vitals) that factor into Google's page experience ranking signal. It won't override content relevance, but between two equally relevant pages, the one with better INP gets the edge.

### How do I measure INP?

Google Search Console's Core Web Vitals report shows field data. PageSpeed Insights and Chrome UX Report provide page-level scores. For debugging, use Chrome DevTools' Performance panel to trace individual interactions.

### Can static pages fail INP?

Rarely. Pages without JavaScript-heavy interactions almost always score under 100ms. INP problems are concentrated on pages with complex interactivity. Filters, forms, dynamic menus, and client-side rendering.

---

Want to publish fast-loading, INP-friendly content without managing the technical details? theStacc publishes 30 SEO-optimized articles to your site every month. Built for performance. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google: Interaction to Next Paint (INP) Documentation](https://web.dev/articles/inp)
- [Google Search Central: Core Web Vitals and Page Experience](https://developers.google.com/search/docs/appearance/core-web-vitals)
- [Chrome for Developers: INP Replaces FID](https://developer.chrome.com/blog/inp-cwv-launch)
- [Web.dev: Optimize Interaction to Next Paint](https://web.dev/articles/optimize-inp)
- [Ahrefs: Core Web Vitals and Rankings Study](https://ahrefs.com/blog/core-web-vitals/)
