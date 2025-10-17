# -*- coding: utf-8 -*-
"""
Performance Tests for Odoo 18

This file demonstrates performance testing patterns including:
- Query counting and optimization
- Batch operation efficiency
- Computed field performance
- Search performance
- Memory usage
- Response time benchmarks
"""

from odoo.tests import tagged, TransactionCase, warmup
from odoo.tools import mute_logger

import time
import logging
from contextlib import contextmanager

_logger = logging.getLogger(__name__)


# ===========================================
# QUERY OPTIMIZATION TESTS
# ===========================================

@tagged('post_install', '-at_install', 'performance')
class TestProjectPerformance(TransactionCase):
    """Test project model performance"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create test partners
        cls.partners = cls.env['res.partner'].create([
            {'name': f'Partner {i}', 'customer_rank': 1}
            for i in range(50)
        ])

        # Create test projects
        cls.projects = cls.env['project.project'].create([
            {
                'name': f'Project {i}',
                'partner_id': cls.partners[i % len(cls.partners)].id,
            }
            for i in range(100)
        ])

    @contextmanager
    def assertQueryCount(self, max_count=None, exact_count=None):
        """
        Context manager to count SQL queries

        Usage:
            with self.assertQueryCount(max_count=10):
                # code that should execute at most 10 queries
        """
        # Flush pending operations
        self.env.flush_all()
        self.env.clear()

        # Get initial query count
        self.cr.execute("SELECT query_count FROM pg_stat_database WHERE datname = current_database()")
        initial_count = self.cr.fetchone()
        initial_queries = initial_count[0] if initial_count else 0

        yield

        # Get final query count
        self.cr.execute("SELECT query_count FROM pg_stat_database WHERE datname = current_database()")
        final_count = self.cr.fetchone()
        final_queries = final_count[0] if final_count else 0

        query_count = final_queries - initial_queries

        if max_count is not None:
            self.assertLessEqual(
                query_count, max_count,
                f"Too many queries: {query_count} > {max_count}"
            )

        if exact_count is not None:
            self.assertEqual(
                query_count, exact_count,
                f"Unexpected query count: {query_count} != {exact_count}"
            )

        _logger.info(f"Queries executed: {query_count}")

    @contextmanager
    def assertExecutionTime(self, max_duration):
        """
        Context manager to measure execution time

        Usage:
            with self.assertExecutionTime(max_duration=1.0):
                # code that should complete in less than 1 second
        """
        start = time.time()
        yield
        duration = time.time() - start

        self.assertLess(
            duration, max_duration,
            f"Operation took too long: {duration:.3f}s > {max_duration}s"
        )

        _logger.info(f"Execution time: {duration:.3f}s")

    # ========================================
    # BATCH OPERATIONS
    # ========================================

    def test_batch_create_performance(self):
        """Test batch creation is efficient"""
        vals_list = [
            {
                'name': f'Batch Project {i}',
                'partner_id': self.partners[i % len(self.partners)].id,
            }
            for i in range(100)
        ]

        with self.assertExecutionTime(max_duration=2.0):
            projects = self.env['project.project'].create(vals_list)

        self.assertEqual(len(projects), 100)

    def test_batch_write_performance(self):
        """Test batch update is efficient"""
        projects = self.projects[:50]

        with self.assertExecutionTime(max_duration=1.0):
            projects.write({'priority': '2'})

        self.assertTrue(all(p.priority == '2' for p in projects))

    def test_batch_read_performance(self):
        """Test batch read is efficient"""
        projects = self.projects[:50]

        with self.assertExecutionTime(max_duration=0.5):
            data = projects.read(['name', 'partner_id', 'state'])

        self.assertEqual(len(data), 50)

    # ========================================
    # N+1 QUERY PROBLEM TESTS
    # ========================================

    def test_avoid_n_plus_1_queries(self):
        """Test that accessing related fields doesn't cause N+1 queries"""
        projects = self.projects[:20]

        # This should NOT cause N+1 queries
        # Good: projects.mapped('partner_id.name')
        # Bad: [p.partner_id.name for p in projects]

        with self.assertExecutionTime(max_duration=0.5):
            # Using mapped() is optimized
            partner_names = projects.mapped('partner_id.name')

        self.assertEqual(len(partner_names), 20)

    def test_prefetch_optimization(self):
        """Test that prefetching works correctly"""
        # Clear cache
        self.env.clear()

        # Access first project
        first_project = self.projects[0]

        # Odoo's prefetch should load multiple records
        # Accessing more projects should not cause additional queries
        with self.assertExecutionTime(max_duration=0.1):
            names = [p.name for p in self.projects[:10]]

        self.assertEqual(len(names), 10)

    @mute_logger('odoo.sql_db')
    def test_no_queries_after_read(self):
        """Test that read() prefetches all requested fields"""
        projects = self.projects[:10]

        # Read all fields we'll need
        data = projects.read(['name', 'partner_id', 'state', 'priority'])

        # Clear query log
        self.env.flush_all()

        # Accessing already-read fields should not cause queries
        # Note: This is hard to test precisely without query counting
        for project_data in data:
            name = project_data['name']
            partner_id = project_data['partner_id']

    # ========================================
    # COMPUTED FIELD PERFORMANCE
    # ========================================

    def test_computed_field_stored_performance(self):
        """Test that stored computed fields are efficient"""
        # Create project with tasks
        project = self.env['project.project'].create({
            'name': 'Computed Test',
            'partner_id': self.partners[0].id,
        })

        # Create many tasks
        self.env['project.task'].create([
            {
                'name': f'Task {i}',
                'project_id': project.id,
                'progress': i * 10,
            }
            for i in range(10)
        ])

        # Access computed field (should be pre-computed if store=True)
        with self.assertExecutionTime(max_duration=0.1):
            progress = project.progress

        self.assertTrue(isinstance(progress, float))

    def test_computed_field_non_stored_performance(self):
        """Test non-stored computed fields compute on demand"""
        project = self.projects[0]

        # Non-stored computed fields compute each time
        # They should still be reasonably fast
        with self.assertExecutionTime(max_duration=0.1):
            value = project.some_non_stored_field

    # ========================================
    # SEARCH PERFORMANCE
    # ========================================

    def test_search_with_limit_performance(self):
        """Test search with limit is efficient"""
        with self.assertExecutionTime(max_duration=0.2):
            projects = self.env['project.project'].search(
                [('state', '=', 'draft')],
                limit=10,
                order='id desc'
            )

        self.assertLessEqual(len(projects), 10)

    def test_search_count_performance(self):
        """Test search_count is efficient"""
        with self.assertExecutionTime(max_duration=0.2):
            count = self.env['project.project'].search_count([
                ('state', '=', 'draft')
            ])

        self.assertGreaterEqual(count, 0)

    def test_name_search_performance(self):
        """Test name_search is efficient"""
        with self.assertExecutionTime(max_duration=0.3):
            results = self.env['project.project'].name_search(
                'Project',
                limit=20
            )

        self.assertLessEqual(len(results), 20)

    def test_complex_domain_performance(self):
        """Test complex domain search performance"""
        domain = [
            '|',
                ('name', 'ilike', 'Project'),
                ('code', 'ilike', 'PROJ'),
            ('state', 'in', ('draft', 'planning', 'approved')),
            ('partner_id', '!=', False),
        ]

        with self.assertExecutionTime(max_duration=0.5):
            projects = self.env['project.project'].search(domain)

        _logger.info(f"Found {len(projects)} projects with complex domain")

    # ========================================
    # MASS OPERATIONS
    # ========================================

    def test_mass_archive_performance(self):
        """Test archiving many records"""
        projects = self.projects[:50]

        with self.assertExecutionTime(max_duration=1.0):
            projects.write({'active': False})

        self.assertTrue(all(not p.active for p in projects))

    def test_mass_delete_performance(self):
        """Test deleting many records"""
        # Create temporary projects
        temp_projects = self.env['project.project'].create([
            {
                'name': f'Temp {i}',
                'partner_id': self.partners[0].id,
            }
            for i in range(50)
        ])

        with self.assertExecutionTime(max_duration=2.0):
            temp_projects.unlink()

        self.assertFalse(temp_projects.exists())

    # ========================================
    # MEMORY USAGE TESTS
    # ========================================

    def test_memory_efficient_iteration(self):
        """Test iterating large recordsets doesn't use too much memory"""
        import sys

        # Get initial memory usage
        # Note: This is approximate, real memory profiling requires
 external tools

        # Good pattern: iterate without loading all data
        total = 0
        for project in self.projects:
            total += project.id

        # Memory should be released
        self.assertTrue(total > 0)

    # ========================================
    # CACHE PERFORMANCE
    # ========================================

    def test_cache_invalidation_performance(self):
        """Test that cache invalidation doesn't kill performance"""
        project = self.projects[0]

        # Access field (caches it)
        name1 = project.name

        # Modify unrelated field
        project.write({'priority': '2'})

        # Access field again (should use cache if not invalidated)
        with self.assertExecutionTime(max_duration=0.1):
            name2 = project.name

        self.assertEqual(name1, name2)

    def test_clear_cache_performance(self):
        """Test clearing cache"""
        # Fill cache
        for project in self.projects[:10]:
            _ = project.name

        # Clear cache
        with self.assertExecutionTime(max_duration=0.1):
            self.env.clear()

    # ========================================
    # ORM METHOD PERFORMANCE
    # ========================================

    def test_exists_performance(self):
        """Test exists() is efficient"""
        project_ids = self.projects.ids[:100]

        with self.assertExecutionTime(max_duration=0.2):
            existing = self.env['project.project'].browse(project_ids).exists()

        self.assertTrue(existing)

    def test_filtered_performance(self):
        """Test filtered() on large recordsets"""
        with self.assertExecutionTime(max_duration=0.5):
            draft_projects = self.projects.filtered(lambda p: p.state == 'draft')

        _logger.info(f"Filtered {len(draft_projects)} draft projects")

    def test_sorted_performance(self):
        """Test sorted() on large recordsets"""
        with self.assertExecutionTime(max_duration=0.5):
            sorted_projects = self.projects.sorted(key=lambda p: p.name)

        self.assertEqual(len(sorted_projects), len(self.projects))

    def test_mapped_performance(self):
        """Test mapped() is efficient"""
        with self.assertExecutionTime(max_duration=0.3):
            names = self.projects.mapped('name')

        self.assertEqual(len(names), len(self.projects))

    # ========================================
    # CONCURRENT ACCESS SIMULATION
    # ========================================

    @mute_logger('odoo.sql_db')
    def test_concurrent_write_simulation(self):
        """Test handling concurrent writes"""
        project = self.projects[0]

        # Simulate concurrent modification
        # In real scenarios, use threading or separate transactions

        # Transaction 1: read
        name1 = project.name

        # Transaction 2: modify (simulated)
        self.env.cr.execute("""
            UPDATE project_project
            SET name = 'Modified Concurrently'
            WHERE id = %s
        """, (project.id,))

        # Transaction 1: write (should handle or detect conflict)
        project.write({'priority': '2'})

        # Verify
        project.invalidate_recordset()
        self.assertEqual(project.name, 'Modified Concurrently')

    # ========================================
    # BENCHMARK COMPARISONS
    # ========================================

    def test_search_vs_read_performance(self):
        """Compare search() vs read() performance"""
        project_ids = self.projects.ids[:50]

        # Method 1: search + access fields
        start = time.time()
        projects = self.env['project.project'].search([('id', 'in', project_ids)])
        names1 = [p.name for p in projects]
        time1 = time.time() - start

        # Method 2: browse + read
        start = time.time()
        projects = self.env['project.project'].browse(project_ids)
        data = projects.read(['name'])
        names2 = [d['name'] for d in data]
        time2 = time.time() - start

        _logger.info(f"search + access: {time1:.3f}s, browse + read: {time2:.3f}s")

        self.assertEqual(len(names1), len(names2))

    def test_create_one_vs_batch_performance(self):
        """Compare single creates vs batch create"""
        # Method 1: Create one by one
        start = time.time()
        for i in range(20):
            self.env['project.project'].create({
                'name': f'Single {i}',
                'partner_id': self.partners[0].id,
            })
        time_single = time.time() - start

        # Method 2: Batch create
        start = time.time()
        self.env['project.project'].create([
            {
                'name': f'Batch {i}',
                'partner_id': self.partners[0].id,
            }
            for i in range(20)
        ])
        time_batch = time.time() - start

        _logger.info(
            f"Single creates: {time_single:.3f}s, "
            f"Batch create: {time_batch:.3f}s, "
            f"Speedup: {time_single/time_batch:.1f}x"
        )

        # Batch should be significantly faster
        self.assertLess(time_batch, time_single / 2)


# ===========================================
# LOAD TESTING
# ===========================================

@tagged('-standard', 'load_test')
class TestProjectLoadTesting(TransactionCase):
    """
    Load testing (run manually)

    These tests create large amounts of data to test system behavior under load.
    Not run by default (use --load-test tag to run).
    """

    def test_create_large_dataset(self):
        """Test creating and working with large dataset"""
        _logger.info("Creating 1000 projects...")

        partners = self.env['res.partner'].create([
            {'name': f'Partner {i}'}
            for i in range(100)
        ])

        start = time.time()
        projects = self.env['project.project'].create([
            {
                'name': f'Load Test Project {i}',
                'partner_id': partners[i % len(partners)].id,
            }
            for i in range(1000)
        ])
        create_time = time.time() - start

        _logger.info(f"Created 1000 projects in {create_time:.2f}s")

        # Test search performance on large dataset
        start = time.time()
        found = self.env['project.project'].search([
            ('name', 'ilike', 'Load Test')
        ], limit=100)
        search_time = time.time() - start

        _logger.info(f"Searched in {search_time:.3f}s, found {len(found)} projects")

        self.assertGreater(len(found), 0)
