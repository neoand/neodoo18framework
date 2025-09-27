# Integration Specialist Role for Odoo 18

## Role Description

The Integration Specialist role is responsible for connecting Odoo 18+ with external systems, developing APIs, and implementing data synchronization solutions. This role requires deep knowledge of Odoo's API architecture, authentication mechanisms, and integration patterns to build robust and secure connections between systems.

## Key Responsibilities

- Design and implement REST APIs following Odoo 18+ standards
- Create webhooks and callback systems for real-time integrations
- Develop connectors with third-party services and platforms
- Implement secure authentication mechanisms for external systems
- Design efficient data synchronization flows and scheduling
- Ensure error handling and recovery mechanisms in integrations
- Document API endpoints and integration specifications

## Technical Knowledge

### Odoo API Architecture

Understanding of Odoo 18's API structure and access patterns:

```python
# External API (JSON-RPC)
import json
import urllib.request

def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    req = urllib.request.Request(
        url=url,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    response = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    if response.get("error"):
        raise Exception(response["error"])
    return response["result"]

def authenticate(url, db, login, password):
    return json_rpc(url, "call", {
        "service": "common",
        "method": "authenticate",
        "args": [db, login, password, {}]
    })

# Example usage
url = "https://my-odoo-server/jsonrpc"
db = "database_name"
login = "user@example.com"
password = "password"

uid = authenticate(url, db, login, password)
partners = json_rpc(url, "call", {
    "service": "object",
    "method": "execute_kw",
    "args": [db, uid, password, "res.partner", "search_read", 
            [[["is_company", "=", True]]], {"fields": ["name", "country_id", "comment"]}]
})
```

### RESTful API Development

```python
from odoo import http
from odoo.http import request
import json

class ProductAPI(http.Controller):
    @http.route('/api/v1/products', auth='api_key', type='http', methods=['GET'], csrf=False)
    def get_products(self, **kwargs):
        """
        @api {get} /api/v1/products Get Products
        @apiName GetProducts
        @apiGroup Products
        @apiParam {Number} [limit=20] Number of products to return
        @apiParam {Number} [offset=0] Offset for pagination
        @apiParam {String} [query] Search query to filter products
        @apiSuccess {Object[]} products List of products
        """
        try:
            limit = int(kwargs.get('limit', 20))
            offset = int(kwargs.get('offset', 0))
            query = kwargs.get('query')
            
            domain = []
            if query:
                domain = [('name', 'ilike', query)]
                
            products = request.env['product.product'].sudo().search_read(
                domain=domain,
                fields=['id', 'name', 'default_code', 'list_price', 'qty_available'],
                limit=limit,
                offset=offset
            )
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'count': len(products),
                    'data': products
                }),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'error': str(e)
                }),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
    
    @http.route('/api/v1/products', auth='api_key', type='json', methods=['POST'], csrf=False)
    def create_product(self, **kwargs):
        """
        @api {post} /api/v1/products Create Product
        @apiName CreateProduct
        @apiGroup Products
        @apiParam {String} name Product name
        @apiParam {String} [default_code] Internal reference
        @apiParam {Number} list_price Sales price
        @apiSuccess {Object} product Created product data
        """
        try:
            required_fields = ['name', 'list_price']
            for field in required_fields:
                if field not in request.jsonrequest:
                    return {
                        'success': False,
                        'error': f"Missing required field: {field}"
                    }, 400
                    
            vals = {
                'name': request.jsonrequest.get('name'),
                'default_code': request.jsonrequest.get('default_code'),
                'list_price': request.jsonrequest.get('list_price'),
            }
            
            product = request.env['product.product'].sudo().create(vals)
            
            return {
                'success': True,
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'default_code': product.default_code,
                    'list_price': product.list_price,
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500
```

### Authentication Systems

