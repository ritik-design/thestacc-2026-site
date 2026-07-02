---
term: "Google Analytics"
slug: "google-analytics"
definition: "Google Analytics is Google's free web analytics platform that tracks and reports website traffic, user behavior, and conversion data. Used by over 28."
category: "Marketing"
difficulty: "Beginner"
keyword: "what is google analytics"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "google-search-console"
  - "utm-parameters"
  - "conversion-rate"
  - "bounce-rate"
  - "organic-traffic"
---

## What is Google Analytics?

**Google Analytics (GA4) is a free measurement platform from Google that collects data about who visits your website, how they got there, what they do on it, and whether they complete the actions you care about.**

The platform transitioned from Universal Analytics to Google Analytics 4 (GA4) in July 2023. A complete rebuild, not just an update. GA4 uses an event-based data model instead of session-based tracking, which means every user interaction (page view, scroll, click, video play, purchase) is tracked as a discrete event. This was a massive shift for the 28+ million websites running GA, per BuiltWith data.

For any business with a website, Google Analytics is typically the first analytics tool installed and the last one removed. It's the baseline. Every conversation about [organic traffic](/glossary/organic-traffic), [conversion rates](/glossary/conversion-rate), and marketing ROI starts with GA data.

## Why Does Google Analytics Matter?

You can't improve what you don't measure. Google Analytics is how most businesses measure what happens on their website. And it's free.

- **Traffic source clarity**. GA shows exactly where visitors come from: [organic search](/glossary/organic-search), paid ads, social, email, direct, referral. Without this, you're guessing which channels actually work
- **Behavior insights**. Which pages do people visit most? Where do they drop off? How long do they stay? GA answers all of these, helping you fix leaks in your [conversion funnel](/glossary/conversion-funnel)
- **ROI measurement**. Connect Google Ads, track [conversion](/glossary/conversion) events, assign monetary values, and calculate actual return on ad spend. GA4's attribution modeling shows which touchpoints contribute to conversions
- **Free and deeply integrated**. GA4 connects natively to Google Ads, [Google Search Console](/glossary/google-search-console), BigQuery, and Looker Studio. No other free tool offers this integration depth

Whether you're a local plumber or a SaaS company, Google Analytics provides the foundation for data-driven decisions. The data is only useful if someone looks at it, though. That's where most small businesses fall short.

## How Google Analytics Works

GA4 tracks users through a JavaScript tracking snippet (or Google Tag Manager) installed on your website. Here's what happens behind the scenes.

### Data Collection

When a visitor loads your page, the GA4 tracking code fires and sends data to Google's servers. It records the page URL, timestamp, referral source, device type, browser, screen size, and geographic location. Every interaction after that. Scrolling, clicking a button, watching a video, completing a purchase. Gets recorded as an event.

### Event-Based Tracking

GA4's core architecture treats everything as an event. A page view is an event. A scroll past 90% of the page is an event. A file download, form submission, or e-commerce transaction. All events. Some are collected automatically. Others (like tracking a specific button click) require configuration through Google Tag Manager or the GA4 interface.

### Reporting and Analysis

GA4 organizes data into reports: Acquisition (how users arrive), Engagement (what they do), Monetization (revenue and conversions), and Retention (whether they come back). The Explorations section lets you build custom reports, funnels, and path analyses. For advanced users, the BigQuery export sends raw event data to Google's data warehouse for SQL-level analysis.

### Attribution

GA4 uses data-driven attribution by default. A machine learning model that distributes conversion credit across multiple touchpoints in the customer journey. This replaced the last-click model that Universal Analytics used, giving a more accurate picture of which marketing channels drive results.

## Types of Google Analytics Reports

GA4 organizes data into several core report categories:

- **Acquisition reports**. Show how users find your site. Breaks down traffic by channel (organic, paid, social, direct, referral), campaign, and source/medium. Connects to [UTM parameters](/glossary/utm-parameters) for campaign tracking
- **Engagement reports**. Track what users do after arriving. Pages viewed, events triggered, time engaged, scroll depth. The "Pages and Screens" report shows your most-visited content
- **Monetization reports**. E-commerce revenue, purchase journeys, product performance. Requires e-commerce event setup
- **Retention reports**. Show how many users return after their first visit, cohort analysis, and lifetime value estimates
- **Exploration reports**. Custom analyses you build yourself. Funnel explorations, path explorations, segment overlap, and free-form data tables

Most small businesses spend 80% of their time in Acquisition and Engagement reports.

## Google Analytics Examples

