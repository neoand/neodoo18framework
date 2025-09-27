# Security Expert Role - Odoo 18+ Security Specialist

## Role Overview

The Security Expert role is responsible for ensuring the security, data protection, and compliance of Odoo 18+ applications. This specialist identifies vulnerabilities, implements security controls, configures proper access rights, and ensures compliance with relevant regulations.

## Core Responsibilities

1. **Access Control Management**
   - Design and implement role-based access control (RBAC) strategies
   - Configure security groups and record rules
   - Implement principle of least privilege across all modules
   - Audit user permissions and access rights

2. **Vulnerability Assessment**
   - Perform security code reviews for custom modules
   - Conduct regular vulnerability assessments
   - Implement secure coding practices
   - Monitor and address security advisories from Odoo

3. **Data Protection**
   - Implement data encryption strategies
   - Configure database security controls
   - Establish data masking for sensitive information
   - Design and implement backup security measures

4. **Compliance Management**
   - Ensure GDPR, CCPA, or other regulatory compliance
   - Implement audit trails and logging mechanisms
   - Create documentation for security controls
   - Support compliance audits with evidence collection

## Technical Expertise

### Access Control Implementation

#### Security Groups Configuration
```xml
<!-- security/security.xml -->
<odoo>
    <data>
        <!-- Define security groups -->
        <record id="group_sensitive_data_manager" model="res.groups">
            <field name="name">Sensitive Data Manager</field>
            <field name="category_id" ref="base.module_category_sales_sales"/>
            <field name="implied_ids" eval="[(4, ref('sales_team.group_sale_manager'))]"/>
            <field name="users" eval="[(4, ref('base.user_admin'))]"/>
            <field name="comment">Users in this group have access to sensitive customer data and encryption keys.</field>
        </record>
    </data>

    <!-- Menu items visibility -->
    <menuitem id="menu_security_sensitive" name="Sensitive Data"
              parent="crm.menu_crm_config" sequence="20"
              groups="group_sensitive_data_manager"/>
</odoo>
```

#### Record Rules for Data Segmentation
```xml
<!-- security/ir_rule.xml -->
<odoo>
    <data noupdate="1">
        <!-- Multi-company data separation -->
        <record id="rule_account_invoice_company" model="ir.rule">
            <field name="name">Invoice: Multi-company rule</field>
            <field name="model_id" ref="model_account_invoice"/>
            <field name="global" eval="True"/>
            <field name="domain_force">['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]</field>
        </record>

        <!-- Department-based access restriction -->
        <record id="rule_department_documents" model="ir.rule">
            <field name="name">Documents: Department access only</field>
            <field name="model_id" ref="model_documents_document"/>
            <field name="groups" eval="[(4, ref('documents.group_documents_user'))]"/>
            <field name="domain_force">['|', ('department_id', '=', False), ('department_id', 'in', user.department_ids.ids)]</field>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="True"/>
        </record>
    </data>
</odoo>
```

#### Model Access Rights
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sensitive_data_user,sensitive.data.user,model_sensitive_data,base.group_user,1,0,0,0
access_sensitive_data_manager,sensitive.data.manager,model_sensitive_data,group_sensitive_data_manager,1,1,1,1
```

### Secure Field Configuration

#### Sensitive Data Handling
```python
from odoo import models, fields, api, _
from odoo.exceptions import AccessError
import logging
import hashlib

_logger = logging.getLogger(__name__)

class SensitiveData(models.Model):
    _name = 'sensitive.data'
    _description = 'Sensitive Data Storage'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    
    # Sensitive fields with proper protection
    personal_id_number = fields.Char(
        string='Personal ID',
        groups="group_sensitive_data_manager",
        tracking=True
    )
    
    # Encrypted field (using custom encryption)
    credit_card_encrypted = fields.Char(
        string='Credit Card (Encrypted)',
        copy=False,
        readonly=True
    )
    
    # Temporary field for input that never gets stored
    credit_card_input = fields.Char(
        string='Credit Card Number',
        copy=False,
        store=False
    )
    
    # Field to store just the last 4 digits
    credit_card_last4 = fields.Char(
        string='Credit Card (Last 4)',
        size=4,
        readonly=True
    )
    
    @api.model
    def _hash_sensitive_data(self, value, salt=None):
        """Hash sensitive data with salt for secure storage"""
        if not value:
            return False
        if not salt:
            salt = self.env['ir.config_parameter'].sudo().get_param('database.secret')
        return hashlib.sha256((value + salt).encode()).hexdigest()
    
    @api.onchange('credit_card_input')
    def _onchange_credit_card(self):
        """Process credit card data securely"""
        if self.credit_card_input:
            # Store just last 4 digits for reference
            self.credit_card_last4 = self.credit_card_input[-4:] if len(self.credit_card_input) >= 4 else ''
            
            # In production, use a proper encryption service
            # This is just a demonstration - never encrypt sensitive data this way
            secret_key = self.env['ir.config_parameter'].sudo().get_param('database.secret')
            self.credit_card_encrypted = self._hash_sensitive_data(self.credit_card_input, secret_key)
            
            # Clear the input field immediately
            self.credit_card_input = False
    
    def unlink(self):
        """Override unlink to prevent deletion of sensitive records"""
        for record in self:
            if not self.env.user.has_group('group_sensitive_data_manager'):
                raise AccessError(_("You don't have permission to delete sensitive data records"))
        return super(SensitiveData, self).unlink()
    
    @api.model
    def _secure_log_activity(self, msg, user_id=None):
        """Log security-related activities"""
        if not user_id:
            user_id = self.env.user.id
            
        self.env['mail.activity'].create({
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'note': _('Security Alert: %s') % msg,
            'user_id': user_id,
            'res_id': self.id,
            'res_model_id': self.env['ir.model']._get(self._name).id,
        })
        _logger.info('Security alert for %s (ID: %s): %s', self._name, self.id, msg)