```python
# API Key Authentication System
from odoo import api, models, fields
from odoo.http import request
from odoo.exceptions import AccessDenied
import secrets
import hmac
import hashlib

class APIKey(models.Model):
    _name = 'api.key'
    _description = 'API Key'
    
    name = fields.Char(string='Name', required=True)
    key = fields.Char(string='API Key', required=True, copy=False, default=lambda self: secrets.token_hex(16))
    secret = fields.Char(string='API Secret', required=True, copy=False, default=lambda self: secrets.token_hex(32))
    user_id = fields.Many2one('res.users', string='User', required=True)
    active = fields.Boolean(default=True)
    
    # For additional security - restrict API access by IP
    allowed_ips = fields.Char(string='Allowed IPs', help="Comma-separated list of allowed IPs")
    
    _sql_constraints = [
        ('key_uniq', 'unique(key)', 'API Key must be unique!')
    ]
    
    @api.model
    def authenticate(self, key, signature, timestamp, nonce):
        """Authenticate an API request using HMAC authentication"""
        api_key = self.search([('key', '=', key), ('active', '=', True)], limit=1)
        
        if not api_key:
            raise AccessDenied()
            
        # Check IP restrictions if defined
        if api_key.allowed_ips:
            client_ip = request.httprequest.remote_addr
            allowed_ips = [ip.strip() for ip in api_key.allowed_ips.split(',')]
            if client_ip not in allowed_ips:
                raise AccessDenied("IP address not allowed")
        
        # Verify signature
        message = f"{key}{timestamp}{nonce}"
        expected_signature = hmac.new(
            api_key.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            raise AccessDenied()
            
        # Update request environment with authenticated user
        request.update_env(user=api_key.user_id.id)
        return api_key.user_id.id
```

### Webhook Implementation

```python
from odoo import api, models, fields
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class WebhookEndpoint(models.Model):
    _name = 'webhook.endpoint'
    _description = 'Webhook Endpoint'
    
    name = fields.Char(required=True)
    url = fields.Char(string='Endpoint URL', required=True)
    is_active = fields.Boolean(default=True)
    secret_token = fields.Char(string='Secret Token', copy=False)
    event_ids = fields.Many2many('webhook.event', string='Events')
    retry_count = fields.Integer(default=3)
    
    def notify(self, event_type, payload):
        """Send webhook notification for the specified event"""
        if not self.is_active:
            return False
            
        if self.event_ids and not self.event_ids.filtered(lambda e: e.code == event_type):
            return False
            
        headers = {
            'Content-Type': 'application/json',
            'X-Odoo-Webhook-Event': event_type
        }
        
        if self.secret_token:
            # Add signature for security
            payload_str = json.dumps(payload)
            signature = hmac.new(
                self.secret_token.encode(),
                payload_str.encode(),
                hashlib.sha256
            ).hexdigest()
            headers['X-Odoo-Webhook-Signature'] = signature
        
        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=10
            )
            if response.status_code >= 200 and response.status_code < 300:
                _logger.info(f"Webhook delivered successfully: {self.name}")
                return True
            else:
                _logger.warning(f"Webhook delivery failed: {self.name}, status: {response.status_code}")
                return False
        except Exception as e:
            _logger.error(f"Webhook delivery error: {self.name}, error: {str(e)}")
            return False
```

### Synchronization Framework

