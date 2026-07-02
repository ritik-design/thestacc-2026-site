#!/usr/bin/env python3
"""Update src/pages/blog/index.astro with actual existing blog posts.

The current index hardcodes slugs that no longer exist, causing 404s.
This script scans src/pages/blog/, extracts metadata from each post's
frontmatter, and rewrites the featured + posts arrays in the index.
"""
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
BLOG_DIR = ROOT / "src" / "pages" / "blog"
INDEX_FILE = BLOG_DIR / "index.astro"


def extract_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm = text[3:end]

    title_match = re.search(r'title:\s*"([^"]+)"', fm)
    desc_match = re.search(r'description:\s*"([^"]+)"', fm)
    date_match = re.search(r'"datePublished":\s*"([^"]+)"', fm)
    # Match the author object inside schemaData Article (comes after datePublished)
    author_match = re.search(
        r'"datePublished":\s*"[^"]+",\s*"dateModified":\s*"[^"]+",\s*"author":\s*\{\s*"@type":\s*"Person",\s*"name":\s*"([^"]+)"',
        fm,
        re.DOTALL,
    )

    title = title_match.group(1) if title_match else ""
    title = re.sub(r"\s*\|\s*theStacc\s*$", "", title)

    return {
        "slug": path.parent.name,
        "title": title,
        "excerpt": desc_match.group(1) if desc_match else "",
        "date": date_match.group(1) if date_match else "2026-01-01",
        "author": author_match.group(1) if author_match else "theStacc team",
    }


def infer_category(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ["local", "gbp", "map pack", "citation", "review", "franchise", "multi-location"]):
        return "Local SEO"
    if any(k in t for k in ["ai agent", "ai search", "perplexity", "chatgpt", "llm", "ai overviews", "gemini", "claude"]):
        return "AI Search"
    if any(k in t for k in ["content", "blog", "writing", "programmatic", "brief", "pillar", "article"]):
        return "Content Strategy"
    return "SEO Tips"


def format_post(p: dict) -> str:
    return (
        f"  {{ slug: '{p['slug']}, cat: '{p['category']}, title: '{p['title']}, "
        f"excerpt: '{p['excerpt']}, author: '{p['author']}, date: '{p['date']}, readTime: '{p['readTime']}' }}"
    )


def escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def main():
    posts = []
    for post_file in sorted(BLOG_DIR.glob("*/index.astro")):
        data = extract_frontmatter(post_file)
        if not data["title"]:
            continue
        data["category"] = infer_category(data["title"])
        data["readTime"] = "7 min"
        posts.append(data)

    # Sort by date descending
    posts.sort(key=lambda x: x["date"], reverse=True)

    if not posts:
        print("No posts found.")
        return

    # Prefer a featured post that isn't an error-code or generic guide slug
    excluded_featured = {'404-error-seo', '301-redirects-guide', '5x-content-output-ai'}
    featured_candidates = [p for p in posts if p['slug'] not in excluded_featured]
    featured = featured_candidates[0] if featured_candidates else posts[0]
    # Build the grid from the remaining posts, keeping sort order
    grid = [p for p in posts if p['slug'] != featured['slug']][:12]

    def fmt(p):
        return (
            f"{{ slug: '{escape(p['slug'])}', cat: '{escape(p['category'])}', "
            f"title: '{escape(p['title'])}', excerpt: '{escape(p['excerpt'])}', "
            f"author: '{escape(p['author'])}', date: '{p['date']}', readTime: '{p['readTime']}' }}"
        )

    new_index = INDEX_FILE.read_text(encoding="utf-8")

    # Replace featured block
    featured_block = (
        f"const featured = {fmt(featured)};\n"
        f"featured.readTime = '11 min';\n"
    )
    new_index = re.sub(
        r"const featured = \{[\s\S]*?\};",
        f"const featured = {fmt(featured)};",
        new_index,
        count=1,
    )

    # Replace posts array
    posts_array = "const posts = [\n" + ",\n".join(f"  {fmt(p)}" for p in grid) + "\n];\n"
    new_index = re.sub(
        r"const posts = \[[\s\S]*?\];",
        posts_array.rstrip(),
        new_index,
        count=1,
    )

    INDEX_FILE.write_text(new_index, encoding="utf-8")
    print(f"Updated {INDEX_FILE}")
    print(f"Featured: {featured['slug']}")
    print(f"Grid posts ({len(grid)}):")
    for p in grid:
        print(f"  - {p['slug']}")


if __name__ == "__main__":
    main()