```

### Authentication Security

#### Secure Authentication Configuration
```python
# settings/security_settings.py
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    # 2FA settings
    enable_2fa = fields.Boolean(
        string="Enable Two-Factor Authentication",
        config_parameter='auth.enable_2fa'
    )
    
    minimum_password_length = fields.Integer(
        string="Minimum Password Length",
        config_parameter='auth.min_password_length',
        default=10
    )
    
    password_complexity_required = fields.Boolean(
        string="Require Complex Passwords",
        config_parameter='auth.password_complexity_required',
        default=True
    )
    
    max_login_attempts = fields.Integer(
        string="Maximum Failed Login Attempts",
        config_parameter='auth.max_login_attempts',
        default=5
    )
    
    session_timeout_minutes = fields.Integer(
        string="Session Timeout (minutes)",
        config_parameter='auth.session_timeout',
        default=60
    )
    
    @api.model
    def enforce_password_security(self, password):
        """Enforce password security requirements"""
        min_length = int(self.env['ir.config_parameter'].sudo().get_param('auth.min_password_length', '10'))
        complexity_required = self.env['ir.config_parameter'].sudo().get_param('auth.password_complexity_required', 'True') == 'True'
        
        if len(password) < min_length:
            return {'success': False, 'message': f'Password must be at least {min_length} characters long'}
            
        if complexity_required:
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(not c.isalnum() for c in password)
            
            if not (has_upper and has_lower and has_digit and has_special):
                return {
                    'success': False,
                    'message': 'Password must include uppercase, lowercase, numbers, and special characters'
                }
                
        return {'success': True}
```

#### Session Security Implementation
```python
# controllers/session_security.py
from odoo import http
from odoo.http import request
import datetime

class SessionSecurityController(http.Controller):
    @http.route('/web/session/check', type='json', auth="user")
    def check_session(self):
        """Check if session has expired based on inactivity"""
        session = request.session
        if not session.uid:
            return {'valid': False, 'reason': 'no_user'}
            
        # Get timeout setting
        timeout_minutes = int(request.env['ir.config_parameter'].sudo().get_param('auth.session_timeout', '60'))
        
        # Check last activity timestamp
        last_activity = session.get('last_activity')
        if not last_activity:
            session['last_activity'] = datetime.datetime.now().isoformat()
            return {'valid': True}
            
        last_time = datetime.datetime.fromisoformat(last_activity)
        current_time = datetime.datetime.now()
        elapsed = (current_time - last_time).total_seconds() / 60
        
        if elapsed > timeout_minutes:
            return {'valid': False, 'reason': 'timeout', 'elapsed': elapsed, 'timeout': timeout_minutes}
            
        # Update timestamp for valid session
        session['last_activity'] = current_time.isoformat()
        return {'valid': True}
```

### Security Audit and Compliance

#### Security Audit Log
```python
# models/security_audit_log.py
from odoo import models, fields, api, _
import json

