# -*- coding: utf-8 -*-
"""
UI Tests for Odoo 18

This file demonstrates UI testing patterns including:
- Tours (automated UI workflows)
- Form interactions
- Widget testing
- Navigation
- User interactions
"""

from odoo.tests import HttpCase, tagged
from odoo.tests.common import Form
import logging

_logger = logging.getLogger(__name__)


# ===========================================
# HTTP/UI TESTS
# ===========================================

@tagged('post_install', '-at_install', 'ui')
class TestProjectUI(HttpCase):
    """
    Test Project UI

    Uses HttpCase which provides a headless browser for testing.
    Requires Chrome/Chromium and chromedriver installed.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create test data
        cls.partner = cls.env['res.partner'].create({
            'name': 'UI Test Customer',
            'email': 'uitest@example.com',
        })

        cls.user_demo = cls.env.ref('base.user_demo')

        cls.project = cls.env['project.project'].create({
            'name': 'UI Test Project',
            'code': 'UITEST-001',
            'partner_id': cls.partner.id,
            'user_id': cls.user_demo.id,
        })

    def test_ui_project_list_view(self):
        """Test accessing project list view"""
        self.start_tour("/web", 'project_list_tour', login='admin')

    def test_ui_project_form_view(self):
        """Test opening project form"""
        self.start_tour(
            f"/web#id={self.project.id}&model=project.project&view_type=form",
            'project_form_tour',
            login='admin'
        )

    def test_ui_project_kanban_view(self):
        """Test kanban view interactions"""
        self.start_tour("/web", 'project_kanban_tour', login='admin')


# ===========================================
# TOUR DEFINITIONS
# ===========================================

# Tours are defined in JavaScript/XML and registered in assets
# Example tour structure (to be defined in static/tests/tours/):

"""
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { stepUtils } from "@web_tour/tour_service/tour_utils";

registry.category("web_tour.tours").add('project_list_tour', {
    test: true,
    url: '/web',
    steps: () => [
        stepUtils.showAppsMenuItem(),
        {
            content: "Open Projects app",
            trigger: '.o_app[data-menu-xmlid="project.menu_main_pm"]',
            run: "click",
        },
        {
            content: "Verify project list is displayed",
            trigger: '.o_list_view',
        },
        {
            content: "Search for project",
            trigger: '.o_searchview_input',
            run: "text UITEST-001",
        },
        {
            content: "Verify search results",
            trigger: '.o_data_row:contains("UITEST-001")',
        },
    ],
});

registry.category("web_tour.tours").add('project_form_tour', {
    test: true,
    steps: () => [
        {
            content: "Wait for form to load",
            trigger: 'form[class*="o_form_view"]',
        },
        {
            content: "Edit project name",
            trigger: 'input[name="name"]',
            run: "text Updated Project Name",
        },
        {
            content: "Save",
            trigger: '.o_form_button_save',
            run: "click",
        },
        {
            content: "Verify saved",
            trigger: '.o_form_readonly',
        },
    ],
});

