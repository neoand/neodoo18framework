# Workflows e State Machines no Odoo 18

## Indice

1. [Introducao](#introducao)
2. [Conceitos Basicos](#conceitos-basicos)
3. [Implementacao de State Machines](#implementacao-de-state-machines)
4. [Transicoes de Estado](#transicoes-de-estado)
5. [Buttons e Actions](#buttons-e-actions)
6. [Tracking de Mudancas](#tracking-de-mudancas)
7. [Record Rules por Estado](#record-rules-por-estado)
8. [Exemplos Praticos](#exemplos-praticos)
9. [Best Practices](#best-practices)
10. [Diagramas de Estado](#diagramas-de-estado)

---

## Introducao

State Machines (Maquinas de Estado) sao padroes de design fundamentais no Odoo para gerenciar workflows de negocios. Elas permitem controlar o ciclo de vida de registros, definindo estados possiveis e as transicoes permitidas entre eles.

### Casos de Uso Comuns
- Processos de aprovacao
- Ciclo de vendas (quotation → sale → delivery → invoice)
- Gestao de projetos (draft → in progress → done → cancelled)
- Processos de fabricacao
- Workflows de RH (recrutamento, ferias, avaliacoes)

---

## Conceitos Basicos

### O que e uma State Machine?

Uma State Machine e um modelo computacional que define:
- **Estados**: Situacoes possiveis de um registro
- **Transicoes**: Mudancas permitidas entre estados
- **Eventos**: Acoes que disparam transicoes
- **Validacoes**: Regras que controlam as transicoes

### Diagrama Conceitual

```
┌──────────┐    action_confirm()    ┌───────────┐
│  DRAFT   │ ──────────────────────> │ CONFIRMED │
└──────────┘                         └───────────┘
     │                                      │
     │ action_cancel()                      │ action_done()
     │                                      │
     v                                      v
┌──────────┐                         ┌───────────┐
│ CANCELLED│                         │   DONE    │
└──────────┘                         └───────────┘
```

---

## Implementacao de State Machines

### 1. Definindo Estados com Selection Field

```python
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _name = 'sale.order'
    _description = 'Sales Order'

    # Campo de estado - nucleo da state machine
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status',
       readonly=True,
       copy=False,
       index=True,
       tracking=True,  # Rastrear mudancas no chatter
       default='draft')

    # Campos relacionados ao workflow
    name = fields.Char('Order Reference', required=True, default='New')
    user_id = fields.Many2one('res.users', 'Salesperson', default=lambda self: self.env.user)
    date_order = fields.Datetime('Order Date', default=fields.Datetime.now)

    # Campos computados baseados no estado
    is_editable = fields.Boolean(
        'Is Editable',
        compute='_compute_is_editable',
        store=False
    )

    @api.depends('state')
    def _compute_is_editable(self):
        """Registros so podem ser editados em certos estados"""
        for record in self:
            record.is_editable = record.state in ['draft', 'sent']
```

### 2. Estados com Hierarquia (State Groups)

```python
class ProjectTask(models.Model):
    _name = 'project.task'
    _description = 'Project Task'

    # Estado principal
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='new', tracking=True)

    # Sub-estados para maior granularidade
    stage_id = fields.Many2one(
        'project.task.type',
        'Stage',
        ondelete='restrict',
        tracking=True,
        domain="[('project_ids', '=', project_id)]"
    )

    # Estados calculados
    state_group = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], compute='_compute_state_group', store=True)

    @api.depends('state')
    def _compute_state_group(self):
        """Agrupa estados em categorias"""
        for task in self:
            if task.state in ['done', 'cancelled']:
                task.state_group = 'closed'
            else:
                task.state_group = 'open'
```

---

## Transicoes de Estado

### 1. Metodos de Transicao Basicos

```python
class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _description = 'Purchase Order'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'RFQ Sent'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('purchase', 'Purchase Order'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], default='draft', tracking=True)

    amount_total = fields.Float('Total', compute='_compute_amount_total')
    approval_required = fields.Boolean(compute='_compute_approval_required')

    @api.depends('amount_total')
    def _compute_approval_required(self):
        """Determina se pedido precisa aprovacao"""
        approval_limit = float(self.env['ir.config_parameter'].sudo().get_param(
            'purchase.approval_limit', '10000'
        ))
        for order in self:
            order.approval_required = order.amount_total > approval_limit

    def action_rfq_send(self):
        """Transicao: draft -> sent"""
        self.ensure_one()

        # Validacoes pre-transicao
        if not self.order_line:
            raise UserError(_("Cannot send an empty purchase order."))

        if not self.partner_id.email:
            raise UserError(_("Partner must have an email address."))

        # Executar transicao
        self.write({'state': 'sent'})

        # Acoes pos-transicao
        self._send_rfq_email()

        return True

    def action_confirm(self):
        """Transicao: sent -> to_approve ou purchase"""
        for order in self:
            # Validacoes
            if order.state not in ['draft', 'sent']:
                raise UserError(_("Only draft or sent orders can be confirmed."))

            # Decisao de estado baseada em regras de negocio
            if order.approval_required:
                order.state = 'to_approve'
                order._notify_approvers()
            else:
                order.state = 'purchase'
                order._create_stock_picking()

        return True

    def action_approve(self):
        """Transicao: to_approve -> purchase (requer permissao)"""
        self.ensure_one()

        # Check de permissao
        if not self.env.user.has_group('purchase.group_purchase_manager'):
            raise UserError(_("Only Purchase Managers can approve orders."))

        # Validacao de estado
        if self.state != 'to_approve':
            raise UserError(_("Only orders waiting approval can be approved."))

        # Transicao
        self.write({
            'state': 'purchase',
            'approved_by': self.env.user.id,
            'approved_date': fields.Datetime.now(),
        })

        # Acoes pos-aprovacao
        self._create_stock_picking()

        return True

    def action_cancel(self):
        """Transicao: * -> cancel"""
        for order in self:
            # Validar se pode cancelar
            if order.state == 'done':
                raise UserError(_("Cannot cancel a completed order."))

            if order.picking_ids.filtered(lambda p: p.state == 'done'):
                raise UserError(_("Cannot cancel order with completed deliveries."))

            # Cancelar operacoes relacionadas
            order.picking_ids.filtered(lambda p: p.state != 'done').action_cancel()

            # Transicao
            order.state = 'cancel'

        return True
```

### 2. Transicoes com Wizards

```python
class InvoiceValidationWizard(models.TransientModel):
    _name = 'invoice.validation.wizard'
    _description = 'Invoice Validation Wizard'

    invoice_id = fields.Many2one('account.move', required=True)
    validation_note = fields.Text('Validation Note')
    validate_date = fields.Date('Validation Date', default=fields.Date.today)

    def action_validate(self):
        """Valida invoice com informacoes adicionais"""
        self.ensure_one()

        invoice = self.invoice_id

        # Validacoes customizadas
        if not invoice.invoice_line_ids:
            raise UserError(_("Cannot validate an invoice without lines."))

        # Realizar transicao com contexto adicional
        invoice.with_context(
            validation_note=self.validation_note,
            validation_date=self.validate_date
        ).action_post()

        return {'type': 'ir.actions.act_window_close'}

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        """Override para adicionar logica customizada"""
        # Capturar contexto do wizard
        validation_note = self.env.context.get('validation_note')

        # Chamar metodo original
        res = super().action_post()

        # Logica adicional
        if validation_note:
            self.message_post(
                body=_("Validation Note: %s") % validation_note,
                message_type='comment'
            )

        return res
```

### 3. Transicoes Automaticas

```python
class SupportTicket(models.Model):
    _name = 'support.ticket'
    _description = 'Support Ticket'

    state = fields.Selection([
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('waiting', 'Waiting Customer'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], default='new', tracking=True)

    assigned_to = fields.Many2one('res.users', 'Assigned To')
    last_activity = fields.Datetime('Last Activity', default=fields.Datetime.now)
    auto_close_days = fields.Integer('Auto Close Days', default=7)

    @api.model
    def _cron_auto_close_tickets(self):
        """Scheduled action para fechar tickets automaticamente"""
        # Buscar tickets elegiveis
        date_limit = fields.Datetime.now() - timedelta(days=7)

        tickets = self.search([
            ('state', '=', 'resolved'),
            ('last_activity', '<', date_limit),
        ])

        # Transicao automatica
        for ticket in tickets:
            ticket.action_close(auto=True)

        return True

    def action_close(self, auto=False):
        """Fecha ticket"""
        for ticket in self:
            if ticket.state != 'resolved':
                raise UserError(_("Only resolved tickets can be closed."))

            ticket.state = 'closed'

            if auto:
                ticket.message_post(
                    body=_("Ticket automatically closed after %d days.") % ticket.auto_close_days
                )

    def write(self, vals):
        """Detectar mudancas e transicionar estados"""
        # Atualizar timestamp de atividade
        if any(field in vals for field in ['assigned_to', 'message_ids']):
            vals['last_activity'] = fields.Datetime.now()

        # Auto-transicao quando ticket e atribuido
        if 'assigned_to' in vals and vals['assigned_to']:
            if self.state == 'new':
                vals['state'] = 'assigned'

        return super().write(vals)
```

---

## Buttons e Actions

### 1. Buttons na View (XML)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_sale_order_form" model="ir.ui.view">
        <field name="name">sale.order.form</field>
        <field name="model">sale.order</field>
        <field name="arch" type="xml">
            <form>
                <!-- Header com buttons de estado -->
                <header>
                    <!-- Button simples -->
                    <button name="action_confirm"
                            string="Confirm"
                            type="object"
                            class="btn-primary"
                            invisible="state != 'draft'"/>

                    <!-- Button com confirmacao -->
                    <button name="action_cancel"
                            string="Cancel"
                            type="object"
                            confirm="Are you sure you want to cancel this order?"
                            invisible="state in ['cancel', 'done']"/>

                    <!-- Button que abre wizard -->
                    <button name="%(action_sale_approval_wizard)d"
                            string="Request Approval"
                            type="action"
                            class="btn-secondary"
                            invisible="state != 'draft'"
                            groups="sales_team.group_sale_salesman"/>

                    <!-- Button com contexto -->
                    <button name="action_send_email"
                            string="Send by Email"
                            type="object"
                            context="{'default_use_template': True, 'default_template_id': %(email_template_sale_order)d}"
                            invisible="state not in ['draft', 'sent']"/>

                    <!-- Button com icon -->
                    <button name="action_view_delivery"
                            string="Delivery"
                            type="object"
                            icon="fa-truck"
                            invisible="state not in ['sale', 'done']"/>

                    <!-- Statusbar - visualizacao do estado -->
                    <field name="state"
                           widget="statusbar"
                           statusbar_visible="draft,sent,sale,done"
                           options="{'clickable': '1'}"/>
                </header>

                <sheet>
                    <!-- Ribbon para destacar estado -->
                    <div class="ribbon ribbon-top-right"
                         invisible="state != 'cancel'">
                        <span class="bg-danger">Cancelled</span>
                    </div>

                    <div class="ribbon ribbon-top-right"
                         invisible="state != 'done'">
                        <span class="bg-success">Completed</span>
                    </div>

                    <!-- Conteudo do form -->
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="partner_id"/>
                        </group>
                        <group>
                            <field name="date_order"/>
                            <field name="user_id"/>
                        </group>
                    </group>

                    <!-- Campos readonly baseados em estado -->
                    <notebook>
                        <page string="Order Lines">
                            <field name="order_line"
                                   readonly="state in ['done', 'cancel']">
                                <tree editable="bottom">
                                    <field name="product_id"/>
                                    <field name="quantity"/>
                                    <field name="price_unit"/>
                                    <field name="price_subtotal"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>

                <!-- Chatter -->
                <chatter/>
            </form>
        </field>
    </record>
</odoo>
```

### 2. Buttons Dinamicos no Python

```python
class WorkflowDocument(models.Model):
    _name = 'workflow.document'
    _description = 'Document with Dynamic Workflow'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='draft')

    # Controlar visibilidade de buttons
    can_review = fields.Boolean(compute='_compute_can_review')
    can_approve = fields.Boolean(compute='_compute_can_approve')
    can_reject = fields.Boolean(compute='_compute_can_reject')

    @api.depends('state')
    def _compute_can_review(self):
        """Usuario pode iniciar review?"""
        for doc in self:
            doc.can_review = (
                doc.state == 'draft' and
                (doc.user_id == self.env.user or
                 self.env.user.has_group('base.group_system'))
            )

    @api.depends('state')
    def _compute_can_approve(self):
        """Usuario pode aprovar?"""
        for doc in self:
            doc.can_approve = (
                doc.state == 'review' and
                self.env.user.has_group('document.group_manager')
            )

    @api.depends('state')
    def _compute_can_reject(self):
        """Usuario pode rejeitar?"""
        for doc in self:
            doc.can_reject = (
                doc.state == 'review' and
                self.env.user.has_group('document.group_manager')
            )
```

### 3. Action Buttons com Progress

```python
class DataImportJob(models.Model):
    _name = 'data.import.job'
    _description = 'Data Import Job'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ], default='draft')

    progress = fields.Float('Progress', default=0.0)
    total_records = fields.Integer('Total Records')
    processed_records = fields.Integer('Processed Records')

    def action_start_import(self):
        """Inicia processo de importacao"""
        self.ensure_one()

        if self.state != 'draft':
            raise UserError(_("Only draft jobs can be started."))

        # Transicao para running
        self.write({
            'state': 'running',
            'processed_records': 0,
            'progress': 0.0,
        })

        # Processar em background (usando queue_job ou similar)
        self.with_delay()._process_import()

        # Retornar action para recarregar view
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Import Started'),
                'message': _('Import job is now running in background.'),
                'type': 'success',
                'sticky': False,
            }
        }

    def _process_import(self):
        """Processa importacao (rodaria em background)"""
        try:
            # Simulacao de processamento
            for i in range(self.total_records):
                # Processar registro
                self._process_record(i)

                # Atualizar progresso
                self.write({
                    'processed_records': i + 1,
                    'progress': ((i + 1) / self.total_records) * 100,
                })

                # Commit parcial para atualizar UI
                self.env.cr.commit()

            # Transicao para done
            self.state = 'done'

        except Exception as e:
            # Transicao para failed
            self.write({
                'state': 'failed',
                'error_message': str(e),
            })
            raise
```

---

## Tracking de Mudancas

### 1. Field Tracking (Chatter)

```python
class Contract(models.Model):
    _name = 'contract.contract'
    _description = 'Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Contract Number', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ], default='draft', tracking=True)  # Tracking no chatter

    partner_id = fields.Many2one('res.partner', 'Customer', tracking=True)
    amount = fields.Float('Contract Value', tracking=True)

    # Campos de auditoria
    activated_by = fields.Many2one('res.users', 'Activated By', tracking=True)
    activated_date = fields.Datetime('Activation Date', tracking=True)

    def action_activate(self):
        """Ativa contrato"""
        self.ensure_one()

        if self.state != 'draft':
            raise UserError(_("Only draft contracts can be activated."))

        # Transicao com tracking automatico
        self.write({
            'state': 'active',
            'activated_by': self.env.user.id,
            'activated_date': fields.Datetime.now(),
        })

        # Mensagem customizada no chatter
        self.message_post(
            body=_("Contract activated by %s") % self.env.user.name,
            message_type='notification',
            subtype_xmlid='mail.mt_note',
        )

        return True
```

### 2. State History (Log Completo)

```python
class Shipment(models.Model):
    _name = 'logistics.shipment'
    _description = 'Shipment'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
    ], default='draft')

    state_history_ids = fields.One2many(
        'logistics.shipment.state.history',
        'shipment_id',
        'State History'
    )

    def write(self, vals):
        """Registrar mudancas de estado"""
        # Se estado mudou, criar registro de historico
        if 'state' in vals:
            for shipment in self:
                if vals['state'] != shipment.state:
                    self.env['logistics.shipment.state.history'].create({
                        'shipment_id': shipment.id,
                        'state_from': shipment.state,
                        'state_to': vals['state'],
                        'user_id': self.env.user.id,
                        'date': fields.Datetime.now(),
                        'notes': self.env.context.get('state_change_note', ''),
                    })

        return super().write(vals)

class ShipmentStateHistory(models.Model):
    _name = 'logistics.shipment.state.history'
    _description = 'Shipment State History'
    _order = 'date desc'

    shipment_id = fields.Many2one('logistics.shipment', 'Shipment', required=True)
    state_from = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
    ], 'From State')
    state_to = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
    ], 'To State')
    user_id = fields.Many2one('res.users', 'Changed By')
    date = fields.Datetime('Date')
    notes = fields.Text('Notes')
    duration = fields.Char('Duration in State', compute='_compute_duration')

    @api.depends('date')
    def _compute_duration(self):
        """Calcular quanto tempo ficou em cada estado"""
        for record in self:
            if record.state_from:
                # Buscar registro anterior
                previous = self.search([
                    ('shipment_id', '=', record.shipment_id.id),
                    ('date', '<', record.date),
                ], order='date desc', limit=1)

                if previous:
                    delta = record.date - previous.date
                    days = delta.days
                    hours = delta.seconds // 3600
                    record.duration = f"{days}d {hours}h"
                else:
                    record.duration = "N/A"
            else:
                record.duration = "N/A"
