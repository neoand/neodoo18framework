# -*- coding: utf-8 -*-
"""
===============================================================================
CONFIGURATION SETTINGS EXAMPLE - ODOO 18
===============================================================================

Este arquivo demonstra como criar configurações personalizadas no Odoo 18.

O modelo res.config.settings permite criar páginas de configuração acessíveis
em Settings > Technical > Settings ou em módulos específicos.

TIPOS DE CONFIGURAÇÃO:
----------------------

1. CONFIG PARAMETERS (ir.config_parameter):
   - Armazenados na tabela ir_config_parameter
   - Escopo global (todas as empresas)
   - Usar config_parameter='nome.do.parametro'
   - Acesso: env['ir.config_parameter'].get_param('nome')

2. COMPANY FIELDS:
   - Armazenados em res.company
   - Escopo por empresa
   - Usar related='company_id.campo'
   - Acesso: company.campo

3. MODEL FIELDS:
   - Armazenados em qualquer modelo
   - Usar related='model_id.campo'
   - Acesso: model.campo

MÉTODOS PRINCIPAIS:
-------------------

- get_values(): Carrega valores salvos
- set_values(): Salva valores
- execute(): Executa ação (botões)

NOTA IMPORTANTE:
----------------
No Odoo 18, o TransientModel res.config.settings não persiste dados
diretamente. Os valores são salvos em:
- ir.config_parameter (para configs globais)
- res.company (para configs por empresa)
- Outros modelos (para configs específicas)

"""

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ResConfigSettings(models.TransientModel):
    """
    Configurações personalizadas do módulo de exemplo.

    Este modelo estende res.config.settings para adicionar configurações
    específicas do módulo.
    """
    _inherit = 'res.config.settings'

    # =========================================================================
    # COMPANY SETTINGS - Configurações por Empresa
    # =========================================================================
    # Estes campos são armazenados em res.company e têm escopo por empresa

    # -------------------------------------------------------------------------
    # Boolean Fields
    # -------------------------------------------------------------------------

    # Campo booleano simples
    company_enable_feature_x = fields.Boolean(
        string='Enable Feature X',
        related='company_id.enable_feature_x',  # Campo em res.company
        readonly=False,  # Permite edição
        help="Enable or disable Feature X for this company.\n"
             "When enabled, users will be able to use advanced features."
    )

    # Campo booleano com valor padrão
    company_auto_backup = fields.Boolean(
        string='Automatic Backup',
        related='company_id.auto_backup',
        readonly=False,
        default=True,
        help="Automatically backup data every day."
    )

    # Campo booleano que afeta outros campos
    company_use_custom_workflow = fields.Boolean(
        string='Use Custom Workflow',
        related='company_id.use_custom_workflow',
        readonly=False,
        help="Enable custom approval workflow for sales orders.\n"
             "When enabled, orders above a certain amount will require approval."
    )

    # -------------------------------------------------------------------------
    # Selection Fields
    # -------------------------------------------------------------------------

    # Campo de seleção
    company_invoice_policy = fields.Selection(
        [
            ('ordered', 'Ordered Quantities'),
            ('delivered', 'Delivered Quantities'),
        ],
        string='Default Invoice Policy',
        related='company_id.invoice_policy',
        readonly=False,
        default='ordered',
        required=True,
        help="Choose the default invoicing policy:\n"
             "- Ordered: Invoice based on ordered quantities\n"
             "- Delivered: Invoice based on delivered quantities"
    )

    # Campo de seleção com mais opções
    company_approval_level = fields.Selection(
        [
            ('none', 'No Approval'),
            ('manager', 'Manager Approval'),
            ('director', 'Director Approval'),
            ('ceo', 'CEO Approval'),
        ],
        string='Required Approval Level',
        related='company_id.approval_level',
        readonly=False,
        default='manager',
        help="Set the required approval level for large orders."
    )

    # -------------------------------------------------------------------------
    # Numeric Fields
    # -------------------------------------------------------------------------

    # Campo integer
    company_credit_days = fields.Integer(
        string='Default Credit Days',
        related='company_id.credit_days',
        readonly=False,
        default=30,
        help="Default number of days for customer credit.\n"
             "This will be used when creating new payment terms."
    )

    # Campo float
    company_discount_limit = fields.Float(
        string='Maximum Discount (%)',
        related='company_id.discount_limit',
        readonly=False,
        default=10.0,
        digits=(3, 2),  # Precisão: 3 dígitos totais, 2 decimais
        help="Maximum discount percentage that sales team can apply.\n"
             "Higher discounts will require manager approval."
    )

    # Campo monetary
    company_approval_amount = fields.Monetary(
        string='Approval Required Above',
        related='company_id.approval_amount',
        readonly=False,
        currency_field='company_currency_id',  # Campo de moeda
        help="Orders above this amount will require approval.\n"
             "Leave as 0 to disable automatic approval workflow."
    )

    # Campo de moeda (auxiliar para monetary)
    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True,
        string='Company Currency',
    )

    # -------------------------------------------------------------------------
    # Many2one Fields (Relational)
    # -------------------------------------------------------------------------

    # Relação Many2one simples
    company_default_warehouse = fields.Many2one(
        'stock.warehouse',
        string='Default Warehouse',
        related='company_id.default_warehouse_id',
        readonly=False,
        help="Default warehouse for this company."
    )

    # Relação Many2one com domínio
    company_default_salesperson = fields.Many2one(
        'res.users',
        string='Default Salesperson',
        related='company_id.default_salesperson_id',
        readonly=False,
        domain=[('share', '=', False)],  # Apenas usuários internos
        help="Default salesperson for new orders.\n"
             "Can be overridden on individual orders."
    )

    # Relação Many2one com domínio dinâmico
    company_default_payment_term = fields.Many2one(
        'account.payment.term',
        string='Default Payment Terms',
        related='company_id.default_payment_term_id',
        readonly=False,
        help="Default payment terms for customer invoices."
    )

    # -------------------------------------------------------------------------
    # Text Fields
    # -------------------------------------------------------------------------

    # Campo Char
    company_api_key = fields.Char(
        string='API Key',
        related='company_id.api_key',
        readonly=False,
        help="API key for external integrations.\n"
             "Keep this secret and secure."
    )

    # Campo Text
    company_terms_conditions = fields.Text(
        string='Default Terms and Conditions',
        related='company_id.terms_conditions',
        readonly=False,
        help="Default terms and conditions to include in quotations and invoices."
    )

    # Campo Html
    company_email_footer = fields.Html(
        string='Email Footer',
        related='company_id.email_footer',
        readonly=False,
        sanitize=True,  # Sanitizar HTML
        help="Custom footer to include in all company emails."
    )

    # =========================================================================
    # CONFIG PARAMETERS - Configurações Globais (todas as empresas)
    # =========================================================================
    # Estes campos são armazenados em ir.config_parameter

    # Boolean config parameter
    module_enable_debug_mode = fields.Boolean(
        string='Enable Debug Mode',
        config_parameter='example_module.enable_debug_mode',
        help="Enable debug mode for troubleshooting.\n"
             "WARNING: This may slow down the system."
    )

    # Boolean para ativar/desativar módulo relacionado
    module_advanced_features = fields.Boolean(
        string='Advanced Features',
        config_parameter='example_module.advanced_features',
        help="Enable advanced features module."
    )

    # Char config parameter
    module_api_endpoint = fields.Char(
        string='API Endpoint URL',
        config_parameter='example_module.api_endpoint',
        default='https://api.example.com',
        help="External API endpoint URL for integrations."
    )

    # Integer config parameter
    module_max_retries = fields.Integer(
        string='Maximum Retry Attempts',
        config_parameter='example_module.max_retries',
        default=3,
        help="Maximum number of retry attempts for failed operations."
    )

    # Float config parameter
    module_timeout_seconds = fields.Float(
        string='Request Timeout (seconds)',
        config_parameter='example_module.timeout_seconds',
        default=30.0,
        help="Timeout in seconds for external API requests."
    )

    # Selection config parameter
    module_log_level = fields.Selection(
        [
            ('debug', 'Debug'),
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('error', 'Error'),
        ],
        string='Log Level',
        config_parameter='example_module.log_level',
        default='info',
        help="Logging level for the module."
    )

    # =========================================================================
    # COMPUTED FIELDS - Campos Calculados
    # =========================================================================

    # Campo computed baseado em outros campos
    show_approval_settings = fields.Boolean(
        string='Show Approval Settings',
        compute='_compute_show_approval_settings',
        help="Technical field to control visibility of approval settings."
    )

    # Campo computed com dados de outro modelo
    pending_approvals_count = fields.Integer(
        string='Pending Approvals',
        compute='_compute_pending_approvals_count',
        help="Number of orders pending approval."
    )

    # =========================================================================
    # DEPENDENT FIELDS - Campos com visibilidade condicional
    # =========================================================================
    # Estes campos só aparecem quando certas condições são atendidas

    # Campo visível apenas se workflow customizado estiver ativo
    company_approval_chain = fields.Many2many(
        'res.users',
        string='Approval Chain',
        related='company_id.approval_chain_ids',
        readonly=False,
        help="Users in the approval chain (in order).\n"
             "Only visible when custom workflow is enabled."
    )

    # =========================================================================
    # COMPUTE METHODS
    # =========================================================================

    @api.depends('company_use_custom_workflow')
    def _compute_show_approval_settings(self):
        """
        Determina se deve mostrar configurações de aprovação.

        Este campo computed é usado para controlar a visibilidade
        de outros campos na view (attrs='invisible': [('show_approval_settings', '=', False)])
        """
        for record in self:
            record.show_approval_settings = record.company_use_custom_workflow

    def _compute_pending_approvals_count(self):
        """
        Calcula o número de aprovações pendentes.

        Este é um exemplo de campo computed que busca dados de outro modelo
        para exibir na página de configurações.
        """
        for record in self:
            # Buscar pedidos pendentes de aprovação
            pending_orders = self.env['sale.order'].search_count([
                ('company_id', '=', record.company_id.id),
                ('state', '=', 'pending_approval'),
            ])
            record.pending_approvals_count = pending_orders

    # =========================================================================
    # ONCHANGE METHODS
    # =========================================================================

    @api.onchange('company_use_custom_workflow')
    def _onchange_use_custom_workflow(self):
        """
        Executado quando o campo 'use_custom_workflow' é alterado na UI.

        Usado para atualizar outros campos ou mostrar avisos ao usuário.
        """
        if self.company_use_custom_workflow:
            # Se ativando workflow, definir valores padrão
            if not self.company_approval_amount:
                self.company_approval_amount = 10000.0

            if not self.company_approval_level:
                self.company_approval_level = 'manager'

            # Retornar mensagem de aviso
            return {
                'warning': {
                    'title': _('Custom Workflow Enabled'),
                    'message': _(
                        'Custom approval workflow has been enabled.\n'
                        'Please configure approval amount and level below.'
                    ),
                }
            }

    @api.onchange('company_approval_amount')
    def _onchange_approval_amount(self):
        """
        Validar o valor do campo approval_amount quando alterado.
        """
        if self.company_approval_amount and self.company_approval_amount < 0:
            self.company_approval_amount = 0
            return {
                'warning': {
                    'title': _('Invalid Amount'),
                    'message': _('Approval amount cannot be negative.'),
                }
            }

    @api.onchange('module_enable_debug_mode')
    def _onchange_debug_mode(self):
        """
        Avisar ao ativar modo debug.
        """
        if self.module_enable_debug_mode:
            return {
                'warning': {
                    'title': _('Debug Mode'),
                    'message': _(
                        'Debug mode will be enabled.\n'
                        'This may slow down the system and expose sensitive information.\n'
                        'Use only for troubleshooting.'
                    ),
                }
            }

    # =========================================================================
    # CONSTRAINT METHODS
    # =========================================================================

    @api.constrains('company_discount_limit')
    def _check_discount_limit(self):
        """
        Validar limite de desconto.

        Constraints são executados ao salvar o registro.
        """
        for record in self:
            if record.company_discount_limit < 0:
                raise ValidationError(_(
                    'Discount limit cannot be negative.'
                ))
            if record.company_discount_limit > 100:
                raise ValidationError(_(
                    'Discount limit cannot exceed 100%%.'
                ))

    @api.constrains('company_credit_days')
    def _check_credit_days(self):
        """
        Validar dias de crédito.
        """
        for record in self:
            if record.company_credit_days < 0:
                raise ValidationError(_(
                    'Credit days cannot be negative.'
                ))
            if record.company_credit_days > 365:
                raise ValidationError(_(
                    'Credit days cannot exceed 365 days (1 year).'
                ))

    # =========================================================================
    # OVERRIDE METHODS - get_values() e set_values()
    # =========================================================================

    @api.model
    def get_values(self):
        """
        Carregar valores das configurações.

        Este método é chamado quando a página de configurações é aberta.
        Usado para carregar valores de config parameters ou fazer
        processamentos especiais.

        IMPORTANTE: Sempre chamar super() para manter funcionalidade padrão!
        """
        res = super(ResConfigSettings, self).get_values()

        # Obter parâmetros de configuração
        IrConfigParam = self.env['ir.config_parameter'].sudo()

        # Exemplo: carregar valor com processamento
        api_key = IrConfigParam.get_param('example_module.api_key_encrypted', default='')
        if api_key:
            # Descriptografar API key (exemplo)
            # api_key = decrypt(api_key)
            pass

        # Exemplo: valores computed ou processados
        res.update({
            # Adicionar valores customizados se necessário
            # 'custom_field': self._get_custom_value(),
        })

        return res

    def set_values(self):
        """
        Salvar valores das configurações.

        Este método é chamado quando o usuário clica em 'Save' na página
        de configurações. Usado para salvar config parameters ou fazer
        processamentos especiais antes de salvar.

        IMPORTANTE: Sempre chamar super() para manter funcionalidade padrão!
        """
        super(ResConfigSettings, self).set_values()

        # Obter parâmetros de configuração
        IrConfigParam = self.env['ir.config_parameter'].sudo()

        # Exemplo: salvar com processamento
        if hasattr(self, 'module_api_key') and self.module_api_key:
            # Criptografar API key antes de salvar (exemplo)
            # encrypted_key = encrypt(self.module_api_key)
            # IrConfigParam.set_param('example_module.api_key_encrypted', encrypted_key)
            pass

        # Exemplo: executar ação após salvar
        if self.company_use_custom_workflow:
            self._setup_approval_workflow()

        # Exemplo: invalidar cache
        if self.module_enable_debug_mode:
            self.env.registry.clear_cache()

    # =========================================================================
    # ACTION METHODS - Métodos para botões
    # =========================================================================

    def action_test_api_connection(self):
        """
        Testar conexão com API externa.

        Este método pode ser chamado por um botão na view de configurações.
        Usa type='object' no botão XML.
        """
        self.ensure_one()

        try:
            # Testar conexão (exemplo)
            endpoint = self.module_api_endpoint
            if not endpoint:
                raise UserError(_('Please configure API endpoint first.'))

            # import requests
            # response = requests.get(endpoint, timeout=5)
            # response.raise_for_status()

            # Simulação de sucesso
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Connection Successful'),
                    'message': _('Successfully connected to API endpoint.'),
                    'type': 'success',
                    'sticky': False,
                }
            }

        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Connection Failed'),
                    'message': _('Failed to connect to API: %s') % str(e),
                    'type': 'danger',
                    'sticky': True,
                }
            }

    def action_reset_to_defaults(self):
        """
        Resetar configurações para valores padrão.

        Exemplo de action que pode ser chamada por um botão.
        """
        self.ensure_one()

        # Confirmar ação
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reset to Defaults'),
            'res_model': 'config.reset.wizard',  # Wizard de confirmação
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_config_id': self.id,
            }
        }

    def action_view_pending_approvals(self):
        """
        Abrir lista de aprovações pendentes.

        Exemplo de action que abre outra view.
        """
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': _('Pending Approvals'),
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [
                ('company_id', '=', self.company_id.id),
                ('state', '=', 'pending_approval'),
            ],
            'context': {
                'create': False,  # Não permitir criar
            }
        }

    # =========================================================================
    # HELPER METHODS - Métodos Auxiliares
    # =========================================================================

    def _setup_approval_workflow(self):
        """
        Configurar workflow de aprovação.

        Método auxiliar privado chamado após salvar configurações.
        """
        self.ensure_one()

        # Criar ou atualizar regras de aprovação
        ApprovalRule = self.env['approval.rule']

        # Buscar regra existente
        rule = ApprovalRule.search([
            ('company_id', '=', self.company_id.id),
        ], limit=1)

        # Valores da regra
        rule_vals = {
            'company_id': self.company_id.id,
            'approval_amount': self.company_approval_amount,
            'approval_level': self.company_approval_level,
            'active': True,
        }

        if rule:
            # Atualizar existente
            rule.write(rule_vals)
        else:
            # Criar nova
            ApprovalRule.create(rule_vals)

    def _get_custom_value(self):
        """
        Obter valor customizado.

        Exemplo de método auxiliar para processar dados.
        """
        self.ensure_one()

        # Processar e retornar valor
        return "Custom Value"

    @api.model
    def _get_api_timeout(self):
        """
        Obter timeout da API.

        Método estático (model) para obter configuração.
        Pode ser chamado de qualquer lugar: env['res.config.settings']._get_api_timeout()
        """
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        timeout = IrConfigParam.get_param(
            'example_module.timeout_seconds',
            default='30.0'
        )
        return float(timeout)

    @api.model
    def _is_debug_mode_enabled(self):
        """
        Verificar se modo debug está ativo.

        Exemplo de método utilitário estático.
        """
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        return IrConfigParam.get_param(
            'example_module.enable_debug_mode',
            default='False'
        ) == 'True'

    # =========================================================================
    # CRON / SCHEDULED ACTIONS
    # =========================================================================

    @api.model
    def cron_cleanup_old_configs(self):
        """
        Limpeza periódica de configurações antigas.

        Este método pode ser chamado por um cron job (ir.cron).
        Usar @api.model para métodos de cron.
        """
        # Exemplo: limpar logs antigos
        # old_logs = self.env['config.log'].search([
        #     ('create_date', '<', fields.Datetime.subtract(fields.Datetime.now(), days=90))
        # ])
        # old_logs.unlink()

        return True


