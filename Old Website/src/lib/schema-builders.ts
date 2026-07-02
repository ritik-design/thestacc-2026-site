// src/lib/schema-builders.ts
// Reusable JSON-LD schema builders for tool pages.

const ORG_NAME = 'theStacc';
const ORG_URL = 'https://thestacc.com';
const ORG_LOGO = 'https://thestacc.com/logo.webp';

export function buildOrganizationSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: ORG_NAME,
    url: ORG_URL,
    logo: ORG_LOGO,
  };
}

export function buildSoftwareApplicationSchema(opts: {
  name: string;
  description: string;
  url: string;
  image?: string;
  ratingValue?: number;
  ratingCount?: number;
}) {
  const schema: any = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: opts.name,
    description: opts.description,
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Web',
    url: opts.url,
    offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
    author: { '@type': 'Organization', name: ORG_NAME, url: ORG_URL },
  };
  if (opts.image) schema.image = opts.image;
  if (opts.ratingValue && opts.ratingCount) {
    schema.aggregateRating = {
      '@type': 'AggregateRating',
      ratingValue: opts.ratingValue,
      ratingCount: opts.ratingCount,
    };
  }
  return schema;
}

export function buildFAQSchema(faqs: Array<{ q: string; a: string }>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map(f => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    })),
  };
}

export function buildBreadcrumbSchema(items: Array<{ name: string; url: string }>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((it, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: it.name,
      item: it.url,
    })),
  };
}

export function buildWebPageWithSpeakable(opts: { url: string; cssSelector?: string[] }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    url: opts.url,
    speakable: {
      '@type': 'SpeakableSpecification',
      cssSelector: opts.cssSelector ?? ['.speakable'],
    },
  };
}
