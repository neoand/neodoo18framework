"""
Plugin de Regras Corporativas - AcmeCorp
========================================

Implementa regras específicas da empresa para validação de código Odoo.

Regras implementadas:
1. Modelos devem ter prefixo 'acme_' no _name
2. Campos monetários devem ter currency_field definido
3. Métodos de ação devem ter docstrings descritivos
4. Views devem seguir padrão de nomenclatura específico
5. Segurança deve incluir grupos corporativos específicos
"""

import re
import ast
from pathlib import Path
import sys

# Adicionar o path do framework
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from framework.validator.plugin import BaseValidatorPlugin, ValidationContext, ValidationResult


class AcmeCorporateRulesPlugin(BaseValidatorPlugin):
    name = "acme_corporate_rules"
    description = "Regras corporativas AcmeCorp para desenvolvimento Odoo"

    def __init__(self):
        # Configurações da empresa
        self.company_prefix = "acme_"
        self.required_groups = ["acme_base.group_user", "acme_base.group_manager"]
        self.forbidden_patterns = ["print(", "breakpoint(", "pdb.set_trace"]
        self.required_docstring_methods = ["action_", "button_", "compute_"]

    def supports(self, file_path: Path, context: ValidationContext) -> bool:
        """Define quais arquivos este plugin deve processar"""
        return file_path.suffix in {'.py', '.xml', '.csv'} or file_path.name == '__manifest__.py'

    def validate_file(self, file_path: Path, context: ValidationContext):
        """Validação principal do arquivo"""
        if file_path.name == '__manifest__.py':
            return self._validate_manifest(file_path, context)
        elif file_path.suffix == '.py':
            return self._validate_python(file_path, context)
        elif file_path.suffix == '.xml':
            return self._validate_xml(file_path, context)
        elif file_path.name == 'ir.model.access.csv':
            return self._validate_security(file_path, context)
        
        return None

    def _validate_manifest(self, file_path: Path, context: ValidationContext):
        """Validações específicas do manifest"""
        result = ValidationResult()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Verificar se o nome do módulo segue padrão corporativo
            if context.module_name and not context.module_name.startswith(self.company_prefix):
                result.add_error(
                    f"Módulo '{context.module_name}' deve ter prefixo corporativo '{self.company_prefix}'"
                )
            
            # Verificar autor corporativo
            if '"author"' in content:
                if 'AcmeCorp' not in content:
                    result.add_warning(
                        f"Manifest deve incluir 'AcmeCorp' como autor em {file_path}"
                    )
            
            # Verificar categoria corporativa
            if '"category"' in content:
                if 'AcmeCorp' not in content:
                    result.add_warning(
                        f"Considere usar categoria corporativa 'AcmeCorp/...' em {file_path}"
                    )
                    
        except Exception as exc:
            result.add_error(f"Erro ao validar manifest {file_path}: {exc}")
            
        return result if result.has_messages() else None

    def _validate_python(self, file_path: Path, context: ValidationContext):
        """Validações específicas de arquivos Python"""
        result = ValidationResult()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 1. Verificar padrões proibidos
            for pattern in self.forbidden_patterns:
                if pattern in content:
                    result.add_error(
                        f"Padrão proibido '{pattern}' encontrado em {file_path}"
                    )
            
            # 2. Verificar modelos com prefixo corporativo
            models = re.findall(r"_name\s*=\s*['\"]([^'\"]+)['\"]", content)
            for model in models:
                if not model.startswith(self.company_prefix):
                    result.add_error(
                        f"Model '{model}' deve ter prefixo corporativo '{self.company_prefix}' em {file_path}"
                    )
            
            # 3. Verificar campos monetários
            monetary_fields = re.findall(r"(\w+)\s*=\s*fields\.Monetary\([^)]*\)", content)
            for field_name in monetary_fields:
                if 'currency_field' not in content:
                    result.add_warning(
                        f"Campo monetário '{field_name}' deve especificar currency_field em {file_path}"
                    )
            
            # 4. Verificar docstrings em métodos de ação
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        for prefix in self.required_docstring_methods:
                            if node.name.startswith(prefix):
                                if not ast.get_docstring(node):
                                    result.add_warning(
                                        f"Método '{node.name}' deve ter docstring descritivo em {file_path}"
                                    )
            except SyntaxError:
                pass  # Ignora erros de sintaxe, outros validadores cuidam disso
                
        except Exception as exc:
            result.add_error(f"Erro ao validar Python {file_path}: {exc}")
            
        return result if result.has_messages() else None

    def _validate_xml(self, file_path: Path, context: ValidationContext):
        """Validações específicas de arquivos XML"""
        result = ValidationResult()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 1. Verificar padrão de nomenclatura de views
            view_ids = re.findall(r'<record[^>]+id="([^"]+)"[^>]*model="ir\.ui\.view"', content)
            for view_id in view_ids:
                if not view_id.startswith(self.company_prefix):
                    result.add_warning(
                        f"View ID '{view_id}' deve ter prefixo corporativo '{self.company_prefix}' em {file_path}"
                    )
            
            # 2. Verificar actions com padrão corporativo
            action_ids = re.findall(r'<record[^>]+id="([^"]+)"[^>]*model="ir\.actions\.act_window"', content)
            for action_id in action_ids:
                if not action_id.startswith(self.company_prefix):
                    result.add_warning(
                        f"Action ID '{action_id}' deve ter prefixo corporativo '{self.company_prefix}' em {file_path}"
                    )
            
            # 3. Verificar se menuitem tem grupos apropriados
            menuitems = re.findall(r'<menuitem[^>]*groups="([^"]+)"', content)
            for groups in menuitems:
                has_corporate_group = any(group.strip().startswith('acme_') for group in groups.split(','))
                if not has_corporate_group:
                    result.add_warning(
                        f"Menuitem deve incluir grupo corporativo AcmeCorp em {file_path}"
                    )
                    
        except Exception as exc:
            result.add_error(f"Erro ao validar XML {file_path}: {exc}")
            
        return result if result.has_messages() else None

    def _validate_security(self, file_path: Path, context: ValidationContext):
        """Validações específicas de segurança"""
        result = ValidationResult()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.strip().split('\n')
            
            if len(lines) < 2:  # Header + pelo menos uma linha
                return None
                
            # Verificar se usa grupos corporativos
            has_corporate_groups = False
            for line in lines[1:]:  # Pula header
                if 'acme_' in line:
                    has_corporate_groups = True
                    break
                    
            if not has_corporate_groups:
                result.add_warning(
                    f"Arquivo de segurança deve usar grupos corporativos 'acme_*' em {file_path}"
                )
                
        except Exception as exc:
            result.add_error(f"Erro ao validar segurança {file_path}: {exc}")
            
        return result if result.has_messages() else None

    def setup(self, context: ValidationContext) -> None:
        """Configuração inicial do plugin"""
        if context.verbose:
            print(f"🏢 Plugin AcmeCorp ativo - Validando com prefixo '{self.company_prefix}'")

    def finalize(self, context: ValidationContext):
        """Validações finais após processar todos os arquivos"""
        results = []
        
        # Exemplo: verificação global que só pode ser feita após ver todos os arquivos
        if context.verbose:
            result = ValidationResult()
            result.add_warning("AcmeCorp: Validação corporativa concluída")
            results.append(result)
            
        return results


def register():
    """Função para registrar o plugin"""
    return [AcmeCorporateRulesPlugin()]