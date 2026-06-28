# Page Templates — Section Recipes

For each page type, the ordered list of sections to include. Pull each section from `sections-library.md`.

## homepage
1. Scroll-progress + Header (mega-menu)
2. Hero (centered, full pitch)
3. Hero video (browser-chrome)
4. Trust logos
5. Stats row
6. Modules bento (3)
7. Problem section (before / after)
8. Solution intro (with `.hl-highlight` sweep)
9. How it works (3 steps)
10. Benefits cards (4)
11. Integrations grid
12. Case studies carousel
13. Testimonials (dark sticky)
14. Verticals bento
15. Cost comparison
16. Resources marquee
17. Guarantee strip
18. Final CTA (dot-pattern dark)
19. Footer

## module-detail (`/modules/content-seo/`, `/modules/local-seo/`, `/modules/social-media/`)
1. Header + scroll progress
2. Hero — H1 = "Module Name · One-line outcome promise"; subhead = the 2-paragraph value pitch; CTAs = "Start $1 trial" + "Book a demo"
3. Trust logos
4. Hero video (a module-specific demo if available; fallback to hero-demo.mp4)
5. Module-feature breakdown — 4 alternating L/R blocks each with: feature title, 2-sentence description, 3 bullet outcomes, mini-mockup visual
6. Stats row — 4 cells specific to that module (e.g. for Local SEO: "92% Map Pack top 3", "3min response", "+47 keywords / 90d", "$40k+ saved")
7. How it works (3 steps, module-specific)
8. Integrations grid (with relevant integrations highlighted)
9. The OTHER two modules as small bento (cross-sell)
10. Case studies carousel (filtered to studies using this module)
11. Cost comparison
12. Guarantee
13. Final CTA
14. Footer

## pricing
1. Header + scroll progress
2. Pricing hero — H1 = "Simple, honest pricing." or "$1 trial. No agency lock-in."; subhead = "Pick a module, or run all three."
3. **Pricing table** — 4 columns: Blog SEO $99 / Local SEO $49 / Social Media $49 / Bundle $167 — with feature-by-feature checkmark grid
4. Cost comparison (vs agency / freelancer)
5. Guarantee strip
6. Testimonials
7. FAQ accordion (12+ questions specific to billing, cancellation, trial, refund)
8. Final CTA
9. Footer

## about
1. Header
2. Hero — H1 = "We're building the AI that publishes the open web."
3. Founder story (Siddharth Gangal — origin, mission, why now)
4. Team section
5. Values / principles (3–4)
6. Press / featured-in row
7. Investors row (if applicable)
8. Open positions teaser
9. Final CTA
10. Footer

## demo (sales-led)
1. Header
2. Two-column hero: LEFT = "Book a 15-min demo" headline + 3 outcome bullets + trust line; RIGHT = scheduling embed (Calendly or HubSpot iframe)
3. Trust logos
4. What you'll see in the demo (3 bullets with mini-screenshots)
5. Testimonials (sales-flavored)
6. FAQ (demo-specific: how long, who from theStacc joins, can I bring my team)
7. Final CTA (smaller — points to $1 trial as the self-serve alternative)
8. Footer

## contact
1. Header
2. Hero — H1 = "We reply within 4 hours."
3. Two-column: LEFT = contact form (Name, Email, Company, Message) → POSTs to backend; RIGHT = direct email + Slack community link + support hours
4. Final CTA (light)
5. Footer

## changelog
1. Header
2. Hero — H1 = "What we shipped this month."
3. Reverse-chronological release entries. Each: date · version · category badge · 1-sentence outcome · expandable details
4. RSS / email-subscribe row
5. Final CTA
6. Footer

## blog-index
1. Header
2. Hero — H1 = "SEO playbooks, AI growth tactics, and the operator's brief."
3. Category pills (Content Strategy, Local SEO, SEO Tips, AI Search)
4. Featured post (1 large card with cover image)
5. Latest posts grid (12 cards, 3 cols) — title, excerpt, author, date, category, reading time
6. Pagination
7. Newsletter inline-CTA (between posts and final CTA)
8. Final CTA
9. Footer

