# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)

class {{MODULE_CLASS}}(models.Model):
    _name = '{{MODULE_TECHNICAL_NAME}}.{{MODEL_NAME}}'
    _description = '{{MODEL_DESCRIPTION}}'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    
    # Basic fields
    name = fields.Char(
        string='Name', 
        required=True, 
        tracking=True,
        help="Name of the {{MODEL_DESCRIPTION}}"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True,
        help="If unchecked, it will allow you to hide the record without removing it"
    )
    
    description = fields.Text(
        string='Description',
        help="Additional description"
    )
    
    # Computed field example
    @api.depends('name')
    def _compute_display_name(self):
        """Compute display name"""
        for record in self:
            record.display_name = record.name or _('New')
    
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True
    )
    
    # Constraints
    @api.constrains('name')
    def _check_name(self):
        """Validate name field"""
        for record in self:
            if record.name and len(record.name) < 2:
                raise ValidationError(_("Name must have at least 2 characters"))
    
    # SQL Constraints
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name must be unique!'),
    ]
    
    # Actions
    def action_archive(self):
        """Archive records"""
        self.ensure_one()
        self.write({'active': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Archived'),
                'message': _('Records have been archived successfully.'),
                'type': 'success',
            }
        }
    
    def action_unarchive(self):
        """Unarchive records"""
        self.ensure_one()
        self.write({'active': True})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Unarchived'),
                'message': _('Records have been unarchived successfully.'),
                'type': 'success',
            }
        }