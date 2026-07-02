/**
 * Build-time syntax highlighter for docs code blocks.
 *
 * Uses Shiki (already bundled via Astro) to highlight at build time —
 * the docs are static (getStaticPaths), so this adds ZERO client-side JS.
 * A single highlighter instance is created lazily and reused across every
 * page render in the build.
 */

import { createHighlighter, type Highlighter } from 'shiki';

// Light theme — the docs are light-only (no dark mode), matching the
// design system. Background is overridden to --stacc-stone-50 in CSS.
const THEME = 'github-light';

// Only the languages that actually appear in src/data/docs.ts, plus the
// common aliases authors might reach for. Keeping this list tight keeps
// the build fast and the loaded grammar set small.
const LANGS = [
  'bash',
  'json',
  'typescript',
  'javascript',
  'python',
  'vue',
  'tsx',
  'jsx',
  'sql',
  'php',
  'astro',
  'yaml',
  'prisma',
  'html',
  'css',
] as const;

// Friendly labels shown in the code-block header bar.
const LANG_LABELS: Record<string, string> = {
  bash: 'Bash',
  sh: 'Shell',
  shell: 'Shell',
  json: 'JSON',
  ts: 'TypeScript',
  typescript: 'TypeScript',
  js: 'JavaScript',
  javascript: 'JavaScript',
  py: 'Python',
  python: 'Python',
  vue: 'Vue',
  tsx: 'TSX',
  jsx: 'JSX',
  sql: 'SQL',
  php: 'PHP',
  astro: 'Astro',
  yaml: 'YAML',
  yml: 'YAML',
  prisma: 'Prisma',
  html: 'HTML',
  css: 'CSS',
};

// Aliases → canonical Shiki lang id (only those not already loaded by id).
const LANG_ALIASES: Record<string, string> = {
  js: 'javascript',
  ts: 'typescript',
  py: 'python',
  sh: 'bash',
  shell: 'bash',
  yml: 'yaml',
};

// Cache the highlighter on globalThis, NOT a module-level variable.
// Astro's dev server (Vite SSR) re-evaluates this module on every request,
// which would reset a module-scoped singleton and spawn a fresh Shiki
// highlighter per doc page (the "[Shiki] N instances created" warning).
// A globalThis key survives module re-evaluation, so we create exactly one.
// Theme is part of the key so changing THEME invalidates the cached
// highlighter (otherwise dev would reuse one without the new theme loaded).
const HL_KEY = `__staccDocsHighlighter__${THEME}`;

function getHighlighter(): Promise<Highlighter> {
  const g = globalThis as Record<string, unknown>;
  if (!g[HL_KEY]) {
    g[HL_KEY] = createHighlighter({
      themes: [THEME],
      langs: [...LANGS],
    });
  }
  return g[HL_KEY] as Promise<Highlighter>;
}

export function langLabel(lang: string): string {
  if (!lang) return 'Code';
  return LANG_LABELS[lang.toLowerCase()] ?? lang.toUpperCase();
}

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

/**
 * Returns highlighted HTML for a code block as a Shiki `<pre class="shiki">…`.
 * Unknown or missing languages fall back to an escaped, unhighlighted block
 * so the build never throws on an unexpected fence.
 */
export async function highlightCode(code: string, lang: string): Promise<string> {
  const hl = await getHighlighter();
  const requested = (lang || '').toLowerCase();
  const resolved = LANG_ALIASES[requested] ?? requested;
  const loaded = hl.getLoadedLanguages();

  if (resolved && loaded.includes(resolved)) {
    return hl.codeToHtml(code, { lang: resolved, theme: THEME });
  }

  // No / unknown language → plain escaped block that still gets the
  // code-block chrome and theme background from CSS.
  return `<pre class="shiki" tabindex="0"><code>${escapeHtml(code)
    .split('\n')
    .map((l) => `<span class="line">${l || ' '}</span>`)
    .join('\n')}</code></pre>`;
}
