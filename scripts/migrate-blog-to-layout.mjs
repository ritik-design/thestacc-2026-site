/**
 * Migrate all src/pages/blog posts to use BlogLayout.astro
 * with sidebar, TOC, author block, and FAQ accordion.
 */
import fs from 'node:fs';
import path from 'node:path';

const BLOG_DIR = path.resolve('src/pages/blog');

const AUTHOR_DB = {
  'siddharth-gangal': {
    name: 'Siddharth Gangal',
    role: 'Founder · theStacc',
    slug: 'siddharth-gangal',
    avatar: 'SG',
    bio: 'Siddharth is the founder of theStacc. Previously co-founded ARKA 360 out of IIT Mandi. He writes about AI search, programmatic SEO, and SaaS founder lessons.',
    linkedin: 'https://www.linkedin.com/in/sidgangal/',
  },
  'akshay-vr': {
    name: 'Akshay VR',
    role: 'Marketing Head · theStacc',
    slug: 'akshay-vr',
    avatar: 'AVR',
    bio: 'Akshay runs marketing and editorial at theStacc. Previously Senior Marketing Specialist at ARKA 360. He writes about SEO strategy, content operations, and B2B SaaS marketing.',
    linkedin: 'https://www.linkedin.com/in/akshay-vr-3aa1b9204/',
  },
  'ritik-namdev': {
    name: 'Ritik Namdev',
    role: 'Growth Manager · theStacc',
    slug: 'ritik-namdev',
    avatar: 'RN',
    bio: 'Ritik runs growth at theStacc. Five years in digital marketing, content strategy, and growth at content-led SaaS. He writes about programmatic SEO, CRO, and analytics.',
    linkedin: 'https://www.linkedin.com/in/ritiknamdev/',
  },
};

function slugifyAuthor(name) {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function extractBetween(text, start, end) {
  const idx = text.indexOf(start);
  if (idx === -1) return '';
  const rest = text.slice(idx + start.length);
  const endIdx = rest.indexOf(end);
  if (endIdx === -1) return '';
  return rest.slice(0, endIdx);
}

function extractTag(html, tag, className) {
  let regex;
  if (className) {
    regex = new RegExp(`<${tag}[^>]*class=["']${className}["'][^>]*>([\\s\\S]*?)<\\/${tag}>`, 'i');
  } else {
    regex = new RegExp(`<${tag}(?:[^>]*)>([\\s\\S]*?)<\\/${tag}>`, 'i');
  }
  const match = html.match(regex);
  return match ? match[1].trim() : '';
}

function stripHtml(html) {
  return html.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function parsePost(filePath) {
  const text = fs.readFileSync(filePath, 'utf-8');

  // Frontmatter
  const frontmatter = extractBetween(text, '---\n', '\n---');

  // SEO object from frontmatter
  const seoMatch = frontmatter.match(/const seo = \{([\s\S]*?)\};/);
  const seo = seoMatch ? `const seo = {${seoMatch[1]}};` : '';

  // Post-hero data
  const heroHtml = extractBetween(text, '<section class="post-hero">', '</section>');
  const category = extractTag(heroHtml, 'span', 'post-cat');
  const title = stripHtml(extractTag(heroHtml, 'h1', ''));
  const description = extractTag(heroHtml, 'p', 'description');

  // Author — extract specific fields directly from hero HTML
  const avatar = stripHtml((heroHtml.match(/<div class="meta-avatar">([\s\S]*?)<\/div>/) || ['', ''])[1]);
  const authorName = stripHtml((heroHtml.match(/<span class="meta-author-name">[\s\S]*?<a[^>]*>([\s\S]*?)<\/a>[\s\S]*?<\/span>/) || ['', ''])[1]);
  const authorRole = stripHtml((heroHtml.match(/<span class="meta-author-role">([\s\S]*?)<\/span>/) || ['', ''])[1]);
  const authorSlugMatch = heroHtml.match(/<a href="\/authors\/([^/]+)\//);
  const authorSlug = authorSlugMatch ? authorSlugMatch[1] : slugifyAuthor(authorName);

  // Date and read time
  let date = '';
  let readTime = '';
  const metaItems = heroHtml.match(/<div class="meta-item">[\s\S]*?<\/div>/g) || [];
  for (const item of metaItems) {
    const label = stripHtml(extractTag(item, 'span', 'meta-label'));
    const value = stripHtml(extractTag(item, 'span', 'meta-value'));
    if (label === 'Published') date = value;
    if (label === 'Read') readTime = value;
  }

  // Article content
  const content = extractBetween(text, '<article class="post-content">', '</article>').trim();

  return {
    seo,
    category,
    title,
    description,
    authorName,
    authorRole,
    authorSlug,
    avatar,
    date,
    readTime,
    content,
  };
}

function buildNewFile(data) {
  const author = AUTHOR_DB[data.authorSlug] || {
    name: data.authorName,
    role: data.authorRole,
    slug: data.authorSlug,
    avatar: data.avatar,
    bio: `${data.authorName} writes for theStacc.`,
    linkedin: '',
  };

  const authorObj = JSON.stringify(author, null, 2).replace(/"([^"]+)":/g, '$1:');

  return `---
import BlogLayout from '../../../layouts/BlogLayout.astro';

${data.seo}

const author = ${authorObj};

const category = ${JSON.stringify(data.category)};
const date = ${JSON.stringify(data.date)};
const readTime = ${JSON.stringify(data.readTime)};
---
<BlogLayout
  seo={seo}
  category={category}
  title={${JSON.stringify(data.title)}}
  description={${JSON.stringify(data.description)}}
  author={author}
  date={date}
  readTime={readTime}
>
${data.content}
</BlogLayout>
`;
}

function main() {
  const dirs = fs.readdirSync(BLOG_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .filter((name) => name !== 'index.astro' && !name.startsWith('.'));

  let migrated = 0;
  let failed = [];

  for (const dir of dirs) {
    const indexPath = path.join(BLOG_DIR, dir, 'index.astro');
    if (!fs.existsSync(indexPath)) continue;
    try {
      const data = parsePost(indexPath);
      if (!data.content) {
        failed.push(`${dir}: no article content found`);
        continue;
      }
      const newFile = buildNewFile(data);
      fs.writeFileSync(indexPath, newFile, 'utf-8');
      migrated++;
    } catch (e) {
      failed.push(`${dir}: ${e.message}`);
    }
  }

  console.log(`Migrated ${migrated} blog posts`);
  if (failed.length) {
    console.log(`Failed: ${failed.length}`);
    for (const f of failed.slice(0, 20)) console.log('  -', f);
  }
}

main();