**Example 1: A local HVAC company tracking lead sources**
A 15-person HVAC company in Dallas installs GA4 and sets up a conversion event for their "Request a Quote" form. After 3 months, GA shows that 62% of form submissions come from organic search, 24% from Google Ads, and 14% from direct/referral. They reduce ad spend by 30% and redirect that budget toward [SEO](/glossary/seo) content. Where theStacc automatically publishes 30 articles per month targeting "AC repair Dallas," "furnace installation," and similar local keywords.

**Example 2: A B2B SaaS company optimizing their funnel**
A project management startup uses GA4's funnel exploration to track the path from blog visit → pricing page → free trial signup. They discover a 78% drop-off between the pricing page and signup. A heat map reveals visitors are confused by the enterprise tier. They simplify pricing, and [conversion rate](/glossary/conversion-rate) jumps 23% in 6 weeks.

**Example 3: A Shopify brand identifying content that converts**
An e-commerce brand selling pet supplies checks GA4's "Pages and Screens" report filtered by users who purchased. They find that visitors who read their blog post "Best Dog Food for Sensitive Stomachs" convert at 4.2x the site average. They create 15 more articles targeting similar informational queries. Turning their blog into a top revenue-driving channel.

## Google Analytics vs. Google Search Console

People mix these up regularly. They measure different things.

| | Google Analytics | Google Search Console |
|---|---|---|
| **Tracks** | What happens on your site | How your site appears in Google Search |
| **Data starts** | When a user arrives on your page | Before a user clicks (impressions, rankings) |
| **Key metrics** | Sessions, conversions, engagement, revenue | Clicks, impressions, average position, CTR |
| **Shows** | All traffic sources (organic, paid, social, direct) | Google organic search only |
| **Best for** | Understanding user behavior and conversions | Understanding search visibility and technical [SEO](/glossary/seo) issues |

Use both. [Google Search Console](/glossary/google-search-console) tells you how you're performing in search. Google Analytics tells you what visitors do once they click.

## Google Analytics Best Practices

- **Set up conversion events on day one**. Don't just install GA4 and leave it. Define what a conversion means for your business (form submission, phone call click, purchase) and configure those events immediately
- **Connect Search Console**. Link GA4 with [Google Search Console](/glossary/google-search-console) to see organic search query data alongside on-site behavior. The integration takes 2 minutes and adds enormous context
- **Use UTM parameters for campaign tracking**. Every link in an email, social post, or ad should include [UTM parameters](/glossary/utm-parameters). Without them, GA4 lumps traffic into generic buckets and you lose attribution clarity
- **Check the "Landing Page" report weekly**. This report shows which pages attract the most traffic and convert best. It's the fastest way to identify content that works and content that doesn't
- **Don't just collect data. Act on it**. The most common GA4 mistake is setting it up and never logging in. Schedule a 15-minute weekly review of acquisition and conversion reports. Pattern recognition compounds over time

## Frequently Asked Questions

### Is Google Analytics free?

GA4's standard version is completely free and handles most businesses' needs. Google Analytics 360 (the enterprise version) starts at approximately $50,000/year and adds higher data limits, SLA support, and advanced BigQuery integration.

### What replaced Universal Analytics?

Google Analytics 4 (GA4) replaced Universal Analytics on July 1, 2023. GA4 uses event-based tracking instead of session-based, has a redesigned interface, and includes built-in machine learning for predictive metrics and attribution.

### How do I install Google Analytics?

Add the GA4 tracking snippet to every page of your site (usually in the `<head>` tag) or install it through Google Tag Manager. Most website platforms. WordPress, Shopify, Webflow, Squarespace. Have native GA4 integrations that require only your Measurement ID.

### Does Google Analytics affect site speed?

The GA4 tracking script is lightweight (~28KB) and loads asynchronously, so it has minimal impact on page performance. Using Google Tag Manager to manage GA4 and other tags is the recommended approach to keep [page speed](/glossary/page-speed) in check.

---

Want the organic traffic Google Analytics measures to actually grow? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google: Introduction to Google Analytics 4](https://support.google.com/analytics/answer/10089681)
- [Google: GA4 Event-Based Data Model](https://developers.google.com/analytics/devguides/collection/ga4)
- [BuiltWith: Google Analytics Usage Statistics](https://trends.builtwith.com/analytics/Google-Analytics)
- [Google: About Attribution in GA4](https://support.google.com/analytics/answer/10596866)
- [Search Engine Journal: GA4 Complete Guide](https://www.searchenginejournal.com/google-analytics-4-guide/)
