/**
 * Converts markdown to HTML for blog posts.
 * Supports: headings, tables, lists, checklists, blockquotes (+ CTA pattern),
 * images, links, bold, inline code, horizontal rules.
 */
export function renderMarkdown(content: string): string {
  const lines = content.split('\n');
  const parts: string[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Skip horizontal rules
    if (line.trim() === '---') { i++; continue; }

    // Heading 2
    if (line.startsWith('## ')) {
      parts.push(`<h2>${inline(line.slice(3))}</h2>`);
      i++; continue;
    }
    // Heading 3
    if (line.startsWith('### ')) {
      parts.push(`<h3>${inline(line.slice(4))}</h3>`);
      i++; continue;
    }
    // Heading 4
    if (line.startsWith('#### ')) {
      parts.push(`<h4>${inline(line.slice(5))}</h4>`);
      i++; continue;
    }

    // Image (standalone line)
    if (/^!\[/.test(line)) {
      const m = line.match(/^!\[([^\]]*)\]\(([^)]+)\)/);
      if (m) {
        parts.push(`<figure class="blog-figure"><img src="${m[2]}" alt="${m[1]}" loading="lazy" /></figure>`);
      }
      i++; continue;
    }

    // Table (line starts with |)
    if (line.startsWith('|') && line.includes('|', 1)) {
      const tableLines: string[] = [];
      while (i < lines.length && lines[i].startsWith('|')) {
        tableLines.push(lines[i]);
        i++;
      }
      parts.push(renderTable(tableLines));
      continue;
    }

    // Blockquote — detect CTA pattern vs normal quote
    if (line.startsWith('> ')) {
      const bqLines: string[] = [];
      while (i < lines.length && lines[i].startsWith('> ')) {
        bqLines.push(lines[i].slice(2));
        i++;
      }
      // Check if this is a CTA blockquote (contains pricing link or "Start for" text)
      const fullText = bqLines.join(' ');
      const isCTA = fullText.includes('/pricing') || fullText.includes('Start for $1') || fullText.includes('Start for the');

      if (isCTA) {
        // Render as CTA card — separate headline, body, and button
        let headline = '';
        let body = '';
        let buttonText = '';
        let buttonHref = '';

        for (const bqLine of bqLines) {
          // Check if line is just a link (the button)
          const linkOnly = bqLine.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
          if (linkOnly) {
            buttonText = linkOnly[1];
            buttonHref = linkOnly[2];
            continue;
          }
          // Extract bold part as headline
          const boldMatch = bqLine.match(/^\*\*(.+?)\*\*\s*(.*)/);
          if (boldMatch) {
            headline = boldMatch[1];
            // Rest of the line is body — but may contain inline link
            let rest = boldMatch[2];
            // Extract any link from rest
            const inlineLink = rest.match(/\[([^\]]+)\]\(([^)]+)\)/);
            if (inlineLink && !buttonText) {
              buttonText = inlineLink[1];
              buttonHref = inlineLink[2];
              rest = rest.replace(/\[([^\]]+)\]\(([^)]+)\)/, '').trim();
            }
            if (rest) body += rest + ' ';
          } else {
            // Plain text line or line with link
            const inlineLink = bqLine.match(/\[([^\]]+)\]\(([^)]+)\)/);
            if (inlineLink && !buttonText) {
              buttonText = inlineLink[1];
              buttonHref = inlineLink[2];
              const rest = bqLine.replace(/\[([^\]]+)\]\(([^)]+)\)/, '').trim();
              if (rest) body += rest + ' ';
            } else {
              body += bqLine + ' ';
            }
          }
        }

        body = body.trim();
        // Clean up body — remove trailing periods after removing link
        body = body.replace(/\.\s*$/, '').replace(/\s+/g, ' ').trim();
        if (body && !body.endsWith('.')) body += '.';

        let ctaHtml = '<div class="blog-cta-card">';
        if (headline) ctaHtml += `<div class="blog-cta-headline">${headline}</div>`;
        if (body) ctaHtml += `<div class="blog-cta-body">${body}</div>`;
        if (buttonText && buttonHref) {
          ctaHtml += `<a href="${buttonHref}" class="blog-cta-button">${buttonText}</a>`;
        }
        ctaHtml += '</div>';
        parts.push(ctaHtml);
      } else {
        // Normal blockquote
        const inner = bqLines.map(l => `<p>${inline(l)}</p>`).join('');
        parts.push(`<blockquote>${inner}</blockquote>`);
      }
      continue;
    }

    // Ordered list
    if (/^\d+\.\s/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        let item = lines[i].replace(/^\d+\.\s/, '');
        i++;
        // Indented continuation
        while (i < lines.length && /^   [^ -]/.test(lines[i])) {
          item += ' ' + lines[i].trim();
          i++;
        }
        // Sub-items
        while (i < lines.length && lines[i].startsWith('   - ')) {
          item += '<br/><span class="sub-item">' + inline(lines[i].trim().slice(2)) + '</span>';
          i++;
        }
        items.push(item);
      }
      parts.push(`<ol>${items.map(it => `<li>${inline(it)}</li>`).join('')}</ol>`);
      continue;
    }

    // Unordered list
    if (line.startsWith('- ')) {
      const items: string[] = [];
      const isCheck = line.startsWith('- [ ] ') || line.startsWith('- [x] ');
      while (i < lines.length && lines[i].startsWith('- ')) {
        items.push(lines[i].slice(2));
        i++;
      }
      if (isCheck) {
        const lis = items.map(item => {
          const checked = item.startsWith('[x] ');
          const text = item.replace(/^\[[ x]\]\s*/, '');
          return `<li class="checklist-item${checked ? ' checked' : ''}"><input type="checkbox" ${checked ? 'checked ' : ''}disabled /><span>${inline(text)}</span></li>`;
        }).join('');
        parts.push(`<ul class="checklist">${lis}</ul>`);
      } else {
        parts.push(`<ul>${items.map(it => `<li>${inline(it)}</li>`).join('')}</ul>`);
      }
      continue;
    }

    // Empty line
    if (line.trim() === '') { i++; continue; }

    // Paragraph
    parts.push(`<p>${inline(line)}</p>`);
    i++;
  }

  return parts.join('\n');
}

