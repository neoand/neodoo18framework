#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neodoo18Framework - Universal Odoo 18+ Validator
Validates and auto-fixes code to ensure Odoo 18+ compliance
"""

import os
import re
import sys
from pathlib import Path
import argparse
import logging
from typing import List, Dict, Tuple, Optional, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class ValidationResult:
    """Result of validation process"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.auto_fixes: List[str] = []
        self.is_valid: bool = True
    
    def add_error(self, message: str):
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        self.warnings.append(message)
    
    def add_auto_fix(self, message: str):
        self.auto_fixes.append(message)

class Odoo18Validator:
    """Universal validator for Odoo 18+ compliance"""
    
    def __init__(self, auto_fix: bool = True, strict: bool = False, template_mode: bool = False):
        self.auto_fix = auto_fix
        self.strict = strict
        self.template_mode = template_mode
        self.fixes_applied = []
        self.module_name: Optional[str] = None
        
        # Odoo 18+ specific rules
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
        
        self.python_rules = {
            'missing_encoding': {
                'pattern': r'^(?!.*# -\*- coding: utf-8 -\*-)',
                'message': 'Missing UTF-8 encoding declaration'
            },
            'missing_api_depends': {
                'pattern': r'def _compute_.*\(self\):(?!.*@api\.depends)',
                'message': 'Computed methods must have @api.depends decorator'
            },
            'missing_model_description': {
                'pattern': r'_name\s*=.*(?!.*_description)',
                'message': 'Models must have _description attribute'
            }
        }
        
        self.security_rules = {
            'missing_access_csv': {
                'pattern': 'ir.model.access.csv',
                'message': 'Missing ir.model.access.csv file'
            }
        }
        
    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate a single file"""
        result = ValidationResult()
        
        if not file_path.exists():
            result.add_error(f"File not found: {file_path}")
            return result
        
        # Derive module name if not provided (walk up to directory with __manifest__.py)
        if not self.module_name:
            self.module_name = self._infer_module_name(file_path)
        
        # Route to appropriate validator
        if file_path.name == '__manifest__.py':
            return self._validate_manifest(file_path)
        elif file_path.suffix == '.xml':
            return self._validate_xml(file_path)
        elif file_path.suffix == '.py':
            return self._validate_python(file_path)
        else:
            result.add_warning(f"No validator for file type: {file_path.suffix}")
        
        return result
    
    def _validate_xml(self, file_path: Path) -> ValidationResult:
        """Validate XML files for Odoo 18+ compliance"""
        result = ValidationResult()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for deprecated patterns
            for rule_name, rule in self.xml_rules.items():
                if re.search(rule['pattern'], content):
                    # Deprecated tags are always errors—even in template mode
                    result.add_error(f"{rule['message']} in {file_path}")
                    
                    # Auto-fix if enabled
                    if self.auto_fix and 'replacement' in rule:
                        if callable(rule['replacement']):
                            new_content = re.sub(rule['pattern'], rule['replacement'], content)
                        else:
                            new_content = re.sub(rule['pattern'], rule['replacement'], content)
                            
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        result.add_auto_fix(f"Fixed {rule_name} in {file_path}")

            # Additional checks: actions must prefer list view
            # Warn if an ir.actions.act_window has view_mode without 'list'
            try:
                if 'ir.actions.act_window' in content:
                    # Rough check for view_mode occurrences
                    for m in re.finditer(r'<field\s+name=["\']view_mode["\']>([^<]+)</field>', content):
                        modes = m.group(1).strip()
                        if 'list' not in modes:
                            # In template mode, keep as warning only
                            self._warn_or_error(result, f"Action view_mode without 'list' in {file_path}: '{modes}'", strict_as_error=False)
                        # Prefer including 'form' alongside 'list' in actions
                        if 'list' in modes and 'form' not in modes:
                            self._warn_or_error(result, f"Action view_mode should include 'form' with 'list' in {file_path}: '{modes}'", strict_as_error=False)
            except Exception:
                # Non-fatal; XML parsing here is heuristic
                pass

            # XML record id prefix: encourage ids to start with module_name_
            try:
                module_prefix = (self.module_name or '').strip()
                if module_prefix:
                    for m in re.finditer(r'<record\s+id=["\']([^"\']+)["\']', content):
                        rec_id = m.group(1)
                        if not rec_id.startswith(module_prefix + '_'):
                            # Naming convention stays a warning in template mode too
                            self._warn_or_error(result, f"XML record id '{rec_id}' should be prefixed with '{module_prefix}_' ({file_path})", strict_as_error=False)
            except Exception:
                pass
            
        except Exception as e:
            result.add_error(f"Error processing {file_path}: {str(e)}")
        
        return result
    
    def _validate_python(self, file_path: Path) -> ValidationResult:
        """Validate Python files for Odoo 18+ compliance"""
        result = ValidationResult()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check for UTF-8 encoding
            if not re.search(r'# -\*- coding: utf-8 -\*-', content):
                # Always an error; not cosmetic
                result.add_error(f"Missing UTF-8 encoding declaration in {file_path}")
                
                # Auto-fix if enabled
                if self.auto_fix:
                    if lines and lines[0].startswith('#!'):
                        lines.insert(1, '# -*- coding: utf-8 -*-')
                    else:
                        lines.insert(0, '# -*- coding: utf-8 -*-')
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))
                    
                    result.add_auto_fix(f"Added UTF-8 encoding to {file_path}")
            
            # Check for @api.depends in computed methods
            compute_methods = re.finditer(r'def (_compute_[^(]*)\(self', content)
            for match in compute_methods:
                method_name = match.group(1)
                method_pos = match.start()
                preceding_lines = content[max(0, method_pos-100):method_pos]
                
                if not re.search(r'@api\.depends', preceding_lines):
                    result.add_error(f"Missing @api.depends for {method_name} in {file_path}")
            
            # Check model classes for _description
            if '_name' in content and 'models.Model' in content:
                model_matches = re.finditer(r'class\s+(\w+)\(models\.Model\)', content)
                for match in model_matches:
                    class_name = match.group(1)
                    class_pos = match.start()
                    
                    # Look for _name and _description in the next 10 lines
                    next_lines = content[class_pos:class_pos + 500]
                    has_name = re.search(r'_name\s*=', next_lines)
                    has_description = re.search(r'_description\s*=', next_lines)
                    
                    if has_name and not has_description:
                        result.add_error(f"Model {class_name} has _name but missing _description in {file_path}")

            # Ban print/breakpoint/pdb in committed code
            for i, line in enumerate(lines, start=1):
                if re.search(r'^\s*print\(', line):
                    # In template mode, keep as warning. In strict mode, escalate to error.
                    self._warn_or_error(result, f"Avoid print() in code ({file_path}:{i}); use _logger instead", strict_as_error=True if not self.template_mode else False)
                if 'pdb.set_trace' in line or re.search(r'^\s*breakpoint\(', line):
                    self._warn_or_error(result, f"Debug statements (pdb/breakpoint) found in {file_path}:{i}", strict_as_error=True)

            # Heuristic: action_/button_ methods should ensure_one()
            for m in re.finditer(r'def\s+(action_\w+|button_\w+)\(self[^\)]*\):', content):
                start = m.end()
                # Take function body until next def/class or end
                tail = content[start:]
                stop_match = re.search(r'\n\s*def\s|\n\s*class\s', tail)
                body = tail[:stop_match.start()] if stop_match else tail
                if 'self.ensure_one()' not in body:
                    self._warn_or_error(result, f"Method {m.group(1)} should call self.ensure_one() in {file_path}", strict_as_error=False)
            
        except Exception as e:
            result.add_error(f"Error processing {file_path}: {str(e)}")
        
        return result

    def _validate_manifest(self, file_path: Path) -> ValidationResult:
        """Validate __manifest__.py for basic Odoo 18+ compliance"""
        import ast
        result = ValidationResult()
        try:
            manifest = self._parse_manifest(file_path)
            if manifest is None:
                result.add_error(f"{file_path}: Manifest must be a top-level dict")
                return result

            # Required keys
            required = ['name', 'version', 'depends', 'data']
            for k in required:
                if k not in manifest:
                    result.add_error(f"{file_path}: Missing required manifest key '{k}'")

            # Version format
            version = str(manifest.get('version', ''))
            if not version.startswith('18.0.'):
                result.add_warning(f"{file_path}: Version should start with '18.0.' (found '{version}')")

            # Depends type
            depends = manifest.get('depends')
            if not isinstance(depends, (list, tuple)):
                result.add_error(f"{file_path}: 'depends' must be a list")

            # Data files exist
            data_files = manifest.get('data') or []
            for rel in data_files:
                if not isinstance(rel, str):
                    # Skip non-string dynamic entries
                    continue
                p = file_path.parent / rel
                if not p.exists():
                    # In strict mode, escalate to error
                    if self.strict:
                        result.add_error(f"{file_path}: Listed data file not found: {rel}")
                    else:
                        result.add_warning(f"{file_path}: Listed data file not found: {rel}")

            # License and installable checks
            if 'license' not in manifest or not manifest.get('license'):
                result.add_error(f"{file_path}: Missing 'license' in manifest")
            installable = manifest.get('installable')
            if installable is False or installable is None:
                result.add_error(f"{file_path}: 'installable' must be True for Odoo 18+ modules")

            # Ensure ir.model.access.csv referenced in manifest if present in module
            try:
                access_rel = 'security/ir.model.access.csv'
                access_file = file_path.parent / access_rel
                if access_file.exists():
                    listed = access_rel in (manifest.get('data') or []) or access_rel in (manifest.get('security') or [])
                    if not listed:
                        # Prefer error in strict
                        if self.strict:
                            result.add_error(f"{file_path}: {access_rel} exists but is not listed in manifest 'data' or 'security'")
                        else:
                            result.add_warning(f"{file_path}: {access_rel} exists but is not listed in manifest 'data' or 'security'")
            except Exception:
                pass

        except Exception as e:
            result.add_error(f"Error validating manifest {file_path}: {e}")

        return result
    
    def validate_directory(self, directory_path: Path, verbose: bool = False) -> List[ValidationResult]:
        """Validate all relevant files in directory"""
        results = []
        
        if not directory_path.exists() or not directory_path.is_dir():
            logger.error(f"Directory not found: {directory_path}")
            return results

        # Set module name for downstream checks
        self.module_name = directory_path.name
        
        # Module directory naming convention: snake_case, lowercase
        mod_name = directory_path.name
        if not re.match(r'^[a-z][a-z0-9_]*$', mod_name):
            r = ValidationResult()
            r.add_error(f"Module directory '{mod_name}' must be snake_case (lowercase, digits, underscores)")
            results.append(r)
        
        # Check for security files
        has_access_csv = False
        access_csv_path: Optional[Path] = None
        for path in directory_path.glob('**/*'):
            if path.name == 'ir.model.access.csv':
                has_access_csv = True
                access_csv_path = path
                break
        
        if not has_access_csv:
            result = ValidationResult()
            # In template mode, allow missing access file (warning), else error
            if self.template_mode:
                result.add_warning(f"Missing ir.model.access.csv in {directory_path}")
            else:
                result.add_error(f"Missing ir.model.access.csv in {directory_path}")
            results.append(result)
        else:
            # Validate CSV header minimally
            try:
                header = access_csv_path.read_text(encoding='utf-8').splitlines()[0].strip()
                expected = 'id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink'
                if header.replace(' ', '') != expected:
                    r = ValidationResult()
                    if self.strict and not self.template_mode:
                        r.add_error(f"{access_csv_path}: Unexpected CSV header. Expected '{expected}'")
                    else:
                        r.add_warning(f"{access_csv_path}: Unexpected CSV header. Expected '{expected}'")
                    results.append(r)
            except Exception as e:
                r = ValidationResult()
                r.add_warning(f"{access_csv_path}: Could not read header ({e})")
                results.append(r)
        
        # Validate individual files
        for path in directory_path.glob('**/*'):
            if path.is_file() and path.suffix in ['.py', '.xml']:
                if verbose:
                    logger.info(f"Validating {path}")
                result = self.validate_file(path)
                if not result.is_valid or verbose:
                    results.append(result)

        # models/__init__.py should import module files
        models_dir = directory_path / 'models'
        init_file = models_dir / '__init__.py'
        if models_dir.exists() and init_file.exists():
            try:
                init_text = init_file.read_text(encoding='utf-8')
                modules = set()
                for py in models_dir.glob('*.py'):
                    if py.name == '__init__.py':
                        continue
                    modules.add(py.stem)
                missing = []
                for m in sorted(modules):
                    # Accept either 'from . import m' or 'from .m import ...'
                    pattern = rf'(from\s+\.[ ]*{re.escape(m)}\s+import)|(from\s+\.[ ]*import\s+{re.escape(m)})|(import\s+{re.escape(m)})'
                    if not re.search(pattern, init_text):
                        missing.append(m)
                if missing:
                    r = ValidationResult()
                    r.add_warning(f"models/__init__.py is not importing: {', '.join(missing)}")
                    results.append(r)
            except Exception as e:
                r = ValidationResult()
                r.add_warning(f"Error checking models/__init__.py imports: {e}")
                results.append(r)
        
        return results

    # ---------- Helpers ----------
    def _warn_or_error(self, result: ValidationResult, message: str, strict_as_error: bool = False):
        """Add warning or error based on strictness policy."""
        if strict_as_error and self.strict:
            result.add_error(message)
        else:
            result.add_warning(message)

    def _infer_module_name(self, file_path: Path) -> Optional[str]:
        """Walk up from file_path to find directory containing __manifest__.py and return its name."""
        cur = file_path if file_path.is_dir() else file_path.parent
        for _ in range(5):  # walk up a few levels
            manifest = cur / '__manifest__.py'
            if manifest.exists():
                return cur.name
            if cur.parent == cur:
                break
            cur = cur.parent
        # Fallback: if file is inside models/, take parent of models
        parts = list(file_path.parts)
        if 'models' in parts:
            try:
                idx = parts.index('models')
                return Path(*parts[:idx]).name
            except Exception:
                pass
        return file_path.parent.name if file_path.parent else None

    def _parse_manifest(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a __manifest__.py file and return a Python dict, or None if not a top-level dict.

        Supports both 'manifest = { ... }' and a bare dict literal at top-level.
        """
        import ast
        text = file_path.read_text(encoding='utf-8')
        node = ast.parse(text, filename=str(file_path))
        manifest_dict_node = None
        for n in node.body:
            if isinstance(n, ast.Expr) and isinstance(getattr(n, 'value', None), ast.Dict):
                manifest_dict_node = n.value
                break
            if isinstance(n, ast.Assign) and isinstance(getattr(n, 'value', None), ast.Dict):
                manifest_dict_node = n.value
                break
        if manifest_dict_node is None:
            return None
        # Safely evaluate the dict AST into a Python dict without executing arbitrary code.
        try:
            manifest_obj = ast.literal_eval(manifest_dict_node)
            if isinstance(manifest_obj, dict):
                return manifest_obj
            return None
        except Exception:
            return None