```

### 3. Audit Trail Completo

```python
class AuditedDocument(models.Model):
    _name = 'audited.document'
    _description = 'Audited Document'
    _inherit = ['mail.thread']

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='draft', tracking=True)

    audit_trail_ids = fields.One2many(
        'document.audit.trail',
        'document_id',
        'Audit Trail',
        readonly=True
    )

    def _track_state_change(self, old_state, new_state, reason=''):
        """Registrar mudanca de estado no audit trail"""
        self.env['document.audit.trail'].create({
            'document_id': self.id,
            'action': 'state_change',
            'old_value': old_state,
            'new_value': new_state,
            'user_id': self.env.user.id,
            'ip_address': self.env.context.get('ip_address', 'unknown'),
            'reason': reason,
        })

    def action_submit(self):
        """Submete documento para aprovacao"""
        self.ensure_one()

        old_state = self.state
        self.state = 'submitted'

        # Registrar no audit trail
        self._track_state_change(
            old_state,
            'submitted',
            reason='Document submitted for approval'
        )

        return True

class DocumentAuditTrail(models.Model):
    _name = 'document.audit.trail'
    _description = 'Document Audit Trail'
    _order = 'create_date desc'

    document_id = fields.Many2one('audited.document', 'Document', required=True)
    action = fields.Char('Action', required=True)
    old_value = fields.Char('Old Value')
    new_value = fields.Char('New Value')
    user_id = fields.Many2one('res.users', 'User', required=True)
    create_date = fields.Datetime('Date', readonly=True)
    ip_address = fields.Char('IP Address')
    reason = fields.Text('Reason')
