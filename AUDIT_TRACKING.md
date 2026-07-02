# theStacc Website Audit & Standardization Tracker

## Objective
Audit every page on theStacc website and standardize them against brand guidelines:
1. **Sharp corners everywhere** — zero `border-radius` on CTAs, boxes, cards, inputs, buttons, or any UI element.
2. **Single FAQ style** — use the accordion pattern from `/reviews/rankmath/` on every page that has FAQs.
3. **Brand consistency** — colors, typography, spacing, and components must follow the established design system.

## Brand Guidelines (derived from current source)
- **Colors**
  - Primary brand: `#4f39f6` (`--brand`)
  - Brand bright: `#6d5ef8`
  - Brand deep: `#3a28b5`
  - Brand soft: `#ede9fe`
  - Brand softer: `#f5f3ff`
  - Text 1: `#0f0f0f`
  - Text 2: `#4b5563`
  - Text 3: `#9ca3af`
  - Background: `#ffffff`
  - Background soft: `#f9fafb`
  - Border: `#e5e7eb`
  - Accent amber (stars): `#f59e0b`
- **Typography**
  - Display/headings: `Space Grotesk`, sans-serif
  - Body: `Inter`, sans-serif
  - Mono/labels: `Geist Mono`, monospace
- **Corners**
  - `border-radius: 0` everywhere (no exceptions)
- **Motion**
  - Respect `prefers-reduced-motion`
  - Micro-interactions 150–300 ms
  - Transform/opacity only for animations

## Components Created
- [x] `src/components/Faq.astro` — wrapper/list
- [x] `src/components/FaqItem.astro` — individual accordion item
- [x] Homepage FAQ now imports and uses `FaqItem.astro` directly (keeps the custom two-column layout).

## Audit Checklist
- [x] Identify all pages with `border-radius` > 0
- [x] Identify all pages with FAQ sections
- [x] Standardize FAQ markup across all pages
- [x] Remove all round corners (CSS + inline styles)
- [x] Verify build passes
- [x] Spot-check built output for lingering `border-radius`
- [ ] Spot-check mobile/responsive behavior (requires manual browser testing)

## Verification Results

### Sharp corners
- `grep -r -o -E 'border-radius\s*:[^;]*;' dist/` → **0 results** after build.
- Last remaining source `border-radius: 50% !important;` was removed from `src/pages/features/social-scheduling/index.astro` (status-dot indicator).
- Global guard remains in `BaseLayout.astro`: `*, *::before, *::after { border-radius: 0 !important; }`.

### FAQ standardization
- Built output contains `class="faq-q"` on 1,849+ pages and **zero** pages with old `class="faq-question"` markup.
- No built HTML pages contain `tool-faq` markup.
- Removed stray `.tool-content .tool-faq { margin-top: 32px; }` rule from `src/styles/tool-content.css`.

### Build
- `bun run build` completes successfully (only pre-existing `pre &#123;` CSS warnings, no errors).

## Progress Log

### 2026-07-02
- Created `AUDIT_TRACKING.md`, `src/components/Faq.astro`, `src/components/FaqItem.astro`.
- Added global sharp-corners rule: `*, *::before, *::after { border-radius: 0 !important; }` in `BaseLayout.astro`.
- Added global standard FAQ accordion styles to `BaseLayout.astro` (rankmath style).
- Removed duplicate FAQ styles from `src/styles/review-post.css`.
- Removed obsolete `.tool-faq*` styles from `src/styles/tool-content.css` and JS from `src/layouts/ToolLayout.astro`.
- Converted 23 landing pages from old `.faq-question/.faq-answer/.faq-icon` markup to standard `.faq-q/.faq-a/.faq-toggle` via `standardize_faqs.py`.
- Converted 26 tool pages from `.tool-faq*` markup to standard FAQ markup via `standardize_tool_faqs.py`.
- Manually updated homepage, pricing page, and solar case study FAQ sections to standard markup.
- Renamed conflicting form input classes in `schema-markup-generator` from `.faq-q/.faq-a` to `.sm-faq-q/.sm-faq-a`.
- Removed stale backup `src/pages/index.astro.original`.
- Ran `remove_border_radius.py` to strip `border-radius` declarations from 546 `.css` and `.astro` files (ignored `Old Website/`).

