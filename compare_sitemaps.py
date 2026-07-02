#!/usr/bin/env python3
"""Compare sitemap URL inventories between current thestacc.com and new Astro site."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen, Request

OLD_SITEMAP = "https://thestacc.com/sitemap-0.xml"
NEW_SITEMAP = Path("dist/sitemap-0.xml")


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "Stacc-Migration-Audit/1.0"})
    with urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def parse_sitemap(xml: str) -> set:
    """Extract normalized paths from sitemap XML."""
    urls = re.findall(r"<loc>([^<]+)</loc>", xml)
    paths = set()
    for url in urls:
        parsed = urlparse(url)
        path = parsed.path or "/"
        # Normalize
        path = re.sub(r"/index\.html$", "/", path)
        if path == "":
            path = "/"
        paths.add(path)
    return paths


def equivalent_paths(path: str) -> set:
    """Return variants of a path for fuzzy matching."""
    variants = {path}
    if path.endswith("/") and path != "/":
        variants.add(path.rstrip("/"))
    else:
        variants.add(path + "/")
    if path.endswith(".html"):
        variants.add(path[:-5])
        variants.add(path[:-5] + "/")
    return variants


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
        "use-cases": "use-cases",
    }
    return mapping.get(first, "other")


def main():
    print("Fetching old site sitemap...")
    old_xml = fetch(OLD_SITEMAP)
    old_paths = parse_sitemap(old_xml)

    print("Reading new site sitemap...")
    new_xml = NEW_SITEMAP.read_text(encoding="utf-8")
    new_paths = parse_sitemap(new_xml)

    # Fuzzy matching
    covered = set()
    missing = []
    for path in sorted(old_paths):
        if equivalent_paths(path) & new_paths:
            covered.add(path)
        else:
            missing.append(path)

    extra = []
    for path in sorted(new_paths):
        if not (equivalent_paths(path) & old_paths):
            extra.append(path)

    coverage_pct = len(covered) / len(old_paths) * 100 if old_paths else 0

    # Categorize
    def count_by_cat(paths):
        cats = {}
        for p in paths:
            cat = categorize(p)
            cats[cat] = cats.get(cat, 0) + 1
        return cats

    old_by_cat = count_by_cat(old_paths)
    new_by_cat = count_by_cat(new_paths)

    missing_by_cat = {}
    for p in missing:
        cat = categorize(p)
        missing_by_cat[cat] = missing_by_cat.get(cat, 0) + 1

    extra_by_cat = {}
    for p in extra:
        cat = categorize(p)
        extra_by_cat[cat] = extra_by_cat.get(cat, 0) + 1

    report = {
        "old_total": len(old_paths),
        "new_total": len(new_paths),
        "covered": len(covered),
        "missing": len(missing),
        "extra": len(extra),
        "coverage_pct": round(coverage_pct, 2),
        "old_by_category": old_by_cat,
        "new_by_category": new_by_cat,
        "missing_by_category": missing_by_cat,
        "extra_by_category": extra_by_cat,
        "missing_pages": sorted(missing),
        "extra_pages": sorted(extra),
    }

    with open("sitemap_comparison.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 70)
    print("SITEMAP COMPARISON: thestacc.com vs new Astro site")
    print("=" * 70)
    print(f"Current site (thestacc.com): {len(old_paths):,} URLs")
    print(f"New site (dist build):       {len(new_paths):,} URLs")
    print(f"Pages covered in new site:   {len(covered):,} ({coverage_pct:.1f}%)")
    print(f"Pages missing from new site: {len(missing):,}")
    print(f"Extra pages in new site:     {len(extra):,}")

    print("\n--- URLs by category ---")
    all_cats = sorted(set(old_by_cat.keys()) | set(new_by_cat.keys()))
    print(f"{'Category':<22} {'Old':>8} {'New':>8} {'Missing':>8} {'Extra':>8}")
    for cat in all_cats:
        old_c = old_by_cat.get(cat, 0)
        new_c = new_by_cat.get(cat, 0)
        miss_c = missing_by_cat.get(cat, 0)
        ext_c = extra_by_cat.get(cat, 0)
        print(f"{cat:<22} {old_c:>8} {new_c:>8} {miss_c:>8} {ext_c:>8}")

    print("\n--- Missing categories (top) ---")
    for cat, count in sorted(missing_by_cat.items(), key=lambda x: -x[1])[:15]:
        print(f"  {cat}: {count}")

    print("\n--- Extra categories (top) ---")
    for cat, count in sorted(extra_by_cat.items(), key=lambda x: -x[1])[:15]:
        print(f"  {cat}: {count}")

    print("\n--- Sample missing pages ---")
    for p in missing[:30]:
        print(f"  {p}")

    print("\n--- Sample extra pages ---")
    for p in extra[:30]:
        print(f"  {p}")

    print(f"\nDetailed report saved to sitemap_comparison.json")


if __name__ == "__main__":
    main()
