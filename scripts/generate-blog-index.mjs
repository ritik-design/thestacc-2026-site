#!/usr/bin/env node
/**
 * Generate src/data/blog-posts.json from all blog post Astro files.
 * Run automatically via `npm run prebuild` or manually with `node scripts/generate-blog-index.mjs`.
 */
import fs from 'node:fs';
import path from 'node:path';

const BLOG_DIR = path.resolve('src/pages/blog');
const OUT_FILE = path.resolve('src/data/blog-posts.json');

function extractQuoted(text, key) {
  const regex = new RegExp(`${key}\\s*:\\s*["']([^"']+)["']`, 'i');
  const match = text.match(regex);
  return match ? match[1] : '';
}

function extractField(text, key) {
  // Try string value
  let val = extractQuoted(text, key);
  if (val) return val;
  // Try template/backtick or multi-line
  const regex = new RegExp(`${key}\\s*:\\s*\`([^\`]*)\``, 'i');
  const match = text.match(regex);
  return match ? match[1] : '';
}

function parsePost(filePath) {
  const text = fs.readFileSync(filePath, 'utf-8');
  const slug = path.basename(path.dirname(filePath));

  // Extract title from `title: "..."` inside `const seo = { ... }`
  const title = extractField(text, 'title');
  const description = extractField(text, 'description');

  // Date fallback: try to find a date field, else use file modification time
  let date = extractField(text, 'date');
  if (!date) {
    const stat = fs.statSync(filePath);
    date = stat.mtime.toISOString().split('T')[0];
  }

  // Author fallback
  let author = extractField(text, 'author');
  if (!author) author = 'theStacc Team';

  // Read time fallback - estimate from content length
  let readTime = extractField(text, 'readTime');
  if (!readTime) {
    const wordCount = text.split(/\s+/).length;
    const minutes = Math.max(3, Math.round(wordCount / 200));
    readTime = `${minutes} min`;
  }

  // Category fallback
  let cat = extractField(text, 'cat') || extractField(text, 'category');
  if (!cat) cat = 'SEO Tips';

  return {
    slug,
    title,
    excerpt: description,
    cat,
    author,
    date,
    readTime,
  };
}

function main() {
  const dirs = fs.readdirSync(BLOG_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .filter((name) => name !== 'index.astro' && !name.startsWith('.'));

  const posts = [];
  for (const dir of dirs) {
    const indexPath = path.join(BLOG_DIR, dir, 'index.astro');
    if (!fs.existsSync(indexPath)) continue;
    try {
      posts.push(parsePost(indexPath));
    } catch (e) {
      console.error(`Failed to parse ${indexPath}:`, e.message);
    }
  }

  // Sort by date descending, then slug
  posts.sort((a, b) => {
    const dateDiff = new Date(b.date) - new Date(a.date);
    if (dateDiff !== 0) return dateDiff;
    return a.slug.localeCompare(b.slug);
  });

  fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });
  fs.writeFileSync(OUT_FILE, JSON.stringify(posts, null, 2), 'utf-8');
  console.log(`Generated ${OUT_FILE} with ${posts.length} posts`);
}

main();
