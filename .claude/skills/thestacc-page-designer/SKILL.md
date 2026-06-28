---
name: thestacc-page-designer
description: Use this skill when the user asks you to design, build, or convert a page for thestacc.com (any URL on the site — homepage, modules, pricing, blog, alternatives, reviews, best-of lists, glossary, case studies, tools, vertical pages, comparison pages, etc.) using the 2026 redesign system. Triggers include phrases like "design the pricing page", "build /alternatives/ahrefs/ in the new design", "convert the about page", "redesign /modules/local-seo/", or anything that maps to a URL listed in thestacc.com/sitemap.xml. Do NOT use this skill for unrelated SaaS sites or for editing the original `/home/ritik/thestacc.com-astro` project.
---

# theStacc 2026 Page Designer

A complete page-design workflow for the new theStacc site, located at `/home/ritik/thestacc-2026-site/`. This skill carries the full product knowledge, URL structure, design tokens, section library, SEO playbook, and page-template patterns needed to produce production-quality pages in the new design.

## Step 0 — Read the reference pack (mandatory)

Before generating any page, read these files in order. They are short and load in seconds. Do NOT skip — the design and product knowledge live here.

1. `reference/product.md` — what theStacc actually is, who it's for, pricing, modules
2. `reference/sitemap.md` — full URL structure, page-type taxonomy, internal linking map
3. `reference/icp.md` — 5 buyer personas, jobs-to-be-done, pain narratives, persona weighting per page type
4. `reference/design-tokens.md` — complete color palette, typography, spacing, radius, shadow, motion, class inventory
5. `reference/brand-voice.md` — personality, the 8 voice rules, the words we use / don't use, ready-made phrases
6. `reference/cta-library.md` — every CTA on the site with copy + URL + which class to use + placement rules
7. `reference/sections-library.md` — catalog of 20 section components proven on the homepage with line-range references
8. `reference/page-structure.md` — the 3-zone model, 6 rhythm beats, spacing rhythm, background rotation, the 8-second test
9. `reference/page-templates.md` — assembled section recipes per page type (homepage, modules, pricing, blog, glossary, reviews, alternatives, best-of, case studies, vs, vertical, keyword-landing)
10. `reference/seo-playbook.md` — title/meta rules, schema per page type, AI-search optimization, off-page SEO, testing checklist
11. `reference/keyword-optimization.md` — primary/secondary keyword placement, intent matching, SERP feature capture, density rules, title patterns

The reference homepage lives at `src/pages/index.astro` — open it whenever you need to copy a specific section's markup verbatim.

## Step 1 — Classify the page

Map the user's request to a **page type** from the taxonomy in `reference/sitemap.md`. The page type determines the section recipe to use. Common types:

| Path pattern | Page type | Recipe (in `page-templates.md`) |
|---|---|---|
| `/` | Homepage | `homepage` |
| `/modules/{slug}/` | Product module | `module-detail` |
| `/pricing/` | Pricing | `pricing` |
| `/about/` | Company | `about` |
| `/demo/` | Demo / sales-led | `demo` |
| `/contact/` | Contact | `contact` |
| `/changelog/` | Changelog | `changelog` |
| `/blog/`, `/blog/{slug}/` | Blog index / post | `blog-index`, `blog-post` |
| `/glossary/`, `/glossary/{term}/` | Glossary | `glossary-index`, `glossary-term` |
| `/tools/`, `/tools/{tool}/` | Free tool | `tools-index`, `tool-page` |
| `/reviews/{tool}/` | Software review | `software-review` |
| `/alternatives/{tool}/` | Alternative landing | `alternative` |
| `/best/{topic}/` | Best-of list | `best-of` |
| `/case-studies/{slug}/` | Case study | `case-study` |
| `/compare/{a-vs-b}/` | Comparison | `vs-page` |
| `/for/{vertical}/` | Vertical landing | `vertical-landing` |
| `/{seo-keyword}/` (e.g. `/local-seo-software/`, `/google-business-profile-software/`, `/seo-automation-software/`) | Keyword landing | `keyword-landing` |

If the request doesn't match a known pattern, ASK the user before proceeding. Don't invent a new page type unless they ask for one.

## Step 2 — Plan the page (one short block of text)

Before writing any code, output a 5-line plan to the user:

```
Page: <path>
Type: <type from taxonomy>
Primary keyword (H1): <keyword>
Section recipe: <recipe-name>
Sections (in order): hero → trust → ... → final-cta → footer
```

This lets the user redirect cheaply before you ship 500 lines of markup.

## Step 3 — Write the page

