# Dicas e Boas Praticas Python no Odoo 18

## Convencoes de Nomenclatura

### 1. Modelos (Models)

**Nomenclatura de Classes:**
```python
# Correto: PascalCase
class SaleOrder(models.Model):
    _name = 'sale.order'

class ResPartner(models.Model):
    _inherit = 'res.partner'

# Incorreto
class sale_order(models.Model):  # Evitar snake_case em classes
    pass
```

**Nomenclatura de _name:**
```python
# Correto: snake_case com namespace do modulo
class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'mail.thread'

# Padrao para modulos customizados
class CustomInventory(models.Model):
    _name = 'custom_module.inventory'

# Incorreto
class BadModel(models.Model):
    _name = 'BadModel'  # Evitar PascalCase
    _name = 'bad-model'  # Evitar hifens
```

### 2. Campos (Fields)

**Nomenclatura de Campos:**
```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    # Correto: snake_case
    partner_id = fields.Many2one('res.partner', string='Customer')
    date_order = fields.Datetime(string='Order Date')
    amount_total = fields.Monetary(string='Total')
    order_line_ids = fields.One2many('sale.order.line', 'order_id')

    # Many2one: sufixo _id
    user_id = fields.Many2one('res.users')
    company_id = fields.Many2one('res.company')

    # One2many e Many2many: sufixo _ids
    tag_ids = fields.Many2many('product.tag')
    invoice_ids = fields.One2many('account.move', 'sale_id')

    # Boolean: prefixo is_ ou has_
    is_exported = fields.Boolean()
    has_invoice = fields.Boolean()

    # Computed: prefixo computed_ (opcional mas recomendado)
    computed_total_tax = fields.Monetary(compute='_compute_total_tax')
```

### 3. Metodos

**Nomenclatura de Metodos:**
```python
class ProductProduct(models.Model):
    _name = 'product.product'

    # CRUD operations: snake_case
    def create_variant(self, vals):
        """Cria variante do produto"""
        pass

    # Metodos publicos: snake_case
    def action_update_price(self):
        """Action para atualizar preco"""
        pass

    # Metodos privados: prefixo _
    def _compute_price(self):
        """Computa preco do produto"""
        pass

    # Metodos de validacao: prefixo _check_
    def _check_stock_availability(self):
        """Valida disponibilidade em estoque"""
        pass

    # Constraints: @api.constrains
    @api.constrains('qty')
    def _check_quantity(self):
        """Valida quantidade"""
        pass

    # Onchange: @api.onchange
    @api.onchange('product_id')
    def _onchange_product(self):
        """Atualiza campos ao mudar produto"""
        pass
```

---

## Estrutura de Models

### 1. Ordem dos Elementos em um Model

