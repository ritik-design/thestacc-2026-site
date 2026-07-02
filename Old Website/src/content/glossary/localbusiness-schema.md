---
term: "LocalBusiness Schema"
slug: "localbusiness-schema"
definition: "LocalBusiness schema is structured data markup from Schema.org that you add to your website's code to explicitly tell search engines your business name."
category: "Local SEO"
difficulty: "Intermediate"
keyword: "what is localbusiness schema"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "schema-markup"
  - "local-seo"
  - "json-ld"
  - "rich-results"
  - "nap"
---

## What is LocalBusiness Schema?

LocalBusiness schema is a specific type of [structured data markup](/glossary/schema-markup) from Schema.org that encodes your business's essential details. Name, address, phone, hours, geo-coordinates. Into a format search engines can read directly.

It lives in your website's HTML (usually as a [JSON-LD](/glossary/json-ld) script in the `<head>`) and acts like a business card for machines. When Google, Bing, or an AI model crawls your page, this markup removes all guesswork about who you are, where you're located, and what you do.

Why bother? Milestone Research found that websites with schema markup rank an average of 4 positions higher in search results. For local businesses specifically, schema helps Google connect your website to your [Google Business Profile](/glossary/google-business-profile). Reinforcing the [NAP](/glossary/nap) signals that drive [Map Pack](/glossary/map-pack) rankings.

## Why Does LocalBusiness Schema Matter?

Schema doesn't directly boost rankings. Google has said that. But it gives Google clearer signals about your business, which indirectly improves how you rank and appear in search.

- **Entity confirmation**. Schema ties your website, GBP listing, and directory citations together as one [entity](/glossary/entity). Google's Knowledge Graph uses this to build confidence in your business data.
- **[Rich results](/glossary/rich-results) eligibility**. Proper schema can trigger enhanced search results showing your star rating, hours, price range, and address directly in the SERP
- **AI visibility**. Large language models and [AI Overviews](/glossary/ai-overviews) extract structured data to answer questions about local businesses. Without schema, your data might not get cited.
- **Reduced NAP ambiguity**. If your address format varies slightly across directories, schema on your website establishes the canonical version that Google should trust

For [local SEO](/glossary/local-seo), LocalBusiness schema is the foundation that holds all your other optimization work together.

## How LocalBusiness Schema Works

### The Markup Format

Google recommends JSON-LD (JavaScript Object Notation for Linked Data) as the preferred format for schema. You place a `<script type="application/ld+json">` block in your page's HTML. Usually in the `<head>` or right before the closing `</body>` tag.

A basic LocalBusiness markup includes: `@type`, `name`, `address` (with `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`), `telephone`, `openingHoursSpecification`, and `geo` (latitude/longitude).

### How Search Engines Process It

When Googlebot crawls your page, it extracts the JSON-LD block and parses it against the Schema.org vocabulary. Google validates the markup, checks it against your [Google Business Profile](/glossary/google-business-profile) data, and uses it to reinforce or correct its understanding of your business.

Mismatches between your schema and your GBP data can actually hurt. If your schema says "123 Main St" but your GBP says "123 Main Street," Google has to decide which is correct. Consistency wins.

### Validation and Testing

Use Google's Rich Results Test or Schema Markup Validator to check your markup before deploying. Common errors include missing required fields, incorrect data types (putting a string where Google expects a number), and nesting errors in the JSON structure.

## Types of LocalBusiness Schema

Schema.org defines LocalBusiness as a parent type with dozens of specific subtypes. Using the most specific type gives Google better context.

- **Dentist**. For dental practices. Inherits from MedicalBusiness > LocalBusiness.
- **Attorney**. For law firms and solo practitioners. Falls under LegalService > LocalBusiness.
- **Plumber**. Under HomeAndConstructionBusiness. Also includes Electrician, HVACBusiness, and RoofingContractor.
- **Restaurant**. Under FoodEstablishment. Has subtypes like FastFoodRestaurant, BarOrPub, and CafeOrCoffeeShop.
- **AutoRepair**. Under AutomotiveBusiness. Also covers AutoDealer, GasStation, and MotorcycleRepair.

