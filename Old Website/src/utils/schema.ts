/**
 * Shared Schema.org JSON-LD utilities for theStacc
 * Used across all page templates for consistent structured data
 */

export const SITE_URL = 'https://thestacc.com';
export const SITE_NAME = 'theStacc';
export const LOGO_URL = `${SITE_URL}/stacc-logo.png`;

/** Reusable Organization entity — referenced by @id across all pages */
export const organizationSchema = {
  '@type': 'Organization',
  '@id': `${SITE_URL}/#organization`,
  name: SITE_NAME,
  url: SITE_URL,
  logo: {
    '@type': 'ImageObject',
    url: LOGO_URL,
    width: 512,
    height: 512,
  },
  description: 'AI-powered SEO automation platform that researches, writes, and publishes blog content, manages Google Business Profiles, and automates social media distribution.',
  sameAs: [
    'https://www.linkedin.com/company/thestacc',
    'https://x.com/thestacc',
  ],
};

/** Reusable publisher reference (compact) */
export const publisherRef = {
  '@type': 'Organization',
  '@id': `${SITE_URL}/#organization`,
  name: SITE_NAME,
  url: SITE_URL,
  logo: { '@type': 'ImageObject', url: LOGO_URL },
};

/** Reusable author — Person entity for E-E-A-T signals */
export const authorRef = {
  '@type': 'Person',
  '@id': `${SITE_URL}/author/siddharth-gangal/#person`,
  name: 'Siddharth Gangal',
  url: `${SITE_URL}/author/siddharth-gangal/`,
};

/** WebSite entity — site identity and publisher linking */
export const websiteSchema = {
  '@type': 'WebSite',
  '@id': `${SITE_URL}/#website`,
  name: SITE_NAME,
  url: SITE_URL,
  publisher: { '@id': `${SITE_URL}/#organization` },
};

/** Build a BreadcrumbList from an array of {name, url} items */
export function buildBreadcrumbs(pageUrl: string, items: { name: string; url: string }[]) {
  return {
    '@type': 'BreadcrumbList',
    '@id': `${pageUrl}#breadcrumb`,
    itemListElement: items.map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

/** Build a Speakable specification targeting given CSS selectors */
export function buildSpeakable(selectors: string[]) {
  return {
    '@type': 'SpeakableSpecification',
    cssSelector: selectors,
  };
}

/** Build FAQPage schema from an array of {question, answer} items */
export function buildFAQSchema(faqs: { question: string; answer: string }[]) {
  if (!faqs.length) return null;
  return {
    '@type': 'FAQPage',
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.answer,
      },
    })),
  };
}

/** Resolve an image URL to absolute */
export function resolveImage(image: string | undefined): string {
  if (!image) return `${SITE_URL}/dashboard-preview.webp`;
  if (image.startsWith('http')) return image;
  return `${SITE_URL}${image}`;
}
