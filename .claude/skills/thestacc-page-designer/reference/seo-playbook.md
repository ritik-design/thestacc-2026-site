# SEO Playbook — theStacc 2026

The non-negotiable SEO checklist for every page in this site. Applies to all four search surfaces: **classic Google**, **Google AI Overviews**, **AI chat engines** (ChatGPT, Perplexity, Claude, Gemini, Copilot), and **Map Pack** for local pages.

## 1. On-page SEO — every page

### Title tag
- 50–60 characters (Google truncates ~580px at desktop, ~545px mobile)
- Primary keyword in the first 30 chars
- Brand "theStacc" at the end after a separator (`|` or ` — `)
- Unique per page; never duplicate

✅ Good: `Local SEO Software — Dominate Maps in 90 Days | theStacc`
❌ Bad: `theStacc — All-in-One SEO Platform for Businesses Looking to Grow` (brand-first, generic)

### Meta description
- 150–160 characters
- Includes primary keyword + a benefit + a CTA verb
- Active voice; no clickbait

✅ Good: `Rank in the top 3 of Google Maps in 90 days. theStacc automates GBP posts, review replies, and grid-rank tracking. $1 trial — start today.`

### Single H1
- Exactly ONE `<h1>` per page
- Contains the primary keyword
- Use `.h-display` class on homepage; `.h-lg` on all other pages
- Brand-purple accent on the emphasis word(s) via `<span class="accent">` — never accent the whole H1

### H2 / H3 hierarchy
- Every section gets one `<h2>` (`.h-lg`)
- Body H3s only inside long-form content (blog, glossary, alternatives, best-of)
- Don't skip levels (no H1 → H3)
- Include secondary keywords in H2s when natural — never forced

### URL
- All lowercase, kebab-case, no underscores
- Trailing slash always (project config enforces this)
- Avoid stop words ("the", "and", "a") unless intent-bearing
- Match the search query exactly when targeting commercial keywords

### Canonical
- Every page: `<link rel="canonical" href="https://thestacc.com/path/" />`
- Self-referencing on standard pages
- Cross-domain pointing when republishing (e.g., a tool that exists on both /tools/ and a partner site)

### Open Graph + Twitter
```html
<meta property="og:type" content="website" /> <!-- or "article" for blog -->
<meta property="og:url" content="https://thestacc.com/path/" />
<meta property="og:title" content="..." />
<meta property="og:description" content="..." />
<meta property="og:image" content="https://thestacc.com/og/page-name.webp" />
<meta property="og:site_name" content="theStacc" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="..." />
<meta name="twitter:description" content="..." />
<meta name="twitter:image" content="https://thestacc.com/og/page-name.webp" />
```

OG images: 1200×630, brand-purple wash, page H1 in white Geist 64px, theStacc wordmark bottom-right.

## 2. Schema.org (JSON-LD)

Every page MUST emit one primary schema object + `BreadcrumbList`. Put in `<head>`.

### Per page type:

| Page type | Primary schema |
|---|---|
| Homepage | `Organization` + `WebSite` (with `potentialAction` SearchAction) |
| `/modules/*` | `Product` + `Offer` |
| `/pricing/` | `Product` + multiple `Offer` |
| `/blog/{slug}/` | `Article` (with `author`, `datePublished`, `image`) |
| `/glossary/{term}/` | `DefinedTerm` + `FAQPage` |
| `/reviews/{tool}/` | `Review` + `AggregateRating` |
| `/alternatives/{tool}/` | `ItemList` (alternative tools) + `FAQPage` |
| `/best/{topic}/` | `ItemList` + `FAQPage` |
| `/case-studies/{slug}/` | `Article` + `Organization` (customer) |
| `/tools/{tool}/` | `WebApplication` |
| `/compare/{a-vs-b}/` | `Article` + `FAQPage` |
| `/for/{vertical}/` | `Service` |
| SEO-keyword landing | `Service` + `FAQPage` |
| `/contact/` | `ContactPage` |
| `/about/` | `AboutPage` + `Organization` |