class SecurityAuditLog(models.Model):
    _name = 'security.audit.log'
    _description = 'Security Audit Log'
    _order = 'timestamp DESC'
    
    name = fields.Char(compute='_compute_name', store=True)
    timestamp = fields.Datetime(default=fields.Datetime.now, index=True)
    user_id = fields.Many2one('res.users', string='User', required=True, index=True)
    event_type = fields.Selection([
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('login_failed', 'Failed Login'),
        ('data_access', 'Sensitive Data Access'),
        ('data_export', 'Data Export'),
        ('settings_change', 'Security Settings Change'),
        ('permission_change', 'Permission Change'),
        ('api_access', 'API Access'),
        ('other', 'Other Security Event')
    ], required=True, index=True)
    
    ip_address = fields.Char(string='IP Address')
    user_agent = fields.Char(string='User Agent')
    resource_model = fields.Char(string='Resource Model')
    resource_id = fields.Integer(string='Resource ID')
    details = fields.Text(string='Event Details')
    
    @api.depends('event_type', 'user_id', 'timestamp')
    def _compute_name(self):
        for log in self:
            log.name = f"{log.event_type} - {log.user_id.name} - {log.timestamp}"
    
    @api.model
    def log_security_event(self, event_type, details=None, resource_model=None, resource_id=None):
        """Create security audit log entry"""
        http_request = self.env['ir.http'].get_request()
        ip_address = http_request.httprequest.remote_addr if http_request else False
        user_agent = http_request.httprequest.user_agent.string if http_request and http_request.httprequest.user_agent else False
        
        if isinstance(details, dict):
            details = json.dumps(details)
            
        return self.create({
            'user_id': self.env.user.id,
            'event_type': event_type,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'resource_model': resource_model,
            'resource_id': resource_id,
            'details': details
        })
    
    def unlink(self):
        """Prevent deletion of audit logs"""
        raise models.AccessError(_("Audit logs cannot be deleted for compliance reasons"))
```

#### GDPR Compliance Tools
```python
# models/gdpr_tools.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json
import csv
import io
import base64

_logger = logging.getLogger(__name__)

class GDPRDataRequest(models.Model):
    _name = 'gdpr.data.request'
    _description = 'GDPR Data Subject Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner', string='Data Subject', required=True)
    request_type = fields.Selection([
        ('access', 'Right to Access'),
        ('rectification', 'Right to Rectification'),
        ('erasure', 'Right to Erasure (Forget)'),
        ('restriction', 'Right to Restrict Processing'),
        ('portability', 'Right to Data Portability'),
        ('objection', 'Right to Object')
    ], required=True)
    
    request_date = fields.Date(default=fields.Date.today, required=True)
    completion_deadline = fields.Date(compute='_compute_deadline')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True)
    
    response_details = fields.Text('Response Details')
    data_output = fields.Binary('Data Output', attachment=True)
    data_output_filename = fields.Char('Output Filename')
    
    @api.depends('request_date')
    def _compute_deadline(self):
        for request in self:
            # GDPR requires response within 30 days
            if request.request_date:
                request.completion_deadline = fields.Date.add(request.request_date, days=30)
            else:
                request.completion_deadline = False
    
    def action_submit(self):
        self.write({'state': 'submitted'})
        # Log submission in audit log
        self.env['security.audit.log'].log_security_event(
            'data_access', 
            details=f"GDPR request submitted: {self.request_type}", 
            resource_model=self._name, 
            resource_id=self.id
        )
    
    def action_process(self):
        self.write({'state': 'in_progress'})
        return True
        
    def action_generate_data_export(self):
        """Generate data export for data subject"""
        self.ensure_one()
        if self.request_type not in ['access', 'portability']:
            raise UserError(_("Data export is only available for Access or Portability requests"))
            
        partner = self.partner_id
        export_data = {
            'data_subject': {
                'id': partner.id,
                'name': partner.name,
                'email': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'street': partner.street,
                'city': partner.city,
                'zip': partner.zip,
                'country': partner.country_id.name if partner.country_id else None,
            },
            'contacts': [],
            'opportunities': [],
            'invoices': [],
            'activities': []
        }
        
        # Add related contacts
        contacts = self.env['res.partner'].search([
            '|', ('parent_id', '=', partner.id), ('id', 'child_of', partner.id)
        ])
        for contact in contacts:
            export_data['contacts'].append({
                'id': contact.id,
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone
            })
        
        # Add CRM opportunities
        if 'crm.lead' in self.env:
            leads = self.env['crm.lead'].search([('partner_id', '=', partner.id)])
            for lead in leads:
                export_data['opportunities'].append({
                    'id': lead.id,
                    'name': lead.name,
                    'expected_revenue': lead.expected_revenue,
                    'stage': lead.stage_id.name if lead.stage_id else None,
                    'creation_date': str(lead.create_date),
                })
        
        # Add invoices
        if 'account.move' in self.env:
            invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', 'in', ['out_invoice', 'out_refund'])
            ])
            for inv in invoices:
                export_data['invoices'].append({
                    'id': inv.id,
                    'name': inv.name,
                    'date': str(inv.date),
                    'amount': inv.amount_total,
                    'state': inv.state
                })
                
        # Output to JSON file
        json_data = json.dumps(export_data, indent=2)
        
        # Create file output
        self.write({
            'data_output': base64.b64encode(json_data.encode('utf-8')),
            'data_output_filename': f'gdpr_data_export_{partner.id}.json'
        })
        
        # Log in audit trail
        self.env['security.audit.log'].log_security_event(
            'data_export', 
            details=f"GDPR data export generated for partner ID {partner.id}", 
            resource_model=self._name, 
            resource_id=self.id
        )
        
        return True
        
    def action_complete_erasure(self):
        """Execute right to erasure (be forgotten)"""
        self.ensure_one()
        if self.request_type != 'erasure':
            raise UserError(_("This action is only for Right to Erasure requests"))
            
        partner = self.partner_id
        # Before erasing, create audit log
        self.env['security.audit.log'].log_security_event(
            'data_access', 
            details=f"GDPR erasure request executed for partner ID {partner.id}", 
            resource_model='res.partner', 
            resource_id=partner.id
        )
        
        # Anonymize data rather than delete to maintain referential integrity
        anonymized_email = f"anonymized-{partner.id}@gdpr.anonymized"
        anonymized_name = f"Anonymized-{partner.id}"
        
        # Update the partner record
        partner.write({
            'name': anonymized_name,
            'email': anonymized_email,
            'phone': False,
            'mobile': False,
            'street': False,
            'street2': False,
            'city': False,
            'zip': False,
            'vat': False,
            'website': False,
            'comment': "This record has been anonymized following a GDPR erasure request",
            'active': False,  # Archive the record
        })
        
        # Mark the request as completed
        self.write({
            'state': 'completed',
            'response_details': f"Data erasure completed on {fields.Date.today()}. Personal data has been anonymized."
        })
        
        return True