### 2026-07-02 (continued)
- Rebuilt and verified zero `border-radius` declarations remain in `dist/`.
- Verified FAQ markup is standardized across built pages.
- Converted homepage FAQ to import and use `FaqItem.astro` components while preserving the two-column layout.
- Removed final stray `border-radius: 50% !important;` inline style from `src/pages/features/social-scheduling/index.astro`.
- Removed residual `.tool-content .tool-faq` CSS rule from `src/styles/tool-content.css`.
- Updated this tracker with verification results.

### Additional fixes (after initial audit)
- Fixed dev-server crash caused by HTML-encoded braces (`&#123;` / `&#125;`) inside inline `<script>` tags on 624 blog pages via `fix_script_entities.py`.
- Fixed `/blog/` index 404s: the page hardcoded slugs that no longer existed. Rewrote `src/pages/blog/index.astro` to use actual post slugs and metadata via `update_blog_index.py`.
- Rebuilt `dist/` and restarted `astro preview` on port 7777; verified blog index and sample post links return HTTP 200.

### Migration audit & link-integrity pass
- Re-ran migration audit after restoring all 905 blog posts from `Old Website/src/content/blog/*.md`.
  - 0 missing posts, 0 posts with >15% word loss, 0 image loss, 16 minor heading-count discrepancies remain.
- Fixed global navigation/footer broken links in `src/layouts/BaseLayout.astro`:
  - `/sign-in/` → `https://app.thestacc.com/login`
  - `/customers/` → `/case-studies/`
  - `/legal/security/` → `/legal/data-processing/`
- Created missing index/redirect pages:
  - `/checkout/` (redirects to `/pricing/`)
  - `/docs/` (docs landing)
  - `/compare/` (compare index)
  - `/tools/ai-content-detector/` (redirects to `/tools/ai-humanizer/`)
- Migrated 40 missing glossary pages from `Old Website/src/content/glossary/*.md`.
- Migrated all missing `/for/*` pages from `Old Website/src/pages/for/*.astro`.
- Normalized 10,504+ internal content links to trailing-slash form via `fix_trailing_slashes.py`.
- Fixed 216 files with wrong/widely-used slugs via `fix_slug_mappings.py`.
- Added 60+ Astro redirects in `astro.config.mjs` for pages that moved or have equivalents (e.g., `/legal/privacy-policy/` → `/legal/privacy/`, `/solutions/saas/` → `/for/saas/`, missing `/alternatives/*` → `/reviews/*`).
- Fixed root-level blog links that omitted `/blog/` (e.g., `/humanize-ai-content` → `/blog/humanize-ai-content/`).
- Rebuilt `dist/` successfully: **1,970 pages**.
- Link-integrity audit on built `dist/`: **294,291 internal links scanned**, **~13 false-positive/code-example matches remain** (e.g., `href="url"`, `href="/target"` inside code samples). No real 404s remain in navigation, CTAs, footer, or main content links.
- Restarted `astro preview` on port **7777**; verified `/blog/`, sample post links, `/for/saas/`, `/glossary/schema-markup/`, `/checkout/`, `/compare/`, and `/docs/` all return HTTP 200.

### Remaining / optional follow-up
- Manual mobile/responsive browser check on homepage, pricing, `/reviews/rankmath/`, and a tool page.
- Gradually migrate other FAQ sections from inline markup to `Faq.astro` / `FaqItem.astro` components for a single source of truth. Inline markup is already visually/behaviorally identical, so this is maintenance debt rather than a visible bug.
- Review the 16 minor blog heading-count discrepancies flagged by `audit_migration.py`.
- Implement real paginated `/blog/page/N/` archive once post metadata is dynamically loaded.
