"""Command line interface for migration analysis."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from framework.migration.analyzer import MigrationAnalyzer  # type: ignore[import-not-found]
else:
    from .analyzer import MigrationAnalyzer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze Odoo modules for migration to version 18")
    parser.add_argument('path', help="Module path to analyze")
    parser.add_argument('--from-version', choices=['15', '16', '17'], required=True, help="Source Odoo major version")
    parser.add_argument('--json', action='store_true', help="Output report in JSON format")
    parser.add_argument('--auto-fix', action='store_true', help="Allow safe auto-fixes during validation phase")
    return parser


def run_cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    analyzer = MigrationAnalyzer(args.from_version, auto_fix=args.auto_fix)
    report = analyzer.analyze(Path(args.path))

    if args.json:
        print(analyzer.to_json(report))
    else:
        counts = report.counts()
        print(f"Migration analysis for {report.root} (from {report.from_version} to {report.to_version})")
        print(f" - Errors:   {counts['errors']}")
        print(f" - Warnings: {counts['warnings']}")
        print(f" - Info:     {counts['info']}")
        print("\nIssues:")
        if report.issues:
            for issue in report.issues:
                location = f" ({issue.path})" if issue.path else ""
                print(f"[{issue.severity.upper()}] {issue.message}{location}")
                if issue.hint:
                    print(f"      ↳ {issue.hint}")
        else:
            print("  No issues detected by migration heuristics.")
        print("\nRecommended tasks:")
        for category, tasks in report.recommended_tasks.items():
            if not tasks:
                continue
            print(f" - {category.title()}:")
            for task in tasks:
                print(f"    • {task}")
    return 0


if __name__ == '__main__':
    raise SystemExit(run_cli())
