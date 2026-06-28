# Ideal Customer Profile (ICP)

theStacc serves five distinct buyer personas. Every page must speak to AT LEAST ONE explicitly. Vertical landings + the `/for/` section pick a single persona; module + pricing + homepage speak to all five.

## Persona 1 — SaaS Growth Lead

| Trait | Value |
|---|---|
| Title | Head of Growth / Head of Content / VP Marketing / Founder (Seed–Series B) |
| Company size | 10–250 employees |
| ARR | $1M–$30M |
| Pain | Content team is the bottleneck. Programmatic SEO ideas exist but engineering deprioritises. Agency $8k/mo only ships 4 articles. |
| Jobs-to-be-done | Ship 100s of programmatic pages (alternatives, integrations, use-case, comparison). Get cited by ChatGPT/Perplexity. Replace 2 freelancers + 1 content lead with a system. |
| Triggers | Trial-to-paid funnel needs more top-of-funnel traffic. Hit a content production ceiling. New competitor ranking for "alternative to X". |
| Budget | $99–500/mo for tools |
| Buying behaviour | Self-serve trial → talks to peers in private Slack → expects $1 trial or free tier |
| Tone | Direct, data-driven, low-tolerance for marketing fluff |

**Where to surface this persona**: `/modules/content-seo/`, `/for/saas/`, `/alternatives/{tool}/`, `/compare/{a-vs-b}/`, `/seo-software/`, `/seo-automation-software/`

## Persona 2 — Local Service Business Owner / Operator

| Trait | Value |
|---|---|
| Title | Owner, founder, office manager |
| Company size | 1–25 employees, 1–10 locations |
| Verticals | Dental, legal, HVAC, plumbing, roofing, real estate, chiropractic, med-spa, restaurants, fitness, salon |
| Pain | Pays $2,500–4,500/mo agency for 2 blog posts + zero results. Map Pack shows competitors. Reviews going unanswered. |
| Jobs-to-be-done | Show up #1 when someone searches "{service} near me". Get more 5★ reviews. Reply to every review within 30 min. |
| Triggers | Agency contract renewal. Bad month for booked appointments. New competitor opened nearby. |
| Budget | $49–200/mo for tools |
| Buying behaviour | Searches "{service} SEO software", reads a blog post, books a demo OR signs up for $1 trial |
| Tone | Plain English, concrete dollar/customer outcomes, no jargon |

**Where to surface this persona**: `/modules/local-seo/`, `/for/dentists/`, `/for/lawyers/`, `/for/plumbers/`, `/for/hvac/`, `/google-maps-ranking/`, `/google-business-profile-software/`, `/local-seo-software/`, `/citation-building-software/`, `/review-management-software/`

## Persona 3 — SEO / Marketing Agency Owner

| Trait | Value |
|---|---|
| Title | Agency founder, head of operations |
| Company size | 3–30 employees, 10–60 clients |
| Pain | Hiring writers doesn't scale. Margins compressed. Clients want monthly reports. Brand voice per client is impossible to maintain across freelancers. |
| Jobs-to-be-done | White-label content for clients. Per-client brand voice. Bulk publishing across 20+ accounts. Auto-generated client reports. |
| Triggers | Lost a client over slow delivery. Quarterly margin review. Big new RFP. |
| Budget | $300–2,000/mo (priced per seat / per client account) |
| Buying behaviour | Demo first. Annual contract. Wants white-label branding. |
| Tone | Business outcomes (margin, retention, capacity), not features |

**Where to surface this persona**: `/for/agencies/`, `/white-label-seo/`, `/white-label-local-seo/`, `/white-label-reporting/`, `/seo-reseller/`, `/affiliates/`

## Persona 4 — Solo Blogger / Newsletter Operator / Niche-site Owner

| Trait | Value |
|---|---|
| Title | Creator, blogger, "internet artisan" |
| Company size | 1 person |
| Pain | Editorial calendar slipping. Burns out writing every post. Paid freelancers — disappointing. Newsletter open rates fading. |
| Jobs-to-be-done | Keep publishing weekly without writing every word. Brand voice nailed. SEO scored. One-click publish. |
| Triggers | Missed two weeks of publishing. ChatGPT made writing feel productized. Audience growing — needs more content. |
| Budget | $49–99/mo |
| Buying behaviour | $1 trial, fast cancel if not good enough |
| Tone | Honest, blunt, fellow-creator |

**Where to surface this persona**: `/for/bloggers/`, `/modules/content-seo/` (secondary message), `/tools/headline-analyzer/`, `/blog/`

## Persona 5 — Ecommerce / DTC Brand Owner

| Trait | Value |
|---|---|
| Title | Founder, head of brand, head of marketing |
| Company size | 2–40 employees, Shopify/Woo/custom storefront |
| ARR | $200K–$10M |
| Pain | Category pages don't rank. Buying-intent traffic going to Amazon/competitors. Seasonal blog content gets neglected. |
| Jobs-to-be-done | Programmatic category + buying-guide pages. Seasonal blog calendar that doesn't slip. Reviews on Google + integration with Shopify |
| Triggers | Q4 prep. Holiday shopping. A new competitor took the top spot. |
| Budget | $99–300/mo |
| Buying behaviour | Self-serve, fast trial, integrates with their existing stack |
| Tone | Revenue-attribution focused; CAC, AOV, organic-as-channel framing |

**Where to surface this persona**: `/for/ecommerce/`, `/modules/content-seo/`

---

## How to weight personas per page type

| Page type | Primary | Secondary | Tertiary |
|---|---|---|---|
| Homepage | All 5 equally | — | — |
| `/modules/content-seo/` | SaaS, Bloggers | Ecommerce | Agencies |
| `/modules/local-seo/` | Local service | Multi-location | Agencies |
| `/modules/social-media/` | All 5 | — | — |
| `/pricing/` | All 5 | — | — |
| `/about/` | All 5 (founder story matters across) | — | — |
| `/for/{vertical}/` | One specific persona | — | — |
| `/blog/{post}/` | Topic-dependent — match the persona implied by the article topic | — | — |
| `/glossary/{term}/` | Anyone learning SEO — keep generic | — | — |
| `/reviews/{tool}/`, `/alternatives/{tool}/`, `/compare/{a-vs-b}/`, `/best/{topic}/` | SaaS Growth Lead, Bloggers, Agencies | Local service if the topic is local | — |
| SEO-keyword landings | Match the keyword's natural buyer: `local-*` → Local service; `seo-software` → SaaS; `white-label-*` → Agencies | — | — |
| `/tools/*` | Any of the 5 — keep ICP-broad on tool pages, narrow on the upsell CTA | — | — |
| `/case-studies/{slug}/` | The vertical of the actual customer | — | — |

When in doubt, write to **Persona 2 (Local Service)** for plain English + dollar outcomes, then layer in a "for SaaS / agencies / bloggers" callout. Local-service tone wins everyone; SaaS-jargon tone loses local-service buyers.
