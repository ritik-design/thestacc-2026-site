#!/usr/bin/env python3
"""Restore every blog post from old markdown to guarantee 100% content preservation."""
from pathlib import Path
import migrate_missing_posts as mp

ROOT = Path(__file__).parent
OLD_BLOG = ROOT / "Old Website" / "src" / "content" / "blog"


def main():
    slugs = [p.stem for p in OLD_BLOG.glob("*.md")]
    print(f"Restoring all {len(slugs)} blog posts from old markdown...")
    for slug in slugs:
        mp.render_post(slug)
    print(f"Done. Restored {len(slugs)} posts.")


if __name__ == "__main__":
    main()
