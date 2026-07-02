/**
 * Convert FAQ sections in already-migrated BlogLayout blog posts
 * from plain Q/A paragraphs to server-rendered accordion markup.
 */
import fs from 'node:fs';
import path from 'node:path';

const BLOG_DIR = path.resolve('src/pages/blog');

function stripHtml(html) {
  return html.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50);
}

function convertFaqInContent(content) {
  // Find FAQ heading
  const faqRegex = /(<h2[^>]*>)([\s\S]*?)(Frequently Asked Questions|FAQ|Common Questions)([\s\S]*?)(<\/h2>)/i;
  const faqMatch = content.match(faqRegex);
  if (!faqMatch) return content;

  const beforeFaq = content.slice(0, faqMatch.index);
  let afterFaq = content.slice(faqMatch.index + faqMatch[0].length);

  // Build accordion
  let accordion = '<div class="faq-list">\n';
  let idx = 0;

  // Match pairs of <p><strong>Question</strong></p><p>Answer</p> or <h3>Question</h3><p>Answer</p>
  const pairRegex = /(?:<p>\s*<strong>([\s\S]*?)<\/strong>\s*<\/p>|<h3[^>]*>([\s\S]*?)<\/h3>)\s*<p>([\s\S]*?)<\/p>/gi;
  let pair;
  const pairs = [];
  while ((pair = pairRegex.exec(afterFaq)) !== null) {
    const question = stripHtml(pair[1] || pair[2] || '');
    const answer = pair[3].trim();
    if (!question || !answer) continue;
    pairs.push({ question, answer });
  }

  if (pairs.length === 0) return content;

  for (const { question, answer } of pairs) {
    const qid = slugify(question) || `faq-${idx}`;
    accordion += `  <div class="faq-item">\n`;
    accordion += `    <button class="faq-q" onclick="toggleFaq(this)" aria-expanded="false" aria-controls="${qid}">\n`;
    accordion += `      <span class="faq-q-text">${question.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</span>\n`;
    accordion += `      <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>\n`;
    accordion += `    </button>\n`;
    accordion += `    <div class="faq-a" id="${qid}"><div class="faq-a-inner"><p>${answer}</p></div></div>\n`;
    accordion += `  </div>\n`;
    idx++;
  }
  accordion += '</div>';

  // Remove the consumed Q/A pairs from afterFaq
  // We remove from the start of afterFaq up to the end of the last matched pair
  let lastEnd = 0;
  pairRegex.lastIndex = 0;
  while ((pair = pairRegex.exec(afterFaq)) !== null) {
    lastEnd = pair.index + pair[0].length;
  }
  afterFaq = afterFaq.slice(lastEnd);

  return beforeFaq + faqMatch[0] + '\n' + accordion + '\n' + afterFaq;
}

function main() {
  const dirs = fs.readdirSync(BLOG_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .filter((name) => name !== 'index.astro' && !name.startsWith('.'));

  let converted = 0;
  let noFaq = 0;
  let failed = [];

  for (const dir of dirs) {
    const indexPath = path.join(BLOG_DIR, dir, 'index.astro');
    if (!fs.existsSync(indexPath)) continue;
    try {
      const text = fs.readFileSync(indexPath, 'utf-8');
      if (!text.includes('BlogLayout')) {
        noFaq++;
        continue;
      }

      const layoutStart = text.indexOf('<BlogLayout');
      const layoutEnd = text.lastIndexOf('</BlogLayout>');
      if (layoutStart === -1 || layoutEnd === -1) {
        failed.push(`${dir}: could not find BlogLayout tags`);
        continue;
      }

      const beforeLayout = text.slice(0, layoutStart);
      const layoutTag = text.slice(layoutStart, text.indexOf('>', layoutStart) + 1);
      const content = text.slice(text.indexOf('>', layoutStart) + 1, layoutEnd);
      const afterLayout = text.slice(layoutEnd + '</BlogLayout>'.length);

      if (!/frequently asked questions|common questions/i.test(content)) {
        noFaq++;
        continue;
      }

      const newContent = convertFaqInContent(content);
      const newFile = beforeLayout + layoutTag + '\n' + newContent + '\n</BlogLayout>' + afterLayout;
      fs.writeFileSync(indexPath, newFile, 'utf-8');
      converted++;
    } catch (e) {
      failed.push(`${dir}: ${e.message}`);
    }
  }

  console.log(`Converted FAQs in ${converted} posts`);
  console.log(`No FAQ section: ${noFaq}`);
  if (failed.length) {
    console.log(`Failed: ${failed.length}`);
    for (const f of failed.slice(0, 20)) console.log('  -', f);
  }
}

main();
