#!/usr/bin/env python3
"""Audit blog migration: compare old markdown content vs new Astro pages.

Reports per-post and aggregate metrics for word count, headings, images,
internal/external links, and FAQ counts. Flags posts with significant loss.
"""
import re
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent
OLD_BLOG = ROOT / "Old Website" / "src" / "content" / "blog"
NEW_BLOG = ROOT / "src" / "pages" / "blog"
DIST_BLOG = ROOT / "dist" / "blog"

REPORT_FILE = ROOT / "migration_audit_report.json"


def old_slug_to_path(slug: str) -> Path:
    return OLD_BLOG / f"{slug}.md"


def new_slug_to_path(slug: str) -> Path:
    return NEW_BLOG / slug / "index.astro"


def extract_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 3 :]
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


def extract_astro_body(text: str) -> str:
    """Return the rendered-HTML-like body of an Astro file.

    Strips frontmatter, then removes JSX expressions and some Astro-specific
    syntax. The result is HTML-ish text we can count from.
    """
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            text = text[end + 3 :]
    # Remove JSX map expressions loosely by replacing `{...}` blocks that span
    # multiple lines with a space. This is intentionally simple.
    text = re.sub(r"\{[\s\S]*?\}", " ", text)
    return text


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def count_headings_md(text: str) -> int:
    return len(re.findall(r"^#{1,6} ", text, flags=re.MULTILINE))


def count_headings_html(text: str) -> int:
    return len(re.findall(r"<h[1-6][^>]*>", text, flags=re.IGNORECASE))


def count_images_md(text: str) -> int:
    return len(re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text))


def count_images_html(text: str) -> int:
    return len(re.findall(r"<img[^>]*>", text, flags=re.IGNORECASE))


def count_links_md(text: str) -> tuple[int, int]:
    internal = external = 0
    for _, url in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", text):
        if url.startswith("http") or url.startswith("//"):
            external += 1
        elif url.strip():
            internal += 1
    return internal, external


def count_links_html(text: str) -> tuple[int, int]:
    internal = external = 0
    for match in re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', text, flags=re.IGNORECASE):
        url = match.strip()
        if url.startswith("http") or url.startswith("//") or url.startswith("mailto:"):
            if not url.startswith("mailto:"):
                external += 1
        elif url and not url.startswith("#"):
            internal += 1
    return internal, external


def count_faqs_md(text: str) -> int:
    # Old format likely uses ## FAQ or ### Q / A pattern. Count FAQ schema mentions.
    return len(re.findall(r"@type\":\s*\"FAQPage", text)) + len(
        re.findall(r"^#{1,3} .*\?$", text, flags=re.MULTILINE)
    )


def count_faqs_html(text: str) -> int:
    return len(re.findall(r'<div class="faq-item"', text)) + len(
        re.findall(r'"@type":\s*"Question"', text)
    )


def analyze_post(slug: str) -> dict:
    old_path = old_slug_to_path(slug)
    new_path = new_slug_to_path(slug)
    dist_path = DIST_BLOG / slug / "index.html"

    result = {
        "slug": slug,
        "old_exists": old_path.exists(),
        "new_exists": new_path.exists(),
        "dist_exists": dist_path.exists(),
    }

    if old_path.exists():
        old_text = old_path.read_text(encoding="utf-8")
        old_fm, old_body = extract_frontmatter(old_text)
        result["old_title"] = old_fm.get("title", "")
        result["old_word_count"] = count_words(old_body)
        result["old_headings"] = count_headings_md(old_body)
        result["old_images"] = count_images_md(old_body)
        result["old_links_internal"], result["old_links_external"] = count_links_md(old_body)
        result["old_faqs"] = count_faqs_md(old_body)
    else:
        result["old_exists"] = False

    if new_path.exists():
        new_text = new_path.read_text(encoding="utf-8")
        new_body = extract_astro_body(new_text)
        result["new_word_count"] = count_words(new_body)
        result["new_headings"] = count_headings_html(new_body)
        result["new_images"] = count_images_html(new_body)
        result["new_links_internal"], result["new_links_external"] = count_links_html(new_body)
        result["new_faqs"] = count_faqs_html(new_body)
    else:
        result["new_exists"] = False

    return result


def main():
    old_slugs = {p.stem for p in OLD_BLOG.glob("*.md")}
    new_slugs = {p.name for p in NEW_BLOG.iterdir() if p.is_dir()}

    missing_in_new = sorted(old_slugs - new_slugs)
    missing_in_old = sorted(new_slugs - old_slugs)

    reports = []
    for slug in sorted(old_slugs):
        reports.append(analyze_post(slug))

    # Aggregate stats
    total_old_words = sum(r.get("old_word_count", 0) for r in reports if "old_word_count" in r)
    total_new_words = sum(r.get("new_word_count", 0) for r in reports if "new_word_count" in r)

    word_loss_posts = [
        r for r in reports
        if "old_word_count" in r and "new_word_count" in r and r["new_word_count"] < r["old_word_count"] * 0.85
    ]
    heading_loss_posts = [
        r for r in reports
        if "old_headings" in r and "new_headings" in r and r["new_headings"] < r["old_headings"]
    ]
    image_loss_posts = [
        r for r in reports
        if "old_images" in r and "new_images" in r and r["new_images"] < r["old_images"]
    ]

    summary = {
        "old_post_count": len(old_slugs),
        "new_post_count": len(new_slugs),
        "missing_in_new": missing_in_new,
        "missing_in_old": missing_in_old,
        "total_old_words": total_old_words,
        "total_new_words": total_new_words,
        "word_difference": total_new_words - total_old_words,
        "posts_with_word_loss_over_15pct": len(word_loss_posts),
        "posts_with_heading_loss": len(heading_loss_posts),
        "posts_with_image_loss": len(image_loss_posts),
    }

    output = {
        "summary": summary,
        "word_loss_posts": [
            {
                "slug": r["slug"],
                "old_words": r.get("old_word_count"),
                "new_words": r.get("new_word_count"),
                "loss_pct": round((1 - r["new_word_count"] / r["old_word_count"]) * 100, 1),
            }
            for r in word_loss_posts
        ],
        "heading_loss_posts": [
            {"slug": r["slug"], "old_headings": r.get("old_headings"), "new_headings": r.get("new_headings")}
            for r in heading_loss_posts
        ],
        "image_loss_posts": [
            {"slug": r["slug"], "old_images": r.get("old_images"), "new_images": r.get("new_images")}
            for r in image_loss_posts
        ],
        "all_reports": reports,
    }

    REPORT_FILE.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"\nDetailed report written to {REPORT_FILE}")


if __name__ == "__main__":
    main()
