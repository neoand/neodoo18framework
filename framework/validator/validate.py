#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Neodoo18Framework - Pluggable Odoo 18+ validator."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Iterable, List, Optional

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from framework.validator.plugin import ValidationContext, ValidationResult  # type: ignore[import-not-found]
    from framework.validator.plugin_manager import PluginManager  # type: ignore[import-not-found]
    from framework.validator.plugins import CoreRulesPlugin  # type: ignore[import-not-found]
else:
    from .plugin import ValidationContext, ValidationResult
    from .plugin_manager import PluginManager
    from .plugins import CoreRulesPlugin

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class Odoo18Validator:
    """Coordinates validator plugins and aggregates results."""

    def __init__(
        self,
        *,
        auto_fix: bool = False,
        strict: bool = False,
        template_mode: bool = False,
        verbose: bool = False,
        plugin_dirs: Optional[Iterable[Path]] = None,
    ) -> None:
        self.auto_fix = auto_fix
        self.strict = strict
        self.template_mode = template_mode
        self.verbose = verbose

        self.plugin_manager = PluginManager()
        self.plugin_manager.register(CoreRulesPlugin())

        directories: List[Path] = []
        env_dirs = os.environ.get("NEODOO_VALIDATOR_PLUGINS", "")
        if env_dirs:
            directories.extend(
                Path(entry).expanduser()
                for entry in env_dirs.split(os.pathsep)
                if entry.strip()
            )

        if plugin_dirs:
            directories.extend(Path(directory) for directory in plugin_dirs)

        for directory in directories:
            self.plugin_manager.load_directory(directory)

        for error in self.plugin_manager.load_errors:
            logger.warning(error)

    # ------------------------------------------------------------------
    def list_plugins(self) -> List[str]:
        return self.plugin_manager.describe_plugins()

    # ------------------------------------------------------------------
    def validate_file(self, file_path: Path) -> List[ValidationResult]:
        if not file_path.exists():
            res = ValidationResult()
            res.add_error(f"File not found: {file_path}")
            return [res]

        context = ValidationContext(
            root=file_path,
            auto_fix=self.auto_fix,
            strict=self.strict,
            template_mode=self.template_mode,
            verbose=self.verbose,
            module_name=self._infer_module_name(file_path),
        )

        for plugin in self.plugin_manager.plugins:
            plugin.setup(context)

        results: List[ValidationResult] = []
        for plugin in self.plugin_manager.plugins:
            if not plugin.supports(file_path, context):
                continue
            result = plugin.validate_file(file_path, context)
            if result and (result.has_messages() or self.verbose):
                results.append(result)

        for plugin in self.plugin_manager.plugins:
            for result in plugin.finalize(context):
                if result and (result.has_messages() or self.verbose):
                    results.append(result)

        return results

    # ------------------------------------------------------------------
    def validate_directory(self, directory_path: Path) -> List[ValidationResult]:
        if not directory_path.exists() or not directory_path.is_dir():
            res = ValidationResult()
            res.add_error(f"Directory not found: {directory_path}")
            return [res]

        context = ValidationContext(
            root=directory_path,
            auto_fix=self.auto_fix,
            strict=self.strict,
            template_mode=self.template_mode,
            verbose=self.verbose,
            module_name=directory_path.name,
        )

        for plugin in self.plugin_manager.plugins:
            plugin.setup(context)

        results: List[ValidationResult] = []

        for plugin in self.plugin_manager.plugins:
            for result in plugin.validate_directory(directory_path, context):
                if result and (result.has_messages() or self.verbose):
                    results.append(result)

        for path in sorted(directory_path.glob('**/*')):
            if not path.is_file():
                continue
            for plugin in self.plugin_manager.plugins:
                if not plugin.supports(path, context):
                    continue
                result = plugin.validate_file(path, context)
                if result and (result.has_messages() or self.verbose):
                    results.append(result)

        for plugin in self.plugin_manager.plugins:
            for result in plugin.finalize(context):
                if result and (result.has_messages() or self.verbose):
                    results.append(result)

        return results

    # ------------------------------------------------------------------
    def _infer_module_name(self, file_path: Path) -> Optional[str]:
        cur = file_path if file_path.is_dir() else file_path.parent
        for _ in range(5):
            manifest = cur / '__manifest__.py'
            if manifest.exists():
                return cur.name
            if cur.parent == cur:
                break
            cur = cur.parent
        parts = list(file_path.parts)
        if 'models' in parts:
            try:
                index = parts.index('models')
                return Path(*parts[:index]).name
            except Exception:
                pass
        return file_path.parent.name if file_path.parent else None


