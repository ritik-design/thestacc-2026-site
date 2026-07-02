#!/usr/bin/env python3
"""
Escape raw { and } inside <code> and <pre> blocks in blog pages so Astro
does not interpret them as expression delimiters.
"""
import os
import re
from glob import glob

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
files = glob(os.path.join(ROOT, "src/pages/blog/*/index.astro"))

def escape_braces_in_tag(match):
    tag = match.group(0)
    # Replace raw braces with numeric entities, but not those already part of entities
    tag = re.sub(r"(?<!&)\{", "&#123;", tag)
    tag = re.sub(r"(?<!&)\}", "&#125;", tag)
    return tag

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # Split frontmatter
    if not text.startswith("---"):
        continue
    end_fm = text.find("\n---", 3)
    if end_fm == -1:
        continue
    fm = text[:end_fm+4]
    body = text[end_fm+4:]
    # Process <code>...</code> and <pre>...</pre> blocks
    body = re.sub(r"<code[^>]*>.*?</code>", escape_braces_in_tag, body, flags=re.S)
    body = re.sub(r"<pre[^>]*>.*?</pre>", escape_braces_in_tag, body, flags=re.S)
    new_text = fm + body
    if new_text != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        print(f"fixed: {os.path.basename(os.path.dirname(path))}")
