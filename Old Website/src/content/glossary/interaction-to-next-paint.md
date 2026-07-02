---
term: "Interaction to Next Paint (INP)"
slug: "interaction-to-next-paint"
definition: "Interaction to Next Paint (INP) is a Core Web Vitals metric that measures how quickly a web page responds to user interactions like clicks, taps, and key presses, replacing First Input Delay (FID) as the responsiveness metric."
category: "SEO"
difficulty: "Beginner"
keyword: "what is interaction to next paint"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "core-web-vitals"
  - "first-input-delay"
  - "page-speed"
  - "largest-contentful-paint"
  - "page-experience"
---

## What Is Interaction to Next Paint (INP)?

Interaction to Next Paint (INP) is a Core Web Vitals metric that measures how responsive a web page is to user interactions. It replaced First Input Delay (FID) in March 2024 as the official responsiveness metric.

**The key difference from FID:**

| Metric | Measures | Limitation |
|---|---|---|
| First Input Delay (FID) | Delay before the first interaction is processed | Only measures the first interaction |
| Interaction to Next Paint (INP) | Latency of all interactions throughout the page session | Captures the worst-performing interactions |

INP measures the time from when a user interacts with the page (clicks a button, taps a link, presses a key) to when the browser paints the visual feedback for that interaction. This gives a much more complete picture of a page's responsiveness than FID, which only measured the very first interaction.

## How INP Is Calculated

INP tracks all click, tap, and keyboard interactions during a page session. For each interaction, it measures:

1. **Input delay:** Time between user action and when the browser starts processing
2. **Processing time:** Time to run event handlers
3. **Presentation delay:** Time to paint the next frame showing the interaction result

**INP is the worst interaction latency** (or the 98th percentile for pages with many interactions). If a user clicks 50 times and one click takes 800ms while the rest take 50ms, INP reports 800ms.

## INP Scoring Thresholds

| Rating | Time | User Experience |
|---|---|---|
| Good | ≤ 200 milliseconds | Page feels instantly responsive |
| Needs Improvement | 200 - 500 milliseconds | Users notice occasional lag |
| Poor | > 500 milliseconds | Page feels sluggish and frustrating |

**Target:** Keep INP under 200ms for at least 75% of page loads.

## Why INP Matters

### User Frustration

Slow interactions are one of the most frustrating web experiences. A user who clicks a button and sees no response for half a second assumes the page is broken.

**Impact of poor INP:**
- 32% higher bounce rate on pages with INP > 500ms
- 15% lower conversion rate on slow-interaction checkout flows
- Users are 2x more likely to abandon forms with delayed feedback

### Task Completion

Slow interactions compound. A checkout process with 5 steps, each with 300ms delay, feels unbearably slow. The same process with 50ms interactions feels seamless.

### Google Ranking Factor

INP is a confirmed ranking factor through the Page Experience signal. Pages with poor INP may be outranked by equally relevant pages with better responsiveness.

## What Causes Poor INP

### Long JavaScript Tasks

When JavaScript runs for a long time without yielding control back to the browser, interactions are delayed.

**Example:** A script that processes 10,000 data points in a single loop blocks all interactions until it finishes.

### Heavy Event Handlers

Click handlers that perform complex calculations, DOM manipulations, or API calls before showing feedback.

**Example:** A "Add to cart" button that synchronously updates the entire page state before showing any visual response.

### Third-Party Scripts

Analytics trackers, chat widgets, and advertising scripts often run on the main thread, competing with user interactions.

### Main Thread Congestion

Too many tasks competing for the main thread — rendering, scripting, and user input all fighting for the same resource.

## How to Improve INP

### 1. Break Up Long Tasks

Split large JavaScript tasks into smaller chunks using `setTimeout`, `requestIdleCallback`, or `scheduler.yield()`.

**Before:**
```javascript
function processLargeDataset(data) {
  // Blocks for 2+ seconds
  for (let i = 0; i < data.length; i++) {
    heavyComputation(data[i]);
  }
}
```

**After:**
```javascript
async function processLargeDataset(data) {
  for (let i = 0; i < data.length; i++) {
    heavyComputation(data[i]);
    if (i % 50 === 0) {
      await scheduler.yield(); // Allows interactions to process
    }
  }
}
```

### 2. Optimize Event Handlers

Show visual feedback immediately, then do the heavy work.

**Before:**
```javascript
button.addEventListener('click', () => {
  validateForm();        // 200ms
  submitToServer();      // 500ms
  updateUI();            // 100ms
  showSuccessMessage();  // Finally shows feedback
});
```

**After:**
```javascript
button.addEventListener('click', () => {
  button.classList.add('loading'); // Immediate feedback
  requestAnimationFrame(() => {
    validateForm();
    submitToServer();
    updateUI();
    showSuccessMessage();
  });
});
```

### 3. Defer Non-Critical Third-Party Scripts

Load analytics, chat widgets, and social buttons after the page is interactive.

```html
<script defer src="analytics.js"></script>
<script async src="chat-widget.js"></script>
```

### 4. Use Web Workers

Move heavy computations off the main thread entirely.

```javascript
const worker = new Worker('calculator.js');
worker.postMessage(largeDataset);
worker.onmessage = (event) => {
  displayResults(event.data);
};
```

### 5. Reduce DOM Size

Large DOMs (10,000+ nodes) slow down rendering and interactions.

- Remove unused elements
- Use virtual scrolling for long lists
- Simplify CSS selectors
- Minimize nested DOM depth

## INP Optimization Checklist

**Quick wins:**
- [ ] Show loading states immediately on button clicks
- [ ] Defer non-critical JavaScript
- [ ] Remove unused third-party scripts

**Medium effort:**
- [ ] Break up long JavaScript tasks
- [ ] Optimize event handlers for immediate feedback
- [ ] Implement virtual scrolling for large lists

**High effort:**
- [ ] Move heavy logic to web workers
- [ ] Reduce overall DOM size
- [ ] Implement server-side rendering

## INP Testing Tools

| Tool | What It Shows | Cost |
|---|---|---|
| Chrome DevTools Performance Panel | Individual interaction latencies | Free |
| Lighthouse | INP score and longest interactions | Free |
| PageSpeed Insights | Field and lab INP data | Free |
| Web Vitals Extension | Real-time INP as you browse | Free |
| Google Search Console | INP issues across your site | Free |

## INP vs. FID: What's Different?

| Aspect | FID (Old) | INP (Current) |
|---|---|---|
| What it measures | First interaction delay only | All interactions throughout session |
| Metric type | Single measurement | Worst-case (or 98th percentile) |
| Captures | Input delay only | Full interaction duration |
| Session length | N/A (only first interaction) | Entire page lifetime |
| Rolling out | Deprecated March 2024 | Official metric from March 2024 |

## Related Terms

- [Core Web Vitals](/glossary/core-web-vitals/)
- [First Input Delay](/glossary/first-input-delay/)
- [Page Speed](/glossary/page-speed/)
- [Largest Contentful Paint](/glossary/largest-contentful-paint/)
- [Page Experience](/glossary/page-experience/)