```python
class SaleOrder(models.Model):
    """
    Sale Order Model

    Gerencia pedidos de venda do sistema.
    """
    # 1. Atributos privados
    _name = 'sale.order'
    _description = 'Sales Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc, id desc'
    _rec_name = 'name'
    _check_company_auto = True

    # 2. Campos padrao (obrigatorios do Odoo)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    # 3. Campos basicos (agrupados por tipo)
    # Char/Text
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default='New')
    note = fields.Text(string='Terms and Conditions')

    # Selection
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, default='draft', tracking=True)

    # Date/Datetime
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True,
                                 default=fields.Datetime.now, copy=False)

    # Monetary/Float/Integer
    amount_untaxed = fields.Monetary(string='Untaxed Amount', compute='_compute_amounts', store=True)
    amount_tax = fields.Monetary(string='Taxes', compute='_compute_amounts', store=True)
    amount_total = fields.Monetary(string='Total', compute='_compute_amounts', store=True)
    currency_id = fields.Many2one('res.currency', required=True)

    # 4. Campos relacionais
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, change_default=True)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    team_id = fields.Many2one('crm.team', string='Sales Team')

    order_line_ids = fields.One2many('sale.order.line', 'order_id', string='Order Lines')
    invoice_ids = fields.Many2many('account.move', compute='_compute_invoice_ids')

    # 5. Campos computados
    invoice_count = fields.Integer(compute='_compute_invoice_ids')

    # 6. SQL Constraints
    _sql_constraints = [
        ('name_uniq', 'unique(name, company_id)', 'Order reference must be unique per company!'),
    ]

    # 7. Metodos default/compute (ordem alfabetica)
    @api.depends('order_line_ids.price_total')
    def _compute_amounts(self):
        """Compute order amounts"""
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line_ids:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })

    def _compute_invoice_ids(self):
        """Compute invoices"""
        for order in self:
            invoices = self.env['account.move'].search([('sale_id', '=', order.id)])
            order.invoice_ids = invoices
            order.invoice_count = len(invoices)

    # 8. Constraints e validacoes
    @api.constrains('date_order')
    def _check_date_order(self):
        """Validate order date"""
        for order in self:
            if order.date_order and order.date_order > fields.Datetime.now():
                raise ValidationError('Order date cannot be in the future.')

    # 9. Onchange methods
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Update values when partner changes"""
        if self.partner_id:
            self.user_id = self.partner_id.user_id or self.env.user

    # 10. CRUD methods (create, write, unlink)
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to set sequence"""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or 'New'
        return super().create(vals_list)

    def write(self, vals):
        """Override write for custom logic"""
        # Custom validation
        if 'state' in vals and vals['state'] == 'cancel':
            for order in self:
                if order.invoice_ids.filtered(lambda inv: inv.state == 'posted'):
                    raise UserError('Cannot cancel order with posted invoices.')
        return super().write(vals)

    def unlink(self):
        """Override unlink to prevent deletion"""
        for order in self:
            if order.state not in ('draft', 'cancel'):
                raise UserError('Cannot delete confirmed orders.')
        return super().unlink()

    # 11. Action methods
    def action_confirm(self):
        """Confirm the sales order"""
        for order in self:
            order.state = 'sale'
        return True

    def action_cancel(self):
        """Cancel the sales order"""
        self.write({'state': 'cancel'})
        return True

    def action_view_invoice(self):
        """Action to view invoices"""
        return {
            'name': 'Invoices',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
        }

    # 12. Business methods (ordem alfabetica)
    def _create_invoices(self, grouped=False, final=False):
        """Create invoices for this order"""
        pass

    def _prepare_invoice(self):
        """Prepare invoice values"""
        self.ensure_one()
        return {
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'sale_id': self.id,
        }
```

---

## Decorators do Odoo 18

### 1. @api.model

Metodo de classe (nao depende de recordset).

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    @api.model
    def get_default_warehouse(self):
        """Retorna warehouse padrao"""
        return self.env['stock.warehouse'].search([], limit=1)

    @api.model
    def search_orders_by_date(self, date_from, date_to):
        """Busca orders por periodo"""
        return self.search([
            ('date_order', '>=', date_from),
            ('date_order', '<=', date_to),
        ])
```

### 2. @api.model_create_multi (Novo no Odoo 18)

Substitui `@api.model` para metodo `create`. Mais eficiente para criacao em lote.

```python
class ProductProduct(models.Model):
    _name = 'product.product'

    # Odoo 18 - Preferido
    @api.model_create_multi
    def create(self, vals_list):
        """Create products in batch"""
        for vals in vals_list:
            if 'code' not in vals:
                vals['code'] = self.env['ir.sequence'].next_by_code('product.product')
        products = super().create(vals_list)
        # Post-processing
        products._update_stock()
        return products

    # Odoo 17 e anteriores (ainda funciona, mas menos eficiente)
    @api.model
    def create(self, vals):
        """Old style create"""
        if 'code' not in vals:
            vals['code'] = self.env['ir.sequence'].next_by_code('product.product')
        return super().create(vals)