```

### API Security

#### API Security Implementation
```python
# controllers/api_security.py
from odoo import http, _
from odoo.http import request
import logging
import uuid
import json
from datetime import datetime, timedelta
from werkzeug.exceptions import Unauthorized, BadRequest, Forbidden

_logger = logging.getLogger(__name__)

class APISecurityController(http.Controller):
    @http.route('/api/v1/security/token', type='json', auth='public', methods=['POST'], csrf=False)
    def get_api_token(self, **kwargs):
        """Secure token generation endpoint"""
        data = json.loads(request.httprequest.data.decode('utf-8'))
        if not data.get('api_key') or not data.get('api_secret'):
            raise BadRequest("Missing credentials")
            
        api_key = data.get('api_key')
        api_secret = data.get('api_secret')
        
        # Find API key record
        api_key_record = request.env['api.key'].sudo().search([
            ('key', '=', api_key),
            ('active', '=', True)
        ], limit=1)
        
        if not api_key_record or not api_key_record.check_secret(api_secret):
            # Log failed attempt
            request.env['security.audit.log'].sudo().log_security_event(
                'login_failed', 
                details="Failed API authentication attempt"
            )
            raise Unauthorized("Invalid credentials")
            
        # Check rate limiting
        if not self._check_rate_limit(api_key_record):
            raise Forbidden("Rate limit exceeded")
            
        # Generate token
        expiration = datetime.now() + timedelta(hours=api_key_record.token_expiry_hours)
        token = str(uuid.uuid4())
        
        # Store token
        token_record = request.env['api.access.token'].sudo().create({
            'api_key_id': api_key_record.id,
            'token': token,
            'expiration': expiration,
            'ip_address': request.httprequest.remote_addr,
        })
        
        # Log successful token creation
        request.env['security.audit.log'].sudo().log_security_event(
            'api_access', 
            details=f"API token generated for {api_key_record.name}"
        )
        
        return {
            'token': token,
            'expires_at': expiration.isoformat(),
            'scope': api_key_record.scope
        }
        
    def _check_rate_limit(self, api_key_record):
        """Check if rate limit is exceeded"""
        # Count recent token generation attempts
        recent_attempts = request.env['api.access.token'].sudo().search_count([
            ('api_key_id', '=', api_key_record.id),
            ('create_date', '>=', datetime.now() - timedelta(hours=1))
        ])
        
        return recent_attempts < api_key_record.hourly_limit
        
    @http.route('/api/v1/security/verify', type='json', auth='public', methods=['POST'], csrf=False)
    def verify_token(self, **kwargs):
        """Verify token validity"""
        data = json.loads(request.httprequest.data.decode('utf-8'))
        token = data.get('token')
        
        if not token:
            return {'valid': False, 'reason': 'no_token'}
            
        token_record = request.env['api.access.token'].sudo().search([
            ('token', '=', token),
            ('active', '=', True),
            ('expiration', '>=', datetime.now())
        ], limit=1)
        
        if not token_record:
            return {'valid': False, 'reason': 'invalid_token'}
            
        return {
            'valid': True,
            'api_key_name': token_record.api_key_id.name,
            'scope': token_record.api_key_id.scope,
            'expires_at': token_record.expiration.isoformat()
        }
