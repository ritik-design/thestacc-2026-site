---
name: glossary-migration
description: >
  Migrate all 702 thestacc.com/glossary terms to the new blog-style design.
  Content-only extraction (no design elements from the source), URL/slug
  preservation, per-term SEO/AIO/GEO optimization, DefinedTerm schema,
  Akshay VR byline. Every migration writes a finished Astro file to
  src/pages/glossary/{slug}/index.astro, then updates the progress tracker
  and commits. Fully resumable — reads progress.json on start and skips
  anything already done.
  Use when the user says: "continue glossary migration", "migrate glossary",
  "next batch of glossary terms", "resume glossary work", "glossary term
  by term", or when they provide a specific glossary slug to write.
user_invocable: true
---

# Glossary Migration Skill — thestacc.com

You migrate glossary terms from `https://thestacc.com/glossary/{slug}/` (live) to `/src/pages/glossary/{slug}/index.astro` (new design) at `/home/ritik/thestacc-2026-site/`. **Content-only, URL-preserving, resumable.**

---

## MISSION

Move **702 glossary terms** from the old design to the new blog-style design (hero + 2-col + sticky sidebar + `DefinedTerm` schema). Every term is a standalone Astro page. Content is rewritten from the live source but **improved** — better SEO, AI-Overview readability, and GEO citation-worthiness. Design elements from the old page are **discarded entirely**.

### Non-negotiable rules

1. **URL structure preserved.** Slug stays exactly as on the live site. No renaming, no consolidation, no redirects.
2. **Content-only extraction.** Read the live page to get: definition, sections, examples, FAQs. Ignore its HTML structure, classes, scripts, embedded widgets, images.
3. **Design comes from the new template only.** Never copy CSS classes, layout, or markup from `thestacc.com/glossary/*` source. Every page uses the shared stylesheets + the canonical template shape.
4. **Author is fixed: Akshay VR** — Marketing Head, `AVR` avatar, amber gradient, `bodyClass="author-akshay"`.
5. **Progress is tracked** in `/home/ritik/thestacc-2026-site/Stacc/glossary-migration/progress.json`. Every completed term updates this file.
6. **Resumable.** On start, read progress.json. Skip anything with `status: "done"`. Retry `failed` up to 3 times.
7. **Build-verify before commit.** No commits with a broken build.

---

## FILES YOU MANAGE

| Path | Purpose |
|---|---|
| `/home/ritik/thestacc-2026-site/Stacc/glossary-migration/slugs.txt` | Full list of 702 slugs (read-only reference) |
| `/home/ritik/thestacc-2026-site/Stacc/glossary-migration/progress.json` | Per-term status: `pending` \| `in_progress` \| `done` \| `failed` |
| `/home/ritik/thestacc-2026-site/src/pages/glossary/{slug}/index.astro` | The output file (one per term) |
| `/home/ritik/thestacc-2026-site/src/pages/design/glossary-redesign/index.astro` | Canonical template (read it once per session) |
| `/home/ritik/thestacc-2026-site/src/styles/glossary-post.css` | Glossary-specific CSS (import alongside review-post.css) |

---

## PROGRESS TRACKER STRUCTURE

`progress.json` shape:

```json
{
  "meta": { "total_terms": 702, "author": "akshay-vr", ... },
  "totals": { "pending": 700, "in_progress": 0, "done": 2, "failed": 0 },
  "categories": { "Technical SEO": 20, "Local SEO": 55, ... },
  "terms": {
    "301-redirect": {
      "status": "done",
      "category": "Technical SEO",
      "attempts": 1,
      "last_error": null,
      "word_count": 2380,
      "verified_at": "2026-06-30T10:15:00Z",
      "commit": "abc1234"
    },
    "302-redirect": {
      "status": "pending",
      "category": "Technical SEO",
      "attempts": 0,
      ...
    }
  }
}
```

### Read progress on start

```python
import json
progress = json.load(open('/home/ritik/thestacc-2026-site/Stacc/glossary-migration/progress.json'))
pending = [s for s, t in progress["terms"].items() if t["status"] in ("pending", "failed") and t["attempts"] < 3]
print(f"To do: {len(pending)}")
```

### Update progress after each term

```python
progress["terms"][slug]["status"] = "done"
progress["terms"][slug]["attempts"] += 1
progress["terms"][slug]["word_count"] = word_count
progress["terms"][slug]["verified_at"] = datetime.utcnow().isoformat() + "Z"
progress["terms"][slug]["commit"] = commit_sha[:7]
# recount totals
progress["totals"] = {
  s: sum(1 for t in progress["terms"].values() if t["status"] == s)
  for s in ["pending", "in_progress", "done", "failed"]
}
json.dump(progress, open('.../progress.json', 'w'), indent=2)
```

---

## GLOSSARY SEO — RESEARCH-BACKED BEST PRACTICES

