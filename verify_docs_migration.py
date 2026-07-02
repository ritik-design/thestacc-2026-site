#!/usr/bin/env python3
"""Verify migrated docs pages match original content."""
import json
import re
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from pathlib import Path

BASE = "https://thestacc.com"
PAGES_FILE = Path("src/data/docs/pages.json")
REPORT_FILE = Path("docs-verification-report.md")


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "Stacc-Docs-Verify/1.0"})
    with urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def normalize_text(text: str) -> str:
    """Normalize text for comparison: lowercase, collapse whitespace, remove # anchor chars."""
    text = text.replace("#", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def main():
    with open(PAGES_FILE) as f:
        pages = json.load(f)

    results = []
    for page in pages:
        path = page["path"]
        slug = page["slug"]
        new_file = Path(f"dist/docs/{slug}/index.html")
        url = urljoin(BASE, path)

        result = {
            "path": path,
            "slug": slug,
            "title": page["title"],
            "new_file_exists": new_file.exists(),
        }

        if not new_file.exists():
            result["status"] = "MISSING_FILE"
            results.append(result)
            continue

        try:
            old_html = fetch(url)
            old_soup = BeautifulSoup(old_html, "html.parser")
            old_content = old_soup.find("div", class_="docs-content")
            old_title = old_soup.title.string if old_soup.title else ""
            old_title = re.sub(r"\s*- theStacc Docs\s*$", "", old_title).strip()

            new_html = new_file.read_text(encoding="utf-8")
            new_soup = BeautifulSoup(new_html, "html.parser")
            new_content = new_soup.find("div", class_="docs-body")
            new_title = new_soup.title.string if new_soup.title else ""
            new_title = re.sub(r"\s*- theStacc Docs\s*$", "", new_title).strip()

            title_match = old_title.lower() == new_title.lower() or page["title"].lower() == new_title.lower()

            if old_content and new_content:
                old_text = normalize_text(old_content.get_text())
                new_text = normalize_text(new_content.get_text())
                # Compare word counts
                old_wc = word_count(old_text)
                new_wc = word_count(new_text)
                ratio = new_wc / old_wc if old_wc else 1

                result["old_word_count"] = old_wc
                result["new_word_count"] = new_wc
                result["word_ratio"] = round(ratio, 3)
                result["title_match"] = title_match

                if ratio < 0.9 or ratio > 1.1 or not title_match:
                    result["status"] = "REVIEW"
                    result["note"] = f"word ratio {ratio:.2f}, title match {title_match}"
                else:
                    result["status"] = "OK"
            else:
                result["status"] = "NO_CONTENT"
        except Exception as e:
            result["status"] = "ERROR"
            result["error"] = str(e)

        results.append(result)

    ok = [r for r in results if r["status"] == "OK"]
    review = [r for r in results if r["status"] == "REVIEW"]
    errors = [r for r in results if r["status"] in ("MISSING_FILE", "NO_CONTENT", "ERROR")]

    report = f"""# Docs Migration Verification Report

Generated: auto
Total docs pages: {len(pages)}
- OK: {len(ok)}
- Needs review: {len(review)}
- Errors: {len(errors)}

## Summary

| Status | Count |
|--------|-------|
| OK | {len(ok)} |
| Review | {len(review)} |
| Missing file | {len([r for r in errors if r['status'] == 'MISSING_FILE'])} |
| No content | {len([r for r in errors if r['status'] == 'NO_CONTENT'])} |
| Error | {len([r for r in errors if r['status'] == 'ERROR'])} |

"""

    if review:
        report += "## Pages needing review\n\n"
        for r in review:
            report += f"- `{r['path']}` — {r.get('note', '')}\n"
            if "old_word_count" in r:
                report += f"  - Old words: {r['old_word_count']}, New words: {r['new_word_count']}\n"
            report += f"  - Title match: {r.get('title_match', 'N/A')}\n"

    if errors:
        report += "\n## Errors\n\n"
        for r in errors:
            report += f"- `{r['path']}` — {r['status']}: {r.get('error', '')}\n"

    REPORT_FILE.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nReport saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()
