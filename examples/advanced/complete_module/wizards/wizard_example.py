# -*- coding: utf-8 -*-
"""
Complete Wizard Example for Odoo 18

This file demonstrates wizard (TransientModel) implementation including:
- Multi-step wizard flow
- Default methods
- Complex actions
- Batch processing
- Report generation
- Data import/export
"""

from odoo import api, fields, models, Command, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_date

import base64
import csv
import io
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class ProjectMassUpdateWizard(models.TransientModel):
    """
    Mass Update Wizard

    Simple wizard to update multiple projects at once
    Demonstrates basic wizard pattern
    """
    _name = 'project.mass.update.wizard'
    _description = 'Mass Update Projects'

    # Fields
    project_ids = fields.Many2many(
        'complete.model.example',
        string='Projects',
        required=True,
        help="Projects to update",
    )

    update_type = fields.Selection([
        ('manager', 'Change Manager'),
        ('priority', 'Update Priority'),
        ('tags', 'Add Tags'),
        ('deadline', 'Extend Deadline'),
    ], string='Update Type', required=True)

    # Update fields
    user_id = fields.Many2one(
        'res.users',
        string='New Manager',
    )

    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], string='New Priority')

    tag_ids = fields.Many2many(
        'complete.model.tag',
        string='Tags to Add',
    )

    days_to_extend = fields.Integer(
        string='Days to Extend',
        default=7,
    )

    # Default method
    @api.model
    def default_get(self, fields_list):
        """Set default values from context"""
        res = super().default_get(fields_list)

        # Get active projects from context
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['project_ids'] = [Command.set(active_ids)]

        return res

    # Action method
    def action_update(self):
        """Execute mass update"""
        self.ensure_one()

        if not self.project_ids:
            raise UserError(_('Please select at least one project.'))

        # Prepare values based on update type
        vals = {}

        if self.update_type == 'manager':
            if not self.user_id:
                raise UserError(_('Please select a new manager.'))
            vals['user_id'] = self.user_id.id

        elif self.update_type == 'priority':
            if not self.priority:
                raise UserError(_('Please select a priority.'))
            vals['priority'] = self.priority

        elif self.update_type == 'tags':
            if not self.tag_ids:
                raise UserError(_('Please select at least one tag.'))
            # Add tags without removing existing ones
            vals['tag_ids'] = [Command.link(tag.id) for tag in self.tag_ids]

        elif self.update_type == 'deadline':
            # Extend deadline for each project
            for project in self.project_ids:
                if project.date_deadline:
                    new_deadline = project.date_deadline + timedelta(days=self.days_to_extend)
                    project.write({'date_deadline': new_deadline})
            return {'type': 'ir.actions.act_window_close'}

        # Update all projects
        self.project_ids.write(vals)

        # Show notification
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('%(count)s project(s) updated successfully.',
                           count=len(self.project_ids)),
                'type': 'success',
                'sticky': False,
            }
        }