```

### 3. @api.depends

Define dependencias para campos computados.

```python
class SaleOrderLine(models.Model):
    _name = 'sale.order.line'

    product_id = fields.Many2one('product.product')
    product_uom_qty = fields.Float(string='Quantity')
    price_unit = fields.Float(string='Unit Price')
    discount = fields.Float(string='Discount (%)')
    tax_ids = fields.Many2many('account.tax')

    # Depends simples
    @api.depends('product_uom_qty', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.product_uom_qty * line.price_unit

    # Depends com campos relacionados
    @api.depends('product_id.list_price', 'product_id.standard_price')
    def _compute_margin(self):
        for line in self:
            line.margin = line.product_id.list_price - line.product_id.standard_price

    # Depends com multiplos niveis
    @api.depends('order_id.partner_id.country_id')
    def _compute_country_code(self):
        for line in self:
            line.country_code = line.order_id.partner_id.country_id.code

    # Depends complexo com funcao
    @api.depends('price_subtotal', 'tax_ids')
    def _compute_price_total(self):
        for line in self:
            taxes = line.tax_ids.compute_all(
                line.price_unit,
                line.order_id.currency_id,
                line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_id
            )
            line.price_total = taxes['total_included']
```

### 4. @api.depends_context

Novo no Odoo 18. Define dependencia de contexto.

```python
class ProductProduct(models.Model):
    _name = 'product.product'

    @api.depends_context('company', 'force_company')
    def _compute_company_price(self):
        """Compute price based on company context"""
        for product in self:
            company = self.env.company
            product.company_price = product.with_company(company).list_price
```

### 5. @api.constrains

Validacoes com raise de erro.

```python
class StockMove(models.Model):
    _name = 'stock.move'

    product_qty = fields.Float()
    product_uom_qty = fields.Float()

    @api.constrains('product_qty')
    def _check_quantity(self):
        """Validate quantity is positive"""
        for move in self:
            if move.product_qty < 0:
                raise ValidationError('Quantity cannot be negative.')

    @api.constrains('product_id', 'location_id')
    def _check_product_location(self):
        """Validate product can be stored in location"""
        for move in self:
            if move.product_id.type == 'service':
                raise ValidationError('Cannot move service products.')
```

### 6. @api.onchange

Atualiza valores em tempo real na interface.

```python
class SaleOrderLine(models.Model):
    _name = 'sale.order.line'

    product_id = fields.Many2one('product.product')
    product_uom_qty = fields.Float()
    price_unit = fields.Float()

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Update values when product changes"""
        if self.product_id:
            self.price_unit = self.product_id.list_price
            self.name = self.product_id.display_name

    @api.onchange('product_uom_qty', 'price_unit')
    def _onchange_quantity_price(self):
        """Update discount based on quantity"""
        if self.product_uom_qty >= 100:
            self.discount = 10.0
        elif self.product_uom_qty >= 50:
            self.discount = 5.0
        else:
            self.discount = 0.0

    # Retornar warning
    @api.onchange('product_id')
    def _onchange_product_warning(self):
        """Show warning if product is low in stock"""
        if self.product_id and self.product_id.qty_available < 10:
            return {
                'warning': {
                    'title': 'Low Stock',
                    'message': 'This product has low stock availability.'
                }
            }
```

### 7. @api.ondelete

Novo no Odoo 18. Validacoes antes de deletar.

```python
class AccountMove(models.Model):
    _name = 'account.move'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
    ])

    @api.ondelete(at_uninstall=False)
    def _unlink_if_draft(self):
        """Prevent deletion of posted entries"""
        for move in self:
            if move.state == 'posted':
                raise UserError('Cannot delete posted journal entries.')

    @api.ondelete(at_uninstall=True)
    def _unlink_at_module_uninstall(self):
        """Allow deletion only when uninstalling module"""
        pass
```

### 8. @api.autovacuum

Executa limpeza automatica de registros antigos.

```python
class MailMail(models.Model):
    _name = 'mail.mail'

    @api.autovacuum
    def _gc_sent_emails(self):
        """Garbage collect sent emails older than 30 days"""
        limit_date = fields.Datetime.now() - timedelta(days=30)
        self.search([
            ('state', '=', 'sent'),
            ('create_date', '<', limit_date),
        ]).unlink()
```

---

## Performance Tips

### 1. Evitar Queries em Loops

```python
# RUIM - N+1 queries
def compute_total_sales(self):
    for partner in self.env['res.partner'].search([]):
        orders = self.env['sale.order'].search([('partner_id', '=', partner.id)])
        partner.total_sales = sum(orders.mapped('amount_total'))

# BOM - Uma query com read_group
def compute_total_sales(self):
    result = self.env['sale.order'].read_group(
        domain=[],
        fields=['partner_id', 'amount_total:sum'],
        groupby=['partner_id']
    )
    totals = {r['partner_id'][0]: r['amount_total'] for r in result}

    for partner in self.env['res.partner'].search([]):
        partner.total_sales = totals.get(partner.id, 0.0)
```

### 2. Usar Campos Stored

```python
# RUIM - Compute sem store (calculado sempre)
class SaleOrder(models.Model):
    _name = 'sale.order'

    amount_total = fields.Monetary(compute='_compute_amount_total')

    @api.depends('order_line_ids.price_total')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(order.order_line_ids.mapped('price_total'))

# BOM - Compute com store (calculado uma vez)
class SaleOrder(models.Model):
    _name = 'sale.order'

    amount_total = fields.Monetary(compute='_compute_amount_total', store=True)

    @api.depends('order_line_ids.price_total')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(order.order_line_ids.mapped('price_total'))
```

### 3. Usar read() ao inves de browse()

```python
# RUIM - Carrega todos os campos
partners = self.env['res.partner'].browse([1, 2, 3])
for partner in partners:
    print(partner.name, partner.email)

# BOM - Carrega apenas campos necessarios
partners_data = self.env['res.partner'].browse([1, 2, 3]).read(['name', 'email'])
for partner in partners_data:
    print(partner['name'], partner['email'])
```

### 4. Prefetch e Batch Operations

```python
# RUIM - Acessa registros um por um
def update_products(product_ids):
    for product_id in product_ids:
        product = self.env['product.product'].browse(product_id)
        product.write({'active': True})

# BOM - Batch operation
def update_products(product_ids):
    products = self.env['product.product'].browse(product_ids)
    products.write({'active': True})

# MELHOR - Com prefetch manual se necessario
def update_products(product_ids):
    products = self.env['product.product'].browse(product_ids)
    products._prefetch_field('name')  # Pre-carrega campo se necessario
    products.write({'active': True})
```

### 5. Usar search_count ao inves de len(search())

```python
# RUIM - Carrega todos registros para contar
order_count = len(self.env['sale.order'].search([('state', '=', 'sale')]))

# BOM - Conta direto no banco
order_count = self.env['sale.order'].search_count([('state', '=', 'sale')])
```

### 6. Limitar Resultados de Busca

```python
# RUIM - Busca todos e pega primeiro
latest_order = self.env['sale.order'].search([])[-1]

# BOM - Limita na query
latest_order = self.env['sale.order'].search([], order='id desc', limit=1)
```

### 7. Invalidar Cache Apenas Quando Necessario

```python
class ProductProduct(models.Model):
    _name = 'product.product'

    def _update_price_external(self):
        """Update price from external API"""
        for product in self:
            new_price = self._fetch_price_from_api(product.code)
            # Evita invalidar cache desnecessariamente
            if product.list_price != new_price:
                product.list_price = new_price
```

---

## Security Best Practices

### 1. Record Rules (ir.rule)

```python
# No arquivo security/security.xml
<odoo>
    <data noupdate="1">
        <!-- Rule para usuario ver apenas seus proprios pedidos -->
        <record id="sale_order_personal_rule" model="ir.rule">
            <field name="name">Personal Sale Orders</field>
            <field name="model_id" ref="model_sale_order"/>
            <field name="domain_force">[('user_id', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
            <field name="perm_read" eval="1"/>
            <field name="perm_write" eval="1"/>
            <field name="perm_create" eval="1"/>
            <field name="perm_unlink" eval="1"/>
        </record>

        <!-- Rule para manager ver todos -->
        <record id="sale_order_manager_rule" model="ir.rule">
            <field name="name">All Sale Orders for Manager</field>
            <field name="model_id" ref="model_sale_order"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_manager'))]"/>
        </record>

        <!-- Rule com dominio complexo -->
        <record id="sale_order_team_rule" model="ir.rule">
            <field name="name">Team Sale Orders</field>
            <field name="model_id" ref="model_sale_order"/>
            <field name="domain_force">['|', ('user_id', '=', user.id), ('team_id.member_ids', 'in', [user.id])]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>
    </data>
</odoo>
```

### 2. Field Level Security

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    # Campo visivel apenas para managers
    internal_note = fields.Text(
        groups='sales_team.group_sale_manager'
    )

    # Campo editavel apenas para managers
    discount_rate = fields.Float(
        readonly=True,
        groups='sales_team.group_sale_manager'
    )

    # Readonly dinamico
    state = fields.Selection(
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
```

### 3. Validacao de Permissoes em Codigo

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    def action_confirm(self):
        """Confirm order - only for salesperson"""
        # Verifica permissao
        if not self.env.user.has_group('sales_team.group_sale_salesman'):
            raise AccessError('Only salespeople can confirm orders.')

        # Verifica company
        self.check_access_rights('write')
        self.check_access_rule('write')

        return super().action_confirm()

    def _check_can_modify(self):
        """Check if current user can modify this order"""
        self.ensure_one()
        if self.state == 'done' and not self.env.user.has_group('sales_team.group_sale_manager'):
            raise UserError('Only managers can modify confirmed orders.')
```

### 4. Sudo() - Usar com Cuidado

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    def _create_invoice_internal(self):
        """Create invoice bypassing security (internal use)"""
        # RUIM - sudo sem necessidade
        invoice = self.env['account.move'].sudo().create({
            'partner_id': self.partner_id.id,
        })

        # BOM - sudo apenas quando realmente necessario
        # E com validacao de permissoes antes
        if not self.env.user.has_group('account.group_account_invoice'):
            raise AccessError('Cannot create invoices.')

        # Cria invoice com sudo apenas se usuario nao for owner
        if self.partner_id.user_id != self.env.user:
            invoice = self.env['account.move'].sudo().create({
                'partner_id': self.partner_id.id,
            })
        else:
            invoice = self.env['account.move'].create({
                'partner_id': self.partner_id.id,
            })

        return invoice
```

---

## Testing Guidelines

### 1. Estrutura de Testes

```python
# tests/__init__.py
from . import test_sale_order
from . import test_sale_order_line

# tests/test_sale_order.py
from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError, ValidationError


@tagged('post_install', '-at_install')
class TestSaleOrder(TransactionCase):
    """Test suite for Sale Orders"""

    @classmethod
    def setUpClass(cls):
        """Setup test data"""
        super().setUpClass()

        # Create test data
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
        })

        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'type': 'consu',
        })

    def setUp(self):
        """Setup before each test"""
        super().setUp()
        self.order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })

    def test_01_create_order(self):
        """Test creating a sale order"""
        self.assertTrue(self.order)
        self.assertEqual(self.order.state, 'draft')
        self.assertEqual(self.order.partner_id, self.partner)

    def test_02_add_order_line(self):
        """Test adding order line"""
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2,
        })

        self.assertEqual(len(self.order.order_line_ids), 1)
        self.assertEqual(line.price_unit, self.product.list_price)

    def test_03_confirm_order(self):
        """Test confirming order"""
        self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.id,
            'product_uom_qty': 1,
        })

        self.order.action_confirm()
        self.assertEqual(self.order.state, 'sale')

    def test_04_validate_quantity(self):
        """Test quantity validation"""
        with self.assertRaises(ValidationError):
            self.env['sale.order.line'].create({
                'order_id': self.order.id,
                'product_id': self.product.id,
                'product_uom_qty': -1,
            })

    def test_05_compute_amounts(self):
        """Test amount computation"""
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2,
            'price_unit': 100,
        })

        self.assertEqual(self.order.amount_untaxed, 200.0)
```

### 2. Testes de Performance

```python
from odoo.tests import TransactionCase
import time


class TestPerformance(TransactionCase):
    """Performance tests"""

    def test_batch_create_performance(self):
        """Test batch creation is faster"""
        # Test individual creates
        start = time.time()
        for i in range(100):
            self.env['res.partner'].create({'name': f'Partner {i}'})
        individual_time = time.time() - start

        # Test batch create
        start = time.time()
        self.env['res.partner'].create([
            {'name': f'Partner Batch {i}'} for i in range(100)
        ])
        batch_time = time.time() - start

        # Batch should be faster
        self.assertLess(batch_time, individual_time)
```

### 3. Testes com Mock

```python
from unittest.mock import patch
from odoo.tests import TransactionCase


class TestExternalAPI(TransactionCase):
    """Test external API integration"""

    @patch('requests.get')
    def test_fetch_exchange_rate(self, mock_get):
        """Test fetching exchange rate from API"""
        # Mock API response
        mock_get.return_value.json.return_value = {
            'rates': {'USD': 1.2}
        }

        rate = self.env['res.currency']._fetch_exchange_rate('EUR', 'USD')
        self.assertEqual(rate, 1.2)

        # Verify API was called
        mock_get.assert_called_once()
```

---

## Code Organization

### 1. Estrutura de Modulo

```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── sale_order.py
│   ├── sale_order_line.py
│   └── res_partner.py
├── views/
│   ├── sale_order_views.xml
│   ├── sale_order_line_views.xml
│   └── menu.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── data/
│   ├── data.xml
│   └── sequences.xml
├── demo/
│   └── demo_data.xml
├── wizard/
│   ├── __init__.py
│   ├── sale_order_wizard.py
│   └── sale_order_wizard_views.xml
├── report/
│   ├── __init__.py
│   ├── sale_order_report.py
│   └── sale_order_report_template.xml
├── static/
│   ├── src/
│   │   ├── js/
│   │   ├── xml/
│   │   └── scss/
│   └── description/
│       └── icon.png
└── tests/
    ├── __init__.py
    └── test_sale_order.py
```

### 2. Manifest File

```python
# __manifest__.py
{
    'name': 'My Module',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom Sales Module',
    'description': """
        Long description of the module.
        Can be multiple lines.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'stock',
        'account',
    ],
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',

        # Data
        'data/sequences.xml',
        'data/data.xml',

        # Views
        'views/sale_order_views.xml',
        'views/menu.xml',

        # Wizards
        'wizard/sale_order_wizard_views.xml',

        # Reports
        'report/sale_order_report_template.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'my_module/static/src/js/**/*',
            'my_module/static/src/xml/**/*',
            'my_module/static/src/scss/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

