# Odoo 18+ Core Standards

> **Padrões Obrigatórios para Desenvolvimento Odoo 18 e Superiores**

## 🚨 REGRA DE OURO

**NUNCA USAR PADRÕES DE VERSÕES ANTERIORES À ODOO 18**

Este documento define os padrões obrigatórios que eliminam problemas comuns em desenvolvimento Odoo 18+.

## 📋 XML Views Standards

### ✅ CORRETO - Odoo 18+

```xml
<!-- List Views -->
<record id="model_view_list" model="ir.ui.view">
    <field name="name">model.view.list</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <list string="Models">  <!-- SEMPRE <list> -->
            <field name="name"/>
        </list>
    </field>
</record>

<!-- Actions -->
<record id="model_action" model="ir.actions.act_window">
    <field name="name">Models</field>
    <field name="res_model">my.model</field>
    <field name="view_mode">list,form</field>  <!-- SEMPRE list,form -->
</record>
```

### ❌ INCORRETO - Versões Antigas

```xml
<!-- NUNCA USAR -->
<tree string="Models">  <!-- DEPRECATED em Odoo 18+ -->
</tree>

<!-- NUNCA USAR -->
<field name="view_mode">tree,form</field>  <!-- DEPRECATED -->
```

## 🐍 Python Models Standards

### ✅ Template Padrão

```python
# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model Description'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    
    # Campos básicos
    name = fields.Char(string='Name', required=True, tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    
    # Campos computados com depends
    @api.depends('field_name')
    def _compute_something(self):
        for record in self:
            record.computed_field = calculation
    
    computed_field = fields.Char(compute='_compute_something', store=True)
    
    # Constraints
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name:
                raise ValidationError(_("Name is required"))
    
    # Actions
    def action_confirm(self):
        self.ensure_one()
        # Action logic here
        return True
```

## 🔒 Security Standards

### Model Access (ir.model.access.csv)

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,group_user,1,0,0,0
access_my_model_manager,my.model.manager,model_my_model,group_manager,1,1,1,1
```

### Security Groups (XML)

```xml
<record id="group_manager" model="res.groups">
    <field name="name">My Module Manager</field>
    <field name="category_id" ref="base.module_category_operations"/>
</record>
```

### Record Rules

```xml
<record id="my_model_rule" model="ir.rule">
    <field name="name">My Model Access Rule</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="domain_force">[('active', '=', True)]</field>
    <field name="groups" eval="[(4, ref('group_user'))]"/>
</record>
```

## 📁 Module Structure Standards

```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   ├── my_model_views.xml
│   └── my_menu_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── my_security.xml
├── data/
│   └── my_data.xml
└── static/
    └── description/
        └── icon.png
```

## 🎯 Manifest Standards

```python
# -*- coding: utf-8 -*-
{
    'name': 'My Module',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Brief module description',
    'description': """
Long module description
    """,
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/my_security.xml',
        'views/my_model_views.xml',
        'views/my_menu_views.xml',
        'data/my_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
```

## ⚡ Performance Standards

### Database Optimization

```python
# Use índices quando necessário
class MyModel(models.Model):
    name = fields.Char(index=True)  # Para buscas frequentes
    
    # Use SQL constraints para performance
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name must be unique!'),
    ]
```

### Computed Fields

```python
# SEMPRE usar @api.depends
@api.depends('line_ids.amount')
def _compute_total(self):
    for record in self:
        record.total = sum(record.line_ids.mapped('amount'))

# Armazenar se necessário para performance
total = fields.Float(compute='_compute_total', store=True)
```

## 🚨 Common Errors to Avoid

### XML Errors

- ❌ `<tree>` tags (use `<list>`)
- ❌ `view_mode="tree,form"` (use `list,form`)
- ❌ Missing field refs in many2one
- ❌ Incorrect XML structure

### Python Errors

- ❌ Missing `@api.depends` in computed fields
- ❌ Not using `self.ensure_one()` in action methods
- ❌ Missing encoding declaration
- ❌ Wrong import order

### Security Errors

- ❌ Missing model access rules
- ❌ Overly permissive access
- ❌ Missing security groups
- ❌ Incorrect record rules

## 🔄 Migration from Older Versions

### Quick Fix Commands

```bash
# Replace deprecated tree tags
find . -name "*.xml" -exec sed -i 's/<tree/<list/g' {} \;
find . -name "*.xml" -exec sed -i 's/<\/tree>/<\/list>/g' {} \;

# Replace view_mode
find . -name "*.xml" -exec sed -i 's/tree,form/list,form/g' {} \;
```

## 📊 Validation Checklist

Before any deployment:

- [ ] All views use `<list>` not `<tree>`
- [ ] All actions use `view_mode="list,form"`
- [ ] All models have proper encoding
- [ ] All computed fields have `@api.depends`
- [ ] All security rules defined
- [ ] Module structure follows standards
- [ ] No deprecated patterns used

---

**Remember**: These standards are non-negotiable for Odoo 18+ development. Following them ensures compatibility, performance, and maintainability.
 
## ✅ Regras Não-Negociáveis Adicionais (Odoo 18+)

1) Manifesto disciplinado
- version: deve começar com 18.0. e seguir 18.0.x.y.z
- chaves obrigatórias: name, version, depends, data, license
- depends: obrigatoriamente list/array; installable/application: booleanos
- ordem de carregamento: security (security/*.xml, security/ir.model.access.csv) antes de views/*.xml
- todos os arquivos listados em data devem existir no módulo

2) Nomenclatura consistente
- nome técnico do módulo = nome do diretório, em snake_case começando por letra
- models: _name deve usar prefixo do módulo, ex.: my_module.model
- XML ids (record/menu/view/action): prefixo do módulo para evitar colisões

3) Padrões de segurança
- ir.model.access.csv com cabeçalho exato:
    id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
- cada modelo “usável” deve ter regra(s) de acesso adequadas
- evitar sudo salvo quando indispensável e documentado

4) Padrões Python adicionais
- métodos de ação (def action_...): chamar self.ensure_one() quando operar em um registro
- criar registros com @api.model_create_multi quando aplicável
- evitar print; usar _logger com níveis adequados (info/warning/error)
- usar _sql_constraints e index=True para unicidade/performance quando fizer sentido

5) Padrões XML adicionais
- quando existir view form, as ações relacionadas devem incluir form em view_mode (ex.: list,form)
- search views com filtros e group_by para usabilidade (quando aplicável)

6) Estrutura e carregamento
- models/__init__.py deve importar todos os .py existentes em models/
- nomes de arquivos coerentes: views/<module>_views.xml, <module>_menu.xml, security/<module>_security.xml

7) Internacionalização mínima
- mensagens ao usuário e erros devem usar _(…) para i18n

## 📋 Checklist adicional
- [ ] Manifesto com 18.0.*, chaves obrigatórias, tipos corretos e ordem de data (security antes de views)
- [ ] access.csv presente, cabeçalho correto e citado no manifesto
- [ ] models/__init__.py importa todos os arquivos do diretório
- [ ] Sem prints; ações com ensure_one quando aplicável
- [ ] IDs XML com prefixo do módulo (evitar colisões)