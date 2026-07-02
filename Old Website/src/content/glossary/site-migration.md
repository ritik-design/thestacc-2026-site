---
term: "Site Migration"
slug: "site-migration"
definition: "Site migration is the process of moving a website from one environment to another, such as changing domains, switching CMS platforms, moving to HTTPS, or restructuring URLs, requiring careful planning to preserve SEO value."
category: "SEO"
difficulty: "Advanced"
keyword: "what is site migration"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "301-redirect"
  - "canonical-url"
  - "xml-sitemap"
  - "technical-seo"
  - "crawl-budget"
---

## What Is Site Migration?

Site migration is any significant change to a website's technology, structure, or location that can affect how search engines crawl, index, and rank the site. While "migration" sounds like a simple move, in SEO terms it is a high-risk operation that can destroy years of ranking progress if executed poorly.

**Types of site migration:**

| Migration Type | What Changes | Risk Level |
|---|---|---|
| Domain change | Moving from olddomain.com to newdomain.com | High |
| CMS change | Switching from WordPress to Shopify, etc. | High |
| Protocol change | HTTP to HTTPS | Medium |
| URL structure change | Rewriting URL patterns and slugs | High |
| Content restructuring | Merging, splitting, or reorganizing pages | Medium |
| Hosting change | Moving to a new server or CDN | Low |
| Design change | Major redesign with same URLs | Low-Medium |

## Why Site Migrations Fail

Studies show that 60-70% of site migrations result in some degree of organic traffic loss. The most common causes:

1. **Missing or incorrect 301 redirects.** Old URLs return 404 errors instead of redirecting to new URLs.
2. **Redirect chains.** Old URL → intermediate URL → new URL creates delays and loses equity.
3. **Changed content without preservation.** New CMS generates different title tags, meta descriptions, or page content.
4. **Lost internal links.** Navigation changes break internal link paths.
5. **Slow new site.** The new environment has worse performance than the old one.
6. **Blocked crawlers.** Robots.txt or noindex tags accidentally prevent indexing.
7. **No pre-migration benchmark.** Without baseline data, you cannot measure impact.

## The Site Migration Checklist

### Phase 1: Pre-Migration Planning (2-4 weeks before)

**1. Audit existing site**
- Crawl the entire site with Screaming Frog
- Export all URLs, titles, meta descriptions, and heading tags
- Document top 100 pages by traffic and backlinks
- Note current rankings for priority keywords
- Record Core Web Vitals scores

**2. Map old URLs to new URLs**

Create a redirect mapping spreadsheet:

| Old URL | New URL | Redirect Type | Status |
|---|---|---|---|
| /old-page/ | /new-page/ | 301 | Ready |
| /another-page/ | /another-page/ | None (URL unchanged) | Ready |

Every old URL that will change must have a mapped destination.

**3. Set up staging environment**
- Build the new site on a password-protected staging server
- Block staging from search engines with robots.txt
- Test all functionality before going live

**4. Prepare technical elements**
- SSL certificate installed and tested
- XML sitemap generated for new structure
- Robots.txt reviewed for new site
- Analytics and Search Console verified for new domain (if changing domains)

### Phase 2: Migration Day

**1. Implement redirects**
- Deploy 301 redirects from all old URLs to new URLs
- Test redirects in batches (start with top 100 pages)
- Verify redirects return 301 status, not 302 or meta refresh

**2. Update internal links**
- Change all internal links to point directly to new URLs (not through redirects)
- Update navigation menus, footer links, and sidebar links
- Fix broken internal links

**3. Go live**
- Point DNS to new server
- Remove password protection from staging
- Submit new XML sitemap to Google Search Console
- Update robots.txt to allow crawling

**4. Immediate post-launch checks**
- Crawl the site to find 404 errors
- Test critical user journeys (homepage → category → product → checkout)
- Verify analytics tracking works
- Check that search Console data is flowing

### Phase 3: Post-Migration Monitoring (2-8 weeks after)

**Week 1:**
- Daily crawl to catch 404s and redirect issues
- Monitor Search Console for crawl errors
- Check that priority pages are indexed

**Week 2-4:**
- Weekly traffic comparison (old vs. new)
- Monitor ranking changes for priority keywords
- Fix any missed redirects or broken links

**Week 4-8:**
- Compare full traffic recovery
- Analyze any persistent drops
- Plan additional optimization if needed

## 301 Redirect Best Practices

### Always Use 301, Never 302

A 301 redirect passes approximately 90-95% of link equity to the new URL. A 302 redirect tells search engines the move is temporary and should not pass equity. For permanent migrations, always use 301.

### Avoid Redirect Chains

A redirect chain happens when URL A redirects to URL B, which redirects to URL C. Each hop loses equity and slows crawling.

**Bad:** /old/ → /intermediate/ → /new/
**Good:** /old/ → /new/

Limit chains to 1-2 hops maximum.

### Redirect to the Most Relevant Page

Do not redirect every old page to the homepage. Redirect to the closest equivalent content.

**Bad:** /services/old-service/ → / (homepage)
**Good:** /services/old-service/ → /services/new-service/

If no equivalent exists, a 404 with helpful navigation is better than a misleading redirect.

## Common Migration Mistakes

**Mistake 1: Not budgeting enough time.**

Complex migrations need 4-8 weeks of planning. Rushing increases the risk of errors.

**Mistake 2: Changing too many things at once.**

If you change domains, CMS, design, and URL structure simultaneously, you cannot isolate what caused a traffic drop. Stagger major changes when possible.

**Mistake 3: Forgetting about backlinks.**

Contact owners of your most valuable backlinks and ask them to update the link to your new URL. Updated backlinks pass more authority than redirects.

**Mistake 4: Ignoring mobile performance.**

Test the new site extensively on mobile devices. New designs often look good on desktop but break on phones.

**Mistake 5: Not communicating the migration.**

Inform stakeholders, customers, and partners about the migration. Update social media profiles, email signatures, and business listings.

## Site Migration Tools

| Tool | Purpose | Cost |
|---|---|---|
| Screaming Frog | Crawl and audit URLs | Free (500 URLs) |
| Ahrefs | Backlink audit, redirect mapping | Paid |
| Semrush | Site audit, position tracking | Paid |
| Google Search Console | Monitor indexing and errors | Free |
| Analytics | Traffic comparison | Free |
| Redirect Path (Chrome) | Test redirect chains | Free |

## Related Terms

- [301 Redirect](/glossary/301-redirect/)
- [Canonical URL](/glossary/canonical-url/)
- [XML Sitemap](/glossary/xml-sitemap/)
- [Technical SEO](/glossary/technical-seo/)
- [Crawl Budget](/glossary/crawl-budget/)