```

#### API Key Management
```python
# models/api_key.py
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import hashlib
import secrets
import logging

_logger = logging.getLogger(__name__)

class APIKey(models.Model):
    _name = 'api.key'
    _description = 'API Key'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(required=True, tracking=True)
    key = fields.Char(required=True, readonly=True, copy=False)
    secret_hash = fields.Char(readonly=True, copy=False)
    active = fields.Boolean(default=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, tracking=True)
    
    scope = fields.Selection([
        ('read', 'Read Only'),
        ('read_write', 'Read and Write'),
        ('full', 'Full Access')
    ], default='read', required=True, tracking=True)
    
    ip_whitelist = fields.Text(
        string='IP Whitelist',
        help='Comma-separated list of allowed IP addresses or CIDR ranges'
    )
    
    token_expiry_hours = fields.Integer(
        string='Token Expiry (Hours)',
        default=24,
        help='Number of hours before API tokens expire'
    )
    
    hourly_limit = fields.Integer(
        string='Hourly Request Limit',
        default=100,
        help='Maximum API requests allowed per hour'
    )
    
    last_used = fields.Datetime(string='Last Used')
    
    _sql_constraints = [
        ('key_uniq', 'unique(key)', 'API Key must be unique!')
    ]
    
    @api.model_create_multi
    def create(self, vals_list):
        """Generate unique API key and secret on creation"""
        for vals in vals_list:
            # Generate API key if not provided
            if not vals.get('key'):
                vals['key'] = self._generate_key()
                
            # Always generate a new secret and hash it
            secret = self._generate_secret()
            vals['secret_hash'] = self._hash_secret(secret)
                
        records = super(APIKey, self).create(vals_list)
        
        # Return secrets alongside the records (only time they're available)
        for record in records:
            record.secret = secret  # Temp attribute, not stored
            
        return records
        
    def _generate_key(self):
        """Generate a unique API key"""
        return f'ak_{secrets.token_hex(16)}'
        
    def _generate_secret(self):
        """Generate API secret"""
        return secrets.token_hex(32)
        
    def _hash_secret(self, secret):
        """Hash API secret for secure storage"""
        salt = self.env['ir.config_parameter'].sudo().get_param('database.secret')
        return hashlib.sha256((secret + salt).encode()).hexdigest()
        
    def check_secret(self, secret):
        """Check if a secret matches the stored hash"""
        hashed = self._hash_secret(secret)
        return hashed == self.secret_hash
        
    def regenerate_secret(self):
        """Regenerate API secret"""
        self.ensure_one()
        secret = self._generate_secret()
        self.write({'secret_hash': self._hash_secret(secret)})
        
        # Log regeneration
        self.env['security.audit.log'].log_security_event(
            'settings_change',
            details=f"API secret regenerated for key {self.key}",
            resource_model=self._name,
            resource_id=self.id
        )
        
        # Return new secret
        return {
            'secret': secret,
            'warning': _("Store this secret safely. It cannot be retrieved later!")
        }

class APIAccessToken(models.Model):
    _name = 'api.access.token'
    _description = 'API Access Token'
    
    token = fields.Char(required=True, readonly=True, copy=False)
    api_key_id = fields.Many2one('api.key', string='API Key', required=True, ondelete='cascade')
    expiration = fields.Datetime(required=True)
    active = fields.Boolean(default=True)
    ip_address = fields.Char('Source IP')
    
    _sql_constraints = [
        ('token_uniq', 'unique(token)', 'API Token must be unique!')
    ]
    
    def cron_cleanup_expired_tokens(self):
        """Cleanup expired tokens"""
        expired_tokens = self.search([
            ('expiration', '<', fields.Datetime.now())
        ])
        expired_tokens.write({'active': False})
        _logger.info("Cleaned up %s expired API tokens", len(expired_tokens))
```

## Security Best Practices for Odoo 18+

### SQL Injection Prevention

#### Secure Query Methods
```python
# models/secure_query_examples.py
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class SecureQueryExamples(models.Model):
    _name = 'secure.query.examples'
    _description = 'Examples of Secure Query Patterns'
    
    @api.model
    def insecure_query_example(self, user_input):
        # DON'T DO THIS - Vulnerable to SQL injection
        query = f"SELECT * FROM res_partner WHERE name LIKE '{user_input}'"
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    
    @api.model
    def secure_query_example(self, user_input):
        # DO THIS - Use parameterized queries
        query = "SELECT * FROM res_partner WHERE name LIKE %s"
        self.env.cr.execute(query, [user_input])
        return self.env.cr.dictfetchall()
    
    @api.model
    def secure_orm_example(self, user_input):
        # PREFERRED - Use ORM whenever possible
        return self.env['res.partner'].search([('name', 'like', user_input)]).read()
    
    @api.model
    def secure_id_lookup(self, record_id):
        # Convert to integer for security
        try:
            safe_id = int(record_id)
        except (ValueError, TypeError):
            _logger.warning("Invalid ID parameter: %s", record_id)
            return False
            
        return self.env['res.partner'].browse(safe_id).exists()
