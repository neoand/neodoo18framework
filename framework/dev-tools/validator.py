#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neodoo18Framework - Universal Odoo 18+ Validator
Extraído e generalizado do BJJ Academy para uso universal
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('neodoo18-validator')

@dataclass
class ValidationResult:
    """Resultado de validação"""
    file_path: str
    passed: bool
    errors: List[str]
    warnings: List[str]
    fixes_applied: List[str]
    odoo18_compliant: bool

class Odoo18Validator:
    """Validador Universal para Odoo 18+ - Zero Tolerância para Padrões Antigos"""
    
    def __init__(self):
        self.critical_patterns = {
            # Padrões XML PROIBIDOS no Odoo 18+
            'xml_tree_tag': r'<tree\s',
            'xml_tree_viewmode': r'view_mode=["\'].*tree',
            'xml_attrs_deprecated': r'attrs\s*=\s*["\']',
            'xml_states_deprecated': r'states\s*=\s*["\']',
            
            # Padrões Python OBRIGATÓRIOS
            'python_encoding_missing': r'^(?!.*coding[:=]\s*(utf-8|utf8))',
            'api_depends_missing': r'def\s+_compute_\w+.*\n(?!.*@api\.depends)',
        }
        
        self.required_patterns = {
            # XML - Padrões CORRETOS Odoo 18+
            'xml_list_tag': r'<list\s',
            'xml_list_viewmode': r'view_mode=["\'].*list',
            
            # Python - Padrões CORRETOS
            'python_proper_encoding': r'#\s*-\*-\s*coding[:=]\s*(utf-8|utf8)\s*-\*-',
            'api_depends_present': r'@api\.depends\([^)]+\)',
        }
        
    def validate_file(self, file_path: Path) -> ValidationResult:
        """Valida um arquivo específico"""
        errors = []
        warnings = []
        fixes_applied = []
        
        if not file_path.exists():
            errors.append(f"Arquivo não encontrado: {file_path}")
            return ValidationResult(
                str(file_path), False, errors, warnings, fixes_applied, False
            )
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            errors.append("Arquivo não está em UTF-8")
            return ValidationResult(
                str(file_path), False, errors, warnings, fixes_applied, False
            )
        
        # Validação por tipo de arquivo
        if file_path.suffix == '.xml':
            errors.extend(self._validate_xml(content, file_path))
        elif file_path.suffix == '.py':
            errors.extend(self._validate_python(content, file_path))
        
        # Determinar conformidade
        odoo18_compliant = len(errors) == 0
        passed = odoo18_compliant
        
        return ValidationResult(
            str(file_path), passed, errors, warnings, fixes_applied, odoo18_compliant
        )
    
    def _validate_xml(self, content: str, file_path: Path) -> List[str]:
        """Validação específica para arquivos XML"""
        errors = []
        
        # CRÍTICO: Detectar uso de <tree> (PROIBIDO no Odoo 18+)
        if re.search(self.critical_patterns['xml_tree_tag'], content, re.IGNORECASE):
            errors.append("CRÍTICO: Usa <tree> - DEVE ser <list> no Odoo 18+")
        
        # CRÍTICO: Detectar view_mode="tree" (PROIBIDO no Odoo 18+)
        if re.search(self.critical_patterns['xml_tree_viewmode'], content, re.IGNORECASE):
            errors.append("CRÍTICO: Usa view_mode com 'tree' - DEVE ser 'list' no Odoo 18+")
        
        # Detectar attrs deprecated
        if re.search(self.critical_patterns['xml_attrs_deprecated'], content):
            errors.append("DEPRECATED: Atributo 'attrs' descontinuado no Odoo 18+")
        
        # Detectar states deprecated  
        if re.search(self.critical_patterns['xml_states_deprecated'], content):
            errors.append("DEPRECATED: Atributo 'states' descontinuado no Odoo 18+")
        
        return errors
    
    def _validate_python(self, content: str, file_path: Path) -> List[str]:
        """Validação específica para arquivos Python"""
        errors = []
        lines = content.split('\n')
        
        # Verificar encoding UTF-8 nas primeiras 3 linhas
        encoding_found = False
        for i, line in enumerate(lines[:3]):
            if re.search(self.required_patterns['python_proper_encoding'], line):
                encoding_found = True
                break
        
        if not encoding_found:
            errors.append("OBRIGATÓRIO: Faltando declaração de encoding UTF-8")
        
        # Verificar @api.depends em métodos _compute_
        compute_methods = re.findall(r'def\s+(_compute_\w+)', content)
        for method in compute_methods:
            method_pattern = rf'def\s+{method}.*?(?=def|\Z)'
            method_content = re.search(method_pattern, content, re.DOTALL)
            
            if method_content:
                method_text = method_content.group(0)
                # Verificar se tem @api.depends antes do método
                lines_before = content[:method_content.start()].split('\n')
                depends_found = False
                
                # Procurar @api.depends nas 5 linhas anteriores
                for line in lines_before[-5:]:
                    if '@api.depends' in line:
                        depends_found = True
                        break
                
                if not depends_found:
                    errors.append(f"OBRIGATÓRIO: Método {method} precisa de @api.depends()")
        
        return errors
    
    def auto_fix_file(self, file_path: Path) -> Tuple[str, List[str]]:
        """Aplica correções automáticas quando possível"""
        if not file_path.exists():
            return "", []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixes_applied = []
        original_content = content
        
        # Auto-fix para XML
        if file_path.suffix == '.xml':
            # Corrigir <tree> para <list>
            if re.search(self.critical_patterns['xml_tree_tag'], content, re.IGNORECASE):
                content = re.sub(r'<tree\s', '<list ', content, flags=re.IGNORECASE)
                content = re.sub(r'</tree>', '</list>', content, flags=re.IGNORECASE)
                fixes_applied.append("Convertido <tree> para <list>")
            
            # Corrigir view_mode="tree" para "list"
            if re.search(self.critical_patterns['xml_tree_viewmode'], content):
                content = re.sub(r'view_mode="([^"]*?)tree([^"]*?)"', 
                               r'view_mode="\1list\2"', content)
                fixes_applied.append("Convertido view_mode 'tree' para 'list'")
        
        # Auto-fix para Python
        elif file_path.suffix == '.py':
            # Adicionar encoding UTF-8 se não existir
            lines = content.split('\n')
            encoding_found = any(re.search(self.required_patterns['python_proper_encoding'], line) 
                               for line in lines[:3])
            
            if not encoding_found:
                if lines[0].startswith('#!'):
                    # Inserir após shebang
                    lines.insert(1, '# -*- coding: utf-8 -*-')
                else:
                    # Inserir no início
                    lines.insert(0, '# -*- coding: utf-8 -*-')
                
                content = '\n'.join(lines)
                fixes_applied.append("Adicionado encoding UTF-8")
        
        return content, fixes_applied

