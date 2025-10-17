"""
Plugin de Regras Corporativas - Neo Sempre
==========================================

Implementa regras específicas da Neo Sempre para validação de código Odoo
focado no domínio de beneficiários INSS e margem consignável.

Regras implementadas:
1. Módulos podem usar prefixos: 'semprereal', 'neo_sempre', 'neodoo_ai', 'ns_'
2. Campos de CPF devem usar o campo 'vat' padrão do Odoo
3. Validações específicas para campos INSS (numero_beneficio, margem_consignavel)
4. Métodos de ação devem ter docstrings descritivos
5. Views devem seguir padrões Odoo 18+ (list vs tree)
6. Campos monetários devem usar currency_field correto
"""

import re
import ast
from pathlib import Path
import sys

# Adicionar o path do framework
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from framework.validator.plugin import BaseValidatorPlugin, ValidationContext, ValidationResult


class NeoSempreValidationPlugin(BaseValidatorPlugin):
    name = "neo_sempre_rules"
    description = "Regras corporativas Neo Sempre para sistema INSS de beneficiários"

    def __init__(self):
        # Configurações da empresa Neo Sempre
        self.allowed_module_prefixes = ["semprereal", "neo_sempre", "neodoo_ai", "ns_"]
        self.company_name = "Neo Sempre"
        
        # Campos obrigatórios para beneficiários INSS
        self.required_inss_fields = {
            'numero_beneficio': 'Número do Benefício INSS',
            'margem_consignavel': 'Margem Consignável disponível',
            'valor_beneficio': 'Valor do Benefício',
        }
        
        # Campos que devem usar 'vat' para CPF
        self.cpf_field_name = 'vat'
        
        # Padrões obrigatórios de nomenclatura
        self.beneficio_model_pattern = r'(semprereal\.beneficio|ns\.beneficiarios)'
        
        # Validações monetárias
        self.monetary_fields = ['margem_consignavel', 'valor_beneficio', 'comprometimento_emprestimo']

    def supports(self, file_path: Path, context: ValidationContext) -> bool:
        """Define quais arquivos este plugin deve processar"""
        # Processa apenas arquivos de módulos Neo Sempre
        module_path = str(file_path)
        
        # Verifica se está em um dos módulos da empresa
        for prefix in self.allowed_module_prefixes:
            if f"/{prefix}/" in module_path or f"\\{prefix}\\" in module_path:
                return file_path.suffix in {'.py', '.xml', '.csv'} or file_path.name == '__manifest__.py'
        
        return False

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
        """Valida o arquivo __manifest__.py"""
        result = ValidationResult()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Verificar se tem autor definido
            if self.company_name not in content and 'author' in content:
                result.add_warning(
                    f"Considere incluir '{self.company_name}' como autor em {file_path}"
                )
            
            # Verificar versão Odoo 18
            if "'version':" in content or '"version":' in content:
                if not re.search(r"['\"]version['\"]:\s*['\"]18\.0\.", content):
                    result.add_error(
                        f"Módulo deve ter versão '18.0.x.x.x' para Odoo 18+ em {file_path}"
                    )
            
            # Verificar dependências importantes para INSS
            manifest_dict = ast.literal_eval(content.strip('# -*- coding: utf-8 -*-\n'))
            depends = manifest_dict.get('depends', [])
            
            # Se é módulo de beneficiários, deve depender de 'base' e 'mail'
            if 'beneficio' in str(file_path).lower() or 'semprereal' in str(file_path):
                if 'base' not in depends:
                    result.add_warning(
                        f"Módulo de beneficiários deve depender de 'base' em {file_path}"
                    )
                if 'mail' not in depends and 'tracking' in content:
                    result.add_warning(
                        f"Módulo com tracking deve depender de 'mail' em {file_path}"
                    )
        
        except Exception as e:
            result.add_error(
                f"Erro ao validar manifest {file_path}: {str(e)}"
            )
        
        return result

    def _validate_python(self, file_path: Path, context: ValidationContext):
        """Valida arquivos Python"""
        result = ValidationResult()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Verificar se usa campo correto para CPF
            if 'cpf' in content.lower() and 'field' in content.lower():
                if re.search(r"cpf\s*=\s*fields\.", content, re.IGNORECASE):
                    result.add_error(
                        f"Use o campo 'vat' padrão do Odoo para CPF, não crie campo 'cpf' customizado em {file_path}"
                    )
            
            # Verificar campos monetários com currency_field
            for monetary_field in self.monetary_fields:
                pattern = rf"{monetary_field}\s*=\s*fields\.(?:Float|Monetary)\([^)]*\)"
                matches = re.finditer(pattern, content)
                for match in matches:
                    field_def = match.group(0)
                    if 'Monetary' in field_def and 'currency_field' not in field_def:
                        result.add_warning(
                            f"Campo monetário '{monetary_field}' deve especificar 'currency_field' em {file_path}"
                        )
            
            # Verificar se modelos de benefício têm campos obrigatórios INSS
            if re.search(self.beneficio_model_pattern, content):
                for field_name, field_description in self.required_inss_fields.items():
                    if field_name not in content:
                        result.add_warning(
                            f"Modelo de benefício deve ter campo '{field_name}' ({field_description}) em {file_path}"
                        )
            
            # Verificar docstrings em métodos de ação
            action_methods = re.finditer(r'def\s+(action_|button_|compute_)\w+\(self[^)]*\):', content)
            for match in action_methods:
                method_name = match.group(0)
                method_start = match.end()
                
                # Verificar se tem docstring nos próximos 100 caracteres
                next_content = content[method_start:method_start + 100]
                if '"""' not in next_content and "'''" not in next_content:
                    result.add_warning(
                        f"Método '{match.group(1) + 'xxx'}' deve ter docstring descritivo em {file_path}"
                    )
            
            # Verificar uso de self.ensure_one() em métodos de ação
            if re.search(r'def\s+action_\w+\(self[^)]*\):', content):
                if 'ensure_one()' not in content:
                    result.add_warning(
                        f"Métodos action_ devem chamar self.ensure_one() para garantir operação em registro único em {file_path}"
                    )
        
        except Exception as e:
            result.add_error(
                f"Erro ao validar Python {file_path}: {str(e)}"
            )
        
        return result

    def _validate_xml(self, file_path: Path, context: ValidationContext):
        """Valida arquivos XML"""
        result = ValidationResult()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Verificar uso correto de <list> em vez de <tree> (Odoo 18+)
            if '<tree' in content and 'string=' in content:
                result.add_error(
                    f"Odoo 18+ requer tag <list> em vez de <tree> para list views em {file_path}"
                )
            
            # Verificar views de beneficiários
            if re.search(self.beneficio_model_pattern, content):
                # Verificar se tem campos importantes visíveis
                required_fields = ['numero_beneficio', 'valor_beneficio', 'margem_consignavel']
                for field in required_fields:
                    if field not in content and 'list' in content.lower():
                        result.add_warning(
                            f"View de benefício deve exibir campo '{field}' em {file_path}"
                        )
            
            # Verificar actions com view_mode correto
            if 'ir.actions.act_window' in content:
                if 'view_mode' in content and 'tree,form' in content:
                    result.add_error(
                        f"Odoo 18+ requer view_mode='list,form' em vez de 'tree,form' em {file_path}"
                    )
            
            # Verificar grupos de segurança para beneficiários
            if 'res.groups' in content and 'beneficio' in content.lower():
                if 'group_user' not in content and 'group_manager' not in content:
                    result.add_warning(
                        f"Considere criar grupos de acesso separados: user, manager e admin em {file_path}"
                    )
        
        except Exception as e:
            result.add_error(
                f"Erro ao validar XML {file_path}: {str(e)}"
            )
        
        return result if result.has_messages() else None

    def _validate_security(self, file_path: Path, context: ValidationContext):
        """Valida arquivo de segurança ir.model.access.csv"""
        result = ValidationResult()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.strip().split('\n')
            
            if not lines or len(lines) < 2:
                result.add_error(
                    f"Arquivo de segurança deve ter cabeçalho e pelo menos uma regra de acesso em {file_path}"
                )
                return result
            
            # Verificar cabeçalho correto
            header = lines[0]
            expected_header = "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink"
            if header != expected_header:
                result.add_warning(
                    f"Cabeçalho do CSV deve ser: {expected_header} em {file_path}"
                )
            
            # Verificar se modelos de benefício têm permissões
            if 'beneficio' in str(file_path).lower():
                has_user_access = any('user' in line.lower() for line in lines[1:])
                has_manager_access = any('manager' in line.lower() for line in lines[1:])
                
                if not has_user_access:
                    result.add_warning(
                        f"Modelo de benefício deve ter acesso para grupo 'user' em {file_path}"
                    )
                
                if not has_manager_access:
                    result.add_warning(
                        f"Modelo de benefício deve ter acesso para grupo 'manager' em {file_path}"
                    )
        
        except Exception as e:
            result.add_error(
                f"Erro ao validar security CSV {file_path}: {str(e)}"
            )
        
        return result if result.has_messages() else None


def register():
    """Função obrigatória para registrar o plugin"""
    return [NeoSempreValidationPlugin()]
