# Integracoes com APIs Externas no Odoo 18

## Indice

1. [Introducao](#introducao)
2. [Chamadas a APIs REST](#chamadas-a-apis-rest)
3. [Autenticacao](#autenticacao)
4. [Handling de Responses e Errors](#handling-de-responses-e-errors)
5. [Retry Logic](#retry-logic)
6. [Webhooks](#webhooks)
7. [Queue Systems](#queue-systems)
8. [Logging e Monitoring](#logging-e-monitoring)
9. [Exemplos Praticos](#exemplos-praticos)
10. [Security Best Practices](#security-best-practices)
11. [Testing Integrations](#testing-integrations)

---

## Introducao

Integracoes com APIs externas sao comuns em projetos Odoo, permitindo conectar com:
- Payment Gateways (Stripe, PayPal, MercadoPago)
- Shipping APIs (FedEx, UPS, Correios)
- CRM/Marketing (Salesforce, HubSpot, Mailchimp)
- Accounting (QuickBooks, Xero)
- E-commerce (Shopify, WooCommerce, Magento)
- ERPs externos
- Servicos de terceiros (SMS, WhatsApp, etc)

### Biblioteca Principal: `requests`

O Odoo usa a biblioteca `requests` do Python para chamadas HTTP.

```python
import requests
import json
import logging

_logger = logging.getLogger(__name__)
```

---

## Chamadas a APIs REST

### 1. GET Request Basico

```python
from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ExternalAPIConnector(models.Model):
    _name = 'external.api.connector'
    _description = 'External API Connector'

    name = fields.Char('Name', required=True)
    base_url = fields.Char('Base URL', required=True)
    api_key = fields.Char('API Key')
    timeout = fields.Integer('Timeout (seconds)', default=30)

    def _make_get_request(self, endpoint, params=None):
        """
        Faz requisicao GET para API externa

        Args:
            endpoint (str): Endpoint da API (ex: '/users')
            params (dict): Query parameters

        Returns:
            dict: Response data

        Raises:
            UserError: Em caso de erro na requisicao
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Odoo/18.0',
        }

        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        try:
            _logger.info("GET request to %s with params: %s", url, params)

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            # Raise exception para status codes 4xx e 5xx
            response.raise_for_status()

            data = response.json()
            _logger.info("GET request successful. Response: %s", data)

            return data

        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {self.timeout} seconds"
            _logger.error(error_msg)
            raise UserError(error_msg)

        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: {str(e)}"
            _logger.error(error_msg)
            raise UserError(error_msg)

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {response.status_code}: {response.text}"
            _logger.error(error_msg)
            raise UserError(error_msg)

        except ValueError as e:
            error_msg = f"Invalid JSON response: {str(e)}"
            _logger.error(error_msg)
            raise UserError(error_msg)

    def action_test_connection(self):
        """Testa conexao com a API"""
        self.ensure_one()

        try:
            # Endpoint de teste (ajustar conforme API)
            result = self._make_get_request('/ping')

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Connection Successful',
                    'message': 'Successfully connected to external API',
                    'type': 'success',
                    'sticky': False,
                }
            }

        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Connection Failed',
                    'message': str(e),
                    'type': 'danger',
                    'sticky': True,
                }
            }
```

### 2. POST Request (Criar Recursos)

```python
def _make_post_request(self, endpoint, data=None, json_data=None):
    """
    Faz requisicao POST para API externa

    Args:
        endpoint (str): Endpoint da API
        data (dict): Form data
        json_data (dict): JSON data

    Returns:
        dict: Response data
    """
    url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Odoo/18.0',
    }

    if self.api_key:
        headers['Authorization'] = f'Bearer {self.api_key}'

    # Se enviando JSON, adicionar content-type
    if json_data:
        headers['Content-Type'] = 'application/json'

    try:
        _logger.info("POST request to %s", url)
        _logger.debug("POST data: %s", json_data or data)

        response = requests.post(
            url,
            data=data,
            json=json_data,
            headers=headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        # Algumas APIs retornam 201 Created ou 204 No Content
        if response.status_code == 204:
            return {'success': True}

        data = response.json()
        _logger.info("POST request successful")

        return data

    except requests.exceptions.RequestException as e:
        self._handle_request_exception(e, response if 'response' in locals() else None)

def _handle_request_exception(self, exception, response=None):
    """Trata excecoes de requests de forma centralizada"""
    if isinstance(exception, requests.exceptions.Timeout):
        error_msg = f"Request timeout after {self.timeout} seconds"
    elif isinstance(exception, requests.exceptions.ConnectionError):
        error_msg = f"Connection error: {str(exception)}"
    elif isinstance(exception, requests.exceptions.HTTPError):
        if response:
            try:
                error_data = response.json()
                error_msg = f"HTTP {response.status_code}: {error_data.get('message', response.text)}"
            except:
                error_msg = f"HTTP {response.status_code}: {response.text}"
        else:
            error_msg = str(exception)
    else:
        error_msg = f"Request failed: {str(exception)}"

    _logger.error(error_msg)
    raise UserError(error_msg)
```

### 3. PUT Request (Atualizar Recursos)

```python
def _make_put_request(self, endpoint, json_data=None):
    """
    Faz requisicao PUT para API externa

    Args:
        endpoint (str): Endpoint da API
        json_data (dict): JSON data

    Returns:
        dict: Response data
    """
    url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Odoo/18.0',
    }

    if self.api_key:
        headers['Authorization'] = f'Bearer {self.api_key}'

    try:
        _logger.info("PUT request to %s", url)

        response = requests.put(
            url,
            json=json_data,
            headers=headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        if response.status_code == 204:
            return {'success': True}

        return response.json()

    except requests.exceptions.RequestException as e:
        self._handle_request_exception(e, response if 'response' in locals() else None)
```

### 4. DELETE Request

```python
def _make_delete_request(self, endpoint):
    """
    Faz requisicao DELETE para API externa

    Args:
        endpoint (str): Endpoint da API

    Returns:
        dict: Response data
    """
    url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Odoo/18.0',
    }

    if self.api_key:
        headers['Authorization'] = f'Bearer {self.api_key}'

    try:
        _logger.info("DELETE request to %s", url)

        response = requests.delete(
            url,
            headers=headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        if response.status_code == 204:
            return {'success': True}

        return response.json()

    except requests.exceptions.RequestException as e:
        self._handle_request_exception(e, response if 'response' in locals() else None)
```

### 5. PATCH Request (Atualizar Parcial)

```python
def _make_patch_request(self, endpoint, json_data=None):
    """
    Faz requisicao PATCH para API externa

    Args:
        endpoint (str): Endpoint da API
        json_data (dict): JSON data

    Returns:
        dict: Response data
    """
    url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Odoo/18.0',
    }

    if self.api_key:
        headers['Authorization'] = f'Bearer {self.api_key}'

    try:
        _logger.info("PATCH request to %s", url)

        response = requests.patch(
            url,
            json=json_data,
            headers=headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.json() if response.content else {'success': True}

    except requests.exceptions.RequestException as e:
        self._handle_request_exception(e, response if 'response' in locals() else None)
```

---

## Autenticacao

### 1. API Key Authentication

```python
class APIKeyConnector(models.Model):
    _name = 'api.key.connector'
    _description = 'API Key Connector'

    name = fields.Char('Name')
    api_key = fields.Char('API Key', required=True)
    api_secret = fields.Char('API Secret')  # Algumas APIs usam key + secret

    def _get_headers(self):
        """Retorna headers com autenticacao API Key"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    # Alternativa: API Key no header customizado
    def _get_custom_headers(self):
        """Algumas APIs usam headers customizados"""
        return {
            'X-API-Key': self.api_key,
            'X-API-Secret': self.api_secret,
            'Accept': 'application/json',
        }

    # Alternativa: API Key na query string
    def _add_api_key_to_params(self, params=None):
        """Adiciona API key aos parametros"""
        if params is None:
            params = {}

        params['api_key'] = self.api_key
        return params
```

### 2. Basic Authentication

```python
class BasicAuthConnector(models.Model):
    _name = 'basic.auth.connector'
    _description = 'Basic Auth Connector'

    username = fields.Char('Username', required=True)
    password = fields.Char('Password', required=True)

    def _make_request_with_basic_auth(self, url, method='GET', **kwargs):
        """Faz requisicao com Basic Auth"""
        from requests.auth import HTTPBasicAuth

        auth = HTTPBasicAuth(self.username, self.password)

        response = requests.request(
            method,
            url,
            auth=auth,
            **kwargs
        )

        response.raise_for_status()
        return response.json()
```

### 3. OAuth 2.0 Authentication

```python
class OAuth2Connector(models.Model):
    _name = 'oauth2.connector'
    _description = 'OAuth2 Connector'

    name = fields.Char('Name')
    client_id = fields.Char('Client ID', required=True)
    client_secret = fields.Char('Client Secret', required=True)

    # OAuth endpoints
    auth_url = fields.Char('Authorization URL')
    token_url = fields.Char('Token URL')
    redirect_uri = fields.Char('Redirect URI')

    # Tokens
    access_token = fields.Char('Access Token', readonly=True)
    refresh_token = fields.Char('Refresh Token', readonly=True)
    token_expires_at = fields.Datetime('Token Expires At', readonly=True)

    # Scopes
    scope = fields.Char('Scope', default='read write')

    def _get_authorization_url(self):
        """Gera URL de autorizacao"""
        import urllib.parse

        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': self.scope,
        }

        return f"{self.auth_url}?{urllib.parse.urlencode(params)}"

    def action_authorize(self):
        """Redireciona usuario para autorizacao OAuth"""
        self.ensure_one()

        auth_url = self._get_authorization_url()

        return {
            'type': 'ir.actions.act_url',
            'url': auth_url,
            'target': 'new',
        }

    def exchange_code_for_token(self, code):
        """Troca authorization code por access token"""
        self.ensure_one()

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        try:
            response = requests.post(
                self.token_url,
                data=data,
                timeout=30
            )

            response.raise_for_status()
            token_data = response.json()

            # Salvar tokens
            self.write({
                'access_token': token_data['access_token'],
                'refresh_token': token_data.get('refresh_token'),
                'token_expires_at': fields.Datetime.now() + timedelta(
                    seconds=token_data.get('expires_in', 3600)
                ),
            })

            return True

        except Exception as e:
            _logger.error("Failed to exchange code for token: %s", str(e))
            raise UserError(f"Failed to obtain access token: {str(e)}")

    def _refresh_access_token(self):
        """Renova access token usando refresh token"""
        self.ensure_one()

        if not self.refresh_token:
            raise UserError("No refresh token available. Please re-authorize.")

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        try:
            response = requests.post(
                self.token_url,
                data=data,
                timeout=30
            )

            response.raise_for_status()
            token_data = response.json()

            self.write({
                'access_token': token_data['access_token'],
                'refresh_token': token_data.get('refresh_token', self.refresh_token),
                'token_expires_at': fields.Datetime.now() + timedelta(
                    seconds=token_data.get('expires_in', 3600)
                ),
            })

            return True

        except Exception as e:
            _logger.error("Failed to refresh token: %s", str(e))
            raise UserError(f"Failed to refresh access token: {str(e)}")

    def _ensure_valid_token(self):
        """Garante que temos um token valido"""
        self.ensure_one()

        if not self.access_token:
            raise UserError("No access token. Please authorize first.")

        # Verificar se token expirou
        if self.token_expires_at:
            # Renovar se faltar menos de 5 minutos para expirar
            if self.token_expires_at < fields.Datetime.now() + timedelta(minutes=5):
                _logger.info("Access token expired or expiring soon. Refreshing...")
                self._refresh_access_token()

    def _make_oauth_request(self, url, method='GET', **kwargs):
        """Faz requisicao autenticada com OAuth"""
        self._ensure_valid_token()

        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.access_token}'
        kwargs['headers'] = headers

        try:
            response = requests.request(method, url, **kwargs)

            # Se 401, tentar renovar token e fazer novamente
            if response.status_code == 401:
                _logger.warning("Received 401. Attempting to refresh token...")
                self._refresh_access_token()

                # Atualizar header com novo token
                headers['Authorization'] = f'Bearer {self.access_token}'
                kwargs['headers'] = headers

                # Tentar novamente
                response = requests.request(method, url, **kwargs)

            response.raise_for_status()
            return response.json()

        except Exception as e:
            _logger.error("OAuth request failed: %s", str(e))
            raise
```

### 4. JWT Authentication

```python
class JWTConnector(models.Model):
    _name = 'jwt.connector'
    _description = 'JWT Connector'

    name = fields.Char('Name')
    secret_key = fields.Char('Secret Key', required=True)
    algorithm = fields.Selection([
        ('HS256', 'HMAC-SHA256'),
        ('RS256', 'RSA-SHA256'),
    ], default='HS256')

    def _generate_jwt_token(self, payload, expires_in=3600):
        """
        Gera JWT token

        Requer: pip install PyJWT
        """
        import jwt
        from datetime import datetime, timedelta

        payload['exp'] = datetime.utcnow() + timedelta(seconds=expires_in)
        payload['iat'] = datetime.utcnow()

        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )

        return token

    def _verify_jwt_token(self, token):
        """Verifica e decodifica JWT token"""
        import jwt

        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise UserError("Token has expired")
        except jwt.InvalidTokenError:
            raise UserError("Invalid token")

    def _make_jwt_request(self, url, payload, method='GET', **kwargs):
        """Faz requisicao autenticada com JWT"""
        token = self._generate_jwt_token(payload)

        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {token}'
        kwargs['headers'] = headers

        response = requests.request(method, url, **kwargs)
        response.raise_for_status()

        return response.json()
```

---

## Handling de Responses e Errors

### 1. Response Parser Generico

```python
class APIResponseParser(models.AbstractModel):
    _name = 'api.response.parser'
    _description = 'API Response Parser'

    def parse_response(self, response, expected_status=200):
        """
        Parse response de API

        Args:
            response: requests.Response object
            expected_status: Status code esperado

        Returns:
            dict: Parsed data

        Raises:
            UserError: Se response nao for valida
        """
        try:
            # Verificar status code
            if response.status_code != expected_status:
                self._handle_error_response(response)

            # Verificar se response tem conteudo
            if not response.content:
                return {'success': True}

            # Tentar parsear JSON
            try:
                data = response.json()
            except ValueError:
                # Response nao e JSON, retornar texto
                return {'text': response.text}

            # Validar estrutura da response
            if not isinstance(data, dict):
                _logger.warning("Response is not a dict: %s", type(data))

            return data

        except Exception as e:
            _logger.error("Failed to parse response: %s", str(e))
            raise UserError(f"Failed to parse API response: {str(e)}")

    def _handle_error_response(self, response):
        """Trata responses de erro"""
        status_code = response.status_code
        error_msg = f"API request failed with status {status_code}"

        try:
            error_data = response.json()

            # Diferentes APIs retornam erros em formatos diferentes
            if 'error' in error_data:
                if isinstance(error_data['error'], dict):
                    error_msg = error_data['error'].get('message', error_msg)
                else:
                    error_msg = error_data['error']

            elif 'message' in error_data:
                error_msg = error_data['message']

            elif 'errors' in error_data:
                errors = error_data['errors']
                if isinstance(errors, list):
                    error_msg = ', '.join(str(e) for e in errors)
                else:
                    error_msg = str(errors)

        except ValueError:
            # Response nao e JSON
            error_msg = response.text or error_msg

        _logger.error("API Error: %s", error_msg)

        # Mapear status codes para mensagens mais amigaveis
        friendly_messages = {
            400: "Bad Request - Invalid data sent to API",
            401: "Unauthorized - Invalid credentials",
            403: "Forbidden - Access denied",
            404: "Not Found - Resource does not exist",
            429: "Too Many Requests - Rate limit exceeded",
            500: "Internal Server Error - API is experiencing issues",
            503: "Service Unavailable - API is temporarily unavailable",
        }

        if status_code in friendly_messages:
            error_msg = f"{friendly_messages[status_code]}: {error_msg}"

        raise UserError(error_msg)
```

### 2. Error Logging e Recovery

```python
class APIErrorLog(models.Model):
    _name = 'api.error.log'
    _description = 'API Error Log'
    _order = 'create_date desc'

    name = fields.Char('Error', compute='_compute_name', store=True)
    api_name = fields.Char('API Name')
    endpoint = fields.Char('Endpoint')
    method = fields.Char('Method')
    status_code = fields.Integer('Status Code')
    error_type = fields.Char('Error Type')
    error_message = fields.Text('Error Message')
    request_data = fields.Text('Request Data')
    response_data = fields.Text('Response Data')
    traceback = fields.Text('Traceback')

    # Para retry
    retry_count = fields.Integer('Retry Count', default=0)
    max_retries = fields.Integer('Max Retries', default=3)
    can_retry = fields.Boolean('Can Retry', compute='_compute_can_retry')

    related_model = fields.Char('Related Model')
    related_id = fields.Integer('Related ID')

    @api.depends('api_name', 'endpoint', 'status_code')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.api_name} - {record.endpoint} ({record.status_code})"

    @api.depends('retry_count', 'max_retries', 'status_code')
    def _compute_can_retry(self):
        """Determina se erro pode ser retriado"""
        retriable_codes = [408, 429, 500, 502, 503, 504]

        for record in self:
            record.can_retry = (
                record.retry_count < record.max_retries and
                record.status_code in retriable_codes
            )

    def action_retry(self):
        """Retenta requisicao"""
        self.ensure_one()

        if not self.can_retry:
            raise UserError("This request cannot be retried.")

        # Incrementar contador
        self.retry_count += 1

        # Aqui voce implementaria a logica para reprocessar
        # baseado no related_model e related_id

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Retry Scheduled',
                'message': f'Request will be retried (attempt {self.retry_count}/{self.max_retries})',
                'type': 'info',
            }
        }

class APIIntegrationWithLogging(models.Model):
    _name = 'api.integration.logging'
    _description = 'API Integration with Logging'

    def _make_logged_request(self, url, method='GET', **kwargs):
        """Faz requisicao com logging automatico de erros"""
        import traceback

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            # Log do erro
            error_log = self.env['api.error.log'].create({
                'api_name': self._name,
                'endpoint': url,
                'method': method,
                'status_code': response.status_code if 'response' in locals() else 0,
                'error_type': type(e).__name__,
                'error_message': str(e),
                'request_data': json.dumps(kwargs, indent=2),
                'response_data': response.text if 'response' in locals() else '',
                'traceback': traceback.format_exc(),
                'related_model': self._name,
                'related_id': self.id if hasattr(self, 'id') else 0,
            })

            _logger.error("API request failed. Error log ID: %s", error_log.id)

            raise
```

### 3. Response Validation

```python
class APIResponseValidator(models.AbstractModel):
    _name = 'api.response.validator'
    _description = 'API Response Validator'

    def validate_response_structure(self, data, schema):
        """
        Valida estrutura da response

        Args:
            data: Response data
            schema: Expected schema

        Example schema:
        {
            'required_fields': ['id', 'name', 'email'],
            'optional_fields': ['phone', 'address'],
            'field_types': {
                'id': int,
                'name': str,
                'email': str,
            }
        }
        """
        errors = []

        # Validar campos obrigatorios
        for field in schema.get('required_fields', []):
            if field not in data:
                errors.append(f"Missing required field: {field}")

        # Validar tipos
        for field, expected_type in schema.get('field_types', {}).items():
            if field in data:
                if not isinstance(data[field], expected_type):
                    errors.append(
                        f"Invalid type for {field}: expected {expected_type.__name__}, "
                        f"got {type(data[field]).__name__}"
                    )

        if errors:
            error_msg = "Response validation failed:\n" + "\n".join(errors)
            _logger.error(error_msg)
            raise UserError(error_msg)

        return True
```

---

## Retry Logic

### 1. Decorator para Retry

```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1, backoff=2, exceptions=(Exception,)):
    """
    Decorator para retry automatico

    Args:
        max_retries: Numero maximo de tentativas
        delay: Delay inicial entre tentativas (segundos)
        backoff: Multiplicador do delay a cada retry
        exceptions: Tupla de excecoes que devem ser retriadas
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    if attempt < max_retries:
                        _logger.warning(
                            "Attempt %d/%d failed for %s: %s. Retrying in %d seconds...",
                            attempt + 1, max_retries, func.__name__, str(e), current_delay
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        _logger.error(
                            "All %d attempts failed for %s: %s",
                            max_retries + 1, func.__name__, str(e)
                        )

            raise last_exception

        return wrapper
    return decorator

# Uso:
class APIWithRetry(models.Model):
    _name = 'api.with.retry'
    _description = 'API with Retry Logic'

    @retry_on_failure(
        max_retries=3,
        delay=2,
        backoff=2,
        exceptions=(requests.exceptions.RequestException,)
    )
    def _make_request_with_retry(self, url):
        """Faz requisicao com retry automatico"""
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
```

### 2. Retry com Exponential Backoff

```python
class ExponentialBackoffRetry(models.Model):
    _name = 'exponential.backoff.retry'
    _description = 'Exponential Backoff Retry'

    def _make_request_with_exponential_backoff(
        self, url, max_retries=5, base_delay=1, max_delay=60
    ):
        """
        Faz requisicao com exponential backoff

        Delays: 1s, 2s, 4s, 8s, 16s, 32s, 60s (max)
        """
        import random

        for attempt in range(max_retries + 1):
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                return response.json()

            except requests.exceptions.RequestException as e:
                if attempt == max_retries:
                    _logger.error("All retry attempts failed: %s", str(e))
                    raise

                # Calcular delay com exponential backoff + jitter
                delay = min(base_delay * (2 ** attempt), max_delay)

                # Adicionar jitter (randomizacao) para evitar thundering herd
                jitter = random.uniform(0, delay * 0.1)
                total_delay = delay + jitter

                _logger.warning(
                    "Attempt %d failed: %s. Retrying in %.2f seconds...",
                    attempt + 1, str(e), total_delay
                )

                time.sleep(total_delay)
```

### 3. Retry com Rate Limiting

```python
class RateLimitedAPI(models.Model):
    _name = 'rate.limited.api'
    _description = 'Rate Limited API'

    def _make_rate_limited_request(self, url, rate_limit=100, per_seconds=60):
        """
        Faz requisicao respeitando rate limits

        Args:
            url: URL da API
            rate_limit: Numero maximo de requisicoes
            per_seconds: Periodo de tempo (segundos)
        """
        # Usar cache para rastrear requisicoes
        cache_key = f'api_requests_{self._name}'
        requests_cache = self.env['ir.config_parameter'].sudo().get_param(
            cache_key, '[]'
        )

        try:
            requests_list = json.loads(requests_cache)
        except:
            requests_list = []

        now = time.time()

        # Limpar requisicoes antigas
        requests_list = [
            ts for ts in requests_list
            if now - ts < per_seconds
        ]

        # Verificar rate limit
        if len(requests_list) >= rate_limit:
            # Calcular quanto tempo esperar
            oldest = min(requests_list)
            wait_time = per_seconds - (now - oldest)

            if wait_time > 0:
                _logger.info(
                    "Rate limit reached. Waiting %.2f seconds...",
                    wait_time
                )
                time.sleep(wait_time)

                # Limpar cache apos espera
                requests_list = []

        # Fazer requisicao
        try:
            response = requests.get(url, timeout=30)

            # Registrar timestamp
            requests_list.append(time.time())

            # Salvar no cache
            self.env['ir.config_parameter'].sudo().set_param(
                cache_key,
                json.dumps(requests_list)
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            _logger.error("Request failed: %s", str(e))
            raise
```

---

## Webhooks

### 1. Recebendo Webhooks

```python
from odoo import http
from odoo.http import request
import hashlib
import hmac

class WebhookController(http.Controller):

    @http.route('/webhook/payment', type='json', auth='none', methods=['POST'], csrf=False)
    def payment_webhook(self, **kwargs):
        """
        Endpoint para receber webhooks de payment gateway

        Exemplo de payload:
        {
            "event": "payment.success",
            "payment_id": "pay_123",
            "order_id": "SO001",
            "amount": 100.00,
            "currency": "USD"
        }
        """
        try:
            # Obter payload
            payload = request.get_json_data()

            _logger.info("Received webhook: %s", payload)

            # Validar signature (se aplicavel)
            signature = request.httprequest.headers.get('X-Signature')
            if signature:
                if not self._verify_webhook_signature(payload, signature):
                    _logger.error("Invalid webhook signature")
                    return {'error': 'Invalid signature'}, 401

            # Processar webhook
            event_type = payload.get('event')

            if event_type == 'payment.success':
                self._handle_payment_success(payload)

            elif event_type == 'payment.failed':
                self._handle_payment_failed(payload)

            elif event_type == 'refund.processed':
                self._handle_refund_processed(payload)

            else:
                _logger.warning("Unknown webhook event: %s", event_type)

            return {'status': 'success'}

        except Exception as e:
            _logger.error("Webhook processing failed: %s", str(e), exc_info=True)
            return {'error': str(e)}, 500

    def _verify_webhook_signature(self, payload, signature):
        """Verifica assinatura do webhook"""
        # Obter secret do config
        secret = request.env['ir.config_parameter'].sudo().get_param(
            'payment.webhook.secret'
        )

        if not secret:
            _logger.warning("No webhook secret configured")
            return False

        # Calcular signature esperada
        payload_string = json.dumps(payload, sort_keys=True)
        expected_signature = hmac.new(
            secret.encode(),
            payload_string.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    def _handle_payment_success(self, payload):
        """Processa pagamento bem-sucedido"""
        order_name = payload.get('order_id')
        payment_id = payload.get('payment_id')
        amount = payload.get('amount')

        # Buscar pedido
        SaleOrder = request.env['sale.order'].sudo()
        order = SaleOrder.search([('name', '=', order_name)], limit=1)

        if not order:
            _logger.error("Order not found: %s", order_name)
            return

        # Criar payment
        payment_vals = {
            'payment_type': 'inbound',
            'partner_id': order.partner_id.id,
            'amount': amount,
            'ref': payment_id,
            'payment_method_id': self._get_payment_method().id,
        }

        payment = request.env['account.payment'].sudo().create(payment_vals)
        payment.action_post()

        # Atualizar pedido
        order.message_post(
            body=f"Payment received: {payment_id} - Amount: {amount}",
            message_type='notification'
        )

        _logger.info("Payment processed successfully for order %s", order_name)

    def _handle_payment_failed(self, payload):
        """Processa falha de pagamento"""
        order_name = payload.get('order_id')
        error_message = payload.get('error_message', 'Unknown error')

        SaleOrder = request.env['sale.order'].sudo()
        order = SaleOrder.search([('name', '=', order_name)], limit=1)

        if order:
            order.message_post(
                body=f"Payment failed: {error_message}",
                message_type='comment',
                subtype_xmlid='mail.mt_note'
            )

            # Criar activity para follow-up
            order.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=order.user_id.id,
                summary='Payment Failed - Follow Up Required',
                note=f'Payment failed with error: {error_message}',
            )

    def _handle_refund_processed(self, payload):
        """Processa refund"""
        # Implementar logica de refund
        pass

    def _get_payment_method(self):
        """Retorna metodo de pagamento padrao"""
        return request.env.ref('payment.account_payment_method_electronic_in', False)
```

### 2. Validacao de Webhooks Assinados

```python
class SecureWebhook(http.Controller):

    @http.route('/webhook/stripe', type='json', auth='none', methods=['POST'], csrf=False)
    def stripe_webhook(self):
        """Webhook do Stripe com validacao de signature"""
        try:
            # Obter payload raw (Stripe requer payload exato para signature)
            payload = request.httprequest.get_data()
            sig_header = request.httprequest.headers.get('Stripe-Signature')

            # Validar signature
            webhook_secret = request.env['ir.config_parameter'].sudo().get_param(
                'stripe.webhook.secret'
            )

            if not self._verify_stripe_signature(payload, sig_header, webhook_secret):
                _logger.error("Invalid Stripe signature")
                return {'error': 'Invalid signature'}, 401

            # Parse payload
            event = json.loads(payload)

            # Processar evento
            event_type = event['type']

            if event_type == 'payment_intent.succeeded':
                self._handle_stripe_payment_success(event)

            return {'status': 'success'}

        except Exception as e:
            _logger.error("Stripe webhook failed: %s", str(e), exc_info=True)
            return {'error': str(e)}, 500

    def _verify_stripe_signature(self, payload, sig_header, secret):
        """Verifica assinatura do Stripe"""
        import hmac
        import hashlib

        # Parse signature header
        signatures = {}
        for pair in sig_header.split(','):
            key, value = pair.split('=')
            signatures[key] = value

        timestamp = signatures.get('t')
        signature = signatures.get('v1')

        if not timestamp or not signature:
            return False

        # Calcular expected signature
        signed_payload = f"{timestamp}.{payload.decode()}"
        expected_signature = hmac.new(
            secret.encode(),
            signed_payload.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)
```

### 3. Webhook Queue para Processamento Assíncrono

```python
class WebhookQueue(models.Model):
    _name = 'webhook.queue'
    _description = 'Webhook Queue'
    _order = 'create_date desc'

    name = fields.Char('Name', compute='_compute_name', store=True)
    source = fields.Char('Source', required=True)  # stripe, paypal, etc
    event_type = fields.Char('Event Type', required=True)
    payload = fields.Text('Payload', required=True)

    state = fields.Selection([
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ], default='pending', required=True)

    processed_date = fields.Datetime('Processed Date')
    error_message = fields.Text('Error Message')
    retry_count = fields.Integer('Retry Count', default=0)

    @api.depends('source', 'event_type')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.source} - {record.event_type}"

    @api.model
    def _cron_process_webhooks(self):
        """Scheduled action para processar webhooks pendentes"""
        pending = self.search([
            ('state', '=', 'pending'),
        ], limit=100)

        for webhook in pending:
            webhook.process_webhook()

    def process_webhook(self):
        """Processa webhook"""
        self.ensure_one()

        try:
            self.state = 'processing'

            payload = json.loads(self.payload)

            # Rotear para handler apropriado
            handler_method = f'_handle_{self.source}_{self.event_type.replace(".", "_")}'

            if hasattr(self, handler_method):
                getattr(self, handler_method)(payload)
            else:
                _logger.warning("No handler for %s - %s", self.source, self.event_type)

            self.write({
                'state': 'done',
                'processed_date': fields.Datetime.now(),
            })

        except Exception as e:
            self.retry_count += 1

            if self.retry_count >= 5:
                state = 'failed'
                _logger.error("Webhook processing failed after 5 attempts: %s", str(e))
            else:
                state = 'pending'
                _logger.warning("Webhook processing failed, will retry: %s", str(e))

            self.write({
                'state': state,
                'error_message': str(e),
            })

# Controller que adiciona webhooks na fila
class WebhookQueueController(http.Controller):

    @http.route('/webhook/queue/<string:source>', type='json', auth='none', methods=['POST'], csrf=False)
    def queue_webhook(self, source, **kwargs):
        """Adiciona webhook na fila para processamento assincrono"""
        try:
            payload = request.get_json_data()

            # Criar registro na fila
            request.env['webhook.queue'].sudo().create({
                'source': source,
                'event_type': payload.get('event', payload.get('type', 'unknown')),
                'payload': json.dumps(payload),
            })

            return {'status': 'queued'}

        except Exception as e:
            _logger.error("Failed to queue webhook: %s", str(e))
            return {'error': str(e)}, 500
```

---

## Queue Systems

### 1. Usando Queue Job (OCA)

```python
# Requer: pip install odoo-addon-queue_job

from odoo.addons.queue_job.job import job

class AsyncAPIIntegration(models.Model):
    _name = 'async.api.integration'
    _description = 'Async API Integration'

    @job
    def sync_customers_async(self):
        """Sincroniza customers de forma assincrona"""
        _logger.info("Starting async customer sync...")

        try:
            # Buscar customers da API
            customers = self._fetch_customers_from_api()

            # Processar em batch
            for i in range(0, len(customers), 100):
                batch = customers[i:i+100]
                self._process_customer_batch(batch)

                # Commit periodico
                self.env.cr.commit()

            _logger.info("Customer sync completed successfully")

        except Exception as e:
            _logger.error("Customer sync failed: %s", str(e))
            raise

    def action_sync_customers(self):
        """Button action que dispara job assincrono"""
        self.ensure_one()

        # Adicionar na fila
        self.with_delay().sync_customers_async()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sync Started',
                'message': 'Customer synchronization has been queued',
                'type': 'success',
            }
        }

    @job(default_channel='root.slow')
    def import_large_file_async(self, file_data):
        """Importa arquivo grande de forma assincrona (canal slow)"""
        # Processar arquivo
        pass

    @job(retry_pattern={1: 60, 5: 300, 10: 600})
    def api_call_with_retry(self, endpoint):
        """Job com retry automatico"""
        # Fazer chamada de API
        # Se falhar, sera retriado automaticamente
        pass
```

### 2. Background Jobs Customizado

```python
class BackgroundJob(models.Model):
    _name = 'background.job'
    _description = 'Background Job'
    _order = 'create_date desc'

    name = fields.Char('Job Name', required=True)
    model_name = fields.Char('Model', required=True)
    method_name = fields.Char('Method', required=True)
    args = fields.Text('Arguments')  # JSON
    kwargs = fields.Text('Keyword Arguments')  # JSON

    state = fields.Selection([
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ], default='pending', required=True)

    priority = fields.Integer('Priority', default=10)
    scheduled_date = fields.Datetime('Scheduled Date', default=fields.Datetime.now)
    started_date = fields.Datetime('Started Date')
    completed_date = fields.Datetime('Completed Date')

    result = fields.Text('Result')
    error_message = fields.Text('Error Message')
    traceback = fields.Text('Traceback')

    retry_count = fields.Integer('Retry Count', default=0)
    max_retries = fields.Integer('Max Retries', default=3)

    @api.model
    def _cron_process_jobs(self):
        """Scheduled action para processar jobs"""
        # Buscar jobs pendentes
        jobs = self.search([
            ('state', '=', 'pending'),
            ('scheduled_date', '<=', fields.Datetime.now()),
        ], order='priority desc, create_date asc', limit=10)

        for job in jobs:
            job.execute()

    def execute(self):
        """Executa job"""
        self.ensure_one()

        try:
            self.write({
                'state': 'running',
                'started_date': fields.Datetime.now(),
            })

            # Parse args
            args = json.loads(self.args) if self.args else []
            kwargs = json.loads(self.kwargs) if self.kwargs else {}

            # Obter model e metodo
            model = self.env[self.model_name]
            method = getattr(model, self.method_name)

            # Executar
            result = method(*args, **kwargs)

            # Salvar resultado
            self.write({
                'state': 'done',
                'completed_date': fields.Datetime.now(),
                'result': json.dumps(result) if result else '',
            })

            self.env.cr.commit()

        except Exception as e:
            import traceback as tb

            self.retry_count += 1

            if self.retry_count < self.max_retries:
                # Reagendar
                retry_delay = 2 ** self.retry_count  # Exponential backoff
                self.write({
                    'state': 'pending',
                    'scheduled_date': fields.Datetime.now() + timedelta(minutes=retry_delay),
                    'error_message': str(e),
                })
            else:
                # Falhou definitivamente
                self.write({
                    'state': 'failed',
                    'completed_date': fields.Datetime.now(),
                    'error_message': str(e),
                    'traceback': tb.format_exc(),
                })

            self.env.cr.commit()
            _logger.error("Job %s failed: %s", self.name, str(e), exc_info=True)

    @api.model
    def schedule_job(self, model_name, method_name, args=None, kwargs=None, **job_kwargs):
        """
        Agenda job para execucao

        Usage:
            self.env['background.job'].schedule_job(
                'res.partner',
                'sync_with_external_api',
                args=[123],
                kwargs={'force': True},
                priority=5,
                scheduled_date=fields.Datetime.now() + timedelta(hours=1)
            )
        """
        vals = {
            'name': job_kwargs.pop('name', f"{model_name}.{method_name}"),
            'model_name': model_name,
            'method_name': method_name,
            'args': json.dumps(args) if args else '[]',
            'kwargs': json.dumps(kwargs) if kwargs else '{}',
            **job_kwargs
        }

        return self.create(vals)
```

---

## Logging e Monitoring

### 1. Structured Logging

```python
import logging
import json
from datetime import datetime

class APILogger:
    """Logger estruturado para API calls"""

    def __init__(self, api_name):
        self.api_name = api_name
        self.logger = logging.getLogger(f'odoo.api.{api_name}')

    def log_request(self, method, url, headers=None, data=None):
        """Log de requisicao"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'api': self.api_name,
            'type': 'request',
            'method': method,
            'url': url,
            'headers': self._sanitize_headers(headers or {}),
            'data': self._sanitize_data(data),
        }

        self.logger.info(json.dumps(log_data))

    def log_response(self, method, url, status_code, response_time, data=None):
        """Log de response"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'api': self.api_name,
            'type': 'response',
            'method': method,
            'url': url,
            'status_code': status_code,
            'response_time_ms': response_time,
            'data': self._sanitize_data(data),
        }

        level = logging.INFO if 200 <= status_code < 300 else logging.ERROR
        self.logger.log(level, json.dumps(log_data))

    def log_error(self, method, url, error, traceback=None):
        """Log de erro"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'api': self.api_name,
            'type': 'error',
            'method': method,
            'url': url,
            'error': str(error),
            'error_type': type(error).__name__,
            'traceback': traceback,
        }

        self.logger.error(json.dumps(log_data))

    def _sanitize_headers(self, headers):
        """Remove dados sensiveis dos headers"""
        sensitive_keys = ['authorization', 'api-key', 'x-api-key', 'token']
        sanitized = headers.copy()

        for key in sanitized:
            if key.lower() in sensitive_keys:
                sanitized[key] = '***REDACTED***'

        return sanitized

    def _sanitize_data(self, data):
        """Remove dados sensiveis do payload"""
        if not data:
            return None

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                return '***DATA***'

        if isinstance(data, dict):
            sensitive_keys = ['password', 'secret', 'token', 'api_key', 'credit_card']
            sanitized = data.copy()

            for key in sanitized:
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    sanitized[key] = '***REDACTED***'

            return sanitized

        return str(data)[:100]  # Limitar tamanho

# Uso:
class APIWithLogging(models.Model):
    _name = 'api.with.logging'
    _description = 'API with Logging'

    def _make_logged_request(self, method, url, **kwargs):
        """Faz requisicao com logging completo"""
        logger = APILogger(self._name)

        # Log request
        logger.log_request(
            method,
            url,
            headers=kwargs.get('headers'),
            data=kwargs.get('json')
        )

        start_time = time.time()

        try:
            response = requests.request(method, url, **kwargs)

            # Log response
            response_time = (time.time() - start_time) * 1000
            logger.log_response(
                method,
                url,
                response.status_code,
                response_time,
                data=response.text[:500]  # Limitar tamanho
            )

            response.raise_for_status()
            return response.json()

        except Exception as e:
            import traceback
            logger.log_error(method, url, e, traceback.format_exc())
            raise
```

### 2. Monitoring Dashboard

```python
class APIMonitoring(models.Model):
    _name = 'api.monitoring'
    _description = 'API Monitoring'

    name = fields.Char('API Name', required=True)

    # Metricas
    total_requests = fields.Integer('Total Requests', readonly=True)
    successful_requests = fields.Integer('Successful Requests', readonly=True)
    failed_requests = fields.Integer('Failed Requests', readonly=True)
    success_rate = fields.Float('Success Rate (%)', compute='_compute_success_rate')

    avg_response_time = fields.Float('Avg Response Time (ms)', readonly=True)
    last_request_date = fields.Datetime('Last Request', readonly=True)
    last_error_date = fields.Datetime('Last Error', readonly=True)
    last_error_message = fields.Text('Last Error Message', readonly=True)

    # Status
    is_healthy = fields.Boolean('Is Healthy', compute='_compute_is_healthy')
    status = fields.Selection([
        ('ok', 'OK'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('unknown', 'Unknown'),
    ], compute='_compute_status')

    @api.depends('successful_requests', 'failed_requests')
    def _compute_success_rate(self):
        for record in self:
            total = record.successful_requests + record.failed_requests
            if total > 0:
                record.success_rate = (record.successful_requests / total) * 100
            else:
                record.success_rate = 0

    @api.depends('success_rate', 'last_request_date')
    def _compute_is_healthy(self):
        for record in self:
            # Considerar saudavel se:
            # - Success rate > 95%
            # - Teve requisicao nas ultimas 24h
            recent = record.last_request_date and \
                     record.last_request_date > fields.Datetime.now() - timedelta(hours=24)

            record.is_healthy = record.success_rate > 95 and recent

    @api.depends('is_healthy', 'success_rate')
    def _compute_status(self):
        for record in self:
            if not record.last_request_date:
                record.status = 'unknown'
            elif record.success_rate >= 95:
                record.status = 'ok'
            elif record.success_rate >= 80:
                record.status = 'warning'
            else:
                record.status = 'error'

    def record_request(self, success, response_time, error_message=None):
        """Registra metricas de uma requisicao"""
        self.ensure_one()

        # Calcular nova media de response time
        total_requests = self.total_requests + 1
        new_avg = (
            (self.avg_response_time * self.total_requests + response_time) /
            total_requests
        )

        vals = {
            'total_requests': total_requests,
            'avg_response_time': new_avg,
            'last_request_date': fields.Datetime.now(),
        }

        if success:
            vals['successful_requests'] = self.successful_requests + 1
        else:
            vals.update({
                'failed_requests': self.failed_requests + 1,
                'last_error_date': fields.Datetime.now(),
                'last_error_message': error_message,
            })

        self.write(vals)

    @api.model
    def _cron_check_api_health(self):
        """Scheduled action para checar health das APIs"""
        apis = self.search([])

        for api in apis:
            if api.status == 'error':
                # Enviar notificacao
                api._send_health_alert()

    def _send_health_alert(self):
        """Envia alerta de health"""
        self.ensure_one()

        # Buscar administradores
        admin_group = self.env.ref('base.group_system')
        admins = admin_group.users

        # Enviar email
        template = self.env.ref('module_name.email_template_api_health_alert', False)
        if template:
            for admin in admins:
                template.send_mail(
                    self.id,
                    email_values={'email_to': admin.email},
                    force_send=True
                )
```

### 3. Performance Profiling

```python
class APIPerformanceProfiler:
    """Profiler para medir performance de API calls"""

    def __init__(self, api_name):
        self.api_name = api_name
        self.metrics = []

    def profile_request(self, func):
        """Decorator para profile de requests"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = self._get_memory_usage()

            try:
                result = func(*args, **kwargs)
                success = True
                error = None

            except Exception as e:
                success = False
                error = str(e)
                raise

            finally:
                end_time = time.time()
                end_memory = self._get_memory_usage()

                metrics = {
                    'api': self.api_name,
                    'function': func.__name__,
                    'duration_ms': (end_time - start_time) * 1000,
                    'memory_delta_mb': (end_memory - start_memory) / (1024 * 1024),
                    'success': success,
                    'error': error,
                    'timestamp': datetime.now().isoformat(),
                }

                self.metrics.append(metrics)
                _logger.info("Performance: %s", json.dumps(metrics))

            return result

        return wrapper

    def _get_memory_usage(self):
        """Retorna uso de memoria em bytes"""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        return process.memory_info().rss

    def get_summary(self):
        """Retorna resumo das metricas"""
        if not self.metrics:
            return {}

        durations = [m['duration_ms'] for m in self.metrics]
        memories = [m['memory_delta_mb'] for m in self.metrics]
        successes = sum(1 for m in self.metrics if m['success'])

        return {
            'total_calls': len(self.metrics),
            'successful_calls': successes,
            'failed_calls': len(self.metrics) - successes,
            'avg_duration_ms': sum(durations) / len(durations),
            'max_duration_ms': max(durations),
            'min_duration_ms': min(durations),
            'avg_memory_delta_mb': sum(memories) / len(memories),
        }
```

---

## Exemplos Praticos

### Exemplo 1: Payment Gateway (Stripe)

```python
class StripePaymentProvider(models.Model):
    _name = 'stripe.payment.provider'
    _description = 'Stripe Payment Provider'

    name = fields.Char('Name', default='Stripe')
    secret_key = fields.Char('Secret Key', required=True)
    publishable_key = fields.Char('Publishable Key', required=True)
    webhook_secret = fields.Char('Webhook Secret')

    base_url = fields.Char('Base URL', default='https://api.stripe.com/v1')

    def _get_headers(self):
        """Retorna headers para Stripe API"""
        return {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    def create_payment_intent(self, amount, currency='usd', metadata=None):
        """
        Cria Payment Intent no Stripe

        Args:
            amount: Valor em centavos (ex: 1000 = $10.00)
            currency: Moeda (default: usd)
            metadata: Dados adicionais

        Returns:
            dict: Payment Intent data
        """
        url = f"{self.base_url}/payment_intents"

        data = {
            'amount': int(amount * 100),  # Converter para centavos
            'currency': currency,
        }

        if metadata:
            for key, value in metadata.items():
                data[f'metadata[{key}]'] = value

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                data=data,
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            _logger.error("Failed to create Stripe Payment Intent: %s", str(e))
            raise UserError(f"Payment processing failed: {str(e)}")

    def capture_payment_intent(self, payment_intent_id):
        """Captura Payment Intent"""
        url = f"{self.base_url}/payment_intents/{payment_intent_id}/capture"

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            _logger.error("Failed to capture payment: %s", str(e))
            raise UserError(f"Payment capture failed: {str(e)}")

    def refund_payment(self, charge_id, amount=None):
        """Cria refund"""
        url = f"{self.base_url}/refunds"

        data = {'charge': charge_id}

        if amount:
            data['amount'] = int(amount * 100)

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                data=data,
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            _logger.error("Failed to create refund: %s", str(e))
            raise UserError(f"Refund failed: {str(e)}")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    stripe_payment_intent_id = fields.Char('Stripe Payment Intent ID')

    def action_process_payment(self):
        """Processa pagamento via Stripe"""
        self.ensure_one()

        # Buscar provider
        provider = self.env['stripe.payment.provider'].search([], limit=1)
        if not provider:
            raise UserError("Stripe provider not configured")

        try:
            # Criar Payment Intent
            intent = provider.create_payment_intent(
                amount=self.amount_total,
                currency=self.currency_id.name.lower(),
                metadata={
                    'order_id': self.name,
                    'customer_id': str(self.partner_id.id),
                }
            )

            # Salvar ID
            self.stripe_payment_intent_id = intent['id']

            # Retornar client_secret para frontend
            return {
                'type': 'ir.actions.client',
                'tag': 'stripe_payment',
                'params': {
                    'client_secret': intent['client_secret'],
                    'publishable_key': provider.publishable_key,
                }
            }

        except Exception as e:
            _logger.error("Payment processing failed: %s", str(e))
            raise
```

### Exemplo 2: Shipping API (FedEx)

```python
class FedExShippingProvider(models.Model):
    _name = 'fedex.shipping.provider'
    _description = 'FedEx Shipping Provider'

    name = fields.Char('Name', default='FedEx')
    api_key = fields.Char('API Key', required=True)
    secret_key = fields.Char('Secret Key', required=True)
    account_number = fields.Char('Account Number', required=True)
    meter_number = fields.Char('Meter Number')

    base_url = fields.Char('Base URL', default='https://apis.fedex.com')

    # Cache de token OAuth
    access_token = fields.Char('Access Token')
    token_expires_at = fields.Datetime('Token Expires At')

    def _ensure_valid_token(self):
        """Garante token OAuth valido"""
        if not self.access_token or \
           not self.token_expires_at or \
           self.token_expires_at < fields.Datetime.now():
            self._refresh_token()

    def _refresh_token(self):
        """Obtem novo token OAuth"""
        url = f"{self.base_url}/oauth/token"

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key,
        }

        try:
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()

            token_data = response.json()

            self.write({
                'access_token': token_data['access_token'],
                'token_expires_at': fields.Datetime.now() + timedelta(
                    seconds=token_data['expires_in'] - 300  # 5 min buffer
                ),
            })

        except Exception as e:
            _logger.error("Failed to get FedEx token: %s", str(e))
            raise UserError("Failed to authenticate with FedEx")

    def _get_headers(self):
        """Retorna headers autenticados"""
        self._ensure_valid_token()

        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }

    def get_shipping_rates(self, pickup, delivery, packages):
        """
        Obtem tarifas de envio

        Args:
            pickup: dict com endereco de coleta
            delivery: dict com endereco de entrega
            packages: list de dicts com info dos pacotes

        Returns:
            list: Lista de opcoes de envio
        """
        url = f"{self.base_url}/rate/v1/rates/quotes"

        payload = {
            'accountNumber': {
                'value': self.account_number
            },
            'requestedShipment': {
                'shipper': {
                    'address': pickup
                },
                'recipient': {
                    'address': delivery
                },
                'pickupType': 'DROPOFF_AT_FEDEX_LOCATION',
                'serviceType': 'FEDEX_GROUND',
                'packagingType': 'YOUR_PACKAGING',
                'rateRequestType': ['LIST', 'ACCOUNT'],
                'requestedPackageLineItems': packages,
            }
        }

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            # Parse rates
            rates = []
            for rate_detail in data.get('output', {}).get('rateReplyDetails', []):
                rates.append({
                    'service': rate_detail['serviceType'],
                    'delivery_date': rate_detail.get('commit', {}).get('dateDetail', {}).get('dayFormat'),
                    'amount': rate_detail['ratedShipmentDetails'][0]['totalNetCharge'],
                    'currency': rate_detail['ratedShipmentDetails'][0]['currency'],
                })

            return rates

        except Exception as e:
            _logger.error("Failed to get FedEx rates: %s", str(e))
            raise UserError(f"Failed to get shipping rates: {str(e)}")

    def create_shipment(self, pickup, delivery, packages):
        """Cria envio no FedEx"""
        url = f"{self.base_url}/ship/v1/shipments"

        payload = {
            'accountNumber': {
                'value': self.account_number
            },
            'requestedShipment': {
                'shipper': pickup,
                'recipients': [delivery],
                'pickupType': 'DROPOFF_AT_FEDEX_LOCATION',
                'serviceType': 'FEDEX_GROUND',
                'packagingType': 'YOUR_PACKAGING',
                'shippingChargesPayment': {
                    'paymentType': 'SENDER'
                },
                'labelSpecification': {
                    'labelFormatType': 'COMMON2D',
                    'imageType': 'PDF',
                    'labelStockType': 'PAPER_4X6'
                },
                'requestedPackageLineItems': packages,
            }
        }

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            return {
                'tracking_number': data['output']['transactionShipments'][0]['masterTrackingNumber'],
                'label_url': data['output']['transactionShipments'][0]['pieceResponses'][0]['packageDocuments'][0]['url'],
            }

        except Exception as e:
            _logger.error("Failed to create FedEx shipment: %s", str(e))
            raise UserError(f"Failed to create shipment: {str(e)}")

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    fedex_tracking_number = fields.Char('FedEx Tracking Number')
    fedex_label_url = fields.Char('FedEx Label URL')

    def action_get_fedex_rates(self):
        """Obtem tarifas FedEx"""
        self.ensure_one()

        provider = self.env['fedex.shipping.provider'].search([], limit=1)
        if not provider:
            raise UserError("FedEx provider not configured")

        # Preparar dados
        pickup_address = self._prepare_pickup_address()
        delivery_address = self._prepare_delivery_address()
        packages = self._prepare_packages()

        # Obter tarifas
        rates = provider.get_shipping_rates(pickup_address, delivery_address, packages)

        # Mostrar rates em wizard
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'fedex.rate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_picking_id': self.id,
                'default_rates': rates,
            }
        }
```

### Exemplo 3: CRM Sync (HubSpot)

```python
class HubSpotConnector(models.Model):
    _name = 'hubspot.connector'
    _description = 'HubSpot Connector'

    name = fields.Char('Name', default='HubSpot')
    api_key = fields.Char('API Key', required=True)
    base_url = fields.Char('Base URL', default='https://api.hubapi.com')

    last_sync_date = fields.Datetime('Last Sync Date')
    sync_contacts = fields.Boolean('Sync Contacts', default=True)
    sync_companies = fields.Boolean('Sync Companies', default=True)
    sync_deals = fields.Boolean('Sync Deals', default=True)

    def _get_headers(self):
        """Retorna headers autenticados"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    def sync_all(self):
        """Sincroniza todos os dados"""
        self.ensure_one()

        try:
            if self.sync_contacts:
                self._sync_contacts()

            if self.sync_companies:
                self._sync_companies()

            if self.sync_deals:
                self._sync_deals()

            self.last_sync_date = fields.Datetime.now()

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sync Completed',
                    'message': 'HubSpot synchronization completed successfully',
                    'type': 'success',
                }
            }

        except Exception as e:
            _logger.error("HubSpot sync failed: %s", str(e))
            raise UserError(f"Sync failed: {str(e)}")

    def _sync_contacts(self):
        """Sincroniza contacts"""
        _logger.info("Syncing HubSpot contacts...")

        # Buscar contacts do HubSpot
        url = f"{self.base_url}/crm/v3/objects/contacts"

        params = {
            'limit': 100,
            'properties': 'firstname,lastname,email,phone,company',
        }

        if self.last_sync_date:
            # Buscar apenas contacts modificados desde ultima sync
            timestamp_ms = int(self.last_sync_date.timestamp() * 1000)
            params['filterGroups'] = json.dumps([{
                'filters': [{
                    'propertyName': 'lastmodifieddate',
                    'operator': 'GTE',
                    'value': timestamp_ms
                }]
            }])

        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            contacts = data.get('results', [])

            # Processar contacts
            for contact_data in contacts:
                self._process_hubspot_contact(contact_data)

            _logger.info("Synced %d contacts from HubSpot", len(contacts))

        except Exception as e:
            _logger.error("Failed to sync contacts: %s", str(e))
            raise

    def _process_hubspot_contact(self, contact_data):
        """Processa contact do HubSpot"""
        hubspot_id = contact_data['id']
        properties = contact_data['properties']

        # Buscar partner existente
        partner = self.env['res.partner'].search([
            ('hubspot_id', '=', hubspot_id)
        ], limit=1)

        vals = {
            'name': f"{properties.get('firstname', '')} {properties.get('lastname', '')}".strip(),
            'email': properties.get('email'),
            'phone': properties.get('phone'),
            'hubspot_id': hubspot_id,
        }

        if partner:
            # Atualizar existente
            partner.write(vals)
        else:
            # Criar novo
            self.env['res.partner'].create(vals)

    def create_hubspot_contact(self, partner):
        """Cria contact no HubSpot"""
        url = f"{self.base_url}/crm/v3/objects/contacts"

        payload = {
            'properties': {
                'firstname': partner.name.split()[0] if partner.name else '',
                'lastname': ' '.join(partner.name.split()[1:]) if partner.name else '',
                'email': partner.email or '',
                'phone': partner.phone or '',
                'company': partner.parent_id.name if partner.parent_id else '',
            }
        }

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            # Salvar ID do HubSpot
            partner.hubspot_id = data['id']

            return data

        except Exception as e:
            _logger.error("Failed to create HubSpot contact: %s", str(e))
            raise UserError(f"Failed to create contact in HubSpot: {str(e)}")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    hubspot_id = fields.Char('HubSpot ID', readonly=True, copy=False)

    def write(self, vals):
        """Sincronizar mudancas com HubSpot"""
        result = super().write(vals)

        # Se partner tem HubSpot ID, atualizar no HubSpot
        for partner in self:
            if partner.hubspot_id:
                connector = self.env['hubspot.connector'].search([], limit=1)
                if connector:
                    connector._update_hubspot_contact(partner, vals)

        return result
```

---

## Security Best Practices

### 1. Armazenamento Seguro de Credenciais

```python
class SecureAPIConnector(models.Model):
    _name = 'secure.api.connector'
    _description = 'Secure API Connector'

    name = fields.Char('Name')

    # NUNCA armazenar credenciais em plain text
    # Opcao 1: Usar ir.config_parameter (sudo protected)
    @property
    def api_key(self):
        """Obtem API key do config parameter"""
        return self.env['ir.config_parameter'].sudo().get_param(
            f'{self._name}.api_key.{self.id}'
        )

    def set_api_key(self, api_key):
        """Salva API key de forma segura"""
        self.env['ir.config_parameter'].sudo().set_param(
            f'{self._name}.api_key.{self.id}',
            api_key
        )

    # Opcao 2: Encriptar credenciais
    api_key_encrypted = fields.Char('API Key (Encrypted)')

    def _encrypt_value(self, value):
        """Encripta valor usando Fernet"""
        from cryptography.fernet import Fernet

        # Obter chave de encriptacao (armazenada separadamente)
        key = self._get_encryption_key()
        f = Fernet(key)

        return f.encrypt(value.encode()).decode()

    def _decrypt_value(self, encrypted_value):
        """Decripta valor"""
        from cryptography.fernet import Fernet

        key = self._get_encryption_key()
        f = Fernet(key)

        return f.decrypt(encrypted_value.encode()).decode()

    def _get_encryption_key(self):
        """Obtem chave de encriptacao"""
        # IMPORTANTE: Chave deve ser gerada uma vez e armazenada de forma segura
        # Opcoes:
        # 1. Variavel de ambiente
        # 2. Arquivo de configuracao fora do odoo
        # 3. Key management service (AWS KMS, Azure Key Vault, etc)
        import os
        return os.environ.get('ODOO_ENCRYPTION_KEY', '').encode()
```

### 2. Rate Limiting

```python
class RateLimitedAPI(models.Model):
    _name = 'rate.limited.api'
    _description = 'Rate Limited API'

    def _check_rate_limit(self, max_requests=100, per_seconds=60):
        """
        Verifica rate limit antes de fazer requisicao

        Args:
            max_requests: Numero maximo de requisicoes
            per_seconds: Periodo de tempo (segundos)

        Raises:
            UserError: Se rate limit foi excedido
        """
        cache_key = f'rate_limit_{self._name}_{self.id}'

        # Obter historico de requests
        requests_json = self.env['ir.config_parameter'].sudo().get_param(
            cache_key, '[]'
        )

        try:
            requests_list = json.loads(requests_json)
        except:
            requests_list = []

        now = time.time()

        # Limpar requests antigos
        requests_list = [ts for ts in requests_list if now - ts < per_seconds]

        # Verificar limite
        if len(requests_list) >= max_requests:
            oldest = min(requests_list)
            wait_time = per_seconds - (now - oldest)

            raise UserError(
                f"Rate limit exceeded. Please wait {int(wait_time)} seconds."
            )

        # Registrar novo request
        requests_list.append(now)

        # Salvar
        self.env['ir.config_parameter'].sudo().set_param(
            cache_key,
            json.dumps(requests_list)
        )
```

### 3. Input Validation e Sanitization

```python
class SecureAPIInput(models.Model):
    _name = 'secure.api.input'
    _description = 'Secure API Input'

    def _validate_email(self, email):
        """Valida formato de email"""
        import re

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(pattern, email):
            raise UserError("Invalid email format")

        return email

    def _sanitize_string(self, value, max_length=255):
        """Sanitiza string input"""
        if not isinstance(value, str):
            raise UserError("Expected string value")

        # Remover caracteres perigosos
        import html
        value = html.escape(value)

        # Limitar tamanho
        if len(value) > max_length:
            raise UserError(f"String too long (max {max_length} characters)")

        return value

    def _validate_url(self, url):
        """Valida URL"""
        from urllib.parse import urlparse

        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError

            # Apenas HTTPS
            if result.scheme != 'https':
                raise UserError("Only HTTPS URLs are allowed")

            return url

        except:
            raise UserError("Invalid URL format")

    def _validate_api_request_data(self, data, schema):
        """
        Valida dados antes de enviar para API

        Args:
            data: Dados a validar
            schema: Schema de validacao

        Example schema:
        {
            'email': {'type': 'email', 'required': True},
            'name': {'type': 'string', 'max_length': 100, 'required': True},
            'age': {'type': 'int', 'min': 0, 'max': 150},
        }
        """
        validated = {}

        for field, rules in schema.items():
            value = data.get(field)

            # Check required
            if rules.get('required') and not value:
                raise UserError(f"Field '{field}' is required")

            if value is None:
                continue

            # Validate by type
            field_type = rules.get('type')

            if field_type == 'email':
                validated[field] = self._validate_email(value)

            elif field_type == 'string':
                max_length = rules.get('max_length', 255)
                validated[field] = self._sanitize_string(value, max_length)

            elif field_type == 'int':
                if not isinstance(value, int):
                    raise UserError(f"Field '{field}' must be an integer")

                min_val = rules.get('min')
                max_val = rules.get('max')

                if min_val is not None and value < min_val:
                    raise UserError(f"Field '{field}' must be >= {min_val}")

                if max_val is not None and value > max_val:
                    raise UserError(f"Field '{field}' must be <= {max_val}")

                validated[field] = value

            elif field_type == 'url':
                validated[field] = self._validate_url(value)

        return validated
```

### 4. HTTPS Only

```python
class HTTPSOnlyAPI(models.Model):
    _name = 'https.only.api'
    _description = 'HTTPS Only API'

    def _make_secure_request(self, url, **kwargs):
        """Garante que apenas HTTPS e usado"""
        from urllib.parse import urlparse

        parsed = urlparse(url)

        if parsed.scheme != 'https':
            raise UserError("Only HTTPS connections are allowed")

        # Verificar certificado SSL
        kwargs.setdefault('verify', True)

        return requests.request('GET', url, **kwargs)
```

---

## Testing Integrations

### 1. Mock API Responses

```python
from unittest.mock import patch, Mock
from odoo.tests import TransactionCase

class TestAPIIntegration(TransactionCase):

    def setUp(self):
        super().setUp()
        self.connector = self.env['external.api.connector'].create({
            'name': 'Test API',
            'base_url': 'https://api.example.com',
            'api_key': 'test_key',
        })

    @patch('requests.get')
    def test_get_request_success(self, mock_get):
        """Test successful GET request"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 1, 'name': 'Test'}
        mock_get.return_value = mock_response

        # Execute
        result = self.connector._make_get_request('/users/1')

        # Assert
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['name'], 'Test')

        # Verify call
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_request_error(self, mock_get):
        """Test GET request with error"""
        # Setup mock to raise exception
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        # Execute and assert exception
        with self.assertRaises(UserError):
            self.connector._make_get_request('/users/1')

    @patch('requests.post')
    def test_post_request_with_data(self, mock_post):
        """Test POST request with data"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 1, 'created': True}
        mock_post.return_value = mock_response

        # Execute
        data = {'name': 'New User', 'email': 'user@example.com'}
        result = self.connector._make_post_request('/users', json_data=data)

        # Assert
        self.assertTrue(result['created'])

        # Verify call with correct data
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args[1]
        self.assertEqual(call_kwargs['json'], data)
```

### 2. Integration Tests com API de Sandbox

```python
class TestPaymentGatewayIntegration(TransactionCase):

    def setUp(self):
        super().setUp()

        # Usar credentials de sandbox
        self.provider = self.env['stripe.payment.provider'].create({
            'name': 'Stripe Test',
            'secret_key': 'sk_test_...',  # Sandbox key
            'publishable_key': 'pk_test_...',  # Sandbox key
            'base_url': 'https://api.stripe.com/v1',
        })

    def test_create_payment_intent_sandbox(self):
        """Test creating payment intent in sandbox"""
        # Execute
        result = self.provider.create_payment_intent(
            amount=100.00,
            currency='usd',
            metadata={'test': 'true'}
        )

        # Assert
        self.assertTrue(result.get('id'))
        self.assertTrue(result['id'].startswith('pi_'))
        self.assertEqual(result['amount'], 10000)  # In cents
        self.assertEqual(result['currency'], 'usd')

    def test_payment_flow_end_to_end(self):
        """Test complete payment flow"""
        # 1. Create order
        order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'order_line': [(0, 0, {
                'name': 'Test Product',
                'product_uom_qty': 1,
                'price_unit': 100,
            })],
        })

        # 2. Create payment intent
        intent = self.provider.create_payment_intent(
            amount=order.amount_total,
            metadata={'order_id': order.name}
        )

        order.stripe_payment_intent_id = intent['id']

        # 3. Simulate payment confirmation (via webhook)
        # ... webhook logic ...

        # 4. Verify order state
        # ...
```

### 3. Test de Timeout

```python
class TestAPITimeout(TransactionCase):

    @patch('requests.get')
    def test_request_timeout(self, mock_get):
        """Test request timeout handling"""
        # Setup mock to timeout
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")

        connector = self.env['external.api.connector'].create({
            'name': 'Test',
            'base_url': 'https://api.example.com',
            'timeout': 5,
        })

        # Execute and assert
        with self.assertRaises(UserError) as context:
            connector._make_get_request('/slow-endpoint')

        self.assertIn('timeout', str(context.exception).lower())
```

### 4. Test de Retry Logic

```python
class TestRetryLogic(TransactionCase):

    @patch('time.sleep')  # Mock sleep para acelerar teste
    @patch('requests.get')
    def test_retry_on_failure(self, mock_get, mock_sleep):
        """Test retry logic"""
        # Setup mock to fail 2 times, then succeed
        mock_response_fail = Mock()
        mock_response_fail.status_code = 500
        mock_response_fail.raise_for_status.side_effect = requests.exceptions.HTTPError()

        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {'success': True}

        mock_get.side_effect = [
            mock_response_fail,
            mock_response_fail,
            mock_response_success,
        ]

        connector = self.env['exponential.backoff.retry'].create({
            'name': 'Test',
        })

        # Execute
        result = connector._make_request_with_exponential_backoff(
            'https://api.example.com/endpoint',
            max_retries=3
        )

        # Assert
        self.assertEqual(result, {'success': True})
        self.assertEqual(mock_get.call_count, 3)  # 2 failures + 1 success
        self.assertEqual(mock_sleep.call_count, 2)  # 2 retries
```

---

## Conclusao

Integracoes com APIs externas requerem atencao especial a:

1. **Autenticacao Segura**: Use metodos apropriados e armazene credenciais com seguranca
2. **Error Handling**: Trate todos os tipos de erros possiveis
3. **Retry Logic**: Implemente retry com exponential backoff para requisicoes falhadas
4. **Rate Limiting**: Respeite limites das APIs externas
5. **Logging**: Mantenha logs detalhados para debug
6. **Webhooks**: Implemente endpoints seguros para receber dados
7. **Queue Systems**: Use processamento assincrono para operacoes pesadas
8. **Testing**: Teste extensivamente com mocks e sandboxes
9. **Monitoring**: Monitore health e performance das integracoes
10. **Security**: Valide inputs, use HTTPS, proteja credenciais

Com estas praticas, suas integracoes serao robustas, seguras e manuteníveis!

### Referencias Uteis:

- Requests documentation: https://docs.python-requests.org/
- OAuth 2.0: https://oauth.net/2/
- JWT: https://jwt.io/
- Stripe API: https://stripe.com/docs/api
- FedEx API: https://developer.fedex.com/
- HubSpot API: https://developers.hubspot.com/
- OCA Queue Job: https://github.com/OCA/queue
