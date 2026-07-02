#!/usr/bin/env python3
"""Convert scraped docs JSON into individual Astro Content Collection markdown files."""
import json
import re
from pathlib import Path

PAGES_FILE = Path("src/data/docs/pages.json")
CONTENT_DIR = Path("src/content/docs")


def escape_frontmatter_value(value: str) -> str:
    """Escape a string for YAML frontmatter."""
    value = value.replace("\\", "\\\\")
    if '"' in value or "\n" in value or value.startswith(("'", '"')):
        value = value.replace('"', '\\"')
        return f'"{value}"'
    return value


def main():
    with open(PAGES_FILE) as f:
        pages = json.load(f)

    # Remove existing docs content
    if CONTENT_DIR.exists():
        import shutil
        shutil.rmtree(CONTENT_DIR)
    CONTENT_DIR.mkdir(parents=True)

    for page in pages:
        slug = page["slug"]
        title = page["title"]
        html = page["contentHtml"]
        description = page.get("description", "")

        # Convert slug path to file path: account/billing -> account/billing.md
        file_path = CONTENT_DIR / f"{slug}.md"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        frontmatter = f"""---
title: {escape_frontmatter_value(title)}
slug: {slug}
---

{html}
"""
        file_path.write_text(frontmatter, encoding="utf-8")

    print(f"Created {len(pages)} markdown files in {CONTENT_DIR}")


if __name__ == "__main__":
    main()
