# Tool migration tracking

## Shared infrastructure
- [x] Schema builders (`src/lib/schema-builders.ts`)
- [x] Tool layout (`src/layouts/ToolLayout.astro`)
- [x] Tools index (`src/pages/tools/index.astro`)

## Status

| Slug | Status | Notes |
|------|--------|-------|
| gbp-post-generator | Done | Existing new-design page |
| title-tag-generator | Done | Reference migration |
| ai-humanizer | Done | Client-side demo |
| ai-visibility-checker | Done | Client-side demo |
| cms-detector | Done | Client-side demo |
| competitor-page-audit | Done | Client-side demo |
| content-brief-generator | Done | Client-side demo |
| content-gap-analyzer | Done | Client-side demo |
| faq-generator | Done | Client-side demo |
| headline-analyzer | Done | Client-side demo |
| internal-link-suggester | Done | Client-side demo |
| keyword-difficulty-checker | Done | Client-side demo |
| llms-txt-generator | Done | Client-side real generator |
| meta-tag-analyzer | Done | Client-side demo |
| on-page-seo-checker | Done | Client-side demo |
| paraphraser | Done | Client-side demo |
| people-also-ask | Done | Client-side demo |
| review-qr-code-generator | Done | Real QR rendering + download |
| review-request-generator | Done | Client-side template generator |
| review-response-generator | Done | Client-side template generator |
| schema-markup-generator | Done | Client-side JSON-LD generator |
| seo-audit | Done | Client-side demo |
| seo-roi-calculator | Done | Client-side calculator with chart |
| serp-checker | Done | Client-side demo |
| sitemap-generator | Done | Client-side XML generator |
| website-seo-score | Done | Client-side demo |
| website-traffic-checker | Done | Client-side demo |

## Build verification
- `bun run build` passed: 1893 pages built.
- `bun run preview -- --port 7777` running.
- All `/tools/{slug}/` routes return HTTP 200.

## Notes
- Old tool pages relied on missing server engines (`/js/*-engine.js`) and API endpoints. They were replaced with self-contained client-side scripts so the tools render and work in the static Astro build.
- API-backed features (DataForSEO, Kimi, live SERP, page crawls) run in demo/mock mode with realistic sample output.
- One unrelated page, `src/pages/glossary/meme/index.astro`, was converted to `src/pages/glossary/meme.astro` so the build could resolve it; the `/glossary/meme/` URL still works.
