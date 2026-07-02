---
term: "Cohort Analysis"
slug: "cohort-analysis"
definition: "Cohort analysis is an analytical method that groups users by a shared characteristic or experience within a defined time period. Then tracks how each."
category: "Marketing"
difficulty: "Intermediate"
keyword: "what is cohort analysis"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "retention-rate"
  - "churn-rate"
  - "customer-lifetime-value"
  - "google-analytics"
  - "north-star-metric"
---

## What is Cohort Analysis?

Cohort analysis groups users who share a common trait. Usually their signup date or first purchase date. And tracks their behavior over subsequent weeks or months.

Instead of looking at all users as one blob, you compare how January signups behave differently from February signups. Did January's cohort retain better? Did March's cohort spend more? These patterns are invisible in aggregate data but obvious in cohort views.

[Google Analytics](/glossary/google-analytics) offers a built-in Cohort Analysis report. Amplitude, Mixpanel, and most product analytics platforms make cohorts a core feature. The technique originated in medical research (tracking patient outcomes by treatment date) and became standard in SaaS and ecommerce analytics around 2010.

## Why Does Cohort Analysis Matter?

Aggregate metrics hide the truth. Your overall [retention rate](/glossary/retention-rate) might look steady while a specific cohort is churning rapidly. Masked by new signups.

- **Retention visibility**. See exactly how long each cohort stays engaged, and identify when drop-off happens
- **Product change impact**. Launch a new feature in March? Compare March cohort retention against February to measure the real effect
- **Marketing channel quality**. Cohorts acquired from organic search may retain differently than those from paid ads. Cohort analysis reveals which channels bring lasting customers
- **Revenue forecasting**. Understanding cohort behavior patterns lets you predict future revenue from current signups

Without cohort analysis, you're making growth decisions based on averages that don't represent any real user group.

## How Cohort Analysis Works

The method is straightforward once you understand the components.

### Define the Cohort

Choose a grouping criteria. The most common is acquisition date (all users who signed up in Week 1). But you can also group by first action taken, acquisition channel, geographic location, or pricing plan. The criteria should align with the question you're trying to answer.

### Track the Metric

Pick what you're measuring: retention (% still active), revenue per user, feature usage, [churn rate](/glossary/churn-rate), or purchase frequency. Track this metric for each cohort across equal time intervals. Week 1, Week 2, Week 3, etc.

### Build the Cohort Table

A cohort table is a matrix. Rows represent cohort groups (by signup week/month). Columns represent time periods since signup. Each cell shows the metric value. You'll see patterns immediately. Maybe all cohorts drop 40% after Week 1 but stabilize after Week 4.

### Analyze and Act

Look for anomalies. If one cohort retains significantly better than others, what changed? A product update? A marketing campaign? A new onboarding flow? Cohort analysis doesn't tell you why. It tells you when something changed, and you investigate from there.

## Cohort Analysis Examples

**Example 1: SaaS onboarding improvement**
A SaaS company tracks monthly signup cohorts by 30-day retention. January: 35% retained. February: 34%. March (after a new onboarding tutorial): 48%. The improvement is clearly tied to the March product change. Something aggregate retention data would have taken months to reveal.

**Example 2: Content-driven acquisition quality**
An ecommerce brand uses cohort analysis to compare customers acquired through [organic search](/glossary/organic-search) versus paid social ads. Organic cohorts show 60% 90-day retention versus 38% for paid. [Customer lifetime value](/glossary/customer-lifetime-value) for organic is 2.1x higher. theStacc helps businesses grow the organic channel that produces higher-quality cohorts. Publishing 30 SEO articles monthly that attract intent-driven visitors.
## Frequently Asked Questions

### What tools do I need for cohort analysis?

[Google Analytics](/glossary/google-analytics) has a basic cohort report built in. For deeper analysis, product analytics platforms like Amplitude, Mixpanel, or Heap offer more flexible cohort builders. Spreadsheets work too if you export the raw data.

### How large should a cohort be?

Large enough to be statistically meaningful. For most businesses, 100+ users per cohort is the minimum. Below that, individual user behavior creates too much noise. Monthly cohorts work for smaller businesses; weekly cohorts work for high-volume products.

### What's the most important cohort to watch?

Your most recent cohort. If it's retaining worse than the previous 3 cohorts, something changed. And you need to find out what before it compounds. Catching retention drops early is the primary value of cohort analysis.

---

Want to improve your acquisition cohort quality with organic traffic? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Analytics Help: About Cohort Analysis](https://support.google.com/analytics/answer/6158745)
- [Amplitude: Guide to Cohort Analysis](https://amplitude.com/blog/cohort-analysis)
- [Mixpanel: Cohort Analysis](https://mixpanel.com/blog/cohort-analysis/)