These are the tactics that make glossary terms rank in Google **and** get cited by ChatGPT / Perplexity / Gemini.

### 1. The featured-snippet formula

Google awards featured snippets to pages that answer a question in **40–60 words** immediately after the H1 or H2. This is why the template has a `.snippet-answer` box.

**Formula:** `[Term] is [category] that [what it does]. It [key mechanism / benefit]. [When/why used].`

Example: *"A 301 redirect is an HTTP status code that permanently sends users and search engines from one URL to another. It passes 90–99% of link equity to the new URL. Use it any time a page's URL changes."*

### 2. Entity-first writing (for AI extraction)

Language models parse the first sentence hardest. Structure:
- **Term** = [category]. [Attribute 1]. [Attribute 2]. [Relationship to Y].
- Use dfn markup semantically: the term is defined, not just mentioned.
- Include entity relationships: *X is a type of Y*, *X is often confused with Z*, *X replaces the older technique A*.

### 3. Question-answer chunks (PAA + AI Overview)

Google's "People Also Ask" and AI Overview both mine H2s and FAQs. Every H2 should be a **question form**:
- "What is [term]?" not "Definition"
- "Why does [term] matter?" not "Importance"
- "How does [term] work?" not "How it works"
- "When should you use [term]?" not "Use cases"

Each answer opens with a **direct sentence** (subject-verb-object) before elaboration.

### 4. The "vs" magnet

Nearly every glossary term has a natural comparison (301 vs 302, canonical vs redirect, backlink vs internal link). A `[Term] vs [Other]` H2 with a comparison table wins traffic from side-by-side searches AND gets excerpted by AI engines answering "what's the difference between…".

### 5. Examples-per-abstraction ratio

Every abstract statement needs a concrete example within 100 words. AI engines rank pages higher when they can extract *specific examples*. Formula:
- Definition → 1 example
- Mechanism → 2-3 examples
- Best practice → 1 example per practice

### 6. Numeric anchors

Include real numbers wherever possible: `90–99% of link equity`, `Google recognizes 301 within 24-72 hours`, `Stop following after 5 hops`. Numbers get cited by AI more than qualitative claims.

### 7. Source citations

Cite Google, IETF RFCs, or original studies (Ahrefs / Moz industry data). Perplexity and Claude heavily favor pages with visible sources.

### 8. Semantic HTML for AI parsers