## blog-post
1. Header + scroll progress
2. Article hero — eyebrow category, H1, author + date + reading time row
3. Featured image (16:9, lazy-loaded except this one which is `fetchpriority="high"`)
4. Article body (`prose` styles — H2/H3 hierarchy, image embeds, pull quotes, code blocks, tables of contents on the side at ≥1100px)
5. Author bio card (3-line bio + Twitter / LinkedIn links)
6. **Related posts** (3 cards) — pulled from same category
7. Newsletter inline-CTA
8. Final CTA (lite — single $1 trial button)
9. Footer

## glossary-index
1. Header
2. Hero — H1 = "690+ SEO, marketing & AI terms — explained."
3. Search bar + A–Z anchor links
4. Category tabs (SEO / Marketing / Local SEO / Social / AI & Emerging)
5. Term grid (term name + 1-line definition + arrow)
6. Pagination
7. Final CTA (lite)
8. Footer

## glossary-term
1. Header
2. Eyebrow: category breadcrumb
3. H1 = term name
4. 1-paragraph definition (the answer above the fold)
5. Detailed explanation (H2 sections: What it is, Why it matters, How it works, Common mistakes, FAQ)
6. **Related terms** (5 cards)
7. **Use this with**: 1 module page + 1 free tool that applies to this term
8. Final CTA (lite)
9. Footer

## tools-index
1. Header
2. Hero — H1 = "11 free SEO tools — no signup."
3. Tools grid (4 cols × 3 rows) — each card: icon, name, 1-line benefit, "Open tool →"
4. "Built for the daily SEO grind" — 3 outcomes
5. Final CTA (upgrade prompt to paid modules)
6. Footer

## tool-page (a single free tool)
1. Header
2. Hero — H1 = tool name in benefit form (e.g. "Generate JSON-LD schema in 30 seconds")
3. **The tool UI** — interactive form, runs client-side or via lightweight API
4. Result panel (renders inline below the form)
5. "How to use this tool" (3 steps)
6. "Why this matters" (2-paragraph SEO context)
7. **Related tools** (3 cards)
8. Upgrade CTA — "Use this tool 100×/month with [Module]. Start $1 trial."
9. Footer

## software-review (`/reviews/{tool}/`)
1. Header
2. Hero — H1 = "{Tool} Review ({year}): Honest verdict from a daily user"
3. At-a-glance card: star rating, price, best-for, our verdict in 1 sentence, "Try theStacc instead →"
4. **What is {tool}** (2 paragraphs + product screenshot)
5. **Pros** (3–5)
6. **Cons** (3–5)
7. **Features in depth** (5–7 H3 sections with screenshots)
8. **Pricing breakdown**
9. **Who is it for / not for**
10. **{Tool} vs theStacc** — quick comparison table
11. **Alternatives** (5 cards linking to `/alternatives/{tool}/` and similar reviews)
12. FAQ
13. Final CTA — "Tired of {tool}? Try theStacc — $1 for 30 days."
14. Footer

## alternative (`/alternatives/{tool}/`)
1. Header
2. Hero — H1 = "{N} Best Alternatives to {Tool} in {year}"
3. **Why people leave {tool}** (3 bullets pulled from real complaints)
4. **Featured alternative: theStacc** — featured large card on top, ranked #1 with stat-driven bullets
5. **Ranked list** of alternatives (numbered, each with: name, price, 1-line pitch, 3 pros, 1 con, "Try X →")
6. **Comparison table** (cross-reference key features across all alternatives)
7. **Migration guide** — 3 steps to switch from {tool} to theStacc
8. FAQ
9. Final CTA
10. Footer

