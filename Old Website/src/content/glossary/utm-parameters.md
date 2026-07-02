---
term: "UTM Parameters"
slug: "utm-parameters"
definition: "UTM parameters are short text tags appended to a URL that tell analytics platforms exactly where a visitor came from, which campaign brought them, and."
category: "Marketing"
difficulty: "Beginner"
keyword: "what is utm parameters"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "google-analytics"
  - "attribution"
  - "conversion-rate"
  - "campaign"
  - "organic-traffic"
---

## What are UTM Parameters?

**UTM parameters (Urchin Tracking Module parameters) are query string tags added to the end of a URL that pass campaign tracking data to [Google Analytics](/glossary/google-analytics) and other analytics platforms, letting you see exactly which link, channel, and campaign drove each visitor.**

The name comes from Urchin Software, the company Google acquired in 2005 that became Google Analytics. The tracking format stuck. Today, UTMs are the universal standard for campaign attribution across every major analytics tool. Not just Google's.

Here's why they matter in practice: without UTMs, a link shared in your email newsletter, a LinkedIn post, and a partner's blog all show up as generic referral or direct traffic. With UTMs, each one gets its own trackable identity. A 2023 HubSpot survey found that 72% of marketers who track campaign ROI rely on UTM parameters as their primary attribution method.

## Why Do UTM Parameters Matter?

Marketing without UTMs is like running 5 ad campaigns with the same phone number. You know calls are coming in, but you can't tell which campaign is working.

- **Channel attribution becomes precise**. Instead of "social media drove 500 visits," you see "the LinkedIn carousel post about pricing drove 287 visits, and the X thread drove 213." That changes how you allocate budget
- **Campaign comparison gets real**. Running a spring sale and a webinar promotion simultaneously? UTMs let you compare performance side-by-side in [Google Analytics](/glossary/google-analytics) without guessing
- **Content performance is measurable**. The same link to your pricing page can be tagged differently in your email header vs. footer. Now you know which placement converts better
- **[ROI](/glossary/return-on-investment) calculations have real inputs**. You can't calculate return on a campaign if you can't isolate the traffic and conversions it generated. UTMs make that isolation possible

Any marketer running campaigns across more than one channel needs UTMs. Period.

## How UTM Parameters Work

UTMs work by appending key-value pairs to the end of a URL after a `?` character. When a user clicks the tagged link, the parameters ride along in the URL, and your analytics platform reads them.

### The Five UTM Parameters

There are 5 standard UTM tags. Three are required by Google Analytics; two are optional.

| Parameter | Purpose | Example | Required? |
|---|---|---|---|
| `utm_source` | Where the traffic comes from | `google`, `newsletter`, `linkedin` | Yes |
| `utm_medium` | The marketing channel type | `cpc`, `email`, `social`, `referral` | Yes |
| `utm_campaign` | The specific campaign name | `spring-sale-2026`, `webinar-may` | Yes |
| `utm_term` | The paid keyword (for search ads) | `seo+agency`, `crm+software` | No |
| `utm_content` | Differentiates similar links | `header-cta`, `sidebar-banner` | No |

### How a Tagged URL Looks

A base URL like `https://example.com/pricing` becomes:

`https://example.com/pricing?utm_source=linkedin&utm_medium=social&utm_campaign=spring-sale-2026&utm_content=carousel-post`

When someone clicks this, [Google Analytics](/glossary/google-analytics) records the visit with all four parameters, making it filterable in your Acquisition reports.

### Naming Conventions

This is where most teams get sloppy. "LinkedIn" vs. "linkedin" vs. "LI" vs. "linked-in" creates 4 separate entries in your analytics. Pick a convention. Lowercase, hyphens, no spaces. And document it. Consistency is more important than the convention itself.

## Types of UTM Use Cases

UTMs apply across every marketing channel, but the tagging strategy differs:

- **Email campaigns**. Tag every link in every email. Use `utm_content` to distinguish header links from footer links or different CTAs within the same email. Source: `newsletter` or your ESP name
- **Social media posts**. Tag links in organic and paid social posts separately. Use `utm_medium=social` for organic and `utm_medium=paid-social` for promoted posts
- **Paid search and display**. Google Ads auto-tags with `gclid`, but UTMs give you a backup and work across non-Google analytics tools. Essential for [Bing Ads](/glossary/bing-webmaster-tools) and other platforms
- **Partner and affiliate links**. Give each partner a unique `utm_source` so you can track referral performance per partner without relying on their reporting
- **QR codes and offline campaigns**. QR codes linking to UTM-tagged URLs let you track offline-to-online conversions from print ads, flyers, and event signage