```python
from odoo import api, models, fields
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class SyncTask(models.Model):
    _name = 'sync.task'
    _description = 'Synchronization Task'
    
    name = fields.Char(required=True)
    model_id = fields.Many2one('ir.model', string='Model', required=True)
    external_system = fields.Selection([
        ('shopify', 'Shopify'),
        ('woocommerce', 'WooCommerce'),
        ('salesforce', 'Salesforce'),
        ('custom_api', 'Custom API')
    ], string='External System', required=True)
    
    # Sync configuration
    sync_direction = fields.Selection([
        ('import', 'Import to Odoo'),
        ('export', 'Export from Odoo'),
        ('bidirectional', 'Bidirectional')
    ], default='import', required=True)
    
    interval_number = fields.Integer(default=1)
    interval_type = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')
    ], string='Interval Unit', default='hours')
    
    next_run = fields.Datetime(string='Next Run', compute='_compute_next_run')
    last_run = fields.Datetime(string='Last Sync')
    last_sync_status = fields.Selection([
        ('success', 'Success'),
        ('partial', 'Partial Success'),
        ('failed', 'Failed')
    ], string='Last Status')
    
    # Advanced options
    batch_size = fields.Integer(default=50, help="Number of records to process in each batch")
    mapping_id = fields.Many2one('sync.mapping', string='Field Mapping')
    
    @api.depends('last_run', 'interval_number', 'interval_type')
    def _compute_next_run(self):
        for task in self:
            if not task.last_run:
                task.next_run = fields.Datetime.now()
                continue
                
            if task.interval_type == 'minutes':
                next_run = task.last_run + timedelta(minutes=task.interval_number)
            elif task.interval_type == 'hours':
                next_run = task.last_run + timedelta(hours=task.interval_number)
            elif task.interval_type == 'days':
                next_run = task.last_run + timedelta(days=task.interval_number)
            elif task.interval_type == 'weeks':
                next_run = task.last_run + timedelta(weeks=task.interval_number)
            elif task.interval_type == 'months':
                # Approximate months as 30 days
                next_run = task.last_run + timedelta(days=30*task.interval_number)
            else:
                next_run = task.last_run + timedelta(hours=1)
                
            task.next_run = next_run
    
    def run_sync(self):
        """Execute the synchronization task"""
        self.ensure_one()
        
        start_time = fields.Datetime.now()
        model = self.env[self.model_id.model]
        
        try:
            # Get the appropriate sync handler for the external system
            if self.external_system == 'shopify':
                handler = self.env['sync.handler.shopify']
            elif self.external_system == 'woocommerce':
                handler = self.env['sync.handler.woocommerce']
            # ... other handlers
            else:
                raise ValueError(f"Unsupported external system: {self.external_system}")
            
            if self.sync_direction == 'import':
                result = handler.import_data(self)
            elif self.sync_direction == 'export':
                result = handler.export_data(self)
            else:  # bidirectional
                import_result = handler.import_data(self)
                export_result = handler.export_data(self)
                result = {
                    'status': 'success' if import_result['status'] == 'success' and export_result['status'] == 'success' else 'partial',
                    'records_processed': import_result['records_processed'] + export_result['records_processed'],
                    'records_success': import_result['records_success'] + export_result['records_success'],
                    'records_failed': import_result['records_failed'] + export_result['records_failed'],
                }
            
            self.write({
                'last_run': start_time,
                'last_sync_status': result['status']
            })
            
            self.env['sync.log'].create({
                'task_id': self.id,
                'date': start_time,
                'duration': (fields.Datetime.now() - start_time).total_seconds(),
                'status': result['status'],
                'records_processed': result.get('records_processed', 0),
                'records_success': result.get('records_success', 0),
                'records_failed': result.get('records_failed', 0),
                'log': result.get('log', '')
            })
            
            return result
            
        except Exception as e:
            _logger.error(f"Sync error for task {self.name}: {str(e)}")
            
            self.write({
                'last_run': start_time,
                'last_sync_status': 'failed'
            })
            
            self.env['sync.log'].create({
                'task_id': self.id,
                'date': start_time,
                'duration': (fields.Datetime.now() - start_time).total_seconds(),
                'status': 'failed',
                'log': str(e)
            })
            
            return {
                'status': 'failed',
                'error': str(e)
            }
```

## Best Practices

### API Design

1. **Versioning**
   - Always version your APIs (e.g., `/api/v1/resources`)
   - Plan for backward compatibility
   - Document breaking changes between versions

2. **Consistent Response Format**
   ```json
   {
     "success": true,
     "data": [...],
     "meta": {
       "page": 1,
       "per_page": 20,
       "total": 145
     }
   }
   ```

3. **HTTP Status Codes**
   - Use appropriate status codes (200, 201, 400, 401, 403, 404, 500)
   - Include detailed error messages in responses
   - Return validation errors with field references

4. **Rate Limiting**
   - Implement rate limiting for API endpoints
   - Include rate limit headers in responses
   - Document rate limit policies

### Security Considerations

1. **Authentication**
   - Use OAuth 2.0 or API keys for authentication
   - Implement token expiration and renewal
   - Store credentials securely

2. **Request Validation**
   - Validate all input parameters
   - Implement request throttling
   - Check for SQL injection and XSS attacks

3. **Data Protection**
   - Encrypt sensitive data in transit (HTTPS)
   - Implement field-level access control
   - Log API access for auditing

### Integration Architecture

1. **Synchronization Patterns**
   - Use webhooks for real-time updates
   - Implement polling for systems without webhook support
   - Consider message queues for asynchronous processing

2. **Error Handling**
   - Implement retry mechanisms with exponential backoff
   - Create detailed error logs
   - Set up monitoring and alerting

3. **Data Consistency**
   - Use idempotent operations where possible
   - Implement transaction management
   - Consider eventual consistency for large datasets

## Critical Anti-Patterns

❌ **Avoid these practices:**
- Exposing internal IDs or sensitive information in APIs
- Lacking proper authentication and authorization
- Implementing non-standard API patterns
- Ignoring rate limiting and DoS protection
- Creating tight coupling between systems
- Missing error handling and recovery mechanisms

## Resources & References

- [Odoo 18 External API Documentation](https://www.odoo.com/documentation/18.0/developer/reference/external_api.html)
- [REST API Best Practices](https://restfulapi.net/)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [Webhook Security Best Practices](https://www.apisec.ai/blog/webhook-security-best-practices)