---
term: "Open Graph Tags"
slug: "open-graph-tags"
definition: "Open Graph tags are HTML meta tags that control how a URL appears when shared on social media platforms like Facebook, LinkedIn, and Twitter. Defining."
category: "SEO"
difficulty: "Beginner"
keyword: "what is open graph tags"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "meta-description"
  - "title-tag"
  - "social-media-marketing"
  - "on-page-seo"
  - "schema-markup"
---

## What are Open Graph Tags?

Open Graph (OG) tags are snippets of HTML code that tell social media platforms exactly what title, description, and image to display when someone shares a link to your page.

Facebook created the Open Graph protocol in 2010, and it's now used by LinkedIn, Twitter (which also supports its own Twitter Card tags), Pinterest, and most messaging apps. Without OG tags, these platforms guess what to show. Often pulling the wrong image, a truncated title, or a meaningless snippet of text.

According to Hootsuite data, social media posts with proper images get 2.3x more engagement than those without. OG tags are how you control that image. They don't directly impact [SEO](/glossary/seo) rankings, but they drive social clicks, which drive traffic, which can indirectly influence search performance.

## Why Do Open Graph Tags Matter?

Every shared link is a mini-advertisement for your content. OG tags determine whether it looks professional or broken.

- **Control your appearance**. Without OG tags, Facebook might pull your footer logo or a random sidebar image as the preview
- **Increase click-through rates**. A compelling title and image in the preview dramatically outperform auto-generated ones
- **Brand consistency**. Ensure every shared link reinforces your brand with the right imagery and messaging
- **Prevent sharing friction**. When your links look broken or confusing, people share them less

For any business publishing blog content, OG tags are a 5-minute setup that pays dividends every time someone shares your pages.

## How Open Graph Tags Work

### Core Tags

Four OG tags handle the essentials. `og:title` sets the headline. `og:description` sets the preview text (keep it under 200 characters). `og:image` defines the preview image (recommended size: 1200x630 pixels). `og:url` specifies the canonical URL for the shared page.

### Implementation

Add OG tags in the `<head>` section of your HTML. Most CMS platforms. WordPress, Webflow, Ghost. Have built-in fields or plugins for setting these without touching code. If you're using a static site generator, add them to your page template.

### Platform-Specific Behavior

Facebook and LinkedIn read standard OG tags. Twitter uses its own `twitter:card` tags but falls back to OG tags if those aren't present. Always set both for maximum coverage. Use Facebook's Sharing Debugger and Twitter's Card Validator to preview how your links will appear before publishing.

## Open Graph Tags Examples

**A local bakery** starts sharing blog posts about seasonal recipes on Facebook. Without OG tags, the preview shows a tiny logo and no description. After adding proper OG tags with appetizing food photos at 1200x630px, their social post engagement jumps 180% and website traffic from Facebook doubles.

**A SaaS company** publishing 30 blog posts per month through theStacc adds OG tags to every article template. Each post gets a custom preview title, description, and branded feature image. When their sales team shares articles on LinkedIn, the previews look polished and professional. Driving 3x more clicks than their competitors' plain-text link shares.
### Tools and Resources

| Tool | Purpose | Price |
|---|---|---|
| **[Google Search Console](/glossary/google-search-console)** | Search performance data | Free |
| **Ahrefs** | Backlinks, keywords, site audit | From $99/month |
| **Semrush** | All-in-one SEO platform | From $130/month |
| **Screaming Frog** | Technical crawl analysis | Free (500 URLs) |
| **theStacc** | Automated SEO content publishing | From $99/month |

## Frequently Asked Questions

### Do Open Graph tags affect SEO rankings?

Not directly. Google doesn't use OG tags as a ranking factor. But well-optimized OG tags increase social sharing and click-through rates, which drive traffic and brand signals that can indirectly benefit your [organic search](/glossary/organic-search) performance.

### What size should OG images be?

Use 1200x630 pixels for the best display across platforms. Facebook, LinkedIn, and Twitter all handle this size well. Images should be under 8MB. Use JPG or PNG format. Avoid SVGs.

### How do I test my Open Graph tags?

Use Facebook's Sharing Debugger (developers.facebook.com/tools/debug/) to preview and clear cached versions. Twitter's Card Validator shows Twitter-specific previews. LinkedIn's Post Inspector handles LinkedIn previews.

---

Want content that looks great everywhere it's shared? theStacc publishes 30 SEO-optimized articles to your site every month. Ready for social. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Open Graph Protocol Official Documentation](https://ogp.me/)
- [Facebook: Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter: Cards Documentation](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards)
- [Hootsuite: Social Media Image Sizes](https://blog.hootsuite.com/social-media-image-sizes-guide/)
