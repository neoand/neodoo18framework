# Guia de Desenvolvimento Rápido

Este guia fornece exemplos práticos e atalhos para acelerar o desenvolvimento com o Neodoo18Framework.

## 🚀 Criação de Projetos

### Criação de um Módulo Mínimo

```bash
# Criação rápida com setup.sh
./setup.sh
# Selecione 'minimal' quando solicitado o tipo de projeto

# Alternativa: Usando o gerador diretamente
python framework/generator/create_project.py --name=meu_modulo --type=minimal
```

## 📋 Templates Prontos para Uso

### Modelo Básico

```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MeuModelo(models.Model):
    _name = 'meu.modelo'
    _description = 'Meu Modelo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Nome', required=True, tracking=True)
    description = fields.Text(string='Descrição')
    date = fields.Date(string='Data')
    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('confirmed', 'Confirmado'),
        ('done', 'Concluído')
    ], string='Estado', default='draft', tracking=True)
    
    @api.depends('field1', 'field2')
    def _compute_result(self):
        for record in self:
            record.result = record.field1 + record.field2
```

### View XML Completa

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Form View -->
    <record id="view_meu_modelo_form" model="ir.ui.view">
        <field name="name">meu.modelo.form</field>
        <field name="model">meu.modelo</field>
        <field name="arch" type="xml">
            <form string="Meu Modelo">
                <header>
                    <button name="action_confirm" string="Confirmar" type="object" class="btn-primary" states="draft"/>
                    <button name="action_done" string="Concluir" type="object" class="btn-primary" states="confirmed"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,confirmed,done"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" placeholder="Nome"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="date"/>
                        </group>
                        <group>
                            <field name="description"/>
                        </group>
                    </group>
                </sheet>
                <div class="oe_chatter">
                    <field name="message_follower_ids" widget="mail_followers"/>
                    <field name="activity_ids" widget="mail_activity"/>
                    <field name="message_ids" widget="mail_thread"/>
                </div>
            </form>
        </field>
    </record>

    <!-- List View (Lembre-se: Sempre <list>, nunca <tree>) -->
    <record id="view_meu_modelo_list" model="ir.ui.view">
        <field name="name">meu.modelo.list</field>
        <field name="model">meu.modelo</field>
        <field name="arch" type="xml">
            <list string="Meu Modelo">
                <field name="name"/>
                <field name="date"/>
                <field name="state"/>
            </list>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_meu_modelo_search" model="ir.ui.view">
        <field name="name">meu.modelo.search</field>
        <field name="model">meu.modelo</field>
        <field name="arch" type="xml">
            <search string="Meu Modelo">
                <field name="name"/>
                <field name="description"/>
                <filter string="Rascunho" name="draft" domain="[('state','=','draft')]"/>
                <filter string="Confirmado" name="confirmed" domain="[('state','=','confirmed')]"/>
                <filter string="Concluído" name="done" domain="[('state','=','done')]"/>
                <group expand="0" string="Agrupar Por">
                    <filter string="Estado" name="state" context="{'group_by':'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Action -->
    <record id="action_meu_modelo" model="ir.actions.act_window">
        <field name="name">Meu Modelo</field>
        <field name="res_model">meu.modelo</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crie seu primeiro registro!
            </p>
        </field>
    </record>

    <!-- Menu -->
    <menuitem id="menu_meu_modulo" name="Meu Módulo" sequence="10"/>
    <menuitem id="menu_meu_modulo_root" name="Meu Modelo" parent="menu_meu_modulo" action="action_meu_modelo" sequence="1"/>
</odoo>
```

### Security - IR Model Access

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
        <record id="access_meu_modelo_user" model="ir.model.access">
            <field name="name">meu.modelo.user</field>
            <field name="model_id" ref="model_meu_modelo"/>
            <field name="group_id" ref="base.group_user"/>
            <field name="perm_read" eval="1"/>
            <field name="perm_write" eval="1"/>
            <field name="perm_create" eval="1"/>
            <field name="perm_unlink" eval="0"/>
        </record>

        <record id="access_meu_modelo_manager" model="ir.model.access">
            <field name="name">meu.modelo.manager</field>
            <field name="model_id" ref="model_meu_modelo"/>
            <field name="group_id" ref="base.group_system"/>
            <field name="perm_read" eval="1"/>
            <field name="perm_write" eval="1"/>
            <field name="perm_create" eval="1"/>
            <field name="perm_unlink" eval="1"/>
        </record>
    </data>
</odoo>
```

### Manifest Completo

