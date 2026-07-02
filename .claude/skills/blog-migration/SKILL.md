---
name: blog-migration
description: >
  Migrate all 900 English thestacc.com/blog posts to the new 2026 design
  using the /reviews/aiseo/ layout (review-post.css). Content-only
  extraction from the live source, URL/slug preservation, per-post
  SEO/AIO/GEO optimization, rotating E-E-A-T author byline
  (Siddharth Gangal, Akshay VR, Ritik Namdev), HTML/SVG on-page visuals
  instead of imported images. Every migration writes a finished Astro file
  to src/pages/blog/{slug}/index.astro, updates the progress tracker, and
  commits. Fully resumable — reads progress.json on start and skips
  anything already done.
  Use when the user says: "migrate blog", "continue blog migration",
  "migrate theStacc blog", "next batch of blog posts", "resume blog work",
  "blog post by post", or when they provide a specific blog slug to write.
user_invocable: true
---

# Blog Migration Skill — thestacc.com

You migrate English blog posts from `https://thestacc.com/blog/{slug}/` (live) to `/src/pages/blog/{slug}/index.astro` (new design) at `/home/ritik/thestacc.com-astro/thestacc-2026-site/`. **Content-only, URL-preserving, E-E-A-T-driven, resumable.**

---

## MISSION

Move **900 English blog posts** from the old design to the new blog-post design. Every post is a standalone Astro page. Content is rewritten from the live source but **improved and expanded** — better SEO, AI-Overview readability, GEO citation-worthiness, and conversion intent. Design elements from the old page are **discarded entirely**.

### Non-negotiable rules

1. **URL structure preserved.** Slug stays exactly as on the live site. No renaming, no consolidation, no redirects. Output path is always `src/pages/blog/{slug}/index.astro`.
2. **Content-only extraction.** Read the live page to get: title, H2/H3 sections, body text, examples, FAQs, data, tables, takeaways. Ignore its HTML structure, classes, scripts, embedded widgets, and images.
3. **Design comes from the new template only.** The canonical copy-paste template is `.claude/skills/blog-migration/template.astro` (mirrors the /reviews/aiseo/ layout using `review-post.css`). A live preview exists at `src/pages/design/blog-post-redesign/index.astro`. Never copy CSS classes, layout, or markup from `thestacc.com/blog/*` source.
4. **E-E-A-T author rotation.** Every post carries a real byline from one of the three theStacc operators: Siddharth Gangal, Akshay VR, or Ritik Namdev. Author is chosen by topic fit, not randomly.
5. **No imported images.** Old images are not downloaded or hotlinked. Replace them with on-brand HTML/CSS/SVG diagrams, code blocks, tables, or icon-only visuals generated inline.
6. **Progress is tracked** in `/home/ritik/thestacc.com-astro/thestacc-2026-site/Stacc/blog-migration/progress.json`. Every completed post updates this file.
7. **Resumable.** On start, read `progress.json`. Skip anything with `status: "done"`. Retry `failed` up to 3 times.
8. **Build-verify before commit.** No commits with a broken build.
9. **Detailed, rank-worthy content.** Do not thin the source. Expand weak sections, add concrete examples, add numbered steps, add comparison tables, and add an FAQ block. The goal is to protect and improve current rankings, not just copy them.
10. **Lead generation embedded naturally.** Every post ends with a product-relevant CTA and at least one contextual inline link to a theStacc module, feature, or `/checkout/`.

---

## FILES YOU MANAGE

| Path | Purpose |
|---|---|
| `/home/ritik/thestacc.com-astro/thestacc-2026-site/Stacc/blog-migration/slugs.txt` | Full list of 900 English blog slugs (read-only reference) |
| `/home/ritik/thestacc.com-astro/thestacc-2026-site/Stacc/blog-migration/progress.json` | Per-post status: `pending` \| `in_progress` \| `done` \| `failed` |
| `/home/ritik/thestacc.com-astro/thestacc-2026-site/src/pages/blog/{slug}/index.astro` | The output file (one per post) |
| `/home/ritik/thestacc.com-astro/thestacc-2026-site/.claude/skills/blog-migration/template.astro` | Canonical copy-paste template with `{PLACEHOLDERS}` |
| `/home/ritik/thestacc.com-astro/thestacc-2026-site/src/pages/design/blog-post-redesign/index.astro` | Live design preview of the template (buildable example) |
| `/home/ritik/thestacc.com-astro/thestacc-2026-site/src/styles/review-post.css` | Shared stylesheet for the aiseo-style blog layout |
| `/home/ritik/thestacc.com-astro/thestacc-2026-site/src/pages/authors/{author-slug}/index.astro` | Author pages for byline links |