## UTM Parameter Examples

**Example 1: A dental practice tracking new patient sources**
A dentist runs a Google Ads campaign, posts weekly on Facebook, and sends a monthly email newsletter. All linking to their "Book Appointment" page. Each channel gets unique UTMs. After 90 days, GA4 shows email drives the most bookings (38%), Facebook drives the most traffic but fewest bookings (8% [conversion rate](/glossary/conversion-rate)), and Google Ads has the highest cost per booking. They shift budget from paid to email list growth.

**Example 2: A SaaS company A/B testing email CTAs**
A CRM startup sends the same product announcement email but tests two CTA buttons: "See What's New" vs. "Try It Free." Both link to the same page but use different `utm_content` values. GA4 shows "Try It Free" generates 2.3x more trial signups. They update their default CTA across all emails.

**Example 3: An e-commerce brand measuring influencer ROI**
A D2C pet food brand gives 8 influencers unique UTM-tagged links with each influencer's name as the `utm_source`. After the campaign, they can see exactly which influencer drove the most traffic and revenue. Not just engagement. And adjust future partnerships based on actual [conversion](/glossary/conversion) data rather than follower counts.

## UTM Parameters vs. Google Auto-Tagging

Google Ads users often wonder if they need UTMs when auto-tagging exists.

| | UTM Parameters | Google Auto-Tagging (gclid) |
|---|---|---|
| **Works with** | All analytics platforms | Google Analytics only |
| **Setup** | Manual (you build the URL) | Automatic (enabled in Google Ads) |
| **Customization** | Full control over naming | Fixed by Google's taxonomy |
| **Non-Google channels** | Required (email, social, partners) | Not applicable |
| **Recommended** | For every non-Google link | For Google Ads alongside UTMs as backup |

Use auto-tagging for Google Ads. Use UTMs for everything else. Some teams use both on Google Ads for redundancy and cross-platform reporting.

## UTM Parameter Best Practices

- **Create a naming convention document**. Write down your exact taxonomy for source, medium, and campaign naming. Share it with everyone who creates links. Inconsistent naming is the #1 reason UTM data becomes useless
- **Use a URL builder tool**. Google's free Campaign URL Builder prevents typos and enforces format. For teams, use a shared spreadsheet or tools like UTM.io that standardize and log every tagged URL
- **Never use UTMs on internal links**. Tagging internal site navigation with UTMs overwrites the original traffic source in GA4. A visitor who arrived from organic search gets re-attributed to "internal-banner" when they click a UTM-tagged internal link. Bad data
- **Keep campaign names short and descriptive** ,  `spring-sale-2026` beats `our-amazing-spring-sale-promotion-for-new-customers-v2`. The name needs to be recognizable in a report, not clever
- **Review your UTM data monthly**. Check GA4's Traffic Acquisition report filtered by campaign. If you see duplicates, misspellings, or mystery campaign names, fix the process. theStacc's automated blog publishing pairs well with UTM tracking. Tag your social shares and email links promoting those articles to see exactly which distribution channels drive the most [organic traffic](/glossary/organic-traffic)

## Frequently Asked Questions

### Do UTM parameters affect SEO?

UTM parameters don't affect your search rankings. Google ignores UTM query strings during indexing. That said, UTM-tagged links shared publicly can create messy-looking URLs. Use them on links you control (emails, ads, social) rather than links meant for organic sharing.

### How many UTM parameters should I use?

Three are required by Google Analytics: source, medium, and campaign. Use content and term when you need additional differentiation. Like testing two CTAs in one email or tracking individual paid keywords. Don't over-tag. More parameters means more room for inconsistency.

### Can UTM parameters break my website?

UTM parameters won't break site functionality. They're appended after the `?` in the URL and are ignored by your web server. The only risk is aesthetic. Long parameter strings look cluttered in browser address bars and when shared.

### What happens if I spell a UTM parameter wrong?

Misspelled parameters create new, separate entries in analytics. "linkedIn" and "linkedin" show up as two different sources. There's no way to merge them retroactively in GA4. Consistent naming from the start prevents this.

---

Want the blog content those UTM links point to? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google: Collect Campaign Data with Custom URLs](https://support.google.com/analytics/answer/1033863)
- [Google: Campaign URL Builder Tool](https://ga-dev-tools.google/ga4/campaign-url-builder/)
- [HubSpot: The Ultimate Guide to UTM Parameters](https://blog.hubspot.com/marketing/what-are-utm-tracking-codes)
- [Moz: UTM Parameters and Tracking Best Practices](https://moz.com/blog/utm-parameters)
