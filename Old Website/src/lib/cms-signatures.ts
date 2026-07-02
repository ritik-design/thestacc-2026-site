/* ================================================================
   CMS & Tech Stack Detection Signatures
   ----------------------------------------------------------------
   Each signature describes how to identify a piece of technology
   from HTTP headers, cookies, HTML markup, meta tags, script srcs,
   or hostname patterns.

   Signal weights:
     - Headers/cookies/meta-generator are HIGH confidence (worth 3)
     - HTML markup patterns are MEDIUM (worth 2)
     - Script src / hostname / weak markup are LOW (worth 1)

   Final confidence:
     - >= 5 score → "high"
     - 3-4 score → "medium"
     - 1-2 score → "low"
   ================================================================ */

export type Category =
  | 'cms'
  | 'ecommerce'
  | 'framework'
  | 'webServer'
  | 'language'
  | 'cdn'
  | 'hosting'
  | 'analytics'
  | 'marketing'
  | 'pageBuilder'
  | 'uiLibrary'
  | 'library'
  | 'payment'
  | 'tagManager';

export interface HeaderSignal {
  name: string;
  pattern: RegExp;
  versionGroup?: number;
}

export interface CookieSignal {
  pattern: RegExp;
}

export interface HtmlSignal {
  pattern: RegExp;
  versionGroup?: number;
  weight?: number;
}

export interface ScriptSignal {
  pattern: RegExp;
  versionGroup?: number;
}

export interface DomainSignal {
  pattern: RegExp;
}

export interface Signature {
  name: string;
  category: Category;
  icon?: string;
  url?: string;
  description?: string;
  /** Minimum total score before we report it (default 1). Use 2+ for noisy techs. */
  minScore?: number;
  signals: {
    headers?: HeaderSignal[];
    cookies?: CookieSignal[];
    metaGenerator?: { pattern: RegExp; versionGroup?: number };
    html?: HtmlSignal[];
    scriptSrc?: ScriptSignal[];
    domain?: DomainSignal;
  };
  /** If this is detected, also add these (and inherit confidence). */
  implies?: string[];
  /** If any of these are also detected, drop this one. */
  excludedBy?: string[];
}

export const CATEGORY_META: Record<Category, { label: string; order: number; color: string }> = {
  cms: { label: 'CMS', order: 1, color: '#4f39f6' },
  ecommerce: { label: 'E-commerce', order: 2, color: '#0ea5e9' },
  framework: { label: 'Framework', order: 3, color: '#a855f7' },
  pageBuilder: { label: 'Page Builder', order: 4, color: '#ec4899' },
  webServer: { label: 'Web Server', order: 5, color: '#10b981' },
  language: { label: 'Language', order: 6, color: '#f59e0b' },
  cdn: { label: 'CDN', order: 7, color: '#06b6d4' },
  hosting: { label: 'Hosting', order: 8, color: '#8b5cf6' },
  analytics: { label: 'Analytics', order: 9, color: '#ef4444' },
  tagManager: { label: 'Tag Manager', order: 10, color: '#f97316' },
  marketing: { label: 'Marketing', order: 11, color: '#eab308' },
  payment: { label: 'Payment', order: 12, color: '#84cc16' },
  uiLibrary: { label: 'UI Library', order: 13, color: '#3b82f6' },
  library: { label: 'JS Library', order: 14, color: '#64748b' },
};

