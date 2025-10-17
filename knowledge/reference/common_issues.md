# Erros Comuns e Armadilhas no Odoo 18

## Erros de XML

### Tag `<tree>` ao invés de `<list>`
**Erro:**
```xml
<tree string="Parceiros">
    <field name="name"/>
</tree>
```

**Correto:**
```xml
<list string="Parceiros">
    <field name="name"/>
</list>
```

**Motivo:** No Odoo 18, visualizações de lista devem usar `<list>`. A tag `<tree>` é deprecated.

---

### Tags XML não fechadas
**Erro:**
```xml
<record id="view_form" model="ir.ui.view">
    <field name="model">res.partner</field>
    <field name="arch" type="xml">
        <form string="Partner">
            <group>
                <field name="name"/>
            <!-- Faltando fechar </group> e </form> -->
        </field>
</record>
```

**Correto:**
```xml
<record id="view_form" model="ir.ui.view">
    <field name="model">res.partner</field>
    <field name="arch" type="xml">
        <form string="Partner">
            <group>
                <field name="name"/>
            </group>
        </form>
    </field>
</record>
```

---

### Uso incorreto do `<chatter/>`
**Erro:**
```python
# Model sem herdar mail.thread
class MyModel(models.Model):
    _name = 'my.model'
```

```xml
<!-- View com chatter mas model não herda mail.thread -->
<form>
    <chatter/>
</form>
```

**Correto:**
```python
class MyModel(models.Model):
    _name = 'my.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
```

```xml
<form>
    <chatter/>
</form>
```

---

### External ID não encontrado
**Erro:**
```
ValueError: External ID not found in the system: module.xml_id_that_does_not_exist
```

**Causas comuns:**
1. Módulo de dependência não instalado
2. XML ID digitado errado
3. Arquivo XML não listado em `__manifest__.py`
4. Ordem incorreta de carregamento de arquivos

**Solução:**
```python
# __manifest__.py
'depends': ['base', 'sale', 'stock'],  # Adicione todas as dependências
'data': [
    'security/ir.model.access.csv',  # Security primeiro
    'views/menu.xml',  # Depois views
    'data/data.xml',  # Por último, dados
],
```

---

## Erros de Python

### Field não existe
**Erro:**
```
KeyError: 'Field xxx does not exist'
```

**Causas:**
1. Campo não declarado no modelo
2. Typo no nome do campo
3. Modelo dependente não carregado

**Solução:**
```python
# Verifique se o campo existe no modelo
class MyModel(models.Model):
    _name = 'my.model'

    my_field = fields.Char()  # Declare o campo

    # Ou se estiver herdando
    _inherit = 'res.partner'
    # Certifique-se que o módulo base está nas dependências
```

---

### RecordSet vazio com `ensure_one()`
**Erro:**
```
ValueError: Expected singleton: my.model()
```

**Causa:** Chamar `ensure_one()` em recordset vazio ou com múltiplos registros.

**Solução:**
```python
# ERRADO
record = self.search([('name', '=', 'Test')])
record.ensure_one()  # Pode falhar se não encontrar ou encontrar múltiplos

# CORRETO - opção 1
record = self.search([('name', '=', 'Test')], limit=1)
if record:
    # Processar record
    pass

# CORRETO - opção 2
records = self.search([('name', '=', 'Test')])
for record in records:
    # Processar cada record
    pass
```

---

### Uso incorreto de `create()` sem `@api.model_create_multi`
**Erro:**
```python
def create(self, vals):  # Sem decorator
    return super().create(vals)
# Pode causar problemas ao criar múltiplos registros
```

**Correto:**
```python
@api.model_create_multi
def create(self, vals_list):
    # vals_list é sempre lista
    return super().create(vals_list)
```

---

### Side effects em `compute` methods
**Erro:**
```python
@api.depends('amount')
def _compute_total(self):
    self.tax = self.amount * 0.1  # ERRADO - modificando outro campo
    self.total = self.amount + self.tax
```

**Correto:**
```python
@api.depends('amount')
def _compute_tax(self):
    for record in self:
        record.tax = record.amount * 0.1

@api.depends('amount', 'tax')
def _compute_total(self):
    for record in self:
        record.total = record.amount + record.tax
```

---

### Não usar `for record in self`
**Erro:**
```python
@api.depends('line_ids')
def _compute_total(self):
    # ERRADO - assume self é singleton
    self.total = sum(self.line_ids.mapped('amount'))
```

**Correto:**
```python
@api.depends('line_ids.amount')
def _compute_total(self):
    for record in self:
        record.total = sum(record.line_ids.mapped('amount'))
```

---

## Erros de Segurança

### Access Rights não definidos
**Erro:**
```
AccessError: You do not have access rights to this document
```

**Solução:** Criar `ir.model.access.csv`:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model user,model_my_model,base.group_user,1,1,1,1
access_my_model_manager,my.model manager,model_my_model,base.group_system,1,1,1,1
```

---

### Record Rules conflitantes
**Erro:** Usuários não veem registros que deveriam ver.

**Causa:** Record rules muito restritivas ou com `global=True`.

**Solução:**
```xml
<!-- Use global=False para regras específicas de grupo -->
<record id="rule_own_records" model="ir.rule">
    <field name="name">Own Records Only</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    <field name="global" eval="False"/>
</record>
```

---

## Erros de Performance

### Queries N+1
**Erro:**
```python
# ERRADO - faz uma query por linha
for line in order.line_ids:
    print(line.product_id.name)  # Query para cada product_id
```

**Correto:**
```python
# Carrega todos os produtos de uma vez
order.line_ids.mapped('product_id')
for line in order.line_ids:
    print(line.product_id.name)  # Sem queries adicionais
```

---

### Não usar `prefetch`
**Erro:**
```python
# Carrega todos os campos de todos os registros
partners = self.env['res.partner'].search([])
for partner in partners:
    print(partner.name)  # Carrega TUDO
```

**Correto:**
```python
# Carrega apenas campos necessários
partners = self.env['res.partner'].search([])
partners.read(['name'])  # Apenas o campo name
```

---

## Erros de Deploy

### Módulo não atualiza
**Causa:** Alterações em Python/XML não aplicadas.

**Solução:**
```bash
# Reinicie o Odoo com -u module_name
odoo-bin -u module_name -d database_name

# Ou atualize via interface
# Apps > Buscar módulo > Atualizar
```

---

### Dependências circulares
**Erro:**
```
ValueError: Circular dependency detected
```

**Causa:** Módulo A depende de B, e B depende de A.

**Solução:** Refatore para remover dependência circular ou crie módulo intermediário.

---

## Erros de OWL/JavaScript

### Componente não registra
**Erro:**
```
Component 'MyComponent' is not registered
```

**Solução:**
```javascript
/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class MyComponent extends Component {
    static template = "my_module.MyComponent";
}

registry.category("main_components").add("MyComponent", MyComponent);
```

---

## Checklist de Debug

Ao encontrar erros:

1. Verifique logs do Odoo (`--log-level=debug`)
2. Valide XML com `xmllint`
3. Verifique dependências em `__manifest__.py`
4. Confirme que arquivos estão listados em `data` no manifest
5. Reinicie o servidor após mudanças Python
6. Atualize o módulo após mudanças XML/data
7. Verifique permissões de acesso
8. Use modo debug do Odoo (adicione `?debug=1` na URL)
9. Inspecione elementos na interface para ver XML gerado
10. Use `pdb` para debug Python: `import pdb; pdb.set_trace()`