---

## Documentacao de Codigo

### 1. Docstrings em Models

```python
class SaleOrder(models.Model):
    """
    Sale Order Model

    Manages sales orders in the system. Inherits from mail.thread
    for messaging and activity tracking.

    Attributes:
        name (Char): Order reference number
        partner_id (Many2one): Customer
        order_line_ids (One2many): Order lines
        state (Selection): Order status
    """
    _name = 'sale.order'
    _description = 'Sales Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Order Reference',
        help='Unique reference for this order',
        required=True,
        copy=False,
    )
```

### 2. Docstrings em Metodos

```python
def action_confirm(self):
    """
    Confirm the sales order

    Sets the order state to 'sale' and triggers the delivery
    process. Creates stock picking if products are stockable.

    Returns:
        bool: True if confirmation successful

    Raises:
        UserError: If order has no lines
        ValidationError: If partner has no delivery address

    Examples:
        >>> order.action_confirm()
        True
    """
    if not self.order_line_ids:
        raise UserError('Cannot confirm order without lines.')

    self.write({'state': 'sale'})
    self._create_picking()
    return True
```

### 3. Comentarios Inline

```python
def _compute_amount_total(self):
    """Compute total amounts"""
    for order in self:
        # Initialize amounts
        amount_untaxed = amount_tax = 0.0

        # Sum line amounts
        for line in order.order_line_ids:
            amount_untaxed += line.price_subtotal

            # Calculate taxes
            taxes = line.tax_ids.compute_all(
                line.price_unit,
                order.currency_id,
                line.product_uom_qty,
            )
            amount_tax += taxes['total_included'] - taxes['total_excluded']

        # Update order amounts
        order.update({
            'amount_untaxed': amount_untaxed,
            'amount_tax': amount_tax,
            'amount_total': amount_untaxed + amount_tax,
        })
```

