#!/usr/bin/env python3
"""Download missing /images/blog/* assets from the live thestacc.com site."""
import json
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from urllib.request import urlopen, Request

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
BROKEN_JSON = os.path.join(ROOT, "broken_links.json")
TARGET_DIR = os.path.join(ROOT, "public", "images", "blog")
LIVE_BASE = "https://thestacc.com"

def download(rel_path):
    live_url = f"{LIVE_BASE}{rel_path}"
    target = os.path.join(ROOT, "public", rel_path.lstrip("/"))
    if os.path.exists(target):
        return (rel_path, "exists")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    req = Request(live_url, headers={"User-Agent": "migration-recovery/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                return (rel_path, f"HTTP {resp.status}")
            data = resp.read()
        with open(target, "wb") as f:
            f.write(data)
        return (rel_path, "downloaded")
    except Exception as e:
        return (rel_path, f"ERROR {type(e).__name__}: {e}")

def main():
    with open(BROKEN_JSON) as f:
        data = json.load(f)
    rels = sorted({urlparse(item["url"]).path for item in data if item["url"].startswith("http://localhost:7777/images/blog/")})
    print(f"Downloading {len(rels)} missing /images/blog/ files to {TARGET_DIR}")
    os.makedirs(TARGET_DIR, exist_ok=True)
    results = {"downloaded": 0, "exists": 0, "failed": []}
    with ThreadPoolExecutor(max_workers=20) as executor:
        for rel, status in executor.map(download, rels):
            if status == "downloaded":
                results["downloaded"] += 1
            elif status == "exists":
                results["exists"] += 1
            elif status.startswith("ERROR") or status.startswith("HTTP"):
                results["failed"].append((rel, status))
            print(f"{status}: {rel}")
    print(f"\nDone. Downloaded {results['downloaded']}, already existed {results['exists']}, failed {len(results['failed'])}")
    if results["failed"]:
        for rel, status in results["failed"][:20]:
            print(f"  FAIL {rel}: {status}")

if __name__ == "__main__":
    main()
