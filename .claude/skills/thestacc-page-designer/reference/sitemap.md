# theStacc URL Structure & Sitemap

Source of truth: `https://thestacc.com/sitemap-0.xml` — **3,516 URLs** total. Grouped by top-level path:

| Top path | Count | Page type |
|---|---|---|
| `/blog/{slug}/` | 933 | Blog post |
| `/glossary/{term}/` | 703 | Glossary term |
| `/best/{topic}/` | 119 | Best-of list |
| `/docs/{slug}/` | 83 | Documentation |
| `/reviews/{tool}/` | 44 | Software review |
| `/alternatives/{tool}/` | 31 | Alternative landing |
| `/tools/{tool}/` | 28 | Free tool |
| `/case-studies/{slug}/` | 4 | Case study |
| `/modules/{module}/` | 3 | Product module |
| `/lp/{slug}/` | 2 | Landing page |
| `/compare/{a-vs-b}/` | 2 | Comparison |
| Localized: `/de/`, `/es/`, `/fr/`, `/it/`, `/pt-br/` | 1,534 total | Internationalized clones |
| Root standalone pages | ~30 | Marketing/legal |

## Standalone root pages (~30, all in sitemap)

```
/                                  # Homepage
/about/                            # Company / founder story
/affiliates/                       # Affiliate program
/contact/                          # Contact form
/cookies/                          # Cookie policy
/demo/                             # Book a demo (sales-led)
/editorial/                        # Editorial standards
/franchise-seo/                    # Vertical landing
/franchise-seo-software/           # SEO-keyword landing
/google-business-profile-software/ # SEO-keyword landing
/google-maps-ranking/              # SEO-keyword landing
/local-seo-automation/             # SEO-keyword landing
/local-seo-software/               # SEO-keyword landing
/multi-location-seo/               # Vertical landing
/multi-location-seo-software/      # SEO-keyword landing
/pricing/                          # Pricing
/privacy/                          # Privacy policy
/rank-tracking-software/           # SEO-keyword landing
/review-management-software/       # SEO-keyword landing
/seo-automation-software/          # SEO-keyword landing
/seo-reseller/                     # SEO-keyword landing
/seo-software/                     # SEO-keyword landing
/social-media-automation-tool/     # SEO-keyword landing
/terms/                            # Terms of service
/thankyou-stacc/                   # Post-signup thank-you
/white-label-local-seo/            # SEO-keyword landing
/white-label-reporting/            # SEO-keyword landing
/white-label-seo/                  # SEO-keyword landing
```

## URL conventions (non-negotiable)

- **Trailing slash always** — Astro config enforces `trailingSlash: 'always'`. Never link without it.
- **Lowercase kebab-case** for all slugs
- **No file extensions** in URLs (no `.html`, no `.astro`)
- **No query strings for core pages** — query strings reserved for filtered list views and tracking
- **Canonicals must include trailing slash** and the full origin `https://thestacc.com/...`

## File-system layout (Astro file-based routing)

Each URL maps to one of these patterns inside `src/pages/`:

```
src/pages/
├── index.astro                            # /
├── about/index.astro                      # /about/
├── pricing/index.astro                    # /pricing/
├── demo/index.astro                       # /demo/
├── seo-software/index.astro               # /seo-software/  (keyword landing)
├── modules/
│   ├── index.astro                        # /modules/ (overview)
│   ├── content-seo/index.astro            # /modules/content-seo/
│   ├── local-seo/index.astro              # /modules/local-seo/
│   └── social-media/index.astro           # /modules/social-media/
├── blog/
│   ├── index.astro                        # /blog/
│   ├── page/[page].astro                  # /blog/page/{n}/
│   └── [slug].astro                       # /blog/{slug}/  (dynamic)
├── glossary/
│   ├── index.astro                        # /glossary/
│   └── [term].astro                       # /glossary/{term}/
├── alternatives/
│   ├── index.astro                        # /alternatives/
│   └── [tool].astro                       # /alternatives/{tool}/
├── reviews/
│   ├── index.astro                        # /reviews/
│   └── [tool].astro                       # /reviews/{tool}/
├── best/
│   ├── index.astro                        # /best/
│   └── [topic].astro                      # /best/{topic}/
├── compare/
│   ├── index.astro                        # /compare/
│   └── [a-vs-b].astro                     # /compare/{a-vs-b}/
├── tools/
│   ├── index.astro                        # /tools/
│   └── [tool].astro                       # /tools/{tool}/
├── case-studies/
│   ├── index.astro                        # /case-studies/
│   └── [slug].astro                       # /case-studies/{slug}/
└── for/
    └── [vertical].astro                   # /for/{vertical}/  (e.g. /for/dentists/)
```

## Internal linking map (which pages link to which)

Use these patterns when adding "Related" or "From the blog" sections, or when wiring footer/mega-nav links.

| From | Naturally links to |
|---|---|
| Homepage | All three module pages, `/pricing/`, `/case-studies/`, `/for/*`, `/blog/`, `/tools/`, `/glossary/` |
| `/modules/content-seo/` | `/pricing/`, `/blog/`, `/reviews/*` (vs. content tools), `/alternatives/*`, `/best/ai-blog-writer/`, `/tools/headline-analyzer/` |
| `/modules/local-seo/` | `/google-business-profile-software/`, `/google-maps-ranking/`, `/local-seo-software/`, `/citation-building-software/`, `/review-management-software/`, `/best/local-seo-tools/`, `/tools/gbp-post-generator/` |
| `/modules/social-media/` | `/social-media-automation-tool/`, `/best/social-media-management-tools/` |
| `/blog/{post}/` | 3 related posts, 1 module page, 1 free tool relevant to the topic |
| `/glossary/{term}/` | 5 related terms, 1 module page covering the concept, 1 tool that uses it |
| `/reviews/{tool}/` | The tool's `/alternatives/{tool}/` page, the relevant `/best/*` list, 1 module page that competes |
| `/alternatives/{tool}/` | The corresponding `/reviews/{tool}/`, the relevant `/best/*`, `/pricing/` |
| `/best/{topic}/` | All reviews + alternatives for tools in the list, 1 relevant module page |
| `/tools/{tool}/` | The relevant module page, related free tools (3), 1 related blog post |
| `/case-studies/{slug}/` | The customer's vertical landing (`/for/{vertical}/`), `/pricing/`, `/demo/` |
| `/compare/{a-vs-b}/` | The `/reviews/` and `/alternatives/` pages for both tools, `/pricing/` |
| `/for/{vertical}/` | All three module pages, 2 case studies from that vertical, `/pricing/`, `/demo/` |
| SEO-keyword landings | The matching module page, 1–2 related keyword landings, `/pricing/`, `/demo/` |

## Localization

5 locales already exist: `/de/`, `/es/`, `/fr/`, `/it/`, `/pt-br/`. When building any new English page, leave hooks for translation but do NOT generate the localized clones in this skill — that's a separate batch job.

## When you add a new page

1. Confirm the URL doesn't already exist in `sitemap-0.xml` (use the local cached copy at `/tmp/sitemap-0.xml` or re-fetch).
2. Add the file at the correct `src/pages/...` location.
3. Update `reference/built-pages.md` (this skill's tracker).
4. The `@astrojs/sitemap` integration auto-includes the new URL on the next build.