```

### Input Validation

#### Input Validation Helpers
```python
# tools/input_validators.py
import re
from odoo import _
from odoo.exceptions import ValidationError

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
        
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError(_("Invalid email format"))
    return True
    
def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return False
        
    # Remove common separators
    clean_phone = re.sub(r'[\s\-\(\)\.]+', '', phone)
    
    # Check if it's a valid format (adjust regex for your country format)
    if not re.match(r'^\+?[0-9]{8,15}$', clean_phone):
        raise ValidationError(_("Invalid phone number format"))
    return True
    
def sanitize_text(text):
    """Basic text sanitization"""
    if not text:
        return ""
        
    # Remove potentially dangerous content
    sanitized = re.sub(r'[<>]', '', text)
    return sanitized
    
def validate_url(url):
    """Validate URL format"""
    if not url:
        return False
        
    pattern = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    if not re.match(pattern, url):
        raise ValidationError(_("Invalid URL format. URLs must start with http:// or https://"))
    return True
```

### Cross-Site Scripting (XSS) Prevention

#### Controller with XSS Protection
```python
# controllers/secure_controller.py
from odoo import http
from odoo.http import request
from ..tools.input_validators import sanitize_text
import html
import logging

_logger = logging.getLogger(__name__)

class SecureController(http.Controller):
    @http.route('/secure/form', auth='public', website=True)
    def secure_form(self, **kw):
        return request.render('security_module.secure_form_template', {})
        
    @http.route('/secure/form/submit', type='http', auth='public', website=True, methods=['POST'])
    def secure_form_submit(self, **post):
        # Sanitize all input
        safe_data = {}
        for key, value in post.items():
            if isinstance(value, str):
                # Sanitize string inputs
                safe_data[key] = html.escape(sanitize_text(value))
            else:
                safe_data[key] = value
                
        # Log the sanitized submission for security auditing
        _logger.info("Form submitted with sanitized data: %s", safe_data)
        
        # Process the form with sanitized data
        # ...
        
        return request.render('security_module.form_success', {
            'data': safe_data
        })
```

### XML Security Templates

#### Secure Template Example
```xml
<!-- templates/secure_templates.xml -->
<odoo>
    <template id="security_module.secure_form_template">
        <div class="container">
            <form action="/secure/form/submit" method="post" class="o_form">
                <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>
                
                <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" name="name" class="form-control" required="required"
                           t-att-value="name or ''" maxlength="50"/>
                </div>
                
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" name="email" class="form-control" required="required"
                           t-att-value="email or ''" pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"/>
                </div>
                
                <div class="form-group">
                    <label for="message">Message</label>
                    <textarea name="message" class="form-control" rows="4" maxlength="500"
                              t-esc="message or ''"></textarea>
                </div>
                
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
    </template>
    
    <!-- Success template with proper output sanitization -->
    <template id="security_module.form_success">
        <div class="container">
            <div class="alert alert-success">
                Form submitted successfully!
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h3>Submitted Information</h3>
                </div>
                <div class="card-body">
                    <!-- Use t-esc for proper output encoding to prevent XSS -->
                    <p><strong>Name:</strong> <span t-esc="data.get('name')"/></p>
                    <p><strong>Email:</strong> <span t-esc="data.get('email')"/></p>
                    <p><strong>Message:</strong> <span t-esc="data.get('message')"/></p>
                </div>
            </div>
        </div>
    </template>
</odoo>
```

## Security Testing and Auditing

### Automated Security Scanning

#### Security Scan Setup
```python
# tools/security_scanner.py
from odoo import models, fields, api
import logging
import os
import subprocess
import tempfile
import json
import base64

_logger = logging.getLogger(__name__)