---

## PROGRESS TRACKER STRUCTURE

`progress.json` shape:

```json
{
  "meta": {
    "total_posts": 900,
    "source_site": "https://thestacc.com/blog/",
    "target_site": "https://thestacc.com/blog/",
    "template_reference": "/.claude/skills/blog-migration/template.astro",
    "authors": [
      {"slug": "siddharth-gangal", "name": "Siddharth Gangal", "role": "Founder & CEO", "initials": "SG"},
      {"slug": "akshay-vr", "name": "Akshay VR", "role": "Marketing Head", "initials": "AVR"},
      {"slug": "ritik-namdev", "name": "Ritik Namdev", "role": "Growth Manager", "initials": "RN"}
    ],
    "created": "2026-07-01",
    "note": "English blog only. URLs preserved exactly. Content extracted and rewritten from live source; no design/HTML/scripts copied."
  },
  "totals": { "pending": 900, "in_progress": 0, "done": 0, "failed": 0 },
  "posts": {
    "ai-email-micro-segmentation": {
      "status": "done",
      "category": "AI & Emerging",
      "author": "siddharth-gangal",
      "attempts": 1,
      "last_error": null,
      "word_count": 2100,
      "verified_at": "2026-07-01T10:00:00Z",
      "commit": null
    },
    "...": { "status": "pending", ... }
  }
}
```

### Read progress on start

```python
import json
progress = json.load(open('/home/ritik/thestacc.com-astro/thestacc-2026-site/Stacc/blog-migration/progress.json'))
pending = [s for s, t in progress["posts"].items() if t["status"] in ("pending", "failed") and t["attempts"] < 3]
print(f"To do: {len(pending)}")
```

### Update progress after each post

```python
progress["posts"][slug]["status"] = "done"
progress["posts"][slug]["attempts"] += 1
progress["posts"][slug]["word_count"] = word_count
progress["posts"][slug]["verified_at"] = datetime.utcnow().isoformat() + "Z"
progress["posts"][slug]["commit"] = commit_sha[:7]
progress["totals"] = {
  s: sum(1 for t in progress["posts"].values() if t["status"] == s)
  for s in ["pending", "in_progress", "done", "failed"]
}
json.dump(progress, open('.../progress.json', 'w'), indent=2)
```

---

## AUTHOR ASSIGNMENT — E-E-A-T TOPIC MAPPING

Use the three theStacc authors to maximize expertise signals. Map by **primary topic of the post**, not by word count or random rotation.

| Topic / Post type | Assigned author | Rationale |
|---|---|---|
| AI search, GEO, LLM SEO, AI agents, generative engine optimization, ChatGPT/Perplexity ranking, technical architecture, product strategy, founder operations | **Siddharth Gangal** | Founder & CEO; the public technical/founder voice |
| SEO strategy, keyword research, editorial workflows, content operations, B2B SaaS marketing, brand voice, demand generation, on-page SEO | **Akshay VR** | Marketing Head; owns editorial and SEO strategy |
| Programmatic SEO, CRO, analytics, growth experiments, funnel ops, GA4/Search Console, A/B testing, content scaling, automation | **Ritik Namdev** | Growth Manager; owns growth systems and pSEO |

### Author object to use in frontmatter schema

For each author, build the `author` JSON-LD exactly:

**Siddharth Gangal**
```json
{
  "@type": "Person",
  "name": "Siddharth Gangal",
  "url": "https://thestacc.com/authors/siddharth-gangal/",
  "sameAs": ["https://www.linkedin.com/in/sidgangal/"]
}
```

**Akshay VR**
```json
{
  "@type": "Person",
  "name": "Akshay VR",
  "url": "https://thestacc.com/authors/akshay-vr/",
  "sameAs": ["https://www.linkedin.com/in/akshay-vr-3aa1b9204/"]
}
```

**Ritik Namdev**
```json
{
  "@type": "Person",
  "name": "Ritik Namdev",
  "url": "https://thestacc.com/authors/ritik-namdev/",
  "sameAs": ["https://www.linkedin.com/in/ritiknamdev/"]
}
```

In the byline, link the author name to `/authors/{author-slug}/` and use the matching initials avatar (`SG`, `AVR`, `RN`).

---

