"""Codebase analyzer to assist migrations to Odoo 18."""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .rules import DEPRECATED_DEPENDENCIES, LEGACY_DIRECTORIES, LEGACY_JS_PATTERNS, MIGRATION_TASKS
from framework.validator import Odoo18Validator


@dataclass
class MigrationIssue:
    severity: str  # "error", "warning", "info"
    message: str
    hint: Optional[str] = None
    path: Optional[Path] = None


@dataclass
class MigrationReport:
    root: Path
    from_version: str
    to_version: str
    issues: List[MigrationIssue] = field(default_factory=list)
    recommended_tasks: Dict[str, List[str]] = field(default_factory=lambda: {"mandatory": [], "manual": [], "optional": []})

    def add_issue(self, issue: MigrationIssue) -> None:
        self.issues.append(issue)

    def add_task(self, category: str, text: str) -> None:
        self.recommended_tasks.setdefault(category, []).append(text)

    def counts(self) -> Dict[str, int]:
        return {
            'errors': sum(1 for issue in self.issues if issue.severity == 'error'),
            'warnings': sum(1 for issue in self.issues if issue.severity == 'warning'),
            'info': sum(1 for issue in self.issues if issue.severity == 'info'),
        }


class MigrationAnalyzer:
    """High-level analyzer orchestrating multiple heuristic checks."""

    def __init__(self, from_version: str, *, to_version: str = "18", auto_fix: bool = False, strict: bool = True) -> None:
        self.from_version = from_version
        self.to_version = to_version
        self.auto_fix = auto_fix
        self.strict = strict
        self.validator = Odoo18Validator(auto_fix=auto_fix, strict=True, template_mode=False, verbose=False)

    # ------------------------------------------------------------------
    def analyze(self, path: Path) -> MigrationReport:
        root = path.resolve()
        report = MigrationReport(root=root, from_version=self.from_version, to_version=self.to_version)

        if not root.exists():
            report.add_issue(MigrationIssue('error', f"Path not found: {root}"))
            return report

        if root.is_file():
            self._analyze_file(root, report)
            return report

        # Directory analysis
        self._scan_manifest(root, report)
        self._scan_source(root, report)
        self._scan_validator(root, report)
        self._populate_tasks(report)
        return report

    # ------------------------------------------------------------------
    def _scan_manifest(self, root: Path, report: MigrationReport) -> None:
        manifest = root / '__manifest__.py'
        if not manifest.exists():
            report.add_issue(MigrationIssue('warning', "Missing __manifest__.py; cannot determine module metadata", path=manifest))
            return

        try:
            data = self._parse_manifest(manifest)
        except Exception as exc:
            report.add_issue(MigrationIssue('error', f"Failed to parse manifest: {exc}", path=manifest))
            return

        version = str(data.get('version', ''))
        if not version.startswith('18'):
            report.add_issue(MigrationIssue(
                'error',
                f"Manifest version '{version}' is not targeting 18.x",
                hint="Update the version key to 18.0.x and review changelog entries for intermediate versions.",
                path=manifest,
            ))

        depends = data.get('depends') or []
        if isinstance(depends, (list, tuple)):
            for dep in depends:
                if dep in DEPRECATED_DEPENDENCIES:
                    report.add_issue(MigrationIssue(
                        'warning',
                        f"Dependency '{dep}' is deprecated in Odoo 18",
                        hint=DEPRECATED_DEPENDENCIES[dep],
                        path=manifest,
                    ))
        else:
            report.add_issue(MigrationIssue('error', "'depends' must be a list", path=manifest))

        assets = data.get('assets') or {}
        if assets and isinstance(assets, dict):
            for bundle in assets.keys():
                if bundle.startswith('web.assets_'):
                    report.add_issue(MigrationIssue(
                        'warning',
                        f"Asset bundle '{bundle}' uses legacy naming",
                        hint="Adopt the web._assets_* bundles introduced with the new asset pipeline.",
                        path=manifest,
                    ))

    # ------------------------------------------------------------------
    def _scan_source(self, root: Path, report: MigrationReport) -> None:
        for legacy_dir in LEGACY_DIRECTORIES:
            candidate = root / legacy_dir
            if candidate.exists():
                report.add_issue(MigrationIssue(
                    'warning',
                    f"Legacy front-end directory detected: {legacy_dir}",
                    hint="Port widgets/QWeb templates to OWL 2/3 components.",
                    path=candidate,
                ))

        for file_path in root.glob('**/*'):
            if not file_path.is_file():
                continue
            suffix = file_path.suffix
            if suffix == '.js':
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if any(pattern in content for pattern in LEGACY_JS_PATTERNS):
                    report.add_issue(MigrationIssue(
                        'warning',
                        f"Legacy JS module system detected in {file_path.relative_to(root)}",
                        hint="Rewrite using the ES module/OWL pattern recommended for Odoo 18.",
                        path=file_path,
                    ))
            elif suffix == '.py':
                self._analyze_python(file_path, report)
            elif suffix == '.xml':
                self._analyze_xml(file_path, report)

    def _analyze_python(self, file_path: Path, report: MigrationReport) -> None:
        text = file_path.read_text(encoding='utf-8', errors='ignore')
        if '@api.one' in text or '@api.multi' in text:
            report.add_issue(MigrationIssue(
                'error',
                f"Deprecated decorator found in {file_path}",
                hint="Replace api.one/api.multi usage with api.depends/ensure_one patterns.",
                path=file_path,
            ))

        if re.search(r"\.cr\.execute\(.*format\(", text):
            report.add_issue(MigrationIssue(
                'warning',
                f"Manual SQL with python formatting detected in {file_path}",
                hint="Use parameterized queries or Odoo ORM to avoid SQL injection when migrating.",
                path=file_path,
            ))

        try:
            module = ast.parse(text)
        except SyntaxError:
            return
        for node in ast.walk(module):
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                if node.value.id == 'self' and node.attr == 'pool':
                    report.add_issue(MigrationIssue(
                        'warning',
                        f"Old API 'self.pool' reference in {file_path}",
                        hint="Old API helpers were removed long ago; refactor using env/model registries.",
                        path=file_path,
                    ))

    def _analyze_xml(self, file_path: Path, report: MigrationReport) -> None:
        text = file_path.read_text(encoding='utf-8', errors='ignore')
        if '<tree' in text:
            report.add_issue(MigrationIssue(
                'error',
                f"Deprecated <tree> tag found in {file_path}",
                hint="Replace with <list> and adjust arch attributes per Odoo 18 standards.",
                path=file_path,
            ))

    # ------------------------------------------------------------------
    def _scan_validator(self, root: Path, report: MigrationReport) -> None:
        results = self.validator.validate_directory(root)
        for result in results:
            severity = 'error' if not result.is_valid else 'warning'
            for msg in result.errors:
                report.add_issue(MigrationIssue('error', msg))
            for msg in result.warnings:
                report.add_issue(MigrationIssue('warning', msg))
            for msg in result.auto_fixes:
                report.add_issue(MigrationIssue('info', msg))

    # ------------------------------------------------------------------
    def _populate_tasks(self, report: MigrationReport) -> None:
        for task in MIGRATION_TASKS:
            if report.from_version in task.applies_to:
                report.add_task(task.category, f"{task.title} — {task.description}")

    # ------------------------------------------------------------------
    def to_dict(self, report: MigrationReport) -> Dict[str, object]:
        return {
            'root': str(report.root),
            'from_version': report.from_version,
            'to_version': report.to_version,
            'counts': report.counts(),
            'issues': [
                {
                    'severity': issue.severity,
                    'message': issue.message,
                    'hint': issue.hint,
                    'path': str(issue.path) if issue.path else None,
                }
                for issue in report.issues
            ],
            'tasks': report.recommended_tasks,
        }

    def to_json(self, report: MigrationReport, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(report), indent=indent)

    # ------------------------------------------------------------------
    def _analyze_file(self, file_path: Path, report: MigrationReport) -> None:
        suffix = file_path.suffix
        if suffix == '.py':
            self._analyze_python(file_path, report)
        elif suffix == '.xml':
            self._analyze_xml(file_path, report)
        elif suffix == '.js':
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            if any(pattern in content for pattern in LEGACY_JS_PATTERNS):
                report.add_issue(MigrationIssue('warning', f"Legacy JS module system detected in {file_path}", path=file_path))
        else:
            report.add_issue(MigrationIssue('info', f"No migration rules for {file_path.suffix} files"))

    # ------------------------------------------------------------------
    def _parse_manifest(self, manifest: Path) -> Dict[str, object]:
        text = manifest.read_text(encoding='utf-8')
        module = ast.parse(text, filename=str(manifest))
        for node in module.body:
            if isinstance(node, ast.Assign):
                value = getattr(node, 'value', None)
                if isinstance(value, ast.Dict):
                    return ast.literal_eval(value)
            if isinstance(node, ast.Expr) and isinstance(getattr(node, 'value', None), ast.Dict):
                return ast.literal_eval(node.value)
        raise ValueError("Manifest must assign a dict to a variable or expose a dict literal")