```

---

## Record Rules por Estado

### 1. Security Rules Baseadas em Estado

```python
# models/purchase_order.py
class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _description = 'Purchase Order'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], default='draft')
```

```xml
<!-- security/purchase_security.xml -->
<odoo>
    <data noupdate="1">

        <!-- Rule 1: Usuarios comuns podem ver apenas seus proprios pedidos em draft -->
        <record id="purchase_order_user_rule" model="ir.rule">
            <field name="name">Purchase Order: User can see own draft orders</field>
            <field name="model_id" ref="model_purchase_order"/>
            <field name="domain_force">
                ['|',
                    ('state', '!=', 'draft'),
                    ('user_id', '=', user.id)
                ]
            </field>
            <field name="groups" eval="[(4, ref('purchase.group_purchase_user'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
        </record>

        <!-- Rule 2: Managers podem ver todos -->
        <record id="purchase_order_manager_rule" model="ir.rule">
            <field name="name">Purchase Order: Manager can see all</field>
            <field name="model_id" ref="model_purchase_order"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('purchase.group_purchase_manager'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="True"/>
        </record>

        <!-- Rule 3: Aprovados e Done sao readonly para usuarios -->
        <record id="purchase_order_readonly_rule" model="ir.rule">
            <field name="name">Purchase Order: Approved orders are readonly</field>
            <field name="model_id" ref="model_purchase_order"/>
            <field name="domain_force">
                [('state', 'in', ['draft', 'cancel'])]
            </field>
            <field name="groups" eval="[(4, ref('purchase.group_purchase_user'))]"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_unlink" eval="True"/>
        </record>

    </data>
</odoo>
```

### 2. Dynamic Record Rules

```python
class Project(models.Model):
    _name = 'project.project'
    _description = 'Project'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], default='draft')

    privacy_visibility = fields.Selection([
        ('followers', 'Invited internal users'),
        ('employees', 'All internal users'),
        ('portal', 'Invited portal users and all internal users'),
    ], default='employees')

    @api.model
    def _get_domain_for_current_user(self):
        """Retorna domain dinamico baseado no usuario e estado"""
        user = self.env.user

        if user.has_group('project.group_project_manager'):
            # Managers veem tudo
            return []

        # Usuarios comuns veem apenas projetos ativos onde participam
        return [
            ('state', '=', 'active'),
            '|',
                ('user_id', '=', user.id),
                ('member_ids', 'in', user.id),
        ]
