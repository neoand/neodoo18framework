# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestTemplateModel(TransactionCase):

    def setUp(self):
        super(TestTemplateModel, self).setUp()
        self.template_model = self.env['template.model'].create({
            'name': 'Test Record',
            'description': 'This is a test record',
            'date': fields.Date.today(),
        })

    def test_template_model_create(self):
        """Test template model creation"""
        self.assertTrue(self.template_model.reference, "Reference should be generated")
        self.assertEqual(self.template_model.state, 'draft', "Initial state should be draft")
        self.assertTrue(self.template_model.active, "Record should be active by default")

    def test_template_model_workflow(self):
        """Test template model workflow"""
        # Confirm the record
        self.template_model.action_confirm()
        self.assertEqual(self.template_model.state, 'confirmed', "State should be confirmed")
        
        # Mark as done
        self.template_model.action_done()
        self.assertEqual(self.template_model.state, 'done', "State should be done")
        
        # Reset to draft
        self.template_model.action_draft()
        self.assertEqual(self.template_model.state, 'draft', "State should be draft")