## BLOG SEO — RESEARCH-BACKED BEST PRACTICES

Every migrated post must be more competitive than the live source. Apply these tactics deliberately.

### 1. Title tag (50–60 chars)

Pattern options:
- `{Keyword}: {Benefit} | theStacc`
- `How to {Outcome} in {Year} | theStacc`
- `{N} Ways to {Outcome} ({Year}) | theStacc`
- `{Topic} Guide: {Specific Promise} | theStacc`

Primary keyword appears near the front. Avoid clickbait. Include year only if the post is genuinely time-bound.

### 2. Meta description (150–160 chars)

Include primary keyword + a specific benefit + a number or timeframe where natural. Treat it as ad copy for the SERP.

### 3. H1 = title, single H1 only

The H1 must contain the primary keyword and match search intent. Keep it under 70 characters.

### 4. Lede paragraph (first 100 words)

The first paragraph must answer the query directly. Formula:
- **Definition posts:** "{Topic} is {category} that {does what}. In this guide you will learn {list of 3-4 outcomes}."
- **How-to posts:** "Here is how to {outcome} in {context}. The short version: {3-4 numbered steps}."
- **List posts:** "{Topic} comes down to {N} decisions. This post covers each one, with {proof point}."

### 5. Heading hierarchy

- H2s are major sections (question or benefit form).
- H3s are sub-steps, examples, or variants.
- Never skip levels (no H4 unless there is an H3).
- Every H2 should be a natural PAA candidate.

### 6. Entity and semantic coverage

After extracting the source, expand the post to cover:
- What it is
- Why it matters now
- How it works (step-by-step)
- Common mistakes
- Tools or examples
- Measuring success
- FAQ

### 7. Internal linking

Every post must contain:
- 3–5 internal links to relevant theStacc pages (modules, features, glossary terms, other blog posts)
- 1 contextual link to `/checkout/` or `/pricing/` or `/demo/`
- Author byline link to `/authors/{author-slug}/`

### 8. External sources

Cite 2–4 real, verifiable sources per post. Use inline links, not footnotes alone. Good sources: Google documentation, Ahrefs/Moz/Semrush studies, Statista, Litmus, HubSpot research, academic/industry papers.

### 9. Schema

Every post must include:
- `Article` schema with `headline`, `description`, `image`, `datePublished`, `dateModified`, `author`, `publisher`
- `BreadcrumbList`: Home → Blog → {Post}
- Optional `FAQPage` if the post has 3+ FAQs

### 10. Conversion intent

Do not bolt a generic CTA at the bottom. Tie it to the post:
- Local SEO post → link to `/modules/local-seo/`
- Content SEO post → link to `/modules/content-seo/`
- AI search post → link to `/blog/` or `/demo/`
- Analytics/CRO post → link to `/features/client-reporting/` or `/checkout/`

---

## AIO (AI OVERVIEW) OPTIMIZATION

Google's AI Overview extracts blog content into short-answer boxes. To be the extracted source:

1. **First 100 words = the complete answer.** If the AI cannot answer the query from the first paragraph, it will not cite you.
2. **List format wins.** Use `<ol>` and `<ul>` with 3–7 items for process and feature answers.
3. **Numbered steps for "how" queries.** "1. First, X. 2. Then, Y." gets extracted verbatim.
4. **Table for comparisons.** "X vs Y" tables get pulled into AI Overview cards.
5. **FAQPage schema** — Google explicitly uses FAQPage answers in AI Overview.
6. **Define terms early.** If the post uses jargon, define it in the first 200 words.

---

## GEO (GENERATIVE ENGINE OPTIMIZATION) — per platform

| Platform | What it favors | Tactic in blog pages |
|---|---|---|
| **ChatGPT** | Structured answers with clear definitions | Snippet-like opening + numbered lists |
| **Gemini** | Entity-rich, fact-based content | Author schema + numeric anchors + tables |
| **Perplexity** | Visible sources with citations | Inline links to real sources |
| **Claude** | Nuanced perspective (pros + cons) | Comparison tables + best practices + common mistakes |
| **Copilot** | Actionable step-by-step | Ordered lists for "how to" sections |

---

## IMAGE AND MEDIA POLICY

**Do not import images from the old blog.** Do not hotlink them. Do not use `<img>` tags pointing to thestacc.com or external URLs.

Instead, replace every visual with one of these:

