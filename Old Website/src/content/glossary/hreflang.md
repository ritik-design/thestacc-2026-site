---
term: "Hreflang"
slug: "hreflang"
definition: "Hreflang is an HTML attribute that tells search engines which language and regional version of a page to show to users in different locations. It prevents."
category: "SEO"
difficulty: "Advanced"
keyword: "what is hreflang"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "duplicate-content"
  - "geotargeting"
  - "canonical-url"
  - "meta-robots-tag"
  - "hreflang"
---

## What is Hreflang?

Hreflang is an HTML attribute (rel="alternate" hreflang="x") that signals to Google and other search engines which language and country a specific page version targets.

If your site has pages in multiple languages or region-specific versions (English for US vs. English for UK), hreflang prevents Google from treating them as [duplicate content](/glossary/duplicate-content). Without it, Google picks one version to show globally. And it might not be the right one for each audience.

An Ahrefs study found that only 19% of multilingual sites implement hreflang correctly. The remaining 81% have errors ranging from missing return tags to broken URLs. It's one of the most commonly misconfigured technical SEO elements.

## Why Does Hreflang Matter?

Getting hreflang right directly impacts whether the correct audience sees the correct page.

- **Correct language serving**. Users in France see the French version, users in Germany see the German version, without manual redirecting
- **Prevents duplicate content filtering**. Google understands that your /en/ and /de/ pages aren't duplicates but intentional translations
- **Better user experience**. Visitors landing on a page in their native language are more likely to convert and less likely to bounce
- **Regional pricing and content**. Ecommerce sites serving different prices or products by region need hreflang to ensure the right version appears in each market

Any business operating in multiple countries or languages needs hreflang. Period.

## How Hreflang Works

### Implementation Methods

You can implement hreflang three ways: HTML link tags in the `<head>`, HTTP headers (for PDFs and non-HTML files), or in your [XML sitemap](/glossary/xml-sitemap). Google recommends choosing one method and sticking with it. The sitemap approach works best for large sites with hundreds of language variants.

### The Return Tag Rule

Every hreflang annotation must be bidirectional. If page A says "my French equivalent is page B," then page B must also say "my English equivalent is page A." Missing return tags are the #1 implementation error. Google ignores hreflang annotations without proper return tags.

### The x-default Tag

The x-default hreflang value tells Google which page to show when no specific language/region match exists. It's your fallback. Typically your English or main-market version. Without x-default, Google guesses, and it doesn't always guess right.

## Hreflang Examples

**Example 1: An ecommerce store with US and UK versions**
An online retailer has `example.com/us/shoes` (prices in USD) and `example.com/uk/shoes` (prices in GBP). Without hreflang, Google might show UK users the US page. With proper hreflang tags, each audience sees the correct pricing and currency. The [canonical URL](/glossary/canonical-url) stays independent for each version.

**Example 2: A SaaS company with translated pages**
A project management tool has their homepage in 8 languages. They implement hreflang via XML sitemap, with each language version pointing to every other. German searchers see the /de/ page, Spanish searchers see /es/, and everyone else hits the x-default English version.
## Frequently Asked Questions

### Does hreflang affect rankings?

Hreflang doesn't boost rankings directly. It tells Google which version to show in which market. But showing the right language to the right audience improves engagement signals (lower bounce rate, higher [dwell time](/glossary/dwell-time)) that can indirectly influence rankings over time.

### Can I use hreflang for the same language in different countries?

Yes. That's exactly what hreflang handles well. English for the US (en-us), English for the UK (en-gb), and English for Australia (en-au) can all have separate hreflang annotations. Google uses the country code, not just the language, to determine which version to serve.

### What happens if hreflang is implemented incorrectly?

Google ignores the annotations entirely and falls back to its own judgment about which version to show. No penalty. Just lost control over which page appears in each market. Use Google Search Console's International Targeting report to identify hreflang errors.

---

Want your site's content optimized for search from day one? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Hreflang Implementation](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Ahrefs: Hreflang Tags Guide](https://ahrefs.com/blog/hreflang-tags/)
- [Moz: The Ultimate Guide to Hreflang](https://moz.com/learn/seo/hreflang-tag)
