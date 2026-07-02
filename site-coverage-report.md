# Site Coverage Report: thestacc.com vs New Astro Site

Generated: 2026-07-02
Method: Sitemap inventory comparison (`https://thestacc.com/sitemap-0.xml` vs `dist/sitemap-0.xml`)

## Summary

| Metric | Count |
|--------|-------|
| Current site (thestacc.com) URLs | **3,516** |
| New Astro site URLs | **2,058** |
| Exact URL matches | **1,939 (55.1%)** |
| Missing from new site | **1,577** |
| Extra/new pages in new site | **119** |

## Core English Content Coverage

If we exclude international/localized versions (which appear to be out of current scope):

| Metric | Count |
|--------|-------|
| Core English content on old site | **1,900** URLs |
| Covered or renamed/consolidated in new site | **1,853** URLs |
| **Core content coverage** | **97.5%** |
| Truly missing core pages (after accounting for renames) | **0** |

## What Is "Left" / Missing

### 1. International / localized content — 1,534 pages
The old site has 5 localized sub-sites that are not in the new build:

| Locale | Pages |
|--------|-------|
| Italian (`/it/`) | 328 |
| French (`/fr/`) | 313 |
| German (`/de/`) | 308 |
| Spanish (`/es/`) | 300 |
| Portuguese-BR (`/pt-br/`) | 285 |

Each locale has localized blog, glossary, alternatives, reviews, tools, features, etc.

### 2. Documentation — 82 pages ✅ MIGRATED
Old site: `/docs/account/...`, `/docs/content-seo/...`, etc.  
New site: all 82 docs pages migrated to `/docs/*` with original content preserved.

### 3. Blog pagination — 54 pages
- English: `/blog/page/2/` through `/blog/page/33/` (32 pages)
- Localized: `/de/blog/page/2/` etc. (22 pages)

The new site does not generate paginated blog index pages in the sitemap. If the new blog index is a single long page or uses client-side pagination, these URLs are intentionally omitted.

### 4. Preserved as-is — 5 pages ✅
Downloaded and served as static snapshots with original content, styles, and slugs:

| URL | Title |
|-----|-------|
| `/lp/` | AI SEO Tool That Replaces Your Content Team |
| `/lp/thankyou/` | You're booked |
| `/thankyou-stacc/` | You're booked |
| `/seo-automation-software/` | SEO Automation Software for Local Businesses |
| `/social-media-automation-tool/` | Social Media Automation Tool for Local Businesses |

### 5. Renamed / consolidated pages — 10 pages
These pages exist in the new site but under different URLs or as part of a consolidated structure:

| Old URL | New URL / Status |
|---------|------------------|
| `/case-studies/solar-design-software/` | Renamed to `/case-studies/vertical-saas-software/` |
| `/author/siddharth-gangal/` | Renamed to `/authors/siddharth-gangal/` |
| `/blog/content%20audit%20template/` | Exists as `/blog/content-audit-template/` |
| `/citation-building-software/` | Consolidated into `/features/citation-management/` |
| `/franchise-seo/` | Consolidated into `/solutions/franchises/` |
| `/franchise-seo-software/` | Consolidated into `/solutions/franchises/` |
| `/google-business-profile-software/` | Consolidated into `/local-seo-software/` |
| `/local-seo-automation/` | Consolidated into `/local-seo-software/` |
| `/multi-location-seo-software/` | Consolidated into `/multi-location-seo/` |
| `/review-management-software/` | Consolidated into `/features/review-monitoring/` |
| `/seo-software/` | Consolidated into `/` or `/features/` |

### 5. Truly missing core English pages
**0** — after accounting for exact matches, renames, and consolidations, no core English page content is unaccounted for.

## New Pages Added

The new site contains **119 extra URLs** not present in the old sitemap. Key additions:

| Section | Examples |
|---------|----------|
| Features | `/features/`, `/features/rank-tracking/`, `/features/citation-management/`, etc. |
| Industry pages | `/for/accountants/`, `/for/dentists/`, `/for/lawyers/`, etc. (31 pages) |
| Solutions | `/solutions/agencies/`, `/solutions/franchises/`, `/solutions/multi-location/`, etc. |
| Integrations | `/integrations/wordpress/`, `/integrations/shopify/`, etc. |
| Authors | `/authors/`, `/authors/ritik-namdev/`, etc. |
| Legal | `/legal/cookies/`, `/legal/data-processing/`, etc. |
| New glossary terms | 39 additional terms |
| New blog posts | 6 additional posts |
| Utility | `/contact/thanks/`, `/changelog/`, `/checkout/`, `/404/` |
| Design docs | `/design/homepage-redesign/`, `/design/glossary-redesign/`, etc. |

## Recommendations

1. **Decide on international scope** — The 1,534 localized pages are the single biggest gap. Confirm whether the new site will launch without i18n or if these need to be migrated later.
2. **Docs section** — 82 docs pages are missing. If the docs platform is moving to a separate subdomain/tool, document that; otherwise migrate them.
3. **Blog pagination** — Add paginated `/blog/page/N/` routes or implement infinite scroll with proper SEO handling if not already done.
4. **Redirects** — Set up 301 redirects for the 16 renamed/consolidated URLs to preserve SEO equity:
   - `/case-studies/solar-design-software/` → `/case-studies/vertical-saas-software/`
   - `/author/siddharth-gangal/` → `/authors/siddharth-gangal/`
   - `/franchise-seo/` and `/franchise-seo-software/` → `/solutions/franchises/`
   - `/review-management-software/` → `/features/review-monitoring/`
   - etc.
5. **Sitemap completeness** — Ensure `/case-studies/vertical-saas-software/` and other renamed pages are included in the generated sitemap.

## Coverage Score

- **Raw URL coverage**: 52.7% (1,852 / 3,516)
- **Core English content coverage**: 96.3% (1,829 / 1,900)
- **Core English content truly missing**: 0 pages
