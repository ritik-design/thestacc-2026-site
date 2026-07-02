#!/usr/bin/env python3
"""Restore blog posts whose new versions lost content vs the old markdown.

Reads migration_audit_report.json and regenerates Astro pages from old markdown
for any post that falls below the configured thresholds. Preserves the new design
wrapper while restoring 100% of the original body content.
"""
import json
from pathlib import Path
import migrate_missing_posts as mp

ROOT = Path(__file__).parent
REPORT_FILE = ROOT / "migration_audit_report.json"

# Thresholds
WORD_LOSS_PCT = 0.15  # restore if new words < 85% of old words


def main():
    data = json.loads(REPORT_FILE.read_text(encoding="utf-8"))
    to_restore = []
    for r in data["all_reports"]:
        old_w = r.get("old_word_count")
        new_w = r.get("new_word_count")
        if old_w and new_w and new_w < old_w * (1 - WORD_LOSS_PCT):
            to_restore.append(r["slug"])

    print(f"Restoring {len(to_restore)} posts with >{WORD_LOSS_PCT*100:.0f}% word loss...")
    for slug in to_restore:
        mp.render_post(slug)
    print(f"\nDone. Restored {len(to_restore)} posts.")


if __name__ == "__main__":
    main()
