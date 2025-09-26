#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neodoo18Framework Smart Validator
Universal Odoo 18+ compliance validator extracted from BJJ Academy project
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
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

class SmartValidator:
    """Universal Odoo 18+ validator"""
    
    def __init__(self, auto_fix: bool = False):
        self.auto_fix = auto_fix
        
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
            }
        }
    
    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate a single file"""
        result = ValidationResult()
        
        if not file_path.exists():
            result.add_error(f"File not found: {file_path}")
            return result
        
        # Route to appropriate validator
        if file_path.suffix == '.xml':
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
            if '<tree' in content:
                result.add_error(f"DEPRECATED: Found <tree> tag. Use <list> in Odoo 18+")
                if self.auto_fix:
                    content = re.sub(r'<tree\b', '<list', content)
                    content = re.sub(r'</tree>', '</list>', content)
                    result.add_auto_fix("Replaced <tree> with <list>")
            
            if 'view_mode="tree' in content or "view_mode='tree" in content:
                result.add_error(f"DEPRECATED: Found view_mode='tree'. Use 'list' in Odoo 18+")
                if self.auto_fix:
                    content = re.sub(r'view_mode=["\']tree', 'view_mode="list', content)
                    result.add_auto_fix("Replaced view_mode='tree' with 'list'")
            
            # Try to parse XML structure
            try:
                ET.fromstring(content)
            except ET.ParseError as e:
                result.add_error(f"XML Parse Error: {e}")
            
            # Write back if auto-fixed
            if self.auto_fix and result.auto_fixes:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Auto-fixed {file_path}")
        
        except Exception as e:
            result.add_error(f"Error reading file: {e}")
        
        return result
    
    def _validate_python(self, file_path: Path) -> ValidationResult:
        """Validate Python files for Odoo 18+ compliance"""
        result = ValidationResult()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check encoding in first 2 lines
            has_encoding = any('coding: utf-8' in line for line in lines[:2])
            if not has_encoding and len(lines) > 10:  # Skip small files
                result.add_error("Missing UTF-8 encoding declaration")
            
            # Check for computed methods without @api.depends
            compute_methods = re.findall(r'def (_compute_\w+)\(self\):', content)
            for method in compute_methods:
                # Look for @api.depends before the method
                method_pattern = rf'def {method}\(self\):'
                method_match = re.search(method_pattern, content)
                if method_match:
                    # Check preceding lines for @api.depends
                    before_method = content[:method_match.start()]
                    last_lines = before_method.split('\n')[-10:]  # Check last 10 lines
                    
                    has_depends = any('@api.depends' in line for line in last_lines)
                    if not has_depends:
                        result.add_warning(f"Method {method} should have @api.depends decorator")
            
            # Check for ensure_one in action methods
            action_methods = re.findall(r'def (action_\w+)\(self\):', content)
            for method in action_methods:
                method_content = self._extract_method_content(content, method)
                if 'self.ensure_one()' not in method_content:
                    result.add_warning(f"Action method {method} should call self.ensure_one()")
        
        except Exception as e:
            result.add_error(f"Error reading Python file: {e}")
        
        return result
    
    def _extract_method_content(self, content: str, method_name: str) -> str:
        """Extract method content for analysis"""
        pattern = rf'def {method_name}\(self.*?\):(.*?)(?=\n    def |\n\n|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1) if match else ""
    
    def validate_project(self, project_path: Path) -> Dict[str, ValidationResult]:
        """Validate entire project"""
        results = {}
        
        # Find Python and XML files
        file_patterns = ['**/*.py', '**/*.xml']
        
        for pattern in file_patterns:
            for file_path in project_path.glob(pattern):
                # Skip certain directories
                if any(skip in str(file_path) for skip in ['__pycache__', '.git', 'odoo_source']):
                    continue
                
                relative_path = file_path.relative_to(project_path)
                results[str(relative_path)] = self.validate_file(file_path)
        
        return results
    
    def print_results(self, results: Dict[str, ValidationResult]):
        """Print validation results in a nice format"""
        total_errors = 0
        total_warnings = 0
        total_auto_fixes = 0
        
        print("\n🔍 NEODOO18FRAMEWORK VALIDATION RESULTS")
        print("=" * 50)
        
        for file_path, result in results.items():
            if result.errors or result.warnings or result.auto_fixes:
                print(f"\n📁 {file_path}")
                
                for error in result.errors:
                    print(f"   ❌ {error}")
                    total_errors += 1
                
                for warning in result.warnings:
                    print(f"   ⚠️  {warning}")
                    total_warnings += 1
                
                for fix in result.auto_fixes:
                    print(f"   🛠️  {fix}")
                    total_auto_fixes += 1
        
        print(f"\n📊 SUMMARY")
        print(f"   Errors: {total_errors}")
        print(f"   Warnings: {total_warnings}")
        print(f"   Auto-fixes: {total_auto_fixes}")
        
        if total_errors == 0:
            print("   ✅ All files comply with Odoo 18+ standards!")
        else:
            print("   ❌ Please fix errors before proceeding")

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Neodoo18Framework Smart Validator')
    parser.add_argument('path', help='File or directory to validate')
    parser.add_argument('--auto-fix', action='store_true', help='Apply automatic fixes')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    validator = SmartValidator(auto_fix=args.auto_fix)
    path = Path(args.path)
    
    if path.is_file():
        result = validator.validate_file(path)
        results = {str(path): result}
    else:
        results = validator.validate_project(path)
    
    validator.print_results(results)
    
    # Exit with error code if there are errors
    total_errors = sum(len(r.errors) for r in results.values())
    return 1 if total_errors > 0 else 0

if __name__ == '__main__':
    exit(main())