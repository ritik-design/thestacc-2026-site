#!/usr/bin/env python3
import re, os, glob

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site/src/pages/blog"

def sanitize_file(path):
    text = open(path, encoding="utf-8").read()
    original = text
    # Remove Markdown header anchor markers like {#ch1}, {#section-title}
    text = re.sub(r'\{#[^}]+\}', '', text)

    def sanitize_code_inner(inner):
        # Strip any nested HTML tags and return plain, escaped text.
        from bs4 import BeautifulSoup
        plain = BeautifulSoup(inner, 'html.parser').get_text()
        # Escape HTML-significant characters so Astro does not parse code as markup.
        plain = plain.replace('&', '&amp;')
        plain = plain.replace('<', '&lt;')
        plain = plain.replace('>', '&gt;')
        # Escape Astro expression braces.
        plain = plain.replace('{', '&#123;')
        plain = plain.replace('}', '&#125;')
        return plain

    def sanitize_code_block(m):
        return '<pre><code>' + sanitize_code_inner(m.group(1)) + '</code></pre>'

    def sanitize_inline_code(m):
        return '<code>' + sanitize_code_inner(m.group(1)) + '</code>'

    # Block <pre><code>...</code></pre>
    text = re.sub(r'<pre><code[^>]*>(.*?)</code></pre>', sanitize_code_block, text, flags=re.DOTALL)
    # Inline <code>...</code>
    text = re.sub(r'<code[^>]*>(.*?)</code>', sanitize_inline_code, text, flags=re.DOTALL)

    if text != original:
        open(path, "w", encoding="utf-8").write(text)
        return True
    return False

def main():
    files = glob.glob(os.path.join(ROOT, "*/index.astro"))
    changed = []
    for path in files:
        try:
            if sanitize_file(path):
                changed.append(path)
        except Exception as e:
            print(f"Error on {path}: {e}")
    print(f"Sanitized {len(changed)} files")

if __name__ == "__main__":
    main()