class ResCompany(models.Model):
    """
    Estender res.company para adicionar campos de configuração.

    Estes campos armazenam os valores reais das configurações por empresa.
    """
    _inherit = 'res.company'

    # Campos booleanos
    enable_feature_x = fields.Boolean(
        string='Enable Feature X',
        default=False,
    )

    auto_backup = fields.Boolean(
        string='Automatic Backup',
        default=True,
    )

    use_custom_workflow = fields.Boolean(
        string='Use Custom Workflow',
        default=False,
    )

    # Campos de seleção
    invoice_policy = fields.Selection(
        [
            ('ordered', 'Ordered Quantities'),
            ('delivered', 'Delivered Quantities'),
        ],
        string='Default Invoice Policy',
        default='ordered',
        required=True,
    )

    approval_level = fields.Selection(
        [
            ('none', 'No Approval'),
            ('manager', 'Manager Approval'),
            ('director', 'Director Approval'),
            ('ceo', 'CEO Approval'),
        ],
        string='Required Approval Level',
        default='manager',
    )

    # Campos numéricos
    credit_days = fields.Integer(
        string='Default Credit Days',
        default=30,
    )

    discount_limit = fields.Float(
        string='Maximum Discount (%)',
        default=10.0,
        digits=(3, 2),
    )

    approval_amount = fields.Monetary(
        string='Approval Required Above',
        currency_field='currency_id',
        default=0.0,
    )

    # Campos relacionais
    default_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Default Warehouse',
    )

    default_salesperson_id = fields.Many2one(
        'res.users',
        string='Default Salesperson',
        domain=[('share', '=', False)],
    )

    default_payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Default Payment Terms',
    )

    approval_chain_ids = fields.Many2many(
        'res.users',
        'company_approval_chain_rel',
        'company_id',
        'user_id',
        string='Approval Chain',
    )

    # Campos de texto
    api_key = fields.Char(
        string='API Key',
    )

    terms_conditions = fields.Text(
        string='Default Terms and Conditions',
    )

    email_footer = fields.Html(
        string='Email Footer',
        sanitize=True,
    )


