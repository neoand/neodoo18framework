# Mudanças de API / ORM no Odoo 18

Este documento detalha as principais mudanças na API Python e ORM do Odoo 18 em relação às versões anteriores.

## Mudanças no ORM

### Decorators Removidos
- **`@api.multi`**: REMOVIDO - não use mais decorators para métodos multi-registro
- **`@api.one`**: REMOVIDO - substitua por `@api.model` ou sem decorator
- **`@api.returns()`**: REMOVIDO em muitos casos - o ORM infere automaticamente

### Novos Decorators e Comportamentos

#### `@api.model_create_multi`
Obrigatório para criar múltiplos registros de forma eficiente:
```python
@api.model_create_multi
def create(self, vals_list):
    # vals_list é sempre uma lista de dicionários
    records = super().create(vals_list)
    return records
```

#### `@api.model_create_single`
Para criar um único registro (preferível quando aplicável):
```python
@api.model_create_single
def create(self, vals):
    # vals é um único dicionário
    record = super().create(vals)
    return record
```

### Mudanças em Fields

#### Tracking
```python
# Odoo 17 e anteriores
name = fields.Char(track_visibility='onchange')

# Odoo 18
name = fields.Char(tracking=True)
```

#### Selection Fields
```python
# Herança de selections agora usa tuplas
class MyModel(models.Model):
    _inherit = 'base.model'

    state = fields.Selection(selection_add=[
        ('new_state', 'New State'),
    ], ondelete={'new_state': 'cascade'})
```

#### Related Fields
```python
# Melhor performance com store=True e índices
partner_name = fields.Char(
    related='partner_id.name',
    store=True,  # Armazena no banco
    index=True,  # Cria índice
    readonly=True
)
```

### Mudanças em Métodos CRUD

#### create()
```python
# Agora suporta lista de dicts nativamente
records = self.env['res.partner'].create([
    {'name': 'Partner 1'},
    {'name': 'Partner 2'},
])
```

#### write()
```python
# Validações mais rigorosas em campos readonly
# Use sudo() com cuidado
record.sudo().write({'readonly_field': 'value'})
```

#### search()
```python
# Operador 'ilike' com melhor performance
# Novos operadores de data
records = self.search([
    ('date', '>=', fields.Date.today()),
    ('name', 'ilike', 'search%'),  # Prefira % no final
])
```

### Computed Fields

#### Mudanças em @api.depends
```python
# Agora aceita campos relacionados mais profundos
@api.depends('line_ids.product_id.price')
def _compute_total(self):
    for record in self:
        record.total = sum(record.line_ids.mapped('product_id.price'))
```

#### Evite Side Effects
```python
# ERRADO - não modifique outros campos em compute
@api.depends('amount')
def _compute_tax(self):
    self.total = self.amount + self.tax  # NÃO FAÇA ISSO

# CORRETO - cada campo tem seu próprio compute
@api.depends('amount', 'tax')
def _compute_total(self):
    self.total = self.amount + self.tax
```

### Constrained Methods

```python
# Use @api.constrains com campos específicos
@api.constrains('start_date', 'end_date')
def _check_dates(self):
    for record in self:
        if record.start_date > record.end_date:
            raise ValidationError("Start date must be before end date")
```

### Onchange Methods

```python
# Retorne dicionário com 'value', 'warning' ou 'domain'
@api.onchange('partner_id')
def _onchange_partner_id(self):
    if self.partner_id:
        self.email = self.partner_id.email
        return {
            'warning': {
                'title': 'Warning',
                'message': 'Partner selected'
            },
            'domain': {
                'invoice_ids': [('partner_id', '=', self.partner_id.id)]
            }
        }
```

## Environment e Context

### Mudanças no Environment
```python
# Cache melhorado - use invalidate_model() e invalidate_recordset()
self.env['res.partner'].invalidate_model(['name', 'email'])

# Prefira env.cr.commit() explícito em casos específicos
# Evite auto_commit em loops
```

### Context
```python
# Novos contextos padrão
self.with_context(
    active_test=False,  # Inclui registros arquivados
    tracking_disable=True,  # Desabilita chatter tracking
    mail_create_nosubscribe=True,  # Não inscrever criador
    no_reset_password=True,  # Não enviar email de reset
)
```

## SQL e Performance

### Raw SQL
```python
# Use parametrização para evitar SQL injection
self.env.cr.execute(
    "SELECT id FROM res_partner WHERE name = %s",
    (name,)  # Tupla de parâmetros
)
results = self.env.cr.fetchall()
```

### Flush e Invalidate
```python
# Forçar escrita no banco antes de SQL direto
self.env['res.partner'].flush_model(['name', 'email'])

# Invalidar cache após SQL direto
self.env['res.partner'].invalidate_model()
```

## Módulos e Herança

### Herança de Modelos
```python
# _inherit sem _name (herança por extensão)
class ResPartner(models.Model):
    _inherit = 'res.partner'
    new_field = fields.Char()

# _inherit com _name (herança por delegação/mixin)
class MyMixin(models.AbstractModel):
    _name = 'my.mixin'
    _description = 'My Mixin'

class MyModel(models.Model):
    _name = 'my.model'
    _inherit = ['my.mixin', 'mail.thread']
```

### Herança de Métodos
```python
# Use super() corretamente
def write(self, vals):
    # Lógica antes
    result = super().write(vals)
    # Lógica depois
    return result
```

## Segurança e Access Rights

### Record Rules
```python
# Mudanças no eval de domain
# Prefira usar user.id ao invés de uid
<record id="rule_own_records" model="ir.rule">
    <field name="domain_force">[('user_id', '=', user.id)]</field>
</record>
```

### Sudo e Access Rights
```python
# sudo() bypass TODOS os access rights - use com cuidado
# Prefira verificar permissões explicitamente
if self.env.user.has_group('base.group_system'):
    record.sudo().write({'sensitive_field': value})
```

## Deprecated APIs

### APIs Removidas ou Depreciadas
- `one2many_list`: use lista Python normal
- `search_count(limit=N)`: removido, use sem limit
- `mapped('field').ids`: simplifique para `ids`
- `ensure_one()` em loops: desnecessário se iterar com `for record in self`

## Novas Features

### Batch Operations
```python
# Operações em lote otimizadas
self.env['res.partner'].create_or_update([...])  # Novo método
```

### Better Defaults
```python
# Defaults dinâmicos
def _default_date(self):
    return fields.Date.context_today(self)

date = fields.Date(default=_default_date)
```