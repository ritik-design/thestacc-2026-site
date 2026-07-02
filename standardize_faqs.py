#!/usr/bin/env python3
"""Standardize FAQ markup across theStacc pages to the rankmath accordion style."""

import re
from pathlib import Path

ROOT = Path("src/pages")

def transform_old_faq(text: str) -> str:
    """Replace old .faq-question/.faq-answer/.faq-icon markup with rankmath style."""

    # Pattern for old question button
    # <button class="faq-question" onclick="toggleFaq(this)" aria-expanded="false">TEXT<span class="faq-icon">...</span></button>
    q_pattern = re.compile(
        r'<button\s+class="faq-question"\s+onclick="toggleFaq\(this\)"(?:\s+aria-expanded="false")?>'
        r'(.*?)'
        r'<span\s+class="faq-icon">\s*<svg>.*?</svg>\s*</span>\s*'
        r'</button>',
        re.DOTALL | re.IGNORECASE,
    )

    def replace_question(m):
        question = m.group(1).strip()
        # Clean up stray whitespace/newlines
        question = " ".join(question.split())
        return (
            '<button class="faq-q" onclick="toggleFaq(this)" aria-expanded="false">'
            f'<span class="faq-q-text">{question}</span>'
            '<span class="faq-toggle" aria-hidden="true">'
            '<svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg>'
            '</span></button>'
        )

    text = q_pattern.sub(replace_question, text)

    # Pattern for old answer div (capture content)
    a_pattern = re.compile(
        r'<div\s+class="faq-answer">(.*?</div>)',
        re.DOTALL | re.IGNORECASE,
    )

    def replace_answer(m):
        answer = m.group(1)
        # Strip trailing </div> that we captured greedily
        if answer.rstrip().endswith('</div>'):
            answer = answer[:-6].rstrip()
        answer = answer.strip()
        return f'<div class="faq-a"><div class="faq-a-inner">{answer}</div>'

    text = a_pattern.sub(replace_answer, text)
    return text


def main():
    files = list(ROOT.rglob("*.astro"))
    changed = []
    for f in files:
        try:
            original = f.read_text(encoding="utf-8")
        except Exception as e:
            print(f"SKIP {f}: {e}")
            continue
        if "faq-question" not in original and "faq-answer" not in original:
            continue
        updated = transform_old_faq(original)
        if updated != original:
            f.write_text(updated, encoding="utf-8")
            changed.append(f)
            print(f"UPDATED {f}")
    print(f"\nTotal files changed: {len(changed)}")


if __name__ == "__main__":
    main()
