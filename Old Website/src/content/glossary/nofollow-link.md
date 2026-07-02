---
term: "Nofollow Link"
slug: "nofollow-link"
definition: "A nofollow link includes an HTML attribute (rel='nofollow') that signals search engines not to pass link equity to the linked page. It's used for paid."
category: "SEO"
difficulty: "Beginner"
keyword: "what is a nofollow link"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "link-equity"
  - "backlinks"
  - "dofollow-link"
  - "link-building"
  - "meta-robots-tag"
---

## What is a Nofollow Link?

A nofollow link is a hyperlink with a `rel="nofollow"` attribute that tells search engines not to pass [link equity](/glossary/link-equity) or ranking signals from the linking page to the destination page.

Google introduced the nofollow attribute in 2005 to combat comment spam. Blog owners were drowning in automated comments stuffed with links, all trying to manipulate rankings. Nofollow gave webmasters a way to link to pages without vouching for them.

In 2019, Google changed how it treats nofollow. It's now a "hint" rather than a strict directive. Google may choose to consider nofollow links for crawling and indexing purposes. They also introduced two new attributes: `rel="sponsored"` for paid links and `rel="ugc"` for user-generated content. Ahrefs reports that approximately 43% of all [backlinks](/glossary/backlinks) across the web are nofollow.

## Why Does Nofollow Link Matter?

Understanding nofollow links affects both your link building strategy and how you manage outbound links.

- **Paid link compliance**. Google requires nofollow (or sponsored) on all paid and affiliate links. Failing to tag them risks a [Google penalty](/glossary/google-penalty)
- **Link profile diversity**. A natural backlink profile contains a mix of dofollow and nofollow links. An all-dofollow profile looks suspicious
- **Traffic value**. Nofollow links from high-traffic sites still send referral visitors, even if they pass minimal SEO value
- **User-generated content protection**. Adding nofollow to blog comments, forum posts, and user reviews prevents your site from endorsing spam links

If you're running [link building](/glossary/link-building) campaigns, knowing which links are nofollow helps you measure actual SEO impact.

## How Nofollow Link Works

### The HTML Implementation

A standard dofollow link: `<a href="https://example.com">Example</a>`. A nofollow link: `<a href="https://example.com" rel="nofollow">Example</a>`. The rel attribute is the only difference. CMS platforms like WordPress automatically add nofollow to comment links by default.

### The 2019 Changes

Google now treats nofollow as a hint for ranking, crawling, and indexing. They may still follow and credit nofollow links if they find them useful. The rel="sponsored" attribute specifically identifies paid links. The rel="ugc" attribute marks user-generated content. You can combine them: `rel="nofollow ugc"`.

### Nofollow vs. Dofollow

[Dofollow links](/glossary/dofollow-link) (which are just normal links without any nofollow attribute) pass full link equity. They're what you want from link building. But nofollow links still have value. They diversify your link profile, send referral traffic, and may pass some ranking signal under Google's hint-based system.

## Nofollow Link Examples

**Example 1: A press mention on a major news site**
A SaaS company gets featured in Forbes. The link back to their site is nofollow (most major publishers default to nofollow for external links). Despite being nofollow, the article sends 2,000 referral visitors in the first week and builds brand awareness that leads to natural dofollow links from smaller sites.

**Example 2: Affiliate link compliance**
A review blog earns commissions from Amazon affiliate links. They add `rel="sponsored nofollow"` to every affiliate link. Google sees these as properly disclosed paid links. No penalty risk. The blog maintains a clean link profile while earning revenue.
## Frequently Asked Questions

### Do nofollow links help SEO at all?

They help indirectly. Nofollow links drive referral traffic, increase brand visibility, and create a natural-looking link profile. Since Google's 2019 update treats nofollow as a hint, some SEO value may pass through. Don't ignore nofollow links. They're less valuable than dofollow but far from worthless.

### Should I nofollow all outbound links?

No. Only nofollow links to untrusted content, paid/affiliate links, and user-generated content. Linking out to authoritative sources with dofollow signals to Google that your content references quality information. Over-nofollowing looks paranoid and removes your ability to participate in the web's natural linking ecosystem.

### How do I check if a link is nofollow?

Right-click the link, select "Inspect" (or view page source), and look for `rel="nofollow"` in the HTML. Browser extensions like Nofollow and MozBar highlight nofollow links visually. For bulk analysis, Ahrefs and Semrush show the nofollow status of every backlink in your profile.

---

Want to earn quality backlinks naturally through great content? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Link Spam Policies](https://developers.google.com/search/docs/essentials/spam-policies)
- [Google Blog: Evolving Nofollow](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify)
- [Ahrefs: Nofollow Links Guide](https://ahrefs.com/blog/nofollow-links/)
- [Moz: What is a Nofollow Link](https://moz.com/learn/seo/nofollow)