/** Render a markdown table from pipe-delimited lines */
function renderTable(lines: string[]): string {
  const parseRow = (line: string): string[] =>
    line.split('|').slice(1, -1).map(cell => cell.trim());

  if (lines.length < 2) return '';

  const headers = parseRow(lines[0]);
  // Skip separator row (line with |---|)
  const startRow = lines[1].includes('---') ? 2 : 1;
  const rows: string[][] = [];
  for (let r = startRow; r < lines.length; r++) {
    rows.push(parseRow(lines[r]));
  }

  let html = '<div class="table-scroll-wrapper"><table>';

  // Thead
  html += '<thead><tr>';
  for (const h of headers) {
    html += `<th>${inline(h)}</th>`;
  }
  html += '</tr></thead>';

  // Tbody
  html += '<tbody>';
  for (const row of rows) {
    // Check if this is a Stacc row
    const isStacc = row.some(cell => /stacc/i.test(cell));
    html += `<tr${isStacc ? ' class="stacc-row"' : ''}>`;
    for (const cell of row) {
      html += `<td>${inline(cell)}</td>`;
    }
    html += '</tr>';
  }
  html += '</tbody></table></div>';

  return html;
}

/**
 * Extract FAQ {question, answer} pairs from a markdown body.
 *
 * Detects an `## FAQ` or `## Frequently Asked Questions` H2 section, then parses
 * either:
 *   - `### Question?` followed by paragraphs (until the next H3/H2/EOF), or
 *   - `**Question?**` followed by paragraphs (until the next bold-question or H2/EOF)
 *
 * Returns an empty array if no FAQ section is found. Used to feed `buildFAQSchema`.
 */
export function extractFAQs(body: string): { question: string; answer: string }[] {
  if (!body) return [];
  const lines = body.split('\n');

  // Find the FAQ section start (## heading)
  let start = -1;
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^##\s+(.+)$/);
    if (m && /^(faq|frequently\s+asked)/i.test(m[1].trim())) {
      start = i + 1;
      break;
    }
  }
  if (start === -1) return [];

  // Find the FAQ section end (next ## heading or EOF)
  let end = lines.length;
  for (let i = start; i < lines.length; i++) {
    if (/^##\s+/.test(lines[i])) { end = i; break; }
  }

  const section = lines.slice(start, end);
  const faqs: { question: string; answer: string }[] = [];

  // Detect H3 style first
  const hasH3 = section.some((l) => /^###\s+/.test(l));

  if (hasH3) {
    let current: { question: string; answer: string } | null = null;
    for (const line of section) {
      const h3 = line.match(/^###\s+(.+)$/);
      if (h3) {
        if (current) faqs.push(current);
        current = { question: h3[1].trim(), answer: '' };
      } else if (current) {
        const trimmed = line.trim();
        if (trimmed) current.answer += (current.answer ? ' ' : '') + trimmed;
      }
    }
    if (current) faqs.push(current);
  } else {
    // **Question?** then paragraphs
    let current: { question: string; answer: string } | null = null;
    for (const line of section) {
      const trimmed = line.trim();
      const boldQ = trimmed.match(/^\*\*(.+?)\*\*\s*$/);
      if (boldQ) {
        if (current) faqs.push(current);
        current = { question: boldQ[1].replace(/[:?]+$/, '').trim() + '?', answer: '' };
      } else if (current && trimmed) {
        // Strip markdown bold/italic/links to keep schema clean
        const cleaned = trimmed
          .replace(/\*\*(.+?)\*\*/g, '$1')
          .replace(/\*(.+?)\*/g, '$1')
          .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
        current.answer += (current.answer ? ' ' : '') + cleaned;
      }
    }
    if (current) faqs.push(current);
  }

  // Drop entries with no answer (truncated or malformed)
  return faqs.filter((f) => f.question && f.answer);
}

/** Render inline markdown: bold, code, images, links */
function inline(text: string): string {
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
  text = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" loading="lazy" class="inline-img" />');
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  text = text.replace(/\\\[/g, '[').replace(/\\\]/g, ']');
  return text;
}
