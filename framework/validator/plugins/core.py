"""Core Odoo 18+ validation rules implemented as a plugin."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..plugin import BaseValidatorPlugin, ValidationContext, ValidationResult


class CoreRulesPlugin(BaseValidatorPlugin):
    name = "core_rules"
    description = "Built-in Odoo 18+ compliance checks"

    def __init__(self) -> None:
        self.module_name: Optional[str] = None
        self.xml_rules = {
            'deprecated_tree': {
                'pattern': r'<tree\s',
                'replacement': '<list ',
                'message': 'Use <list> instead of <tree> in Odoo 18+'
            },
            'deprecated_tree_close': {
                'pattern': r'</tree>',
                'replacement': '</list>',
                'message': 'Use </list> instead of </tree> in Odoo 18+'
            },
            'deprecated_view_mode': {
                'pattern': r'view_mode["\'].*tree',
                'replacement': lambda m: m.group(0).replace('tree', 'list'),
                'message': 'Use "list" instead of "tree" in view_mode for Odoo 18+'
            }
        }

    # ------------------------------------------------------------------
    def setup(self, context: ValidationContext) -> None:
        if context.module_name:
            self.module_name = context.module_name
        else:
            self.module_name = context.root.name

    def supports(self, file_path: Path, context: ValidationContext) -> bool:
        return file_path.suffix in {'.py', '.xml'} or file_path.name == '__manifest__.py'

    def validate_directory(self, directory: Path, context: ValidationContext) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        module_name = directory.name
        if not re.match(r'^[a-z][a-z0-9_]*$', module_name):
            res = ValidationResult()
            res.add_error(f"Module directory '{module_name}' must be snake_case (lowercase, digits, underscores)")
            results.append(res)

        has_access_csv = False
        access_csv_path: Optional[Path] = None
        for path in directory.glob('**/*'):
            if path.name == 'ir.model.access.csv':
                has_access_csv = True
                access_csv_path = path
                break

        if not has_access_csv:
            res = ValidationResult()
            if context.template_mode:
                res.add_warning(f"Missing ir.model.access.csv in {directory}")
            else:
                res.add_error(f"Missing ir.model.access.csv in {directory}")
            results.append(res)
        elif access_csv_path is not None:
            try:
                header = access_csv_path.read_text(encoding='utf-8').splitlines()[0].strip()
                expected = 'id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink'
                if header.replace(' ', '') != expected:
                    res = ValidationResult()
                    message = f"{access_csv_path}: Unexpected CSV header. Expected '{expected}'"
                    if context.strict and not context.template_mode:
                        res.add_error(message)
                    else:
                        res.add_warning(message)
                    results.append(res)
            except Exception as exc:
                res = ValidationResult()
                res.add_warning(f"{access_csv_path}: Could not read header ({exc})")
                results.append(res)

        results.extend(self._check_models_init(directory))
        return results

    def validate_file(self, file_path: Path, context: ValidationContext) -> Optional[ValidationResult]:
        if file_path.name == '__manifest__.py':
            return self._validate_manifest(file_path, context)
        if file_path.suffix == '.xml':
            return self._validate_xml(file_path, context)
        if file_path.suffix == '.py':
            return self._validate_python(file_path, context)
        return None

    # ------------------------------------------------------------------
    def _validate_xml(self, file_path: Path, context: ValidationContext) -> ValidationResult:
        result = ValidationResult()
        try:
            content = file_path.read_text(encoding='utf-8')

            for rule_name, rule in self.xml_rules.items():
                if re.search(rule['pattern'], content):
                    result.add_error(f"{rule['message']} in {file_path}")
                    if context.auto_fix and 'replacement' in rule:
                        replacement = rule['replacement']
                        if callable(replacement):
                            new_content = re.sub(rule['pattern'], replacement, content)
                        else:
                            new_content = re.sub(rule['pattern'], rule['replacement'], content)
                        file_path.write_text(new_content, encoding='utf-8')
                        result.add_auto_fix(f"Fixed {rule_name} in {file_path}")
                        content = new_content

            if 'ir.actions.act_window' in content:
                for match in re.finditer(r'<field\s+name=["\']view_mode["\']>([^<]+)</field>', content):
                    modes = match.group(1).strip()
                    if 'list' not in modes:
                        self._warn_or_error(result, context, f"Action view_mode without 'list' in {file_path}: '{modes}'", strict_as_error=False)
                    if 'list' in modes and 'form' not in modes:
                        self._warn_or_error(result, context, f"Action view_mode should include 'form' with 'list' in {file_path}: '{modes}'", strict_as_error=False)

            module_prefix = (self.module_name or '').strip()
            if module_prefix:
                for match in re.finditer(r'<record\s+id=["\']([^"\']+)["\']', content):
                    rec_id = match.group(1)
                    if not rec_id.startswith(f"{module_prefix}_"):
                        self._warn_or_error(result, context, f"XML record id '{rec_id}' should be prefixed with '{module_prefix}_' ({file_path})", strict_as_error=False)
        except Exception as exc:
            result.add_error(f"Error processing {file_path}: {exc}")
        return result

    def _validate_python(self, file_path: Path, context: ValidationContext) -> ValidationResult:
        result = ValidationResult()
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            if not re.search(r'# -\*- coding: utf-8 -\*-', content):
                result.add_error(f"Missing UTF-8 encoding declaration in {file_path}")
                if context.auto_fix:
                    if lines and lines[0].startswith('#!'):
                        lines.insert(1, '# -*- coding: utf-8 -*-')
                    else:
                        lines.insert(0, '# -*- coding: utf-8 -*-')
                    file_path.write_text('\n'.join(lines), encoding='utf-8')
                    result.add_auto_fix(f"Added UTF-8 encoding to {file_path}")
                    content = '\n'.join(lines)

            for match in re.finditer(r'def (_compute_[^(]*)\(self', content):
                method_name = match.group(1)
                method_pos = match.start()
                preceding_lines = content[max(0, method_pos - 200):method_pos]
                if not re.search(r'@api\.depends', preceding_lines):
                    result.add_error(f"Missing @api.depends for {method_name} in {file_path}")

            if '_name' in content and 'models.Model' in content:
                for match in re.finditer(r'class\s+(\w+)\(models\.Model\)', content):
                    class_name = match.group(1)
                    class_pos = match.start()
                    next_lines = content[class_pos:class_pos + 500]
                    has_name = re.search(r'_name\s*=', next_lines)
                    has_description = re.search(r'_description\s*=', next_lines)
                    if has_name and not has_description:
                        result.add_error(f"Model {class_name} has _name but missing _description in {file_path}")

            for i, line in enumerate(lines, start=1):
                if re.search(r'^\s*print\(', line):
                    self._warn_or_error(result, context, f"Avoid print() in code ({file_path}:{i}); use _logger instead", strict_as_error=not context.template_mode)
                if 'pdb.set_trace' in line or re.search(r'^\s*breakpoint\(', line):
                    self._warn_or_error(result, context, f"Debug statements (pdb/breakpoint) found in {file_path}:{i}", strict_as_error=True)

            for match in re.finditer(r'def\s+(action_\w+|button_\w+)\(self[^\)]*\):', content):
                start = match.end()
                tail = content[start:]
                stop_match = re.search(r'\n\s*def\s|\n\s*class\s', tail)
                body = tail[:stop_match.start()] if stop_match else tail
                if 'self.ensure_one()' not in body:
                    self._warn_or_error(result, context, f"Method {match.group(1)} should call self.ensure_one() in {file_path}", strict_as_error=False)
        except Exception as exc:
            result.add_error(f"Error processing {file_path}: {exc}")
        return result

    def _validate_manifest(self, file_path: Path, context: ValidationContext) -> ValidationResult:
        result = ValidationResult()
        try:
            manifest = self._parse_manifest(file_path)
            if manifest is None:
                result.add_error(f"{file_path}: Manifest must be a top-level dict")
                return result

            for key in ['name', 'version', 'depends', 'data']:
                if key not in manifest:
                    result.add_error(f"{file_path}: Missing required manifest key '{key}'")

            version = str(manifest.get('version', ''))
            if not version.startswith('18.0.'):
                result.add_warning(f"{file_path}: Version should start with '18.0.' (found '{version}')")

            depends = manifest.get('depends')
            if not isinstance(depends, (list, tuple)):
                result.add_error(f"{file_path}: 'depends' must be a list")

            data_files = manifest.get('data') or []
            for rel in data_files:
                if not isinstance(rel, str):
                    continue
                path = file_path.parent / rel
                if not path.exists():
                    message = f"{file_path}: Listed data file not found: {rel}"
                    if context.strict:
                        result.add_error(message)
                    else:
                        result.add_warning(message)

            if not manifest.get('license'):
                result.add_error(f"{file_path}: Missing 'license' in manifest")
            installable = manifest.get('installable')
            if installable is False or installable is None:
                result.add_error(f"{file_path}: 'installable' must be True for Odoo 18+ modules")

            access_rel = 'security/ir.model.access.csv'
            access_file = file_path.parent / access_rel
            if access_file.exists():
                listed = access_rel in (manifest.get('data') or []) or access_rel in (manifest.get('security') or [])
                message = f"{file_path}: {access_rel} exists but is not listed in manifest 'data' or 'security'"
                if not listed:
                    if context.strict:
                        result.add_error(message)
                    else:
                        result.add_warning(message)
        except Exception as exc:
            result.add_error(f"Error validating manifest {file_path}: {exc}")
        return result

    # ------------------------------------------------------------------
    def _warn_or_error(self, result: ValidationResult, context: ValidationContext, message: str, *, strict_as_error: bool) -> None:
        if strict_as_error and context.strict:
            result.add_error(message)
        else:
            result.add_warning(message)

    def _parse_manifest(self, file_path: Path) -> Optional[Dict[str, Any]]:
        text = file_path.read_text(encoding='utf-8')
        node = ast.parse(text, filename=str(file_path))
        manifest_node: Optional[ast.Dict] = None
        for item in node.body:
            value = getattr(item, 'value', None)
            if isinstance(value, ast.Dict):
                manifest_node = value
                break
        if manifest_node is None:
            return None
        try:
            obj = ast.literal_eval(manifest_node)
            if isinstance(obj, dict):
                return obj
            return None
        except Exception:
            return None

    def _check_models_init(self, directory: Path) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        models_dir = directory / 'models'
        init_file = models_dir / '__init__.py'
        if not models_dir.exists() or not init_file.exists():
            return results
        try:
            init_text = init_file.read_text(encoding='utf-8')
            modules = {py.stem for py in models_dir.glob('*.py') if py.name != '__init__.py'}
            missing: List[str] = []
            for module in sorted(modules):
                pattern = rf'(from\s+\.[ ]*{re.escape(module)}\s+import)|(from\s+\.[ ]*import\s+{re.escape(module)})|(import\s+{re.escape(module)})'
                if not re.search(pattern, init_text):
                    missing.append(module)
            if missing:
                res = ValidationResult()
                res.add_warning(f"models/__init__.py is not importing: {', '.join(missing)}")
                results.append(res)
        except Exception as exc:
            res = ValidationResult()
            res.add_warning(f"Error checking models/__init__.py imports: {exc}")
            results.append(res)
        return results