class ProjectReportWizard(models.TransientModel):
    """
    Report Generation Wizard

    Multi-step wizard for report generation
    Demonstrates wizard flow and PDF generation
    """
    _name = 'project.report.wizard'
    _description = 'Project Report Generator'

    # Step 1: Selection
    state = fields.Selection([
        ('selection', 'Selection'),
        ('options', 'Options'),
        ('preview', 'Preview'),
    ], default='selection', required=True)

    report_type = fields.Selection([
        ('summary', 'Summary Report'),
        ('detailed', 'Detailed Report'),
        ('timesheet', 'Timesheet Report'),
        ('financial', 'Financial Report'),
    ], string='Report Type', required=True, default='summary')

    # Filters
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        domain="[('customer_rank', '>', 0)]",
    )

    date_from = fields.Date(
        string='From Date',
        default=lambda self: fields.Date.today() - timedelta(days=30),
    )

    date_to = fields.Date(
        string='To Date',
        default=fields.Date.today,
    )

    state_filter = fields.Selection([
        ('all', 'All States'),
        ('in_progress', 'In Progress Only'),
        ('done', 'Completed Only'),
    ], default='all', required=True)

    # Step 2: Options
    include_tasks = fields.Boolean(
        string='Include Tasks',
        default=True,
    )

    include_timesheets = fields.Boolean(
        string='Include Timesheets',
        default=False,
    )

    include_financials = fields.Boolean(
        string='Include Financial Data',
        default=False,
    )

    group_by = fields.Selection([
        ('customer', 'Customer'),
        ('manager', 'Project Manager'),
        ('state', 'Status'),
    ], string='Group By')

    # Step 3: Preview
    project_count = fields.Integer(
        string='Projects',
        compute='_compute_preview_data',
    )

    total_amount = fields.Monetary(
        string='Total Amount',
        compute='_compute_preview_data',
        currency_field='currency_id',
    )

    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id,
    )

    @api.depends('partner_id', 'date_from', 'date_to', 'state_filter')
    def _compute_preview_data(self):
        """Compute preview statistics"""
        for wizard in self:
            domain = wizard._get_project_domain()
            projects = self.env['complete.model.example'].search(domain)

            wizard.project_count = len(projects)
            wizard.total_amount = sum(projects.mapped('amount_total'))

    def _get_project_domain(self):
        """Build domain for project search"""
        self.ensure_one()

        domain = []

        if self.partner_id:
            domain.append(('partner_id', '=', self.partner_id.id))

        if self.date_from:
            domain.append(('date_start', '>=', self.date_from))

        if self.date_to:
            domain.append(('date_end', '<=', self.date_to))

        if self.state_filter == 'in_progress':
            domain.append(('state', '=', 'in_progress'))
        elif self.state_filter == 'done':
            domain.append(('state', '=', 'done'))

        return domain

    def action_next(self):
        """Go to next step"""
        self.ensure_one()

        if self.state == 'selection':
            self.state = 'options'
        elif self.state == 'options':
            self.state = 'preview'

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_back(self):
        """Go to previous step"""
        self.ensure_one()

        if self.state == 'preview':
            self.state = 'options'
        elif self.state == 'options':
            self.state = 'selection'

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_generate_report(self):
        """Generate and download report"""
        self.ensure_one()

        # Get projects
        domain = self._get_project_domain()
        projects = self.env['complete.model.example'].search(domain)

        if not projects:
            raise UserError(_('No projects found matching the criteria.'))

        # Generate report based on type
        if self.report_type == 'summary':
            return self._generate_summary_report(projects)
        elif self.report_type == 'detailed':
            return self._generate_detailed_report(projects)
        elif self.report_type == 'timesheet':
            return self._generate_timesheet_report(projects)
        elif self.report_type == 'financial':
            return self._generate_financial_report(projects)

    def _generate_summary_report(self, projects):
        """Generate summary PDF report"""
        self.ensure_one()

        # Get PDF report action
        return self.env.ref('module.action_report_project_summary').report_action(
            projects,
            data={
                'include_tasks': self.include_tasks,
                'date_from': self.date_from,
                'date_to': self.date_to,
            }
        )

    def _generate_detailed_report(self, projects):
        """Generate detailed Excel report"""
        self.ensure_one()

        # Create Excel file
        output = io.BytesIO()
        workbook = self.env['ir.exports'].create_excel_report(
            projects,
            fields=['code', 'name', 'partner_id', 'state', 'amount_total'],
            headers=['Code', 'Name', 'Customer', 'Status', 'Amount'],
        )

        # Return download action
        attachment = self.env['ir.attachment'].create({
            'name': f'Project_Report_{datetime.now().strftime("%Y%m%d")}.xlsx',
            'datas': base64.b64encode(output.getvalue()),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def _generate_timesheet_report(self, projects):
        """Generate timesheet report"""
        # Implementation here
        pass

    def _generate_financial_report(self, projects):
        """Generate financial report"""
        # Implementation here
        pass


class ProjectImportWizard(models.TransientModel):
    """
    CSV Import Wizard

    Demonstrates file import functionality
    """
    _name = 'project.import.wizard'
    _description = 'Import Projects from CSV'

    # Upload
    file_data = fields.Binary(
        string='CSV File',
        required=True,
        help="Upload CSV file with project data",
    )

    file_name = fields.Char(
        string='File Name',
    )

    # Options
    update_existing = fields.Boolean(
        string='Update Existing',
        default=False,
        help="Update projects if code already exists",
    )

    create_customers = fields.Boolean(
        string='Create Customers',
        default=False,
        help="Create customers if they don't exist",
    )

    # Results
    import_log = fields.Text(
        string='Import Log',
        readonly=True,
    )

    success_count = fields.Integer(
        string='Successful',
        readonly=True,
    )

    error_count = fields.Integer(
        string='Errors',
        readonly=True,
    )

    def action_validate(self):
        """Validate CSV file"""
        self.ensure_one()

        if not self.file_data:
            raise UserError(_('Please upload a CSV file.'))

        try:
            # Decode file
            csv_data = base64.b64decode(self.file_data).decode('utf-8')
            csv_file = io.StringIO(csv_data)
            reader = csv.DictReader(csv_file)

            # Validate headers
            required_fields = ['code', 'name', 'customer']
            headers = reader.fieldnames

            missing = set(required_fields) - set(headers)
            if missing:
                raise UserError(_(
                    'Missing required columns: %(fields)s',
                    fields=', '.join(missing)
                ))

            # Validate data
            errors = []
            row_num = 1

            for row in reader:
                row_num += 1

                # Validate code
                if not row.get('code'):
                    errors.append(_('Row %(num)s: Code is required', num=row_num))

                # Validate dates
                if row.get('date_start'):
                    try:
                        datetime.strptime(row['date_start'], '%Y-%m-%d')
                    except ValueError:
                        errors.append(_(
                            'Row %(num)s: Invalid date format. Use YYYY-MM-DD',
                            num=row_num
                        ))

            if errors:
                self.import_log = '\n'.join(errors)
                raise UserError(_('Validation failed:\n%(errors)s',
                               errors='\n'.join(errors)))

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Validation Successful'),
                    'message': _('CSV file is valid. Ready to import.'),
                    'type': 'success',
                }
            }

        except Exception as e:
            raise UserError(_('Error reading CSV file: %(error)s', error=str(e)))

    def action_import(self):
        """Import projects from CSV"""
        self.ensure_one()

        # Decode file
        csv_data = base64.b64decode(self.file_data).decode('utf-8')
        csv_file = io.StringIO(csv_data)
        reader = csv.DictReader(csv_file)

        success = 0
        errors = 0
        log_lines = []

        for row_num, row in enumerate(reader, start=2):
            try:
                # Find or create customer
                customer = self._find_or_create_customer(row['customer'])
                if not customer:
                    raise UserError(_('Customer not found: %(name)s',
                                   name=row['customer']))

                # Prepare values
                vals = {
                    'code': row['code'],
                    'name': row['name'],
                    'partner_id': customer.id,
                    'description': row.get('description', ''),
                }

                # Add dates
                if row.get('date_start'):
                    vals['date_start'] = row['date_start']

                if row.get('budget'):
                    vals['budget'] = float(row['budget'])

                # Check if project exists
                existing = self.env['complete.model.example'].search([
                    ('code', '=', row['code']),
                ], limit=1)

                if existing:
                    if self.update_existing:
                        existing.write(vals)
                        log_lines.append(_(
                            'Row %(num)s: Updated project %(code)s',
                            num=row_num, code=row['code']
                        ))
                    else:
                        log_lines.append(_(
                            'Row %(num)s: Skipped (already exists): %(code)s',
                            num=row_num, code=row['code']
                        ))
                else:
                    # Create new project
                    self.env['complete.model.example'].create(vals)
                    log_lines.append(_(
                        'Row %(num)s: Created project %(code)s',
                        num=row_num, code=row['code']
                    ))

                success += 1

            except Exception as e:
                errors += 1
                log_lines.append(_(
                    'Row %(num)s: ERROR - %(error)s',
                    num=row_num, error=str(e)
                ))
                _logger.error('Import error on row %s: %s', row_num, str(e))

        # Update results
        self.write({
            'import_log': '\n'.join(log_lines),
            'success_count': success,
            'error_count': errors,
        })

        # Show result
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Import Complete'),
                'message': _(
                    'Success: %(success)s\nErrors: %(errors)s',
                    success=success, errors=errors
                ),
                'type': 'success' if errors == 0 else 'warning',
                'sticky': True,
            }
        }

    def _find_or_create_customer(self, name):
        """Find or create customer"""
        self.ensure_one()

        # Search by name
        partner = self.env['res.partner'].search([
            ('name', '=', name),
        ], limit=1)

        if not partner and self.create_customers:
            # Create new customer
            partner = self.env['res.partner'].create({
                'name': name,
                'customer_rank': 1,
            })

        return partner