`BreadcrumbList` always:
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/"},
    {"@type": "ListItem", "position": 2, "name": "Modules", "item": "https://thestacc.com/modules/"},
    {"@type": "ListItem", "position": 3, "name": "Local SEO", "item": "https://thestacc.com/modules/local-seo/"}
  ]
}
```

## 3. AI-search optimization (GEO)

AI engines (ChatGPT, Perplexity, Gemini, Claude, Copilot, Google AI Overviews) cite content very differently from Google's blue links. Optimize for citation, not just rank.

### Tactics that work for AI citation
- **Answer the question in the first paragraph.** AI extracts the first 50–100 words. Lead with the answer; defer the supporting context.
- **Use clean H2 + numbered lists.** AI engines pull list items as citation snippets. Bullet points work too; numbered lists work best.
- **Include a TL;DR / key-takeaways box.** A `<div class="ai-summary">` near the top with the 3–5 most-important facts. Wrap in `<section aria-label="Summary">`.
- **Quote authoritative sources by name** — "According to Search Engine Journal (March 2025)…" gives the AI a hook for a citation that benefits you.
- **Comparison tables in HTML** (not images). AI engines parse `<table>` data; they cannot read screenshots.
- **FAQ schema** boosts both classic AI Overviews and ChatGPT citation rates.
- **Last-updated date visible** ("Updated 2026-Q2"). AI engines prefer fresh sources.
- **Statistic with source link** in the first 200 words. AI cites stats more than narrative.

### Anti-patterns (cost you citations)
- Long preambles before the answer ("In today's competitive digital landscape...") — fatal.
- Text inside images. Always render text as HTML.
- Hiding the answer behind a "click to expand". Above-the-fold answer or no citation.
- Hedging language ("might", "could", "in many cases") — AI prefers confident statements.
- Auto-translated content (low quality scores from the engines).

### `llms.txt`

Maintain `/llms.txt` at the site root listing the canonical URLs of the most important pages with 1-line summaries. The project already has this — keep it in sync as new pages launch.

## 4. Internal linking

Each new page needs at least 3 internal links to relevant cluster pages (see `sitemap.md` linking map for which pages naturally link to which).

- **In-body**: 2–4 contextual links per 1,000 words. Use exact-match or partial-match anchor text for the linked page's primary keyword.
- **Sidebar / cards**: Use the "Related" sections specified in `page-templates.md`.
- **Mega-menu** + **footer** handle the always-visible nav.

Build hubs: every cluster has a hub page (e.g., `/modules/`) and spoke pages (`/modules/content-seo/`, etc.). Hub links to all spokes; spokes link back to hub + to 1–2 sister spokes.

## 5. Image SEO

- All images **WebP** (no PNGs except `apple-touch-icon.png`).
- `alt` text describes the image's content + includes target keyword when natural.
- `loading="lazy"` on below-fold images; `fetchpriority="high"` on the LCP image (usually the hero video poster or first article featured image).
- Width and height attributes set to avoid CLS.
- File names kebab-case + descriptive (`/blog/dental-seo-results-chart.webp`, not `/blog/IMG_3421.webp`).

## 6. Core Web Vitals

| Metric | Target | How |
|---|---|---|
| LCP | < 2.5s | Hero image/video lazy-loaded only past 200px scroll; explicit width/height; preload the hero asset |
| INP | < 200ms | Heavy JS (carousel, mega-menu, scroll handlers) wrapped in `requestAnimationFrame` |
| CLS | < 0.1 | Width/height on all `<img>`/`<video>`; reserve space for above-fold ads/embeds |

## 7. Off-page SEO (longer game)

Not directly part of building a single page, but every page should be linkable:

- **Linkable assets**: Pages with proprietary data, original research, or interactive tools earn natural backlinks 5–10× more than text pages. Prioritize `/tools/*`, `/blog/{data-study}`, `/case-studies/*`.
- **Guest posts** from new blog content → high-DR SEO publications. Pitch with a TL;DR + original stat.
- **Podcast appearances** by Siddharth Gangal → link to specific landing pages (`/seo-automation-software/`, `/local-seo-software/`).
- **Affiliate program** at `/affiliates/` → activate creators in the SEO + SaaS space.
- **Free tool embeds** for partners → backlink to `/tools/{tool}/` from external sites.
- **Press / "Featured in"** logos on the homepage trust strip — pursue Mashable, TechCrunch, SEMrush blog, Backlinko, MartechZone listings.
- **Reverse mentions**: Set up Google Alerts for "theStacc" + competitor names → respond to unlinked mentions with link requests.

## 8. Local SEO specifics (for local-vertical landings)

- Embed a Google Map showing the customer's HQ (or theStacc's HQ for the local-SEO module page).
- `LocalBusiness` schema if the page represents a physical location.
- City + state in the H1 and at least 3 H2s when targeting a city-specific keyword.
- NAP consistency: name, address, phone identical across the page, the footer, and the Google Business Profile.

## 9. Page-specific extras

- **/blog/{slug}/** — `Article` schema with `image`, `datePublished`, `dateModified`, `author`, `publisher`, `headline`. Include a Table of Contents at ≥1100px with anchor links to each H2 (improves session duration).
- **/glossary/{term}/** — `DefinedTerm` schema with `termCode`, `inDefinedTermSet`. Below the definition, include a "Use this in your strategy" box linking to a related module page.
- **/tools/{tool}/** — `WebApplication` schema. Server-render the tool's empty state so the page indexes before JS runs.
- **/case-studies/{slug}/** — `Article` schema. Add a "Get results like this" CTA tied to the customer's vertical.

## 10. AI Overviews specifically

Google's AI Overviews now show on ~40% of commercial queries. To get cited:

- Hit a clean "definition" pattern in the first paragraph: `**{Term}** is a {category} that {does what} for {who}.`
- Include a table with column headers that match Google's expected feature axes (Price, Best for, Free trial, etc.).
- A `<details>` / `<summary>` FAQ section with valid `FAQPage` schema.
- An updated-date stamp.
- Outbound link to 1–2 authoritative sources (Search Engine Journal, Google's own docs, etc.) — counter-intuitively, this boosts your authority signal.

## 11. Testing checklist before "ship"

Before reporting any page as done:

1. ✅ `bun run build` exits cleanly
2. ✅ Page validates on https://validator.schema.org/ (paste the rendered HTML)
3. ✅ Lighthouse Mobile score ≥ 90 on Performance, ≥ 95 on SEO, ≥ 95 on Accessibility
4. ✅ Page loads with JavaScript disabled and shows: H1, meta, primary content, no broken layout
5. ✅ Manual test of: the magnetic CTA, scroll progress bar, sticky CTA appearance, mega-menu open/close
6. ✅ All internal links resolve (no 404s within the new project)
7. ✅ View page source — confirm canonical, OG image, JSON-LD all present

If any check fails, fix it before declaring done.
