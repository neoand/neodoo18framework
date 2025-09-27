# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class TemplateModel(models.Model):
    _name = 'template.model'
    _description = 'Template Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(
        string='Name',
        required=True,
        tracking=True
    )
    
    description = fields.Text(
        string='Description',
        tracking=True
    )
    
    active = fields.Boolean(
        default=True,
        tracking=True
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], default='draft', tracking=True)
    
    date = fields.Date(
        string='Date',
        default=fields.Date.context_today
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        tracking=True
    )
    
    reference = fields.Char(
        string='Reference',
        copy=False,
        readonly=True
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('template.model')
        return super().create(vals_list)
    
    @api.depends('name', 'reference')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.reference or ''} - {record.name}"
    
    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
    
    def action_done(self):
        for record in self:
            record.state = 'done'
    
    def action_draft(self):
        for record in self:
            record.state = 'draft'