```

```xml
<!-- security/project_security.xml -->
<odoo>
    <data noupdate="1">

        <!-- Rule com domain complexo baseado em estado -->
        <record id="project_visibility_rule" model="ir.rule">
            <field name="name">Project: User access based on state</field>
            <field name="model_id" ref="model_project_project"/>
            <field name="domain_force">
                [
                    '|', '|',
                        ('state', '=', 'draft'),
                        '&amp;',
                            ('state', '=', 'active'),
                            '|',
                                ('user_id', '=', user.id),
                                ('member_ids', 'in', [user.id]),
                        '&amp;',
                            ('state', '=', 'closed'),
                            ('privacy_visibility', '=', 'employees')
                ]
            </field>
            <field name="groups" eval="[(4, ref('base.group_user'))]"/>
        </record>

    </data>
</odoo>
```

### 3. Programmatic Security Checks

```python
class SensitiveDocument(models.Model):
    _name = 'sensitive.document'
    _description = 'Sensitive Document'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('classified', 'Classified'),
        ('archived', 'Archived'),
    ], default='draft')

    security_level = fields.Selection([
        ('public', 'Public'),
        ('internal', 'Internal'),
        ('confidential', 'Confidential'),
        ('secret', 'Secret'),
    ], default='internal')

    def check_access_rights(self, operation, raise_exception=True):
        """Override para adicionar checks baseados em estado"""
        # Check padrao
        res = super().check_access_rights(operation, raise_exception)

        # Check adicional para documentos classificados
        if operation in ['write', 'unlink']:
            for doc in self:
                if doc.state == 'classified':
                    if not self.env.user.has_group('document.group_classification_manager'):
                        if raise_exception:
                            raise AccessError(_("Classified documents can only be modified by managers."))
                        return False

        return res

    def _check_state_access(self):
        """Valida acesso baseado em estado e nivel de seguranca"""
        self.ensure_one()

        user = self.env.user

        # Documentos secretos
        if self.security_level == 'secret':
            if not user.has_group('document.group_secret_clearance'):
                raise AccessError(_("You don't have clearance to access this document."))

        # Documentos arquivados
        if self.state == 'archived':
            if not user.has_group('document.group_archive_access'):
                raise AccessError(_("You don't have permission to access archived documents."))

        return True

    def read(self, fields=None, load='_classic_read'):
        """Override read para validar acesso"""
        for doc in self:
            doc._check_state_access()

        return super().read(fields=fields, load=load)
