#!/usr/bin/env python3
"""Remove every border-radius declaration from CSS and inline styles."""

import re
from pathlib import Path

ROOT = Path(".")

def remove_from_css(text: str) -> str:
    """Strip border-radius declarations from CSS text."""
    # Match border-radius: <anything>;
    return re.sub(r'\s*border-radius\s*:\s*[^;]+!important\s*;|\s*border-radius\s*:\s*[^;]+\s*;', '', text, flags=re.IGNORECASE)

def remove_from_inline_styles(text: str) -> str:
    """Remove border-radius from inline style="..." attributes."""
    def clean_style(m):
        style = m.group(1)
        cleaned = re.sub(r'\s*border-radius\s*:\s*[^;]+!important\s*;?\s*|\s*border-radius\s*:\s*[^;]+\s*;?\s*', '', style, flags=re.IGNORECASE)
        cleaned = cleaned.strip()
        if not cleaned:
            return ''
        return f' style="{cleaned}"'
    return re.sub(r'\s?style="([^"]*)"', clean_style, text, flags=re.IGNORECASE)

def process_file(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    updated = original
    if path.suffix == '.css':
        updated = remove_from_css(updated)
    elif path.suffix == '.astro':
        updated = remove_from_inline_styles(updated)
        # Also remove border-radius from <style> blocks inside .astro files
        def clean_style_block(m):
            return f'<style{m.group(1)}>{remove_from_css(m.group(2))}</style>'
        updated = re.sub(r'<style([^>]*)>(.*?)</style>', clean_style_block, updated, flags=re.DOTALL | re.IGNORECASE)
    if updated != original:
        path.write_text(updated, encoding='utf-8')
        return True
    return False

def main():
    changed = []
    for ext in ('*.css', '*.astro'):
        for f in ROOT.rglob(ext):
            # Skip node_modules and dist
            if 'node_modules' in f.parts or 'dist' in f.parts:
                continue
            try:
                if process_file(f):
                    changed.append(f)
                    print(f"UPDATED {f}")
            except Exception as e:
                print(f"ERROR {f}: {e}")
    print(f"\nTotal files changed: {len(changed)}")

if __name__ == '__main__':
    main()