# =============================================================================
# EXEMPLO DE USO EM OUTROS MODELOS
# =============================================================================

class SaleOrder(models.Model):
    """
    Exemplo de como usar as configurações em outros modelos.
    """
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        """
        Aplicar configurações ao criar pedido.
        """
        # Obter configurações da empresa
        company = self.env.company

        # Aplicar política de faturamento padrão
        if 'invoice_policy' not in vals:
            vals['invoice_policy'] = company.invoice_policy

        # Aplicar vendedor padrão
        if 'user_id' not in vals and company.default_salesperson_id:
            vals['user_id'] = company.default_salesperson_id.id

        # Aplicar prazo de pagamento padrão
        if 'payment_term_id' not in vals and company.default_payment_term_id:
            vals['payment_term_id'] = company.default_payment_term_id.id

        return super(SaleOrder, self).create(vals)

    def action_confirm(self):
        """
        Verificar se requer aprovação ao confirmar.
        """
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            # Verificar se usa workflow customizado
            if order.company_id.use_custom_workflow:
                # Verificar se valor requer aprovação
                if order.amount_total >= order.company_id.approval_amount:
                    # Enviar para aprovação ao invés de confirmar
                    order.state = 'pending_approval'
                    order._create_approval_activity()

        return res

    def _create_approval_activity(self):
        """
        Criar atividade de aprovação.
        """
        self.ensure_one()

        # Determinar aprovador baseado no nível
        approver = self._get_approver()

        if approver:
            self.activity_schedule(
                'mail.mail_activity_data_warning',
                summary=_('Order Approval Required'),
                note=_('Order %s requires approval (amount: %s)') % (
                    self.name,
                    '{:,.2f}'.format(self.amount_total)
                ),
                user_id=approver.id,
            )

    def _get_approver(self):
        """
        Obter aprovador baseado no nível de aprovação.
        """
        self.ensure_one()

        approval_level = self.company_id.approval_level

        if approval_level == 'manager':
            return self.team_id.user_id
        elif approval_level == 'director':
            # Buscar diretor
            return self.env.ref('base.group_erp_manager').users[:1]
        elif approval_level == 'ceo':
            # Buscar CEO
            return self.company_id.partner_id.user_id

        return False
