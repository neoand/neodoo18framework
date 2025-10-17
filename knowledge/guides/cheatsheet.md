# Odoo 18 Cheat Sheet

## Quick Reference Guide for Odoo 18 Development

---

## Table of Contents

1. [CLI Commands](#cli-commands)
2. [Field Types Reference](#field-types-reference)
3. [Decorator Reference](#decorator-reference)
4. [ORM Methods](#orm-methods)
5. [Domain Syntax](#domain-syntax)
6. [Widget Reference](#widget-reference)
7. [View Attributes](#view-attributes)
8. [JavaScript Hooks](#javascript-hooks)
9. [Common Patterns](#common-patterns)
10. [Debugging Tips](#debugging-tips)

---

## CLI Commands

### Server Management

| Command | Description | Example |
|---------|-------------|---------|
| `odoo-bin -c config.conf` | Start server with config | `./odoo-bin -c /etc/odoo.conf` |
| `odoo-bin -d dbname -i module` | Install module | `./odoo-bin -d mydb -i sale` |
| `odoo-bin -d dbname -u module` | Update module | `./odoo-bin -d mydb -u sale` |
| `odoo-bin --dev=all` | Development mode | `./odoo-bin --dev=xml,reload,qweb` |
| `odoo-bin shell -d dbname` | Open Python shell | `./odoo-bin shell -d mydb` |
| `odoo-bin scaffold module_name path` | Create module skeleton | `./odoo-bin scaffold my_module addons/` |

### Development Flags

| Flag | Description |
|------|-------------|
| `--dev=xml` | Auto-reload XML files |
| `--dev=reload` | Auto-restart on Python changes |
| `--dev=qweb` | Don't cache QWeb templates |
| `--dev=all` | Enable all dev features |
| `--test-enable` | Enable tests |
| `--log-level=debug` | Set log level |

### Database Operations

```bash
# Create database
odoo-bin -d newdb --db-filter=newdb --without-demo=all

# Drop database
dropdb dbname

# Backup database
pg_dump dbname > backup.sql

# Restore database
psql dbname < backup.sql

# List databases
psql -l
```

---

## Field Types Reference

### Basic Fields

| Field Type | Python Example | Description |
|------------|----------------|-------------|
| **Boolean** | `active = fields.Boolean(default=True)` | True/False value |
| **Char** | `name = fields.Char(size=128, required=True)` | String field |
| **Text** | `notes = fields.Text()` | Multiline text |
| **Html** | `description = fields.Html(sanitize=True)` | HTML content |
| **Integer** | `quantity = fields.Integer(default=1)` | Integer number |
| **Float** | `price = fields.Float(digits=(12, 2))` | Decimal number |
| **Monetary** | `amount = fields.Monetary(currency_field='currency_id')` | Currency amount |
| **Date** | `date = fields.Date(default=fields.Date.today)` | Date only |
| **Datetime** | `datetime = fields.Datetime(default=fields.Datetime.now)` | Date and time |
| **Binary** | `image = fields.Binary(attachment=True)` | File/Image data |
| **Selection** | `state = fields.Selection([('a','A'),('b','B')])` | Dropdown list |
| **Image** | `avatar = fields.Image(max_width=128)` | Resizable image |

### Relational Fields

| Field Type | Syntax | Description |
|------------|--------|-------------|
| **Many2one** | `partner_id = fields.Many2one('res.partner', string='Customer', ondelete='cascade')` | Foreign key |
| **One2many** | `line_ids = fields.One2many('sale.line', 'order_id', string='Lines')` | Inverse relation |
| **Many2many** | `tag_ids = fields.Many2many('product.tag', string='Tags')` | Many-to-many table |

### Computed & Related Fields

| Field Type | Example | Description |
|------------|---------|-------------|
| **Computed** | `total = fields.Float(compute='_compute_total', store=True)` | Calculated field |
| **Related** | `partner_email = fields.Char(related='partner_id.email')` | Related field shortcut |
| **Property** | `property_field = fields.Property(type='char')` | Company-specific value |

### Field Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `string` | str | Field label | `string='Customer Name'` |
| `required` | bool | Mandatory field | `required=True` |
| `readonly` | bool | Read-only field | `readonly=True` |
| `index` | str/bool | Database index | `index='btree'` |
| `default` | any | Default value | `default=lambda self: self.env.user` |
| `help` | str | Tooltip text | `help='Enter customer name'` |
| `copy` | bool | Copy on duplicate | `copy=False` |
| `store` | bool | Store computed | `store=True` |
| `tracking` | bool | Track changes | `tracking=True` |
| `groups` | str | Access groups | `groups='base.group_system'` |
| `company_dependent` | bool | Per-company value | `company_dependent=True` |
| `domain` | list | Filter records | `domain=[('active','=',True)]` |
| `context` | dict | Context values | `context={'default_type':'sale'}` |
| `ondelete` | str | Delete behavior | `ondelete='cascade'` |
| `check_company` | bool | Multi-company check | `check_company=True` |

---

## Decorator Reference

### API Decorators

| Decorator | Usage | Description |
|-----------|-------|-------------|
| `@api.model` | Methods that don't need recordset | Class-level method |
| `@api.model_create_multi` | `def create(self, vals_list):` | Batch create support |
| `@api.depends('field')` | `def _compute_x(self):` | Computed field dependencies |
| `@api.depends_context('uid')` | `def _compute_x(self):` | Context-dependent compute |
| `@api.constrains('field')` | `def _check_x(self):` | Field validation |
| `@api.onchange('field')` | `def _onchange_x(self):` | UI onchange handler |
| `@api.ondelete(at_uninstall=False)` | `def _unlink_x(self):` | Pre-delete validation |
| `@api.returns('model')` | `def method(self):` | Return value type hint |

### Examples

```python
from odoo import api, fields, models, Command

class MyModel(models.Model):
    _name = 'my.model'

    # Model method (no record needed)
    @api.model
    def get_config(self):
        return self.env['ir.config_parameter'].get_param('my_key')

    # Batch create (receives list of dicts)
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)

    # Computed field
    @api.depends('line_ids.amount')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.line_ids.mapped('amount'))

    # Context-dependent compute
    @api.depends_context('uid', 'company_id')
    def _compute_user_specific(self):
        for record in self:
            record.value = self.env.user.name

    # Validation constraint
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_end < record.date_start:
                raise ValidationError("End date must be after start date")

    # Onchange (UI only)
    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.email = self.partner_id.email
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'Partner email loaded'
                }
            }

    # Pre-delete check
    @api.ondelete(at_uninstall=False)
    def _check_unlink(self):
        if any(rec.state == 'confirmed' for rec in self):
            raise UserError("Cannot delete confirmed records")
```

---

## ORM Methods

### CRUD Operations

| Method | Syntax | Returns | Description |
|--------|--------|---------|-------------|
| **create** | `self.env['model'].create(vals)` | recordset | Create record(s) |
| **search** | `self.env['model'].search([domain])` | recordset | Search records |
| **search_count** | `self.env['model'].search_count([domain])` | int | Count records |
| **search_read** | `self.env['model'].search_read([domain], fields)` | list[dict] | Search + read optimized |
| **read** | `records.read(['field1', 'field2'])` | list[dict] | Read field values |
| **write** | `records.write({'field': value})` | bool | Update records |
| **unlink** | `records.unlink()` | bool | Delete records |
| **copy** | `record.copy(default={'field': value})` | recordset | Duplicate record |

### Search Methods

| Method | Example | Description |
|--------|---------|-------------|
| **browse** | `self.env['model'].browse([1,2,3])` | Get records by IDs |
| **exists** | `records.exists()` | Filter existing records |
| **ensure_one** | `self.ensure_one()` | Assert single record |
| **filtered** | `records.filtered(lambda r: r.active)` | Filter recordset |
| **mapped** | `records.mapped('partner_id.name')` | Extract field values |
| **sorted** | `records.sorted(key=lambda r: r.date)` | Sort recordset |
| **batched** | `records.batched(batch_size=100)` | Iterate in batches |

### Advanced ORM

```python
# Fetch references
Model = self.env['model.name']

# With context
Model.with_context(lang='es_ES', tz='Europe/Madrid').search([])

# With company
Model.with_company(company_id).create({})

# With user (sudo)
Model.sudo().write({})  # Bypass access rights

# With environment
new_env = self.env(user=user_id, context={'key': 'value'})
Model.with_env(new_env).search([])

# Batch processing
for batch in records.batched(batch_size=1000):
    batch.process()

# Invalidate cache
records.invalidate_recordset(['field1', 'field2'])

# Refresh from database
records.refresh()
```

### Command Class (x2many)

```python
from odoo.models import Command

# Create new record
commands = [Command.create({'name': 'New Line'})]

# Update existing
commands = [Command.update(line_id, {'quantity': 5})]

# Delete (remove + delete from DB)
commands = [Command.delete(line_id)]

# Unlink (remove from relation, keep in DB)
commands = [Command.unlink(line_id)]

# Link existing
commands = [Command.link(line_id)]

# Clear all
commands = [Command.clear()]

# Set (replace all)
commands = [Command.set([line1_id, line2_id])]

# Multiple operations
self.line_ids = [
    Command.create({'name': 'Line 1'}),
    Command.update(existing_id, {'qty': 10}),
    Command.delete(old_id),
]
```

---

## Domain Syntax

### Basic Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `[('name', '=', 'John')]` | Equals |
| `!=` | `[('state', '!=', 'cancel')]` | Not equals |
| `>` | `[('age', '>', 18)]` | Greater than |
| `>=` | `[('age', '>=', 18)]` | Greater or equal |
| `<` | `[('price', '<', 100)]` | Less than |
| `<=` | `[('price', '<=', 100)]` | Less or equal |
| `in` | `[('id', 'in', [1,2,3])]` | In list |
| `not in` | `[('id', 'not in', [1,2,3])]` | Not in list |
| `like` | `[('name', 'like', 'John%')]` | Pattern match |
| `ilike` | `[('name', 'ilike', 'john')]` | Case-insensitive like |
| `=like` | `[('email', '=like', '%@gmail.com')]` | Exact pattern |
| `=ilike` | `[('email', '=ilike', '%@GMAIL.com')]` | Case-insensitive exact |
| `child_of` | `[('id', 'child_of', parent_id)]` | Hierarchical child |
| `parent_of` | `[('id', 'parent_of', child_id)]` | Hierarchical parent |

### Logical Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `&` (AND) | `['&', ('a', '=', 1), ('b', '=', 2)]` | Both conditions |
| `|` (OR) | `['|', ('a', '=', 1), ('b', '=', 2)]` | Either condition |
| `!` (NOT) | `['!', ('active', '=', False)]` | Negate condition |

### Domain Examples

```python
# Simple domain
[('customer_rank', '>', 0)]

# AND (implicit)
[('customer_rank', '>', 0), ('active', '=', True)]

# OR
['|', ('is_company', '=', True), ('customer_rank', '>', 0)]

# Complex: (A OR B) AND C
['&', '|', ('a', '=', 1), ('b', '=', 2), ('c', '=', 3)]

# NOT
['!', ('state', '=', 'cancel')]

# Relational field
[('partner_id.country_id.code', '=', 'US')]

# Multiple OR
['|', '|', ('state', '=', 'a'), ('state', '=', 'b'), ('state', '=', 'c')]
# Better: [('state', 'in', ['a', 'b', 'c'])]

# Date range
[('date', '>=', '2024-01-01'), ('date', '<=', '2024-12-31')]

# Empty/Not empty
[('partner_id', '!=', False)]  # Has partner
[('partner_id', '=', False)]   # No partner

# Child of (hierarchical)
[('category_id', 'child_of', parent_category_id)]
```

---

## Widget Reference

### Form View Widgets

| Widget | Field Type | Description | Example |
|--------|------------|-------------|---------|
| `many2one` | Many2one | Standard dropdown | `widget="many2one"` |
| `many2one_barcode` | Many2one | With barcode scan | `widget="many2one_barcode"` |
| `many2one_avatar` | Many2one | With avatar image | `widget="many2one_avatar"` |
| `many2one_avatar_user` | Many2one | User with avatar | `widget="many2one_avatar_user"` |
| `selection` | Many2one/Selection | Radio buttons | `widget="selection"` |
| `radio` | Selection | Radio buttons | `widget="radio"` |
| `priority` | Selection | Star rating | `widget="priority"` |
| `boolean_toggle` | Boolean | Toggle switch | `widget="boolean_toggle"` |
| `statusbar` | Selection | Status bar | `widget="statusbar"` |
| `monetary` | Float/Monetary | Currency format | `widget="monetary"` |
| `percentage` | Float | Percentage | `widget="percentage"` |
| `progressbar` | Float | Progress bar | `widget="progressbar"` |
| `handle` | Integer | Drag handle | `widget="handle"` |
| `image` | Binary | Image preview | `widget="image"` |
| `pdf_viewer` | Binary | PDF viewer | `widget="pdf_viewer"` |
| `html` | Html | HTML editor | `widget="html"` |
| `ace` | Text | Code editor | `widget="ace"` |
| `phone` | Char | Phone link | `widget="phone"` |
| `email` | Char | Email link | `widget="email"` |
| `url` | Char | URL link | `widget="url"` |
| `badge` | Selection/Char | Badge pill | `widget="badge"` |
| `color` | Integer | Color picker | `widget="color"` |
| `remaining_days` | Date | Days remaining | `widget="remaining_days"` |
| `daterange` | Date | Date range picker | `widget="daterange"` |
| `many2many_tags` | Many2many | Tag badges | `widget="many2many_tags"` |
| `many2many_checkboxes` | Many2many | Checkbox list | `widget="many2many_checkboxes"` |
| `one2many` | One2many | Embedded list | `widget="one2many"` |
| `section_and_note_one2many` | One2many | With sections | `widget="section_and_note_one2many"` |
| `statinfo` | Integer | Stat button | `widget="statinfo"` |

### Tree View Widgets

| Widget | Description |
|--------|-------------|
| `badge` | Colored badge |
| `boolean_toggle` | Toggle switch |
| `handle` | Drag and drop handle |
| `monetary` | Currency formatting |
| `many2many_tags` | Tag pills |
| `progressbar` | Progress bar |

---

## View Attributes

### Form View Attributes

```xml
<form string="Title" create="true" edit="true" delete="true" duplicate="true">
    <!-- create: Allow creation (default: true) -->
    <!-- edit: Allow editing (default: true) -->
    <!-- delete: Allow deletion (default: true) -->
    <!-- duplicate: Allow duplication (default: true) -->
</form>
```

### Tree View Attributes

```xml
<tree string="Title"
      editable="top"
      multi_edit="1"
      create="true"
      delete="true"
      sample="1"
      decoration-info="state == 'draft'"
      decoration-success="state == 'done'"
      decoration-danger="state == 'cancel'"
      decoration-muted="active == False"
      decoration-bf="priority == '1'"
      decoration-it="priority == '2'">

    <!-- editable: top|bottom (inline edit) -->
    <!-- multi_edit: Enable multi-edit (1|0) -->
    <!-- sample: Show sample data (1|0) -->
    <!-- decoration-*: Conditional formatting -->
    <!-- decoration-bf: Bold font -->
    <!-- decoration-it: Italic font -->
</tree>
```

### Field Attributes

```xml
<field name="field_name"
       string="Label"
       required="1"
       readonly="1"
       invisible="state != 'draft'"
       domain="[('active', '=', True)]"
       context="{'default_type': 'sale'}"
       options="{'no_create': True}"
       placeholder="Enter value..."
       help="Tooltip text"
       widget="many2one"
       class="oe_inline"
       groups="base.group_system"
       password="true"
       kanban_view_ref="module.view_id"
       nolabel="1"
       colspan="2"
       force_save="1"/>
```

### Button Attributes

```xml
<button name="action_confirm"
        string="Confirm"
        type="object"
        class="btn-primary"
        invisible="state != 'draft'"
        confirm="Are you sure?"
        icon="fa-check"
        help="Confirm the record"
        groups="base.group_user"/>

<!-- type: object|action|workflow -->
<!-- class: btn-primary|btn-secondary|btn-success|btn-danger|btn-warning|btn-info|btn-link -->
```

---

## JavaScript Hooks

### OWL Hooks

| Hook | Usage | Description |
|------|-------|-------------|
| `setup()` | Component initialization | Setup services, state, refs |
| `onWillStart()` | Before first render | Async data loading |
| `onMounted()` | After first render | DOM manipulation |
| `onWillUpdateProps()` | Before props update | Validate new props |
| `onWillPatch()` | Before re-render | Pre-update logic |
| `onPatched()` | After re-render | Post-update DOM changes |
| `onWillUnmount()` | Before destroy | Cleanup |
| `onWillDestroy()` | Before component destroyed | Final cleanup |

### Hook Examples

```javascript
import { Component, useState, useRef, onMounted, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class MyComponent extends Component {
    setup() {
        // Services
        this.orm = useService("orm");

        // State
        this.state = useState({ data: null });

        // Refs
        this.inputRef = useRef("input");

        // Lifecycle
        onWillStart(async () => {
            // Load data before rendering
            this.state.data = await this.loadData();
        });

        onMounted(() => {
            // Access DOM after render
            this.inputRef.el.focus();
        });
    }

    async loadData() {
        return await this.orm.searchRead("model", [], ["name"]);
    }
}
```

---

## Common Patterns

### Sequence Generation

```python
# In model
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('model.sequence')
    return super().create(vals_list)

# In data XML
<record id="seq_model" model="ir.sequence">
    <field name="name">Model Sequence</field>
    <field name="code">model.sequence</field>
    <field name="prefix">MO</field>
    <field name="padding">5</field>
    <field name="number_next">1</field>
    <field name="number_increment">1</field>
</record>
```

### Computed Field Pattern

```python
# Stored computed field with dependencies
total = fields.Float(
    compute='_compute_total',
    store=True,
    tracking=True,
)

@api.depends('line_ids.amount')
def _compute_total(self):
    for record in self:
        record.total = sum(record.line_ids.mapped('amount'))

# Inverse method (editable computed)
@api.depends('line_ids.amount')
def _compute_total(self):
    for record in self:
        record.total = sum(record.line_ids.mapped('amount'))

def _inverse_total(self):
    for record in self:
        if record.line_ids:
            record.line_ids[0].amount = record.total
```

### State Machine Pattern

```python
state = fields.Selection([
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('done', 'Done'),
    ('cancel', 'Cancelled'),
], default='draft', tracking=True)

def action_confirm(self):
    self.ensure_one()
    if self.state != 'draft':
        raise UserError("Only draft records can be confirmed")
    self.state = 'confirmed'

def action_done(self):
    self.ensure_one()
    if self.state != 'confirmed':
        raise UserError("Only confirmed records can be done")
    self.state = 'done'

def action_cancel(self):
    if any(r.state == 'done' for r in self):
        raise UserError("Cannot cancel done records")
    self.state = 'cancel'
```

### Wizard Pattern

```python
# Wizard model
class MyWizard(models.TransientModel):
    _name = 'my.wizard'
    _description = 'My Wizard'

    # Fields
    name = fields.Char(required=True)

    # Action
    def action_process(self):
        # Get active records
        active_ids = self.env.context.get('active_ids', [])
        records = self.env['my.model'].browse(active_ids)

        # Process
        records.write({'name': self.name})

        return {'type': 'ir.actions.act_window_close'}

# Open wizard from action
def open_wizard(self):
    return {
        'name': 'My Wizard',
        'type': 'ir.actions.act_window',
        'res_model': 'my.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {'default_name': self.name},
    }
```

---

## Debugging Tips

### Python Debugging

```python
# Print to log
import logging
_logger = logging.getLogger(__name__)
_logger.info("Debug message: %s", variable)

# Debug with pdb
import pdb; pdb.set_trace()

# IPython debugger (better)
import ipdb; ipdb.set_trace()

# Print SQL queries
self.env.cr.execute("SELECT * FROM model WHERE id = %s", (1,))
_logger.info("SQL: %s", self.env.cr.query)

# Check cache
_logger.info("Cache: %s", self.env.cache)
```

### Shell Commands

```python
# In odoo shell
env['model'].search([])  # Search records
env.ref('module.xml_id')  # Get record by XML ID
env.user  # Current user
env.company  # Current company

# Update module
env['ir.module.module'].search([('name','=','my_module')]).button_immediate_upgrade()

# Clear cache
env.registry.clear_caches()

# Recompute field
env['model'].search([])._recompute_fields(['field_name'])
```

### JavaScript Debugging

```javascript
// Console log
console.log("Debug:", data);

// Debugger
debugger;

// Access ORM from console
const orm = odoo.__DEBUG__.services["orm"];
await orm.searchRead("res.partner", [], ["name"]);

// Access registry
const registry = odoo.__DEBUG__.services.registry;
```

---

## Performance Quick Tips

| Issue | Solution |
|-------|----------|
| Slow list view | Use `search_read` instead of `search` + `read` |
| N+1 queries | Use `mapped()` or `prefetch()` |
| Slow computed field | Add `store=True` |
| Slow search | Add index: `index='btree'` |
| Large recordset | Use `batched()` for iteration |
| Unnecessary fields | Limit fields in `search_read` |
| Cache issues | Use `@tools.ormcache()` |

---

## Quick Setup Checklist

### New Module

- [ ] Create module structure
- [ ] Add `__manifest__.py`
- [ ] Define models in `models/`
- [ ] Create views in `views/`
- [ ] Add security in `security/`
- [ ] Write tests in `tests/`
- [ ] Update module with `-u module_name`

### New Model

- [ ] Create Python file in `models/`
- [ ] Define `_name` and `_description`
- [ ] Add fields
- [ ] Create views (form, tree, search)
- [ ] Add access rights in `ir.model.access.csv`
- [ ] Add menu item
- [ ] Add record rules if needed

---

**Quick Reference Version**: 1.0
**Last Updated**: 2025-10-16
**Odoo Version**: 18.0