- `<code>` for URLs, config snippets, HTTP methods
- `<table>` for comparisons — AI engines extract table rows as structured data
- `<ol>` for sequential steps (Google's numbered-list snippet target)
- `<ul>` for parallel items (definitions, features)
- `<blockquote>` for cited claims

### 9. Related-terms cross-linking (topical clustering)

Every term links to **6 related terms** at the bottom. This builds topical authority for Google and helps AI engines understand the term's neighborhood. Choose related terms from:
- The same category
- Direct comparisons (X vs Y)
- Prerequisites (learn X first)
- Advanced concepts (X leads to Y)
- Common confusions (X is not Y)

### 10. Sidebar A-Z navigation

The letter-jump sidebar isn't decoration — Google uses on-page anchors as UX signal AND crawlers use them to discover sibling terms. Every letter should link to `/glossary/?letter=X`.

---

## AIO (AI OVERVIEW) OPTIMIZATION

Google's AI Overview extracts glossary content into its short-answer boxes. To be the extracted source:

1. **First 100 words = the complete answer.** If the AI can't answer the query from your first paragraph, it won't cite you.
2. **List format wins.** AI Overview loves `<ol>` and `<ul>` with 3-7 items.
3. **Numbered steps for "how" queries.** Formats like "1. First, X. 2. Then, Y." get extracted verbatim.
4. **Table for comparisons.** "301 vs 302" tables get pulled into AI Overview cards.
5. **FAQPage schema** — Google explicitly uses FAQPage answers in AI Overview.

---

## GEO (GENERATIVE ENGINE OPTIMIZATION) — per platform

| Platform | What it favors | Tactic in glossary pages |
|---|---|---|
| **ChatGPT** | Structured answers with clear definitions | Snippet answer box + numbered lists |
| **Gemini** | Entity-rich, fact-based content | Metadata strip + numeric anchors |
| **Perplexity** | Visible sources with citations | Sources block with real links |
| **Claude** | Nuanced perspective (pros + cons) | `vs` comparison + best practices + common mistakes |
| **Copilot** | Actionable step-by-step | Ordered lists for "how to" sections |

---

## PER-TERM WORKFLOW (10 steps)

For each `{slug}`:

### Step 1 — Read progress
Check `progress.json`. If `terms[slug].status == "done"`, skip.

### Step 2 — Fetch live source
```bash
curl -s -A "Mozilla/5.0" "https://thestacc.com/glossary/{slug}/" -o /tmp/gloss-src-{slug}.html
```
If curl fails (404 or empty), mark `failed` with reason `source_unavailable` and continue.

### Step 3 — Extract content
Parse the source HTML. Extract ONLY:
- H1 (the term name)
- H2 section titles
- Body text of each section
- FAQ questions + answers
- Real customer quotes / stats / examples
- External source citations

Ignore: image tags, embedded widgets, CSS classes, JavaScript, ad blocks, promo banners.

### Step 4 — Categorize
Use the category already in `progress.json[terms][slug].category`. Confirm it matches actual content — if the source clearly belongs to another category, update `progress.json`.

### Step 5 — Identify related terms
Look at the source's "Related Terms" section for hints, but also search the slugs list for:
- Terms with shared word roots
- Common comparisons (`{slug}-vs-*` or `*-vs-{slug}`)
- Parent concept (if `slug = 301-redirect`, parent = `redirect`)

Pick 6 that will exist in the site once migration is done. Never link to a slug that isn't in `slugs.txt`.

### Step 6 — Write the page

Follow the canonical template at `/src/pages/design/glossary-redesign/index.astro`. Every page has:

**Frontmatter:**
```astro
---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';
import '../../../styles/glossary-post.css';

const seo = {
  title: '{Term Name}: Definition, How It Works & 2026 Guide | theStacc Glossary',
  description: '{40-80 char direct-answer definition of the term}',
  canonical: 'https://thestacc.com/glossary/{slug}/',
  ogImage: '/og/glossary/{slug}.webp',
  schemaData: [
    { /* BreadcrumbList: Home / Glossary / Category / Term */ },
    {
      "@context": "https://schema.org",
      "@type": "DefinedTerm",
      "name": "{Term Name}",
      "description": "{40-60 word definition}",
      "inDefinedTermSet": "https://thestacc.com/glossary/",
      "termCode": "{slug}",
      "url": "https://thestacc.com/glossary/{slug}/"
    },
    { /* FAQPage with 4-6 Qs */ }
  ]
};
---
<BaseLayout seo={seo} bodyClass="author-akshay">
  <!-- content -->
</BaseLayout>
```

**Body sections (in order — mandatory):**
1. `<section class="post-hero">` — breadcrumb (Home → Glossary → Category → Term), `.term-badge` (category dot + difficulty pill), `<h1>`, `.description` (preview definition), `.post-meta` (Akshay byline + Published + Read time + "Also called")
2. `<div class="post-body-wrap"><div class="post-grid">` — main + sidebar
3. `<article class="post-content">`:
   - `.snippet-answer` — 40-80 word direct definition (featured snippet target)
   - `.term-meta-strip` — 4 cells (relevant metric · Category · Key attribute · Difficulty)
   - `.lede-p` — sets up context
   - `<h2 id="what-is">What is {Term}?</h2>` — full definition + background + entities
   - `.callout.callout-info` — key context (Google's stance / RFC / industry fact)
   - `<h2 id="why-it-matters">Why {Term} matters</h2>` — 3-5 numbered reasons
   - `<h2 id="how-it-works">How {Term} works</h2>` — mechanism + optional `.url-flow` code block
   - `<h2 id="types">Types / Variants of {Term}</h2>` — comparison table with `.row-highlight` on best pick
   - `<h2 id="examples">Real {Term} examples</h2>` — 3-4 concrete examples with `.url-flow` blocks
   - `<h2 id="vs-related">{Term} vs {Closest Related} — which to use</h2>` — `.pros-cons` grid
   - `<h2 id="best-practices">{N} best practices</h2>` — numbered `<ol>`
   - `.callout.callout-warn` — common mistake / trap
   - `<h2 id="mistakes">Common {Term} mistakes to avoid</h2>` — `<ul>`
   - `<h2 id="faq">Frequently asked questions</h2>` — `.faq-list` accordion (5+ Qs)
   - `<h2 id="related-terms">Related glossary terms</h2>` — `.related-terms` grid (6 cards)
   - `<h2 id="sources">Sources</h2>` — `.sources-block` (real links, `[01]` numbered)
   - `.author-block` — Akshay VR bio
4. `<aside class="post-sidebar">`:
   - `.sidebar-cta` — audit CTA (glossary variant: "Every redirect + broken chain surfaced")
   - `.sidebar-toc` — H2 anchors, scroll-spy
   - `.letter-jumps` — A-Z grid linking to `/glossary/?letter=X`
   - `.sidebar-share`
5. `<script is:inline>` — `toggleFaq` + TOC scroll-spy

**Voice & style:**
- Akshay's editorial voice: practitioner-led, framing everything as a repeatable playbook
- Word count: 1,500–2,500 words per term (matches source depth, don't pad)
- No "In today's..." intros
- No banned words ("delve", "leverage", "world-class", "game-changer", etc.)
- Real numbers with sources
- Ordered lists for sequential things, unordered for parallel

### Step 7 — Improve SEO/AIO/GEO
Do all these before saving:
- ☐ First paragraph answers the query in 40-80 words
- ☐ H1 = term name exactly
- ☐ Every H2 is a question or benefit-driven
- ☐ At least 1 table
- ☐ At least 1 ordered list (best practices or steps)
- ☐ At least 2 concrete examples
- ☐ At least 4 FAQ questions
- ☐ 6 related-terms cross-links
- ☐ 3+ sources cited with real links
- ☐ `DefinedTerm` schema populated

### Step 8 — Build verify
```bash
cd /home/ritik/thestacc-2026-site && bun run build 2>&1 | tail -3
```
If it fails, mark as `failed`, save error to `last_error`, and move on. Don't halt the whole run.

### Step 9 — Update progress
```python
progress["terms"][slug]["status"] = "done"
progress["terms"][slug]["word_count"] = actual_count
progress["terms"][slug]["verified_at"] = now_iso()
progress["terms"][slug]["attempts"] += 1
# Recount totals
```

### Step 10 — Commit
Commit every 10 terms (batch commits) so progress is durable:
```bash
git add src/pages/glossary/{slug1}/index.astro ... Stacc/glossary-migration/progress.json
git commit -m "Glossary: migrate {slug1}, {slug2}, ..., {slug10} to new design"
git push
```

---

## RESUMABILITY

The skill is stateless — every run reads `progress.json` fresh.

### On start
```python
progress = load_progress()
# What's left?
pending = [s for s, t in progress["terms"].items() 
           if t["status"] in ("pending", "failed") and t["attempts"] < 3]
done = progress["totals"]["done"]
print(f"Progress: {done}/702 done. {len(pending)} to go.")
```

### On error
- Mark term `failed`, increment `attempts`, record `last_error`
- Continue with the next term — never halt

### On quota limit
- Update progress before quota hits (commit every 10)
- Next run picks up automatically

### On session end without finishing
- Any term with `status: "in_progress"` gets reset to `pending` at start of next run

---

## CATEGORY TAXONOMY

Categories are already assigned in `progress.json`. Distribution:

| Category | Count |
|---|---|
| General Marketing | 367 |
| Local SEO | 55 |
| Content | 49 |
| Social Media | 40 |
| Paid Advertising | 26 |
| CRO | 22 |
| Keyword Research | 21 |
| Technical SEO | 20 |
| Brand & Strategy | 20 |
| AI & Emerging | 18 |
| Email Marketing | 16 |
| Off-Page SEO | 14 |
| Sales & Growth | 10 |
| Analytics | 9 |
| Structured Data | 8 |
| On-Page SEO | 7 |

Categories drive:
- Breadcrumb 3rd segment
- `.term-badge` label
- Related-terms selection preference
- OG image path (`/og/glossary/{category-slug}/{slug}.webp`)

---

## BATCH SIZING

- **Sequential run:** 1 term at a time (safe, slow — good for high-value first pass)
- **Parallel dispatch:** 6-8 agents, 6 terms each = 36-48 terms per wave
- **Wave cadence:** dispatch → wait for completion → build verify → commit → next wave
- **Between waves:** always update `progress.json` and commit

---

## FILE PATHS SUMMARY

```
/home/ritik/thestacc-2026-site/
├── src/pages/glossary/{slug}/index.astro     ← output (write these)
├── src/pages/design/glossary-redesign/       ← canonical template (read once)
├── src/styles/review-post.css                ← shared blog CSS (import)
├── src/styles/glossary-post.css              ← glossary-specific CSS (import)
└── Stacc/glossary-migration/
    ├── slugs.txt                              ← 702 slugs (reference)
    └── progress.json                          ← state (update after each term)
```

---

## STRICT RULES — INSTANT FAIL

1. Copying HTML/CSS/scripts from the source page
2. Renaming or altering a slug
3. Inserting `<img>` tags
4. Inline `<style>` block in the page (both stylesheets are imported already)
5. Missing DefinedTerm schema
6. Byline other than Akshay VR
7. Less than 6 related terms
8. Sidebar without A-Z letter jumps
9. Not updating `progress.json` after completing a term
10. Halting on a single failure instead of marking `failed` and moving on

---

## SUCCESS DEFINITION

The skill is done when:
- `progress["totals"]["done"] == 702`
- `bun run build` passes with 260 + 702 = ~962 pages
- Every `/glossary/{slug}/` URL returns 200
- Zero `<img>` tags across all glossary pages
- Every glossary page has DefinedTerm + BreadcrumbList + FAQPage schema
- Random spot-checks (10 pages) all have: snippet-answer box, metadata strip, related-terms grid, letter jumps

---

*End of skill. Read `progress.json` on every run — never rely on session memory for state.*
