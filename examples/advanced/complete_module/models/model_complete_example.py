# -*- coding: utf-8 -*-
"""
Complete Model Example for Odoo 18

This file demonstrates all features available for Odoo models including:
- All field types
- Computed fields with store and inverse
- Constraints and validations
- Onchange methods
- CRUD method overrides
- Business methods
- Inheritance patterns
- Mail thread integration
- Multi-company support
- Proper documentation
"""

from odoo import api, fields, models, Command, _
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.tools import float_compare, float_is_zero, date_utils
from odoo.tools.misc import format_date, get_lang

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging
import re

_logger = logging.getLogger(__name__)


class CompleteModelExample(models.Model):
    """
    Complete Model Example

    This model demonstrates all Odoo 18 features and best practices.
    It represents a project management system with tasks, resources, and tracking.

    Inherits:
        - mail.thread: Chatter and messaging
        - mail.activity.mixin: Activity scheduling
        - portal.mixin: Customer portal access
        - rating.mixin: Rating and feedback system
    """
    _name = 'complete.model.example'
    _description = 'Complete Model Example'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin', 'rating.mixin']
    _order = 'priority desc, date_start desc, id desc'
    _rec_name = 'display_name'
    _check_company_auto = True

    # ========================================
    # FIELD DEFINITIONS
    # ========================================

    # -------------------
    # Basic Fields
    # -------------------

    # Char fields - String with size limit
    name = fields.Char(
        string='Project Name',
        required=True,
        index='btree',  # Database index for faster searches
        tracking=True,  # Track changes in chatter
        copy=False,  # Don't copy when duplicating
        help="Enter the project name",
        default=lambda self: _('New'),
    )

    code = fields.Char(
        string='Project Code',
        size=10,  # Maximum length
        required=True,
        copy=False,
        index=True,
        tracking=True,
        help="Unique code for this project (e.g., PROJ-001)",
    )

    reference = fields.Char(
        string='External Reference',
        copy=False,
        help="External reference number from customer",
    )

    # Text fields - Multiline text without size limit
    description = fields.Text(
        string='Description',
        translate=True,  # Enable translation for multi-language support
        help="Detailed project description",
    )

    internal_notes = fields.Text(
        string='Internal Notes',
        groups='base.group_user',  # Only internal users can see
        help="Internal notes not visible to customers",
    )

    # Html fields - Rich text editor
    specification = fields.Html(
        string='Technical Specification',
        sanitize=True,  # Remove dangerous HTML
        sanitize_style=True,  # Remove dangerous CSS
        translate=True,
        help="Technical specifications in HTML format",
    )

    # Boolean fields
    active = fields.Boolean(
        string='Active',
        default=True,
        help="If unchecked, this record is archived",
    )

    is_template = fields.Boolean(
        string='Is Template',
        default=False,
        copy=False,
        help="Check if this project is a template",
    )

    is_billable = fields.Boolean(
        string='Billable',
        default=True,
        tracking=True,
        help="Check if this project is billable to customer",
    )

    # Integer fields
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering",
    )

    expected_duration_days = fields.Integer(
        string='Expected Duration (Days)',
        default=30,
        tracking=True,
        help="Expected project duration in days",
    )

    task_count = fields.Integer(
        string='Task Count',
        compute='_compute_task_count',
        store=False,  # Don't store in database
        help="Number of tasks in this project",
    )

    # Float fields
    budget = fields.Float(
        string='Budget',
        digits=(12, 2),  # Total 12 digits, 2 decimals
        default=0.0,
        tracking=True,
        help="Project budget amount",
    )

    progress = fields.Float(
        string='Progress',
        compute='_compute_progress',
        store=True,
        group_operator='avg',  # Average when grouping
        help="Project completion percentage (0-100)",
    )

    # Monetary fields
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    amount_total = fields.Monetary(
        string='Total Amount',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=True,
        tracking=True,
        help="Total project amount",
    )

    amount_invoiced = fields.Monetary(
        string='Invoiced Amount',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=True,
        help="Total invoiced amount",
    )

    amount_remaining = fields.Monetary(
        string='Remaining Amount',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=True,
        help="Remaining amount to invoice",
    )

    # Date fields
    date_start = fields.Date(
        string='Start Date',
        default=fields.Date.context_today,
        required=True,
        tracking=True,
        copy=False,
        help="Project start date",
    )

    date_end = fields.Date(
        string='End Date',
        tracking=True,
        copy=False,
        help="Expected project end date",
    )

    date_deadline = fields.Date(
        string='Deadline',
        tracking=True,
        help="Final deadline for project completion",
    )

    # Datetime fields
    last_update_date = fields.Datetime(
        string='Last Update',
        readonly=True,
        copy=False,
        help="Last modification date and time",
    )

    date_approved = fields.Datetime(
        string='Approval Date',
        readonly=True,
        copy=False,
        tracking=True,
        help="Date and time when project was approved",
    )

    # Binary fields
    attachment = fields.Binary(
        string='Attachment',
        attachment=True,  # Store in filestore instead of database
        help="Attach project documents",
    )

    attachment_name = fields.Char(
        string='Attachment Name',
    )

    # Image fields (enhanced binary with resize)
    image_1920 = fields.Image(
        string='Image',
        max_width=1920,
        max_height=1920,
    )

    image_512 = fields.Image(
        string='Image 512',
        related='image_1920',
        max_width=512,
        max_height=512,
        store=True,
    )

    image_128 = fields.Image(
        string='Image 128',
        related='image_1920',
        max_width=128,
        max_height=128,
        store=True,
    )

    # Selection fields
    priority = fields.Selection(
        selection=[
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High'),
            ('3', 'Urgent'),
        ],
        string='Priority',
        default='1',
        required=True,
        index=True,
        tracking=True,
        help="Project priority level",
    )

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('planning', 'Planning'),
            ('approved', 'Approved'),
            ('in_progress', 'In Progress'),
            ('on_hold', 'On Hold'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
        index=True,
        tracking=True,
        copy=False,
        group_expand='_expand_states',
        help="Current project status",
    )

    project_type = fields.Selection(
        selection=[
            ('internal', 'Internal'),
            ('customer', 'Customer Project'),
            ('maintenance', 'Maintenance'),
            ('development', 'Development'),
            ('consulting', 'Consulting'),
        ],
        string='Project Type',
        required=True,
        default='customer',
        help="Type of project",
    )

    # -------------------
    # Relational Fields
    # -------------------

    # Many2one - Foreign Key
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True,
        index=True,
        tracking=True,
        domain="[('customer_rank', '>', 0)]",
        context={'show_address': 1, 'show_vat': True},
        ondelete='restrict',  # Prevent deletion if used
        check_company=True,
        help="Customer for this project",
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Project Manager',
        default=lambda self: self.env.user,
        required=True,
        index=True,
        tracking=True,
        check_company=True,
        help="Responsible person for this project",
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )

    parent_id = fields.Many2one(
        comodel_name='complete.model.example',
        string='Parent Project',
        index=True,
        ondelete='cascade',
        check_company=True,
        help="Parent project for sub-projects",
    )

    template_id = fields.Many2one(
        comodel_name='complete.model.example',
        string='Template',
        domain=[('is_template', '=', True)],
        help="Project template to use",
    )

    # One2many - Reverse Foreign Key
    task_ids = fields.One2many(
        comodel_name='complete.model.task',
        inverse_name='project_id',
        string='Tasks',
        copy=True,
        help="Project tasks",
    )

    child_ids = fields.One2many(
        comodel_name='complete.model.example',
        inverse_name='parent_id',
        string='Sub-Projects',
        help="Child projects",
    )

    timesheet_ids = fields.One2many(
        comodel_name='complete.model.timesheet',
        inverse_name='project_id',
        string='Timesheets',
        help="Time entries for this project",
    )

    # Many2many - Junction Table
    tag_ids = fields.Many2many(
        comodel_name='complete.model.tag',
        relation='complete_model_example_tag_rel',  # Table name
        column1='project_id',  # This model column
        column2='tag_id',  # Other model column
        string='Tags',
        help="Project tags for categorization",
    )

    team_member_ids = fields.Many2many(
        comodel_name='res.users',
        relation='complete_model_example_user_rel',
        column1='project_id',
        column2='user_id',
        string='Team Members',
        check_company=True,
        help="Project team members",
    )

    allowed_user_ids = fields.Many2many(
        comodel_name='res.users',
        compute='_compute_allowed_users',
        string='Allowed Users',
        help="Users who can access this project",
    )

    # -------------------
    # Related Fields (shortcuts)
    # -------------------

    partner_email = fields.Char(
        string='Customer Email',
        related='partner_id.email',
        readonly=True,
        store=False,
    )

    partner_phone = fields.Char(
        string='Customer Phone',
        related='partner_id.phone',
        readonly=True,
    )

    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True,
    )

    # -------------------
    # Computed Fields
    # -------------------

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        index=True,
    )

    days_remaining = fields.Integer(
        string='Days Remaining',
        compute='_compute_days_remaining',
        help="Days until deadline",
    )

    is_overdue = fields.Boolean(
        string='Overdue',
        compute='_compute_is_overdue',
        search='_search_is_overdue',
        help="Project is past deadline",
    )

    completion_rate = fields.Float(
        string='Completion Rate',
        compute='_compute_completion_rate',
        store=True,
        help="Task completion percentage",
    )

    total_hours_planned = fields.Float(
        string='Planned Hours',
        compute='_compute_hours',
        store=True,
        help="Total planned hours",
    )

    total_hours_spent = fields.Float(
        string='Hours Spent',
        compute='_compute_hours',
        store=True,
        help="Total hours spent",
    )

    # Property field (company-specific values)
    default_task_stage_id = fields.Many2one(
        'complete.model.stage',
        string='Default Task Stage',
        company_dependent=True,
        help="Default stage for new tasks",
    )

    # ========================================
    # SQL CONSTRAINTS
    # ========================================

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code, company_id)',
         'Project code must be unique per company!'),

        ('budget_positive', 'CHECK(budget >= 0)',
         'Budget must be a positive value!'),

        ('progress_valid', 'CHECK(progress >= 0 AND progress <= 100)',
         'Progress must be between 0 and 100!'),

        ('date_check', 'CHECK(date_end >= date_start)',
         'End date must be after start date!'),
    ]

    # ========================================
    # COMPUTE METHODS
    # ========================================

    @api.depends('name', 'code')
    def _compute_display_name(self):
        """Compute display name combining code and name"""
        for record in self:
            if record.code and record.name:
                record.display_name = f"[{record.code}] {record.name}"
            else:
                record.display_name = record.name or record.code or _('New')

    @api.depends('task_ids')
    def _compute_task_count(self):
        """Compute number of tasks"""
        for record in self:
            record.task_count = len(record.task_ids)

    @api.depends('task_ids.progress')
    def _compute_progress(self):
        """Compute overall project progress based on tasks"""
        for record in self:
            if record.task_ids:
                record.progress = sum(record.task_ids.mapped('progress')) / len(record.task_ids)
            else:
                record.progress = 0.0

    @api.depends('task_ids.state')
    def _compute_completion_rate(self):
        """Compute task completion percentage"""
        for record in self:
            if record.task_ids:
                done_tasks = record.task_ids.filtered(lambda t: t.state == 'done')
                record.completion_rate = (len(done_tasks) / len(record.task_ids)) * 100
            else:
                record.completion_rate = 0.0

    @api.depends('task_ids.amount', 'task_ids.amount_invoiced')
    def _compute_amounts(self):
        """Compute monetary amounts"""
        for record in self:
            record.amount_total = sum(record.task_ids.mapped('amount'))
            record.amount_invoiced = sum(record.task_ids.mapped('amount_invoiced'))
            record.amount_remaining = record.amount_total - record.amount_invoiced

    @api.depends('date_deadline')
    def _compute_days_remaining(self):
        """Compute days until deadline"""
        today = fields.Date.context_today(self)
        for record in self:
            if record.date_deadline:
                delta = record.date_deadline - today
                record.days_remaining = delta.days
            else:
                record.days_remaining = 0

    @api.depends('date_deadline', 'state')
    def _compute_is_overdue(self):
        """Check if project is overdue"""
        today = fields.Date.context_today(self)
        for record in self:
            record.is_overdue = (
                record.date_deadline and
                record.date_deadline < today and
                record.state not in ('done', 'cancelled')
            )

    @api.depends('timesheet_ids.hours_planned', 'timesheet_ids.hours_spent')
    def _compute_hours(self):
        """Compute planned and spent hours"""
        for record in self:
            record.total_hours_planned = sum(record.timesheet_ids.mapped('hours_planned'))
            record.total_hours_spent = sum(record.timesheet_ids.mapped('hours_spent'))

    @api.depends('user_id', 'team_member_ids')
    def _compute_allowed_users(self):
        """Compute users who can access this project"""
        for record in self:
            allowed = record.team_member_ids | record.user_id
            record.allowed_user_ids = allowed

    # ========================================
    # SEARCH METHODS
    # ========================================

    def _search_is_overdue(self, operator, value):
        """Search method for is_overdue computed field"""
        today = fields.Date.context_today(self)

        if (operator == '=' and value) or (operator == '!=' and not value):
            # Search for overdue projects
            return [
                ('date_deadline', '<', today),
                ('state', 'not in', ('done', 'cancelled')),
            ]
        else:
            # Search for not overdue projects
            return [
                '|',
                ('date_deadline', '>=', today),
                ('date_deadline', '=', False),
                ('state', 'in', ('done', 'cancelled')),
            ]

    # ========================================
    # CONSTRAINT METHODS
    # ========================================

    @api.constrains('date_start', 'date_end', 'date_deadline')
    def _check_dates(self):
        """Validate date consistency"""
        for record in self:
            if record.date_start and record.date_end:
                if record.date_end < record.date_start:
                    raise ValidationError(_(
                        'End date cannot be before start date.\n'
                        'Start: %(start)s\n'
                        'End: %(end)s',
                        start=format_date(self.env, record.date_start),
                        end=format_date(self.env, record.date_end),
                    ))

            if record.date_deadline and record.date_start:
                if record.date_deadline < record.date_start:
                    raise ValidationError(_(
                        'Deadline cannot be before start date.\n'
                        'Start: %(start)s\n'
                        'Deadline: %(deadline)s',
                        start=format_date(self.env, record.date_start),
                        deadline=format_date(self.env, record.date_deadline),
                    ))

    @api.constrains('budget', 'amount_total')
    def _check_budget(self):
        """Check budget is not exceeded"""
        for record in self:
            if record.budget and record.amount_total:
                if float_compare(
                    record.amount_total,
                    record.budget,
                    precision_rounding=record.currency_id.rounding
                ) > 0:
                    raise ValidationError(_(
                        'Total amount (%(total)s) exceeds budget (%(budget)s)!',
                        total=record.amount_total,
                        budget=record.budget,
                    ))

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        """Prevent circular parent relationships"""
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive projects.'))

    @api.constrains('user_id', 'team_member_ids')
    def _check_manager_in_team(self):
        """Ensure project manager is in team"""
        for record in self:
            if record.user_id and record.user_id not in record.team_member_ids:
                raise ValidationError(_(
                    'Project Manager must be in the team members list.'
                ))

    # ========================================
    # ONCHANGE METHODS
    # ========================================

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Update fields when partner changes"""
        if self.partner_id:
            # Update currency from partner
            if self.partner_id.property_product_pricelist:
                self.currency_id = self.partner_id.property_product_pricelist.currency_id

            # Suggest project manager from partner
            if self.partner_id.user_id:
                self.user_id = self.partner_id.user_id

            # Warning if partner has no email
            if not self.partner_id.email:
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _(
                            'The selected customer has no email address.\n'
                            'Communication may be limited.'
                        ),
                    }
                }

    @api.onchange('template_id')
    def _onchange_template_id(self):
        """Load values from template"""
        if self.template_id:
            # Copy fields from template
            self.project_type = self.template_id.project_type
            self.is_billable = self.template_id.is_billable
            self.budget = self.template_id.budget
            self.expected_duration_days = self.template_id.expected_duration_days

            # Copy tags
            self.tag_ids = [Command.set(self.template_id.tag_ids.ids)]

            # Copy tasks from template
            task_commands = []
            for template_task in self.template_id.task_ids:
                task_commands.append(Command.create({
                    'name': template_task.name,
                    'description': template_task.description,
                    'hours_planned': template_task.hours_planned,
                }))
            self.task_ids = task_commands

    @api.onchange('date_start', 'expected_duration_days')
    def _onchange_date_start(self):
        """Calculate end date based on duration"""
        if self.date_start and self.expected_duration_days:
            self.date_end = self.date_start + timedelta(days=self.expected_duration_days)
            self.date_deadline = self.date_end + timedelta(days=7)  # 1 week buffer

    @api.onchange('user_id')
    def _onchange_user_id(self):
        """Add manager to team members"""
        if self.user_id and self.user_id not in self.team_member_ids:
            self.team_member_ids = [Command.link(self.user_id.id)]

    # ========================================
    # CRUD METHODS
    # ========================================

    @api.model_create_multi
    def create(self, vals_list):
        """
        Create projects with auto-generated code if needed

        Override to:
        - Generate sequence code
        - Set default dates
        - Create default tasks
        - Send notifications
        """
        for vals in vals_list:
            # Generate code from sequence if not provided
            if 'code' not in vals or vals['code'] == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'complete.model.example'
                ) or _('New')

            # Set current company if not specified
            if 'company_id' not in vals:
                vals['company_id'] = self.env.company.id

            # Calculate end date if not provided
            if 'date_start' in vals and 'date_end' not in vals:
                if 'expected_duration_days' in vals:
                    start_date = fields.Date.to_date(vals['date_start'])
                    vals['date_end'] = start_date + timedelta(
                        days=vals['expected_duration_days']
                    )

        # Create records
        projects = super().create(vals_list)

        # Post-creation operations
        for project in projects:
            # Add manager to team
            if project.user_id and project.user_id not in project.team_member_ids:
                project.team_member_ids = [Command.link(project.user_id.id)]

            # Create default tasks if template was used
            if project.template_id and not project.task_ids:
                project._create_tasks_from_template()

            # Send notification
            project._send_creation_notification()

            # Log creation
            project.message_post(
                body=_('Project created by %(user)s', user=self.env.user.name),
                message_type='notification',
            )

        return projects

    def write(self, vals):
        """
        Update projects with validation and logging

        Override to:
        - Validate state transitions
        - Track important changes
        - Update related records
        - Send notifications
        """
        # Track state changes for notification
        state_changes = {}
        if 'state' in vals:
            for project in self:
                state_changes[project.id] = {
                    'old': project.state,
                    'new': vals['state'],
                }

        # Validate state transitions
        if 'state' in vals:
            self._validate_state_transition(vals['state'])

        # Update last_update_date
        vals['last_update_date'] = fields.Datetime.now()

        # Update records
        result = super().write(vals)

        # Post-update operations
        if 'state' in vals:
            self._handle_state_change(state_changes)

        # Notify team members of important changes
        if any(key in vals for key in ['user_id', 'date_deadline', 'priority']):
            self._notify_team_changes(vals)

        return result

    def unlink(self):
        """
        Delete projects with validation

        Override to:
        - Prevent deletion in certain states
        - Archive instead of delete
        - Clean up related records
        """
        # Check if any project is in a non-deletable state
        non_deletable = self.filtered(
            lambda p: p.state not in ('draft', 'cancelled')
        )
        if non_deletable:
            raise UserError(_(
                'Cannot delete projects in state: %(states)s\n'
                'Projects: %(names)s\n\n'
                'Please cancel them first.',
                states=', '.join(non_deletable.mapped('state')),
                names=', '.join(non_deletable.mapped('name')),
            ))

        # Check for related invoices
        projects_with_invoices = self.filtered(
            lambda p: float_compare(
                p.amount_invoiced, 0,
                precision_rounding=p.currency_id.rounding
            ) > 0
        )
        if projects_with_invoices:
            raise UserError(_(
                'Cannot delete projects with invoiced amounts.\n'
                'Projects: %(names)s',
                names=', '.join(projects_with_invoices.mapped('name')),
            ))

        # Archive instead of delete if context flag set
        if self.env.context.get('soft_delete'):
            return self.write({'active': False})

        # Log deletion
        for project in self:
            _logger.info(
                'Deleting project: %s (ID: %s) by user: %s',
                project.name, project.id, self.env.user.name
            )

        return super().unlink()

    def copy(self, default=None):
        """
        Duplicate project with custom defaults

        Override to:
        - Reset dates
        - Generate new code
        - Clear computed values
        """
        self.ensure_one()

        default = dict(default or {})

        # Set new name
        default.setdefault('name', _("%s (Copy)", self.name))

        # Generate new code
        default.setdefault('code', self.env['ir.sequence'].next_by_code(
            'complete.model.example'
        ))

        # Reset dates
        today = fields.Date.context_today(self)
        default.setdefault('date_start', today)

        if self.expected_duration_days:
            default.setdefault(
                'date_end',
                today + timedelta(days=self.expected_duration_days)
            )

        # Reset state
        default.setdefault('state', 'draft')

        # Clear approval date
        default.setdefault('date_approved', False)

        return super().copy(default=default)

    # ========================================
    # ACTION METHODS (Button Methods)
    # ========================================

    def action_plan(self):
        """Move project to planning state"""
        self.ensure_one()

        if self.state != 'draft':
            raise UserError(_('Only draft projects can be planned.'))

        # Validation
        if not self.task_ids:
            raise UserError(_(
                'Cannot plan project without tasks.\n'
                'Please add at least one task.'
            ))

        self.write({'state': 'planning'})

        self.message_post(
            body=_('Project moved to planning stage.'),
            subject=_('Planning Started'),
        )

        return True

    def action_approve(self):
        """Approve project"""
        self.ensure_one()

        if self.state not in ('draft', 'planning'):
            raise UserError(_('Only draft or planning projects can be approved.'))

        # Check permissions
        if not self.env.user.has_group('base.group_system'):
            raise AccessError(_('Only managers can approve projects.'))

        # Validation
        self._validate_approval()

        self.write({
            'state': 'approved',
            'date_approved': fields.Datetime.now(),
        })

        # Notify team
        self.message_post(
            body=_('Project approved by %(user)s', user=self.env.user.name),
            subject=_('Project Approved'),
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )

        # Create activities for team members
        self._create_team_activities()

        return True

    def action_start(self):
        """Start project execution"""
        self.ensure_one()

        if self.state != 'approved':
            raise UserError(_('Only approved projects can be started.'))

        self.write({'state': 'in_progress'})

        # Start first tasks
        first_tasks = self.task_ids.filtered(lambda t: t.state == 'draft')[:5]
        if first_tasks:
            first_tasks.write({'state': 'in_progress'})

        return True

    def action_hold(self):
        """Put project on hold"""
        self.ensure_one()

        if self.state != 'in_progress':
            raise UserError(_('Only in-progress projects can be put on hold.'))

        # Get reason from wizard
        return {
            'name': _('Put Project on Hold'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.hold.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_project_id': self.id,
            },
        }

    def action_resume(self):
        """Resume project from hold"""
        self.ensure_one()

        if self.state != 'on_hold':
            raise UserError(_('Only on-hold projects can be resumed.'))

        self.write({'state': 'in_progress'})

        return True

    def action_done(self):
        """Mark project as done"""
        self.ensure_one()

        if self.state not in ('in_progress', 'approved'):
            raise UserError(_('Only in-progress or approved projects can be completed.'))

        # Validation
        incomplete_tasks = self.task_ids.filtered(lambda t: t.state != 'done')
        if incomplete_tasks:
            return {
                'warning': {
                    'title': _('Warning'),
                    'message': _(
                        'There are %(count)s incomplete tasks.\n'
                        'Are you sure you want to complete this project?',
                        count=len(incomplete_tasks),
                    ),
                }
            }

        self.write({'state': 'done'})

        # Send completion notification
        self._send_completion_notification()

        return True

    def action_cancel(self):
        """Cancel project"""
        if any(p.state == 'done' for p in self):
            raise UserError(_('Cannot cancel completed projects.'))

        self.write({'state': 'cancelled'})

        # Cancel all tasks
        self.task_ids.action_cancel()

        return True

    def action_reset_to_draft(self):
        """Reset to draft state"""
        if any(p.state not in ('cancelled', 'planning') for p in self):
            raise UserError(_(
                'Only cancelled or planning projects can be reset to draft.'
            ))

        self.write({
            'state': 'draft',
            'date_approved': False,
        })

        return True

    # ========================================
    # BUSINESS METHODS
    # ========================================

    def _create_tasks_from_template(self):
        """Create tasks from project template"""
        self.ensure_one()

        if not self.template_id:
            return

        task_vals_list = []
        for template_task in self.template_id.task_ids:
            task_vals_list.append({
                'project_id': self.id,
                'name': template_task.name,
                'description': template_task.description,
                'hours_planned': template_task.hours_planned,
                'user_id': template_task.user_id.id,
            })

        if task_vals_list:
            self.env['complete.model.task'].create(task_vals_list)

    def _validate_approval(self):
        """Validate project can be approved"""
        self.ensure_one()

        errors = []

        # Check required fields
        if not self.partner_id:
            errors.append(_('Customer is required'))

        if not self.user_id:
            errors.append(_('Project Manager is required'))

        if not self.task_ids:
            errors.append(_('At least one task is required'))

        if not self.date_start:
            errors.append(_('Start date is required'))

        if not self.date_deadline:
            errors.append(_('Deadline is required'))

        if float_is_zero(self.budget, precision_rounding=self.currency_id.rounding):
            errors.append(_('Budget must be set'))

        if errors:
            raise ValidationError('\n'.join(errors))

    def _validate_state_transition(self, new_state):
        """Validate state transitions"""
        valid_transitions = {
            'draft': ['planning', 'cancelled'],
            'planning': ['draft', 'approved', 'cancelled'],
            'approved': ['in_progress', 'cancelled'],
            'in_progress': ['on_hold', 'done', 'cancelled'],
            'on_hold': ['in_progress', 'cancelled'],
            'done': [],
            'cancelled': ['draft'],
        }

        for project in self:
            if new_state not in valid_transitions.get(project.state, []):
                raise UserError(_(
                    'Invalid state transition from %(from)s to %(to)s for project %(name)s',
                    from_=project.state,
                    to=new_state,
                    name=project.name,
                ))

    def _handle_state_change(self, state_changes):
        """Handle state change side effects"""
        for project in self:
            if project.id not in state_changes:
                continue

            change = state_changes[project.id]

            # Log state change
            project.message_post(
                body=_('State changed from %(old)s to %(new)s by %(user)s',
                      old=change['old'],
                      new=change['new'],
                      user=self.env.user.name),
            )

            # State-specific actions
            if change['new'] == 'approved':
                project._create_team_activities()

            elif change['new'] == 'done':
                project._send_completion_notification()

    def _send_creation_notification(self):
        """Send notification when project is created"""
        self.ensure_one()

        if self.user_id:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=self.user_id.id,
                summary=_('New Project Assigned'),
                note=_('You have been assigned as manager for project: %(name)s',
                      name=self.name),
            )

    def _send_completion_notification(self):
        """Send notification when project is completed"""
        self.ensure_one()

        # Notify customer
        if self.partner_id.email:
            template = self.env.ref('module.email_template_project_completion')
            template.send_mail(self.id, force_send=True)

        # Notify team
        for member in self.team_member_ids:
            self.message_notify(
                partner_ids=member.partner_id.ids,
                subject=_('Project Completed: %(name)s', name=self.name),
                body=_('The project has been marked as completed.'),
            )

    def _create_team_activities(self):
        """Create activities for team members"""
        self.ensure_one()

        for member in self.team_member_ids:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=member.id,
                summary=_('Project Started'),
                note=_('Project %(name)s has been approved and is ready to start.',
                      name=self.name),
            )

    def _notify_team_changes(self, vals):
        """Notify team of important changes"""
        self.ensure_one()

        changes = []

        if 'user_id' in vals:
            new_manager = self.env['res.users'].browse(vals['user_id'])
            changes.append(_('Project Manager: %(name)s', name=new_manager.name))

        if 'date_deadline' in vals:
            changes.append(_('Deadline: %(date)s',
                           date=format_date(self.env, vals['date_deadline'])))

        if 'priority' in vals:
            priority_dict = dict(self._fields['priority'].selection)
            changes.append(_('Priority: %(priority)s',
                           priority=priority_dict[vals['priority']]))

        if changes:
            body = _('Project updated:\n') + '\n'.join(changes)
            self.message_post(body=body, message_type='notification')

    # ========================================
    # ORM OVERRIDE METHODS
    # ========================================

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        """
        Custom name search to search by code and name

        Args:
            name: Search term
            domain: Additional domain
            operator: Search operator
            limit: Result limit
            order: Sort order

        Returns:
            List of IDs matching search
        """
        domain = domain or []

        if name:
            # Search by code or name
            domain = [
                '|',
                ('code', operator, name),
                ('name', operator, name),
            ] + domain

        return self._search(domain, limit=limit, order=order)

    def name_get(self):
        """
        Custom display name format

        Returns:
            List of (id, name) tuples
        """
        result = []
        for project in self:
            if project.code and project.name:
                name = f"[{project.code}] {project.name}"
            else:
                name = project.name or project.code or _('New')

            result.append((project.id, name))

        return result

    @api.model
    def _expand_states(self, states, domain, order):
        """
        Expand states for kanban view grouping

        Returns all possible states for kanban columns
        """
        return [key for key, _ in self._fields['state'].selection]

    # ========================================
    # HELPER METHODS
    # ========================================

    def _get_report_base_filename(self):
        """Filename for report downloads"""
        self.ensure_one()
        return f'Project_{self.code}_{self.name}'

    @api.model
    def get_empty_list_help(self, help_message):
        """Custom help message for empty list view"""
        return super().get_empty_list_help(
            _("""
                <p class="o_view_nocontent_smiling_face">
                    Create your first project
                </p>
                <p>
                    Projects help you organize and track your work.
                </p>
            """)
        )