class ProjectBatchActionWizard(models.TransientModel):
    """
    Batch Action Wizard

    Demonstrates batch operations on selected records
    """
    _name = 'project.batch.action.wizard'
    _description = 'Batch Actions on Projects'

    project_ids = fields.Many2many(
        'complete.model.example',
        string='Projects',
        required=True,
    )

    action = fields.Selection([
        ('approve', 'Approve All'),
        ('start', 'Start All'),
        ('cancel', 'Cancel All'),
        ('archive', 'Archive All'),
        ('export', 'Export to CSV'),
    ], string='Action', required=True)

    confirm_action = fields.Boolean(
        string='I confirm this action',
        help="Check to confirm batch action",
    )

    @api.model
    def default_get(self, fields_list):
        """Set default values"""
        res = super().default_get(fields_list)

        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['project_ids'] = [Command.set(active_ids)]

        return res

    def action_execute(self):
        """Execute batch action"""
        self.ensure_one()

        if not self.confirm_action:
            raise UserError(_('Please confirm the action.'))

        # Execute based on action type
        if self.action == 'approve':
            self._batch_approve()
        elif self.action == 'start':
            self._batch_start()
        elif self.action == 'cancel':
            self._batch_cancel()
        elif self.action == 'archive':
            self._batch_archive()
        elif self.action == 'export':
            return self._batch_export()

        return {'type': 'ir.actions.act_window_close'}

    def _batch_approve(self):
        """Approve all projects"""
        for project in self.project_ids:
            try:
                project.action_approve()
            except Exception as e:
                _logger.warning('Failed to approve project %s: %s',
                              project.name, str(e))

    def _batch_start(self):
        """Start all projects"""
        for project in self.project_ids:
            try:
                project.action_start()
            except Exception as e:
                _logger.warning('Failed to start project %s: %s',
                              project.name, str(e))

    def _batch_cancel(self):
        """Cancel all projects"""
        self.project_ids.action_cancel()

    def _batch_archive(self):
        """Archive all projects"""
        self.project_ids.write({'active': False})

    def _batch_export(self):
        """Export projects to CSV"""
        # Create CSV file
        output = io.StringIO()
        writer = csv.writer(output)

        # Write headers
        writer.writerow([
            'Code', 'Name', 'Customer', 'Manager',
            'State', 'Progress', 'Amount Total'
        ])

        # Write data
        for project in self.project_ids:
            writer.writerow([
                project.code,
                project.name,
                project.partner_id.name,
                project.user_id.name,
                project.state,
                f'{project.progress}%',
                project.amount_total,
            ])

        # Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'Projects_Export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            'datas': base64.b64encode(output.getvalue().encode()),
            'mimetype': 'text/csv',
        })

        # Download
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
