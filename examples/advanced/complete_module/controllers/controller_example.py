# -*- coding: utf-8 -*-
"""
Complete HTTP Controller Example for Odoo 18

Demonstrates:
- Public and authenticated routes
- JSON API endpoints
- File upload/download
- CORS handling
- Error handling
- Authentication methods
"""

from odoo import http, _
from odoo.http import request, Response
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import image_process

import json
import base64
import logging
from datetime import datetime
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

_logger = logging.getLogger(__name__)


class ProjectController(http.Controller):
    """
    Project API Controller

    Provides REST API for project management
    """

    # ========================================
    # PUBLIC ROUTES
    # ========================================

    @http.route('/api/projects/public', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_public_projects(self, **kwargs):
        """
        Get list of public projects (no authentication required)

        Query Parameters:
            - limit: int, number of records (default: 10)
            - offset: int, pagination offset (default: 0)

        Returns:
            JSON response with project list
        """
        try:
            limit = int(kwargs.get('limit', 10))
            offset = int(kwargs.get('offset', 0))

            # Search public projects
            projects = request.env['complete.model.example'].sudo().search([
                ('state', '=', 'done'),
            ], limit=limit, offset=offset)

            # Prepare response data
            data = []
            for project in projects:
                data.append({
                    'id': project.id,
                    'name': project.name,
                    'code': project.code,
                    'customer': project.partner_id.name,
                    'description': project.description,
                })

            return request.make_json_response({
                'status': 'success',
                'data': data,
                'total': len(projects),
            })

        except Exception as e:
            _logger.error('Error in get_public_projects: %s', str(e))
            return request.make_json_response({
                'status': 'error',
                'message': str(e),
            }, status=500)

    @http.route('/api/projects/<int:project_id>/public', type='http', auth='public', methods=['GET'], csrf=False)
    def get_public_project_detail(self, project_id, **kwargs):
        """Get single project details (public)"""
        try:
            project = request.env['complete.model.example'].sudo().browse(project_id)

            if not project.exists() or project.state != 'done':
                return request.make_json_response({
                    'status': 'error',
                    'message': 'Project not found',
                }, status=404)

            return request.make_json_response({
                'status': 'success',
                'data': {
                    'id': project.id,
                    'name': project.name,
                    'code': project.code,
                    'customer': project.partner_id.name,
                    'description': project.description,
                    'progress': project.progress,
                    'date_start': project.date_start.isoformat() if project.date_start else None,
                    'date_end': project.date_end.isoformat() if project.date_end else None,
                },
            })

        except Exception as e:
            _logger.error('Error getting project %s: %s', project_id, str(e))
            return request.make_json_response({
                'status': 'error',
                'message': str(e),
            }, status=500)

    # ========================================
    # AUTHENTICATED USER ROUTES
    # ========================================

    @http.route('/api/projects', type='json', auth='user', methods=['POST'])
    def get_projects(self, filters=None, fields=None, limit=100, offset=0, order='id desc'):
        """
        Get projects list (requires authentication)

        Args:
            filters: list, search domain
            fields: list, fields to return
            limit: int, max records
            offset: int, pagination
            order: str, sort order

        Returns:
            dict with projects data
        """
        try:
            # Build domain
            domain = filters or []

            # Search with access rights check
            projects = request.env['complete.model.example'].search(
                domain,
                limit=limit,
                offset=offset,
                order=order
            )

            # Read fields
            if not fields:
                fields = ['id', 'name', 'code', 'state', 'partner_id', 'progress']

            data = projects.read(fields)

            return {
                'status': 'success',
                'data': data,
                'total': len(data),
            }

        except Exception as e:
            _logger.error('Error in get_projects: %s', str(e))
            return {
                'status': 'error',
                'message': str(e),
            }

    @http.route('/api/projects/<int:project_id>', type='json', auth='user', methods=['POST'])
    def get_project(self, project_id, fields=None):
        """Get single project (authenticated)"""
        try:
            project = request.env['complete.model.example'].browse(project_id)

            if not project.exists():
                raise NotFound('Project not found')

            # Check access rights
            project.check_access_rights('read')
            project.check_access_rule('read')

            # Read fields
            if not fields:
                fields = ['id', 'name', 'code', 'description', 'state',
                         'partner_id', 'user_id', 'progress', 'amount_total']

            data = project.read(fields)[0]

            return {
                'status': 'success',
                'data': data,
            }

        except AccessError:
            return {
                'status': 'error',
                'message': 'Access denied',
            }
        except Exception as e:
            _logger.error('Error getting project: %s', str(e))
            return {
                'status': 'error',
                'message': str(e),
            }

    @http.route('/api/projects/create', type='json', auth='user', methods=['POST'])
    def create_project(self, **values):
        """Create new project"""
        try:
            # Validate required fields
            required = ['name', 'partner_id']
            missing = [f for f in required if f not in values]

            if missing:
                return {
                    'status': 'error',
                    'message': f'Missing required fields: {", ".join(missing)}',
                }

            # Create project
            project = request.env['complete.model.example'].create(values)

            return {
                'status': 'success',
                'message': 'Project created successfully',
                'data': {
                    'id': project.id,
                    'code': project.code,
                    'name': project.name,
                },
            }

        except ValidationError as e:
            return {
                'status': 'error',
                'message': str(e),
            }
        except Exception as e:
            _logger.error('Error creating project: %s', str(e))
            return {
                'status': 'error',
                'message': 'Internal server error',
            }

    @http.route('/api/projects/<int:project_id>/update', type='json', auth='user', methods=['POST'])
    def update_project(self, project_id, **values):
        """Update project"""
        try:
            project = request.env['complete.model.example'].browse(project_id)

            if not project.exists():
                return {
                    'status': 'error',
                    'message': 'Project not found',
                }

            # Check write access
            project.check_access_rights('write')
            project.check_access_rule('write')

            # Update
            project.write(values)

            return {
                'status': 'success',
                'message': 'Project updated successfully',
            }

        except AccessError:
            return {
                'status': 'error',
                'message': 'Access denied',
            }
        except ValidationError as e:
            return {
                'status': 'error',
                'message': str(e),
            }
        except Exception as e:
            _logger.error('Error updating project: %s', str(e))
            return {
                'status': 'error',
                'message': 'Internal server error',
            }

    @http.route('/api/projects/<int:project_id>/delete', type='json', auth='user', methods=['POST'])
    def delete_project(self, project_id):
        """Delete project"""
        try:
            project = request.env['complete.model.example'].browse(project_id)

            if not project.exists():
                return {
                    'status': 'error',
                    'message': 'Project not found',
                }

            # Check access
            project.check_access_rights('unlink')
            project.check_access_rule('unlink')

            # Delete
            project.unlink()

            return {
                'status': 'success',
                'message': 'Project deleted successfully',
            }

        except UserError as e:
            return {
                'status': 'error',
                'message': str(e),
            }
        except Exception as e:
            _logger.error('Error deleting project: %s', str(e))
            return {
                'status': 'error',
                'message': 'Internal server error',
            }

    # ========================================
    # FILE UPLOAD/DOWNLOAD
    # ========================================

    @http.route('/api/projects/<int:project_id>/upload', type='http', auth='user', methods=['POST'], csrf=False)
    def upload_attachment(self, project_id, **kwargs):
        """Upload file attachment to project"""
        try:
            project = request.env['complete.model.example'].browse(project_id)

            if not project.exists():
                return request.make_json_response({
                    'status': 'error',
                    'message': 'Project not found',
                }, status=404)

            # Get uploaded file
            uploaded_file = request.httprequest.files.get('file')

            if not uploaded_file:
                return request.make_json_response({
                    'status': 'error',
                    'message': 'No file uploaded',
                }, status=400)

            # Create attachment
            attachment = request.env['ir.attachment'].create({
                'name': uploaded_file.filename,
                'datas': base64.b64encode(uploaded_file.read()),
                'res_model': 'complete.model.example',
                'res_id': project.id,
                'mimetype': uploaded_file.content_type,
            })

            return request.make_json_response({
                'status': 'success',
                'message': 'File uploaded successfully',
                'data': {
                    'id': attachment.id,
                    'name': attachment.name,
                    'size': attachment.file_size,
                },
            })

        except Exception as e:
            _logger.error('Error uploading file: %s', str(e))
            return request.make_json_response({
                'status': 'error',
                'message': str(e),
            }, status=500)

    @http.route('/api/projects/<int:project_id>/attachments', type='json', auth='user', methods=['POST'])
    def get_attachments(self, project_id):
        """Get list of project attachments"""
        try:
            attachments = request.env['ir.attachment'].search([
                ('res_model', '=', 'complete.model.example'),
                ('res_id', '=', project_id),
            ])

            data = [{
                'id': att.id,
                'name': att.name,
                'size': att.file_size,
                'mimetype': att.mimetype,
                'create_date': att.create_date.isoformat() if att.create_date else None,
                'download_url': f'/web/content/{att.id}?download=true',
            } for att in attachments]

            return {
                'status': 'success',
                'data': data,
            }

        except Exception as e:
            _logger.error('Error getting attachments: %s', str(e))
            return {
                'status': 'error',
                'message': str(e),
            }

    @http.route('/api/projects/<int:project_id>/export', type='http', auth='user', methods=['GET'])
    def export_project(self, project_id, format='pdf', **kwargs):
        """Export project as PDF or Excel"""
        try:
            project = request.env['complete.model.example'].browse(project_id)

            if not project.exists():
                return request.make_json_response({
                    'status': 'error',
                    'message': 'Project not found',
                }, status=404)

            if format == 'pdf':
                # Generate PDF report
                pdf_content, content_type = request.env['ir.actions.report']._render_qweb_pdf(
                    'module.report_project_template',
                    [project.id]
                )

                return request.make_response(
                    pdf_content,
                    headers=[
                        ('Content-Type', 'application/pdf'),
                        ('Content-Disposition', f'attachment; filename="{project.code}.pdf"'),
                    ]
                )

            elif format == 'excel':
                # Generate Excel (implementation depends on your Excel library)
                # This is a placeholder
                return request.make_json_response({
                    'status': 'error',
                    'message': 'Excel export not implemented',
                }, status=501)

            else:
                return request.make_json_response({
                    'status': 'error',
                    'message': 'Invalid format. Use pdf or excel',
                }, status=400)

        except Exception as e:
            _logger.error('Error exporting project: %s', str(e))
            return request.make_json_response({
                'status': 'error',
                'message': str(e),
            }, status=500)

    # ========================================
    # ACTION ROUTES
    # ========================================

    @http.route('/api/projects/<int:project_id>/action/<string:action>', type='json', auth='user', methods=['POST'])
    def execute_action(self, project_id, action, **kwargs):
        """Execute project action (confirm, cancel, etc.)"""
        try:
            project = request.env['complete.model.example'].browse(project_id)

            if not project.exists():
                return {
                    'status': 'error',
                    'message': 'Project not found',
                }

            # Map action to method
            action_methods = {
                'approve': 'action_approve',
                'start': 'action_start',
                'hold': 'action_hold',
                'resume': 'action_resume',
                'done': 'action_done',
                'cancel': 'action_cancel',
            }

            method_name = action_methods.get(action)

            if not method_name or not hasattr(project, method_name):
                return {
                    'status': 'error',
                    'message': f'Invalid action: {action}',
                }

            # Execute action
            method = getattr(project, method_name)
            result = method()

            return {
                'status': 'success',
                'message': f'Action {action} executed successfully',
                'data': result if isinstance(result, dict) else {},
            }

        except UserError as e:
            return {
                'status': 'error',
                'message': str(e),
            }
        except AccessError:
            return {
                'status': 'error',
                'message': 'Access denied',
            }
        except Exception as e:
            _logger.error('Error executing action %s: %s', action, str(e))
            return {
                'status': 'error',
                'message': 'Internal server error',
            }

    # ========================================
    # WEBHOOK/CALLBACK ROUTES
    # ========================================

    @http.route('/webhook/project/status', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def webhook_project_status(self, **kwargs):
        """
        Webhook endpoint for external systems

        Receives project status updates from external systems
        """
        try:
            # Validate webhook token
            token = request.httprequest.headers.get('X-Webhook-Token')
            expected_token = request.env['ir.config_parameter'].sudo().get_param('webhook.token')

            if not token or token != expected_token:
                return {
                    'status': 'error',
                    'message': 'Invalid token',
                }

            # Get data
            data = json.loads(request.httprequest.data)

            project_code = data.get('project_code')
            status = data.get('status')

            # Find project
            project = request.env['complete.model.example'].sudo().search([
                ('code', '=', project_code),
            ], limit=1)

            if not project:
                return {
                    'status': 'error',
                    'message': f'Project not found: {project_code}',
                }

            # Update status
            project.write({'state': status})

            # Log webhook
            _logger.info('Webhook received for project %s: %s', project_code, status)

            return {
                'status': 'success',
                'message': 'Status updated',
            }

        except Exception as e:
            _logger.error('Webhook error: %s', str(e))
            return {
                'status': 'error',
                'message': str(e),
            }


class ProjectPortalController(http.Controller):
    """
    Portal Controller for Customer Access

    Allows customers to view their projects via portal
    """

    @http.route('/my/projects', type='http', auth='user', website=True)
    def portal_my_projects(self, **kwargs):
        """Customer portal - project list"""
        try:
            # Get current user's partner
            partner = request.env.user.partner_id

            # Search customer's projects
            projects = request.env['complete.model.example'].search([
                ('partner_id', '=', partner.id),
            ])

            return request.render('module.portal_my_projects', {
                'projects': projects,
                'page_name': 'project',
            })

        except Exception as e:
            _logger.error('Portal error: %s', str(e))
            return request.render('website.404')

    @http.route('/my/projects/<int:project_id>', type='http', auth='user', website=True)
    def portal_project_detail(self, project_id, **kwargs):
        """Customer portal - project details"""
        try:
            project = request.env['complete.model.example'].browse(project_id)

            # Check access
            if not project.exists() or project.partner_id != request.env.user.partner_id:
                return request.render('website.403')

            return request.render('module.portal_project_detail', {
                'project': project,
                'page_name': 'project',
            })

        except Exception as e:
            _logger.error('Portal error: %s', str(e))
            return request.render('website.404')

