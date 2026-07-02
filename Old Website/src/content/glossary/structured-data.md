---
term: "Structured Data"
slug: "structured-data"
definition: "Structured data is standardized code added to web pages to help search engines understand the content and context, enabling rich results like ratings, prices, and event details in search listings."
category: "SEO"
difficulty: "Beginner"
keyword: "what is structured data"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "schema-markup"
  - "rich-snippets"
  - "json-ld"
  - "google-search-console"
  - "knowledge-graph"
---

## What Is Structured Data?

Structured data is a standardized format for providing information about a web page and its content. It uses specific vocabulary — primarily Schema.org — to label content so search engines can understand not just what the words say, but what they mean.

Without structured data, Google sees a page with text, images, and links. With structured data, Google understands that a specific string of text is a product price, that a date is an event start time, or that a name is the author of an article.

**The most common format is JSON-LD** (JavaScript Object Notation for Linked Data), which Google recommends. It is added as a script tag in the page's HTML head or body.

**Example JSON-LD for an article:**

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "What Is Structured Data?",
  "author": {
    "@type": "Person",
    "name": "Jane Smith"
  },
  "datePublished": "2026-06-08"
}
```

## Why Structured Data Matters

### Rich Results in Search

Structured data enables rich results — enhanced search listings that include additional visual elements and information:

| Rich Result Type | What Appears | Schema Type |
|---|---|---|
| Star ratings | Review stars and count | AggregateRating |
| Product prices | Price and availability | Product |
| Recipe cards | Image, cook time, calories | Recipe |
| Event listings | Date, time, location | Event |
| FAQ dropdowns | Expandable Q&A | FAQPage |
| How-to steps | Numbered instructions | HowTo |
| Breadcrumb navigation | Category path | BreadcrumbList |
| Video thumbnails | Play button and duration | VideoObject |
| Local business info | Address, hours, phone | LocalBusiness |

**Key statistic:** Pages with rich results see 20-30% higher click-through rates than standard listings (Search Engine Journal).

### Knowledge Graph Inclusion

Structured data helps Google identify entities (people, places, organizations, things) and add them to the Knowledge Graph. This can trigger Knowledge Panels — the information boxes that appear on the right side of search results for notable entities.

### Voice Search Optimization

Voice assistants like Google Assistant rely heavily on structured data to provide direct answers. A page with clear FAQ schema is more likely to be read aloud as a voice search answer.

### Machine-Readable Context

As AI-powered search evolves, structured data becomes even more important. Google's AI systems use structured data to understand page context, extract facts, and generate AI Overview citations.

## Common Schema Types

### Content Schemas

| Schema | Use For | Key Properties |
|---|---|---|
| Article / BlogPosting | Blog posts, news articles | headline, author, datePublished, image |
| FAQPage | FAQ sections | mainEntity (question + acceptedAnswer) |
| HowTo | Step-by-step guides | step, tool, supply, totalTime |
| Recipe | Cooking recipes | recipeIngredient, recipeInstructions, cookTime |
| VideoObject | Embedded videos | name, description, thumbnailUrl, uploadDate |

### Business Schemas

| Schema | Use For | Key Properties |
|---|---|---|
| LocalBusiness | Local businesses | name, address, telephone, openingHours |
| Organization | Companies and orgs | name, logo, url, sameAs (social profiles) |
| Person | Individual profiles | name, jobTitle, worksFor, alumniOf |

### E-commerce Schemas

| Schema | Use For | Key Properties |
|---|---|---|
| Product | Product pages | name, image, offers (price, availability), brand |
| AggregateRating | Review summaries | ratingValue, reviewCount |
| Review | Individual reviews | author, reviewRating, reviewBody |
| Offer | Pricing details | price, priceCurrency, availability |

### Navigation Schemas

| Schema | Use For | Key Properties |
|---|---|---|
| BreadcrumbList | Breadcrumb navigation | itemListElement (position, name, item) |
| WebSite | Site search | url, potentialAction (search action) |
| SiteNavigationElement | Navigation menus | name, url |

## How to Implement Structured Data

### Method 1: JSON-LD (Recommended)

Add a script tag to your page's HTML:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Smith Plumbing",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "Austin",
    "addressRegion": "TX",
    "postalCode": "78701"
  },
  "telephone": "(555) 123-4567"
}
</script>
```

**Pros:** Easy to implement, keeps markup separate from content, Google-recommended

### Method 2: Microdata

Embed schema attributes directly in HTML tags:

```html
<div itemscope itemtype="https://schema.org/LocalBusiness">
  <span itemprop="name">Smith Plumbing</span>
  <div itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
    <span itemprop="streetAddress">123 Main St</span>
  </div>
</div>
```

**Pros:** Tightly coupled with visible content
**Cons:** Harder to maintain, clutters HTML

### Method 3: RDFa

Similar to microdata but using different attribute syntax. Less commonly used for SEO purposes.

## Structured Data Testing Tools

| Tool | Purpose | URL |
|---|---|---|
| Google's Rich Results Test | Test specific schema types | search.google.com/test/rich-results |
| Schema Markup Validator | General schema validation | validator.schema.org |
| Google Search Console | Monitor structured data issues | search.google.com/search-console |
| Merkle's Schema Markup Generator | Generate schema code | technicalseo.com/tools/schema-markup-generator |

## Common Structured Data Mistakes

**Mistake 1: Adding schema for content not on the page.**

Google considers this spam. If you add Product schema, the product details must be visible to users on the page.

**Mistake 2: Inaccurate or misleading data.**

Fake reviews, incorrect prices, or wrong dates in schema can trigger manual penalties.

**Mistake 3: Conflicting schema types.**

Using multiple schema types that contradict each other confuses search engines.

**Mistake 4: Missing required properties.**

Each schema type has required properties. Missing these prevents rich results from appearing.

**Mistake 5: Implementing schema but not requesting indexing.**

After adding structured data, submit the URL for indexing in Google Search Console or wait for Google to recrawl.

## Related Terms

- [Schema Markup](/glossary/schema-markup/)
- [Rich Snippets](/glossary/rich-snippets/)
- [JSON-LD](/glossary/json-ld/)
- [Google Search Console](/glossary/google-search-console/)
- [Knowledge Graph](/glossary/knowledge-graph/)