class SecurityScan(models.Model):
    _name = 'security.scan'
    _description = 'Security Scanning Results'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'scan_date DESC'
    
    name = fields.Char(compute='_compute_name', store=True)
    scan_date = fields.Datetime(default=fields.Datetime.now)
    module_id = fields.Many2one('ir.module.module', string='Module Scanned')
    scan_type = fields.Selection([
        ('code', 'Code Analysis'),
        ('dependency', 'Dependency Check'),
        ('config', 'Configuration Review')
    ], required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('done', 'Completed'),
        ('failed', 'Failed')
    ], default='draft', tracking=True)
    
    issues_count = fields.Integer('Issues Found', default=0)
    high_severity_count = fields.Integer('High Severity Issues', default=0)
    medium_severity_count = fields.Integer('Medium Severity Issues', default=0)
    low_severity_count = fields.Integer('Low Severity Issues', default=0)
    
    result_summary = fields.Text('Result Summary')
    result_detail = fields.Binary('Detailed Results', attachment=True)
    result_filename = fields.Char('Result Filename')
    
    @api.depends('scan_type', 'module_id', 'scan_date')
    def _compute_name(self):
        for scan in self:
            if scan.module_id:
                scan.name = f"{scan.scan_type} scan - {scan.module_id.name} - {scan.scan_date}"
            else:
                scan.name = f"{scan.scan_type} scan - {scan.scan_date}"
    
    @api.model
    def scan_module_code(self, module_name):
        """Scan module code for security issues"""
        module = self.env['ir.module.module'].search([('name', '=', module_name)], limit=1)
        if not module:
            return {'error': f"Module {module_name} not found"}
            
        # Create scan record
        scan = self.create({
            'module_id': module.id,
            'scan_type': 'code',
            'state': 'running'
        })
        
        try:
            module_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), module_name)
            if not os.path.exists(module_path):
                scan.write({
                    'state': 'failed',
                    'result_summary': f"Module path not found: {module_path}"
                })
                return {'error': f"Module path not found: {module_path}"}
                
            # Run security scan - example using bandit for Python
            with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
                result_file = temp.name
                
            cmd = ['bandit', '-r', module_path, '-f', 'json', '-o', result_file]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode not in [0, 1]:  # Bandit returns 1 when issues are found
                scan.write({
                    'state': 'failed',
                    'result_summary': f"Scan failed: {stderr.decode('utf-8')}"
                })
                return {'error': f"Scan failed: {stderr.decode('utf-8')}"}
                
            # Process results
            with open(result_file, 'r') as f:
                results = json.load(f)
                
            # Count issues by severity
            high_count = 0
            medium_count = 0
            low_count = 0
            for result in results.get('results', []):
                severity = result.get('issue_severity')
                if severity == 'HIGH':
                    high_count += 1
                elif severity == 'MEDIUM':
                    medium_count += 1
                else:
                    low_count += 1
                    
            total_issues = len(results.get('results', []))
            
            # Generate summary
            summary = f"""
            Security scan completed for module {module_name}
            
            Total issues found: {total_issues}
            - High severity: {high_count}
            - Medium severity: {medium_count}
            - Low severity: {low_count}
            
            See detailed report for more information.
            """
            
            # Save results
            with open(result_file, 'rb') as f:
                result_content = f.read()
                
            scan.write({
                'state': 'done',
                'issues_count': total_issues,
                'high_severity_count': high_count,
                'medium_severity_count': medium_count,
                'low_severity_count': low_count,
                'result_summary': summary,
                'result_detail': base64.b64encode(result_content),
                'result_filename': f"security_scan_{module_name}_{fields.Date.today()}.json"
            })
            
            # Cleanup
            os.unlink(result_file)
            
            return {
                'scan_id': scan.id,
                'issues_found': total_issues,
                'summary': summary
            }
            
        except Exception as e:
            _logger.exception("Security scan failed")
            scan.write({
                'state': 'failed',
                'result_summary': f"Error: {str(e)}"
            })
            return {'error': str(e)}
