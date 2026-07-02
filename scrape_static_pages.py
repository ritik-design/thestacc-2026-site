#!/usr/bin/env python3
"""Scrape specific pages from current site and save as static files in public/."""
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

BASE = "https://thestacc.com"
USER_AGENT = "Stacc-Static-Migration/1.0"

PAGES = [
    "/lp/",
    "/lp/thankyou/",
    "/thankyou-stacc/",
    "/seo-automation-software/",
    "/social-media-automation-tool/",
]

PUBLIC_DIR = Path("public")


def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=60) as resp:
        return resp.read()


def fetch_text(url: str) -> str:
    return fetch(url).decode("utf-8", errors="replace")


ASSET_EXTS = (
    ".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif",
    ".mp4", ".webm", ".mov", ".pdf", ".woff", ".woff2", ".ttf", ".eot",
    ".ico", ".json", ".xml", ".txt", ".csv", ".zip", ".manifest"
)


def local_path_for_url(url: str) -> tuple[bool, str]:
    """Return (is_local, public_relative_path) for an asset URL."""
    parsed = urlparse(url)
    base_parsed = urlparse(BASE)

    if parsed.netloc and parsed.netloc != base_parsed.netloc:
        return False, ""

    path = parsed.path
    if not path or path == "/":
        return False, ""

    # Skip external schemes
    if parsed.scheme and parsed.scheme not in ("http", "https"):
        return False, ""

    # Only download actual asset files
    lower = path.lower()
    if not any(lower.endswith(ext) for ext in ASSET_EXTS):
        return False, ""

    # Ensure leading slash is removed for public/
    rel = path.lstrip("/")
    return True, rel


def download_asset(url: str, rel_path: str):
    """Download an asset to public/rel_path."""
    dest = PUBLIC_DIR / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    try:
        data = fetch(url)
        dest.write_bytes(data)
        print(f"  Downloaded: {rel_path} ({len(data)} bytes)")
    except Exception as e:
        print(f"  FAILED to download {url}: {e}")


def migrate_page(path: str) -> dict:
    """Download a page and its local assets, save to public/."""
    print(f"\nMigrating {path}")
    url = urljoin(BASE, path)
    html = fetch_text(url)
    soup = BeautifulSoup(html, "html.parser")

    assets = []

    # Find all local assets: link[href], script[src], img[src], source[src], video[poster]
    for tag in soup.find_all(["link", "script", "img", "source", "video", "audio"]):
        attr = "href" if tag.name == "link" else "src"
        if tag.name == "video":
            attr = "poster"
        value = tag.get(attr)
        if not value:
            continue

        is_local, rel_path = local_path_for_url(urljoin(url, value))
        if not is_local:
            continue

        assets.append({"tag": tag.name, "old": value, "rel": rel_path})
        asset_url = urljoin(BASE, value)
        download_asset(asset_url, rel_path)

    # Also find inline style background-image urls
    bg_urls = re.findall(r'url\(["\']?(/[^"\')\s]+)', html)
    for bg_url in bg_urls:
        is_local, rel_path = local_path_for_url(bg_url)
        if not is_local:
            continue
        assets.append({"tag": "inline-bg", "old": bg_url, "rel": rel_path})
        download_asset(urljoin(BASE, bg_url), rel_path)

    # Update asset paths to root-relative (they already are)
    # Save HTML to public/[path]/index.html
    dest_dir = PUBLIC_DIR / path.strip("/")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "index.html"

    # Clean up: remove Google Tag Manager / analytics if desired, or keep them
    # Keep everything as-is to preserve content exactly

    dest_file.write_text(html, encoding="utf-8")
    print(f"  Saved: {dest_file}")

    return {
        "path": path,
        "assets": len(assets),
        "dest": str(dest_file),
    }


def main():
    results = []
    for path in PAGES:
        results.append(migrate_page(path))

    summary = {
        "pages": len(results),
        "results": results,
    }
    Path("static-pages-migration.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nMigrated {len(results)} pages. Summary saved to static-pages-migration.json")


if __name__ == "__main__":
    main()