def validate_path(path_str: str, auto_fix: bool = False, verbose: bool = False, strict: bool = False, template_mode: bool = False) -> bool:
    """Validate a file or directory"""
    path = Path(path_str)
    validator = Odoo18Validator(auto_fix=auto_fix, strict=strict, template_mode=template_mode)
    
    if path.is_file():
        result = validator.validate_file(path)
        
        if not result.is_valid:
            logger.error(f"Validation failed for {path}")
            for error in result.errors:
                logger.error(f"  - {error}")
            for warning in result.warnings:
                logger.warning(f"  - {warning}")
            for fix in result.auto_fixes:
                logger.info(f"  ✓ {fix}")
            return False
        else:
            if verbose:
                logger.info(f"Validation passed for {path}")
            return True
    
    elif path.is_dir():
        results = validator.validate_directory(path, verbose)
        valid = all(result.is_valid for result in results)
        
        # Display results
        error_count = sum(len(result.errors) for result in results)
        warning_count = sum(len(result.warnings) for result in results)
        fix_count = sum(len(result.auto_fixes) for result in results)
        
        if not valid:
            logger.error(f"Validation failed for directory {path}")
            logger.error(f"  {error_count} errors, {warning_count} warnings")
            
            if verbose:
                for result in results:
                    if not result.is_valid:
                        for error in result.errors:
                            logger.error(f"  - {error}")
                        for warning in result.warnings:
                            logger.warning(f"  - {warning}")
                        for fix in result.auto_fixes:
                            logger.info(f"  ✓ {fix}")
            
            if auto_fix and fix_count > 0:
                logger.info(f"Applied {fix_count} auto-fixes")
                
            return False
        else:
            if warning_count > 0:
                logger.warning(f"Validation passed with {warning_count} warnings for {path}")
            else:
                logger.info(f"Validation passed for directory {path}")
                
            if auto_fix and fix_count > 0:
                logger.info(f"Applied {fix_count} auto-fixes")
                
            return True
    
    else:
        logger.error(f"Path not found: {path}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Neodoo18Framework Universal Validator")
    parser.add_argument('path', help="File or directory to validate")
    parser.add_argument('--auto-fix', action='store_true', help="Auto-fix issues when possible")
    parser.add_argument('--verbose', '-v', action='store_true', help="Show detailed validation information")
    parser.add_argument('--strict', action='store_true', help="Enable strict mode (promote selected warnings to errors)")
    parser.add_argument('--template-mode', action='store_true', help="Permit template placeholders and missing optional files as warnings")
    
    args = parser.parse_args()
    
    success = validate_path(args.path, args.auto_fix, args.verbose, args.strict, args.template_mode)
    
    if success:
        logger.info("✅ Validation successful!")
        sys.exit(0)
    else:
        logger.error("❌ Validation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()