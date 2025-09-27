#!/usr/bin/env python3
"""
Weekly OCA digests rollup generator.

Scans docs/oca-digests/ for entries updated in the last 7 days and aggregates
them into docs/oca-digests/rollups/YYYY-Www.md with a simple table of contents
and per-repo sections. Intended to be run via GitHub Actions weekly.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIGESTS_DIR = ROOT / "docs" / "oca-digests"
ROLLUPS_DIR = DIGESTS_DIR / "rollups"


def iso_week_key(date: dt.date) -> str:
    y, w, _ = date.isocalendar()
    return f"{y}-W{w:02d}"


def find_recent_digests(days: int = 7) -> list[Path]:
    cutoff = dt.datetime.utcnow() - dt.timedelta(days=days)
    files: list[Path] = []
    if not DIGESTS_DIR.exists():
        return files
    for p in DIGESTS_DIR.glob("OCA-*.md"):
        try:
            mtime = dt.datetime.utcfromtimestamp(p.stat().st_mtime)
            if mtime >= cutoff:
                files.append(p)
        except FileNotFoundError:
            continue
    return sorted(files)


def extract_sections(md: str) -> dict[str, str]:
    # Headings like: ## OCA/some-repo (YYYY-MM-DD)
    sections: dict[str, str] = {}
    parts = re.split(r"^## \\[(?P<repo>[^\]]+)\]\([^\)]+\)\s*$", md, flags=re.M)
    # re.split yields [pre, repo1, body1, repo2, body2, ...]
    if parts[1:]:
        pass
    else:
        return sections
    it = iter(parts[1:])
    for repo, body in zip(it, it):
        repo = repo.strip()
        sections.setdefault(repo, "")
        sections[repo] += body.strip() + "\n\n"
    return sections


def build_rollup_md(week_key: str, collected: dict[str, str], files: list[Path]) -> str:
    date_range = f"week {week_key}"
    lines = [
        f"# OCA Weekly Rollup - {date_range}",
        "",
        "This rollup aggregates OCA digests updated in the last 7 days.",
        "",
        "## Table of Contents",
    ]
    for repo in sorted(collected.keys()):
        anchor = repo.lower().replace("/", "-")
        lines.append(f"- [{repo}](#{anchor})")

    lines.append("")
    for repo in sorted(collected.keys()):
        anchor = repo.lower().replace("/", "-")
        lines.append(f"## {repo}")
        lines.append("")
        lines.append(collected[repo].strip())
        lines.append("")

    if files:
        lines.append("---")
        lines.append("")
        lines.append("Sources:")
        for p in files:
            rel = p.relative_to(ROOT)
            lines.append(f"- {rel}")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate weekly OCA digests rollup")
    parser.add_argument("--days", type=int, default=7, help="Window size in days (default 7)")
    args = parser.parse_args()

    recent = find_recent_digests(days=args.days)
    collected: dict[str, str] = {}
    for p in recent:
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        sections = extract_sections(text)
        for repo, body in sections.items():
            collected.setdefault(repo, "")
            collected[repo] += body

    today = dt.date.today()
    week_key = iso_week_key(today)
    ROLLUPS_DIR.mkdir(parents=True, exist_ok=True)
    out = ROLLUPS_DIR / f"{week_key}.md"
    md = build_rollup_md(week_key, collected, recent)
    out.write_text(md, encoding="utf-8")
    print(f"Wrote rollup: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
