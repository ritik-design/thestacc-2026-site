#!/usr/bin/env python3
"""Normalize internal page links to trailing-slash form for Astro static routes."""
from pathlib import Path
import re

ROOT = Path('src')
# Route prefixes that are directory-based static routes in the new site.
# We will add a trailing slash to links like /blog/slug -> /blog/slug/
PREFIXES = (
    '/blog/',
    '/glossary/',
    '/reviews/',
    '/alternatives/',
    '/best/',
    '/compare/',
    '/for/',
    '/tools/',
    '/authors/',
    '/case-studies/',
    '/features/',
    '/modules/',
    '/solutions/',
    '/integrations/',
    '/legal/',
    '/white-label-seo/',
    '/white-label-local-seo/',
    '/white-label-reporting/',
    '/seo-reseller/',
    '/local-seo-software/',
    '/multi-location-seo/',
    '/rank-tracking-software/',
    '/google-maps-ranking/',
)

# Regex to match an href attribute value
href_re = re.compile(r'href=["\']([^"\']+)["\']')


def should_add_slash(url: str) -> bool:
    # Skip external/mailto/tel/anchor-only
    if url.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', '//')):
        return False
    if not url.startswith('/'):
        return False
    # Skip if already has trailing slash
    if url.endswith('/'):
        return False
    # Skip file assets
    if re.search(r'\.[a-zA-Z0-9]+(?:\?|$)', url):
        return False
    # Skip if has query or hash in the path part
    if '?' in url or '#' in url:
        return False
    # Must match one of our known prefixes
    if not any(url.startswith(p) for p in PREFIXES):
        return False
    return True


def fix_file(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    original = text
    changed = 0

    def repl(m: re.Match) -> str:
        nonlocal changed
        quote = m.group(0)[5]  # ' or "
        url = m.group(1)
        if should_add_slash(url):
            changed += 1
            return f'href={quote}{url}/{quote}'
        return m.group(0)

    new_text = href_re.sub(repl, text)
    if new_text != original:
        path.write_text(new_text, encoding='utf-8')
    return changed


def main():
    total = 0
    files = 0
    for f in ROOT.rglob('*.astro'):
        n = fix_file(f)
        if n:
            files += 1
            total += n
    print(f'Fixed {total} links in {files} files')


if __name__ == '__main__':
    main()