def main():
    """Função principal para uso via CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Neodoo18Framework Universal Validator')
    parser.add_argument('--file', type=str, help='Arquivo para validar')
    parser.add_argument('--directory', type=str, help='Diretório para validar')
    parser.add_argument('--auto-fix', action='store_true', help='Aplicar correções automáticas')
    parser.add_argument('--report', type=str, help='Salvar relatório JSON')
    
    args = parser.parse_args()
    
    validator = Odoo18Validator()
    results = []
    
    if args.file:
        file_path = Path(args.file)
        result = validator.validate_file(file_path)
        results.append(result)
        
        if args.auto_fix and not result.passed:
            fixed_content, fixes = validator.auto_fix_file(file_path)
            if fixes:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✅ {len(fixes)} correções aplicadas em {file_path}")
                for fix in fixes:
                    print(f"   • {fix}")
    
    elif args.directory:
        directory = Path(args.directory)
        for file_path in directory.rglob('*.py'):
            if '/migrations/' not in str(file_path) and '__pycache__' not in str(file_path):
                result = validator.validate_file(file_path)
                results.append(result)
        
        for file_path in directory.rglob('*.xml'):
            result = validator.validate_file(file_path)
            results.append(result)
    
    # Mostrar relatório
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    
    print(f"\n📊 Relatório de Validação Odoo 18+")
    print(f"✅ Aprovados: {passed}/{total}")
    print(f"❌ Com problemas: {total - passed}/{total}")
    
    for result in results:
        if not result.passed:
            print(f"\n❌ {result.file_path}")
            for error in result.errors:
                print(f"   • {error}")
    
    # Salvar relatório se solicitado
    if args.report:
        with open(args.report, 'w') as f:
            json.dump([{
                'file_path': r.file_path,
                'passed': r.passed,
                'errors': r.errors,
                'warnings': r.warnings,
                'odoo18_compliant': r.odoo18_compliant
            } for r in results], f, indent=2)
        print(f"📄 Relatório salvo: {args.report}")

if __name__ == '__main__':
    main()