Always use the most specific subtype available. "Dentist" tells Google more than "LocalBusiness." Check Schema.org's full hierarchy before picking.

## LocalBusiness Schema Examples

**Example 1: A plumbing company**
A plumbing business in Austin adds JSON-LD to their homepage with `@type: "Plumber"`, full address, phone, 24/7 hours, service area, and a link to their GBP profile. Within weeks, their search listing starts showing hours and a star rating snippet. Increasing click-through rate by 25%.

**Example 2: A multi-location restaurant**
A taco chain with 5 locations creates separate [location pages](/glossary/location-pages) on their website, each with unique LocalBusiness schema. Each page has its own `@type: "Restaurant"`, unique address, individual hours, and location-specific [Google Reviews](/glossary/google-reviews) rating. Google associates each page with the correct GBP listing.

**Example 3: A service area business with no storefront**
A mobile locksmith doesn't have a physical address customers visit. Instead of using `address`, they use `areaServed` with a list of cities and zip codes. This signals their service area without exposing a home address. Matching their [service area business](/glossary/service-area-business) setup in GBP.

## LocalBusiness Schema vs. Organization Schema

These two get confused a lot. Both are Schema.org types, but they serve different purposes.

| | LocalBusiness Schema | Organization Schema |
|---|---|---|
| **Best for** | Businesses serving a local area | Companies without a specific local focus |
| **Includes address** | Yes. Physical address required (or areaServed) | Optional |
| **Includes hours** | Yes. OpeningHoursSpecification | No |
| **Includes geo-coordinates** | Yes. Latitude and longitude | No |
| **Rich result triggers** | Local business panels, hours, ratings | Knowledge panels, logo, social links |
| **Use when** | You want to rank in local search | You want brand-level search presence |

If you're a local business, use LocalBusiness (or a subtype). Organization schema is for non-local entities like software companies or media brands.

## LocalBusiness Schema Best Practices

- **Match your schema NAP exactly to your GBP**. Same abbreviations, same formatting, same phone number format. "St" vs "Street" matters. Consistency builds entity confidence.
- **Use the most specific @type**. Don't default to "LocalBusiness" when "Dentist" or "Plumber" exists. Specific types give Google stronger context and may unlock type-specific [rich results](/glossary/rich-results).
- **Add geo-coordinates**. Latitude and longitude aren't technically required, but they remove location ambiguity. Use Google Maps to get exact coordinates for your address.
- **Include openingHoursSpecification**. This field powers the "Open now" and "Closes at 6 PM" displays in search results. Format it correctly using dayOfWeek arrays and opens/closes times.
- **Pair schema with local content**. Schema tells Google what your business is. [Local SEO content](/glossary/local-seo) tells Google what your business knows. theStacc publishes 30 articles/month targeting the keywords that complement your schema signals.

## Frequently Asked Questions

### Does LocalBusiness schema improve rankings?

Not directly. Google has confirmed schema isn't a ranking factor. But it improves entity clarity, enables rich results, and helps Google connect your website to your GBP. All of which indirectly support better [local rankings](/glossary/local-ranking-factors).

### Where should I place LocalBusiness schema?

Add it to your homepage and every [location page](/glossary/location-pages). Use JSON-LD format in the `<head>` section. Don't place the same schema on every page of your site. That's redundant and can confuse crawlers.

### Can I have multiple schema types on one page?

Yes. A page can include both LocalBusiness schema and other types like FAQPage, Service, or Product. Just make sure each is a separate, valid JSON-LD block.

### Do I need a plugin to add schema?

No. You can add JSON-LD manually to your HTML. WordPress users can use plugins like Rank Math or Yoast SEO to generate it automatically. Either approach works. The output matters more than the method.

---

Want your local SEO content to match the signals your schema sends? theStacc publishes 30 SEO articles/month to your website. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Schema.org: LocalBusiness Type](https://schema.org/LocalBusiness)
- [Google Search Central: Structured Data Guidelines](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Milestone Research: Schema Markup and Search Rankings Study](https://www.milestoneinternet.com/thought-leadership/schema-performance-study)
- [Moz: Local Business Schema for SEO](https://moz.com/learn/seo/schema-structured-data)
