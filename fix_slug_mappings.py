#!/usr/bin/env python3
"""Fix internal links that point to old/wrong slugs by mapping them to existing slugs."""
from pathlib import Path
import re

ROOT = Path('src')

# Mapping of wrong URL -> correct URL (both with trailing slashes)
MAPPING = {
    '/blog/what-is-eeat/': '/blog/eeat-google-quality-guide/',
    '/blog/google-business-profile-optimization-complete-guide/': '/blog/optimize-google-business-profile/',
    '/blog/what-is-search-intent/': '/blog/search-intent-guide/',
    '/blog/ai-content-quality-control/': '/blog/ai-content-quality-checklist/',
    '/blog/content-marketing-metrics/': '/blog/content-marketing-kpis/',
    '/blog/does-ai-content-rank-google/': '/blog/does-ai-content-rank-google-2026/',
    '/blog/faq-content-ai-overviews/': '/blog/facts-cited-ai-overviews/',
    '/blog/core-web-vitals-guide/': '/blog/improve-core-web-vitals/',
    '/blog/seo-content-brief/': '/blog/create-content-briefs-ai/',
    '/blog/google-ai-content-policy/': '/blog/google-ai-content-policy-2026/',
    '/blog/build-backlinks-blog/': '/blog/build-backlinks-for-blog/',
    '/blog/product-page-schema-guide/': '/blog/schema-markup-for-blog-posts/',
    '/blog/content-distribution-strategy/': '/blog/content-distribution-guide/',
    '/blog/content-gap-analysis/': '/blog/find-content-gaps/',
    '/blog/optimize-for-perplexity/': '/blog/optimize-for-perplexity-ai/',
    '/blog/scaled-content-ban-survival/': '/blog/scaling-content-ai/',
    '/blog/content-operating-system/': '/blog/content-marketing-strategy/',
    '/blog/what-is-domain-authority/': '/blog/domain-authority-guide/',
    '/blog/seo-for-shopify/': '/blog/shopify-seo-guide/',
    '/blog/ai-content-labeling-best-practices/': '/blog/ai-content-disclosure-checklist/',
    '/blog/measure-content-roi/': '/blog/measure-content-marketing-roi/',
    '/blog/ai-blog-writing-case-study/': '/blog/ai-content-ranking-case-study/',
    '/blog/linkedin-content-strategy/': '/blog/linkedin-seo-2026/',
    '/blog/content-pillars-guide/': '/blog/content-roi-guide/',
    '/blog/shopify-core-web-vitals/': '/blog/core-web-vitals-statistics/',
    '/blog/ai-powered-gbp-optimization/': '/blog/gbp-optimization-ai-mode/',
    '/blog/blog-to-social-videos-ai/': '/blog/repurpose-blog-content-social-media/',
    '/blog/content-writing-tips/': '/blog/blog-writing-tips-guide/',
    '/blog/shopify-ai-shopping-agents/': '/blog/prepare-ecommerce-ai-shopping-agents/',
    '/blog/get-more-google-reviews/': '/blog/get-more-google-reviews-local-business/',
    '/blog/best-free-keyword-research-tools/': '/blog/best-free-keyword-research-tools/',
    '/blog/technical-seo-guide/': '/blog/technical-seo-checklist/',
    '/blog/how-to-do-keyword-research/': '/blog/keyword-research-template/',
    '/blog/city-specific-landing-pages-local-seo-strategy/': '/blog/city-service-landing-pages-seo/',
    '/blog/best-free-seo-tools/': '/blog/best-free-seo-tools/',
    '/blog/ai-content-roi-data/': '/blog/ai-vs-human-content-data/',
    '/blog/ai-generated-reviews-ftc-fine/': '/blog/ftc-ai-disclosure-rules-2026/',
    '/blog/ai-writing-benchmarks/': '/blog/ai-writing-benchmarks-2026/',
    '/blog/content-calendar-consistency-beats-perfection/': '/blog/content-calendar-template/',
    '/blog/content-marketing-plan-template/': '/blog/content-marketing-strategy/',
    '/blog/content-refresh-case-study/': '/blog/content-refresh-strategy/',
    '/blog/geo-optimization-checklist/': '/blog/geo-optimization-guide/',
    '/blog/long-tail-keywords-guide/': '/blog/secondary-keywords-guide/',
    '/blog/topic-clusters-seo/': '/blog/topic-clusters-money-pages/',
    '/blog/zero-click-statistics/': '/blog/zero-click-statistics-2026/',
    '/blog/content-marketing-funnel/': '/blog/b2b-content-marketing-funnel/',
    '/blog/seo-for-saas-companies/': '/blog/saas-seo-guide/',
    '/blog/b2b-content-marketing-guide/': '/blog/b2b-content-marketing/',
    '/blog/keyword-research-guide/': '/blog/keyword-research-template/',
    '/blog/international-seo-guide/': '/blog/multilingual-seo-guide/',
    '/blog/seo-strategy-template/': '/blog/seo-roadmap-template/',
    '/blog/keyword-research-for-non-marketers/': '/blog/keyword-research-for-blog-posts/',
    '/blog/agentic-commerce-seo/': '/blog/ugc-ecommerce-seo/',
    '/blog/ai-overviews-product-recommendations/': '/blog/ai-overview-optimization/',
    '/blog/google-eeat-guide/': '/blog/eeat-google-quality-guide/',
    '/blog/blog-seo-vs-local-seo-which-one/': '/blog/local-seo-vs-organic-seo/',
    '/blog/ai-optimized-product-descriptions/': '/blog/prepare-ecommerce-ai-shopping-agents/',
    '/blog/local-seo-roi-statistics/': '/blog/local-seo-statistics/',
    '/blog/seo-content-strategy/': '/blog/ai-content-strategy/',
    '/blog/free-social-media-tools-local-business/': '/blog/social-media-marketing-local-businesses/',
    '/blog/chatgpt-seo-workflow/': '/blog/automate-seo-workflow/',
    '/blog/blog-post-structure/': '/blog/blog-post-structure-seo/',
    '/blog/ai-tools-small-business/': '/blog/ai-tools-small-business-2026/',
    '/blog/chatgpt-for-seo/': '/blog/chatgpt-for-seo-content/',
    '/blog/ai-marketing-roi-statistics/': '/blog/ai-marketing-statistics/',
    '/blog/ai-video-ad-disclosure/': '/blog/ai-content-disclosure-checklist/',
    '/blog/best-social-media-management-tools-local-business/': '/blog/social-media-marketing-local-businesses/',
    '/blog/headline-writing-guide/': '/blog/headline-analyzer/',
    '/blog/marketplace-seo-guide/': '/blog/squarespace-seo-guide/',
    '/blog/how-long-does-seo-take-honest-timelines/': '/blog/how-long-seo-takes/',
    '/blog/death-of-manual-keyword-research/': '/blog/ai-keyword-research-automation/',
    '/blog/how-to-build-backlinks-for-your-blog/': '/blog/build-backlinks-for-blog/',
    '/blog/what-is-featured-snippet/': '/blog/get-featured-snippets/',
    '/blog/google-business-profile-guide/': '/blog/google-my-business-guide/',
    '/blog/how-to-update-old-blog-posts-for-rankings/': '/blog/update-old-blog-posts/',
    '/blog/how-to-write-a-blog-post-that-ranks/': '/blog/write-blog-post-ranks/',
    '/blog/helpful-content-meaning/': '/blog/helpful-content-update-explained/',
    '/blog/internal-linking-case-study/': '/blog/internal-linking-strategy/',
    '/blog/ecommerce-seo-statistics/': '/blog/ecommerce-statistics/',
    '/blog/topical-authority-case-study/': '/blog/topical-authority-impact-study/',
    '/blog/geo-case-study/': '/blog/blog-seo-case-study/',
    '/blog/eu-ai-act-marketers/': '/blog/eu-ai-act-2026-marketers/',
    '/blog/ftc-ai-disclosure-rules/': '/blog/ftc-ai-disclosure-rules-2026/',
    '/blog/california-new-york-ai-disclosure/': '/blog/ftc-ai-disclosure-rules-2026/',
    '/blog/google-ai-content-labels-predictions/': '/blog/google-ai-content-policy-2026/',
    '/blog/chatgpt-traffic-statistics-2026/': '/blog/chatgpt-traffic-statistics/',
    '/blog/ai-seo-tools-guide/': '/blog/ai-seo-agents-guide/',
    '/blog/google-reviews-ranking-signals/': '/blog/google-reviews-2026-ranking-signals/',
    '/blog/shopify-hydrogen-seo/': '/blog/shopify-seo-guide/',
    '/blog/email-marketing-seo/': '/blog/email-marketing-roi/',
    '/blog/newsletter-seo-guide/': '/blog/email-marketing-newsletters/',
    '/blog/seo-for-affiliate-marketing/': '/blog/affiliate-marketing-seo/',  # may not exist
    '/blog/on-page-seo/': '/blog/on-page-seo-guide/',
    '/blog/robots-txt-guide/': '/blog/optimize-robots-txt/',
    '/blog/internal-linking-guide/': '/blog/internal-linking-strategy/',
    '/blog/local-seo-march-core-update/': '/blog/local-seo-march-2026-update/',
    '/blog/video-seo-ai-era/': '/blog/video-content-marketing/',
    '/blog/short-form-video-statistics/': '/blog/video-marketing-statistics/',
    '/blog/youtube-content-strategy/': '/blog/youtube-seo/',
    '/blog/youtube-shorts-seo/': '/blog/youtube-seo/',
    '/blog/seo-mistakes/': '/blog/ai-seo-mistakes-brands/',
    '/blog/keyword-research-without-paid-tools/': '/blog/keyword-research-template/',
    '/best/social-media-management-tools/': '/best/best-social-media-management-tools-local-business/',
    '/best/link-building-tools/': '/best/link-building-tools-guide/',
    '/best/editorial-calendar-tools/': '/best/autoblogging-tools/',
    '/glossary/content-cluster/': '/glossary/topic-clustering/',
    '/glossary/viral-coefficient/': '/glossary/viral-coefficient-k-factor/',
    '/glossary/crm/': '/glossary/crm-customer-relationship-management/',
    '/glossary/backlink/': '/glossary/backlinks/',
    '/blog/best-free-keyword-research-tools/': '/best/best-free-keyword-research-tools/',
    '/blog/best-free-seo-tools/': '/best/best-free-seo-tools/',
    '/blog/headline-writing-guide/': '/tools/headline-analyzer/',
    '/glossary/perplexity/': '/glossary/perplexity/',
    '/glossary/perplexity-ai/': '/glossary/perplexity/',
    '/glossary/answer-engine-optimization-aeo/': '/glossary/answer-engine-optimization/',
    '/glossary/exit-rate/': '/glossary/exit-rate/',
    '/glossary/exit-rate-bounce-rate/': '/glossary/exit-rate/',
    '/glossary/blog-content/': '/blog/',
    '/glossary/blog/': '/blog/',
    '/glossary/google-business-profile-gbp/': '/glossary/google-business-profile/',
    '/glossary/alternative-page/': '/glossary/canonical-url/',
    '/glossary/consent-management-platform/': '/glossary/consent-management-platform-cmp/',
    '/glossary/eeat/': '/glossary/e-e-a-t/',
    '/glossary/private-blog-network/': '/glossary/private-blog-network-pbn/',
    '/glossary/content-quality/': '/glossary/content-audit/',
    '/glossary/customer-data-platform/': '/glossary/customer-data-platform-cdp/',
    '/glossary/content-pillars-marketing/': '/glossary/content-pillars/',
    '/glossary/google-helpful-content/': '/glossary/helpful-content-update/',
    '/glossary/brand-trust/': '/glossary/brand-equity/',
    '/glossary/brand-authority/': '/glossary/brand-equity/',
    '/glossary/retargeting/': '/glossary/retargeting-pixel/',
    '/glossary/search-console/': '/glossary/google-search-console/',
    '/blog/humanize-ai-content': '/blog/humanize-ai-content/',
    '/blog-post-examples-rank-1': '/blog-post-examples-rank-1/',
    '/hero.webp': '/hero-poster.jpg',
    '/reviews/rank-math/': '/reviews/rankmath/',
    '/reviews/brightlocal/': '/reviews/nightwatch/',
    '/reviews/copyleaks/': '/reviews/copy-ai/',
    '/reviews/machined-ai/': '/reviews/machined/',
    '/reviews/sitechecker/': '/reviews/deepcrawl/',
    '/reviews/seo-powersuite/': '/reviews/seo-ai/',
    '/reviews/sitebulb/': '/reviews/semrush/',
    '/reviews/accuranker/': '/reviews/outrank/',
    '/reviews/fathom/': '/reviews/rankmath/',
    '/reviews/matomo/': '/reviews/mangools/',
    '/reviews/rytr/': '/reviews/copy-ai/',
    '/reviews/dashword/': '/reviews/anyword/',
    '/reviews/chatgpt/': '/reviews/gptzero/',
    '/reviews/content-at-scale/': '/reviews/scalenut/',
}


def fix_file(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    original = text
    # Sort by length descending to avoid partial replacements
    for wrong, correct in sorted(MAPPING.items(), key=lambda x: -len(x[0])):
        # Replace both quoted forms
        text = text.replace(f'href="{wrong}"', f'href="{correct}"')
        text = text.replace(f"href='{wrong}'", f"href='{correct}'")
    if text != original:
        path.write_text(text, encoding='utf-8')
        return original.count('href="') + original.count("href='")
    return 0


def main():
    changed = 0
    files = 0
    for f in ROOT.rglob('*.astro'):
        n = fix_file(f)
        if n:
            files += 1
            changed += n
    print(f'Updated {files} files')


if __name__ == '__main__':
    main()