Create `src/pages/{path}/index.astro` (Astro's file-based routing). Pattern:

1. **Wrap with `BaseLayout`** (`src/layouts/BaseLayout.astro`) — gives you `<head>` (meta, fonts, design tokens, JSON-LD scaffolding), the global header with mega-menu, the global footer with arrowed-link grid, and the sticky CTA.
2. **Pass page metadata** as props: `title`, `description`, `canonical`, `ogImage`, optional `schemaType` (Article / Product / FAQPage / BreadcrumbList).
3. **Assemble sections** from `reference/sections-library.md` — copy the markup verbatim from the homepage if a near-identical section already exists; ADAPT copy and stats per the page's narrative.
4. **Reuse design tokens** — never introduce new colors, font sizes, or radii. The universal `border-radius: 0 !important` and brand purple `#4f39f6` rules are non-negotiable.

Example shell:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
const seo = {
  title: 'Local SEO Module — theStacc',
  description: '...',
  canonical: 'https://thestacc.com/modules/local-seo/',
  ogImage: '/og/modules-local-seo.webp',
  schemaType: 'Product',
};
---
<BaseLayout seo={seo}>
  <!-- HERO -->
  <section class="hero-section">...</section>
  <!-- TRUST LOGOS -->
  <section class="trust-section">...</section>
  <!-- ... remaining sections from the page-templates recipe ... -->
</BaseLayout>
```

## Step 4 — Write copy in the brand voice

Pull the voice rules from `reference/brand-voice.md`. Quick reminders while you write:

- Lead with the outcome, not the feature.
- Direct address: "you", never "users".
- Specific numbers > vague claims.
- Short sentences, two-clause max.
- One verb per CTA.
- Drop "really", "very", "incredibly", "actually".

Match CTA copy + classes to `reference/cta-library.md` — never invent a new CTA when an existing one fits. Pair Primary + Secondary in the hero.

## Step 5 — Apply the on-page SEO checklist (every page)

Pull from `reference/seo-playbook.md` and `reference/keyword-optimization.md`. Minimum non-negotiable:

- Single `<h1>` containing the primary keyword
- Meta title 50–60 chars including the primary keyword and brand
- Meta description 150–160 chars including the primary keyword + a benefit
- Canonical URL with trailing slash (project enforces `trailingSlash: 'always'`)
- One OG image (1200×630, brand-purple wash, page-specific)
- JSON-LD `BreadcrumbList` on every page beyond the homepage
- A page-appropriate primary schema (Article for blog, Product for modules, FAQPage for tool/landing pages, Review for review pages, ItemList for best-of)
- At least 3 internal links to relevant cluster pages (use the linking map in `reference/sitemap.md`)
- Image `alt` for every visual; no decorative images without `aria-hidden="true"`
- `loading="lazy"` on below-fold images, `fetchpriority="high"` on the LCP image

## Step 6 — Verify

Before reporting "done":

1. Run `bun run build` (from project root) — must complete without errors
2. Open the new URL at `http://localhost:4444/{path}/` (start the dev server with `bun dev --port 4444` if needed) and screenshot the page
3. Confirm: H1 visible above the fold, brand purple `#4f39f6` accents present, no rounded corners (per universal reset), sticky CTA appears after 200px scroll, mega-menu navbar shows, footer purple
4. Run a quick a11y pass: every interactive element keyboard-focusable, every `<img>` has `alt`, color contrast on the purple footer ≥ 4.5:1

Report what you built in one short paragraph.

## Quick rules — do these, don't argue

- The skill is for `/home/ritik/thestacc-2026-site/` only. Never touch `/home/ritik/thestacc.com-astro/` or `/home/ritik/thestacc-redesign-2026/`.
- Reuse the homepage's section markup wherever possible. The design system was tuned over many iterations — re-deriving spacing, colors, or motion from scratch wastes user time and produces inconsistency.
- Brand purple is exactly `#4f39f6`. Hover state `#615fff`. Deep `#3a28b5`. Soft `#ede9fe`. Softer `#f5f3ff`. Glow `rgba(79, 57, 246, 0.4)`. No other purples.
- All section H2 headings use `.h-lg` (38–60px clamp). No exceptions per the user's heading-uniformity preference.
- Stat-number suffixes (×, +, k, %, etc.) inside `.accent` use **the same `font-weight: 700`** as the number itself.
- Every footer link must show the up-right arrow icon (the global `::after` rule handles this — never disable it).
- The mega-menu panel is `position: fixed; left: 50%` — always centered to the viewport, not to the trigger.
- The video, the hero CTAs, the final CTA must keep their existing copy and structure unless the user explicitly asks to change them.
- Never use placeholder logos like "Acme" — pull from `public/customer-logos/` which contains 11 real customer logos.
- Universal CSS reset enforces `border-radius: 0 !important`. Round shapes (avatar tiles, brand logos, the trust-logo grayscale circles) get explicit `border-radius: 50% !important` only when intentional.

## When you finish

Update `reference/built-pages.md` with one line: `- /{path}/ — <one-sentence summary> — built <YYYY-MM-DD>`. This lets the next session know what's done.
