import { ROUTE_REGISTRY } from '../data/hreflang-registry.generated';

const SITE = 'https://thestacc.com';

export interface HreflangAlternate {
  lang: string;
  url: string;
}

type Lang = 'de' | 'es' | 'fr' | 'it' | 'pt-BR';
const ALL_LANGS: Lang[] = ['de', 'es', 'fr', 'it', 'pt-BR'];

// Locale path prefixes for each dynamic content type (slug is appended after prefix)
const CONTENT_PREFIXES: Array<{ baseType: string; prefixes: Record<string, string> }> = [
  { baseType: 'blog',         prefixes: { en: '/blog/', fr: '/fr/blog/', es: '/es/blog/', 'pt-BR': '/pt-br/blog/', it: '/it/blog/', de: '/de/blog/' } },
  { baseType: 'glossary',     prefixes: { en: '/glossary/', fr: '/fr/glossaire/', es: '/es/glosario/', 'pt-BR': '/pt-br/glossario/', it: '/it/glossario/', de: '/de/glossar/' } },
  { baseType: 'alternatives', prefixes: { en: '/alternatives/', fr: '/fr/alternatives/', es: '/es/alternativas/', 'pt-BR': '/pt-br/alternativas/', it: '/it/alternative/', de: '/de/alternativen/' } },
  { baseType: 'best',         prefixes: { en: '/best/', fr: '/fr/meilleures-listes/', es: '/es/mejor/', 'pt-BR': '/pt-br/melhores/', it: '/it/migliori/', de: '/de/best/' } },
  { baseType: 'reviews',      prefixes: { en: '/reviews/', fr: '/fr/avis/', es: '/es/resenas/', 'pt-BR': '/pt-br/avaliacoes/', it: '/it/recensioni/', de: '/de/bewertungen/' } },
  { baseType: 'compare',      prefixes: { en: '/compare/', fr: '/fr/vs/', es: '/es/vs/', 'pt-BR': '/pt-br/vs/', it: '/it/confronto/', de: '/de/vergleich/' } },
];

function matchContentRoute(pathname: string): { slug: string; prefixes: Record<string, string>; baseType: string } | null {
  for (const { baseType, prefixes } of CONTENT_PREFIXES) {
    for (const prefix of Object.values(prefixes)) {
      if (pathname.startsWith(prefix) && pathname.length > prefix.length) {
        return { slug: pathname.slice(prefix.length), prefixes, baseType };
      }
    }
  }
  return null;
}

// Reverse lookup: given any localized path, find its English canonical.
const REVERSE_LOOKUP: Map<string, string> = (() => {
  const m = new Map<string, string>();
  for (const [enPath, locales] of Object.entries(ROUTE_REGISTRY)) {
    for (const localized of Object.values(locales)) {
      if (localized) m.set(localized, enPath);
    }
  }
  return m;
})();

export function buildHreflangAlternates(
  pathname: string,
  contentIndex?: Map<string, Set<string>>,
): HreflangAlternate[] {
  // Dynamic content routes (blog, glossary, alternatives, best, reviews, compare)
  const content = matchContentRoute(pathname);
  if (content) {
    const { slug, prefixes, baseType } = content;
    const lookupSlug = slug.endsWith('/') ? slug.slice(0, -1) : slug;
    const exists = (locale: string): boolean => {
      if (!contentIndex) return true;
      const collectionName = locale === 'en'
        ? baseType
        : locale === 'pt-BR'
          ? `${baseType}_ptbr`
          : `${baseType}_${locale}`;
      const slugs = contentIndex.get(collectionName);
      return slugs ? slugs.has(lookupSlug) : false;
    };
    const alternates: HreflangAlternate[] = [];
    if (exists('en')) {
      alternates.push({ lang: 'x-default', url: `${SITE}${prefixes.en}${slug}` });
      alternates.push({ lang: 'en',        url: `${SITE}${prefixes.en}${slug}` });
    }
    if (exists('fr'))    alternates.push({ lang: 'fr',    url: `${SITE}${prefixes.fr}${slug}` });
    if (exists('es'))    alternates.push({ lang: 'es',    url: `${SITE}${prefixes.es}${slug}` });
    if (exists('pt-BR')) alternates.push({ lang: 'pt-BR', url: `${SITE}${prefixes['pt-BR']}${slug}` });
    if (exists('it'))    alternates.push({ lang: 'it',    url: `${SITE}${prefixes.it}${slug}` });
    if (exists('de'))    alternates.push({ lang: 'de',    url: `${SITE}${prefixes.de}${slug}` });
    return alternates;
  }

  // Static-page routes — look up via registry.
  const enPath = REVERSE_LOOKUP.get(pathname) ?? (ROUTE_REGISTRY[pathname] ? pathname : null);
  if (!enPath) return [];

  const locales = ROUTE_REGISTRY[enPath];
  const alternates: HreflangAlternate[] = [
    { lang: 'x-default', url: `${SITE}${enPath}` },
    { lang: 'en',        url: `${SITE}${enPath}` },
  ];
  for (const lang of ALL_LANGS) {
    const p = locales[lang];
    if (p) alternates.push({ lang, url: `${SITE}${p}` });
  }
  return alternates;
}

export function getLangFromPath(pathname: string): string {
  if (pathname.startsWith('/fr/') || pathname === '/fr') return 'fr';
  if (pathname.startsWith('/es/') || pathname === '/es') return 'es';
  if (pathname.startsWith('/pt-br/') || pathname === '/pt-br') return 'pt-BR';
  if (pathname.startsWith('/it/') || pathname === '/it') return 'it';
  if (pathname.startsWith('/de/') || pathname === '/de') return 'de';
  return 'en';
}