```python
# -*- coding: utf-8 -*-
{
    'name': 'Meu Módulo',
    'version': '18.0.1.0.0',
    'category': 'Customizations',
    'summary': 'Descrição curta do módulo',
    'description': """
Descrição longa do módulo.
Pode ter múltiplas linhas.
    """,
    'author': 'Sua Empresa',
    'website': 'https://www.suaempresa.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/meu_modelo_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'meu_modulo/static/src/scss/style.scss',
            'meu_modulo/static/src/js/component.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

## 🔄 Operações Comuns

### Métodos ORM Úteis

```python
# Busca de registros
records = self.env['model.name'].search([('field', '=', value)])

# Criação de registro
new_record = self.env['model.name'].create({
    'field1': 'value1',
    'field2': 'value2',
})

# Atualização de registros
records.write({
    'field1': 'new_value',
})

# Contagem de registros
count = self.env['model.name'].search_count([('field', '=', value)])

# Busca paginada
records = self.env['model.name'].search([('field', '=', value)], limit=10, offset=0)

# Ordenação
records = self.env['model.name'].search([('field', '=', value)], order='name asc, date desc')
```

### Componentes OWL Comuns

```javascript
// Componente OWL Básico
import { Component } from "@odoo/owl";
import { useState } from "@odoo/owl";

export class MyComponent extends Component {
    setup() {
        this.state = useState({
            counter: 0,
            name: "",
        });
    }
    
    increment() {
        this.state.counter++;
    }
    
    updateName(ev) {
        this.state.name = ev.target.value;
    }
    
    async callServer() {
        const result = await this.env.services.rpc({
            model: "my.model",
            method: "my_method",
            args: [this.state.counter],
            kwargs: { name: this.state.name },
        });
        // Process result
    }
}

MyComponent.template = "module_name.MyComponentTemplate";
```

### XML para Template OWL

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="module_name.MyComponentTemplate" owl="1">
        <div class="my-component">
            <h2>My Component</h2>
            <div class="counter">
                <span>Counter: <t t-esc="state.counter"/></span>
                <button t-on-click="increment">Increment</button>
            </div>
            <div class="name-input">
                <label for="name">Name:</label>
                <input type="text" id="name" t-on-input="updateName" t-att-value="state.name"/>
            </div>
            <div t-if="state.name">
                <p>Hello, <t t-esc="state.name"/>!</p>
            </div>
            <button t-on-click="callServer" class="btn btn-primary">Call Server</button>
        </div>
    </t>
</templates>
```

## 🧪 Testes Rápidos

### Teste Unitário Básico

```python
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestMeuModelo(TransactionCase):

    def setUp(self):
        super(TestMeuModelo, self).setUp()
        self.modelo = self.env['meu.modelo'].create({
            'name': 'Teste',
            'description': 'Descrição de teste',
        })

    def test_confirmacao(self):
        self.assertEqual(self.modelo.state, 'draft')
        self.modelo.action_confirm()
        self.assertEqual(self.modelo.state, 'confirmed')
```

## 🔍 Validação Rápida

### Verificação de Código

```bash
# Validação rápida de arquivo
python framework/validator/validate.py models/meu_modelo.py

# Validação com auto-correção
python framework/validator/validate.py models/meu_modelo.py --auto-fix

# Validação de todo o módulo
python framework/validator/validate.py meu_modulo/
```

## 📦 Scaffolding Rápido

### Criar Novo Arquivo de Modelo

```bash
# Criar diretório se não existir
mkdir -p meu_modulo/models

# Criar arquivo de modelo
cat > meu_modulo/models/novo_modelo.py << 'EOF'
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class NovoModelo(models.Model):
    _name = 'novo.modelo'
    _description = 'Novo Modelo'
    
    name = fields.Char(string='Nome', required=True)
    # Adicione mais campos aqui
EOF

# Atualizar __init__.py
echo "from . import novo_modelo" >> meu_modulo/models/__init__.py
```

## 🎯 Dicas Importantes

1. **Sempre use `<list>` em vez de `<tree>`** para visualizações de lista.
2. **Sempre adicione `@api.depends()`** nos métodos de campos computados.
3. **Inclua cabeçalhos UTF-8** em todos os arquivos Python.
4. **Verifique os arquivos de segurança** para cada modelo.
5. **Use o validador frequentemente** para garantir conformidade com os padrões.

## 🔗 Links para Referência Rápida

- [[index|Documentação Principal]]
- [[workflows|Workflows e Processos]]
- [[faq|Perguntas Frequentes]]
- [[glossary|Glossário de Termos]]