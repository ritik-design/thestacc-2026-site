---
term: "Redirect Chain"
slug: "redirect-chain"
definition: "A redirect chain occurs when a URL redirects to another URL, which redirects to yet another URL. Creating multiple hops that waste crawl budget, slow."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is redirect chain"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "301-redirect"
  - "crawl-budget"
  - "link-equity"
  - "technical-seo"
  - "page-speed"
---

## What is a Redirect Chain?

A redirect chain happens when a URL passes through two or more redirects before reaching the final destination page. Creating unnecessary hops that waste time, authority, and crawl resources.

The typical chain looks like this: Page A redirects to Page B, which redirects to Page C, which finally loads. Each hop adds latency, and Google may drop some [link equity](/glossary/link-equity) at each step. Google's John Mueller has stated that Googlebot follows up to 5 redirects in a chain before giving up. But that doesn't mean chains are harmless.

Redirect chains are one of the most common [technical SEO](/glossary/technical-seo) issues. An Ahrefs study of 10 million domains found that 17% of sites had redirect chains affecting their most important pages.

## Why Do Redirect Chains Matter?

Every extra redirect costs you performance and authority.

- **[Link equity](/glossary/link-equity) loss**. While Google says redirects pass most PageRank, practical testing shows some dilution at each hop
- **Slower page load**. Each redirect adds 50-500ms of latency, which compounds across multiple hops
- **Wasted [crawl budget](/glossary/crawl-budget)**. Googlebot spends requests following redirect chains instead of crawling your actual content
- **User experience degrades**. Visitors on slow connections notice the added loading time, increasing [bounce rates](/glossary/bounce-rate)

One redirect is fine. Two is tolerable. Three or more signals a structural problem that needs fixing.

## How Redirect Chains Work

### How They Form

Chains build up over time. You move a page from URL A to URL B (creating redirect 1). A year later, you restructure and move it to URL C (creating redirect 2). Now the original backlinks follow a 2-hop chain. Repeat this through site redesigns, CMS migrations, and domain changes, and chains of 4-5 hops aren't unusual.

### Detecting Them

Run a full crawl with Screaming Frog, Sitebulb, or Ahrefs Site Audit. These tools flag redirect chains and show you the full hop sequence. Check your most-linked pages first. Those have the most authority to lose.

### Fixing Them

Update every redirect in the chain to point directly to the final destination. Page A should redirect straight to Page C. Then update [internal links](/glossary/internal-link) throughout your site to point to the final URL directly, eliminating the redirect entirely. For external backlinks you can't control, the direct redirect from first URL to final URL is the best you can do.

## Redirect Chain Examples

**A real estate website** redesigns twice over 5 years. Their top blog post ,  "How to Buy a House in Austin". Originally lived at `/blog/buying-house-austin`, then moved to `/guides/homebuying-austin`, then to `/austin/homebuying-guide`. Each move added a redirect. The post had 230 [backlinks](/glossary/backlinks) following a 3-hop chain. Collapsing the chain into a single [301 redirect](/glossary/301-redirect) from both old URLs to the final URL recovered lost link equity. Rankings improved from position 8 to position 3.

**A SaaS company** migrates from WordPress to a custom CMS. The old URL structure (`/blog/post-title`) redirects to a temporary structure (`/articles/post-title`), which later redirects to the final structure (`/resources/blog/post-title`). With theStacc publishing 30 new articles per month, catching and fixing these chains early prevents compounding problems.
## Frequently Asked Questions

### Do redirect chains really lose link equity?

Google says [301 redirects](/glossary/301-redirect) pass PageRank, but the SEO community has observed practical authority loss through chains. Even if the loss per hop is small, it compounds. A 3-hop chain measurably underperforms a single direct redirect in most tests.

### How many redirects is too many?

One redirect is ideal. Two is acceptable for temporary situations. Three or more should always be consolidated. Google will follow up to 5 hops, but that's a ceiling, not a recommendation.

### Should I fix all redirect chains at once?

Prioritize by impact. Fix chains on your most-linked and highest-traffic pages first. Use a site audit tool to sort chains by the number of inbound backlinks affected.

---

Want a technically clean site with fresh content? theStacc publishes 30 SEO-optimized articles to your site every month. No messy redirects. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Ahrefs: How to Find and Fix Redirect Chains](https://ahrefs.com/blog/redirect-chains/)
- [Screaming Frog: Redirect Chain Detection](https://www.screamingfrog.co.uk/seo-spider/)
- [Moz: Redirection for SEO](https://moz.com/learn/seo/redirection)
