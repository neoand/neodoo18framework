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
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

@dataclass
class ValidationResult:
    """Result of validation check"""
    file_path: str
    errors: List[str]
    warnings: List[str] 
    fixes_applied: List[str]
    compliance_score: float

class Odoo18Validator:
    """Universal validator for Odoo 18+ compliance"""
    
    def __init__(self, auto_fix=True):
        self.auto_fix = auto_fix
        self.fixes_applied = []
        
    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate a single file"""
        errors = []
        warnings = []
        fixes = []
        
        if not file_path.exists():
            return ValidationResult(str(file_path), ["File not found"], [], [], 0.0)
        
        content = file_path.read_text(encoding='utf-8')
        
        if file_path.suffix == '.xml':
            xml_result = self._validate_xml(content, file_path)
            errors.extend(xml_result['errors'])
            warnings.extend(xml_result['warnings'])
            
            if self.auto_fix and xml_result['fixes']:
                fixed_content = self._apply_xml_fixes(content, xml_result['fixes'])
                file_path.write_text(fixed_content, encoding='utf-8')
                fixes.extend([f"Applied: {fix}" for fix in xml_result['fixes']])
                
        elif file_path.suffix == '.py':
            py_result = self._validate_python(content, file_path)
            errors.extend(py_result['errors'])
            warnings.extend(py_result['warnings'])
            
            if self.auto_fix and py_result['fixes']:
                fixed_content = self._apply_python_fixes(content, py_result['fixes'])
                file_path.write_text(fixed_content, encoding='utf-8')
                fixes.extend([f"Applied: {fix}" for fix in py_result['fixes']])
        
        # Calculate compliance score
        total_issues = len(errors) + len(warnings)
        compliance_score = max(0.0, 100.0 - (total_issues * 10))
        
        return ValidationResult(str(file_path), errors, warnings, fixes, compliance_score)
    
    def _validate_xml(self, content: str, file_path: Path) -> Dict:
        """Validate XML content for Odoo 18+ compliance"""
        errors = []
        warnings = []
        fixes = []
        
        # Check for <tree> instead of <list>
        if '<tree' in content:
            errors.append("Uses <tree> tag - should use <list> in Odoo 18+")
            fixes.append("tree_to_list")
        
        # Check for view_mode="tree"
        if 'view_mode="tree' in content:
            errors.append("Uses view_mode='tree' - should use 'list' in Odoo 18+")
            fixes.append("view_mode_tree_to_list")
            
        # Check for deprecated attrs
        if 'attrs=' in content:
            warnings.append("Uses deprecated 'attrs' attribute - consider direct attributes")
            
        return {
            'errors': errors,
            'warnings': warnings, 
            'fixes': fixes
        }
    
    def _validate_python(self, content: str, file_path: Path) -> Dict:
        """Validate Python content for Odoo 18+ compliance"""
        errors = []
        warnings = []
        fixes = []
        
        # Check for proper encoding
        if not content.startswith('#!/usr/bin/env python3') and not content.startswith('# -*- coding: utf-8 -*-'):
            if '# -*- coding: utf-8 -*-' not in content[:200]:
                warnings.append("Missing UTF-8 encoding declaration")
                fixes.append("add_encoding")
        
        # Check for @api.depends on computed fields
        if '_compute_' in content and '@api.depends' not in content:
            warnings.append("Computed field without @api.depends decorator")
            
        # Check for proper model inheritance
        if 'class ' in content and 'models.Model' in content:
            if 'mail.thread' not in content and '_inherit' in content:
                warnings.append("Consider inheriting from mail.thread for tracking")
        
        return {
            'errors': errors,
            'warnings': warnings,
            'fixes': fixes
        }
    
    def _apply_xml_fixes(self, content: str, fixes: List[str]) -> str:
        """Apply XML fixes automatically"""
        for fix in fixes:
            if fix == "tree_to_list":
                content = re.sub(r'<tree([^>]*)>', r'<list\1>', content)
                content = re.sub(r'</tree>', r'</list>', content)
                
            elif fix == "view_mode_tree_to_list":
                content = re.sub(r'view_mode="tree', r'view_mode="list', content)
                content = re.sub(r'view_mode=\'tree', r'view_mode=\'list', content)
                
        return content
    
    def _apply_python_fixes(self, content: str, fixes: List[str]) -> str:
        """Apply Python fixes automatically"""
        for fix in fixes:
            if fix == "add_encoding":
                if not content.startswith('#'):
                    content = '# -*- coding: utf-8 -*-\n\n' + content
                    
        return content
    
    def validate_directory(self, directory: Path, recursive=True) -> List[ValidationResult]:
        """Validate all files in a directory"""
        results = []
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in directory.glob(pattern):
            if file_path.is_file() and file_path.suffix in ['.py', '.xml']:
                # Skip certain directories
                if any(exclude in str(file_path) for exclude in ['__pycache__', '.git', 'odoo_source']):
                    continue
                    
                result = self.validate_file(file_path)
                results.append(result)
                
        return results

def main():
    """CLI interface for the validator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Neodoo18Framework - Odoo 18+ Validator")
    parser.add_argument("path", help="File or directory to validate")
    parser.add_argument("--no-fix", action="store_true", help="Don't apply automatic fixes")
    parser.add_argument("--recursive", action="store_true", default=True, help="Validate recursively")
    
    args = parser.parse_args()
    
    validator = Odoo18Validator(auto_fix=not args.no_fix)
    path = Path(args.path)
    
    print("🚀 Neodoo18Framework Validator")
    print("=" * 50)
    
    if path.is_file():
        result = validator.validate_file(path)
        results = [result]
    else:
        results = validator.validate_directory(path, args.recursive)
    
    # Print results
    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results) 
    total_fixes = sum(len(r.fixes_applied) for r in results)
    avg_compliance = sum(r.compliance_score for r in results) / len(results) if results else 0
    
    print(f"\n📊 Summary:")
    print(f"   Files checked: {len(results)}")
    print(f"   Errors: {total_errors}")
    print(f"   Warnings: {total_warnings}")
    print(f"   Auto-fixes applied: {total_fixes}")
    print(f"   Average compliance: {avg_compliance:.1f}%")
    
    # Show details for files with issues
    for result in results:
        if result.errors or result.warnings or result.fixes_applied:
            print(f"\n📁 {result.file_path}")
            
            for error in result.errors:
                print(f"   ❌ {error}")
                
            for warning in result.warnings:
                print(f"   ⚠️  {warning}")
                
            for fix in result.fixes_applied:
                print(f"   🛠️  {fix}")
                
            print(f"   📊 Compliance: {result.compliance_score:.1f}%")
    
    # Exit code based on errors
    sys.exit(1 if total_errors > 0 else 0)

if __name__ == "__main__":
    main()