---

## Otimizacao de Queries

### 1. Use read_group para Agregacoes

```python
# RUIM
def get_sales_by_partner(self):
    partners = self.env['res.partner'].search([])
    result = {}
    for partner in partners:
        orders = self.env['sale.order'].search([('partner_id', '=', partner.id)])
        result[partner.id] = sum(orders.mapped('amount_total'))
    return result

# BOM
def get_sales_by_partner(self):
    data = self.env['sale.order'].read_group(
        domain=[('state', '=', 'sale')],
        fields=['partner_id', 'amount_total:sum'],
        groupby=['partner_id']
    )
    return {r['partner_id'][0]: r['amount_total'] for r in data}
```

### 2. Use search_read ao inves de search + read

```python
# RUIM
partners = self.env['res.partner'].search([('customer_rank', '>', 0)])
partner_data = partners.read(['name', 'email'])

# BOM
partner_data = self.env['res.partner'].search_read(
    domain=[('customer_rank', '>', 0)],
    fields=['name', 'email']
)
```

### 3. Evite Computeds Complexos sem Store

```python
# RUIM - Computed sem store e complexo
class ProductProduct(models.Model):
    _name = 'product.product'

    total_sales = fields.Float(compute='_compute_total_sales')

    def _compute_total_sales(self):
        for product in self:
            orders = self.env['sale.order.line'].search([
                ('product_id', '=', product.id)
            ])
            product.total_sales = sum(orders.mapped('price_total'))

# BOM - Use scheduled action para atualizar periodicamente
class ProductProduct(models.Model):
    _name = 'product.product'

    total_sales = fields.Float(store=True)

    @api.model
    def _cron_update_total_sales(self):
        """Cron to update total sales"""
        data = self.env['sale.order.line'].read_group(
            domain=[],
            fields=['product_id', 'price_total:sum'],
            groupby=['product_id']
        )
        for item in data:
            product = self.env['product.product'].browse(item['product_id'][0])
            product.total_sales = item['price_total']
```

