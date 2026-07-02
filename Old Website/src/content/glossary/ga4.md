---
term: "Google Analytics 4 (GA4)"
slug: "ga4"
definition: "Google Analytics 4 is Google's latest web analytics platform, replacing Universal Analytics with an event-based data model, cross-platform tracking, and machine learning-powered insights for measuring user behavior across websites and apps."
category: "SEO"
difficulty: "Beginner"
keyword: "what is ga4"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "google-analytics"
  - "conversion-tracking"
  - "events"
  - "looker-studio"
  - "user-behavior"
---

## What Is Google Analytics 4?

Google Analytics 4, commonly called GA4, is Google's current analytics platform. It replaced Universal Analytics in July 2023 and uses a fundamentally different data model built around events rather than sessions and pageviews.

GA4 tracks user interactions as events. A pageview, button click, scroll, video play, purchase, and file download are all events. This model provides more flexibility and better cross-platform measurement across websites and mobile apps.

## GA4 vs Universal Analytics

| Factor | Universal Analytics | Google Analytics 4 |
|---|---|---|
| Data model | Session-based, pageview-centric | Event-based |
| Cross-platform | Separate properties for web and app | Single property for web and app |
| User identification | Client ID only | Client ID plus User ID and Google signals |
| Reporting interface | Pre-built reports | Exploration reports and custom dashboards |
| Machine learning | Limited | Built-in predictive metrics |
| Data retention | Up to 26 months | 2 or 14 months for user-level data |
| Sampling | More common | Less sampling with standard reports |
| Cookie dependency | Heavy | Designed for a cookieless future |

## Key GA4 Concepts

### Events

Everything in GA4 is an event. Events fall into four categories:

| Category | Description | Examples |
|---|---|---|
| Automatically collected events | Tracked without setup | page_view, session_start, first_visit |
| Enhanced measurement events | Tracked when enabled | scroll, outbound_click, site_search, video_engagement |
| Recommended events | Predefined for common use cases | sign_up, purchase, generate_lead, share |
| Custom events | Created for your specific needs | download_whitepaper, play_demo, toggle_pricing |

### Conversions

In GA4, conversions are events you mark as important. Any event can become a conversion, giving you flexibility beyond the old goal system.

### Audiences

Audiences are groups of users defined by behavior, demographics, or attributes. GA4 audiences update in real time and can be shared with Google Ads.

### Exploration Reports

Explorations let you build custom analyses using techniques like:

- Free-form exploration
- Funnel exploration
- Path exploration
- Segment overlap
- Cohort exploration

## Why SEOs Use GA4

### Track Organic Traffic

GA4 breaks down traffic by source and medium, showing how much traffic comes from organic search. SEOs monitor organic sessions, engaged sessions, and key events from search traffic.

### Measure Content Performance

The Pages and screens report shows which pages attract the most views, engagement, and conversions. This helps identify top-performing content and content that needs improvement.

### Understand User Engagement

GA4 introduces engagement metrics that go beyond bounce rate:

| Metric | What It Measures |
|---|---|
| Engaged sessions | Sessions lasting 10+ seconds, with 2+ events, or including a conversion |
| Engagement rate | Percentage of sessions that are engaged |
| Average engagement time | Time users actively spend on your site |
| Events per session | Average number of events in a session |

### Cross-Platform Tracking

For businesses with websites and mobile apps, GA4 provides unified reporting across platforms in a single property.

### Predictive Metrics

GA4 uses machine learning to estimate:

- Purchase probability
- Churn probability
- Predicted revenue

These metrics are available when enough data exists and can guide remarketing and content strategy.

## Key GA4 Reports for SEO

| Report | What It Shows |
|---|---|
| Traffic acquisition | Sessions and engagement by source and medium |
| Pages and screens | Performance of individual pages |
| Landing page report | Where organic traffic enters your site |
| Events | All tracked interactions |
| Conversions | Which events drive business outcomes |
| Demographics | User location, device, language, and interests |
| Search console linking | Combined GA4 and Search Console data |

## Linking GA4 to Google Search Console

Connecting GA4 with Google Search Console combines ranking data with on-site behavior. This integration shows:

- Which queries bring traffic to specific landing pages
- How organic visitors engage after arriving
- Which pages have high impressions but low engagement

To set it up, go to Admin > Product links > Search Console links in GA4.

## Common GA4 Mistakes

### Treating GA4 Like Universal Analytics

GA4 is not a direct replacement with the same reports. SEOs need to learn the event model and build new reporting habits.

### Ignoring Event Tracking Setup

GA4 collects basic data automatically, but meaningful SEO and conversion insights require a deliberate event measurement plan.

### Not Defining Conversions

Without marking key events as conversions, GA4 cannot show which traffic sources and pages drive business results.

### Poor Data Retention Settings

User-level data in GA4 expires after 2 or 14 months depending on settings. For long-term analysis, export data to BigQuery or Looker Studio.

## Best Practices

- Define a clear event and conversion strategy before implementation
- Link GA4 to Google Search Console for combined SEO insights
- Set up custom exploration reports for your specific KPIs
- Use BigQuery export for long-term data storage
- Regularly audit events to ensure clean, accurate data
- Train stakeholders on GA4's different reporting model

## Frequently Asked Questions

### Is Universal Analytics still available?

No. Google sunset Universal Analytics in July 2023. All standard properties stopped processing data, and users were required to migrate to GA4.

### Is GA4 free?

Yes, the standard version of GA4 is free. GA4 360 is the paid enterprise version with higher limits and support.

### Can GA4 track keywords?

GA4 does not show organic search keywords directly due to privacy restrictions. Linking Google Search Console is the best way to see query data alongside GA4 behavior metrics.

### What is engagement rate in GA4?

Engagement rate is the percentage of sessions that qualify as engaged. An engaged session lasts longer than 10 seconds, contains two or more events, or includes at least one conversion.

## Summary

Google Analytics 4 is the standard for modern web and app analytics. Its event-based model, cross-platform capabilities, and predictive insights make it essential for SEOs and marketers. Learning GA4 thoroughly unlocks better understanding of organic traffic, content performance, and user behavior.