```

### Security Reports

#### Security Dashboard
```xml
<!-- views/security_dashboard.xml -->
<odoo>
    <record id="security_dashboard_view" model="ir.ui.view">
        <field name="name">security.dashboard.view</field>
        <field name="model">ir.actions.act_window</field>
        <field name="arch" type="xml">
            <form string="Security Dashboard" create="false" edit="false">
                <sheet>
                    <div class="oe_title">
                        <h1>Security Dashboard</h1>
                    </div>
                    
                    <div class="row mt16">
                        <div class="col-md-4">
                            <div class="o_stat_info bg-success p-3">
                                <h3>User Security</h3>
                                <div class="row">
                                    <div class="col-6">
                                        <div class="h4">Users</div>
                                        <div class="h3 text-right" t-esc="user_count"/>
                                    </div>
                                    <div class="col-6">
                                        <div class="h4">Admin Users</div>
                                        <div class="h3 text-right" t-esc="admin_count"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-4">
                            <div class="o_stat_info bg-info p-3">
                                <h3>API Security</h3>
                                <div class="row">
                                    <div class="col-6">
                                        <div class="h4">API Keys</div>
                                        <div class="h3 text-right" t-esc="api_key_count"/>
                                    </div>
                                    <div class="col-6">
                                        <div class="h4">Active Tokens</div>
                                        <div class="h3 text-right" t-esc="token_count"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-4">
                            <div class="o_stat_info bg-warning p-3">
                                <h3>Security Incidents</h3>
                                <div class="row">
                                    <div class="col-6">
                                        <div class="h4">Failed Logins</div>
                                        <div class="h3 text-right" t-esc="failed_login_count"/>
                                    </div>
                                    <div class="col-6">
                                        <div class="h4">Total Logs</div>
                                        <div class="h3 text-right" t-esc="log_count"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row mt16">
                        <div class="col-md-6">
                            <h3>Recent Security Logs</h3>
                            <field name="recent_logs"/>
                        </div>
                        <div class="col-md-6">
                            <h3>Security Scan Results</h3>
                            <field name="recent_scans"/>
                        </div>
                    </div>
                    
                    <div class="row mt16">
                        <div class="col-md-12">
                            <h3>Security Action Items</h3>
                            <field name="security_actions"/>
                        </div>
                    </div>
                </sheet>
            </form>
        </field>
    </record>
    
    <record id="security_dashboard_action" model="ir.actions.act_window">
        <field name="name">Security Dashboard</field>
        <field name="res_model">security.dashboard</field>
        <field name="view_mode">form</field>
        <field name="target">main</field>
    </record>
    
    <menuitem id="menu_security_dashboard" 
              name="Security Dashboard" 
              parent="base.menu_administration"
              sequence="1"
              action="security_dashboard_action"
              groups="base.group_system"/>
</odoo>
```

## GDPR Compliance Implementation

### Data Protection Impact Assessment

#### DPIA Implementation
```python
# models/data_protection.py
from odoo import models, fields, api, _

class DataProtectionImpactAssessment(models.Model):
    _name = 'data.protection.impact.assessment'
    _description = 'Data Protection Impact Assessment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(required=True)
    date_performed = fields.Date(default=fields.Date.today)
    responsible_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user.id)
    
    processing_description = fields.Text(string='Processing Description', required=True)
    processing_purpose = fields.Text(string='Purpose of Processing', required=True)
    data_subjects = fields.Many2many('res.groups', string='Data Subjects')
    data_categories = fields.Text(string='Categories of Personal Data', required=True)
    
    # Risk assessment
    has_sensitive_data = fields.Boolean('Contains Sensitive Data')
    has_children_data = fields.Boolean('Contains Children\'s Data')
    has_automated_decisions = fields.Boolean('Involves Automated Decision-Making')
    has_systematic_monitoring = fields.Boolean('Involves Systematic Monitoring')
    has_large_scale_processing = fields.Boolean('Involves Large Scale Processing')
    
    risk_level = fields.Selection([
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('very_high', 'Very High Risk')
    ], compute='_compute_risk_level', store=True)
    
    risk_details = fields.Text('Risk Details')
    mitigation_measures = fields.Text('Mitigation Measures')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True)
    
    @api.depends('has_sensitive_data', 'has_children_data', 'has_automated_decisions', 
                 'has_systematic_monitoring', 'has_large_scale_processing')
    def _compute_risk_level(self):
        for assessment in self:
            # Count risk factors
            risk_count = sum([
                assessment.has_sensitive_data,
                assessment.has_children_data,
                assessment.has_automated_decisions,
                assessment.has_systematic_monitoring,
                assessment.has_large_scale_processing
            ])
            
            # Determine risk level
            if risk_count == 0:
                assessment.risk_level = 'low'
            elif risk_count <= 2:
                assessment.risk_level = 'medium'
            elif risk_count <= 3:
                assessment.risk_level = 'high'
            else:
                assessment.risk_level = 'very_high'
```

## Knowledge Resources

1. **Official Documentation**
   - [Odoo 18 Security Documentation](https://www.odoo.com/documentation/18.0/developer/reference/security.html)
   - [PostgreSQL Security Best Practices](https://www.postgresql.org/docs/current/security.html)
   - [OWASP Top 10 Web Application Security Risks](https://owasp.org/www-project-top-ten/)

2. **Community Resources**
   - [Odoo Security Forum](https://www.odoo.com/forum/help-1/security-53)
   - [OCA Security Tools](https://github.com/OCA/server-tools/tree/18.0/security)
   - [GDPR Compliance Guidelines](https://gdpr.eu/checklist/)

3. **Books and Articles**
   - "Odoo 18 Security Best Practices"
   - "Implementing GDPR in Odoo Applications"
   - "API Security for Odoo Developers"

---

This role documentation serves as a comprehensive guide for Security Experts working with the Neodoo18Framework and Odoo 18+ applications. It covers all aspects of securing Odoo applications, from access control to API security, GDPR compliance, and security testing.