#!/usr/bin/env python3
"""Compare page inventories between current thestacc.com and new Astro site."""
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import urlopen, Request

SITES = {
    "old": {"base": "https://thestacc.com", "max_pages": 5000},
    "new": {"base": "http://localhost:8888", "max_pages": 5000},
}

USER_AGENT = "Stacc-Migration-Audit/1.0"
STATIC_EXTS = (
    ".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif",
    ".mp4", ".pdf", ".woff", ".woff2", ".ttf", ".eot", ".ico", ".xml",
    ".json", ".txt", ".zip", ".csv"
)


class LinkExtractor(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base = base_url
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("a", "link") and attrs.get("href"):
            self.links.append(urljoin(self.base, attrs["href"]))


def normalize_path(base: str, url: str) -> str:
    """Return a normalized path for comparison."""
    parsed = urlparse(url)
    base_parsed = urlparse(base)
    if parsed.netloc and parsed.netloc != base_parsed.netloc:
        return None
    path = parsed.path or "/"
    # Collapse trailing index.html
    path = re.sub(r"/index\.html$", "/", path)
    # Ensure root is /
    if path == "" or path == "index.html":
        path = "/"
    # Strip trailing slash for comparison set? Keep consistent.
    # We keep trailing slash if present, but also store slashless variant.
    return path


def equivalent_paths(path: str) -> set:
    """Return variants of a path for fuzzy matching."""
    variants = {path}
    if path.endswith("/") and path != "/":
        variants.add(path.rstrip("/"))
    else:
        variants.add(path + "/")
    # Remove .html suffix variants
    if path.endswith(".html"):
        variants.add(path[:-5])
        variants.add(path[:-5] + "/")
    return variants


def is_html_url(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path
    if any(path.lower().endswith(ext) for ext in STATIC_EXTS):
        return False
    return True


def fetch(url: str, timeout: int = 30):
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=timeout) as resp:
            ctype = resp.headers.get("Content-Type", "")
            body = resp.read()
            return resp.status, ctype, body
    except Exception as e:
        return type(e).__name__, "", str(e).encode("utf-8")


def crawl_site(name: str, base: str, max_pages: int):
    visited = set()
    to_visit = {base + "/"}
    broken = []
    errors = []
    pages = {}  # normalized path -> {url, status, title?}

    def check(url: str):
        url = urldefrag(url)[0]
        norm = normalize_path(base, url)
        if norm is None:
            return None
        if norm in visited:
            return None
        visited.add(norm)

        status, ctype, body = fetch(url)
        if isinstance(status, str) or status >= 400:
            broken.append((url, status))
            return None

        title = ""
        if b"<title>" in body.lower():
            m = re.search(rb"<title[^>]*>(.*?)</title>", body, re.S | re.I)
            if m:
                title = m.group(1).decode("utf-8", errors="replace").strip()

        pages[norm] = {"url": url, "status": status, "title": title, "content_type": ctype}

        if "text/html" in ctype and len(visited) < max_pages:
            try:
                html = body.decode("utf-8", errors="replace")
                extractor = LinkExtractor(url)
                extractor.feed(html)
                for link in extractor.links:
                    link = urldefrag(link)[0]
                    if not is_html_url(link):
                        continue
                    link_norm = normalize_path(base, link)
                    if link_norm and link_norm not in visited and len(visited) < max_pages:
                        to_visit.add(link)
            except Exception as e:
                errors.append((url, str(e)))
        return status

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = set()
        while to_visit and len(visited) < max_pages:
            batch = []
            while to_visit and len(batch) < 16:
                batch.append(to_visit.pop())
            for url in batch:
                futures.add(executor.submit(check, url))
            for fut in as_completed(futures):
                futures.remove(fut)
                # refill if possible
                while to_visit and len(futures) < 16:
                    futures.add(executor.submit(check, to_visit.pop()))
                if not to_visit and not futures:
                    break

    return pages, broken, errors


def categorize(path: str) -> str:
    if path == "/":
        return "homepage"
    parts = [p for p in path.strip("/").split("/") if p]
    if not parts:
        return "homepage"
    first = parts[0].lower()
    mapping = {
        "blog": "blog",
        "glossary": "glossary",
        "best": "best",
        "alternatives": "alternatives",
        "reviews": "reviews",
        "tools": "tools",
        "features": "features",
        "solutions": "solutions",
        "for": "for",
        "integrations": "integrations",
        "case-studies": "case-studies",
        "legal": "legal",
        "about": "about",
        "pricing": "pricing",
        "contact": "contact",
        "demo": "demo",
        "authors": "authors",
        "affiliates": "affiliates",
        "compare": "compare",
        "lp": "lp",
        "thank-you": "thank-you",
        "thankyou": "thank-you",
        "page": "paginated",
    }
    return mapping.get(first, "other")


def main():
    results = {}
    for name, cfg in SITES.items():
        print(f"\n=== Crawling {name}: {cfg['base']} ===")
        start = time.time()
        pages, broken, errors = crawl_site(name, cfg["base"], cfg["max_pages"])
        elapsed = time.time() - start
        results[name] = {"pages": pages, "broken": broken, "errors": errors}
        print(f"Crawled {len(pages)} pages in {elapsed:.1f}s")
        print(f"Broken/errors: {len(broken)} broken, {len(errors)} errors")

    old_pages = results["old"]["pages"]
    new_pages = results["new"]["pages"]

    # Build fuzzy match sets
    old_norm = set(old_pages.keys())
    new_norm = set(new_pages.keys())

    # For each old page, check if any equivalent variant exists in new
    covered = set()
    missing = []
    for path in sorted(old_norm):
        variants = equivalent_paths(path)
        if variants & new_norm:
            covered.add(path)
        else:
            missing.append(path)

    # Extra pages in new (not matching any old variant)
    extra = []
    for path in sorted(new_norm):
        variants = equivalent_paths(path)
        if not (variants & old_norm):
            extra.append(path)

    # Categorize
    missing_by_cat = {}
    for p in missing:
        cat = categorize(p)
        missing_by_cat.setdefault(cat, []).append(p)

    extra_by_cat = {}
    for p in extra:
        cat = categorize(p)
        extra_by_cat.setdefault(cat, []).append(p)

    old_by_cat = {}
    for p in old_norm:
        cat = categorize(p)
        old_by_cat.setdefault(cat, 0)
        old_by_cat[cat] += 1

    new_by_cat = {}
    for p in new_norm:
        cat = categorize(p)
        new_by_cat.setdefault(cat, 0)
        new_by_cat[cat] += 1

    coverage_pct = len(covered) / len(old_norm) * 100 if old_norm else 0

    report = {
        "old_total": len(old_norm),
        "new_total": len(new_norm),
        "covered": len(covered),
        "missing": len(missing),
        "extra": len(extra),
        "coverage_pct": round(coverage_pct, 2),
        "old_by_category": old_by_cat,
        "new_by_category": new_by_cat,
        "missing_by_category": {k: len(v) for k, v in missing_by_cat.items()},
        "extra_by_category": {k: len(v) for k, v in extra_by_cat.items()},
        "missing_pages": missing,
        "extra_pages": extra,
        "old_broken": [(u, str(s)) for u, s in results["old"]["broken"]],
        "new_broken": [(u, str(s)) for u, s in results["new"]["broken"]],
    }

    with open("site_inventory_comparison.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 60)
    print("INVENTORY COMPARISON SUMMARY")
    print("=" * 60)
    print(f"Current site (thestacc.com): {len(old_norm)} pages")
    print(f"New site (localhost:8888):   {len(new_norm)} pages")
    print(f"Pages covered in new site:   {len(covered)} ({coverage_pct:.1f}%)")
    print(f"Pages missing from new site: {len(missing)}")
    print(f"Extra pages in new site:     {len(extra)}")
    print(f"\nOld site broken/errors:      {len(results['old']['broken'])}")
    print(f"New site broken/errors:      {len(results['new']['broken'])}")

    print("\n--- Coverage by category ---")
    all_cats = sorted(set(old_by_cat.keys()) | set(new_by_cat.keys()))
    print(f"{'Category':<20} {'Old':>8} {'New':>8} {'Missing':>8}")
    for cat in all_cats:
        old_c = old_by_cat.get(cat, 0)
        new_c = new_by_cat.get(cat, 0)
        miss_c = len(missing_by_cat.get(cat, []))
        print(f"{cat:<20} {old_c:>8} {new_c:>8} {miss_c:>8}")

    print("\n--- Top missing categories ---")
    for cat, pages in sorted(missing_by_cat.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"{cat}: {len(pages)} pages")
        for p in pages[:5]:
            print(f"  - {p}")
        if len(pages) > 5:
            print(f"  ... and {len(pages)-5} more")

    print("\n--- Top extra categories ---")
    for cat, pages in sorted(extra_by_cat.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"{cat}: {len(pages)} pages")
        for p in pages[:5]:
            print(f"  - {p}")
        if len(pages) > 5:
            print(f"  ... and {len(pages)-5} more")

    print(f"\nDetailed report saved to site_inventory_comparison.json")


if __name__ == "__main__":
    main()