1. **Designed feature image (mandatory).** The hero image must be a custom SVG illustration that represents the post topic — not just a gradient box. Use the brand palette (`#4f39f6`, `#615fff`, `#ede9fe`, `#f5f3ff`), simple geometric shapes, labels, arrows, and icons. It must be wrapped in `.feature-image` and have `aria-hidden="true"`.
2. **Inline SVG diagram** for workflows, funnels, architectures, redirect chains, etc.
3. **HTML table** for comparisons, feature matrices, schedules.
4. **Code block** for config snippets, regex, JSON, commands.
5. **Numbered step visual** built with flex/grid and CSS counters.

If the source contains a screenshot, diagram, or infographic, describe it in words or reproduce it as a clean HTML/CSS/SVG equivalent.

---

## LAYOUT AND SIDEBAR STRUCTURE

Every blog post must use the /reviews/aiseo/ two-column desktop layout:

```astro
---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';
---
```

```
<section class="post-hero">...</section>
<section class="post-cover">...</section>
<div class="post-body-wrap">
  <div class="post-grid">
    <article class="post-content">...</article>
    <aside class="post-sidebar">
      <div class="sidebar-cta">...</div>
      <nav class="sidebar-toc" id="toc">...</nav>
      <div class="sidebar-share">...</div>
    </aside>
  </div>
</div>
<section class="related-posts">...</section>
```

### Required CSS behavior
- `.post-body-wrap` centers the content and constrains max-width
- `.post-grid` uses flexbox: content `flex: 1 1 0`, sidebar `flex: 0 0 320px`, gap `48px`, `align-items: flex-start`
- `.post-content` holds the article body; tables and code blocks must not overflow
- On screens ≤1024px, the sidebar hides and the content becomes single-column
- `.sidebar-cta` and `.sidebar-toc` are sticky via `position: sticky; top: 96px;`
- `.sidebar-cta` uses the brand gradient (`var(--brand)` to `var(--brand-deep)`) with white text and a white button
- `.sidebar-toc` links to every H2 `id` and highlights the active section on scroll
- `.post-cover` contains a designed SVG feature image (no `<img>` tags)

### Sticky CTA banner copy rules
- Eyebrow: short offer label (e.g. “Free SEO audit · 24-hour delivery”)
- Title: 4–7 words tied to the post topic
- Description: one sentence, specific outcome
- Button: one verb + “$1 trial” or “Book demo”
- Examples:
  - Redirect post → “Audit every redirect on your site”
  - Local SEO post → “Rank higher in local search”
  - AI content post → “Publish 30 AI-optimized articles/month"

---

## PER-POST WORKFLOW (12 steps)

For each `{slug}`:

### Step 1 — Read progress
Check `progress.json`. If `posts[slug].status == "done"`, skip.

### Step 2 — Fetch live source
```bash
curl -s -A "Mozilla/5.0" "https://thestacc.com/blog/{slug}/" -o /tmp/blog-src-{slug}.html
```
If curl fails (404 or empty), mark `failed` with reason `source_unavailable` and continue.

### Step 3 — Extract content
Parse the source HTML. Extract ONLY:
- `<title>` and H1
- Meta description (if useful)
- Category/topic tags (often shown near the title)
- Published/updated dates
- H2 section titles and body text
- H3 subsections
- Any lists, tables, or code blocks
- FAQ questions + answers
- Real examples, stats, cited sources
- Existing internal links and CTAs

Ignore: image tags, embedded widgets, CSS classes, JavaScript, ad blocks, promo banners, header/footer markup.

### Step 4 — Determine category
Use the source category if clear (SEO Tips, Content Strategy, Local SEO, AI & Emerging). If unclear, infer from the title and content. Store it in `progress.json[posts][slug].category`.

### Step 5 — Assign author
Use the E-E-A-T topic mapping table. Store `progress.json[posts][slug].author`.

### Step 6 — Build SEO metadata
- Primary keyword = the natural search query the post answers
- Title: 50–60 chars, keyword-front-loaded
- Description: 150–160 chars, benefit + keyword
- Canonical: `https://thestacc.com/blog/{slug}/`
- OG image: `/og/blog-{slug}.webp`
- `datePublished` and `dateModified`: preserve the original year/month if discoverable; otherwise use current year

### Step 7 — Write the page

Follow the canonical template at `/.claude/skills/blog-migration/template.astro` (uses `review-post.css` and mirrors the /reviews/aiseo/ layout). A live preview is at `/src/pages/design/blog-post-redesign/index.astro`. Every page has:

