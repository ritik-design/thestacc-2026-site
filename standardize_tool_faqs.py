#!/usr/bin/env python3
"""Convert .tool-faq blocks on tool pages to the standard rankmath-style .faq-* markup."""

import re
from pathlib import Path

ROOT = Path("src/pages/tools")

TOOL_FAQ_RE = re.compile(
    r'<div\s+class="tool-faq">\s*'
    r'(\{faqs\.map\(\(faq\)\s*=>\s*\(\s*)'
    r'<div\s+class="tool-faq-item">\s*'
    r'<button\s+class="tool-faq-btn"\s+aria-expanded="false">\s*'
    r'(\{[^}]+\})\s*'
    r'<svg\s+class="tool-faq-icon"[^>]*>.*?</svg>\s*'
    r'</button>\s*'
    r'<div\s+class="tool-faq-answer">\s*'
    r'(.*?)\s*'
    r'</div>\s*'
    r'</div>\s*'
    r'(\)\)\}\s*)'
    r'</div>',
    re.DOTALL | re.IGNORECASE,
)

TOGGLE_SVG = '<span class="faq-toggle" aria-hidden="true"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>'


def rewrite_block(m):
    map_open = m.group(1)
    question_expr = m.group(2).strip()
    answer_content = m.group(3).strip()
    map_close = m.group(4)
    return (
        f'<div class="faq-list">\n'
        f'      {map_open}'
        f'<div class="faq-item">\n'
        f'          <button class="faq-q" onclick="toggleFaq(this)" aria-expanded="false">'
        f'<span class="faq-q-text">{question_expr}</span>{TOGGLE_SVG}</button>\n'
        f'          <div class="faq-a"><div class="faq-a-inner">{answer_content}</div></div>\n'
        f'        </div>\n'
        f'      {map_close}'
        f'    </div>'
    )


def main():
    changed = []
    for f in ROOT.rglob("*.astro"):
        text = f.read_text(encoding="utf-8")
        if "tool-faq" not in text:
            continue
        updated = TOOL_FAQ_RE.sub(rewrite_block, text)
        if updated != text:
            f.write_text(updated, encoding="utf-8")
            changed.append(f)
            print(f"UPDATED {f}")
    print(f"\nTotal files changed: {len(changed)}")


if __name__ == "__main__":
    main()
