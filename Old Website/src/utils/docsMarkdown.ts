/**
 * Enhanced markdown renderer for docs pages.
 * Outputs clean HTML without inline classes — styled by .docs-content CSS.
 * Also generates heading IDs for table-of-contents linking.
 */

import { highlightCode, langLabel } from './docsHighlight';

export type DocHeading = {
  id: string;
  text: string;
  level: 2 | 3;
};

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

function escapeAttr(value: string): string {
  return value.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// Escapes HTML metacharacters for BODY-TEXT contexts only — inside
// <p>, <code>, <li>, etc. Does NOT escape quotes, so it MUST NOT be
// used to build attribute values (would XSS via `<div title="${...}">`
// when the input contains a `"`). Use `escapeAttr` for attributes —
// the function name suffix `Text` is the contract.
function escapeHtmlText(value: string): string {
  return value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function renderInline(text: string): string {
  // Bold
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  // Inline code — MUST html-escape the captured content. Without this,
  // markdown like `<h2>` rendered as `<code><h2></code>` and the browser
  // interpreted the inner <h2> as a real heading tag, eating subsequent
  // text into the wrong DOM context (the bug that broke the Webhook
  // Reference field-reference table — `<a>` inside backticks captured
  // ", etc." as link text).
  text = text.replace(/`([^`]+)`/g, (_m, code) => `<code>${escapeHtmlText(code)}</code>`);
  // Images — must run before links since both share `[` syntax
  text = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_m, alt, src) => {
    return `<img src="${escapeAttr(src)}" alt="${escapeAttr(alt)}" loading="lazy" />`;
  });
  // Links
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  return text;
}

function isTableSeparator(line: string): boolean {
  // Matches lines like `| --- | :---: | ---: |`
  return /^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
}

function splitTableRow(line: string): string[] {
  // Strip leading/trailing pipes, then split on `|` not preceded by `\`.
  // Lookbehind `(?<!\\)` keeps escaped pipes (`\|`) inside cells —
  // standard markdown behavior used by tables that say "string \| null".
  // After splitting, replace the literal `\|` with `|` so the cell
  // renders as a real pipe character. The previous version's comment
  // claimed to do this but the implementation just did `split('|')` —
  // any cell with a `\|` got split mid-content, shifting later cells
  // into the wrong columns of the rendered <table>.
  const trimmed = line.trim().replace(/^\|/, '').replace(/\|$/, '');
  return trimmed
    .split(/(?<!\\)\|/)
    .map(c => c.trim().replace(/\\\|/g, '|'));
}

export function extractHeadings(content: string): DocHeading[] {
  const headings: DocHeading[] = [];
  for (const line of content.split('\n')) {
    if (line.startsWith('### ')) {
      const raw = line.slice(4).replace(/\*\*(.+?)\*\*/g, '$1').replace(/`([^`]+)`/g, '$1');
      headings.push({ id: slugify(raw), text: raw, level: 3 });
    } else if (line.startsWith('## ')) {
      const raw = line.slice(3).replace(/\*\*(.+?)\*\*/g, '$1').replace(/`([^`]+)`/g, '$1');
      headings.push({ id: slugify(raw), text: raw, level: 2 });
    }
  }
  return headings;
}

// SVG icons for the code-block copy button (copy + check states).
const COPY_ICON = '<svg class="docs-code-copy-icon-copy" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>';
const CHECK_ICON = '<svg class="docs-code-copy-icon-check" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';

export async function renderDocsMarkdown(content: string): Promise<string> {
  const lines = content.split('\n');
  const parts: string[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Code block
    if (line.startsWith('```')) {
      const lang = line.slice(3).trim();
      const codeLines: string[] = [];
      i++;
      while (i < lines.length && !lines[i].startsWith('```')) {
        codeLines.push(lines[i]);
        i++;
      }
      i++; // skip closing ```
      const raw = codeLines.join('\n');
      const highlighted = await highlightCode(raw, lang);
      parts.push(
        `<div class="docs-code">` +
          `<div class="docs-code-bar">` +
            `<span class="docs-code-lang">${escapeHtmlText(langLabel(lang))}</span>` +
            `<button type="button" class="docs-code-copy" aria-label="Copy code">` +
              COPY_ICON + CHECK_ICON +
              `<span class="docs-code-copy-label">Copy</span>` +
            `</button>` +
          `</div>` +
          highlighted +
        `</div>`
      );
      continue;
    }

    // Heading 2
    if (line.startsWith('## ')) {
      const text = line.slice(3);
      const raw = text.replace(/\*\*(.+?)\*\*/g, '$1').replace(/`([^`]+)`/g, '$1');
      const id = slugify(raw);
      parts.push(`<h2 id="${id}">${renderInline(text)}<a href="#${id}" class="heading-anchor" aria-label="Copy link to ${raw}">#</a></h2>`);
      i++;
      continue;
    }

    // Heading 3
    if (line.startsWith('### ')) {
      const text = line.slice(4);
      const raw = text.replace(/\*\*(.+?)\*\*/g, '$1').replace(/`([^`]+)`/g, '$1');
      const id = slugify(raw);
      parts.push(`<h3 id="${id}">${renderInline(text)}<a href="#${id}" class="heading-anchor" aria-label="Copy link to ${raw}">#</a></h3>`);
      i++;
      continue;
    }

    // Blockquote
    if (line.startsWith('> ')) {
      const quoteLines: string[] = [];
      while (i < lines.length && lines[i].startsWith('> ')) {
        quoteLines.push(lines[i].slice(2));
        i++;
      }
      const inner = quoteLines.map(l => `<p>${renderInline(l)}</p>`).join('');
      parts.push(`<blockquote>${inner}</blockquote>`);
      continue;
    }

    // Ordered list
    if (/^\d+\.\s/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        items.push(lines[i].replace(/^\d+\.\s/, ''));
        i++;
      }
      const lis = items.map(item => `<li>${renderInline(item)}</li>`).join('');
      parts.push(`<ol>${lis}</ol>`);
      continue;
    }

    // Unordered list
    if (line.startsWith('- ')) {
      const items: string[] = [];
      while (i < lines.length && lines[i].startsWith('- ')) {
        items.push(lines[i].slice(2));
        i++;
      }
      const lis = items.map(item => `<li>${renderInline(item)}</li>`).join('');
      parts.push(`<ul>${lis}</ul>`);
      continue;
    }

    // Pipe table — header row, then `| --- |` separator, then body rows
    if (line.includes('|') && i + 1 < lines.length && isTableSeparator(lines[i + 1])) {
      const headerCells = splitTableRow(line);
      i += 2; // skip header + separator
      const bodyRows: string[][] = [];
      while (i < lines.length && lines[i].includes('|') && lines[i].trim() !== '') {
        bodyRows.push(splitTableRow(lines[i]));
        i++;
      }
      const thead = `<thead><tr>${headerCells.map(c => `<th>${renderInline(c)}</th>`).join('')}</tr></thead>`;
      const tbody = `<tbody>${bodyRows.map(row => `<tr>${row.map(c => `<td>${renderInline(c)}</td>`).join('')}</tr>`).join('')}</tbody>`;
      parts.push(`<div class="table-wrap"><table>${thead}${tbody}</table></div>`);
      continue;
    }

    // Standalone image on its own line — wrap in <figure> for proper styling
    if (/^!\[[^\]]*\]\([^)]+\)\s*$/.test(line.trim())) {
      const match = line.trim().match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
      if (match) {
        const [, alt, src] = match;
        parts.push(
          `<figure class="docs-figure"><img src="${escapeAttr(src)}" alt="${escapeAttr(alt)}" loading="lazy" />${alt ? `<figcaption>${escapeAttr(alt)}</figcaption>` : ''}</figure>`
        );
        i++;
        continue;
      }
    }

    // Horizontal rule
    if (line.trim() === '---') {
      parts.push('<hr>');
      i++;
      continue;
    }

    // Empty line
    if (line.trim() === '') {
      i++;
      continue;
    }

    // Paragraph
    parts.push(`<p>${renderInline(line)}</p>`);
    i++;
  }

  return parts.join('\n');
}
