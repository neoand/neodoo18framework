# Odoo 18 Migration Guide

## Complete Migration Guide from Odoo 17 to 18

This comprehensive guide covers all aspects of migrating your custom modules from Odoo 17 to Odoo 18, including breaking changes, step-by-step procedures, and common issues.

---

## Table of Contents

1. [Breaking Changes Overview](#breaking-changes-overview)
2. [Migration Checklist](#migration-checklist)
3. [Python Changes](#python-changes)
4. [JavaScript Changes](#javascript-changes)
5. [XML/Views Changes](#xmlviews-changes)
6. [Database Migration](#database-migration)
7. [Security Changes](#security-changes)
8. [Migration Scripts](#migration-scripts)
9. [Testing After Migration](#testing-after-migration)
10. [Common Issues and Solutions](#common-issues-and-solutions)

---

## Breaking Changes Overview

### Critical Breaking Changes

#### 1. Python Version Requirement
**Change**: Minimum Python version is now 3.10 (was 3.8 in Odoo 17)

**Migration Impact**: HIGH
- Update your deployment environment
- Review Python 3.10 specific features and deprecated syntax
- Update CI/CD pipelines

**Before (Odoo 17)**:
```python
# Python 3.8+ syntax
from typing import Optional, Union

def get_value(self) -> Optional[Union[str, int]]:
    return self.value if self.value else None
```

**After (Odoo 18)**:
```python
# Python 3.10+ syntax with new features
def get_value(self) -> str | int | None:
    match self.value:
        case str() | int():
            return self.value
        case _:
            return None
```

---

#### 2. ORM Changes

##### a) Command System Refactoring

**Change**: The x2many command system has been refactored with new helper methods

**Migration Impact**: MEDIUM

**Before (Odoo 17)**:
```python
# Old command syntax (still works but deprecated)
self.line_ids = [(0, 0, {
    'product_id': product.id,
    'quantity': 5,
})]

# Update
self.line_ids = [(1, line.id, {'quantity': 10})]

# Delete
self.line_ids = [(2, line.id, 0)]

# Unlink
self.line_ids = [(3, line.id, 0)]

# Clear all
self.line_ids = [(5, 0, 0)]

# Replace
self.line_ids = [(6, 0, [line1.id, line2.id])]
```

**After (Odoo 18)**:
```python
# New helper methods (recommended)
from odoo.models import Command

# Create
self.line_ids = [Command.create({
    'product_id': product.id,
    'quantity': 5,
})]

# Update
self.line_ids = [Command.update(line.id, {'quantity': 10})]

# Delete (remove and delete the record)
self.line_ids = [Command.delete(line.id)]

# Unlink (remove but don't delete the record)
self.line_ids = [Command.unlink(line.id)]

# Clear all
self.line_ids = [Command.clear()]

# Set (replace all)
self.line_ids = [Command.set([line1.id, line2.id])]

# Link (add existing records)
self.line_ids = [Command.link(line.id)]

# Multiple operations
self.line_ids = [
    Command.create({'product_id': p1.id}),
    Command.update(line1.id, {'quantity': 10}),
    Command.delete(line2.id),
]
```

##### b) Search Method Changes

**Change**: Enhanced search with better performance and new parameters

**Before (Odoo 17)**:
```python
# Basic search
records = self.env['res.partner'].search([
    ('customer_rank', '>', 0)
], limit=10, offset=0, order='name')

# Count
count = self.env['res.partner'].search_count([
    ('customer_rank', '>', 0)
])
```

**After (Odoo 18)**:
```python
# New search with performance hints
records = self.env['res.partner'].search([
    ('customer_rank', '>', 0)
], limit=10, offset=0, order='name', load='_classic_write')

# Search with prefetch optimization
records = self.env['res.partner'].with_prefetch().search([
    ('customer_rank', '>', 0)
])

# Batch search (new in 18)
batches = self.env['res.partner'].search([
    ('customer_rank', '>', 0)
]).batched(batch_size=100)

for batch in batches:
    # Process batch
    batch.write({'processed': True})
```

---

#### 3. Field Definition Changes

**Change**: New field attributes and deprecated options

**Migration Impact**: MEDIUM

**Before (Odoo 17)**:
```python
class MyModel(models.Model):
    _name = 'my.model'

    # Old style
    name = fields.Char(string='Name', required=True, index=True)

    # Old selection
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], default='draft')

    # Old compute
    total = fields.Float(compute='_compute_total', store=True)

    @api.depends('line_ids.amount')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.line_ids.mapped('amount'))
```

**After (Odoo 18)**:
```python
class MyModel(models.Model):
    _name = 'my.model'

    # New style with index parameter object
    name = fields.Char(
        string='Name',
        required=True,
        index='btree',  # Can be: 'btree', 'hash', 'gin', 'gist'
        tracking=True,  # Enhanced tracking
    )

    # Selection with selection_add support
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
        ],
        default='draft',
        required=True,
        tracking=True,
    )

    # Compute with better cache control
    total = fields.Float(
        compute='_compute_total',
        store=True,
        recursive=True,  # New: handle recursive dependencies
        precompute=True,  # New: compute on create
    )

    @api.depends('line_ids.amount')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.line_ids.mapped('amount'))
```

---

#### 4. JavaScript/OWL Changes

**Change**: OWL framework updated to version 2.0 with significant API changes

**Migration Impact**: HIGH

**Before (Odoo 17 - OWL 1.x)**:
```javascript
/** @odoo-module **/

import { Component } from "@web/core/component";
import { useState } from "@odoo/owl";

export class MyComponent extends Component {
    setup() {
        this.state = useState({
            counter: 0,
            name: '',
        });
    }

    increment() {
        this.state.counter++;
    }
}

MyComponent.template = 'my_module.MyComponent';
```

**After (Odoo 18 - OWL 2.0)**:
```javascript
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class MyComponent extends Component {
    static template = "my_module.MyComponent";
    static props = {
        title: { type: String, optional: true },
        count: { type: Number, optional: false },
    };

    setup() {
        this.state = useState({
            counter: this.props.count || 0,
            name: '',
        });
    }

    increment() {
        this.state.counter++;
    }
}
```

**Key Changes**:
- Template is now a static property
- Props must be explicitly defined with static props
- Better type checking and validation

---

#### 5. View Architecture Changes

**Change**: New view attributes and deprecated elements

**Before (Odoo 17)**:
```xml
<record id="view_my_form" model="ir.ui.view">
    <field name="name">my.model.form</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <form string="My Model">
            <header>
                <button name="action_confirm" string="Confirm"
                        type="object" states="draft"/>
            </header>
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="partner_id"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

**After (Odoo 18)**:
```xml
<record id="view_my_form" model="ir.ui.view">
    <field name="name">my.model.form</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <form string="My Model">
            <header>
                <button name="action_confirm" string="Confirm"
                        type="object"
                        invisible="state != 'draft'"
                        class="btn-primary"/>
            </header>
            <sheet>
                <group>
                    <field name="name" placeholder="Enter name..."/>
                    <field name="partner_id"
                           widget="res_partner_many2one"
                           context="{'show_vat': True}"/>
                </group>
            </sheet>
            <chatter/>
        </form>
    </field>
</record>
```

**Key Changes**:
- `states` attribute is deprecated, use `invisible` with domain
- New widget variants with better UX
- Enhanced placeholder support
- Simplified chatter inclusion

---

## Migration Checklist

### Pre-Migration Phase

- [ ] **Backup Everything**
  - Full database dump
  - Filestore backup
  - Custom modules repository backup
  - Configuration files

- [ ] **Environment Preparation**
  - [ ] Install Python 3.10+
  - [ ] Update system dependencies
  - [ ] Setup test environment
  - [ ] Clone Odoo 18 source

- [ ] **Module Analysis**
  - [ ] List all custom modules
  - [ ] Identify dependencies
  - [ ] Review breaking changes impact
  - [ ] Create migration plan per module

- [ ] **Code Review**
  - [ ] Check Python syntax compatibility
  - [ ] Review deprecated API usage
  - [ ] Identify JavaScript components
  - [ ] Review XML view definitions

### Migration Phase

- [ ] **Update Module Structure**
  - [ ] Update `__manifest__.py` version to '18.0.1.0.0'
  - [ ] Review and update dependencies
  - [ ] Update Python imports
  - [ ] Update JavaScript imports

- [ ] **Python Code Migration**
  - [ ] Replace old command syntax with Command class
  - [ ] Update field definitions
  - [ ] Review and update @api decorators
  - [ ] Update ORM method calls
  - [ ] Fix deprecated method usage

- [ ] **JavaScript Migration**
  - [ ] Convert to OWL 2.0 syntax
  - [ ] Add static props definitions
  - [ ] Update template references
  - [ ] Review event handling
  - [ ] Update service usage

- [ ] **XML/View Migration**
  - [ ] Replace `states` with `invisible`
  - [ ] Update widget names
  - [ ] Review and update domains
  - [ ] Update action definitions
  - [ ] Fix deprecated view attributes

- [ ] **Security Migration**
  - [ ] Review access rights
  - [ ] Update record rules
  - [ ] Check security group changes
  - [ ] Validate field-level security

### Post-Migration Phase

- [ ] **Testing**
  - [ ] Run unit tests
  - [ ] Execute integration tests
  - [ ] Perform UI testing
  - [ ] Load testing
  - [ ] Security testing

- [ ] **Data Migration**
  - [ ] Run database migration scripts
  - [ ] Validate data integrity
  - [ ] Check computed field values
  - [ ] Verify related records

- [ ] **Documentation**
  - [ ] Update technical documentation
  - [ ] Update user manuals
  - [ ] Document migration issues
  - [ ] Create rollback plan

- [ ] **Deployment**
  - [ ] Staging deployment
  - [ ] Performance validation
  - [ ] User acceptance testing
  - [ ] Production deployment

---

## Python Changes

### API Decorator Changes

**Before (Odoo 17)**:
```python
from odoo import api, fields, models

class MyModel(models.Model):
    _name = 'my.model'

    # Old depends
    @api.depends('field1', 'field2')
    def _compute_something(self):
        for record in self:
            record.computed_field = record.field1 + record.field2

    # Old constrains
    @api.constrains('field1')
    def _check_field1(self):
        for record in self:
            if record.field1 < 0:
                raise ValidationError("Field1 must be positive")

    # Old onchange
    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.email = self.partner_id.email
```

**After (Odoo 18)**:
```python
from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError

class MyModel(models.Model):
    _name = 'my.model'

    # Enhanced depends with dot notation support
    @api.depends('field1', 'field2', 'line_ids.amount')
    def _compute_something(self):
        for record in self:
            record.computed_field = (
                record.field1 +
                record.field2 +
                sum(record.line_ids.mapped('amount'))
            )

    # Enhanced constrains with better error messages
    @api.constrains('field1', 'field2')
    def _check_fields(self):
        for record in self:
            if record.field1 < 0:
                raise ValidationError(
                    "Field1 must be positive. Current value: %s" % record.field1
                )
            if record.field2 and record.field2 < record.field1:
                raise ValidationError(
                    "Field2 must be greater than Field1"
                )

    # Onchange with return value for warnings
    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.email = self.partner_id.email
            if not self.partner_id.email:
                return {
                    'warning': {
                        'title': 'No Email',
                        'message': 'The selected partner has no email address.'
                    }
                }
```

### Model Method Changes

**Before (Odoo 17)**:
```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        # Custom logic before create
        if 'name' not in vals or vals['name'] == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order')
        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        # Custom logic before write
        if 'state' in vals:
            self._log_state_change(vals['state'])
        return super(SaleOrder, self).write(vals)

    def unlink(self):
        # Check before delete
        if any(order.state != 'draft' for order in self):
            raise UserError("Cannot delete non-draft orders")
        return super(SaleOrder, self).unlink()
```

**After (Odoo 18)**:
```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        # Batch create support
        for vals in vals_list:
            if 'name' not in vals or vals['name'] == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order')

        orders = super().create(vals_list)

        # Post-create logic on recordset
        orders._send_creation_notification()

        return orders

    def write(self, vals):
        # Better state tracking
        if 'state' in vals:
            # Track previous states
            state_changes = {
                order.id: {'old': order.state, 'new': vals['state']}
                for order in self
            }

        result = super().write(vals)

        if 'state' in vals:
            self._log_state_changes(state_changes)

        return result

    def unlink(self):
        # Enhanced validation
        non_draft = self.filtered(lambda o: o.state != 'draft')
        if non_draft:
            raise UserError(
                "Cannot delete orders in state: %s" %
                ', '.join(non_draft.mapped('state'))
            )

        # Archive instead of delete for audit trail
        if self.env.context.get('soft_delete'):
            return self.write({'active': False})

        return super().unlink()
```

---

## JavaScript Changes

### Component Migration

**Before (Odoo 17)**:
```javascript
/** @odoo-module **/

import { Component } from "@web/core/component";
import { useState, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class MyWidget extends Component {
    setup() {
        this.state = useState({
            value: this.props.value || 0,
        });
        this.inputRef = useRef("input");
    }

    onInputChange(ev) {
        this.state.value = parseFloat(ev.target.value);
        this.props.onChange(this.state.value);
    }
}

MyWidget.template = "my_module.MyWidget";

registry.category("fields").add("my_widget", MyWidget);
```

**After (Odoo 18)**:
```javascript
/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class MyWidget extends Component {
    static template = "my_module.MyWidget";
    static props = {
        ...standardFieldProps,
        value: { type: Number, optional: true },
        onChange: { type: Function, optional: true },
    };

    setup() {
        this.state = useState({
            value: this.props.value || 0,
        });
        this.inputRef = useRef("input");
    }

    onInputChange(ev) {
        const newValue = parseFloat(ev.target.value);
        this.state.value = newValue;

        // Better event handling
        if (this.props.onChange) {
            this.props.onChange(newValue);
        }

        // Update record value for field widgets
        if (this.props.record) {
            this.props.record.update({ [this.props.name]: newValue });
        }
    }
}

registry.category("fields").add("my_widget", MyWidget);
```

### Service Usage

**Before (Odoo 17)**:
```javascript
/** @odoo-module **/

import { Component } from "@web/core/component";
import { useService } from "@web/core/utils/hooks";

export class MyComponent extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
    }

    async loadData() {
        try {
            const result = await this.rpc({
                model: 'my.model',
                method: 'search_read',
                args: [[]],
            });
            this.notification.add("Data loaded", { type: 'success' });
        } catch (error) {
            this.notification.add(error.message, { type: 'danger' });
        }
    }
}
```

**After (Odoo 18)**:
```javascript
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class MyComponent extends Component {
    static template = "my_module.MyComponent";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");
    }

    async loadData() {
        try {
            // New ORM service (preferred over direct RPC)
            const records = await this.orm.searchRead(
                "my.model",
                [],  // domain
                ["name", "value"],  // fields
                { limit: 100, order: "name" }
            );

            this.notification.add("Data loaded successfully", {
                type: 'success',
                sticky: false,
            });

            return records;
        } catch (error) {
            this.notification.add(error.message, {
                type: 'danger',
                sticky: true,
            });
            throw error;
        }
    }

    async createRecord(values) {
        const recordId = await this.orm.create("my.model", [values]);
        return recordId[0];
    }

    async updateRecord(recordId, values) {
        await this.orm.write("my.model", [recordId], values);
    }

    async deleteRecord(recordId) {
        await this.orm.unlink("my.model", [recordId]);
    }

    openRecord(recordId) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'my.model',
            res_id: recordId,
            views: [[false, 'form']],
            target: 'current',
        });
    }
}
```

---

## XML/Views Changes

### Form View Migration

**Before (Odoo 17)**:
```xml
<record id="view_order_form" model="ir.ui.view">
    <field name="name">sale.order.form</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <form string="Sale Order">
            <header>
                <button name="action_confirm" string="Confirm"
                        type="object" states="draft"
                        class="oe_highlight"/>
                <button name="action_cancel" string="Cancel"
                        type="object" states="sale"/>
                <field name="state" widget="statusbar"/>
            </header>
            <sheet>
                <group>
                    <group>
                        <field name="partner_id"/>
                        <field name="date_order"/>
                    </group>
                    <group>
                        <field name="user_id"/>
                        <field name="company_id" groups="base.group_multi_company"/>
                    </group>
                </group>
                <notebook>
                    <page string="Order Lines">
                        <field name="order_line">
                            <tree editable="bottom">
                                <field name="product_id"/>
                                <field name="product_uom_qty"/>
                                <field name="price_unit"/>
                                <field name="price_subtotal"/>
                            </tree>
                        </field>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```

**After (Odoo 18)**:
```xml
<record id="view_order_form" model="ir.ui.view">
    <field name="name">sale.order.form</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <form string="Sale Order">
            <header>
                <!-- Use invisible instead of states -->
                <button name="action_confirm" string="Confirm"
                        type="object"
                        invisible="state != 'draft'"
                        class="btn-primary"/>
                <button name="action_cancel" string="Cancel"
                        type="object"
                        invisible="state not in ('draft', 'sent', 'sale')"
                        class="btn-secondary"/>
                <field name="state" widget="statusbar"
                       statusbar_visible="draft,sent,sale,done"/>
            </header>
            <sheet>
                <!-- Enhanced widget attribute -->
                <div class="oe_button_box" name="button_box">
                    <button name="action_view_invoice"
                            type="object"
                            class="oe_stat_button"
                            icon="fa-pencil-square-o"
                            invisible="invoice_count == 0">
                        <field name="invoice_count" widget="statinfo"
                               string="Invoices"/>
                    </button>
                </div>

                <group>
                    <group>
                        <!-- Enhanced widget with context -->
                        <field name="partner_id"
                               widget="res_partner_many2one"
                               context="{'show_address': 1, 'show_vat': True}"/>
                        <field name="date_order"
                               widget="daterange"
                               options="{'end_date_field': 'date_deadline'}"/>
                    </group>
                    <group>
                        <field name="user_id"
                               widget="many2one_avatar_user"/>
                        <field name="company_id"
                               groups="base.group_multi_company"
                               widget="selection"/>
                    </group>
                </group>

                <notebook>
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
                                <field name="product_id"
                                       widget="many2one_barcode"/>
                                <field name="product_uom_qty"
                                       string="Quantity"/>
                                <field name="price_unit"
                                       widget="monetary"/>
                                <field name="discount"
                                       widget="percentage"
                                       optional="show"/>
                                <field name="price_subtotal"
                                       widget="monetary"/>
                            </tree>
                        </field>
                    </page>

                    <page string="Other Information" name="other_info">
                        <group>
                            <group string="Sales">
                                <field name="payment_term_id"/>
                                <field name="fiscal_position_id"/>
                            </group>
                            <group string="Delivery">
                                <field name="warehouse_id"/>
                                <field name="picking_policy"/>
                            </group>
                        </group>
                    </page>
                </notebook>
            </sheet>

            <!-- Simplified chatter -->
            <chatter/>
        </form>
    </field>
</record>
```

### Tree View Migration

**Before (Odoo 17)**:
```xml
<record id="view_order_tree" model="ir.ui.view">
    <field name="name">sale.order.tree</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <tree string="Sales Orders" colors="blue:state=='draft';green:state=='sale'">
            <field name="name"/>
            <field name="partner_id"/>
            <field name="date_order"/>
            <field name="amount_total"/>
            <field name="state"/>
        </tree>
    </field>
</record>
```

**After (Odoo 18)**:
```xml
<record id="view_order_tree" model="ir.ui.view">
    <field name="name">sale.order.tree</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <!-- colors attribute is deprecated, use decoration- -->
        <tree string="Sales Orders"
              decoration-info="state == 'draft'"
              decoration-success="state == 'sale'"
              decoration-muted="state == 'cancel'"
              multi_edit="1"
              sample="1">

            <field name="name" string="Order Reference"/>
            <field name="partner_id" widget="many2one_avatar"/>
            <field name="date_order" widget="remaining_days"/>
            <field name="user_id" widget="many2one_avatar_user" optional="show"/>
            <field name="amount_total" widget="monetary" sum="Total"/>
            <field name="state" widget="badge"
                   decoration-info="state == 'draft'"
                   decoration-success="state == 'sale'"/>

            <!-- Optional fields (hidden by default, user can show) -->
            <field name="payment_term_id" optional="hide"/>
            <field name="company_id" optional="hide"
                   groups="base.group_multi_company"/>
        </tree>
    </field>
</record>
```

---

## Database Migration

### Migration Scripts

Create migration script in: `migrations/18.0.1.0.0/pre-migrate.py`

```python
"""
Pre-migration script for Odoo 18
This runs BEFORE the module is loaded
"""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Pre-migration tasks
    """
    _logger.info("Starting pre-migration to 18.0.1.0.0")

    # 1. Rename columns if needed
    _rename_columns(cr)

    # 2. Add new required columns with default values
    _add_required_columns(cr)

    # 3. Migrate data before model changes
    _migrate_selection_values(cr)

    _logger.info("Pre-migration completed")


def _rename_columns(cr):
    """Rename columns that changed names"""
    # Check if column exists before renaming
    cr.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'my_model'
        AND column_name = 'old_column_name'
    """)

    if cr.fetchone():
        _logger.info("Renaming column old_column_name to new_column_name")
        cr.execute("""
            ALTER TABLE my_model
            RENAME COLUMN old_column_name TO new_column_name
        """)


def _add_required_columns(cr):
    """Add new required columns with default values"""
    cr.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'my_model'
        AND column_name = 'new_required_field'
    """)

    if not cr.fetchone():
        _logger.info("Adding new_required_field column")
        cr.execute("""
            ALTER TABLE my_model
            ADD COLUMN new_required_field VARCHAR DEFAULT 'default_value'
        """)


def _migrate_selection_values(cr):
    """Migrate selection field values"""
    _logger.info("Migrating selection values")
    cr.execute("""
        UPDATE my_model
        SET state = 'confirmed'
        WHERE state = 'confirm'
    """)
```

Create post-migration script in: `migrations/18.0.1.0.0/post-migrate.py`

```python
"""
Post-migration script for Odoo 18
This runs AFTER the module is loaded
"""
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Post-migration tasks
    """
    _logger.info("Starting post-migration to 18.0.1.0.0")

    env = api.Environment(cr, SUPERUSER_ID, {})

    # 1. Recompute stored computed fields
    _recompute_fields(env)

    # 2. Create missing records
    _create_default_records(env)

    # 3. Update security rules
    _update_security(env)

    # 4. Migrate related data
    _migrate_related_data(env)

    _logger.info("Post-migration completed")


def _recompute_fields(env):
    """Recompute stored computed fields"""
    _logger.info("Recomputing computed fields")

    # Recompute all records
    records = env['my.model'].search([])
    if records:
        records._compute_total()
        records._compute_display_name()


def _create_default_records(env):
    """Create default/required records"""
    _logger.info("Creating default records")

    # Create default configuration
    if not env['my.config'].search([('is_default', '=', True)]):
        env['my.config'].create({
            'name': 'Default Configuration',
            'is_default': True,
        })


def _update_security(env):
    """Update security rules and access rights"""
    _logger.info("Updating security rules")

    # Update record rules
    rule = env.ref('my_module.my_record_rule', raise_if_not_found=False)
    if rule:
        rule.write({
            'domain_force': "[('company_id', 'in', company_ids)]"
        })


def _migrate_related_data(env):
    """Migrate related data between models"""
    _logger.info("Migrating related data")

    # Example: Move data from one model to another
    old_records = env['old.model'].search([])
    for old_record in old_records:
        env['new.model'].create({
            'name': old_record.name,
            'value': old_record.value,
            'old_id': old_record.id,
        })
```

---

## Security Changes

### Access Rights Migration

**Before (Odoo 17)** - `security/ir.model.access.csv`:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,0
access_my_model_manager,my.model.manager,model_my_model,base.group_system,1,1,1,1
```

**After (Odoo 18)** - Enhanced with better naming:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,Access My Model User,model_my_model,base.group_user,1,1,1,0
access_my_model_manager,Access My Model Manager,model_my_model,base.group_system,1,1,1,1
access_my_model_public,Access My Model Public,model_my_model,,1,0,0,0
```

### Record Rules Migration

**Before (Odoo 17)**:
```xml
<record id="my_model_rule" model="ir.rule">
    <field name="name">My Model: User Access</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
</record>
```

**After (Odoo 18)**:
```xml
<!-- Enhanced with better multi-company and team support -->
<record id="my_model_rule_user" model="ir.rule">
    <field name="name">My Model: User Own Records</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="domain_force">[
        '|',
            ('user_id', '=', user.id),
            ('user_id', '=', False)
    ]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="False"/>
</record>

<record id="my_model_rule_manager" model="ir.rule">
    <field name="name">My Model: Manager All Access</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="domain_force">[(1, '=', 1)]</field>
    <field name="groups" eval="[(4, ref('base.group_system'))]"/>
</record>

<!-- Multi-company rule -->
<record id="my_model_rule_company" model="ir.rule">
    <field name="name">My Model: Multi-Company</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="global" eval="True"/>
    <field name="domain_force">[
        '|',
            ('company_id', '=', False),
            ('company_id', 'in', company_ids)
    ]</field>
</record>
```

---

## Common Issues and Solutions

### Issue 1: Import Errors

**Problem**: Module fails to load with import errors

**Error Message**:
```
ImportError: cannot import name 'X' from 'odoo.addons.Y'
```

**Solution**:
```python
# Old import (Odoo 17)
from odoo.addons.web.controllers.main import Home

# New import (Odoo 18)
from odoo.addons.web.controllers.home import Home
```

### Issue 2: OWL Component Not Rendering

**Problem**: JavaScript component doesn't render

**Error Message**:
```
Error: Props validation failed for component MyComponent
```

**Solution**:
```javascript
// Add static props definition
export class MyComponent extends Component {
    static template = "my_module.MyComponent";
    static props = {
        '*': true,  // Accept any props (not recommended)
        // OR define specific props:
        // title: { type: String, optional: true },
        // value: Number,
    };
}
```

### Issue 3: Computed Field Not Computing

**Problem**: Computed fields show empty values after migration

**Solution**:
```python
# Run in Odoo shell or migration script
env = api.Environment(cr, SUPERUSER_ID, {})
records = env['my.model'].search([])
records._recompute_fields(['computed_field_name'])

# Or force recompute
for record in records:
    record._compute_computed_field_name()
```

### Issue 4: Access Rights Issues

**Problem**: Users can't access records after migration

**Solution**:
```bash
# Update security after migration
# In Odoo shell:
env['ir.model.access'].call_cache_clearing_methods()
env['ir.rule'].clear_caches()

# Force security reload
env.registry.clear_caches()
```

### Issue 5: View Inheritance Not Working

**Problem**: View inheritance doesn't apply changes

**Solution**:
```xml
<!-- Make sure inherit_id is correct -->
<record id="view_my_form_inherit" model="ir.ui.view">
    <field name="name">my.model.form.inherit</field>
    <field name="model">my.model</field>
    <field name="inherit_id" ref="module_name.view_id"/>
    <field name="arch" type="xml">
        <!-- Use xpath with correct positions -->
        <xpath expr="//field[@name='partner_id']" position="after">
            <field name="my_new_field"/>
        </xpath>
    </field>
</record>
```

---

## Performance Optimization After Migration

### Database Indexes

```python
# Add indexes for better performance
class MyModel(models.Model):
    _name = 'my.model'

    # Add index to frequently searched fields
    partner_id = fields.Many2one('res.partner', index=True)
    date = fields.Date(index=True)
    state = fields.Selection([...], index=True)

    # Composite index for complex queries
    _sql_constraints = [
        ('unique_partner_date',
         'UNIQUE(partner_id, date)',
         'Partner and date must be unique')
    ]

    def init(self):
        # Create custom indexes
        self.env.cr.execute("""
            CREATE INDEX IF NOT EXISTS my_model_partner_state_idx
            ON my_model (partner_id, state)
            WHERE state != 'cancel'
        """)
```

### Batch Processing

```python
# Old approach (slow for large datasets)
for record in self.env['my.model'].search([]):
    record.process()

# New approach (batch processing)
records = self.env['my.model'].search([])
for batch in records.batched(batch_size=100):
    batch.process()  # Process 100 records at a time
```

---

## Rollback Plan

### Pre-Rollback Checklist

- [ ] Backup current state
- [ ] Document issues encountered
- [ ] Prepare communication plan
- [ ] Test rollback in staging

### Rollback Steps

1. **Stop Odoo Service**
```bash
sudo systemctl stop odoo18
```

2. **Restore Database**
```bash
# Drop current database
sudo -u postgres dropdb odoo18_production

# Restore backup
sudo -u postgres pg_restore -d odoo18_production backup_pre_migration.dump
```

3. **Restore Filestore**
```bash
rm -rf /opt/odoo/filestore/odoo18_production
cp -r /backup/filestore/odoo18_production /opt/odoo/filestore/
```

4. **Checkout Odoo 17**
```bash
cd /opt/odoo/odoo
git checkout 17.0
```

5. **Restore Custom Modules**
```bash
cd /opt/odoo/custom-addons
git checkout odoo-17-stable
```

6. **Start Odoo Service**
```bash
sudo systemctl start odoo17
```

---

## Automated Migration Testing

```python
# tests/test_migration.py
from odoo.tests import TransactionCase, tagged

@tagged('post_install', '-at_install', 'migration')
class TestMigration(TransactionCase):

    def test_all_modules_installed(self):
        """Verify all modules installed successfully"""
        failed_modules = self.env['ir.module.module'].search([
            ('state', '=', 'to install'),
        ])
        self.assertFalse(failed_modules,
                        f"Modules failed to install: {failed_modules.mapped('name')}")

    def test_computed_fields(self):
        """Verify computed fields are working"""
        record = self.env['my.model'].create({
            'name': 'Test',
            'value1': 10,
            'value2': 20,
        })
        self.assertEqual(record.computed_total, 30,
                        "Computed field not calculating correctly")

    def test_security_rules(self):
        """Verify security rules are applied"""
        user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'testuser',
            'groups_id': [(4, self.env.ref('base.group_user').id)],
        })

        record = self.env['my.model'].sudo().create({
            'name': 'Test',
            'user_id': user.id,
        })

        # User should see their own record
        records = self.env['my.model'].sudo(user).search([])
        self.assertIn(record, records, "User can't see their own record")

    def test_view_definitions(self):
        """Verify all views are valid"""
        views = self.env['ir.ui.view'].search([
            ('model', '=', 'my.model'),
        ])

        for view in views:
            try:
                self.env['my.model'].fields_view_get(view_id=view.id)
            except Exception as e:
                self.fail(f"View {view.name} is invalid: {str(e)}")
```

---

## Additional Resources

- Official Odoo 18 Release Notes: https://www.odoo.com/odoo-18
- Migration Guide Repository: https://github.com/odoo/odoo/wiki/Migration
- OWL 2.0 Documentation: https://github.com/odoo/owl
- Community Forum: https://www.odoo.com/forum

---

## Migration Timeline Template

| Phase | Duration | Tasks | Responsible |
|-------|----------|-------|-------------|
| Preparation | 2 weeks | Environment setup, code analysis | Dev Team |
| Development | 4 weeks | Code migration, testing | Dev Team |
| Testing | 2 weeks | QA, UAT | QA Team |
| Deployment | 1 week | Staging, Production | DevOps |
| Support | 2 weeks | Bug fixes, optimization | Support Team |

---

**Document Version**: 1.0
**Last Updated**: 2025-10-16
**Odoo Version**: 18.0