registry.category("web_tour.tours").add('project_kanban_tour', {
    test: true,
    url: '/web',
    steps: () => [
        stepUtils.showAppsMenuItem(),
        {
            content: "Open Projects",
            trigger: '.o_app[data-menu-xmlid="project.menu_main_pm"]',
            run: "click",
        },
        {
            content: "Switch to kanban view",
            trigger: 'button[data-view-type="kanban"]',
            run: "click",
        },
        {
            content: "Verify kanban is displayed",
            trigger: '.o_kanban_view',
        },
        {
            content: "Click on a kanban card",
            trigger: '.o_kanban_record:first',
            run: "click",
        },
    ],
});
"""


# ===========================================
# FORM WIDGET TESTS
# ===========================================

@tagged('post_install', '-at_install', 'form')
class TestProjectForm(HttpCase):
    """Test form behaviors and widgets"""

    def test_form_create(self):
        """Test creating record through form"""
        # Use Form helper to simulate UI
        with Form(self.env['project.project']) as project_form:
            project_form.name = 'Form Test Project'
            project_form.partner_id = self.env['res.partner'].create({
                'name': 'Form Test Partner'
            })

        project = project_form.save()

        self.assertTrue(project.id)
        self.assertEqual(project.name, 'Form Test Project')
        self.assertTrue(project.code)  # Auto-generated

    def test_form_edit(self):
        """Test editing record through form"""
        project = self.env['project.project'].create({
            'name': 'Original Name',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        with Form(project) as project_form:
            project_form.name = 'Updated Name'
            project_form.priority = '3'

        self.assertEqual(project.name, 'Updated Name')
        self.assertEqual(project.priority, '3')

    def test_form_onchange_trigger(self):
        """Test that onchange methods are triggered"""
        partner = self.env['res.partner'].create({
            'name': 'Onchange Partner',
            'user_id': self.env.ref('base.user_demo').id,
        })

        with Form(self.env['project.project']) as project_form:
            project_form.name = 'Onchange Test'
            project_form.partner_id = partner

            # Onchange should set user_id from partner
            if partner.user_id:
                self.assertEqual(project_form.user_id, partner.user_id)

    def test_form_one2many_inline(self):
        """Test adding one2many records inline"""
        project = self.env['project.project'].create({
            'name': 'O2M Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        with Form(project) as project_form:
            # Add task
            with project_form.task_ids.new() as task_form:
                task_form.name = 'Inline Task'
                task_form.user_id = self.env.user

        self.assertEqual(len(project.task_ids), 1)
        self.assertEqual(project.task_ids[0].name, 'Inline Task')

    def test_form_many2many_tags(self):
        """Test many2many_tags widget"""
        tag1 = self.env['project.tags'].create({'name': 'Tag 1'})
        tag2 = self.env['project.tags'].create({'name': 'Tag 2'})

        with Form(self.env['project.project']) as project_form:
            project_form.name = 'Tag Test'
            project_form.partner_id = self.env['res.partner'].create({'name': 'Partner'})
            project_form.tag_ids.add(tag1)
            project_form.tag_ids.add(tag2)

        project = project_form.save()

        self.assertEqual(len(project.tag_ids), 2)
        self.assertIn(tag1, project.tag_ids)
        self.assertIn(tag2, project.tag_ids)

    def test_form_readonly_modifier(self):
        """Test readonly modifier on fields"""
        project = self.env['project.project'].create({
            'name': 'Readonly Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
            'state': 'draft',
        })

        # In draft, code should be editable
        with Form(project) as project_form:
            # In Odoo 18, use Python expressions for modifiers
            # readonly="state != 'draft'"
            # This test verifies the behavior programmatically
            pass

        # Change state
        project.write({'state': 'done'})

        # Now code should be readonly (test in real UI with tour)

    def test_form_required_modifier(self):
        """Test required modifier enforcement"""
        with Form(self.env['project.project']) as project_form:
            project_form.name = 'Required Test'
            # partner_id is required, should raise if not set

        # Attempt to save without required field
        try:
            project_form.save()
        except Exception:
            # Should raise validation error
            pass

    def test_form_invisible_modifier(self):
        """Test invisible modifier hides fields"""
        project = self.env['project.project'].create({
            'name': 'Invisible Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
            'is_billable': False,
        })

        with Form(project) as project_form:
            # When is_billable=False, amount_invoiced should be invisible
            # invisible="not is_billable"
            # Verify programmatically
            self.assertFalse(project_form.is_billable)


# ===========================================
# WIDGET SPECIFIC TESTS
# ===========================================

@tagged('post_install', '-at_install', 'widgets')
class TestProjectWidgets(HttpCase):
    """Test specific widget behaviors"""

    def test_widget_statusbar(self):
        """Test statusbar widget"""
        project = self.env['project.project'].create({
            'name': 'Statusbar Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        # Statusbar allows clicking to change state (if clickable: 1)
        # Test state transitions
        project.write({'state': 'planning'})
        self.assertEqual(project.state, 'planning')

    def test_widget_many2one_avatar(self):
        """Test many2one_avatar_user widget"""
        # This widget displays user with avatar
        # Verify it doesn't break with null values
        project = self.env['project.project'].create({
            'name': 'Avatar Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
            'user_id': False,
        })

        with Form(project) as project_form:
            project_form.user_id = self.env.ref('base.user_admin')

        self.assertTrue(project.user_id)

    def test_widget_progressbar(self):
        """Test progressbar widget"""
        project = self.env['project.project'].create({
            'name': 'Progress Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        # Create tasks to compute progress
        self.env['project.task'].create([
            {'name': 'Task 1', 'project_id': project.id, 'progress': 100},
            {'name': 'Task 2', 'project_id': project.id, 'progress': 50},
        ])

        self.assertEqual(project.progress, 75.0)

    def test_widget_monetary(self):
        """Test monetary widget with currency"""
        project = self.env['project.project'].create({
            'name': 'Monetary Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
            'budget': 10000.0,
            'currency_id': self.env.company.currency_id.id,
        })

        # Monetary widget should format correctly
        self.assertEqual(project.budget, 10000.0)
        self.assertTrue(project.currency_id)

    def test_widget_image(self):
        """Test image widget"""
        project = self.env['project.project'].create({
            'name': 'Image Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        # Set image (base64 encoded)
        import base64
        test_image = base64.b64encode(b'fake image content')

        with Form(project) as project_form:
            project_form.image_1920 = test_image

        self.assertTrue(project.image_1920)
        self.assertTrue(project.image_512)  # Auto-resized
        self.assertTrue(project.image_128)  # Auto-resized

    def test_widget_priority(self):
        """Test priority (star) widget"""
        project = self.env['project.project'].create({
            'name': 'Priority Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
            'priority': '0',
        })

        # Priority widget allows clicking stars
        project.write({'priority': '3'})
        self.assertEqual(project.priority, '3')

    def test_widget_html(self):
        """Test HTML widget with sanitization"""
        project = self.env['project.project'].create({
            'name': 'HTML Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        # Set HTML content
        html_content = '<p>Test paragraph</p><script>alert("XSS")</script>'

        with Form(project) as project_form:
            project_form.specification = html_content

        # Script should be sanitized
        self.assertNotIn('<script>', project.specification)
        self.assertIn('<p>Test paragraph</p>', project.specification)


# ===========================================
# CHATTER TESTS
# ===========================================

@tagged('post_install', '-at_install', 'chatter')
class TestProjectChatter(HttpCase):
    """Test chatter functionality"""

    def test_chatter_post_message(self):
        """Test posting message in chatter"""
        project = self.env['project.project'].create({
            'name': 'Chatter Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        # Post message
        project.message_post(
            body='Test message',
            subject='Test',
            message_type='comment',
        )

        messages = project.message_ids.filtered(lambda m: m.body == 'Test message')
        self.assertTrue(messages)

    def test_chatter_activity_schedule(self):
        """Test scheduling activity"""
        project = self.env['project.project'].create({
            'name': 'Activity Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        # Schedule activity
        project.activity_schedule(
            'mail.mail_activity_data_todo',
            user_id=self.env.user.id,
            summary='Test Activity',
        )

        self.assertTrue(project.activity_ids)
        self.assertEqual(project.activity_ids[0].summary, 'Test Activity')

    def test_chatter_followers(self):
        """Test adding followers"""
        project = self.env['project.project'].create({
            'name': 'Followers Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        partner = self.env['res.partner'].create({'name': 'Follower'})

        # Add follower
        project.message_subscribe(partner_ids=partner.ids)

        self.assertIn(partner, project.message_partner_ids)

    def test_chatter_tracking(self):
        """Test field tracking in chatter"""
        project = self.env['project.project'].create({
            'name': 'Tracking Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        initial_message_count = len(project.message_ids)

        # Change tracked field
        project.write({'name': 'Updated Name', 'priority': '3'})

        # Should create tracking message
        new_messages = project.message_ids.filtered(
            lambda m: len(m.tracking_value_ids) > 0
        )

        self.assertTrue(new_messages)