```

---

## Exemplos Praticos

### Exemplo 1: Invoice Workflow

```python
class AccountMove(models.Model):
    _name = 'account.move'
    _description = 'Account Move (Invoice)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], default='draft', tracking=True, copy=False)

    move_type = fields.Selection([
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Customer Invoice'),
        ('out_refund', 'Customer Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
    ], required=True, tracking=True)

    name = fields.Char('Number', copy=False, tracking=True)
    date = fields.Date('Date', default=fields.Date.context_today, required=True)
    partner_id = fields.Many2one('res.partner', 'Partner', tracking=True)
    amount_total = fields.Monetary('Total', compute='_compute_amount')

    # Campos de controle
    posted_before = fields.Boolean('Posted Before', copy=False)

    def action_post(self):
        """Posta invoice (draft -> posted)"""
        for move in self:
            # Validacoes
            if move.state != 'draft':
                raise UserError(_("Only draft invoices can be posted."))

            if not move.line_ids:
                raise UserError(_("Cannot post an invoice without lines."))

            if not move.name or move.name == '/':
                # Gerar numero de sequencia
                move.name = move._get_sequence()

            # Transicao
            move.write({
                'state': 'posted',
                'posted_before': True,
            })

            # Acoes pos-posting
            move._post_accounting_entries()
            move._notify_partners()

        return True

    def button_draft(self):
        """Retorna invoice para draft (posted -> draft)"""
        for move in self:
            # Validacoes
            if move.state != 'posted':
                raise UserError(_("Only posted invoices can be reset to draft."))

            if move.payment_ids:
                raise UserError(_("Cannot reset invoice with payments."))

            # Reverter lancamentos contabeis
            move._reverse_accounting_entries()

            # Transicao
            move.state = 'draft'

        return True

    def button_cancel(self):
        """Cancela invoice"""
        for move in self:
            if move.state == 'posted':
                # Se ja foi postada, reverter
                move._reverse_accounting_entries()

            move.state = 'cancel'

        return True

    def _get_sequence(self):
        """Gera numero de sequencia"""
        sequence_code = 'account.move.' + self.move_type
        return self.env['ir.sequence'].next_by_code(sequence_code)

    def _post_accounting_entries(self):
        """Cria lancamentos contabeis"""
        # Implementacao de logica contabil
        pass

    def _reverse_accounting_entries(self):
        """Reverte lancamentos contabeis"""
        # Implementacao de reversao
        pass

    def _notify_partners(self):
        """Notifica parceiros"""
        for move in self:
            if move.move_type in ['out_invoice', 'out_refund']:
                move.message_post_with_template(
                    template_id=self.env.ref('account.email_template_invoice').id
                )
```

**View XML para Invoice:**

```xml
<record id="view_move_form" model="ir.ui.view">
    <field name="name">account.move.form</field>
    <field name="model">account.move</field>
    <field name="arch" type="xml">
        <form>
            <header>
                <!-- Buttons de transicao -->
                <button name="action_post"
                        string="Post"
                        type="object"
                        class="oe_highlight"
                        invisible="state != 'draft'"/>

                <button name="button_draft"
                        string="Reset to Draft"
                        type="object"
                        invisible="state != 'posted'"
                        groups="account.group_account_manager"
                        confirm="Are you sure? This will reverse the accounting entries."/>

                <button name="button_cancel"
                        string="Cancel"
                        type="object"
                        invisible="state == 'cancel'"
                        confirm="Are you sure you want to cancel this invoice?"/>

                <!-- Status bar -->
                <field name="state" widget="statusbar" statusbar_visible="draft,posted"/>
            </header>

            <sheet>
                <div class="oe_title">
                    <h1>
                        <field name="name" readonly="state != 'draft'"/>
                    </h1>
                </div>

                <group>
                    <group>
                        <field name="partner_id" readonly="state != 'draft'"/>
                        <field name="date" readonly="state != 'draft'"/>
                    </group>
                    <group>
                        <field name="move_type" readonly="state != 'draft'"/>
                        <field name="amount_total"/>
                    </group>
                </group>

                <notebook>
                    <page string="Invoice Lines">
                        <field name="line_ids" readonly="state != 'draft'">
                            <tree editable="bottom">
                                <field name="account_id"/>
                                <field name="name"/>
                                <field name="debit"/>
                                <field name="credit"/>
                            </tree>
                        </field>
                    </page>
                </notebook>
            </sheet>

            <chatter/>
        </form>
    </field>
</record>
```

### Exemplo 2: Sale Order Workflow Completo

```python
class SaleOrder(models.Model):
    _name = 'sale.order'
    _description = 'Sales Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], default='draft', tracking=True, copy=False)

    name = fields.Char('Order Reference', required=True, default='New')
    partner_id = fields.Many2one('res.partner', 'Customer', required=True, tracking=True)
    date_order = fields.Datetime('Order Date', default=fields.Datetime.now, required=True)
    validity_date = fields.Date('Expiration', compute='_compute_validity_date', store=True)

    order_line = fields.One2many('sale.order.line', 'order_id', 'Order Lines')

    amount_total = fields.Monetary('Total', compute='_compute_amounts', store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    # Campos de integracao
    invoice_ids = fields.Many2many('account.move', 'sale_order_invoice_rel', 'order_id', 'invoice_id', 'Invoices')
    invoice_count = fields.Integer('Invoice Count', compute='_compute_invoice_count')

    picking_ids = fields.Many2many('stock.picking', 'sale_order_picking_rel', 'order_id', 'picking_id', 'Deliveries')
    delivery_count = fields.Integer('Delivery Count', compute='_compute_delivery_count')

    # Campos computados
    invoice_status = fields.Selection([
        ('no', 'Nothing to Invoice'),
        ('to invoice', 'To Invoice'),
        ('invoiced', 'Fully Invoiced'),
    ], compute='_compute_invoice_status', store=True)

    @api.depends('order_line.price_subtotal')
    def _compute_amounts(self):
        """Calcula totais"""
        for order in self:
            order.amount_total = sum(order.order_line.mapped('price_subtotal'))

    @api.depends('date_order')
    def _compute_validity_date(self):
        """Quotation valida por 30 dias"""
        for order in self:
            if order.state in ['draft', 'sent']:
                order.validity_date = order.date_order.date() + timedelta(days=30)
            else:
                order.validity_date = False

    def _compute_invoice_count(self):
        for order in self:
            order.invoice_count = len(order.invoice_ids)

    def _compute_delivery_count(self):
        for order in self:
            order.delivery_count = len(order.picking_ids)

    @api.depends('order_line.invoice_status', 'state')
    def _compute_invoice_status(self):
        """Calcula status de faturamento"""
        for order in self:
            if order.state not in ['sale', 'done']:
                order.invoice_status = 'no'
            elif all(line.invoice_status == 'invoiced' for line in order.order_line):
                order.invoice_status = 'invoiced'
            elif any(line.invoice_status == 'to invoice' for line in order.order_line):
                order.invoice_status = 'to invoice'
            else:
                order.invoice_status = 'no'

    @api.model
    def create(self, vals):
        """Gera numero de sequencia na criacao"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or 'New'
        return super().create(vals)

    # === WORKFLOW TRANSITIONS ===

    def action_quotation_send(self):
        """Envia quotation por email (draft/sent -> sent)"""
        self.ensure_one()

        if self.state not in ['draft', 'sent']:
            raise UserError(_("Cannot send email for orders in state %s.") % self.state)

        # Transicao
        self.state = 'sent'

        # Abrir composer de email
        template = self.env.ref('sale.email_template_sale_order', raise_if_not_found=False)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'sale.order',
                'default_res_id': self.id,
                'default_use_template': bool(template),
                'default_template_id': template.id if template else False,
            },
        }

    def action_confirm(self):
        """Confirma order (draft/sent -> sale)"""
        for order in self:
            # Validacoes
            if order.state not in ['draft', 'sent']:
                raise UserError(_("Only quotations can be confirmed."))

            if not order.order_line:
                raise UserError(_("Cannot confirm order without lines."))

            # Transicao
            order.write({
                'state': 'sale',
                'date_order': fields.Datetime.now(),
            })

            # Acoes pos-confirmacao
            order._create_delivery_picking()
            order._create_invoice()

            # Notificacoes
            order.message_post(
                body=_("Sales Order confirmed by %s") % self.env.user.name,
                message_type='notification'
            )

            # Activity para follow-up
            order.activity_schedule(
                'sale.mail_act_sale_order_follow_up',
                user_id=order.user_id.id,
                date_deadline=fields.Date.today() + timedelta(days=7),
            )

        return True

    def action_done(self):
        """Fecha order (sale -> done)"""
        for order in self:
            if order.state != 'sale':
                raise UserError(_("Only sales orders can be locked."))

            # Validar que tudo foi faturado e entregue
            if order.invoice_status != 'invoiced':
                raise UserError(_("All order lines must be invoiced before locking."))

            if any(picking.state not in ['done', 'cancel'] for picking in order.picking_ids):
                raise UserError(_("All deliveries must be completed before locking."))

            order.state = 'done'

        return True

    def action_cancel(self):
        """Cancela order (* -> cancel)"""
        for order in self:
            if order.state == 'done':
                raise UserError(_("Cannot cancel a locked order."))

            # Cancelar operacoes relacionadas
            order.picking_ids.filtered(lambda p: p.state not in ['done', 'cancel']).action_cancel()
            order.invoice_ids.filtered(lambda i: i.state == 'draft').button_cancel()

            order.state = 'cancel'

        return True

    def action_draft(self):
        """Retorna para draft (cancel -> draft)"""
        for order in self:
            if order.state != 'cancel':
                raise UserError(_("Only cancelled orders can be reset to draft."))

            order.state = 'draft'

        return True

    # === INTEGRATION ACTIONS ===

    def _create_delivery_picking(self):
        """Cria picking de entrega"""
        self.ensure_one()

        if not self.order_line.filtered(lambda l: l.product_id.type in ['product', 'consu']):
            return False

        picking = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'move_ids': [(0, 0, {
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
            }) for line in self.order_line if line.product_id.type in ['product', 'consu']],
        })

        self.picking_ids = [(4, picking.id)]
        return picking

    def _create_invoice(self):
        """Cria invoice"""
        self.ensure_one()

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [(0, 0, {
                'name': line.name,
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
            }) for line in self.order_line],
        }

        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_ids = [(4, invoice.id)]

        return invoice

    def action_view_invoice(self):
        """Abre invoices"""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
            'context': {'default_move_type': 'out_invoice'},
        }

    def action_view_delivery(self):
        """Abre deliveries"""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': _('Deliveries'),
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.picking_ids.ids)],
        }

class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _description = 'Sales Order Line'

    order_id = fields.Many2one('sale.order', 'Order Reference', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product')
    name = fields.Text('Description', required=True)
    product_uom_qty = fields.Float('Quantity', default=1.0)
    price_unit = fields.Float('Unit Price')
    price_subtotal = fields.Float('Subtotal', compute='_compute_price_subtotal', store=True)

    invoice_status = fields.Selection([
        ('no', 'Nothing to Invoice'),
        ('to invoice', 'To Invoice'),
        ('invoiced', 'Invoiced'),
    ], default='no', compute='_compute_invoice_status', store=True)

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.product_uom_qty * line.price_unit

    @api.depends('order_id.state')
    def _compute_invoice_status(self):
        for line in self:
            if line.order_id.state not in ['sale', 'done']:
                line.invoice_status = 'no'
            else:
                # Simplificado - verificar se linha foi faturada
                line.invoice_status = 'to invoice'
```

### Exemplo 3: Project Task Workflow com Stages

```python
class ProjectTask(models.Model):
    _name = 'project.task'
    _description = 'Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Estados simples
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='new', tracking=True)

    # Stages (mais granular)
    stage_id = fields.Many2one(
        'project.task.type',
        'Stage',
        ondelete='restrict',
        tracking=True,
        index=True,
        copy=False,
        domain="[('project_ids', '=', project_id)]",
        group_expand='_read_group_stage_ids'
    )

    name = fields.Char('Title', required=True, tracking=True)
    project_id = fields.Many2one('project.project', 'Project', required=True)
    user_ids = fields.Many2many('res.users', string='Assignees', tracking=True)

    # Campos de progresso
    progress = fields.Float('Progress', compute='_compute_progress', store=True)
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked'),
    ], default='normal', tracking=True)

    # Campos de tempo
    planned_hours = fields.Float('Planned Hours')
    effective_hours = fields.Float('Effective Hours', compute='_compute_effective_hours')
    remaining_hours = fields.Float('Remaining Hours')

    # Campos de dependencia
    parent_id = fields.Many2one('project.task', 'Parent Task')
    child_ids = fields.One2many('project.task', 'parent_id', 'Subtasks')
    depend_on_ids = fields.Many2many(
        'project.task',
        'task_dependencies_rel',
        'task_id',
        'depends_on_id',
        'Depends On'
    )

    @api.depends('stage_id', 'stage_id.fold')
    def _compute_progress(self):
        """Calcula progresso baseado no stage"""
        for task in self:
            if task.stage_id.fold:
                task.progress = 100.0
            elif task.stage_id.sequence == 0:
                task.progress = 0.0
            else:
                # Progresso baseado na sequencia do stage
                max_seq = max(self.env['project.task.type'].search([]).mapped('sequence'))
                if max_seq > 0:
                    task.progress = (task.stage_id.sequence / max_seq) * 100
                else:
                    task.progress = 0.0

    def write(self, vals):
        """Auto-transicionar estado baseado em stage"""
        result = super().write(vals)

        # Se stage mudou, atualizar estado
        if 'stage_id' in vals:
            for task in self:
                stage = task.stage_id

                if stage.fold:
                    # Stage final - marcar como done
                    if task.state not in ['done', 'cancelled']:
                        task.state = 'done'
                elif task.state == 'new':
                    # Mover de new para in_progress
                    task.state = 'in_progress'

        return result

    def action_start(self):
        """Inicia task"""
        self.ensure_one()

        if self.state != 'new':
            raise UserError(_("Only new tasks can be started."))

        # Validar dependencias
        if self.depend_on_ids:
            incomplete = self.depend_on_ids.filtered(lambda t: t.state != 'done')
            if incomplete:
                raise UserError(_(
                    "Cannot start task. The following dependencies must be completed first:\n%s"
                ) % '\n'.join(incomplete.mapped('name')))

        # Transicao
        self.write({
            'state': 'in_progress',
            'kanban_state': 'normal',
        })

        return True

    def action_done(self):
        """Completa task"""
        self.ensure_one()

        if self.state not in ['new', 'in_progress']:
            raise UserError(_("Only active tasks can be completed."))

        # Validar subtasks
        if self.child_ids:
            incomplete = self.child_ids.filtered(lambda t: t.state != 'done')
            if incomplete:
                raise UserError(_("All subtasks must be completed first."))

        # Mover para ultimo stage
        final_stage = self.env['project.task.type'].search([
            ('project_ids', '=', self.project_id.id),
            ('fold', '=', True),
        ], limit=1)

        self.write({
            'state': 'done',
            'stage_id': final_stage.id if final_stage else False,
            'kanban_state': 'done',
            'progress': 100.0,
        })

        # Notificar dependentes
        dependent_tasks = self.search([('depend_on_ids', 'in', self.id)])
        for task in dependent_tasks:
            task.activity_schedule(
                'project.mail_act_dependency_completed',
                user_id=task.user_ids[0].id if task.user_ids else self.env.user.id,
            )

        return True

    def action_cancel(self):
        """Cancela task"""
        for task in self:
            if task.state == 'done':
                raise UserError(_("Cannot cancel completed tasks."))

            task.state = 'cancelled'

        return True

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """Usado para group_expand no kanban view"""
        project_id = self.env.context.get('default_project_id')

        if project_id:
            return stages.search([
                ('project_ids', '=', project_id)
            ], order=order)

        return stages

class ProjectTaskType(models.Model):
    _name = 'project.task.type'
    _description = 'Task Stage'
    _order = 'sequence, id'

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=10)
    fold = fields.Boolean('Folded in Kanban', help='Stage is folded in kanban view')
    project_ids = fields.Many2many('project.project', string='Projects')

    # Configuracoes de automacao
    auto_validation = fields.Boolean('Auto Validation',
        help='Automatically validate task when reaching this stage')
```

---

## Best Practices

### 1. Design de Estados

```python
# BOM: Estados claros e significativos
state = fields.Selection([
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('done', 'Done'),
    ('cancel', 'Cancelled'),
], default='draft')

# RUIM: Estados ambiguos
state = fields.Selection([
    ('state1', 'State 1'),
    ('state2', 'State 2'),
    ('state3', 'State 3'),
])
```

### 2. Validacoes de Transicao

```python
# BOM: Validacoes claras antes da transicao
def action_confirm(self):
    self.ensure_one()

    # 1. Validar estado atual
    if self.state != 'draft':
        raise UserError(_("Only draft records can be confirmed."))

    # 2. Validar dados necessarios
    if not self.line_ids:
        raise UserError(_("Cannot confirm without lines."))

    # 3. Validar permissoes
    if not self.env.user.has_group('module.group_manager'):
        raise UserError(_("Only managers can confirm."))

    # 4. Realizar transicao
    self.state = 'confirmed'

    return True

# RUIM: Transicao sem validacoes
def action_confirm(self):
    self.state = 'confirmed'
```

### 3. Atomicidade de Transicoes

```python
# BOM: Usar write() para garantir atomicidade
def action_approve(self):
    self.ensure_one()

    vals = {
        'state': 'approved',
        'approved_by': self.env.user.id,
        'approved_date': fields.Datetime.now(),
    }

    self.write(vals)

    # Acoes pos-transicao
    self._create_approval_document()

    return True

# RUIM: Multiplas escritas
def action_approve(self):
    self.state = 'approved'
    self.approved_by = self.env.user.id
    self.approved_date = fields.Datetime.now()
```

### 4. Naming Conventions

```python
# BOM: Nomes descritivos para metodos de transicao
def action_confirm(self):  # Acao do usuario
    pass

def _auto_close_expired(self):  # Processo automatico
    pass

def button_reset_to_draft(self):  # Button na UI
    pass

# RUIM: Nomes confusos
def do_stuff(self):
    pass

def change_state(self):
    pass
```

### 5. Documentacao de Workflow

```python
class DocumentWorkflow(models.Model):
    """
    Document Workflow

    State Machine:
    --------------
    draft -> submitted -> approved -> published
      |          |           |
      +-----> rejected <-----+

    Transitions:
    - draft -> submitted: action_submit() - Any user
    - submitted -> approved: action_approve() - Managers only
    - submitted -> rejected: action_reject() - Managers only
    - approved -> published: action_publish() - Publishers only
    - submitted/approved -> rejected: action_reject() - Managers only
    - rejected -> draft: action_reset() - Original author

    Business Rules:
    - Documents require at least one line before submission
    - Approved documents cannot be edited
    - Published documents cannot be unpublished
    """
    _name = 'document.workflow'
    _description = 'Document Workflow'
```

### 6. Testing Workflows

```python
from odoo.tests import TransactionCase
from odoo.exceptions import UserError

class TestSaleOrderWorkflow(TransactionCase):

    def setUp(self):
        super().setUp()
        self.SaleOrder = self.env['sale.order']
        self.partner = self.env['res.partner'].create({'name': 'Test Customer'})

    def test_01_draft_to_confirmed(self):
        """Test transition from draft to confirmed"""
        order = self.SaleOrder.create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'name': 'Test Product',
                'product_uom_qty': 1,
                'price_unit': 100,
            })],
        })

        self.assertEqual(order.state, 'draft')

        # Confirmar
        order.action_confirm()

        self.assertEqual(order.state, 'sale')

    def test_02_cannot_confirm_without_lines(self):
        """Test that order without lines cannot be confirmed"""
        order = self.SaleOrder.create({
            'partner_id': self.partner.id,
        })

        with self.assertRaises(UserError):
            order.action_confirm()

    def test_03_cancel_confirmed_order(self):
        """Test cancellation of confirmed order"""
        order = self.SaleOrder.create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'name': 'Test Product',
                'product_uom_qty': 1,
                'price_unit': 100,
            })],
        })

        order.action_confirm()
        self.assertEqual(order.state, 'sale')

        order.action_cancel()
        self.assertEqual(order.state, 'cancel')
```

### 7. Performance em Workflows

```python
# BOM: Processar em batch quando possivel
def action_bulk_approve(self):
    """Aprovar multiplos registros de uma vez"""
    # Validar todos primeiro
    for record in self:
        if record.state != 'pending':
            raise UserError(_("All records must be in pending state."))

    # Transicionar em batch
    self.write({
        'state': 'approved',
        'approved_by': self.env.user.id,
        'approved_date': fields.Datetime.now(),
    })

    # Notificar em batch
    self._notify_approval()

    return True

# RUIM: Processar um por um desnecessariamente
def action_bulk_approve(self):
    for record in self:
        record.state = 'approved'
        record.approved_by = self.env.user.id
        record.approved_date = fields.Datetime.now()
        record._notify_approval()
```

### 8. Tratamento de Erros

```python
# BOM: Erros claros e acionaveis
def action_confirm(self):
    self.ensure_one()

    try:
        # Validacoes
        if self.state != 'draft':
            raise UserError(_("Only draft orders can be confirmed."))

        if not self.order_line:
            raise UserError(_(
                "Cannot confirm order without lines. "
                "Please add at least one order line."
            ))

        # Transicao
        self.state = 'confirmed'

        # Acoes que podem falhar
        try:
            self._create_stock_picking()
        except Exception as e:
            # Reverter transicao
            self.state = 'draft'
            raise UserError(_(
                "Failed to create delivery: %s\n"
                "The order has been reset to draft."
            ) % str(e))

    except Exception as e:
        # Log para debug
        _logger.error("Failed to confirm order %s: %s", self.name, str(e))
        raise

    return True
```

---

## Diagramas de Estado

### Diagrama 1: Workflow Simples (Linear)

```
Draft --> Confirmed --> Done
  |                      ^
  |                      |
  +-----> Cancelled -----+
```

### Diagrama 2: Workflow com Aprovacao

```
         +----------+
         |  Draft   |
         +----------+
              |
              | submit
              v
         +----------+
         |Submitted |
         +----------+
              |
      +-------+-------+
      |               |
  approve         reject
      |               |
      v               v
 +----------+    +----------+
 | Approved |    | Rejected |
 +----------+    +----------+
      |               |
   publish         reset
      |               |
      v               v
 +----------+    +----------+
 |Published |    |  Draft   |
 +----------+    +----------+
```

### Diagrama 3: Workflow Complexo (E-commerce Order)

```
┌──────────┐
│  Quote   │ Quotation criada
└─────┬────┘
      │ send_quote
      v
┌──────────┐
│   Sent   │ Enviada para cliente
└─────┬────┘
      │ customer_confirm
      v
┌──────────┐
│   Sale   │ Pedido confirmado
└─────┬────┘
      │
      ├─────────────────┐
      │                 │
      v                 v
┌──────────┐      ┌──────────┐
│Processing│      │ Invoiced │
│ Delivery │      └──────────┘
└─────┬────┘            │
      │                 │
      v                 │
┌──────────┐            │
│Delivered │            │
└─────┬────┘            │
      │                 │
      v                 v
      └────────┬────────┘
               │
               v
         ┌──────────┐
         │   Done   │ Pedido completo
         └──────────┘

    (Qualquer estado pode ir para Cancelled)
```

### Diagrama 4: Task Lifecycle com Stages

```
┌────────────┐
│    New     │ Task criada
└─────┬──────┘
      │ assign
      v
┌────────────┐
│  Assigned  │ Atribuida a alguem
└─────┬──────┘
      │ start_work
      v
┌────────────┐
│In Progress │ Trabalho iniciado
└─────┬──────┘
      │
      ├──────────────────┐
      │                  │
      v                  v
┌────────────┐    ┌────────────┐
│  Blocked   │    │   Review   │
└─────┬──────┘    └─────┬──────┘
      │                  │
      │ unblock         approve
      │                  │
      └────────┬─────────┘
               │
               v
         ┌────────────┐
         │    Done    │ Task completa
         └────────────┘

  Stages:
  [Backlog] → [To Do] → [In Progress] → [Testing] → [Done]
```

### Diagrama 5: Approval Workflow com Multiplos Niveis

```
                 ┌──────────┐
                 │  Draft   │
                 └────┬─────┘
                      │ submit
                      v
                 ┌──────────┐
           ┌─────┤ Pending  ├─────┐
           │     │ Level 1  │     │
           │     └────┬─────┘     │
           │          │           │
       reject    approve       cancel
           │          │           │
           v          v           v
      ┌─────────┐┌──────────┐┌─────────┐
      │Rejected ││ Pending  ││Cancelled│
      │         ││ Level 2  ││         │
      └────┬────┘└────┬─────┘└─────────┘
           │          │
         reset    approve
           │          │
           │          v
           │     ┌──────────┐
           │     │ Pending  │
           │     │ Level 3  │
           │     └────┬─────┘
           │          │
           │      approve
           │          │
           │          v
           │     ┌──────────┐
           │     │ Approved │
           │     └──────────┘
           │          │
           │       execute
           │          │
           └──────────┤
                      v
                 ┌──────────┐
                 │  Draft   │
                 └──────────┘
```

### Diagrama 6: Support Ticket Workflow

```
┌─────────┐
│   New   │ Ticket aberto
└────┬────┘
     │ assign
     v
┌─────────┐
│Assigned │ Atribuido ao agente
└────┬────┘
     │ start
     v
┌─────────┐
│Working  │ Agente trabalhando
└────┬────┘
     │
     ├──────────────┐
     │              │
     v              v
┌─────────┐   ┌─────────┐
│Waiting  │   │Escalated│
│Customer │   └────┬────┘
└────┬────┘        │
     │             │ resolve
     │             │
     │ response    │
     │             │
     └─────┬───────┘
           │
           v
     ┌─────────┐
     │Resolved │ Problema resolvido
     └────┬────┘
          │
          │ (auto after 7 days)
          │ OR customer_confirm
          v
     ┌─────────┐
     │ Closed  │ Ticket fechado
     └─────────┘
```

---

## Conclusao

State Machines sao fundamentais para gerenciar workflows complexos no Odoo 18. Seguindo as melhores praticas apresentadas, voce pode criar workflows robustos, manuteníveis e escaláveis.

### Pontos-chave:

1. **Estados Claros**: Use Selection fields com valores significativos
2. **Validacoes**: Sempre valide antes de transicionar
3. **Atomicidade**: Use write() para mudancas atomicas
4. **Tracking**: Implemente tracking adequado (chatter, history)
5. **Security**: Implemente record rules baseadas em estado
6. **Testing**: Teste todas as transicoes possiveis
7. **Documentacao**: Documente o workflow claramente
8. **Performance**: Processe em batch quando possivel

### Referencias:

- Odoo Official Documentation: https://www.odoo.com/documentation/18.0/
- Sale Order workflow: `addons/sale/models/sale_order.py`
- Invoice workflow: `addons/account/models/account_move.py`
- Project Task workflow: `addons/project/models/project_task.py`