# ----------------------------------------------------------------------

def _summarise_results(results: List[ValidationResult], verbose: bool) -> bool:
    valid = all(result.is_valid for result in results)
    error_count = sum(len(result.errors) for result in results)
    warning_count = sum(len(result.warnings) for result in results)
    fix_count = sum(len(result.auto_fixes) for result in results)

    if not valid:
        logger.error(f"Validation failed: {error_count} errors, {warning_count} warnings")
    elif warning_count:
        logger.warning(f"Validation passed with {warning_count} warnings")
    else:
        logger.info("Validation passed")

    if verbose or not valid:
        for result in results:
            for message in result.errors:
                logger.error(f"  - {message}")
            for message in result.warnings:
                logger.warning(f"  - {message}")
            for message in result.auto_fixes:
                logger.info(f"  ✓ {message}")

    if fix_count:
        logger.info(f"Applied {fix_count} auto-fixes")

    return valid


def validate_path(
    path_str: str,
    *,
    auto_fix: bool = False,
    verbose: bool = False,
    strict: bool = False,
    template_mode: bool = False,
    plugin_dirs: Optional[Iterable[str]] = None,
) -> bool:
    path = Path(path_str)
    validator = Odoo18Validator(
        auto_fix=auto_fix,
        strict=strict,
        template_mode=template_mode,
        verbose=verbose,
        plugin_dirs=[Path(p) for p in plugin_dirs] if plugin_dirs else None,
    )

    results = (
        validator.validate_directory(path)
        if path.is_dir()
        else validator.validate_file(path)
    )

    return _summarise_results(results, verbose)


def main() -> None:
    parser = argparse.ArgumentParser(description="Neodoo18Framework Universal Validator")
    parser.add_argument('path', nargs='?', help="File or directory to validate")
    parser.add_argument('--auto-fix', action='store_true', help="Auto-fix issues when possible")
    parser.add_argument('--verbose', '-v', action='store_true', help="Show detailed validation information")
    parser.add_argument('--strict', action='store_true', help="Enable strict mode (promote selected warnings to errors)")
    parser.add_argument('--template-mode', action='store_true', help="Permit template placeholders and missing optional files as warnings")
    parser.add_argument('--plugins-dir', action='append', default=[], help="Additional directory to load validator plugins from")
    parser.add_argument('--list-plugins', action='store_true', help="List available validator plugins and exit")

    args = parser.parse_args()

    validator = Odoo18Validator(
        auto_fix=args.auto_fix,
        strict=args.strict,
        template_mode=args.template_mode,
        verbose=args.verbose,
        plugin_dirs=[Path(p) for p in args.plugins_dir] if args.plugins_dir else None,
    )

    if args.list_plugins:
        print("Available validator plugins:")
        for line in validator.list_plugins():
            print(f" - {line}")
        if validator.plugin_manager.load_errors:
            print("\nPlugin load issues:")
            for err in validator.plugin_manager.load_errors:
                print(f" - {err}")
        sys.exit(0)

    if not args.path:
        parser.error("path is required unless --list-plugins is provided")

    success = validate_path(
        args.path,
        auto_fix=args.auto_fix,
        verbose=args.verbose,
        strict=args.strict,
        template_mode=args.template_mode,
        plugin_dirs=args.plugins_dir,
    )

    if success:
        logger.info("✅ Validation successful!")
        sys.exit(0)
    else:
        logger.error("❌ Validation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
