---
term: "Real-Time Bidding (RTB)"
slug: "real-time-bidding-rtb"
definition: "Real-time bidding (RTB) is the automated auction process that buys and sells individual digital ad impressions in milliseconds. Determining which ad a."
category: "Marketing"
difficulty: "Advanced"
keyword: "what is real-time bidding rtb"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "demand-side-platform-dsp"
  - "supply-side-platform-ssp"
  - "ad-exchange"
  - "programmatic-advertising"
  - "display-advertising"
---

## What is Real-Time Bidding (RTB)?

Real-time bidding (RTB) is the process of buying and selling individual ad impressions through instantaneous auctions that happen in under 100 milliseconds. While a webpage or app is loading.

Every time you visit a website with ads, an auction runs behind the scenes. The publisher offers the impression through an [ad exchange](/glossary/ad-exchange). Advertisers' [DSPs](/glossary/demand-side-platform-dsp) evaluate the impression and submit bids. The highest bidder wins. Their ad appears. You never notice because it all happened before the page finished rendering.

RTB powers the majority of [display advertising](/glossary/display-advertising) and video advertising on the open web. Google estimates that their exchanges handle over 100 billion bid requests per day. The entire process. From bid request to ad served. Takes less time than a human blink.

## Why Does RTB Matter?

RTB replaced the old model of buying ads in bulk at fixed prices. Instead of paying $10 CPM for all impressions on a site, advertisers bid different amounts for each impression based on how valuable that specific user is to them.

- **Impression-level precision**. Bid more for a user who matches your [ideal customer profile](/glossary/ideal-customer-profile) and less for everyone else
- **Market-efficient pricing**. You only pay what an impression is worth in competition, not an arbitrary rate
- **Real-time optimization**. Adjust bids based on performance data continuously, not after a campaign ends
- **Scale with control**. Access millions of impressions across the web while maintaining targeting and budget discipline

RTB made digital advertising smarter. Instead of buying ad space on websites, advertisers buy access to specific audiences wherever they happen to be.

## How RTB Works

The auction process involves multiple technology platforms communicating in milliseconds.

### Step 1: Bid Request

A user loads a webpage. The publisher's [SSP](/glossary/supply-side-platform-ssp) sends a bid request to connected ad exchanges. This request includes: ad placement details (size, position), user data (cookies, device type, location), page content category, and the publisher's floor price (minimum acceptable bid).

### Step 2: Bid Evaluation

Connected DSPs receive the bid request and evaluate it against their advertisers' campaigns. Does this user match any active targeting criteria? What's the predicted conversion probability? Based on these calculations, each DSP submits a bid or passes.

### Step 3: Auction and Winner Selection

The ad exchange runs a second-price auction (winner pays $0.01 above the second-highest bid) or a first-price auction (winner pays their actual bid). The winning DSP is notified and serves its advertiser's ad creative.

### Step 4: Ad Delivery

The winning ad renders in the user's browser. The DSP logs the impression and tracks any subsequent actions (clicks, conversions). This data feeds back into the bidding algorithm to improve future bid decisions.

## RTB Examples

**Example 1: B2B targeting at scale**
A cybersecurity company wants to reach IT directors. Their DSP evaluates millions of impressions daily through RTB. When a user matching their criteria (tech industry, senior title, enterprise company) loads a news article, the DSP bids $12 CPM. For a random user on the same page, it bids $2 or passes entirely. Same website, wildly different bids based on user value.

**Example 2: Retargeting precision**
An ecommerce brand [retargets](/glossary/retargeting-pixel) cart abandoners through RTB. Their DSP bids aggressively ($15 CPM) on users who abandoned a $500 cart and conservatively ($3 CPM) on users who abandoned a $20 cart. ROI on high-value retargeting: 12:1. theStacc helps businesses build the website traffic that feeds these retargeting pools. Publishing 30 SEO articles monthly that attract visitors who can then be retargeted through RTB.
## Frequently Asked Questions

### How is RTB different from programmatic advertising?

RTB is a type of [programmatic advertising](/glossary/programmatic-advertising). Programmatic is the broader category that includes RTB auctions, programmatic guaranteed deals, and private marketplaces. RTB specifically refers to the open auction mechanism. All RTB is programmatic, but not all programmatic is RTB.

### Does RTB work for small advertisers?

Small advertisers access RTB indirectly through Google Ads and Meta Ads. Direct RTB access through standalone DSPs typically requires $10,000+ monthly budgets. But every time you run a Google Display campaign, you're participating in RTB auctions.

### What data is shared in a bid request?

Bid requests include device type, browser, approximate location, page URL, ad size, and anonymized user identifiers. Personal data like names and email addresses are not shared. Privacy regulations like [GDPR](/glossary/gdpr) restrict what data can be included.

---

Want traffic that doesn't require bidding? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [IAB: OpenRTB Protocol Specification](https://www.iab.com/guidelines/openrtb/)
- [Google: How the Ad Auction Works](https://support.google.com/google-ads/answer/142918)
- [The Trade Desk: Real-Time Bidding Explained](https://www.thetradedesk.com/us/knowledge-center)
