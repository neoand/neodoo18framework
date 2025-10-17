# Odoo 18 Best Practices Guide

## Comprehensive Best Practices for Odoo 18 Development

This guide covers architecture patterns, coding standards, security, performance optimization, and deployment best practices for Odoo 18.

---

## Table of Contents

1. [Module Architecture](#module-architecture)
2. [Code Organization](#code-organization)
3. [Python Best Practices](#python-best-practices)
4. [JavaScript Best Practices](#javascript-best-practices)
5. [XML/View Best Practices](#xmlview-best-practices)
6. [Security Best Practices](#security-best-practices)
7. [Performance Optimization](#performance-optimization)
8. [Testing Standards](#testing-standards)
9. [Documentation Standards](#documentation-standards)
10. [Deployment Best Practices](#deployment-best-practices)
11. [Code Review Checklist](#code-review-checklist)

---

## Module Architecture

### Module Structure

**Recommended Directory Structure**:

```
my_module/
├── __init__.py                 # Module initialization
├── __manifest__.py             # Module manifest
├── models/                     # Business logic
│   ├── __init__.py
│   ├── my_model.py
│   ├── res_partner.py          # Inherits existing models
│   └── ir_actions.py
├── views/                      # UI definitions
│   ├── my_model_views.xml
│   ├── res_partner_views.xml
│   ├── templates.xml           # QWeb templates
│   └── menu.xml                # Menu definitions
├── security/                   # Access control
│   ├── ir.model.access.csv
│   └── security.xml            # Groups and record rules
├── data/                       # Master data
│   ├── data.xml
│   └── demo.xml
├── wizards/                    # Transient models
│   ├── __init__.py
│   └── my_wizard.py
├── controllers/                # HTTP controllers
│   ├── __init__.py
│   └── main.py
├── static/                     # Static assets
│   ├── description/
│   │   ├── icon.png
│   │   └── index.html
│   └── src/
│       ├── js/
│       │   └── components/
│       ├── xml/
│       │   └── templates.xml
│       ├── css/
│       │   └── styles.css
│       └── img/
├── tests/                      # Test files
│   ├── __init__.py
│   ├── test_my_model.py
│   ├── test_wizard.py
│   └── test_controllers.py
├── migrations/                 # Migration scripts
│   └── 18.0.1.0.0/
│       ├── pre-migrate.py
│       └── post-migrate.py
├── reports/                    # Report definitions
│   ├── __init__.py
│   ├── report.xml
│   └── report_template.xml
├── i18n/                       # Translations
│   ├── es.po
│   ├── pt_BR.po
│   └── my_module.pot
├── doc/                        # Documentation
│   ├── index.rst
│   └── changelog.rst
└── README.md                   # Module README
```

### Naming Conventions

#### Module Names

```python
# GOOD: Clear, descriptive, prefixed
sale_advanced_discount
crm_lead_scoring
website_product_configurator

# BAD: Unclear, too generic
discount
leads
website_ext
```

#### Python Class Names

```python
# Models: CamelCase
class SaleOrder(models.Model):
    _name = 'sale.order'

class ProductTemplate(models.Model):
    _name = 'product.template'

# Wizards: CamelCase with Wizard suffix
class CreateInvoiceWizard(models.TransientModel):
    _name = 'create.invoice.wizard'

# Controllers: CamelCase with Controller suffix
class MyModuleController(http.Controller):
    pass
```

#### Field Names

```python
# GOOD: snake_case, descriptive
partner_id = fields.Many2one('res.partner')
invoice_date = fields.Date()
amount_total = fields.Monetary()
is_active = fields.Boolean()
payment_term_id = fields.Many2one('account.payment.term')

# BAD: Unclear, abbreviated
pid = fields.Many2one('res.partner')
dt = fields.Date()
amt = fields.Monetary()
active = fields.Boolean()  # 'active' is reserved, use 'is_active'
```

#### Method Names

```python
# GOOD: Descriptive verb + object
def action_confirm_order(self):
    pass

def _compute_total_amount(self):
    pass

def _check_date_validity(self):
    pass

# BAD: Unclear, too short
def confirm(self):  # What are we confirming?
    pass

def calc(self):  # Calculate what?
    pass
```

### Model Design Patterns

#### Single Responsibility Principle

```python
# GOOD: Each model has a single, clear purpose

class SaleOrder(models.Model):
    """Handles sales order operations"""
    _name = 'sale.order'
    # Only sale order related fields and methods

class SaleOrderLine(models.Model):
    """Handles individual order lines"""
    _name = 'sale.order.line'
    # Only line-specific fields and methods

class SaleOrderReport(models.Model):
    """Handles sale order reporting"""
    _name = 'sale.order.report'
    _auto = False  # SQL View
    # Only reporting-related fields


# BAD: Model doing too many things
class SaleOrder(models.Model):
    _name = 'sale.order'
    # Sales order fields
    # Shipping fields
    # Invoice fields
    # Report fields
    # Customer portal fields
    # Too much responsibility!
```

#### Composition Over Inheritance

```python
# GOOD: Use mixins for reusable functionality

class MailThread(models.AbstractModel):
    """Mixin for mail threading"""
    _name = 'mail.thread'
    _inherit = ['mail.thread']

class PortalMixin(models.AbstractModel):
    """Mixin for portal access"""
    _name = 'portal.mixin'

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    # Inherits functionality from multiple mixins


# BAD: Deep inheritance hierarchy
class BaseOrder(models.Model):
    pass

class AbstractOrder(models.Model):
    _inherit = 'base.order'

class GenericOrder(models.Model):
    _inherit = 'abstract.order'

class SaleOrder(models.Model):
    _inherit = 'generic.order'
    # Too deep, hard to maintain
```

---

## Code Organization

### __init__.py Structure

```python
# __init__.py (root)
from . import models
from . import wizards
from . import controllers
from . import reports

# Post-load hook for initialization
def post_init_hook(cr, registry):
    """
    Post-initialization hook
    Called after module installation
    """
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Initialization logic
    env['my.model']._setup_defaults()

# Uninstall hook
def uninstall_hook(cr, registry):
    """
    Uninstall hook
    Called before module uninstallation
    """
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Cleanup logic
    env['my.model']._cleanup_data()
```

### __manifest__.py Best Practices

```python
# __manifest__.py
{
    'name': 'My Module',
    'version': '18.0.1.0.0',  # Format: {Odoo version}.{major}.{minor}.{patch}
    'category': 'Sales',
    'summary': 'Short one-line description',
    'description': """
        Long description
        ================
        * Feature 1
        * Feature 2
        * Feature 3
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale',
        'stock',
    ],
    'data': [
        # Security always first
        'security/security.xml',
        'security/ir.model.access.csv',

        # Data files
        'data/data.xml',

        # Views
        'views/menu.xml',
        'views/my_model_views.xml',
        'views/res_partner_views.xml',

        # Wizards
        'wizards/my_wizard_views.xml',

        # Reports
        'reports/report.xml',
        'reports/report_template.xml',

        # Demo data (optional)
        'data/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'my_module/static/src/js/**/*',
            'my_module/static/src/xml/**/*',
            'my_module/static/src/css/**/*',
        ],
        'web.assets_frontend': [
            'my_module/static/src/js/frontend/**/*',
            'my_module/static/src/css/frontend/**/*',
        ],
    },
    'demo': [
        'data/demo.xml',
    ],
    'installable': True,
    'application': False,  # True only for main apps
    'auto_install': False,  # True only for bridge modules
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
```

---

## Python Best Practices

### Model Definition

```python
from odoo import api, fields, models, Command, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class SaleOrder(models.Model):
    """
    Sales Order Model

    Handles all sales order operations including:
    - Order creation and confirmation
    - Invoice generation
    - Delivery processing
    """
    _name = 'sale.order'
    _description = 'Sales Order'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'date_order desc, id desc'
    _check_company_auto = True

    # ----------------------------------------
    # Database fields
    # ----------------------------------------

    # Basic Information
    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        readonly=True,
        index='btree',
        default=lambda self: _('New'),
        tracking=True,
    )

    # Relational fields
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True,
        change_default=True,
        index='btree',
        tracking=True,
        domain="[('customer_rank', '>', 0)]",
        check_company=True,
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )

    # One2many fields
    order_line = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='order_id',
        string='Order Lines',
        copy=True,
    )

    # Selection fields
    state = fields.Selection(
        selection=[
            ('draft', 'Quotation'),
            ('sent', 'Quotation Sent'),
            ('sale', 'Sales Order'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        readonly=True,
        copy=False,
        index=True,
        tracking=True,
        default='draft',
    )

    # ----------------------------------------
    # Computed fields
    # ----------------------------------------

    amount_total = fields.Monetary(
        string='Total',
        compute='_compute_amounts',
        store=True,
        tracking=True,
    )

    invoice_count = fields.Integer(
        string='Invoice Count',
        compute='_compute_invoice_count',
    )

    # ----------------------------------------
    # Compute methods
    # ----------------------------------------

    @api.depends('order_line.price_subtotal')
    def _compute_amounts(self):
        """
        Compute order amounts
        Depends on order lines amounts
        """
        for order in self:
            order.amount_total = sum(order.order_line.mapped('price_subtotal'))

    def _compute_invoice_count(self):
        """Compute number of invoices"""
        for order in self:
            order.invoice_count = len(order.invoice_ids)

    # ----------------------------------------
    # Constraint methods
    # ----------------------------------------

    @api.constrains('date_order', 'commitment_date')
    def _check_dates(self):
        """Validate order dates"""
        for order in self:
            if order.commitment_date and order.date_order:
                if order.commitment_date < order.date_order:
                    raise ValidationError(_(
                        'Commitment date cannot be before order date.\n'
                        'Order date: %s\n'
                        'Commitment date: %s'
                    ) % (order.date_order, order.commitment_date))

    # ----------------------------------------
    # Onchange methods
    # ----------------------------------------

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """
        Update order values when partner changes
        """
        if not self.partner_id:
            return

        self.payment_term_id = self.partner_id.property_payment_term_id
        self.fiscal_position_id = self.env['account.fiscal.position'].get_fiscal_position(
            self.partner_id.id
        )

        if self.partner_id.user_id:
            self.user_id = self.partner_id.user_id

        return {
            'warning': {
                'title': _('Warning'),
                'message': _('Partner payment term updated.'),
            }
        } if self.payment_term_id else {}

    # ----------------------------------------
    # CRUD methods
    # ----------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        """
        Create sales orders with sequence
        """
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])

            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sale.order'
                ) or _('New')

        orders = super().create(vals_list)

        # Post-creation operations
        orders._create_default_lines()

        return orders

    def write(self, vals):
        """
        Update sales orders with validation
        """
        # Validate state transitions
        if 'state' in vals:
            self._validate_state_change(vals['state'])

        result = super().write(vals)

        # Post-write operations
        if 'partner_id' in vals:
            self._update_partner_data()

        return result

    def unlink(self):
        """
        Delete sales orders with validation
        """
        # Check if orders can be deleted
        if any(order.state not in ('draft', 'cancel') for order in self):
            raise UserError(_(
                'You cannot delete a confirmed sales order.\n'
                'You must first cancel it.'
            ))

        return super().unlink()

    # ----------------------------------------
    # Action methods
    # ----------------------------------------

    def action_confirm(self):
        """
        Confirm sales orders
        """
        self.ensure_one()

        if self.state != 'draft':
            raise UserError(_('Only draft orders can be confirmed.'))

        # Validation
        if not self.order_line:
            raise UserError(_('You cannot confirm an order without lines.'))

        # State change
        self.write({
            'state': 'sale',
            'date_order': fields.Datetime.now(),
        })

        # Create invoice if needed
        if self.payment_term_id.invoice_on_confirm:
            self._create_invoices()

        # Send confirmation email
        self.message_post_with_template(
            self.env.ref('sale.email_template_sale_confirmation').id
        )

        return True

    def action_cancel(self):
        """Cancel sales orders"""
        self.ensure_one()
        self.state = 'cancel'
        return True

    # ----------------------------------------
    # Business methods
    # ----------------------------------------

    def _create_invoices(self):
        """
        Create invoices for orders
        Returns: account.move recordset
        """
        if not self:
            return self.env['account.move']

        # Prepare invoice values
        invoice_vals_list = []
        for order in self:
            invoice_vals_list.append(order._prepare_invoice())

        # Create invoices
        invoices = self.env['account.move'].create(invoice_vals_list)

        # Link invoices to orders
        for order, invoice in zip(self, invoices):
            order.invoice_ids = [Command.link(invoice.id)]

        return invoices

    def _prepare_invoice(self):
        """
        Prepare invoice values
        Returns: dict
        """
        self.ensure_one()

        return {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.context_today(self),
            'company_id': self.company_id.id,
            'invoice_line_ids': [
                Command.create(line._prepare_invoice_line())
                for line in self.order_line
            ],
        }

    # ----------------------------------------
    # Helper methods (private)
    # ----------------------------------------

    def _validate_state_change(self, new_state):
        """Validate state transitions"""
        valid_transitions = {
            'draft': ['sent', 'sale', 'cancel'],
            'sent': ['draft', 'sale', 'cancel'],
            'sale': ['done', 'cancel'],
            'done': [],
            'cancel': ['draft'],
        }

        for order in self:
            if new_state not in valid_transitions.get(order.state, []):
                raise UserError(_(
                    'Invalid state transition from %s to %s'
                ) % (order.state, new_state))

    # ----------------------------------------
    # ORM override methods
    # ----------------------------------------

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        """
        Custom name search
        Search by name or partner name
        """
        domain = domain or []

        if name:
            domain = [
                '|',
                ('name', operator, name),
                ('partner_id.name', operator, name),
            ] + domain

        return self._search(domain, limit=limit, order=order)

    def name_get(self):
        """
        Custom display name
        Returns: list of (id, name) tuples
        """
        result = []
        for order in self:
            name = f"{order.name} - {order.partner_id.name}"
            result.append((order.id, name))
        return result
```

### Error Handling

```python
from odoo.exceptions import (
    AccessError,
    UserError,
    ValidationError,
    Warning as OdooWarning,
)

# GOOD: Specific, informative errors

def action_validate(self):
    """Validate order with proper error handling"""
    self.ensure_one()

    # User errors (user can fix)
    if not self.order_line:
        raise UserError(_(
            'Cannot validate order without lines.\n'
            'Please add at least one product.'
        ))

    # Validation errors (data validation)
    if self.amount_total <= 0:
        raise ValidationError(_(
            'Order total must be greater than zero.\n'
            'Current total: %s'
        ) % self.amount_total)

    # Access errors (permission issues)
    if not self.env.user.has_group('sales_team.group_sale_manager'):
        raise AccessError(_(
            'Only Sales Managers can validate orders above %s.\n'
            'Please contact your manager.'
        ) % self.company_id.currency_id.symbol)

    # Warnings (non-blocking)
    if self.partner_id.credit_limit and self.amount_total > self.partner_id.credit_limit:
        raise OdooWarning(_(
            'Warning: Customer credit limit exceeded.\n'
            'Credit limit: %s\n'
            'Order amount: %s'
        ) % (self.partner_id.credit_limit, self.amount_total))

    return True


# BAD: Generic, unhelpful errors
def action_validate(self):
    if not self.order_line:
        raise UserError('Error')  # What error?

    if self.amount_total <= 0:
        raise ValidationError('Invalid')  # Invalid what?
```

### Context Management

```python
# GOOD: Proper context usage

def process_with_context(self):
    """Process records with proper context"""

    # Bypass security for system operations
    self.sudo().write({'processed': True})

    # Change company context
    self.with_company(self.company_id).action_process()

    # Add context flags
    self.with_context(
        mail_create_nosubscribe=True,
        tracking_disable=True,
    ).write({'state': 'done'})

    # Batch operations without tracking
    self.env.cr.execute("UPDATE sale_order SET state='done' WHERE id IN %s", (tuple(self.ids),))
    self.invalidate_recordset()

# BAD: Context misuse
def process_with_context(self):
    # Don't use sudo unnecessarily
    self.sudo().sudo().sudo()  # Multiple sudo() calls

    # Don't modify env directly
    self.env.context['my_flag'] = True  # Context is immutable
```

---

## JavaScript Best Practices

### Component Structure

```javascript
/** @odoo-module **/

import { Component, useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

/**
 * My Custom Component
 *
 * Displays and manages custom data
 *
 * @extends Component
 */
export class MyCustomComponent extends Component {
    static template = "my_module.MyCustomComponent";
    static props = {
        // Required props
        recordId: { type: Number },
        model: { type: String },

        // Optional props
        title: { type: String, optional: true },
        readonly: { type: Boolean, optional: true },

        // Callbacks
        onSave: { type: Function, optional: true },
        onCancel: { type: Function, optional: true },
    };

    static defaultProps = {
        readonly: false,
        title: "My Component",
    };

    setup() {
        // Services
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.dialog = useService("dialog");
        this.action = useService("action");

        // State management
        this.state = useState({
            data: null,
            loading: false,
            error: null,
        });

        // Refs
        this.inputRef = useRef("input");
        this.containerRef = useRef("container");

        // Lifecycle
        onMounted(() => {
            this._loadData();
        });

        onWillUnmount(() => {
            this._cleanup();
        });
    }

    // ----------------------------------------
    // Lifecycle methods
    // ----------------------------------------

    async _loadData() {
        this.state.loading = true;
        this.state.error = null;

        try {
            const data = await this.orm.read(
                this.props.model,
                [this.props.recordId],
                ["name", "value", "description"]
            );
            this.state.data = data[0];
        } catch (error) {
            this.state.error = error.message;
            this.notification.add(error.message, { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }

    _cleanup() {
        // Cleanup resources
        this.state.data = null;
    }

    // ----------------------------------------
    // Event handlers
    // ----------------------------------------

    async onSaveClick() {
        if (this.props.readonly) {
            return;
        }

        this.state.loading = true;

        try {
            await this.orm.write(
                this.props.model,
                [this.props.recordId],
                {
                    name: this.state.data.name,
                    value: this.state.data.value,
                }
            );

            this.notification.add("Saved successfully", { type: "success" });

            if (this.props.onSave) {
                this.props.onSave();
            }
        } catch (error) {
            this.notification.add(error.message, { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }

    onCancelClick() {
        if (this.props.onCancel) {
            this.props.onCancel();
        }
    }

    onInputChange(field, value) {
        this.state.data[field] = value;
    }

    // ----------------------------------------
    // Helper methods
    // ----------------------------------------

    get isValid() {
        return this.state.data && this.state.data.name && this.state.data.value;
    }

    get canSave() {
        return !this.props.readonly && this.isValid && !this.state.loading;
    }
}

// Register component
registry.category("my_components").add("MyCustomComponent", MyCustomComponent);
```

### Template Best Practices

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">

    <!-- Component template -->
    <t t-name="my_module.MyCustomComponent">
        <div class="my-custom-component" t-ref="container">

            <!-- Loading state -->
            <div t-if="state.loading" class="text-center p-4">
                <i class="fa fa-spinner fa-spin fa-2x"/>
                <p class="mt-2">Loading...</p>
            </div>

            <!-- Error state -->
            <div t-elif="state.error" class="alert alert-danger">
                <i class="fa fa-exclamation-triangle"/>
                <t t-esc="state.error"/>
            </div>

            <!-- Content -->
            <div t-else-if="state.data" class="card">
                <div class="card-header">
                    <h3 t-esc="props.title"/>
                </div>

                <div class="card-body">
                    <!-- Input field -->
                    <div class="mb-3">
                        <label class="form-label">Name</label>
                        <input
                            type="text"
                            class="form-control"
                            t-ref="input"
                            t-att-disabled="props.readonly"
                            t-model="state.data.name"
                            t-on-change="() => this.onInputChange('name', $event.target.value)"
                        />
                    </div>

                    <!-- Number field -->
                    <div class="mb-3">
                        <label class="form-label">Value</label>
                        <input
                            type="number"
                            class="form-control"
                            t-att-disabled="props.readonly"
                            t-model="state.data.value"
                            t-on-change="() => this.onInputChange('value', parseFloat($event.target.value))"
                        />
                    </div>

                    <!-- Conditional content -->
                    <div t-if="state.data.description" class="mb-3">
                        <label class="form-label">Description</label>
                        <p t-esc="state.data.description"/>
                    </div>
                </div>

                <!-- Actions -->
                <div class="card-footer">
                    <button
                        t-if="!props.readonly"
                        class="btn btn-primary"
                        t-att-disabled="!canSave"
                        t-on-click="onSaveClick"
                    >
                        <i class="fa fa-save"/> Save
                    </button>

                    <button
                        class="btn btn-secondary ms-2"
                        t-on-click="onCancelClick"
                    >
                        <i class="fa fa-times"/> Cancel
                    </button>
                </div>
            </div>

        </div>
    </t>

</templates>
```

---

## XML/View Best Practices

### Form View Structure

```xml
<record id="view_sale_order_form" model="ir.ui.view">
    <field name="name">sale.order.form</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <form string="Sales Order">

            <!-- Status bar -->
            <header>
                <!-- Primary action -->
                <button name="action_confirm" string="Confirm"
                        type="object"
                        invisible="state != 'draft'"
                        class="btn-primary"/>

                <!-- Secondary actions -->
                <button name="action_send" string="Send by Email"
                        type="object"
                        invisible="state not in ('draft', 'sent')"
                        class="btn-secondary"/>

                <button name="action_cancel" string="Cancel"
                        type="object"
                        invisible="state in ('done', 'cancel')"
                        class="btn-secondary"/>

                <!-- Status bar -->
                <field name="state" widget="statusbar"
                       statusbar_visible="draft,sent,sale,done"/>
            </header>

            <sheet>
                <!-- Smart buttons -->
                <div class="oe_button_box" name="button_box">
                    <button name="action_view_invoice"
                            type="object"
                            class="oe_stat_button"
                            icon="fa-pencil-square-o"
                            invisible="invoice_count == 0">
                        <field name="invoice_count" widget="statinfo"
                               string="Invoices"/>
                    </button>

                    <button name="action_view_delivery"
                            type="object"
                            class="oe_stat_button"
                            icon="fa-truck"
                            invisible="delivery_count == 0">
                        <field name="delivery_count" widget="statinfo"
                               string="Deliveries"/>
                    </button>
                </div>

                <!-- Title -->
                <div class="oe_title">
                    <h1>
                        <field name="name" readonly="1"/>
                    </h1>
                </div>

                <!-- Main groups -->
                <group>
                    <group name="customer_info">
                        <field name="partner_id"
                               widget="res_partner_many2one"
                               context="{'show_address': 1, 'show_vat': True}"/>
                        <field name="partner_invoice_id"
                               context="{'show_address': 1}"
                               groups="sale.group_delivery_invoice_address"/>
                        <field name="partner_shipping_id"
                               context="{'show_address': 1}"
                               groups="sale.group_delivery_invoice_address"/>
                    </group>

                    <group name="sale_info">
                        <field name="date_order"
                               widget="daterange"
                               options="{'end_date_field': 'validity_date'}"/>
                        <field name="validity_date"/>
                        <field name="pricelist_id"
                               groups="product.group_sale_pricelist"/>
                        <field name="payment_term_id"/>
                    </group>
                </group>

                <!-- Notebook -->
                <notebook>
                    <!-- Order Lines -->
                    <page string="Order Lines" name="order_lines">
                        <field name="order_line"
                               widget="section_and_note_one2many"
                               mode="tree">
                            <tree editable="bottom"
                                  decoration-info="state == 'draft'">
                                <control>
                                    <create string="Add a product"/>
                                    <create string="Add a section"
                                            context="{'default_display_type': 'line_section'}"/>
                                    <create string="Add a note"
                                            context="{'default_display_type': 'line_note'}"/>
                                </control>

                                <field name="display_type" column_invisible="1"/>
                                <field name="sequence" widget="handle"/>

                                <field name="product_id"
                                       widget="many2one_barcode"
                                       context="{'partner_id': parent.partner_id}"/>

                                <field name="name" widget="section_and_note_text"/>
                                <field name="product_uom_qty"/>
                                <field name="product_uom"
                                       groups="uom.group_uom"
                                       optional="show"/>
                                <field name="price_unit" widget="monetary"/>
                                <field name="discount" widget="percentage"
                                       groups="product.group_discount_per_so_line"
                                       optional="show"/>
                                <field name="tax_id" widget="many2many_tags"
                                       optional="show"/>
                                <field name="price_subtotal" widget="monetary"
                                       sum="Total"/>
                            </tree>
                        </field>

                        <!-- Totals -->
                        <group class="oe_subtotal_footer oe_right">
                            <field name="amount_untaxed" widget="monetary"/>
                            <field name="amount_tax" widget="monetary"/>
                            <field name="amount_total" widget="monetary"
                                   class="oe_subtotal_footer_separator"/>
                        </group>
                    </page>

                    <!-- Other Information -->
                    <page string="Other Information" name="other_info">
                        <group>
                            <group name="sales_person">
                                <field name="user_id"
                                       widget="many2one_avatar_user"/>
                                <field name="team_id"
                                       widget="selection"/>
                            </group>

                            <group name="logistics">
                                <field name="warehouse_id"
                                       groups="stock.group_stock_multi_warehouses"/>
                                <field name="picking_policy"/>
                            </group>
                        </group>

                        <group string="Tracking">
                            <field name="client_order_ref"/>
                            <field name="origin"/>
                            <field name="reference"/>
                        </group>
                    </page>

                    <!-- Notes -->
                    <page string="Terms and Conditions" name="terms">
                        <field name="note" placeholder="Define your terms and conditions..."/>
                    </page>
                </notebook>

            </sheet>

            <!-- Chatter -->
            <chatter/>

        </form>
    </field>
</record>
```

---

## Security Best Practices

### Access Rights Strategy

```csv
# security/ir.model.access.csv

id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
# User access (read and create own)
access_sale_order_user,Access Sale Order User,model_sale_order,sales_team.group_sale_salesman,1,1,1,0

# Manager access (full access)
access_sale_order_manager,Access Sale Order Manager,model_sale_order,sales_team.group_sale_manager,1,1,1,1

# Multi-company access
access_sale_order_company,Access Sale Order Company,model_sale_order,base.group_multi_company,1,0,0,0

# Portal access (read only own)
access_sale_order_portal,Access Sale Order Portal,model_sale_order,base.group_portal,1,0,0,0

# Public access (no access by default)
# Don't give public access unless absolutely necessary
```

### Record Rules Best Practices

```xml
<!-- security/security.xml -->
<odoo>
    <data noupdate="1">

        <!-- User can see their own records and team records -->
        <record id="sale_order_rule_user" model="ir.rule">
            <field name="name">Sale Order: User Own and Team</field>
            <field name="model_id" ref="model_sale_order"/>
            <field name="domain_force">[
                '|',
                    ('user_id', '=', user.id),
                    ('team_id.member_ids', 'in', user.id)
            ]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="False"/>
        </record>

        <!-- Manager sees all -->
        <record id="sale_order_rule_manager" model="ir.rule">
            <field name="name">Sale Order: Manager All Access</field>
            <field name="model_id" ref="model_sale_order"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_manager'))]"/>
        </record>

        <!-- Multi-company rule (global) -->
        <record id="sale_order_rule_company" model="ir.rule">
            <field name="name">Sale Order: Multi-Company</field>
            <field name="model_id" ref="model_sale_order"/>
            <field name="global" eval="True"/>
            <field name="domain_force">[
                '|',
                    ('company_id', '=', False),
                    ('company_id', 'in', company_ids)
            ]</field>
        </record>

        <!-- Portal user sees only their orders -->
        <record id="sale_order_rule_portal" model="ir.rule">
            <field name="name">Sale Order: Portal User Own</field>
            <field name="model_id" ref="model_sale_order"/>
            <field name="domain_force">[('partner_id', 'child_of', user.partner_id.commercial_partner_id.id)]</field>
            <field name="groups" eval="[(4, ref('base.group_portal'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
        </record>

    </data>
</odoo>
```

### Field-Level Security

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    # Sensitive field - restricted access
    margin = fields.Float(
        string='Margin',
        compute='_compute_margin',
        store=True,
        groups='sales_team.group_sale_manager',  # Only managers can see
    )

    # Internal notes - not visible to portal users
    internal_notes = fields.Text(
        string='Internal Notes',
        groups='base.group_user',  # Only internal users
    )

    # Public field - everyone can see
    name = fields.Char(
        string='Order Reference',
        required=True,
    )
```

---

## Performance Optimization

### Database Optimization

```python
# GOOD: Efficient database queries

class SaleOrder(models.Model):
    _name = 'sale.order'

    def process_orders(self):
        """Process orders efficiently"""

        # 1. Use search_read for list views
        orders_data = self.search_read(
            [('state', '=', 'draft')],
            ['name', 'partner_id', 'amount_total'],
            limit=100,
        )

        # 2. Prefetch related fields
        orders = self.search([('state', '=', 'draft')])
        orders.mapped('partner_id.name')  # Prefetch all partners at once

        # 3. Batch processing
        for batch in orders.batched(batch_size=100):
            batch.action_confirm()

        # 4. Use SQL for aggregations
        self.env.cr.execute("""
            SELECT partner_id, SUM(amount_total)
            FROM sale_order
            WHERE state = 'sale'
            GROUP BY partner_id
        """)
        results = self.env.cr.dictfetchall()

        # 5. Use computed fields with store=True
        # Instead of calculating on-the-fly

        return True


# BAD: Inefficient queries

def process_orders_bad(self):
    """Inefficient processing"""

    # 1. Don't iterate and read each record
    order_ids = self.search([('state', '=', 'draft')])
    for order in order_ids:
        # Each iteration = 1 query
        name = order.name
        partner = order.partner_id.name
        total = order.amount_total

    # 2. Don't make unnecessary queries
    for order in order_ids:
        # Query inside loop = N queries
        lines = self.env['sale.order.line'].search([
            ('order_id', '=', order.id)
        ])

    # 3. Don't compute every time
    for order in order_ids:
        # Calculate on each call
        total = sum(line.price_subtotal for line in order.order_line)
```

### Caching Strategies

```python
from functools import lru_cache
from odoo import tools

class SaleOrder(models.Model):
    _name = 'sale.order'

    @tools.ormcache('self.id')
    def _get_cached_data(self):
        """
        Cache method results
        Cache is cleared when record is modified
        """
        return self._compute_expensive_data()

    def _compute_expensive_data(self):
        """Expensive computation"""
        # Complex calculations
        return result
```

### Index Management

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    # Add indexes to frequently searched fields
    partner_id = fields.Many2one('res.partner', index=True)
    state = fields.Selection([...], index=True)
    date_order = fields.Datetime(index=True)

    # Composite index for complex queries
    def init(self):
        """Create database indexes"""
        self.env.cr.execute("""
            CREATE INDEX IF NOT EXISTS sale_order_partner_state_idx
            ON sale_order (partner_id, state)
            WHERE state != 'cancel'
        """)

        # Partial index for active records
        self.env.cr.execute("""
            CREATE INDEX IF NOT EXISTS sale_order_active_idx
            ON sale_order (date_order DESC)
            WHERE state IN ('draft', 'sent', 'sale')
        """)
```

---

## Testing Standards

### Unit Test Example

```python
# tests/test_sale_order.py

from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError, ValidationError

@tagged('post_install', '-at_install')
class TestSaleOrder(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Setup test data
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'test@example.com',
        })

        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
        })

    def test_order_creation(self):
        """Test order creation with sequence"""
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })

        self.assertTrue(order.name)
        self.assertNotEqual(order.name, '/')
        self.assertEqual(order.state, 'draft')

    def test_order_confirmation(self):
        """Test order confirmation process"""
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
            })],
        })

        order.action_confirm()

        self.assertEqual(order.state, 'sale')
        self.assertTrue(order.date_order)

    def test_order_validation(self):
        """Test order validation rules"""
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })

        # Should raise error for order without lines
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_amount_computation(self):
        """Test amount computation"""
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 2,
                'price_unit': 100.0,
            })],
        })

        self.assertEqual(order.amount_total, 200.0)

    def test_batch_processing(self):
        """Test batch processing performance"""
        # Create multiple orders
        orders = self.env['sale.order'].create([
            {
                'partner_id': self.partner.id,
                'order_line': [(0, 0, {
                    'product_id': self.product.id,
                    'product_uom_qty': 1,
                })],
            }
            for _ in range(100)
        ])

        # Batch confirm
        orders.action_confirm()

        self.assertTrue(all(o.state == 'sale' for o in orders))
```

---

## Code Review Checklist

### Pre-Commit Checklist

- [ ] Code follows PEP 8 style guide
- [ ] All methods have docstrings
- [ ] No debug print statements or commented code
- [ ] All strings are translatable with _()
- [ ] Proper error handling
- [ ] No hardcoded values (use parameters)
- [ ] Security rules defined
- [ ] Tests added/updated
- [ ] Migration scripts (if needed)
- [ ] Documentation updated

### Security Review

- [ ] No SQL injection vulnerabilities
- [ ] Proper access rights defined
- [ ] Record rules implemented
- [ ] Field-level security checked
- [ ] CSRF protection for controllers
- [ ] Input validation implemented
- [ ] No sensitive data in logs

### Performance Review

- [ ] Efficient database queries
- [ ] Proper indexes defined
- [ ] No N+1 query problems
- [ ] Batch processing used
- [ ] Computed fields properly stored
- [ ] Cache strategies implemented

---

**Document Version**: 1.0
**Last Updated**: 2025-10-16
**Odoo Version**: 18.0
