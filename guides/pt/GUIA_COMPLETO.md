# 🚀 Guia Completo: Neodoo18Framework

> **Framework Universal para Desenvolvimento Odoo 18+ com Sistema SOIL**

## 📚 **ÍNDICE**

1. [Instalação Rápida](#instalação-rápida)
2. [Primeiro Projeto](#primeiro-projeto)  
3. [Desenvolvimento com IA](#desenvolvimento-com-ia)
4. [Padrões Obrigatórios](#padrões-obrigatórios)
5. [Validação Automática](#validação-automática)
6. [Exemplos Práticos](#exemplos-práticos)
7. [Integração com Odoo](#integração-com-odoo)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 **INSTALAÇÃO RÁPIDA**

### Método 1: Git Clone (Recomendado)
```bash
# 1. Clone o framework
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# 2. Torne executável
chmod +x quick-start.sh

# 3. Pronto para usar!
./quick-start.sh --help
```

### Método 2: Download Direto
```bash
wget https://github.com/neoand/neodoo18framework/archive/refs/heads/main.zip
unzip main.zip
cd neodoo18framework-main
chmod +x quick-start.sh
```

### Verificar Instalação:
```bash
python3 framework/validator.py --version
# Expected: Neodoo18Framework Validator v1.0.0
```

---

## 🏗️ **PRIMEIRO PROJETO**

### Criar Projeto em 10 Segundos:
```bash
./quick-start.sh meu_primeiro_modulo
```

### O que Foi Criado:
```
meu_primeiro_modulo/
├── __init__.py                 # Inicialização Python
├── __manifest__.py             # Configuração Odoo
├── models/                     # Modelos de dados
│   ├── __init__.py
│   └── template_model.py       # Modelo exemplo
├── views/                      # Interfaces (criadas sob demanda)
├── security/                   # Controle de acesso
├── tests/                      # Testes unitários
├── wizard/                     # Assistentes
├── demo/                       # Dados de demonstração
└── README.md                   # Documentação
```

### Verificar Qualidade:
```bash
python3 framework/validator.py meu_primeiro_modulo/
# Expected: 100% compliance
```

---

## 🤖 **DESENVOLVIMENTO COM IA**

### Para ChatGPT/Claude/Gemini:

#### 1. Preparar Contexto:
```bash
# Copie o contexto SOIL para a IA
cat framework/SOIL_CORE.md
```

#### 2. Prompt Exemplo:
```
Usando o Neodoo18Framework, desenvolva um módulo para gestão de biblioteca com:

📚 REQUISITOS:
- Modelo: bjj.livro (título, autor, isbn, categoria)
- Views: list, form, kanban seguindo Odoo 18+
- Menu: "Biblioteca" no menu principal
- Security: Regras básicas de acesso

⚠️ CRÍTICO:
- Use <list> NUNCA <tree> 
- Use "list,form" NUNCA "tree,form"
- Validar com: python3 framework/validator.py

📋 BASE:
Use os templates do framework como referência
```

#### 3. Desenvolver e Validar:
```bash
# Após IA gerar o código
python3 framework/validator.py biblioteca/
# Se 100% = pronto para produção!
```

---

## ⚠️ **PADRÕES OBRIGATÓRIOS**

### ✅ XML Views (Odoo 18+):
```xml
<!-- CORRETO -->
<record id="livro_view_tree" model="ir.ui.view">
    <field name="name">livro.view.list</field>
    <field name="model">bjj.livro</field>
    <field name="arch" type="xml">
        <list string="Livros">
            <field name="titulo"/>
            <field name="autor"/>
        </list>
    </field>
</record>

<!-- CORRETO - Action -->
<record id="livro_action" model="ir.actions.act_window">
    <field name="name">Livros</field>
    <field name="res_model">bjj.livro</field>
    <field name="view_mode">list,form</field>
</record>
```

### ❌ XML Obsoleto (Odoo ≤17):
```xml
<!-- ERRADO - Não use mais -->
<tree string="Livros">  <!-- Use <list> -->
    <field name="titulo"/>
</tree>

<!-- ERRADO - Action -->
<field name="view_mode">tree,form</field>  <!-- Use list,form -->
```

### ✅ Python Models:
```python
# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class Livro(models.Model):
    _name = 'bjj.livro'
    _description = 'Livro da Biblioteca'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'titulo asc'
    
    titulo = fields.Char(
        string='Título', 
        required=True, 
        tracking=True
    )
    autor = fields.Char(string='Autor', required=True)
    isbn = fields.Char(string='ISBN', size=13)
    
    @api.constrains('isbn')
    def _check_isbn(self):
        for record in self:
            if record.isbn and len(record.isbn) != 13:
                raise ValidationError(_('ISBN deve ter 13 dígitos'))
```

---

## ✅ **VALIDAÇÃO AUTOMÁTICA**

### Comando Básico:
```bash
python3 framework/validator.py meu_projeto/
```

### Saída Exemplo:
```
🚀 Neodoo18Framework Validator
==================================================

📊 Summary:
   Files checked: 8
   Errors: 0
   Warnings: 0
   Auto-fixes applied: 0
   Average compliance: 100.0%

✅ All checks passed! Ready for production.
```

### Validação com Auto-Correção:
```bash
python3 framework/validator.py meu_projeto/ --auto-fix
```

### Validação Detalhada:
```bash
python3 framework/validator.py meu_projeto/ --verbose
```

---

## 💡 **EXEMPLOS PRÁTICOS**

### Exemplo 1: E-commerce Simples
```bash
./quick-start.sh loja_online
cd loja_online

# Desenvolver com IA usando contexto SOIL
# Resultado: Módulo com produtos, categorias, pedidos
```

### Exemplo 2: CRM Personalizado  
```bash
./quick-start.sh meu_crm
cd meu_crm

# Desenvolver: clientes, oportunidades, atividades
# Validar: python3 ../framework/validator.py .
```

### Exemplo 3: Sistema Escolar
```bash
./quick-start.sh escola_sistema
cd escola_sistema

# Modelos: alunos, professores, turmas, notas
# Integration: res.partner inheritance
```

---

## 🔗 **INTEGRAÇÃO COM ODOO**

### Método 1: Cópia Direta
```bash
# Copiar módulo para addons do Odoo
cp -r meu_projeto /opt/odoo/addons/
sudo chown -R odoo:odoo /opt/odoo/addons/meu_projeto
sudo systemctl restart odoo
```

### Método 2: Symlink (Desenvolvimento)
```bash
# Criar link simbólico
ln -s $(pwd)/meu_projeto /opt/odoo/addons/
# Restart Odoo
```

### Método 3: Odoo.sh / SaaS
```bash
# Zipar módulo
zip -r meu_projeto.zip meu_projeto/
# Upload via interface Odoo.sh
```

### Ativação no Odoo:
1. **Apps** → **Update Apps List**
2. **Search**: Nome do seu módulo  
3. **Install**
4. **Verify**: Menu aparece na interface

---

## 🛠️ **TROUBLESHOOTING**

### ❌ Erro: "Invalid view mode 'tree'"
**Solução:**
```bash
python3 framework/validator.py meu_projeto/ --auto-fix
# Corrige automaticamente tree → list
```

### ❌ Erro: "Module not found"  
**Verificar:**
```bash
# 1. __init__.py existe?
ls meu_projeto/__init__.py

# 2. Imports corretos?
cat meu_projeto/models/__init__.py
# Deve conter: from . import nome_modelo
```

### ❌ Erro: "XML Syntax Error"
**Validar XML:**
```bash
python3 framework/xml_validator.py meu_projeto/views/
```

### ❌ Erro: "Access Rights"
**Verificar Security:**
```bash
# 1. ir.model.access.csv existe?
ls meu_projeto/security/

# 2. Grupos definidos?
grep "group_" meu_projeto/security/*.xml
```

---

## 📋 **CHECKLIST DE QUALIDADE**

### Antes de Deploy:
- [ ] `python3 framework/validator.py projeto/` = 100%
- [ ] XML usa `<list>` não `<tree>`  
- [ ] Actions usam `"list,form"` não `"tree,form"`
- [ ] Models herdam `mail.thread`
- [ ] Security rules definidas
- [ ] Tests básicos criados
- [ ] README atualizado

### Estrutura Mínima:
- [ ] `__manifest__.py` completo
- [ ] `models/__init__.py` com imports
- [ ] `security/ir.model.access.csv`
- [ ] `views/` com menus e actions
- [ ] Documentação básica

---

## 🚀 **COMANDOS AVANÇADOS**

### Análise de Projeto:
```bash
# Estatísticas detalhadas
python3 framework/analyzer.py meu_projeto/

# Dependências
python3 framework/dependency_checker.py meu_projeto/

# Documentação auto
python3 framework/doc_generator.py meu_projeto/
```

### Geração Específica:
```bash
# Criar modelo específico
python3 generator/create_model.py --name="Produto" --fields="name:char,price:float"

# Criar views para modelo
python3 generator/create_views.py --model="produto" --views="list,form,kanban"

# Criar wizard
python3 generator/create_wizard.py --name="ImportProdutos"
```

---

## 📚 **RECURSOS ADICIONAIS**

### Documentação Técnica:
- **SOIL_CORE.md**: Guia para LLMs
- **STANDARDS.md**: Padrões Odoo 18+  
- **templates/**: Exemplos prontos
- **framework/**: Ferramentas de desenvolvimento

### Comunidade:
- **GitHub**: https://github.com/neoand/neodoo18framework
- **Issues**: Reportar bugs e sugestões  
- **Pull Requests**: Contribuições sempre bem-vindas
- **Discussions**: Ajuda e dicas da comunidade

### Suporte:
- **Wiki**: Casos de uso avançados
- **Examples**: Projetos exemplo  
- **Updates**: Framework sempre atualizado

---

## 🎯 **CONCLUSÃO**

O **Neodoo18Framework** transforma desenvolvimento Odoo de **semanas em minutos**:

✅ **Templates Battle-Tested** - Padrões validados em produção  
✅ **100% Odoo 18+ Compliance** - Sem erros de compatibilidade  
✅ **Validação Automática** - Qualidade enterprise garantida  
✅ **IA-Friendly** - Sistema SOIL otimizado para LLMs  
✅ **Open Source** - MIT License, liberdade total  

**🚀 Start coding now!**

```bash
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework  
./quick-start.sh amazing_project
python3 framework/validator.py amazing_project/
# 100% = Ready for production! 🎉
```

---

**Happy Coding! 🎯**