**Frontmatter:**
```astro
---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {
  title: '{Optimized title} | theStacc',
  description: '{Optimized meta description}',
  canonical: 'https://thestacc.com/blog/{slug}/',
  ogImage: '/og/blog-{slug}.webp',
  schemaData: [
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/" },
        { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/" },
        { "@type": "ListItem", "position": 3, "name": "{Post name}", "item": "https://thestacc.com/blog/{slug}/" }
      ]
    },
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{H1 text}",
      "description": "{Meta description}",
      "image": "https://thestacc.com/og/blog-{slug}.webp",
      "datePublished": "YYYY-MM-DD",
      "dateModified": "YYYY-MM-DD",
      "author": { "@type": "Person", "name": "{Author Name}", "url": "https://thestacc.com/authors/{author-slug}/", "sameAs": ["..."] },
      "publisher": { "@type": "Organization", "name": "theStacc" }
    },
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        { "@type": "Question", "name": "{FAQ question}", "acceptedAnswer": { "@type": "Answer", "text": "{FAQ answer}" }}
      ]
    }
  ]
};
---
<BaseLayout seo={seo}>
  <!-- content -->
</BaseLayout>
```

**Body sections (in order — mandatory):**
1. `<section class="post-hero">` — breadcrumb, category eyebrow, `<h1>`, hero description, post meta (author avatar + name + role · published date · read time · updated)
2. `<section class="post-cover">` — **designed SVG feature image** (no `<img>`). Must visually explain the post topic at a glance. Use `.cover-mono`, `.cover-title`, `.cover-sub`.
3. `<div class="post-body-wrap">` → `<div class="post-grid">` two-column grid:
   - **Left column `<article class="post-content">`**:
     - `.lede-p` — 40–80 word direct answer (featured-snippet target)
     - `.callout.callout-tldr` — "TL;DR" key takeaway box
     - `.inline-cta` — contextual CTA tied to the post topic
     - `<h2 id="...">` sections covering the full topic (minimum 5–7 H2s for posts over 1,500 words)
     - At least one `<table>` for comparison or schedule
     - At least one `<ol>` for numbered steps or best practices
     - At least one `<ul>` for parallel items
     - `<h2>Common mistakes to avoid</h2>` — when relevant
     - `<h2 id="faq">Frequently asked questions</h2>` — `.faq-list` with 4–6 Qs and accordion script
     - `.inline-cta.dark` — bottom CTA before sources
     - `<h2 id="sources">Sources & methodology</h2>` — `.sources-block` with 2–4 cited sources
     - `.author-block` — avatar initials, author name linked to `/authors/{author-slug}/`, role, short bio, social links
   - **Right column `<aside class="post-sidebar">`** (hidden on mobile, sticky on desktop):
     - `.sidebar-cta` — sticky CTA banner with eyebrow, title, description, button, bullets, social proof
     - `.sidebar-toc#toc` — sticky table of contents linking to every H2 `id`
     - `.sidebar-share` — X, LinkedIn, copy-link buttons
4. `<section class="related-posts">` — 3 related cards linking to other blog posts, glossary, or modules

**Required script (inline, at the bottom of the page):**
```astro
<script is:inline>
  function toggleFaq(btn) {
    const item = btn.parentElement;
    const wasOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    if (!wasOpen) item.classList.add('open');
  }

  const toc = document.getElementById('toc');
  if (toc) {
    const links = toc.querySelectorAll('a[href^="#"]');
    const headings = Array.from(links).map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          links.forEach(l => l.classList.remove('active'));
          const active = toc.querySelector('a[href="#' + entry.target.id + '"]');
          if (active) active.classList.add('active');
        }
      });
    }, { rootMargin: '-96px 0px -70% 0px', threshold: 0 });
    headings.forEach(h => observer.observe(h));
  }
</script>
```

### Step 8 — Improve and expand content
Before saving, ensure:
- ☐ Post answers the search query in the first 100 words
- ☐ H1 contains primary keyword
- ☐ H2s are questions or benefit statements and have unique `id` attributes
- ☐ At least one comparison table
- ☐ At least one ordered list
- ☐ At least 2 concrete examples or case-style numbers
- ☐ 4–6 FAQ questions
- ☐ 3–5 internal links + 1 conversion CTA
- ☐ 2–4 external source citations
- ☐ Banned words removed ("delve", "leverage", "game-changer", "world-class", "synergy")
- ☐ Short paragraphs (2–4 sentences max)
- ☐ Specific numbers wherever possible

