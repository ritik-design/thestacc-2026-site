#!/usr/bin/env python3
"""Scrape all docs pages from current thestacc.com and prepare data for Astro migration."""
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

BASE = "https://thestacc.com"
DOCS_DIR = Path("src/data/docs")
PAGES_FILE = DOCS_DIR / "pages.json"
NAV_FILE = DOCS_DIR / "navigation.json"
TRACKING_FILE = Path("docs-migration-tracking.md")

USER_AGENT = "Stacc-Docs-Migration/1.0"


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def slug_from_path(path: str) -> str:
    """Convert /docs/foo/bar/ to foo/bar."""
    return path.strip("/").replace("docs/", "", 1)


def normalize_doc_link(href: str, current_slug: str) -> str:
    """Make internal docs links work with trailing-slash Astro site."""
    if not href or href.startswith("http") or href.startswith("mailto:") or href.startswith("#"):
        return href
    if href.startswith("/docs/"):
        # Ensure trailing slash
        href = href.rstrip("/") + "/"
        return href
    return href


def extract_page(url: str, path: str) -> dict:
    """Scrape a single docs page."""
    print(f"  Scraping {path}")
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string if soup.title else ""
    # Strip " - theStacc Docs" suffix
    title = re.sub(r"\s*- theStacc Docs\s*$", "", title).strip()

    content_div = soup.find("div", class_="docs-content")
    if not content_div:
        print(f"    WARNING: No docs-content div found for {path}")
        content_html = ""
    else:
        # Remove script tags if any
        for script in content_div.find_all("script"):
            script.decompose()
        # Fix internal doc links
        for a in content_div.find_all("a", href=True):
            a["href"] = normalize_doc_link(a["href"], slug_from_path(path))
        # Add IDs to headings for TOC if missing
        for heading in content_div.find_all(["h2", "h3", "h4"]):
            if not heading.get("id"):
                text = heading.get_text(strip=True).replace("#", "").strip()
                heading_id = re.sub(r"[^\w\s-]", "", text).strip().lower()
                heading_id = re.sub(r"[-\s]+", "-", heading_id)
                heading["id"] = heading_id
        content_html = str(content_div.decode_contents())

    # Extract headings for TOC
    headings = []
    if content_div:
        for h in content_div.find_all(["h2", "h3", "h4"]):
            text = h.get_text(strip=True).replace("#", "").strip()
            hid = h.get("id", "")
            if text:
                headings.append({"level": int(h.name[1]), "text": text, "id": hid})

    return {
        "path": path,
        "slug": slug_from_path(path),
        "title": title,
        "contentHtml": content_html,
        "headings": headings,
    }


def extract_navigation(soup: BeautifulSoup) -> list:
    """Extract docs navigation structure from any docs page."""
    sections = []
    for section in soup.find_all("div", class_="docs-nav-section"):
        heading_div = section.find("div", class_="docs-nav-heading")
        heading = heading_div.get_text(strip=True) if heading_div else ""
        items = []
        items_div = section.find("div", class_="docs-nav-items")
        if items_div:
            for a in items_div.find_all("a"):
                href = a.get("href", "")
                if href.startswith("/docs/"):
                    href = href.rstrip("/") + "/"
                items.append({
                    "title": a.get_text(strip=True),
                    "href": href,
                })
        sections.append({"heading": heading, "items": items})
    return sections


def main():
    # Get list of docs pages from sitemap comparison
    with open("sitemap_comparison.json") as f:
        data = json.load(f)

    docs_paths = sorted([p for p in data["missing_pages"] if p.startswith("/docs/")])
    print(f"Found {len(docs_paths)} docs pages to scrape")

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # Scrape first page to get navigation
    first_url = urljoin(BASE, docs_paths[0])
    first_html = fetch(first_url)
    first_soup = BeautifulSoup(first_html, "html.parser")
    navigation = extract_navigation(first_soup)
    NAV_FILE.write_text(json.dumps(navigation, indent=2), encoding="utf-8")
    print(f"Navigation saved: {len(navigation)} sections")

    # Scrape all pages
    pages = []
    errors = []
    for path in docs_paths:
        url = urljoin(BASE, path)
        try:
            page = extract_page(url, path)
            pages.append(page)
        except Exception as e:
            print(f"    ERROR scraping {path}: {e}")
            errors.append({"path": path, "error": str(e)})
        time.sleep(0.2)

    PAGES_FILE.write_text(json.dumps(pages, indent=2), encoding="utf-8")
    print(f"\nScraped {len(pages)} pages, {len(errors)} errors")

    # Write tracking file
    tracking = f"""# Docs Migration Tracking

Started: {time.strftime("%Y-%m-%d %H:%M:%S")}
Source: {BASE}
Total docs pages: {len(docs_paths)}
Scraped successfully: {len(pages)}
Errors: {len(errors)}

## Navigation sections
"""
    for section in navigation:
        tracking += f"\n### {section['heading'] or '(no heading)'}\n"
        for item in section["items"]:
            status = "✅" if any(p["path"].rstrip("/") == item["href"].rstrip("/") for p in pages) else "❌"
            tracking += f"- {status} [{item['title']}]({item['href']})\n"

    if errors:
        tracking += "\n## Errors\n"
        for e in errors:
            tracking += f"- {e['path']}: {e['error']}\n"

    TRACKING_FILE.write_text(tracking, encoding="utf-8")
    print(f"Tracking file written: {TRACKING_FILE}")


if __name__ == "__main__":
    main()