## best-of (`/best/{topic}/`)
1. Header
2. Hero — H1 = "Best {topic} for {year}: {N} tools tested and ranked"
3. **Quick verdict box** — winner / best-value / best-for-{persona} / runner-up — 4 cards
4. **Methodology** (200 words — how we tested, criteria)
5. **Ranked list** — 8–12 entries, each with: rank, name, screenshot, price, 1-paragraph review, 3 pros, 1 con, link
6. **Comparison table**
7. **What to look for** (buyer's-guide H2)
8. **FAQ**
9. Final CTA — "Skip the comparison shopping. Try theStacc."
10. Footer

## case-study (`/case-studies/{slug}/`)
1. Header
2. Hero — eyebrow vertical + location, H1 = customer's outcome quote, customer headshot + company logo
3. **The challenge** (2 paragraphs)
4. **The approach** (which theStacc modules they used)
5. **The results** — big stat grid (4–6 numbers, animated counters)
6. **Pull-quote** from the customer (full-bleed, brand-soft background)
7. **Timeline** (Week-by-week milestones with mini-screenshots)
8. **Tools used** (list of theStacc modules + integrations)
9. **What's next** (1 paragraph on the customer's roadmap)
10. **Other case studies** (3 cards in carousel)
11. Final CTA — vertical-targeted ("Run a dental practice? Talk to us.")
12. Footer

## vs-page (`/compare/{a-vs-b}/`)
1. Header
2. Hero — H1 = "{A} vs {B} ({year}): Which one's right for your team?"
3. **Side-by-side at-a-glance** (3-col table: feature / A / B)
4. **The big picture** (one paragraph for each tool)
5. **Feature-by-feature deep dive** — 6–8 sections, each with H2 = feature category, then a comparison
6. **Pricing** (side-by-side)
7. **Who should pick A** + **Who should pick B** (decision tree)
8. **Why theStacc beats both** (1 short section — fair, not slimy)
9. FAQ
10. Final CTA
11. Footer

## vertical-landing (`/for/dentists/`, `/for/lawyers/`, etc.)
1. Header
2. Hero — H1 names the vertical explicitly ("Win more patients with AI-powered local SEO."), CTAs adapted
3. Trust logos (filtered to that vertical if possible)
4. **What this vertical struggles with** (3-card pain section using the persona's actual pain language from icp.md)
5. **What theStacc does for {vertical}** — 4 outcomes
6. **Live local SERP mockup** for that vertical's queries (use the homepage's `.serp-section`)
7. **Module breakdown** — typically Local SEO is featured here
8. **Case studies** from this vertical (if available — otherwise generic case-studies carousel)
9. **Pricing** mini-table
10. **FAQ** specific to the vertical
11. Final CTA — "Book a 15-min demo for {vertical}s"
12. Footer

## keyword-landing (e.g. `/seo-automation-software/`, `/local-seo-software/`, `/google-business-profile-software/`)

The keyword IS the H1. Match search intent (commercial-investigation).

1. Header
2. Hero — H1 = the exact keyword, subhead = a benefit-driven expansion, CTAs
3. Trust logos
4. **What is {keyword}** (H2, 2-paragraph definition — captures featured-snippet intent)
5. **Why most {keyword} tools fail** (3-card pain)
6. **What to look for** (5 numbered criteria)
7. **theStacc as the answer** — 3–4 outcome bullets
8. **Comparison table** (3–5 competitor tools vs theStacc, with ✓/✗ marks)
9. **How theStacc {keyword}** — 3-step how-it-works
10. **Pricing** mini-table
11. **Case study** — 1 featured study
12. **FAQ** — 8–12 questions matching People Also Ask data for the keyword
13. Final CTA
14. Footer

## Mini-template: lite final CTA (for content pages)

Content pages (glossary, blog post, tool, docs) end with a SINGLE-section CTA instead of the full guarantee+final-CTA combo:

```html
<section class="final-section dark" style="padding: 64px 32px;">
  <div class="final-content" style="max-width: 720px;">
    <h2 class="final-headline" style="font-size: clamp(28px, 3.5vw, 44px);">Ready to publish on autopilot?</h2>
    <p class="final-sub">$1 trial. 24-hour setup. Cancel anytime.</p>
    <a href="/checkout/" class="final-cta-btn">Start your $1 trial →</a>
  </div>
</section>
```
