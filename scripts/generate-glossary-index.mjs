#!/usr/bin/env node
/**
 * Generate src/data/glossary-terms.json from all glossary term Astro files.
 * Run automatically via `npm run prebuild` or manually with `node scripts/generate-glossary-index.mjs`.
 */
import fs from 'node:fs';
import path from 'node:path';

const GLOSSARY_DIR = path.resolve('src/pages/glossary');
const OUT_FILE = path.resolve('src/data/glossary-terms.json');

function stripHtml(html) {
  return html
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

function extractFrontmatter(text) {
  const match = text.match(/^---\s*\n([\s\S]*?)\n---/);
  return match ? match[1] : '';
}

function extractDefinedTerm(text) {
  // Find the DefinedTerm schema object
  const fm = extractFrontmatter(text);
  const match = fm.match(/\{[\s\S]*?"@type"\s*:\s*"DefinedTerm"[\s\S]*?\}/);
  return match ? match[0] : '';
}

function extractJsonString(block, key) {
  const regex = new RegExp(`"${key}"\\s*:\\s*"([^"]{3,})"`, 'i');
  const match = block.match(regex);
  return match ? match[1] : '';
}

function parseTerm(filePath) {
  const text = fs.readFileSync(filePath, 'utf-8');
  const slug = path.basename(path.dirname(filePath));

  // Term name from H1
  let term = '';
  const h1Match = text.match(/<section class="post-hero">[\s\S]*?<h1>([\s\S]*?)<\/h1>/);
  if (h1Match) {
    term = stripHtml(h1Match[1]).replace(/\s+/g, ' ').trim();
  }
  if (!term) {
    // Fallback to DefinedTerm name
    const dt = extractDefinedTerm(text);
    term = extractJsonString(dt, 'name');
  }
  if (!term) {
    term = slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }

  // Category from term badge
  let cat = 'Other';
  const badgeMatch = text.match(/<div class="term-badge">[\s\S]*?<span class="term-cat-dot"><\/span>\s*([^·\n]+)\s*·/);
  if (badgeMatch) {
    cat = badgeMatch[1].trim();
  }
  if (cat === 'Other') {
    // Fallback to breadcrumb category link
    const crumbMatch = text.match(/<a href="\/glossary\/\?cat=[^"]+">([^<]+)<\/a><span class="sep">\/[^/]*<\/span>\s*<span class="current">/);
    if (crumbMatch) cat = crumbMatch[1].trim();
  }

  // Definition from description paragraph
  let def = '';
  const descMatch = text.match(/<p class="description">([\s\S]*?)<\/p>/);
  if (descMatch) {
    def = stripHtml(descMatch[1]).replace(/\s+/g, ' ').trim();
  }
  if (!def) {
    // Fallback to DefinedTerm description
    const dt = extractDefinedTerm(text);
    def = extractJsonString(dt, 'description');
  }
  if (!def) {
    // Fallback to meta description
    def = extractJsonString(extractFrontmatter(text), 'description');
  }

  return { slug, term, cat, def };
}

function main() {
  const dirs = fs.readdirSync(GLOSSARY_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .filter((name) => name !== 'index.astro' && !name.startsWith('.'));

  const terms = [];
  for (const dir of dirs) {
    const indexPath = path.join(GLOSSARY_DIR, dir, 'index.astro');
    if (!fs.existsSync(indexPath)) continue;
    try {
      terms.push(parseTerm(indexPath));
    } catch (e) {
      console.error(`Failed to parse ${indexPath}:`, e.message);
    }
  }

  // Sort alphabetically by term
  terms.sort((a, b) => a.term.localeCompare(b.term));

  fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });
  fs.writeFileSync(OUT_FILE, JSON.stringify(terms, null, 2), 'utf-8');
  console.log(`Generated ${OUT_FILE} with ${terms.length} terms`);
}

main();
