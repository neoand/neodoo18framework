# -*- coding: utf-8 -*-
"""
Model Tests for Odoo 18

This file demonstrates comprehensive testing patterns for Odoo models including:
- CRUD operations
- Computed fields
- Constraints and validations
- Business logic
- Access rights
- Performance considerations
"""

from odoo import Command
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase, Form
from odoo.tools import mute_logger, float_compare

from datetime import datetime, timedelta
from freezegun import freeze_time
import logging

_logger = logging.getLogger(__name__)


# ===========================================
# BASIC MODEL TESTS
# ===========================================

@tagged('post_install', '-at_install', 'model')
class TestProjectModel(TransactionCase):
    """
    Test Project Model

    Tests basic CRUD operations and model behavior.
    Uses TransactionCase which provides transaction rollback after each test.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test data (runs once per test class)

        Use setUpClass for data that can be shared across tests.
        All changes will be rolled back after each test method.
        """
        super().setUpClass()

        # Create test users
        cls.user_manager = cls.env['res.users'].create({
            'name': 'Test Manager',
            'login': 'test_manager',
            'email': 'manager@test.com',
            'groups_id': [(6, 0, [cls.env.ref('base.group_user').id])],
        })

        cls.user_member = cls.env['res.users'].create({
            'name': 'Test Member',
            'login': 'test_member',
            'email': 'member@test.com',
            'groups_id': [(6, 0, [cls.env.ref('base.group_user').id])],
        })

        # Create test partner
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'customer@test.com',
            'customer_rank': 1,
        })

        # Create test company
        cls.company = cls.env.company

        # Create test project
        cls.project = cls.env['project.project'].create({
            'name': 'Test Project',
            'code': 'TEST-001',
            'partner_id': cls.partner.id,
            'user_id': cls.user_manager.id,
            'company_id': cls.company.id,
            'date_start': datetime.today(),
            'expected_duration_days': 30,
        })

    def setUp(self):
        """Set up before each test method"""
        super().setUp()
        # Reset project state for each test
        self.project.write({'state': 'draft'})

    # ========================================
    # CREATE TESTS
    # ========================================

    def test_create_project_minimal(self):
        """Test creating project with minimal required fields"""
        project = self.env['project.project'].create({
            'name': 'Minimal Project',
            'partner_id': self.partner.id,
        })

        self.assertTrue(project.id)
        self.assertEqual(project.state, 'draft')
        self.assertEqual(project.user_id, self.env.user)
        self.assertEqual(project.company_id, self.env.company)
        self.assertTrue(project.code)  # Auto-generated

    def test_create_project_complete(self):
        """Test creating project with all fields"""
        project = self.env['project.project'].create({
            'name': 'Complete Project',
            'code': 'COMP-001',
            'partner_id': self.partner.id,
            'user_id': self.user_manager.id,
            'company_id': self.company.id,
            'project_type': 'customer',
            'priority': '2',
            'is_billable': True,
            'budget': 10000.0,
            'date_start': datetime.today(),
            'expected_duration_days': 60,
            'description': 'Test description',
        })

        self.assertEqual(project.name, 'Complete Project')
        self.assertEqual(project.code, 'COMP-001')
        self.assertEqual(project.partner_id, self.partner)
        self.assertEqual(project.budget, 10000.0)
        self.assertTrue(project.is_billable)

    def test_create_multi(self):
        """Test batch creation (@api.model_create_multi)"""
        vals_list = [
            {'name': f'Project {i}', 'partner_id': self.partner.id}
            for i in range(10)
        ]
        projects = self.env['project.project'].create(vals_list)

        self.assertEqual(len(projects), 10)
        self.assertTrue(all(p.code for p in projects))  # All have codes

    # ========================================
    # READ TESTS
    # ========================================

    def test_read_project(self):
        """Test reading project fields"""
        values = self.project.read(['name', 'code', 'state'])[0]

        self.assertEqual(values['name'], 'Test Project')
        self.assertEqual(values['code'], 'TEST-001')
        self.assertEqual(values['state'], 'draft')

    def test_search_project(self):
        """Test searching projects"""
        projects = self.env['project.project'].search([
            ('partner_id', '=', self.partner.id)
        ])

        self.assertIn(self.project, projects)

    def test_name_search(self):
        """Test name_search override"""
        # Search by name
        projects = self.env['project.project'].name_search('Test')
        self.assertTrue(any(p[0] == self.project.id for p in projects))

        # Search by code
        projects = self.env['project.project'].name_search('TEST-001')
        self.assertTrue(any(p[0] == self.project.id for p in projects))

    # ========================================
    # UPDATE TESTS
    # ========================================

    def test_write_project(self):
        """Test updating project"""
        self.project.write({
            'name': 'Updated Project',
            'priority': '3',
        })

        self.assertEqual(self.project.name, 'Updated Project')
        self.assertEqual(self.project.priority, '3')
        self.assertTrue(self.project.last_update_date)

    def test_write_multi(self):
        """Test batch update"""
        projects = self.env['project.project'].create([
            {'name': f'Project {i}', 'partner_id': self.partner.id}
            for i in range(3)
        ])

        projects.write({'priority': '2'})

        self.assertTrue(all(p.priority == '2' for p in projects))

    # ========================================
    # DELETE TESTS
    # ========================================

    def test_unlink_draft_project(self):
        """Test deleting draft project (should succeed)"""
        project = self.env['project.project'].create({
            'name': 'To Delete',
            'partner_id': self.partner.id,
        })
        project_id = project.id

        project.unlink()

        self.assertFalse(self.env['project.project'].browse(project_id).exists())

    def test_unlink_in_progress_project(self):
        """Test deleting in-progress project (should fail)"""
        self.project.write({'state': 'in_progress'})

        with self.assertRaises(UserError):
            self.project.unlink()

    def test_soft_delete(self):
        """Test archiving instead of deleting"""
        project_id = self.project.id

        self.project.with_context(soft_delete=True).unlink()

        project = self.env['project.project'].browse(project_id)
        self.assertTrue(project.exists())
        self.assertFalse(project.active)

    # ========================================
    # COMPUTED FIELD TESTS
    # ========================================

    def test_compute_display_name(self):
        """Test display_name computed field"""
        self.assertEqual(
            self.project.display_name,
            '[TEST-001] Test Project'
        )

    def test_compute_progress(self):
        """Test progress computation based on tasks"""
        # Create tasks with different progress
        self.env['project.task'].create([
            {'name': 'Task 1', 'project_id': self.project.id, 'progress': 100},
            {'name': 'Task 2', 'project_id': self.project.id, 'progress': 50},
            {'name': 'Task 3', 'project_id': self.project.id, 'progress': 0},
        ])

        # Progress should be average: (100 + 50 + 0) / 3 = 50
        self.assertEqual(self.project.progress, 50.0)

    def test_compute_days_remaining(self):
        """Test days_remaining computation"""
        # Set deadline to 10 days from today
        self.project.write({
            'date_deadline': datetime.today() + timedelta(days=10)
        })

        self.assertEqual(self.project.days_remaining, 10)

    def test_compute_is_overdue(self):
        """Test is_overdue computed field"""
        # Not overdue
        self.project.write({
            'date_deadline': datetime.today() + timedelta(days=10)
        })
        self.assertFalse(self.project.is_overdue)

        # Overdue
        self.project.write({
            'date_deadline': datetime.today() - timedelta(days=1),
            'state': 'in_progress',
        })
        self.assertTrue(self.project.is_overdue)

        # Done projects are not overdue
        self.project.write({'state': 'done'})
        self.assertFalse(self.project.is_overdue)

    # ========================================
    # CONSTRAINT TESTS
    # ========================================

    def test_sql_constraint_code_unique(self):
        """Test code uniqueness constraint"""
        with self.assertRaises(Exception):  # psycopg2.IntegrityError wrapped
            self.env['project.project'].create({
                'name': 'Duplicate Code',
                'code': 'TEST-001',  # Same as existing project
                'partner_id': self.partner.id,
            })

    def test_sql_constraint_budget_positive(self):
        """Test budget must be positive"""
        with self.assertRaises(Exception):
            self.env['project.project'].create({
                'name': 'Negative Budget',
                'partner_id': self.partner.id,
                'budget': -1000.0,
            })

    def test_python_constraint_dates(self):
        """Test date validation constraint"""
        with self.assertRaises(ValidationError):
            self.project.write({
                'date_start': datetime.today(),
                'date_end': datetime.today() - timedelta(days=1),  # Before start
            })

    def test_python_constraint_budget(self):
        """Test budget exceeded constraint"""
        self.project.write({'budget': 1000.0})

        # Create tasks that exceed budget
        with self.assertRaises(ValidationError):
            self.env['project.task'].create({
                'name': 'Expensive Task',
                'project_id': self.project.id,
                'amount': 2000.0,  # Exceeds budget
            })

    # ========================================
    # ONCHANGE TESTS
    # ========================================

    def test_onchange_partner(self):
        """Test onchange_partner_id"""
        # Use Form to trigger onchange
        with Form(self.env['project.project']) as project_form:
            project_form.name = 'Onchange Test'
            project_form.partner_id = self.partner

            # Check if user_id was set from partner
            if self.partner.user_id:
                self.assertEqual(project_form.user_id, self.partner.user_id)

    def test_onchange_date_start(self):
        """Test onchange_date_start calculates end date"""
        with Form(self.env['project.project']) as project_form:
            project_form.name = 'Date Test'
            project_form.partner_id = self.partner
            project_form.date_start = datetime.today()
            project_form.expected_duration_days = 30

            # date_end should be calculated
            expected_end = datetime.today() + timedelta(days=30)
            self.assertEqual(
                project_form.date_end.date() if project_form.date_end else None,
                expected_end.date()
            )

    # ========================================
    # BUSINESS LOGIC TESTS
    # ========================================

    def test_action_plan(self):
        """Test planning action"""
        # Create task first
        self.env['project.task'].create({
            'name': 'Test Task',
            'project_id': self.project.id,
        })

        self.project.action_plan()

        self.assertEqual(self.project.state, 'planning')

    def test_action_plan_without_tasks(self):
        """Test planning without tasks should fail"""
        with self.assertRaises(UserError):
            self.project.action_plan()

    def test_action_approve(self):
        """Test approval action"""
        # Setup: add required fields
        self.project.write({
            'date_start': datetime.today(),
            'date_deadline': datetime.today() + timedelta(days=30),
            'budget': 1000.0,
        })

        # Add task
        self.env['project.task'].create({
            'name': 'Task',
            'project_id': self.project.id,
        })

        # Move to planning first
        self.project.write({'state': 'planning'})

        # Approve (as system user)
        self.project.with_user(self.env.ref('base.user_admin')).action_approve()

        self.assertEqual(self.project.state, 'approved')
        self.assertTrue(self.project.date_approved)

    def test_state_transitions(self):
        """Test complete state transition flow"""
        # Setup
        self.project.write({
            'date_start': datetime.today(),
            'date_deadline': datetime.today() + timedelta(days=30),
            'budget': 1000.0,
        })
        self.env['project.task'].create({
            'name': 'Task',
            'project_id': self.project.id,
        })

        # Draft → Planning
        self.project.action_plan()
        self.assertEqual(self.project.state, 'planning')

        # Planning → Approved
        self.project.with_user(self.env.ref('base.user_admin')).action_approve()
        self.assertEqual(self.project.state, 'approved')

        # Approved → In Progress
        self.project.action_start()
        self.assertEqual(self.project.state, 'in_progress')

        # In Progress → Done
        self.project.task_ids.write({'state': 'done'})
        self.project.action_done()
        self.assertEqual(self.project.state, 'done')

    # ========================================
    # COPY TESTS
    # ========================================

    def test_copy_project(self):
        """Test project duplication"""
        copy = self.project.copy()

        self.assertNotEqual(copy.id, self.project.id)
        self.assertNotEqual(copy.code, self.project.code)
        self.assertEqual(copy.name, 'Test Project (Copy)')
        self.assertEqual(copy.state, 'draft')
        self.assertFalse(copy.date_approved)

    # ========================================
    # TRACKING TESTS (Chatter)
    # ========================================

    def test_tracking_changes(self):
        """Test that field changes are tracked"""
        initial_message_count = len(self.project.message_ids)

        # Change tracked field
        self.project.write({'name': 'Updated Name'})

        # Should create a message
        self.assertGreater(len(self.project.message_ids), initial_message_count)

    # ========================================
    # SEARCH METHOD TESTS
    # ========================================

    def test_search_is_overdue(self):
        """Test custom search method for is_overdue"""
        # Create overdue project
        overdue_project = self.env['project.project'].create({
            'name': 'Overdue Project',
            'partner_id': self.partner.id,
            'date_deadline': datetime.today() - timedelta(days=1),
            'state': 'in_progress',
        })

        # Search for overdue projects
        overdue = self.env['project.project'].search([
            ('is_overdue', '=', True)
        ])

        self.assertIn(overdue_project, overdue)
        self.assertNotIn(self.project, overdue)  # Not overdue