### Step 9 — Replace images and add visuals
Remove all `<img>` tags from extracted content. Then add:
- **A designed SVG feature image** in the hero that explains the topic visually
- Inline SVG diagrams where they clarify workflows
- HTML tables for comparisons
- Code blocks for snippets

### Step 10 — Build verify
```bash
cd /home/ritik/thestacc.com-astro/thestacc-2026-site && bun run build 2>&1 | tail -5
```
If it fails, mark as `failed`, save error to `last_error`, and move on. Do not halt the whole run.

### Step 11 — Update progress
```python
progress["posts"][slug]["status"] = "done"
progress["posts"][slug]["word_count"] = actual_count
progress["posts"][slug]["verified_at"] = now_iso()
progress["posts"][slug]["attempts"] += 1
# Recount totals
```

### Step 12 — Commit
Commit every 5–10 posts (batch commits) so progress is durable:
```bash
git add src/pages/blog/{slug1}/index.astro ... Stacc/blog-migration/progress.json
git commit -m "Blog: migrate {slug1}, {slug2}, ..., {slugN} to new design"
git push
```

---

## RESUMABILITY

The skill is stateless — every run reads `progress.json` fresh.

### On start
```python
progress = load_progress()
pending = [s for s, t in progress["posts"].items()
           if t["status"] in ("pending", "failed") and t["attempts"] < 3]
done = progress["totals"]["done"]
print(f"Progress: {done}/900 done. {len(pending)} to go.")
```

### On error
- Mark post `failed`, increment `attempts`, record `last_error`
- Continue with the next post — never halt

### On quota limit
- Update progress before quota hits (commit every 5–10)
- Next run picks up automatically

### On session end without finishing
- Any post with `status: "in_progress"` gets reset to `pending` at start of next run

---

## CATEGORY TAXONOMY

Infer categories from the source. Primary categories seen on the live blog:

| Category | Typical topics |
|---|---|
| SEO Tips | Rank tracking, on-page, technical SEO, link building, audits |
| Content Strategy | Editorial calendars, briefs, scaling, content ops |
| Local SEO | GBP, citations, local ranking, maps, reviews |
| AI & Emerging | AI search, GEO, LLM SEO, agents, automation |

Categories drive:
- Eyebrow label
- Author assignment
- Related post selection
- OG image path naming

---

## BATCH SIZING

- **Sequential run:** 1 post at a time (safe, slow — good for first few test posts)
- **Parallel dispatch:** 6–8 agents, 5 posts each = 30–40 posts per wave
- **Wave cadence:** dispatch → wait for completion → build verify → commit → next wave
- **Between waves:** always update `progress.json` and commit

---

## FILE PATHS SUMMARY

```
/home/ritik/thestacc.com-astro/thestacc-2026-site/
├── src/pages/blog/{slug}/index.astro              ← output (write these)
├── .claude/skills/blog-migration/template.astro   ← canonical copy-paste template
├── src/pages/design/blog-post-redesign/           ← live design preview (buildable)
├── src/styles/review-post.css                      ← shared aiseo-style stylesheet
├── src/pages/authors/                             ← author pages (byline links)
└── Stacc/blog-migration/
    ├── slugs.txt                                   ← 900 slugs (reference)
    └── progress.json                               ← state (update after each post)
```

---

## STRICT RULES — INSTANT FAIL

1. Copying HTML/CSS/scripts from the source page
2. Renaming or altering a slug
3. Downloading or hotlinking old images
4. Using an author outside the three defined authors
5. Missing `Article` schema or `BreadcrumbList`
6. No conversion-relevant CTA
7. Less than 3 internal links
8. No author byline
9. No designed SVG feature image in the hero
10. No sticky sidebar with CTA banner and table of contents
11. Not updating `progress.json` after completing a post
12. Halting on a single failure instead of marking `failed` and moving on

---

## SUCCESS DEFINITION

The skill is done when:
- `progress["totals"]["done"] == 900`
- `bun run build` passes
- Every `/blog/{slug}/` URL returns 200
- Zero external `<img>` tags across all migrated blog pages
- Every migrated post has `Article` + `BreadcrumbList` schema
- Every migrated post has an author byline from the three defined authors
- Every migrated post has a designed SVG feature image
- Every migrated post has a sticky sidebar with CTA banner and TOC
- Random spot-checks (20 pages) all have: lede answer, comparison table or ordered list, FAQ block, author card, related section, homepage-style final CTA

---

*End of skill. Read `progress.json` on every run — never rely on session memory for state.*