### 4. Use flush() e invalidate_cache() com Cuidado

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    def custom_update_bulk(self, vals):
        """Bulk update with manual cache control"""
        # Disable auto-flush
        self.env.cr.execute("""
            UPDATE sale_order
            SET state = %s
            WHERE id IN %s
        """, (vals['state'], tuple(self.ids)))

        # Manual cache invalidation
        self.invalidate_cache(['state'])

        # Or flush specific fields
        # self.flush(['state'])
```

---

## Padroes Comuns

### 1. Wizard Pattern

```python
# wizard/sale_order_wizard.py
class SaleOrderWizard(models.TransientModel):
    _name = 'sale.order.wizard'
    _description = 'Sale Order Wizard'

    order_ids = fields.Many2many('sale.order')
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    def action_confirm_orders(self):
        """Confirm selected orders"""
        self.ensure_one()

        orders = self.order_ids.filtered(
            lambda o: o.state == 'draft' and
            o.date_order >= self.date_from and
            o.date_order <= self.date_to
        )

        orders.action_confirm()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'{len(orders)} orders confirmed.',
                'type': 'success',
                'sticky': False,
            }
        }
```

### 2. Abstract Model Pattern

```python
class AbstractProduct(models.AbstractModel):
    """Abstract model for products"""
    _name = 'abstract.product'
    _description = 'Abstract Product'

    name = fields.Char(required=True)
    code = fields.Char()
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique!')
    ]

