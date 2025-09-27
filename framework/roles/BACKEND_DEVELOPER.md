# Odoo 18 Backend Developer Role

## Role Description

The Backend Developer role is responsible for developing and maintaining the server-side logic, database structure, and business logic of Odoo 18 applications. This role requires deep understanding of Odoo's ORM, models, and backend architecture.

## Key Responsibilities

- Design and implement Odoo models and database structures
- Create business logic using Python and Odoo's ORM
- Develop API endpoints and integrate with external systems
- Optimize database queries and backend performance
- Implement security rules and access controls
- Create and maintain automated tests

## Technical Knowledge

### ORM Fundamentals

```python
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SampleModel(models.Model):
    _name = 'sample.model'
    _description = 'Sample Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], default='draft', tracking=True)
    
    @api.depends('line_ids.amount')
    def _compute_total(self):
        for record in self:
            record.total_amount = sum(record.line_ids.mapped('amount'))
```

### Model Types

Understanding of model inheritance types and when to use them:

1. **Regular Models** (`models.Model`)
   - Stored in database tables
   - For business entities with persistence needs

2. **Transient Models** (`models.TransientModel`)
   - Temporary data with automatic cleanup
   - Used for wizards and temporary processes

3. **Abstract Models** (`models.AbstractModel`)
   - Not stored in database
   - Used for reusable model behaviors

### Field Types and Attributes

Knowledge of all field types and their specific behaviors:

- **Basic Types**: `Boolean`, `Char`, `Integer`, `Float`, `Text`
- **Date/Time**: `Date`, `Datetime`
- **Relational**: `Many2one`, `One2many`, `Many2many`
- **Special**: `Binary`, `Selection`, `Reference`, `Monetary`, `Image`

Field attributes and their implications:
- `required`, `readonly`, `store`, `compute`, `related`
- `index`, `copy`, `default`, `group_operator`
- `domain`, `context`, `tracking`

### API Decorators

Proper use of API decorators for method definitions:

```python
@api.model
def function_without_recordset_dependency(self, value):
    # self is a recordset, but its content is not relevant

@api.depends('field1', 'field2')
def _compute_something(self):
    # Used for computed fields with dependencies

@api.constrains('field1', 'field2')
def _check_something(self):
    # Validation constraints when fields are changed

@api.onchange('field1')
def _onchange_something(self):
    # UI feedback when field values change in forms

@api.returns('res.partner')
def get_partner(self):
    # Specify return value model
```

### Database Operations

```python
# Creating records
partner = self.env['res.partner'].create({
    'name': 'Test Partner',
    'email': 'test@example.com',
})

# Searching records
partners = self.env['res.partner'].search([
    ('customer_rank', '>', 0),
    '|', 
    ('city', '=', 'New York'),
    ('state_id.code', '=', 'NY')
])

# Reading fields
data = partners.read(['name', 'email', 'phone'])

# Updating records
partners.write({'category_id': [(4, category_id)]})

# Using ORM commands for relational fields
product.write({
    'seller_ids': [
        (0, 0, {'name': vendor.id, 'price': 100.0}),  # Create
        (1, seller.id, {'price': 90.0}),              # Update
        (2, old_seller.id, 0),                        # Delete
        (3, seller_to_unlink.id, 0),                  # Unlink
        (4, seller_to_link.id, 0),                    # Link
        (5, 0, 0),                                    # Clear
        (6, 0, [id1, id2, id3])                       # Replace
    ]
})
```

### Security Implementation

```python
# ir.model.access.csv
"id","name","model_id:id","group_id:id","perm_read","perm_write","perm_create","perm_unlink"
"access_model_user","model.name.user","model_model_name","group_user",1,0,0,0
"access_model_manager","model.name.manager","model_model_name","group_manager",1,1,1,1

# security/security.xml
<record id="rule_model_name_own" model="ir.rule">
    <field name="name">Own Records Only</field>
    <field name="model_id" ref="model_model_name"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('group_user'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="True"/>
</record>
```

## Debugging and Error Handling

```python
import logging
_logger = logging.getLogger(__name__)

# Proper error logging
try:
    result = some_function()
except Exception as e:
    _logger.error("Failed to execute function: %s", e)
    raise UserError(_("An error occurred: %s", str(e)))

# Debug logging with context
_logger.debug("Processing order %s with lines: %s", order.name, order.line_ids.ids)
```

## Advanced Backend Features

### SQL for Performance

When ORM isn't efficient enough:

```python
self.env.cr.execute("""
    SELECT p.id, p.name, COUNT(o.id) as order_count
    FROM res_partner p
    LEFT JOIN sale_order o ON o.partner_id = p.id
    WHERE p.active = true
    GROUP BY p.id, p.name
    HAVING COUNT(o.id) > 5
""")
results = self.env.cr.dictfetchall()

# Always flush models before raw SQL that depends on them
self.env['sale.order'].flush_model(['partner_id'])
```

### Environment Management

```python
# Changing user context
records_as_admin = records.with_user(self.env.ref('base.user_admin'))

# Changing company context
records_in_company = records.with_company(self.env.company)

# Changing environment context
records_with_ctx = records.with_context(default_date=fields.Date.today())

# Running as superuser
records_sudo = records.sudo()
```

## Critical Anti-Patterns

❌ **Avoid these practices:**
- Bypassing ORM with SQL when not needed for performance
- Not handling record existence checks
- Ignoring security implications
- Missing transaction management
- Inappropriate use of sudo()
- Not validating user input

## Resources & References

- [Odoo 18 ORM API Documentation](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html)
- [Odoo Security Documentation](https://www.odoo.com/documentation/18.0/developer/reference/backend/security.html)
- [Odoo Performance Best Practices](https://www.odoo.com/documentation/18.0/developer/reference/backend/performance.html)