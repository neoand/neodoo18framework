#!/usr/bin/env python3
"""
Minimal OCA watchlist inspector.
Purpose: load .neodoo/oca_watch.yml and print a compact summary.
No network calls; just validates structure and intended scope.
"""
from __future__ import annotations
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
WATCH = ROOT / ".neodoo" / "oca_watch.yml"

def main() -> int:
    if not WATCH.exists():
        print(f"Watchlist not found: {WATCH}")
        return 1
    if yaml is None:
        print("PyYAML is not installed. Please run: pip install -r requirements-dev.txt (in neodoo18framework)")
        return 2
    data = yaml.safe_load(WATCH.read_text(encoding="utf-8"))
    repos = data.get("repos", [])
    print(f"OCA watchlist: {len(repos)} repos configured")
    for r in repos:
        repo = r.get("repo")
        branch = r.get("branch")
        monitor = r.get("monitor")
        areas = ",".join(r.get("areas", [])) or "-"
        print(f"- {repo} [{branch}] via {monitor} | areas: {areas}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