class ProductTemplate(models.Model):
    """Product template inherits abstract"""
    _name = 'product.template'
    _inherit = 'abstract.product'
```

### 3. Mixin Pattern

```python
class SequenceMixin(models.AbstractModel):
    """Mixin to add sequence functionality"""
    _name = 'sequence.mixin'
    _description = 'Sequence Mixin'

    name = fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self._get_next_sequence()
        return super().create(vals_list)

    def _get_next_sequence(self):
        """Get next sequence number"""
        sequence_code = f'{self._name}.sequence'
        return self.env['ir.sequence'].next_by_code(sequence_code) or '/'

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sequence.mixin', 'mail.thread']
```

---

## Tratamento de Erros

```python
from odoo.exceptions import (
    AccessError,
    UserError,
    ValidationError,
    RedirectWarning,
)

class SaleOrder(models.Model):
    _name = 'sale.order'

    def action_confirm(self):
        """Confirm order with proper error handling"""
        # UserError - Erro de usuario
        if not self.order_line_ids:
            raise UserError('Cannot confirm order without lines.')

        # ValidationError - Erro de validacao
        if self.amount_total <= 0:
            raise ValidationError('Order total must be greater than zero.')

        # AccessError - Erro de permissao
        if not self.env.user.has_group('sales_team.group_sale_salesman'):
            raise AccessError('Only salespeople can confirm orders.')

        # RedirectWarning - Erro com acao de redirecionamento
        if not self.partner_id.property_payment_term_id:
            action = self.env.ref('account.action_payment_term_form')
            raise RedirectWarning(
                'No payment term defined for customer.',
                action.id,
                'Configure Payment Term'
            )

        return super().action_confirm()
```

---

## Boas Praticas Gerais

1. **Use always ensure_one()** quando metodo espera um unico registro
2. **Evite side effects** em metodos compute
3. **Prefira @api.model_create_multi** ao inves de @api.model no create
4. **Use store=True** em campos computados frequentemente acessados
5. **Adicione indices** em campos usados em buscas frequentes
6. **Documente** seu codigo com docstrings
7. **Escreva testes** para funcionalidades criticas
8. **Use record rules** ao inves de verificacoes manuais de seguranca
9. **Evite sudo()** sempre que possivel
10. **Prefira batch operations** ao inves de loops

---

## Checklist de Codigo

- [ ] Codigo segue convencoes de nomenclatura
- [ ] Models tem _name, _description definidos
- [ ] Campos tem string e help text
- [ ] Metodos tem docstrings
- [ ] Decorators corretos (@api.depends, @api.constrains, etc)
- [ ] Validacoes de seguranca implementadas
- [ ] Tests escritos e passando
- [ ] Performance otimizada (sem N+1 queries)
- [ ] Codigo documentado
- [ ] Access rights e record rules configurados
