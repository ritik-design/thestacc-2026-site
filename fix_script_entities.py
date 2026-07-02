#!/usr/bin/env python3
"""Replace HTML-encoded braces inside <script> tags back to literal { }.

A migration/encoding step left `&#123;` and `&#125;` inside <script is:inline>
blocks, which breaks Astro's dev server. This script fixes only the content
inside <script> ... </script> tags and leaves other HTML untouched.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "src" / "pages"


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    def repl(match: re.Match) -> str:
        nonlocal changed
        script = match.group(0)
        fixed = script.replace("&#123;", "{").replace("&#125;", "}")
        if fixed != script:
            changed = True
        return fixed

    # Match <script> blocks (including attributes like is:inline)
    new_text = re.sub(r"<script[^>]*>.*?</script>", repl, text, flags=re.DOTALL)

    if changed:
        path.write_text(new_text, encoding="utf-8")
    return changed


def main():
    changed_files = []
    for path in ROOT.rglob("*.astro"):
        if fix_file(path):
            changed_files.append(path)

    print(f"Fixed {len(changed_files)} files")
    for p in changed_files[:10]:
        print(f"  - {p}")
    if len(changed_files) > 10:
        print(f"  ... and {len(changed_files) - 10} more")


if __name__ == "__main__":
    main()