export const SIGNATURES: Signature[] = [
  /* ============================================================
     CMS — Content Management Systems
     ============================================================ */
  {
    name: 'WordPress',
    category: 'cms',
    icon: 'wordpress',
    url: 'https://wordpress.org',
    description: 'The most popular CMS in the world. Open source, PHP-based.',
    signals: {
      headers: [
        { name: 'x-pingback', pattern: /xmlrpc\.php/i },
        { name: 'link', pattern: /wp-json/i },
      ],
      metaGenerator: { pattern: /WordPress\s*([\d.]+)?/i, versionGroup: 1 },
      cookies: [
        { pattern: /wordpress_logged_in/i },
        { pattern: /wp-settings-/i },
        { pattern: /wp_woocommerce_session/i },
      ],
      html: [
        { pattern: /\/wp-content\//i, weight: 2 },
        { pattern: /\/wp-includes\//i, weight: 2 },
        { pattern: /<link[^>]+rel=["']https:\/\/api\.w\.org\//i, weight: 2 },
      ],
    },
    implies: ['PHP', 'MySQL'],
  },
  {
    name: 'Drupal',
    category: 'cms',
    icon: 'drupal',
    url: 'https://www.drupal.org',
    description: 'Enterprise open-source CMS. PHP-based, highly customizable.',
    signals: {
      headers: [
        { name: 'x-drupal-cache', pattern: /.+/ },
        { name: 'x-drupal-dynamic-cache', pattern: /.+/ },
        { name: 'x-generator', pattern: /Drupal\s*([\d.]+)?/i, versionGroup: 1 },
      ],
      metaGenerator: { pattern: /Drupal\s*([\d.]+)?/i, versionGroup: 1 },
      html: [
        { pattern: /\/sites\/default\/files\//i, weight: 2 },
        { pattern: /\/sites\/all\/(themes|modules)\//i, weight: 2 },
        { pattern: /Drupal\.settings/i, weight: 2 },
      ],
    },
    implies: ['PHP'],
  },
  {
    name: 'Joomla',
    category: 'cms',
    icon: 'joomla',
    url: 'https://www.joomla.org',
    description: 'Open-source PHP CMS. Mid-market alternative to WordPress.',
    signals: {
      metaGenerator: { pattern: /Joomla!?\s*-?\s*([\d.]+)?/i, versionGroup: 1 },
      html: [
        { pattern: /\/media\/jui\//i, weight: 2 },
        { pattern: /\/components\/com_/i, weight: 2 },
        { pattern: /\/templates\/[a-z0-9_-]+\/css\//i, weight: 1 },
      ],
      cookies: [{ pattern: /^[a-f0-9]{32}=/i }],
    },
    implies: ['PHP'],
  },
  {
    name: 'Ghost',
    category: 'cms',
    icon: 'ghost',
    url: 'https://ghost.org',
    description: 'Modern publishing platform built on Node.js. Popular for blogs.',
    signals: {
      metaGenerator: { pattern: /Ghost\s*([\d.]+)?/i, versionGroup: 1 },
      html: [
        { pattern: /<link[^>]+href=["'][^"']*\/ghost\//i, weight: 2 },
        { pattern: /<script[^>]+src=["'][^"']*ghost\.io/i, weight: 2 },
      ],
      headers: [{ name: 'x-ghost-cache-status', pattern: /.+/ }],
    },
    implies: ['Node.js'],
  },
  {
    name: 'TYPO3',
    category: 'cms',
    icon: 'typo3',
    url: 'https://typo3.org',
    description: 'Enterprise open-source CMS popular in Europe.',
    signals: {
      metaGenerator: { pattern: /TYPO3\s*([\d.]+)?/i, versionGroup: 1 },
      html: [
        { pattern: /\/typo3conf\//i, weight: 2 },
        { pattern: /\/typo3temp\//i, weight: 2 },
        { pattern: /\/fileadmin\//i, weight: 1 },
      ],
    },
    implies: ['PHP'],
  },
  {
    name: 'Wix',
    category: 'cms',
    icon: 'wix',
    url: 'https://www.wix.com',
    description: 'Drag-and-drop website builder. Hosted SaaS.',
    signals: {
      domain: { pattern: /\.wixsite\.com$|\.wix\.com$/i },
      headers: [{ name: 'x-wix-request-id', pattern: /.+/ }],
      html: [
        { pattern: /static\.parastorage\.com/i, weight: 2 },
        { pattern: /<meta[^>]+name=["']generator["'][^>]+content=["']Wix\.com/i, weight: 3 },
        { pattern: /window\.wixBiSession/i, weight: 2 },
      ],
    },
  },
  {
    name: 'Squarespace',
    category: 'cms',
    icon: 'squarespace',
    url: 'https://www.squarespace.com',
    description: 'All-in-one website builder + e-commerce.',
    signals: {
      domain: { pattern: /\.squarespace\.com$/i },
      headers: [{ name: 'server', pattern: /Squarespace/i }],
      html: [
        { pattern: /static1\.squarespace\.com/i, weight: 2 },
        { pattern: /<meta[^>]+name=["']generator["'][^>]+content=["']Squarespace/i, weight: 3 },
        { pattern: /Static\.SQUARESPACE_CONTEXT/i, weight: 2 },
      ],
    },
  },
  {
    name: 'Webflow',
    category: 'cms',
    icon: 'webflow',
    url: 'https://webflow.com',
    description: 'Visual web design platform with hosting.',
    signals: {
      domain: { pattern: /\.webflow\.io$/i },
      metaGenerator: { pattern: /Webflow/i },
      html: [
        { pattern: /webflow\.com\/api\/site\//i, weight: 2 },
        { pattern: /data-wf-site=/i, weight: 3 },
        { pattern: /assets\.website-files\.com/i, weight: 2 },
      ],
    },
  },
  {
    name: 'Weebly',
    category: 'cms',
    icon: 'weebly',
    url: 'https://www.weebly.com',
    description: 'Website builder owned by Square.',
    signals: {
      domain: { pattern: /\.weebly\.com$|\.weeblysite\.com$/i },
      html: [
        { pattern: /cdn[12]?\.editmysite\.com/i, weight: 2 },
        { pattern: /weebly\.com\/r\/EXTERNAL/i, weight: 2 },
        { pattern: /<meta[^>]+name=["']generator["'][^>]+content=["']Weebly/i, weight: 3 },
      ],
    },
  },
  {
    name: 'Duda',
    category: 'cms',
    icon: 'duda',
    url: 'https://www.duda.co',
    description: 'White-label website builder for agencies.',
    signals: {
      domain: { pattern: /\.dudaone\.com$|\.duda\.co$/i },
      html: [
        { pattern: /irp(-cdn)?\.multiscreensite\.com/i, weight: 2 },
        { pattern: /lirp\.cdn-website\.com/i, weight: 2 },
        { pattern: /window\.DM\.[a-z]/i, weight: 2 },
      ],
    },
  },
  {
    name: 'Concrete CMS',
    category: 'cms',
    icon: 'concrete',
    url: 'https://www.concretecms.com',
    description: 'Open source PHP CMS, formerly concrete5.',
    signals: {
      metaGenerator: { pattern: /concrete\s*5|concrete\s*cms\s*([\d.]+)?/i, versionGroup: 1 },
      html: [{ pattern: /\/concrete\/(blocks|themes|js)\//i, weight: 2 }],
    },
    implies: ['PHP'],
  },
  {
    name: 'Hubspot CMS',
    category: 'cms',
    icon: 'hubspot',
    url: 'https://www.hubspot.com/products/cms',
    description: 'HubSpot CMS Hub for marketing-focused sites.',
    signals: {
      headers: [{ name: 'x-hs-cf-cache-status', pattern: /.+/ }],
      html: [
        { pattern: /js\.hs-scripts\.com/i, weight: 2 },
        { pattern: /js\.hsforms\.net/i, weight: 2 },
        { pattern: /<meta[^>]+name=["']generator["'][^>]+content=["']HubSpot/i, weight: 3 },
        { pattern: /hubspotusercontent/i, weight: 2 },
      ],
    },
  },

  /* ============================================================
     E-commerce
     ============================================================ */
  {
    name: 'Shopify',
    category: 'ecommerce',
    icon: 'shopify',
    url: 'https://www.shopify.com',
    description: 'Leading hosted e-commerce platform.',
    signals: {
      domain: { pattern: /\.myshopify\.com$/i },
      headers: [
        { name: 'x-shopify-stage', pattern: /.+/ },
        { name: 'x-shopid', pattern: /.+/ },
        { name: 'x-shardid', pattern: /.+/ },
        { name: 'powered-by', pattern: /Shopify/i },
      ],
      cookies: [{ pattern: /_shopify_/i }, { pattern: /_secure_session_id/i }],
      html: [
        { pattern: /cdn\.shopify\.com/i, weight: 3 },
        { pattern: /Shopify\.theme/i, weight: 2 },
        { pattern: /window\.Shopify\s*=/i, weight: 2 },
      ],
    },
  },
  {
    name: 'WooCommerce',
    category: 'ecommerce',
    icon: 'woocommerce',
    url: 'https://woocommerce.com',
    description: 'WordPress-based e-commerce plugin.',
    signals: {
      metaGenerator: { pattern: /WooCommerce\s*([\d.]+)?/i, versionGroup: 1 },
      cookies: [{ pattern: /woocommerce_/i }, { pattern: /wp_woocommerce_session/i }],
      html: [
        { pattern: /\/wp-content\/plugins\/woocommerce\//i, weight: 3 },
        { pattern: /class=["'][^"']*woocommerce[^"']*["']/i, weight: 2 },
      ],
    },
    implies: ['WordPress', 'PHP'],
  },
  {
    name: 'Magento',
    category: 'ecommerce',
    icon: 'magento',
    url: 'https://magento.com',
    description: 'Open source Adobe-owned e-commerce platform.',
    signals: {
      headers: [{ name: 'x-magento-cache-debug', pattern: /.+/ }],
      cookies: [{ pattern: /^frontend=/i }, { pattern: /X-Magento-Vary/i }],
      html: [
        { pattern: /\/skin\/frontend\//i, weight: 2 },
        { pattern: /Mage\.Cookies/i, weight: 2 },
        { pattern: /\/static\/version\d+\/frontend\//i, weight: 2 },
      ],
    },
    implies: ['PHP'],
  },
  {
    name: 'BigCommerce',
    category: 'ecommerce',
    icon: 'bigcommerce',
    url: 'https://www.bigcommerce.com',
    description: 'Hosted e-commerce platform for SMBs and mid-market.',
    signals: {
      domain: { pattern: /\.mybigcommerce\.com$/i },
      headers: [{ name: 'x-bc-apache-cache', pattern: /.+/ }],
      html: [
        { pattern: /cdn[12]?\.bigcommerce\.com/i, weight: 2 },
        { pattern: /window\.BCData/i, weight: 2 },
      ],
    },
  },
  {
    name: 'PrestaShop',
    category: 'ecommerce',
    icon: 'prestashop',
    url: 'https://www.prestashop.com',
    description: 'Open source PHP e-commerce, popular in Europe.',
    signals: {
      headers: [{ name: 'powered-by', pattern: /PrestaShop/i }],
      metaGenerator: { pattern: /PrestaShop/i },
      cookies: [{ pattern: /^PrestaShop/i }],
      html: [
        { pattern: /\/themes\/[^\/]+\/assets\//i, weight: 1 },
        { pattern: /var\s+prestashop\s*=/i, weight: 2 },
      ],
    },
    implies: ['PHP'],
  },
  {
    name: 'OpenCart',
    category: 'ecommerce',
    icon: 'opencart',
    url: 'https://www.opencart.com',
    description: 'Open source PHP e-commerce platform.',
    signals: {
      cookies: [{ pattern: /OCSESSID/i }],
      html: [
        { pattern: /catalog\/view\/theme/i, weight: 2 },
        { pattern: /index\.php\?route=/i, weight: 2 },
      ],
    },
    implies: ['PHP'],
  },
  {
    name: 'Square Online',
    category: 'ecommerce',
    icon: 'square',
    url: 'https://squareup.com/online-store',
    description: 'Square\'s e-commerce builder, runs on Weebly engine.',
    signals: {
      domain: { pattern: /\.square\.site$/i },
      html: [{ pattern: /squareup\.com/i, weight: 2 }],
    },
  },

  /* ============================================================
     Modern frameworks / SSGs
     ============================================================ */
  {
    name: 'Next.js',
    category: 'framework',
    icon: 'nextjs',
    url: 'https://nextjs.org',
    description: 'Production React framework by Vercel.',
    signals: {
      headers: [{ name: 'x-nextjs-cache', pattern: /.+/ }, { name: 'x-nextjs-prerender', pattern: /.+/ }],
      html: [
        { pattern: /\/_next\/static\//i, weight: 3 },
        { pattern: /__NEXT_DATA__/i, weight: 3 },
      ],
    },
    implies: ['React'],
  },
  {
    name: 'Nuxt',
    category: 'framework',
    icon: 'nuxt',
    url: 'https://nuxt.com',
    description: 'Vue.js framework for SSR and static sites.',
    signals: {
      headers: [{ name: 'x-nuxt-version', pattern: /([\d.]+)/, versionGroup: 1 }],
      html: [
        { pattern: /__NUXT__/i, weight: 3 },
        { pattern: /\/_nuxt\//i, weight: 2 },
        { pattern: /id=["']__nuxt["']/i, weight: 2 },
      ],
    },
    implies: ['Vue.js'],
  },
  {
    name: 'Gatsby',
    category: 'framework',
    icon: 'gatsby',
    url: 'https://www.gatsbyjs.com',
    description: 'React-based static site generator.',
    signals: {
      metaGenerator: { pattern: /Gatsby\s*([\d.]+)?/i, versionGroup: 1 },
      html: [
        { pattern: /id=["']___gatsby["']/i, weight: 3 },
        { pattern: /__GATSBY/i, weight: 2 },
        { pattern: /window\.___loader/i, weight: 2 },
      ],
    },
    implies: ['React'],
  },
  {
    name: 'Astro',
    category: 'framework',
    icon: 'astro',
    url: 'https://astro.build',
    description: 'Modern static site framework with islands architecture.',
    signals: {
      metaGenerator: { pattern: /Astro\s*v?([\d.]+)?/i, versionGroup: 1 },
      headers: [{ name: 'x-astro-prerender', pattern: /.+/ }],
      html: [
        { pattern: /data-astro-cid-/i, weight: 3 },
        { pattern: /\/_astro\//i, weight: 2 },
      ],
    },
  },
  {
    name: 'Hugo',
    category: 'framework',
    icon: 'hugo',
    url: 'https://gohugo.io',
    description: 'Fast static site generator written in Go.',
    signals: {
      metaGenerator: { pattern: /Hugo\s*([\d.]+)?/i, versionGroup: 1 },
    },
  },
  {
    name: 'Jekyll',
    category: 'framework',
    icon: 'jekyll',
    url: 'https://jekyllrb.com',
    description: 'Ruby-based static site generator. Powers GitHub Pages.',
    signals: {
      metaGenerator: { pattern: /Jekyll\s*v?([\d.]+)?/i, versionGroup: 1 },
    },
  },
  {
    name: 'Eleventy',
    category: 'framework',
    icon: 'eleventy',
    url: 'https://www.11ty.dev',
    description: 'Simpler static site generator. JavaScript-based.',
    signals: {
      metaGenerator: { pattern: /Eleventy\s*v?([\d.]+)?/i, versionGroup: 1 },
    },
  },
  {
    name: 'Docusaurus',
    category: 'framework',
    icon: 'docusaurus',
    url: 'https://docusaurus.io',
    description: 'React-based documentation site generator.',
    signals: {
      metaGenerator: { pattern: /Docusaurus\s*v?([\d.]+)?/i, versionGroup: 1 },
      html: [
        { pattern: /id=["']__docusaurus["']/i, weight: 3 },
        { pattern: /docusaurus_skipToContent_fallback/i, weight: 2 },
      ],
    },
    implies: ['React'],
  },
  {
    name: 'Remix',
    category: 'framework',
    icon: 'remix',
    url: 'https://remix.run',
    description: 'React framework focused on web standards.',
    signals: {
      html: [
        { pattern: /__remixContext/i, weight: 3 },
        { pattern: /window\.__remixManifest/i, weight: 3 },
      ],
    },
    implies: ['React'],
  },
  {
    name: 'SvelteKit',
    category: 'framework',
    icon: 'sveltekit',
    url: 'https://kit.svelte.dev',
    description: 'Full-stack framework for Svelte.',
    signals: {
      html: [
        { pattern: /__sveltekit_/i, weight: 3 },
        { pattern: /\/_app\/immutable\//i, weight: 2 },
      ],
    },
    implies: ['Svelte'],
  },
  {
    name: 'Typesetter',
    category: 'cms',
    icon: 'typesetter',
    url: 'https://www.typesettercms.com',
    description: 'PHP flat-file CMS.',
    signals: {
      html: [{ pattern: /Powered by Typesetter/i, weight: 3 }],
    },
    implies: ['PHP'],
  },

  /* ============================================================
     JS frameworks
     ============================================================ */
  {
    name: 'React',
    category: 'framework',
    icon: 'react',
    url: 'https://react.dev',
    description: 'Most popular JavaScript UI library.',
    signals: {
      html: [
        { pattern: /data-reactroot|data-reactid/i, weight: 2 },
        { pattern: /react-dom@([\d.]+)/i, versionGroup: 1, weight: 2 },
        { pattern: /\.production\.min\.js/i, weight: 0 },
      ],
      scriptSrc: [{ pattern: /react(?:-dom)?[.@-]([\d.]+)/i, versionGroup: 1 }],
    },
  },
  {
    name: 'Vue.js',
    category: 'framework',
    icon: 'vue',
    url: 'https://vuejs.org',
    description: 'Progressive JavaScript framework.',
    signals: {
      html: [
        { pattern: /data-v-[a-f0-9]{8}/i, weight: 2 },
        { pattern: /vue(?:\.runtime)?[.@-]([\d.]+)/i, versionGroup: 1, weight: 2 },
      ],
      scriptSrc: [{ pattern: /vue(?:\.runtime)?[.@-]([\d.]+)/i, versionGroup: 1 }],
    },
  },
  {
    name: 'Angular',
    category: 'framework',
    icon: 'angular',
    url: 'https://angular.dev',
    description: 'Google\'s TypeScript-based framework.',
    signals: {
      html: [
        { pattern: /ng-version=["']([\d.]+)/i, versionGroup: 1, weight: 3 },
        { pattern: /ng-app=/i, weight: 2 },
      ],
    },
  },
  {
    name: 'Svelte',
    category: 'framework',
    icon: 'svelte',
    url: 'https://svelte.dev',
    description: 'Compile-time reactive framework.',
    signals: {
      html: [{ pattern: /class=["']svelte-[a-z0-9]{6,}["']/i, weight: 2 }],
    },
  },
  {
    name: 'Alpine.js',
    category: 'framework',
    icon: 'alpine',
    url: 'https://alpinejs.dev',
    description: 'Minimal reactive framework for HTML.',
    signals: {
      html: [
        { pattern: /\bx-data\s*=/i, weight: 2 },
        { pattern: /alpine\.js/i, weight: 2 },
      ],
    },
  },
  {
    name: 'jQuery',
    category: 'library',
    icon: 'jquery',
    url: 'https://jquery.com',
    description: 'JavaScript library that simplifies HTML DOM manipulation.',
    signals: {
      scriptSrc: [{ pattern: /jquery[.-]?([\d.]+)?\.?(?:min|slim)?\.js/i, versionGroup: 1 }],
      html: [{ pattern: /jQuery\s+v?([\d.]+)/i, versionGroup: 1, weight: 1 }],
    },
  },

  /* ============================================================
     Web servers
     ============================================================ */
  {
    name: 'Nginx',
    category: 'webServer',
    icon: 'nginx',
    url: 'https://nginx.org',
    description: 'High-performance HTTP server and reverse proxy.',
    signals: {
      headers: [{ name: 'server', pattern: /nginx[\/\s]?([\d.]+)?/i, versionGroup: 1 }],
    },
  },
  {
    name: 'Apache',
    category: 'webServer',
    icon: 'apache',
    url: 'https://httpd.apache.org',
    description: 'Apache HTTP Server, the most widely used.',
    signals: {
      headers: [{ name: 'server', pattern: /Apache[\/\s]?([\d.]+)?/i, versionGroup: 1 }],
    },
  },
  {
    name: 'Microsoft IIS',
    category: 'webServer',
    icon: 'iis',
    url: 'https://www.iis.net',
    description: 'Microsoft\'s web server for Windows.',
    signals: {
      headers: [
        { name: 'server', pattern: /Microsoft-IIS[\/\s]?([\d.]+)?/i, versionGroup: 1 },
        { name: 'x-powered-by', pattern: /ASP\.NET/i },
      ],
    },
  },
  {
    name: 'LiteSpeed',
    category: 'webServer',
    icon: 'litespeed',
    url: 'https://www.litespeedtech.com',
    description: 'High-performance Apache replacement.',
    signals: {
      headers: [{ name: 'server', pattern: /LiteSpeed/i }, { name: 'x-litespeed-cache', pattern: /.+/ }],
    },
  },
  {
    name: 'Caddy',
    category: 'webServer',
    icon: 'caddy',
    url: 'https://caddyserver.com',
    description: 'Modern web server with automatic HTTPS.',
    signals: {
      headers: [{ name: 'server', pattern: /Caddy/i }],
    },
  },

  /* ============================================================
     Programming languages
     ============================================================ */
  {
    name: 'PHP',
    category: 'language',
    icon: 'php',
    url: 'https://www.php.net',
    description: 'Server-side scripting language.',
    signals: {
      headers: [{ name: 'x-powered-by', pattern: /PHP[\/\s]?([\d.]+)?/i, versionGroup: 1 }],
      cookies: [{ pattern: /PHPSESSID/i }],
    },
  },
  {
    name: 'Node.js',
    category: 'language',
    icon: 'nodejs',
    url: 'https://nodejs.org',
    description: 'JavaScript runtime for server-side.',
    signals: {
      headers: [{ name: 'x-powered-by', pattern: /Express|Node\.js/i }],
    },
  },
  {
    name: 'Ruby',
    category: 'language',
    icon: 'ruby',
    url: 'https://www.ruby-lang.org',
    description: 'Dynamic, object-oriented programming language.',
    signals: {
      headers: [{ name: 'x-powered-by', pattern: /Ruby|Rails/i }, { name: 'server', pattern: /Phusion Passenger/i }],
    },
  },
  {
    name: 'Python',
    category: 'language',
    icon: 'python',
    url: 'https://www.python.org',
    description: 'High-level programming language.',
    signals: {
      headers: [{ name: 'server', pattern: /gunicorn|uvicorn|werkzeug/i }, { name: 'x-powered-by', pattern: /Python|Django|Flask/i }],
    },
  },
  {
    name: 'ASP.NET',
    category: 'language',
    icon: 'aspnet',
    url: 'https://dotnet.microsoft.com',
    description: 'Microsoft\'s web framework.',
    signals: {
      headers: [{ name: 'x-aspnet-version', pattern: /([\d.]+)/, versionGroup: 1 }, { name: 'x-powered-by', pattern: /ASP\.NET/i }],
      cookies: [{ pattern: /ASP\.NET_SessionId/i }],
    },
  },
  {
    name: 'Java',
    category: 'language',
    icon: 'java',
    url: 'https://www.java.com',
    description: 'Enterprise-class programming language.',
    signals: {
      headers: [{ name: 'server', pattern: /Tomcat|Jetty|JBoss/i }],
      cookies: [{ pattern: /JSESSIONID/i }],
    },
  },

  /* ============================================================
     CDNs
     ============================================================ */
  {
    name: 'Cloudflare',
    category: 'cdn',
    icon: 'cloudflare',
    url: 'https://www.cloudflare.com',
    description: 'Global CDN, DDoS protection, and edge platform.',
    signals: {
      headers: [
        { name: 'cf-ray', pattern: /.+/ },
        { name: 'cf-cache-status', pattern: /.+/ },
        { name: 'server', pattern: /cloudflare/i },
      ],
      cookies: [{ pattern: /__cfduid|__cf_bm/i }],
    },
  },
  {
    name: 'Fastly',
    category: 'cdn',
    icon: 'fastly',
    url: 'https://www.fastly.com',
    description: 'Edge cloud platform.',
    signals: {
      headers: [
        { name: 'x-served-by', pattern: /cache-[a-z0-9]+/i },
        { name: 'x-fastly-request-id', pattern: /.+/ },
        { name: 'fastly-restarts', pattern: /.+/ },
        { name: 'x-cache', pattern: /Fastly/i },
      ],
    },
  },
  {
    name: 'Akamai',
    category: 'cdn',
    icon: 'akamai',
    url: 'https://www.akamai.com',
    description: 'Enterprise CDN and security platform.',
    signals: {
      headers: [
        { name: 'x-akamai-transformed', pattern: /.+/ },
        { name: 'akamai-grn', pattern: /.+/ },
        { name: 'server', pattern: /AkamaiGHost/i },
      ],
    },
  },
  {
    name: 'AWS CloudFront',
    category: 'cdn',
    icon: 'cloudfront',
    url: 'https://aws.amazon.com/cloudfront',
    description: 'Amazon Web Services CDN.',
    signals: {
      headers: [
        { name: 'x-amz-cf-id', pattern: /.+/ },
        { name: 'via', pattern: /CloudFront/i },
        { name: 'x-amz-cf-pop', pattern: /.+/ },
      ],
    },
  },
  {
    name: 'Bunny CDN',
    category: 'cdn',
    icon: 'bunny',
    url: 'https://bunny.net',
    description: 'Affordable, high-performance CDN.',
    signals: {
      headers: [{ name: 'cdn', pattern: /BunnyCDN/i }, { name: 'server', pattern: /BunnyCDN/i }],
      html: [{ pattern: /b-cdn\.net/i, weight: 1 }],
    },
  },
  {
    name: 'KeyCDN',
    category: 'cdn',
    icon: 'keycdn',
    url: 'https://www.keycdn.com',
    description: 'High-performance CDN.',
    signals: {
      headers: [{ name: 'server', pattern: /keycdn-engine/i }],
    },
  },
  {
    name: 'Google Cloud CDN',
    category: 'cdn',
    icon: 'gcp',
    url: 'https://cloud.google.com/cdn',
    description: 'Google Cloud\'s CDN.',
    signals: {
      headers: [{ name: 'via', pattern: /google/i }, { name: 'server', pattern: /^gws$/i }],
    },
  },

  /* ============================================================
     Hosting platforms
     ============================================================ */
  {
    name: 'Vercel',
    category: 'hosting',
    icon: 'vercel',
    url: 'https://vercel.com',
    description: 'Frontend platform from the creators of Next.js.',
    signals: {
      domain: { pattern: /\.vercel\.app$/i },
      headers: [
        { name: 'server', pattern: /Vercel/i },
        { name: 'x-vercel-id', pattern: /.+/ },
        { name: 'x-vercel-cache', pattern: /.+/ },
      ],
    },
  },
  {
    name: 'Netlify',
    category: 'hosting',
    icon: 'netlify',
    url: 'https://www.netlify.com',
    description: 'Modern web platform for Jamstack sites.',
    signals: {
      domain: { pattern: /\.netlify\.app$|\.netlify\.com$/i },
      headers: [{ name: 'server', pattern: /Netlify/i }, { name: 'x-nf-request-id', pattern: /.+/ }],
    },
  },
  {
    name: 'Cloudflare Pages',
    category: 'hosting',
    icon: 'cloudflare',
    url: 'https://pages.cloudflare.com',
    description: 'JAMstack hosting from Cloudflare.',
    signals: {
      domain: { pattern: /\.pages\.dev$/i },
    },
  },
  {
    name: 'GitHub Pages',
    category: 'hosting',
    icon: 'github',
    url: 'https://pages.github.com',
    description: 'Free static hosting from GitHub.',
    signals: {
      domain: { pattern: /\.github\.io$/i },
      headers: [{ name: 'server', pattern: /GitHub\.com/i }],
    },
  },
  {
    name: 'AWS Amplify',
    category: 'hosting',
    icon: 'aws',
    url: 'https://aws.amazon.com/amplify',
    description: 'AWS full-stack hosting.',
    signals: {
      domain: { pattern: /\.amplifyapp\.com$/i },
    },
  },
  {
    name: 'Heroku',
    category: 'hosting',
    icon: 'heroku',
    url: 'https://www.heroku.com',
    description: 'Cloud platform-as-a-service.',
    signals: {
      domain: { pattern: /\.herokuapp\.com$/i },
      headers: [{ name: 'via', pattern: /vegur/i }],
    },
  },
  {
    name: 'Render',
    category: 'hosting',
    icon: 'render',
    url: 'https://render.com',
    description: 'Modern cloud platform.',
    signals: {
      domain: { pattern: /\.onrender\.com$/i },
      headers: [{ name: 'rndr-id', pattern: /.+/ }],
    },
  },
  {
    name: 'Fly.io',
    category: 'hosting',
    icon: 'fly',
    url: 'https://fly.io',
    description: 'Edge application platform.',
    signals: {
      domain: { pattern: /\.fly\.dev$/i },
      headers: [{ name: 'fly-request-id', pattern: /.+/ }],
    },
  },

  /* ============================================================
     Analytics
     ============================================================ */
  {
    name: 'Google Analytics',
    category: 'analytics',
    icon: 'google-analytics',
    url: 'https://analytics.google.com',
    description: 'Google\'s web analytics platform.',
    signals: {
      scriptSrc: [
        { pattern: /googletagmanager\.com\/gtag\/js/i },
        { pattern: /google-analytics\.com\/analytics\.js/i },
      ],
      html: [
        { pattern: /gtag\(['"]config['"],\s*['"](G-[A-Z0-9]+|UA-\d+-\d+)/i, weight: 3 },
        { pattern: /ga\(['"]create['"],\s*['"]UA-\d+-\d+/i, weight: 3 },
      ],
    },
  },
  {
    name: 'Google Tag Manager',
    category: 'tagManager',
    icon: 'gtm',
    url: 'https://tagmanager.google.com',
    description: 'Tag management system from Google.',
    signals: {
      scriptSrc: [{ pattern: /googletagmanager\.com\/gtm\.js/i }],
      html: [{ pattern: /GTM-[A-Z0-9]+/i, weight: 3 }],
    },
  },
  {
    name: 'Plausible',
    category: 'analytics',
    icon: 'plausible',
    url: 'https://plausible.io',
    description: 'Privacy-friendly Google Analytics alternative.',
    signals: {
      scriptSrc: [{ pattern: /plausible\.io\/js\/plausible/i }],
      html: [{ pattern: /data-domain=["'][^"']+["'][^>]+plausible/i, weight: 2 }],
    },
  },
  {
    name: 'Fathom',
    category: 'analytics',
    icon: 'fathom',
    url: 'https://usefathom.com',
    description: 'Simple, privacy-focused website analytics.',
    signals: {
      scriptSrc: [{ pattern: /cdn\.usefathom\.com|cdn-eu\.usefathom\.com/i }],
    },
  },
  {
    name: 'Mixpanel',
    category: 'analytics',
    icon: 'mixpanel',
    url: 'https://mixpanel.com',
    description: 'Product analytics for user behavior.',
    signals: {
      scriptSrc: [{ pattern: /cdn\.mxpnl\.com/i }],
      html: [{ pattern: /window\.mixpanel\b/i, weight: 2 }],
    },
  },
  {
    name: 'Hotjar',
    category: 'analytics',
    icon: 'hotjar',
    url: 'https://www.hotjar.com',
    description: 'Heatmaps, recordings, and feedback.',
    signals: {
      scriptSrc: [{ pattern: /static\.hotjar\.com/i }],
      html: [{ pattern: /window\.hj\b|_hjSettings/i, weight: 2 }],
    },
  },
  {
    name: 'Segment',
    category: 'analytics',
    icon: 'segment',
    url: 'https://segment.com',
    description: 'Customer data platform.',
    signals: {
      scriptSrc: [{ pattern: /cdn\.segment\.com|cdn\.segment\.io/i }],
      html: [{ pattern: /analytics\.load\(['"]/i, weight: 1 }],
    },
  },
  {
    name: 'PostHog',
    category: 'analytics',
    icon: 'posthog',
    url: 'https://posthog.com',
    description: 'Open source product analytics.',
    signals: {
      scriptSrc: [{ pattern: /posthog\.com|i\.posthog\.com/i }],
      html: [{ pattern: /posthog\.init\(/i, weight: 2 }],
    },
  },
  {
    name: 'Matomo',
    category: 'analytics',
    icon: 'matomo',
    url: 'https://matomo.org',
    description: 'Open source analytics platform.',
    signals: {
      scriptSrc: [{ pattern: /matomo\.js|piwik\.js/i }],
      html: [{ pattern: /var\s+_paq\s*=/i, weight: 2 }],
    },
  },
  {
    name: 'Amplitude',
    category: 'analytics',
    icon: 'amplitude',
    url: 'https://amplitude.com',
    description: 'Product analytics for digital teams.',
    signals: {
      scriptSrc: [{ pattern: /cdn\.amplitude\.com/i }],
    },
  },

  /* ============================================================
     Marketing / CRM
     ============================================================ */
  {
    name: 'HubSpot',
    category: 'marketing',
    icon: 'hubspot',
    url: 'https://www.hubspot.com',
    description: 'Marketing, sales, and service platform.',
    signals: {
      scriptSrc: [
        { pattern: /js\.hs-scripts\.com/i },
        { pattern: /js\.hsforms\.net/i },
        { pattern: /js\.hsleadflows\.net/i },
      ],
      html: [{ pattern: /hubspotusercontent/i, weight: 1 }],
    },
  },
  {
    name: 'Marketo',
    category: 'marketing',
    icon: 'marketo',
    url: 'https://www.marketo.com',
    description: 'Adobe marketing automation.',
    signals: {
      scriptSrc: [{ pattern: /munchkin\.marketo\.net/i }],
      html: [{ pattern: /Munchkin\.init\(/i, weight: 2 }],
    },
  },
  {
    name: 'Mailchimp',
    category: 'marketing',
    icon: 'mailchimp',
    url: 'https://mailchimp.com',
    description: 'Email marketing platform.',
    signals: {
      scriptSrc: [{ pattern: /chimpstatic\.com|list-manage\.com/i }],
    },
  },
  {
    name: 'Drift',
    category: 'marketing',
    icon: 'drift',
    url: 'https://www.drift.com',
    description: 'Conversational marketing platform.',
    signals: {
      scriptSrc: [{ pattern: /js\.driftt\.com|widget\.drift\.com/i }],
    },
  },
  {
    name: 'Intercom',
    category: 'marketing',
    icon: 'intercom',
    url: 'https://www.intercom.com',
    description: 'Customer messaging platform.',
    signals: {
      scriptSrc: [{ pattern: /widget\.intercom\.io/i }],
      html: [{ pattern: /window\.intercomSettings/i, weight: 2 }],
    },
  },
  {
    name: 'Klaviyo',
    category: 'marketing',
    icon: 'klaviyo',
    url: 'https://www.klaviyo.com',
    description: 'E-commerce email and SMS marketing.',
    signals: {
      scriptSrc: [{ pattern: /static\.klaviyo\.com/i }],
    },
  },
  {
    name: 'ActiveCampaign',
    category: 'marketing',
    icon: 'activecampaign',
    url: 'https://www.activecampaign.com',
    description: 'Customer experience automation.',
    signals: {
      scriptSrc: [{ pattern: /trackcmp\.net/i }],
    },
  },
  {
    name: 'ConvertKit',
    category: 'marketing',
    icon: 'convertkit',
    url: 'https://convertkit.com',
    description: 'Email marketing for creators.',
    signals: {
      scriptSrc: [{ pattern: /f\.convertkit\.com/i }],
    },
  },
  {
    name: 'Meta Pixel',
    category: 'marketing',
    icon: 'meta',
    url: 'https://www.facebook.com/business/tools/meta-pixel',
    description: 'Facebook/Meta tracking pixel.',
    signals: {
      scriptSrc: [{ pattern: /connect\.facebook\.net/i }],
      html: [{ pattern: /fbq\(['"]init['"]/i, weight: 3 }],
    },
  },

  /* ============================================================
     Page builders (WordPress)
     ============================================================ */
  {
    name: 'Elementor',
    category: 'pageBuilder',
    icon: 'elementor',
    url: 'https://elementor.com',
    description: 'Most popular WordPress page builder.',
    signals: {
      metaGenerator: { pattern: /Elementor\s*([\d.]+)?/i, versionGroup: 1 },
      html: [
        { pattern: /\/wp-content\/plugins\/elementor\//i, weight: 3 },
        { pattern: /class=["'][^"']*elementor-[^"']*["']/i, weight: 2 },
      ],
    },
    implies: ['WordPress'],
  },
  {
    name: 'Divi',
    category: 'pageBuilder',
    icon: 'divi',
    url: 'https://www.elegantthemes.com/gallery/divi/',
    description: 'Premium WordPress theme + page builder.',
    signals: {
      html: [
        { pattern: /\/wp-content\/themes\/Divi\//i, weight: 3 },
        { pattern: /et_builder|et_pb_/i, weight: 2 },
      ],
    },
    implies: ['WordPress'],
  },
  {
    name: 'Beaver Builder',
    category: 'pageBuilder',
    icon: 'beaver',
    url: 'https://www.wpbeaverbuilder.com',
    description: 'Premium WordPress page builder.',
    signals: {
      html: [{ pattern: /\/wp-content\/plugins\/(?:bb-plugin|beaver-builder-lite-version)\//i, weight: 3 }],
    },
    implies: ['WordPress'],
  },
  {
    name: 'WPBakery',
    category: 'pageBuilder',
    icon: 'wpbakery',
    url: 'https://wpbakery.com',
    description: 'WordPress page builder, formerly Visual Composer.',
    signals: {
      html: [
        { pattern: /\/wp-content\/plugins\/js_composer\//i, weight: 3 },
        { pattern: /vc_(?:row|column|element)/i, weight: 2 },
      ],
    },
    implies: ['WordPress'],
  },
  {
    name: 'Oxygen Builder',
    category: 'pageBuilder',
    icon: 'oxygen',
    url: 'https://oxygenbuilder.com',
    description: 'WordPress builder for designers.',
    signals: {
      html: [{ pattern: /\/wp-content\/plugins\/oxygen\//i, weight: 3 }],
    },
    implies: ['WordPress'],
  },

  /* ============================================================
     UI Libraries / CSS Frameworks
     ============================================================ */
  {
    name: 'Bootstrap',
    category: 'uiLibrary',
    icon: 'bootstrap',
    url: 'https://getbootstrap.com',
    description: 'Most popular CSS framework.',
    minScore: 2,
    signals: {
      scriptSrc: [{ pattern: /bootstrap[.@-]([\d.]+)/i, versionGroup: 1 }],
      html: [
        { pattern: /<link[^>]+href=["'][^"']*bootstrap[^"']*\.css/i, weight: 2 },
        { pattern: /class=["'][^"']*\bcol-(?:xs|sm|md|lg|xl|xxl)-\d+\b/i, weight: 1 },
      ],
    },
  },
  {
    name: 'Tailwind CSS',
    category: 'uiLibrary',
    icon: 'tailwind',
    url: 'https://tailwindcss.com',
    description: 'Utility-first CSS framework.',
    signals: {
      html: [
        { pattern: /class=["'][^"']*\b(?:flex|grid|hidden|block|text-(?:xs|sm|base|lg|xl|2xl)|p[xytrbl]?-\d|m[xytrbl]?-\d)\b[^"']*["']/i, weight: 1 },
        { pattern: /tailwindcss\.com|cdn\.tailwindcss/i, weight: 2 },
      ],
    },
    minScore: 2,
  },
  {
    name: 'Material UI',
    category: 'uiLibrary',
    icon: 'mui',
    url: 'https://mui.com',
    description: 'React component library following Material Design.',
    signals: {
      html: [{ pattern: /class=["'][^"']*\bMui[A-Z][a-zA-Z]+\b/i, weight: 2 }],
    },
  },
  {
    name: 'Bulma',
    category: 'uiLibrary',
    icon: 'bulma',
    url: 'https://bulma.io',
    description: 'Modern CSS framework based on Flexbox.',
    signals: {
      html: [{ pattern: /<link[^>]+href=["'][^"']*bulma[^"']*\.css/i, weight: 2 }],
    },
  },
  {
    name: 'Foundation',
    category: 'uiLibrary',
    icon: 'foundation',
    url: 'https://get.foundation',
    description: 'Responsive front-end framework by ZURB.',
    signals: {
      html: [{ pattern: /<link[^>]+href=["'][^"']*foundation[^"']*\.css/i, weight: 2 }],
    },
  },

  /* ============================================================
     Payment processors
     ============================================================ */
  {
    name: 'Stripe',
    category: 'payment',
    icon: 'stripe',
    url: 'https://stripe.com',
    description: 'Online payment processing.',
    signals: {
      scriptSrc: [{ pattern: /js\.stripe\.com/i }],
    },
  },
  {
    name: 'PayPal',
    category: 'payment',
    icon: 'paypal',
    url: 'https://www.paypal.com',
    description: 'Online payments and money transfers.',
    signals: {
      scriptSrc: [{ pattern: /paypal\.com\/sdk|paypalobjects\.com/i }],
    },
  },
  {
    name: 'Square',
    category: 'payment',
    icon: 'square',
    url: 'https://squareup.com',
    description: 'Payment processing and POS.',
    signals: {
      scriptSrc: [{ pattern: /js\.squareup\.com/i }],
    },
  },
  {
    name: 'Braintree',
    category: 'payment',
    icon: 'braintree',
    url: 'https://www.braintreepayments.com',
    description: 'PayPal-owned payment platform.',
    signals: {
      scriptSrc: [{ pattern: /js\.braintreegateway\.com/i }],
    },
  },
];

/* ============================================================
   Helper map: name -> Signature for fast lookup by `implies`
   ============================================================ */
export const SIGNATURE_MAP: Map<string, Signature> = new Map(
  SIGNATURES.map((s) => [s.name, s])
);
