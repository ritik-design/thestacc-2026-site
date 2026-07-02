---
term: "JSON-LD"
slug: "json-ld"
definition: "JSON-LD (JavaScript Object Notation for Linked Data) is a structured data format that helps search engines understand page content. Google recommends."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is json ld"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "schema-markup"
  - "rich-results"
  - "knowledge-graph"
  - "local-schema-markup"
  - "serp-features"
---

## What is JSON-LD?

JSON-LD is a script-based method of embedding structured data into web pages using JavaScript Object Notation, making your content machine-readable for search engines and AI systems.

Google has explicitly stated JSON-LD is their "recommended format" for [schema markup](/glossary/schema-markup). Unlike older formats (Microdata and RDFa) that require weaving code into your HTML, JSON-LD sits in a clean `<script>` block in the page header. It doesn't touch your visible content.

A Search Engine Journal analysis found that pages with JSON-LD structured data are 35% more likely to appear in [rich results](/glossary/rich-results) than pages without it. Google uses this data to generate star ratings, FAQ dropdowns, recipe cards, event listings, and other enhanced SERP features.

## Why Does JSON-LD Matter?

JSON-LD bridges the gap between human-readable content and what machines can parse.

- **Rich results eligibility**. FAQ snippets, how-to steps, product ratings, and review stars all require structured data, and JSON-LD is the cleanest way to implement them
- **[Knowledge Graph](/glossary/knowledge-graph) inclusion**. Structured data helps Google connect your content to entities in the Knowledge Graph, increasing visibility
- **AI visibility**. Large language models and AI systems parse JSON-LD to understand and cite your content, making it a key [GEO](/glossary/generative-engine-optimization) signal
- **Easy implementation**. JSON-LD doesn't require modifying page HTML, making it simpler to add, maintain, and debug than inline markup formats

For local businesses, JSON-LD is how you communicate your address, hours, and services to Google.

## How JSON-LD Works

### The Script Block

JSON-LD lives inside a `<script type="application/ld+json">` tag, usually in the page `<head>`. It contains a structured object with properties like @type, name, description, and other schema.org vocabulary. Google's crawler reads this block separately from the visible page content.

### Common Schema Types

The most used JSON-LD types include Article, LocalBusiness, Product, FAQPage, HowTo, BreadcrumbList, and Organization. Each type has required and recommended properties. Google's [Rich Results Test](https://search.google.com/test/rich-results) validates whether your markup is correctly formatted.

### Relationship to Schema.org

JSON-LD is the *format*. Schema.org is the *vocabulary*. Schema.org defines the property names and types (like "name," "address," "aggregateRating"). JSON-LD is how you write those properties into your page. They work together. You can't have useful JSON-LD without schema.org vocabulary.

## JSON-LD Examples

**Example 1: A local dental practice**
A dentist adds [LocalBusiness JSON-LD](/glossary/local-schema-markup) with their name, address, phone, hours, and aggregate rating. Google now shows their star rating and hours directly in search results. Click-through rate increases 22% because the listing stands out from competitors without structured data.

**Example 2: A blog post with FAQ markup**
A marketing agency adds FAQPage JSON-LD to their guide on "email marketing best practices." Three FAQ items now appear as expandable dropdowns directly in Google's search results, giving the page 3x more SERP real estate than a standard listing.
### Tools and Resources

| Tool | Purpose | Price |
|---|---|---|
| **[Google Search Console](/glossary/google-search-console)** | Search performance data | Free |
| **Ahrefs** | Backlinks, keywords, site audit | From $99/month |
| **Semrush** | All-in-one SEO platform | From $130/month |
| **Screaming Frog** | Technical crawl analysis | Free (500 URLs) |
| **theStacc** | Automated SEO content publishing | From $99/month |

## Frequently Asked Questions

### Is JSON-LD better than Microdata?

For most use cases, yes. Google recommends JSON-LD because it's easier to implement, maintain, and debug. Microdata requires inline annotations throughout your HTML. JSON-LD keeps structured data in one clean block that doesn't affect page rendering. Use JSON-LD unless you have a specific technical reason not to.

### Does JSON-LD directly improve rankings?

JSON-LD doesn't boost rankings directly. But it enables [rich results](/glossary/rich-results) that significantly increase click-through rates, and higher CTR sends positive engagement signals to Google. Think of it as a visibility amplifier rather than a ranking factor.

### How do I validate my JSON-LD?

Use Google's Rich Results Test (search.google.com/test/rich-results) or Schema Markup Validator (validator.schema.org). Both check syntax errors, missing required fields, and whether your markup qualifies for specific rich result types. Test before deploying to production.

---

Want your content structured for maximum search visibility? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Structured Data Overview](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Schema.org: Getting Started](https://schema.org/docs/gs.html)
- [Google: Rich Results Test](https://search.google.com/test/rich-results)
- [Search Engine Journal: JSON-LD for SEO](https://www.searchenginejournal.com/json-ld-for-seo/440577/)