# ===========================================
# PERFORMANCE TESTS
# ===========================================

@tagged('post_install', '-at_install', 'performance')
class TestProjectPerformance(TransactionCase):
    """Test model performance and query optimization"""

    def test_batch_create_performance(self):
        """Test that batch create is efficient"""
        import time

        # Create many records at once
        vals_list = [
            {
                'name': f'Project {i}',
                'partner_id': self.env['res.partner'].create({'name': f'Partner {i}'}).id,
            }
            for i in range(100)
        ]

        start = time.time()
        projects = self.env['project.project'].create(vals_list)
        duration = time.time() - start

        self.assertEqual(len(projects), 100)
        self.assertLess(duration, 5.0, "Batch create took too long")

    @mute_logger('odoo.sql_db')
    def test_query_count(self):
        """Test number of queries is reasonable"""
        # Create test data
        project = self.env['project.project'].create({
            'name': 'Query Test',
            'partner_id': self.env['res.partner'].create({'name': 'Partner'}).id,
        })

        # Reset query counter
        self.cr.execute("SELECT 1")  # Dummy query

        # Access fields (should not cause N+1 queries)
        projects = self.env['project.project'].search([])
        names = [p.name for p in projects]
        partners = [p.partner_id.name for p in projects]

        # Check queries are reasonable (this is a simple heuristic)
        # In real tests, use profiling tools


# ===========================================
# SECURITY TESTS
# ===========================================

@tagged('post_install', '-at_install', 'security')
class TestProjectSecurity(TransactionCase):
    """Test access rights and record rules"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_portal = cls.env['res.users'].create({
            'name': 'Portal User',
            'login': 'portal',
            'groups_id': [(6, 0, [cls.env.ref('base.group_portal').id])],
        })

        cls.project = cls.env['project.project'].create({
            'name': 'Security Test',
            'partner_id': cls.env['res.partner'].create({'name': 'Partner'}).id,
        })

    def test_access_rights_read(self):
        """Test read access for different user groups"""
        # Internal user should be able to read
        project = self.project.with_user(self.env.ref('base.user_admin'))
        self.assertTrue(project.check_access_rights('read', raise_exception=False))

        # Portal user might not (depends on access rights config)
        project = self.project.with_user(self.user_portal)
        # self.assertFalse(project.check_access_rights('read', raise_exception=False))

    def test_access_rights_write(self):
        """Test write access"""
        # Normal user can write
        self.assertTrue(
            self.project.check_access_rights('write', raise_exception=False)
        )

    def test_record_rules(self):
        """Test record rules restrict access"""
        # This depends on your record rules configuration
        pass
