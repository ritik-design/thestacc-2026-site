#!/usr/bin/env python3
"""
Recover missing blog images from the live thestacc.com site.
- For every /images/blog/ path that 404'd locally, try to find a live variant.
- Rewrite source references from the old filename to the live filename.
- Download the live file to public/ so the new filename resolves.
"""
import json
import os
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
LIVE = "https://thestacc.com"

def exists(path):
    url = f"{LIVE}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except Exception:
        return False

def download(rel):
    url = f"{LIVE}{rel}"
    target = os.path.join(ROOT, "public", rel.lstrip("/"))
    if os.path.exists(target):
        return True
    os.makedirs(os.path.dirname(target), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        with open(target, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"  download failed {rel}: {e}")
        return False

def find_variant(rel):
    """Return a live variant path, or None."""
    filename = rel.split("/")[-1]
    stem, ext = filename.rsplit(".", 1)
    # 1. same stem, alternate extension
    for e in ("webp", "jpg", "jpeg", "png"):
        if e == ext:
            continue
        cand = f"/images/blog/{stem}.{e}"
        if exists(cand):
            return cand
    # 2. remove last hyphen segment(s)
    parts = stem.split("-")
    for drop in range(1, min(3, len(parts))):
        shorter = "-".join(parts[:-drop])
        for e in ("webp", "jpg", "jpeg", "png"):
            cand = f"/images/blog/{shorter}.{e}"
            if exists(cand):
                return cand
    return None

def main():
    with open(os.path.join(ROOT, "broken_links.json")) as f:
        broken = json.load(f)
    missing = sorted({urlparse(b["url"]).path for b in broken if urlparse(b["url"]).path.startswith("/images/blog/")})
    print(f"Missing /images/blog/ files: {len(missing)}")

    # Find variants
    maps = {}
    unmapped = []
    def map_one(rel):
        var = find_variant(rel)
        return rel, var
    with ThreadPoolExecutor(max_workers=15) as ex:
        for rel, var in ex.map(map_one, missing):
            if var:
                maps[rel] = var
            else:
                unmapped.append(rel)

    print(f"  mapped to variants: {len(maps)}")
    print(f"  unmapped: {len(unmapped)}")
    for rel in unmapped:
        print(f"    UNMAPPED {rel}")

    # Download variant files
    print("\nDownloading variants...")
    for var in sorted(set(maps.values())):
        ok = download(var)
        print(f"  {'OK' if ok else 'FAIL'} {var}")

    # Rewrite source references
    print("\nRewriting source references...")
    src_files = []
    for dirpath, _, filenames in os.walk(os.path.join(ROOT, "src", "pages", "blog")):
        for fn in filenames:
            if fn.endswith(".astro") or fn.endswith(".md"):
                src_files.append(os.path.join(dirpath, fn))
    # Also check old markdown? New source is .astro only, but include .md just in case
    changed = 0
    for path in src_files:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        new_text = text
        for old_rel, new_rel in maps.items():
            new_text = new_text.replace(old_rel, new_rel)
        if new_text != text:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
            changed += 1
    print(f"  edited {changed} files")

    # Save mapping
    with open(os.path.join(ROOT, "image_recovery_map.json"), "w") as f:
        json.dump({"mapped": maps, "unmapped": unmapped}, f, indent=2)

if __name__ == "__main__":
    main()
