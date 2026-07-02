/**
 * Build-time content index for hreflang validation.
 *
 * For each locale × content-collection pair, loads the full set of slugs that
 * exist on disk. The hreflang alternate emitter uses this to skip locale links
 * that point at 404s.
 *
 * Background: src/utils/hreflang.ts originally emitted hreflang alternates for
 * every locale assuming the slug existed everywhere. In practice each locale
 * only mirrors ~3-7% of English content — so EN pages were emitting ~6,500
 * broken hreflang URLs sitewide. Google ignores broken hreflang clusters
 * (and may de-trust them), so we filter alternates against this index.
 *
 * Cache: module-level. First call loads all 36 collections once per
 * build/SSR; subsequent calls return the same map.
 */

import { getCollection } from 'astro:content';

export interface ContentIndex {
  // collectionName → Set of slugs that exist
  bySet: Map<string, Set<string>>;
}

let _cache: ContentIndex | null = null;
let _loadPromise: Promise<ContentIndex> | null = null;

const COLLECTIONS = [
  'blog', 'blog_de', 'blog_es', 'blog_fr', 'blog_it', 'blog_ptbr',
  'glossary', 'glossary_de', 'glossary_es', 'glossary_fr', 'glossary_it', 'glossary_ptbr',
  'best', 'best_de', 'best_es', 'best_fr', 'best_it', 'best_ptbr',
  'alternatives', 'alternatives_de', 'alternatives_es', 'alternatives_fr', 'alternatives_it', 'alternatives_ptbr',
  'reviews', 'reviews_de', 'reviews_es', 'reviews_fr', 'reviews_it', 'reviews_ptbr',
  'compare', 'compare_de', 'compare_es', 'compare_fr', 'compare_it', 'compare_ptbr',
] as const;

export async function getContentIndex(): Promise<ContentIndex> {
  if (_cache) return _cache;
  if (_loadPromise) return _loadPromise;

  _loadPromise = (async () => {
    const bySet = new Map<string, Set<string>>();
    for (const c of COLLECTIONS) {
      try {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const items = await getCollection(c as any);
        const slugs = new Set<string>();
        for (const item of items) {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          const slug = (item as any).data?.slug;
          if (typeof slug === 'string') slugs.add(slug);
        }
        bySet.set(c, slugs);
      } catch {
        bySet.set(c, new Set());
      }
    }
    _cache = { bySet };
    return _cache;
  })();

  return _loadPromise;
}

/**
 * Map a CONTENT_PREFIXES key (en/fr/es/pt-BR/it/de) + a base content type
 * (blog/glossary/best/alternatives/reviews/compare) to a collection name.
 */
export function collectionFor(locale: string, baseType: string): string {
  if (locale === 'en') return baseType;
  if (locale === 'pt-BR') return `${baseType}_ptbr`;
  return `${baseType}_${locale}`;
}
