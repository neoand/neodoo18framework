# Data Migration Specialist Role - Odoo 18+ Migration Expert

## Role Overview

The Data Migration Specialist role is responsible for planning, executing, and validating data migrations between different Odoo versions or from external systems to Odoo 18+. This specialist ensures data integrity, handles complex transformations, and creates migration scripts while minimizing business disruptions during the migration process.

## Core Responsibilities

1. **Migration Planning & Analysis**
   - Assess source and target data structures
   - Identify data mapping requirements and transformation rules
   - Create detailed migration plans with timelines and milestones
   - Analyze data quality and cleansing requirements

2. **Migration Development**
   - Develop migration scripts using Python and ORM
   - Create data transformation and mapping logic
   - Build data validation and error handling mechanisms
   - Design and implement pre/post-migration verification tools

3. **Execution & Validation**
   - Execute migration processes in development/staging environments
   - Validate data integrity and completeness after migration
   - Troubleshoot and resolve migration issues
   - Optimize migration performance for large datasets

4. **Documentation & Knowledge Transfer**
   - Create comprehensive migration documentation
   - Develop rollback procedures for migration failures
   - Train team members on data structures and relationships
   - Document post-migration data handling procedures

## Technical Expertise

### Migration Framework Structure

```python
# migration/migration_framework.py
import logging
import time
from contextlib import contextmanager
from datetime import datetime

_logger = logging.getLogger(__name__)

class MigrationTool:
    """Base class for Odoo data migration tools"""
    
    def __init__(self, env, options=None):
        self.env = env
        self.options = options or {}
        self.start_time = None
        self.stats = {
            'records_processed': 0,
            'records_created': 0,
            'records_updated': 0,
            'records_skipped': 0,
            'errors': 0
        }
        
    @contextmanager
    def migration_stats(self, description):
        """Context manager to track migration statistics"""
        self.start_time = time.time()
        _logger.info("Starting migration task: %s", description)
        
        try:
            yield
            elapsed = time.time() - self.start_time
            _logger.info(
                "Completed migration task: %s in %.2f seconds\n"
                "Records processed: %d\n"
                "Records created: %d\n"
                "Records updated: %d\n"
                "Records skipped: %d\n"
                "Errors: %d",
                description, elapsed,
                self.stats['records_processed'],
                self.stats['records_created'],
                self.stats['records_updated'],
                self.stats['records_skipped'],
                self.stats['errors']
            )
        except Exception as e:
            elapsed = time.time() - self.start_time
            _logger.error(
                "Error in migration task: %s after %.2f seconds\n"
                "Error: %s",
                description, elapsed, str(e)
            )
            raise
    
    def log_migration_step(self, model_name, record_id, action, message=None):
        """Log individual migration steps"""
        self.env['migration.log'].create({
            'model': model_name,
            'record_id': record_id,
            'action': action,
            'message': message or f"{action} completed successfully",
            'date': fields.Datetime.now()
        })
    
    def batch_process(self, model_name, domain=None, batch_size=1000, process_func=None):
        """Process records in batches to manage memory usage"""
        domain = domain or []
        offset = 0
        
        while True:
            records = self.env[model_name].search(domain, limit=batch_size, offset=offset)
            if not records:
                break
                
            if process_func:
                for record in records:
                    try:
                        process_func(record)
                        self.stats['records_processed'] += 1
                    except Exception as e:
                        self.stats['errors'] += 1
                        _logger.error(
                            "Error processing %s record ID %s: %s",
                            model_name, record.id, str(e)
                        )
                        self.log_migration_step(model_name, record.id, 'error', str(e))
                        
            offset += batch_size
            self.env.cr.commit()  # Commit each batch
            
        return self.stats
```

### Data Mapping Framework

```python
# migration/data_mapping.py
from odoo import models, fields, api
import json
import logging

_logger = logging.getLogger(__name__)

class DataMapping(models.Model):
    _name = 'migration.data.mapping'
    _description = 'Data Migration Field Mapping'
    
    name = fields.Char(required=True)
    source_model = fields.Char(string='Source Model', required=True)
    target_model = fields.Char(string='Target Model', required=True)
    
    field_mapping = fields.Text(string='Field Mapping', required=True,
                               help='JSON mapping of source fields to target fields')
    mapping_logic = fields.Selection([
        ('simple', 'Simple Mapping'),
        ('transform', 'Transformation Required'),
        ('complex', 'Complex Logic Required')
    ], default='simple', required=True)
    
    transformation_code = fields.Text(
        string='Transformation Code',
        help='Python code for transforming data during migration'
    )
    
    active = fields.Boolean(default=True)
    
    @api.model
    def apply_mapping(self, mapping_name, source_data):
        """Apply a data mapping to source data"""
        mapping = self.search([('name', '=', mapping_name), ('active', '=', True)], limit=1)
        if not mapping:
            _logger.error("Mapping not found: %s", mapping_name)
            return None
            
        try:
            field_mapping = json.loads(mapping.field_mapping)
            result = {}
            
            # Apply simple field mappings
            for src_field, tgt_field in field_mapping.items():
                if src_field in source_data:
                    result[tgt_field] = source_data[src_field]
            
            # Apply transformations if needed
            if mapping.mapping_logic in ['transform', 'complex'] and mapping.transformation_code:
                # Create a safe environment for executing transformation code
                local_dict = {
                    'source': source_data,
                    'result': result,
                    'mapping': mapping,
                }
                
                # Execute transformation code
                exec(mapping.transformation_code, {'__builtins__': {}}, local_dict)
                
                # Get back the transformed result
                result = local_dict.get('result', {})
                
            return result
            
        except Exception as e:
            _logger.error("Error applying mapping %s: %s", mapping_name, str(e))
            return None

class MigrationFieldTransformer(models.Model):
    _name = 'migration.field.transformer'
    _description = 'Field Data Transformation Rules'
    
    name = fields.Char(required=True)
    field_name = fields.Char(string='Field Name', required=True)
    source_value = fields.Char(string='Source Value')
    target_value = fields.Char(string='Target Value')
    
    transformation_type = fields.Selection([
        ('direct', 'Direct Mapping'),
        ('function', 'Function Call'),
        ('regex', 'Regular Expression'),
        ('default', 'Default Value')
    ], default='direct', required=True)
    
    transformation_code = fields.Text(string='Transformation Code')
    
    mapping_id = fields.Many2one('migration.data.mapping', string='Mapping')
    sequence = fields.Integer(default=10)
    
    def transform_value(self, value):
        """Transform a single value based on the transformation rule"""
        if self.transformation_type == 'direct':
            if self.source_value and value == self.source_value:
                return self.target_value
            return value
            
        elif self.transformation_type == 'default':
            return self.target_value if value in [False, None, ''] else value
            
        elif self.transformation_type == 'function' and self.transformation_code:
            try:
                local_dict = {
                    'value': value,
                    'result': None
                }
                exec(self.transformation_code, {'__builtins__': {}}, local_dict)
                return local_dict.get('result', value)
            except Exception as e:
                _logger.error("Error in transformation function: %s", str(e))
                return value
                
        elif self.transformation_type == 'regex' and self.transformation_code:
            try:
                import re
                pattern = re.compile(self.source_value)
                return pattern.sub(self.target_value, value) if isinstance(value, str) else value
            except Exception as e:
                _logger.error("Error in regex transformation: %s", str(e))
                return value
                
        return value
```

### Version Migration Scripts

#### From Odoo 17 to 18 Migration

```python
# migration/odoo17_to_18.py
from odoo import api, fields, models, SUPERUSER_ID
import logging
from .migration_framework import MigrationTool

_logger = logging.getLogger(__name__)

class Odoo17To18Migration(MigrationTool):
    """Migration tool for Odoo 17 to Odoo 18 database migration"""
    
    def __init__(self, env, options=None):
        super().__init__(env, options)
        self.old_view_types = {'tree': 'list'}  # Map old view types to new ones
    
    def migrate_views(self):
        """Migrate view definitions from 17 to 18"""
        with self.migration_stats("Migrating views (tree -> list)"):
            # Find all views that need updating
            views = self.env['ir.ui.view'].search([
                ('type', '=', 'tree'),
            ])
            
            for view in views:
                try:
                    # Update view type
                    view.type = 'list'
                    
                    # Update arch_db content
                    if view.arch_db and '<tree' in view.arch_db:
                        new_arch = view.arch_db.replace('<tree', '<list')
                        view.arch_db = new_arch
                    
                    self.stats['records_updated'] += 1
                    self.log_migration_step('ir.ui.view', view.id, 'updated', 
                                           'Converted tree view to list view')
                except Exception as e:
                    self.stats['errors'] += 1
                    self.log_migration_step('ir.ui.view', view.id, 'error', str(e))
    
    def migrate_actions(self):
        """Update action view_mode from tree to list"""
        with self.migration_stats("Migrating actions (tree -> list in view_mode)"):
            actions = self.env['ir.actions.act_window'].search([
                ('view_mode', 'like', 'tree'),
            ])
            
            for action in actions:
                try:
                    if action.view_mode:
                        new_view_mode = action.view_mode.replace('tree', 'list')
                        action.view_mode = new_view_mode
                        
                    self.stats['records_updated'] += 1
                    self.log_migration_step('ir.actions.act_window', action.id, 'updated',
                                           'Updated view_mode from tree to list')
                except Exception as e:
                    self.stats['errors'] += 1
                    self.log_migration_step('ir.actions.act_window', action.id, 'error', str(e))
    
    def migrate_model_data(self):
        """Update model data related to view changes"""
        with self.migration_stats("Updating model data references"):
            # Example: update reference data for view types
            model_data = self.env['ir.model.data'].search([
                ('model', '=', 'ir.ui.view'),
                ('name', 'like', '%_tree_%')
            ])
            
            for data in model_data:
                try:
                    # Update name to use list instead of tree
                    if '_tree_' in data.name:
                        new_name = data.name.replace('_tree_', '_list_')
                        data.name = new_name
                    
                    self.stats['records_updated'] += 1
                    self.log_migration_step('ir.model.data', data.id, 'updated')
                except Exception as e:
                    self.stats['errors'] += 1
                    self.log_migration_step('ir.model.data', data.id, 'error', str(e))
    
    def run_full_migration(self):
        """Run the complete migration process"""
        # Start transaction
        self.env.cr.execute('SAVEPOINT migration_start')
        
        try:
            self.migrate_views()
            self.migrate_actions()
            self.migrate_model_data()
            
            # Add more migration steps as needed
            
            _logger.info("Migration completed successfully")
            return True
        except Exception as e:
            self.env.cr.execute('ROLLBACK TO SAVEPOINT migration_start')
            _logger.error("Migration failed: %s", str(e))
            return False
```

### External Data Import Frameworks

#### CSV Data Import Tool

```python
# migration/csv_importer.py
import csv
import logging
import os
from odoo import models, fields, api, exceptions, _
from odoo.tools import config
import base64
import tempfile

_logger = logging.getLogger(__name__)

class CSVImportJob(models.Model):
    _name = 'migration.csv.import.job'
    _description = 'CSV Import Job'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char(required=True)
    model_id = fields.Many2one('ir.model', string='Model', required=True)
    model_name = fields.Char(related='model_id.model', readonly=True)
    
    csv_file = fields.Binary(string='CSV File', required=True)
    csv_filename = fields.Char(string='CSV Filename')
    delimiter = fields.Char(string='Delimiter', default=',', size=1)
    has_header = fields.Boolean(string='Has Header', default=True)
    
    field_mapping = fields.Text(
        string='Field Mapping',
        help='JSON mapping of CSV columns to model fields',
        default='{}'
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('running', 'Running'),
        ('done', 'Completed'),
        ('failed', 'Failed')
    ], default='draft', tracking=True)
    
    total_rows = fields.Integer(string='Total Rows', readonly=True)
    processed_rows = fields.Integer(string='Processed', readonly=True)
    created_records = fields.Integer(string='Created', readonly=True)
    updated_records = fields.Integer(string='Updated', readonly=True)
    error_rows = fields.Integer(string='Errors', readonly=True)
    
    log_ids = fields.One2many('migration.import.log', 'import_job_id', string='Import Logs')
    
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    create_date = fields.Datetime(string='Created on', readonly=True)
    
    def action_validate(self):
        """Validate the CSV file and mapping before import"""
        self.ensure_one()
        
        if not self.csv_file:
            raise exceptions.UserError(_("Please upload a CSV file first"))
            
        try:
            # Decode the CSV file
            csv_data = base64.b64decode(self.csv_file)
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(csv_data)
                temp_file_path = temp_file.name
                
            # Read the CSV file to count rows and validate
            with open(temp_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=self.delimiter)
                # Get the header row if exists
                header = next(reader) if self.has_header else None
                
                # Count the remaining rows
                row_count = sum(1 for _ in reader)
                
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            # Update job statistics
            self.write({
                'total_rows': row_count,
                'state': 'validated'
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Validation Complete'),
                    'message': _(f"The CSV file has been validated with {row_count} rows ready for import."),
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            raise exceptions.UserError(_(f"Validation failed: {str(e)}"))
    
    def action_import(self):
        """Execute the CSV import process"""
        self.ensure_one()
        
        if self.state != 'validated':
            raise exceptions.UserError(_("Please validate the file before importing"))
            
        # Update job status
        self.write({
            'state': 'running',
            'processed_rows': 0,
            'created_records': 0,
            'updated_records': 0,
            'error_rows': 0
        })
        
        try:
            # Import in a separate transaction
            self._cr.commit()
            
            # Start the import process
            self._process_csv_import()
            
            # Update job status on completion
            self.write({
                'state': 'done'
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Import Complete'),
                    'message': _(f"Successfully processed {self.processed_rows} rows. "
                                f"Created: {self.created_records}, "
                                f"Updated: {self.updated_records}, "
                                f"Errors: {self.error_rows}"),
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            self.write({
                'state': 'failed'
            })
            # Log the error
            self.env['migration.import.log'].create({
                'import_job_id': self.id,
                'level': 'error',
                'message': f"Import process failed: {str(e)}",
            })
            raise exceptions.UserError(_(f"Import failed: {str(e)}"))
    
    def _process_csv_import(self):
        """Process the CSV file and import data"""
        import json
        
        # Get field mapping
        try:
            field_mapping = json.loads(self.field_mapping)
        except:
            raise exceptions.UserError(_("Invalid field mapping JSON"))
            
        # Decode the CSV file
        csv_data = base64.b64decode(self.csv_file)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(csv_data)
            temp_file_path = temp_file.name
            
        try:
            # Process the file
            with open(temp_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=self.delimiter)
                
                # Get headers if file has them
                headers = next(reader) if self.has_header else None
                
                # Process each row
                for row_num, row in enumerate(reader, start=2 if self.has_header else 1):
                    try:
                        # Create data dict from row
                        data = {}
                        
                        # Map CSV columns to model fields
                        for csv_col, field_name in field_mapping.items():
                            try:
                                col_idx = int(csv_col)
                                if col_idx < len(row):
                                    data[field_name] = row[col_idx]
                            except (ValueError, IndexError):
                                if headers and csv_col in headers:
                                    col_idx = headers.index(csv_col)
                                    data[field_name] = row[col_idx]
                        
                        # Create or update record
                        if data:
                            result = self._create_or_update_record(data)
                            
                            # Update statistics
                            self.processed_rows += 1
                            if result.get('created'):
                                self.created_records += 1
                            elif result.get('updated'):
                                self.updated_records += 1
                                
                            # Log success
                            self.env['migration.import.log'].create({
                                'import_job_id': self.id,
                                'row_num': row_num,
                                'level': 'info',
                                'record_id': result.get('record_id'),
                                'message': f"Record {'created' if result.get('created') else 'updated'}"
                            })
                        
                        # Commit every 100 rows to avoid large transactions
                        if row_num % 100 == 0:
                            self.env.cr.commit()
                            self.write({
                                'processed_rows': self.processed_rows,
                                'created_records': self.created_records,
                                'updated_records': self.updated_records,
                                'error_rows': self.error_rows
                            })
                            
                    except Exception as e:
                        self.error_rows += 1
                        # Log the error
                        self.env['migration.import.log'].create({
                            'import_job_id': self.id,
                            'row_num': row_num,
                            'level': 'error',
                            'message': f"Error processing row: {str(e)}",
                        })
                        _logger.error("Error importing row %s: %s", row_num, str(e))
                        
            # Update final statistics
            self.write({
                'processed_rows': self.processed_rows,
                'created_records': self.created_records,
                'updated_records': self.updated_records,
                'error_rows': self.error_rows
            })
            
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)
    
    def _create_or_update_record(self, data):
        """Create or update a record based on import data"""
        model = self.env[self.model_name]
        result = {'created': False, 'updated': False, 'record_id': None}
        
        # Check if we need to find an existing record
        external_id = data.pop('external_id', None)
        
        if external_id:
            # Try to find by external ID
            existing = self.env.ref(external_id, False)
            if existing and existing._name == self.model_name:
                existing.write(data)
                result['updated'] = True
                result['record_id'] = existing.id
                return result
                
        # Create new record
        record = model.create(data)
        result['created'] = True
        result['record_id'] = record.id
        return result

class ImportLog(models.Model):
    _name = 'migration.import.log'
    _description = 'Import Log Entry'
    _order = 'create_date desc'
    
    import_job_id = fields.Many2one('migration.csv.import.job', string='Import Job')
    row_num = fields.Integer(string='Row Number')
    level = fields.Selection([
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error')
    ], default='info')
    message = fields.Text(string='Message')
    record_id = fields.Integer(string='Record ID')
    create_date = fields.Datetime(string='Created on', readonly=True)
```

### Database Migration Tools

#### Pre-Migration Analysis Tool

```python
# migration/db_analysis.py
from odoo import models, fields, api, SUPERUSER_ID
import logging
import json
import psycopg2
import base64
import tempfile
import os

_logger = logging.getLogger(__name__)

class MigrationDatabaseAnalysis(models.Model):
    _name = 'migration.db.analysis'
    _description = 'Database Migration Analysis'
    _order = 'create_date desc'
    
    name = fields.Char(required=True)
    source_db_name = fields.Char(string='Source Database')
    target_version = fields.Char(string='Target Odoo Version', default='18.0')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('analyzing', 'Analyzing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='draft')
    
    analysis_date = fields.Datetime(string='Analysis Date')
    analysis_results = fields.Binary(string='Analysis Report')
    report_filename = fields.Char(string='Report Filename')
    
    # Summary statistics
    total_tables = fields.Integer(string='Total Tables')
    modules_installed = fields.Integer(string='Modules Installed')
    custom_modules = fields.Integer(string='Custom Modules')
    data_volume_mb = fields.Float(string='Data Volume (MB)')
    estimated_time_minutes = fields.Float(string='Est. Migration Time (min)')
    
    # Issue statistics
    critical_issues = fields.Integer(string='Critical Issues')
    major_issues = fields.Integer(string='Major Issues')
    minor_issues = fields.Integer(string='Minor Issues')
    
    issue_ids = fields.One2many('migration.db.issue', 'analysis_id', string='Issues')
    
    def action_analyze_database(self):
        """Analyze the current database for migration readiness"""
        self.ensure_one()
        
        self.write({
            'state': 'analyzing',
            'analysis_date': fields.Datetime.now()
        })
        
        # Use a separate cursor for analysis to avoid interfering with the current transaction
        db_name = self.env.cr.dbname
        db_host = tools.config.get('db_host', 'localhost')
        db_port = tools.config.get('db_port', 5432)
        db_user = tools.config.get('db_user', 'odoo')
        db_password = tools.config.get('db_password', 'odoo')
        
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                dbname=db_name
            )
            
            # Start analysis
            analysis_results = {
                'database': db_name,
                'analysis_date': fields.Datetime.now().isoformat(),
                'tables': {},
                'modules': {},
                'issues': [],
                'summary': {}
            }
            
            # Analyze database structure
            self._analyze_table_structure(conn, analysis_results)
            
            # Analyze installed modules
            self._analyze_modules(analysis_results)
            
            # Check for known migration issues
            self._analyze_migration_issues(analysis_results)
            
            # Calculate summary statistics
            self._calculate_summary(analysis_results)
            
            # Create issues records
            self._create_issue_records(analysis_results['issues'])
            
            # Generate report
            report_content = self._generate_report(analysis_results)
            
            # Update record with results
            self.write({
                'state': 'completed',
                'analysis_results': base64.b64encode(report_content.encode('utf-8')),
                'report_filename': f'migration_analysis_{self.source_db_name or db_name}_{fields.Date.today()}.json',
                'total_tables': analysis_results['summary']['total_tables'],
                'modules_installed': analysis_results['summary']['modules_installed'],
                'custom_modules': analysis_results['summary']['custom_modules'],
                'data_volume_mb': analysis_results['summary']['data_volume_mb'],
                'estimated_time_minutes': analysis_results['summary']['estimated_time_minutes'],
                'critical_issues': analysis_results['summary']['critical_issues'],
                'major_issues': analysis_results['summary']['major_issues'],
                'minor_issues': analysis_results['summary']['minor_issues']
            })
            
        except Exception as e:
            _logger.error("Database analysis failed: %s", str(e))
            self.write({
                'state': 'failed'
            })
            # Create an issue record for the failure
            self.env['migration.db.issue'].create({
                'analysis_id': self.id,
                'severity': 'critical',
                'issue_type': 'error',
                'description': f"Analysis failed: {str(e)}",
                'recommended_action': "Check database connection settings and permissions"
            })
            
        finally:
            if 'conn' in locals():
                conn.close()
    
    def _analyze_table_structure(self, conn, results):
        """Analyze database table structure"""
        cursor = conn.cursor()
        
        # Get table information
        cursor.execute("""
            SELECT 
                table_name, 
                pg_total_relation_size('"' || table_schema || '"."' || table_name || '"') as size_bytes
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY size_bytes DESC
        """)
        
        tables = cursor.fetchall()
        total_size = 0
        
        for table_name, size_bytes in tables:
            total_size += size_bytes
            
            # Check column structure for specific tables
            if table_name in ['ir_ui_view', 'ir_actions_act_window']:
                cursor.execute(f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = %s
                """, (table_name,))
                
                columns = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Store table info
                results['tables'][table_name] = {
                    'size_bytes': size_bytes,
                    'size_mb': round(size_bytes / (1024 * 1024), 2),
                    'columns': columns
                }
                
                # Check for known issues in table structure
                self._check_table_issues(table_name, columns, results)
        
        # Store overall database size
        results['summary'] = {
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'total_tables': len(tables)
        }
        
        cursor.close()
    
    def _analyze_modules(self, results):
        """Analyze installed modules for migration issues"""
        Module = self.env['ir.module.module']
        
        # Get all installed modules
        modules = Module.search([('state', '=', 'installed')])
        
        results['summary']['modules_installed'] = len(modules)
        results['summary']['custom_modules'] = 0
        
        for module in modules:
            # Check if it's a custom module
            is_custom = not module.website.startswith('https://www.odoo.com')
            
            if is_custom:
                results['summary']['custom_modules'] += 1
                
            # Store module info
            results['modules'][module.name] = {
                'name': module.name,
                'installed_version': module.installed_version,
                'is_custom': is_custom,
                'dependencies': [dep.name for dep in module.dependencies_id]
            }
            
            # Check for known module migration issues
            self._check_module_issues(module, results)
    
    def _check_table_issues(self, table_name, columns, results):
        """Check for known issues in table structure"""
        if table_name == 'ir_ui_view':
            if 'type' in columns:
                # Check if we have any tree views
                self.env.cr.execute("""
                    SELECT id, name FROM ir_ui_view WHERE type = 'tree'
                """)
                tree_views = self.env.cr.fetchall()
                
                if tree_views:
                    results['issues'].append({
                        'severity': 'critical',
                        'issue_type': 'structure',
                        'description': f"Found {len(tree_views)} tree views that need migration to list views",
                        'details': {
                            'view_ids': [view[0] for view in tree_views],
                            'view_names': [view[1] for view in tree_views]
                        },
                        'recommended_action': "Convert tree views to list views using migration script"
                    })
        
        elif table_name == 'ir_actions_act_window':
            if 'view_mode' in columns:
                # Check for view_mode containing 'tree'
                self.env.cr.execute("""
                    SELECT id, name, view_mode 
                    FROM ir_actions_act_window 
                    WHERE view_mode LIKE '%tree%'
                """)
                tree_actions = self.env.cr.fetchall()
                
                if tree_actions:
                    results['issues'].append({
                        'severity': 'critical',
                        'issue_type': 'structure',
                        'description': f"Found {len(tree_actions)} actions using 'tree' in view_mode",
                        'details': {
                            'action_ids': [action[0] for action in tree_actions],
                            'action_names': [action[1] for action in tree_actions]
                        },
                        'recommended_action': "Convert view_mode from 'tree' to 'list' in actions"
                    })
    
    def _check_module_issues(self, module, results):
        """Check for known module migration issues"""
        # Check for deprecated modules in Odoo 18
        deprecated_modules = ['web_kanban', 'web_settings_dashboard']
        
        if module.name in deprecated_modules:
            results['issues'].append({
                'severity': 'critical',
                'issue_type': 'module',
                'description': f"Module '{module.name}' is deprecated in Odoo 18",
                'details': {
                    'module_name': module.name,
                    'installed_version': module.installed_version
                },
                'recommended_action': f"Remove dependency on {module.name} and update code to use new APIs"
            })
        
        # Check for modules with known API changes
        api_changed_modules = ['web', 'mail', 'base']
        
        if module.name in api_changed_modules and module.is_custom:
            results['issues'].append({
                'severity': 'major',
                'issue_type': 'module',
                'description': f"Module '{module.name}' has significant API changes in Odoo 18",
                'details': {
                    'module_name': module.name,
                    'installed_version': module.installed_version
                },
                'recommended_action': "Review custom code for API compatibility"
            })
    
    def _analyze_migration_issues(self, results):
        """Analyze database for known migration issues"""
        # Check for deprecated features
        self._check_deprecated_features(results)
        
        # Check for data integrity issues
        self._check_data_integrity(results)
    
    def _check_deprecated_features(self, results):
        """Check for usage of deprecated features"""
        # Example: Check for old view syntax in arch_db
        self.env.cr.execute("""
            SELECT id, name
            FROM ir_ui_view
            WHERE arch_db LIKE '%<tree%'
        """)
        old_views = self.env.cr.fetchall()
        
        if old_views:
            results['issues'].append({
                'severity': 'critical',
                'issue_type': 'syntax',
                'description': f"Found {len(old_views)} views using deprecated <tree> element",
                'details': {
                    'view_ids': [view[0] for view in old_views],
                    'view_names': [view[1] for view in old_views]
                },
                'recommended_action': "Replace <tree> with <list> in view definitions"
            })
    
    def _check_data_integrity(self, results):
        """Check for data integrity issues that could affect migration"""
        # Example: Check for orphaned records
        self.env.cr.execute("""
            SELECT m.model
            FROM ir_model_data d
            JOIN ir_model m ON d.model = m.model
            WHERE NOT EXISTS (
                SELECT 1
                FROM ir_model_fields f
                WHERE f.model_id = m.id
            )
            GROUP BY m.model
        """)
        orphaned_models = [row[0] for row in self.env.cr.fetchall()]
        
        if orphaned_models:
            results['issues'].append({
                'severity': 'major',
                'issue_type': 'data',
                'description': f"Found {len(orphaned_models)} models with potential orphaned records",
                'details': {
                    'models': orphaned_models
                },
                'recommended_action': "Clean up orphaned records before migration"
            })
    
    def _calculate_summary(self, results):
        """Calculate summary statistics for the analysis"""
        # Count issues by severity
        critical = 0
        major = 0
        minor = 0
        
        for issue in results['issues']:
            if issue['severity'] == 'critical':
                critical += 1
            elif issue['severity'] == 'major':
                major += 1
            elif issue['severity'] == 'minor':
                minor += 1
        
        # Update summary
        results['summary'].update({
            'critical_issues': critical,
            'major_issues': major,
            'minor_issues': minor,
            'data_volume_mb': results['summary']['total_size_mb'],
            # Estimate migration time based on data volume and issues
            'estimated_time_minutes': self._estimate_migration_time(
                results['summary']['total_size_mb'], 
                critical, 
                major, 
                minor
            )
        })
    
    def _estimate_migration_time(self, data_volume_mb, critical, major, minor):
        """Estimate migration time based on data size and issues"""
        # Simple estimation formula
        base_time = 30  # Base time in minutes
        volume_factor = data_volume_mb / 100  # 1 minute per 100MB
        issue_factor = critical * 20 + major * 5 + minor * 1  # Time per issue
        
        return round(base_time + volume_factor + issue_factor, 2)
    
    def _create_issue_records(self, issues):
        """Create database issue records from analysis"""
        for issue in issues:
            self.env['migration.db.issue'].create({
                'analysis_id': self.id,
                'severity': issue['severity'],
                'issue_type': issue['issue_type'],
                'description': issue['description'],
                'details': json.dumps(issue.get('details', {})),
                'recommended_action': issue['recommended_action']
            })
    
    def _generate_report(self, results):
        """Generate a detailed report from analysis results"""
        # Format results as pretty JSON
        return json.dumps(results, indent=2)

class MigrationDatabaseIssue(models.Model):
    _name = 'migration.db.issue'
    _description = 'Database Migration Issue'
    _order = 'severity desc, id'
    
    analysis_id = fields.Many2one('migration.db.analysis', string='Analysis', ondelete='cascade')
    severity = fields.Selection([
        ('critical', 'Critical'),
        ('major', 'Major'),
        ('minor', 'Minor')
    ], default='minor', required=True)
    
    issue_type = fields.Selection([
        ('structure', 'Database Structure'),
        ('module', 'Module Compatibility'),
        ('syntax', 'Code Syntax'),
        ('data', 'Data Issue'),
        ('error', 'Error')
    ], default='data', required=True)
    
    description = fields.Text(required=True)
    details = fields.Text(help="JSON format details about the issue")
    recommended_action = fields.Text(required=True)
    
    resolved = fields.Boolean(default=False)
    resolution_note = fields.Text()
    resolution_date = fields.Datetime()
    
    def action_mark_resolved(self):
        """Mark an issue as resolved"""
        self.write({
            'resolved': True,
            'resolution_date': fields.Datetime.now()
        })
```

## Migration Best Practices

### Pre-Migration Workflow

1. **Assessment and Planning**
   - Perform complete database analysis using tools
   - Document all custom modules and modifications
   - Map out data dependencies and relationships
   - Create comprehensive migration plan with timeline

2. **Environment Setup**
   - Create isolated development environment
   - Set up target Odoo version with required dependencies
   - Create database backup strategy for recovery
   - Configure version control for migration scripts

3. **Data Cleansing**
   - Remove obsolete or redundant data
   - Fix data integrity issues and inconsistencies
   - Normalize data structures where possible
   - Document data volumes and growth patterns

4. **Test Migration Strategy**
   - Create small-scale test migrations
   - Document technical challenges and solutions
   - Establish data validation procedures
   - Create automated testing for critical functions

### Migration Execution Steps

1. **Database Structure Migration**
   ```python
   # Steps:
   # 1. Backup source database
   # 2. Run pre-migration scripts
   # 3. Update database structure
   # 4. Run post-migration data fixes
   
   # Example pre-migration script
   def pre_migrate_views():
      """Convert tree views to list views before upgrading"""
      env.cr.execute("""
          UPDATE ir_ui_view SET type = 'list' WHERE type = 'tree'
      """)
      
      env.cr.execute("""
          UPDATE ir_ui_view 
          SET arch_db = REPLACE(arch_db, '<tree', '<list')
          WHERE arch_db LIKE '%<tree%'
      """)
      
      env.cr.execute("""
          UPDATE ir_actions_act_window
          SET view_mode = REPLACE(view_mode, 'tree', 'list')
          WHERE view_mode LIKE '%tree%'
      """)
   ```

2. **Module Migration Order**
   - Base modules first (base, web, mail)
   - Standard application modules (account, sale, purchase)
   - Custom modules in dependency order
   - Interface and theme modules last

3. **Data Transformation**
   ```python
   # Example data transformation for changed field types
   def transform_data_types():
      """Transform data types for changed fields"""
      # Example: Convert text to json fields
      env.cr.execute("""
          ALTER TABLE my_model
          ADD COLUMN new_json_field JSONB
      """)
      
      env.cr.execute("""
          UPDATE my_model
          SET new_json_field = old_text_field::JSONB
          WHERE old_text_field IS NOT NULL
      """)
   ```

4. **Testing and Validation**
   - Automated test suite execution
   - Data integrity validation checks
   - User acceptance testing with real data
   - Performance benchmarking against source system

### Post-Migration Activities

1. **Data Verification**
   ```python
   # Example verification query
   def verify_migration():
      """Verify data consistency after migration"""
      # Check record counts match
      env.cr.execute("""
          SELECT 'partners', COUNT(*) FROM res_partner
          UNION ALL
          SELECT 'invoices', COUNT(*) FROM account_move
          UNION ALL
          SELECT 'products', COUNT(*) FROM product_template
      """)
      counts = env.cr.fetchall()
      
      # Compare with expected counts
      expected = {
          'partners': 15420,
          'invoices': 28760,
          'products': 3451
      }
      
      discrepancies = []
      for model, count in counts:
          if model in expected and expected[model] != count:
              discrepancies.append(f"{model}: Expected {expected[model]}, got {count}")
              
      return discrepancies
   ```

2. **Performance Optimization**
   - Database index optimization
   - Query performance analysis
   - Module and view loading optimization
   - Server configuration tuning

3. **Documentation Update**
   - Update technical documentation
   - Document migration process and challenges
   - Create user guides for new features
   - Document system architecture changes

## Odoo 18+ Specific Migration Considerations

### Key Changes in Odoo 18

1. **View Changes**
   - `<tree>` renamed to `<list>` in XML views
   - `view_mode="tree,form"` changed to `view_mode="list,form"`
   - Changes in kanban view structure and API

2. **ORM Changes**
   - New field attributes and options
   - Changes in compute method behaviors
   - Modified onchange handling
   - New API decorators

3. **Frontend Framework Updates**
   - OWL component system changes
   - JavaScript API modifications
   - Asset bundling system updates
   - QWeb template rendering differences

4. **Database Schema Changes**
   - New field types and constraints
   - Modified table structures in core modules
   - Changes in PostgreSQL requirements and features
   - Indexing strategy updates

### Critical Migration Fixes

#### Tree to List View Migration

```python
# Complete tree to list migration script
def migrate_tree_to_list_views(env):
    """Comprehensive migration of tree views to list views"""
    # 1. Update view records
    env.cr.execute("""
        UPDATE ir_ui_view 
        SET type = 'list' 
        WHERE type = 'tree'
    """)
    
    # 2. Update view arch content
    views = env['ir.ui.view'].search([
        ('arch_db', 'like', '%<tree')
    ])
    
    for view in views:
        modified_arch = view.arch_db.replace('<tree', '<list')
        view.write({'arch_db': modified_arch})
    
    # 3. Update action view modes
    actions = env['ir.actions.act_window'].search([
        ('view_mode', 'like', '%tree%')
    ])
    
    for action in actions:
        modified_view_mode = action.view_mode.replace('tree', 'list')
        action.write({'view_mode': modified_view_mode})
    
    # 4. Update references in ir_model_data
    env.cr.execute("""
        UPDATE ir_model_data
        SET name = REPLACE(name, '_tree_', '_list_')
        WHERE model = 'ir.ui.view'
        AND name LIKE '%_tree_%'
    """)
    
    # 5. Update custom views that inherit tree views
    env.cr.execute("""
        UPDATE ir_ui_view
        SET arch_db = REPLACE(arch_db, 'tree_view_ref', 'list_view_ref')
        WHERE arch_db LIKE '%tree_view_ref%'
    """)
```

#### Model and Field Changes

```python
def handle_field_type_changes(env):
    """Handle changes in field types between versions"""
    # Example: Handle changes in char fields that are now selection fields
    env.cr.execute("""
        CREATE OR REPLACE FUNCTION validate_selection_values(
            p_table_name text,
            p_column_name text,
            p_valid_values text[]
        ) RETURNS void AS $$
        DECLARE
            invalid_records text;
        BEGIN
            EXECUTE format('
                SELECT string_agg(%I::text, '', '') 
                FROM %I 
                WHERE %I IS NOT NULL 
                  AND %I != ALL($1)
            ', p_column_name, p_table_name, p_column_name, p_column_name)
            INTO invalid_records
            USING p_valid_values;
            
            IF invalid_records IS NOT NULL THEN
                RAISE EXCEPTION 'Invalid values found in %.%: %', 
                    p_table_name, p_column_name, invalid_records;
            END IF;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Example validation for status field that changed to selection
    env.cr.execute("""
        SELECT validate_selection_values(
            'my_model',
            'state',
            ARRAY['draft', 'confirmed', 'done']
        );
    """)
    
    # Fix any records with invalid values
    env.cr.execute("""
        UPDATE my_model
        SET state = 'draft'
        WHERE state NOT IN ('draft', 'confirmed', 'done')
        OR state IS NULL
    """)
```

## Data Migration Case Studies

### Case Study 1: CRM Data Migration

```python
# Case study for migrating CRM data from legacy system to Odoo 18
def migrate_legacy_crm(env, legacy_data):
    """Migrate CRM data from legacy system to Odoo 18"""
    # 1. Create data mappings
    partner_mapping = {
        'company_name': 'name',
        'tax_id': 'vat',
        'address': 'street',
        'zip_code': 'zip',
        'city_name': 'city',
        'phone_number': 'phone',
        'email_address': 'email'
    }
    
    # 2. Map country codes
    country_codes = {
        'USA': 'US',
        'United Kingdom': 'GB',
        'Deutschland': 'DE'
        # Add more mappings as needed
    }
    
    # 3. Process partners
    for legacy_partner in legacy_data.get('customers', []):
        partner_data = {}
        
        # Apply field mappings
        for legacy_field, odoo_field in partner_mapping.items():
            if legacy_field in legacy_partner:
                partner_data[odoo_field] = legacy_partner[legacy_field]
        
        # Handle country mapping
        if 'country' in legacy_partner:
            legacy_country = legacy_partner['country']
            if legacy_country in country_codes:
                country_code = country_codes[legacy_country]
                country = env['res.country'].search([('code', '=', country_code)], limit=1)
                if country:
                    partner_data['country_id'] = country.id
        
        # Create partner record
        partner = env['res.partner'].create(partner_data)
        
        # Process opportunities for this partner
        if 'opportunities' in legacy_partner:
            for legacy_opp in legacy_partner['opportunities']:
                opp_data = {
                    'name': legacy_opp.get('title', 'Untitled'),
                    'partner_id': partner.id,
                    'expected_revenue': float(legacy_opp.get('value', 0.0)),
                    'probability': float(legacy_opp.get('probability', 0.0)),
                    'description': legacy_opp.get('notes'),
                    'user_id': env.uid,  # Current user as salesperson
                    'team_id': env.ref('sales_team.salesteam_website_sales').id
                }
                
                # Map status
                status_mapping = {
                    'New': 1,  # ID of 'New' stage
                    'Qualified': 2,  # ID of 'Qualified' stage
                    'Proposition': 3,  # ID of 'Proposition' stage
                    'Won': 4  # ID of 'Won' stage
                }
                
                if 'status' in legacy_opp and legacy_opp['status'] in status_mapping:
                    opp_data['stage_id'] = status_mapping[legacy_opp['status']]
                
                # Create opportunity
                env['crm.lead'].create(opp_data)
    
    # Commit the changes
    env.cr.commit()
    
    return {
        'partners_created': len(legacy_data.get('customers', [])),
        'opportunities_created': sum(len(partner.get('opportunities', [])) 
                                    for partner in legacy_data.get('customers', []))
    }
```

### Case Study 2: E-commerce Integration

```python
# Case study for migrating e-commerce data to Odoo 18
def migrate_ecommerce_data(env, ecommerce_data):
    """Migrate e-commerce data to Odoo 18"""
    # Product category mapping
    category_map = {}
    
    # 1. Create product categories
    for category in ecommerce_data.get('categories', []):
        category_vals = {
            'name': category['name'],
            'description': category.get('description', '')
        }
        
        # Handle parent categories
        if category.get('parent_id') and category['parent_id'] in category_map:
            category_vals['parent_id'] = category_map[category['parent_id']]
            
        new_category = env['product.category'].create(category_vals)
        category_map[category['id']] = new_category.id
    
    # 2. Create products
    product_map = {}
    for product in ecommerce_data.get('products', []):
        # Find or create product template
        product_vals = {
            'name': product['name'],
            'description': product.get('description', ''),
            'description_sale': product.get('short_description', ''),
            'list_price': float(product.get('price', 0.0)),
            'default_code': product.get('sku', ''),
            'type': 'product',  # Storable product
            'invoice_policy': 'order',  # Invoice based on ordered quantity
            'purchase_method': 'purchase'  # Control policy for Purchase
        }
        
        # Set category if available
        if product.get('category_id') and product['category_id'] in category_map:
            product_vals['categ_id'] = category_map[product['category_id']]
            
        # Create the product
        new_product = env['product.template'].create(product_vals)
        product_map[product['id']] = new_product.id
        
        # Process product attributes and variants
        if 'attributes' in product:
            self._create_product_attributes(env, new_product, product['attributes'])
            
        # Process product images
        if 'images' in product:
            self._attach_product_images(env, new_product, product['images'])
    
    # 3. Import customers from e-commerce platform
    customer_map = {}
    for customer in ecommerce_data.get('customers', []):
        partner_vals = {
            'name': f"{customer.get('first_name', '')} {customer.get('last_name', '')}",
            'email': customer.get('email', ''),
            'phone': customer.get('phone', ''),
            'customer_rank': 1  # Mark as customer
        }
        
        # Create or update partner
        partner = env['res.partner'].create(partner_vals)
        customer_map[customer['id']] = partner.id
        
        # Create shipping addresses
        if 'addresses' in customer:
            for address in customer['addresses']:
                addr_vals = {
                    'name': f"{address.get('first_name', '')} {address.get('last_name', '')}",
                    'street': address.get('address1', ''),
                    'street2': address.get('address2', ''),
                    'city': address.get('city', ''),
                    'zip': address.get('postcode', ''),
                    'phone': address.get('phone', ''),
                    'type': 'delivery',
                    'parent_id': partner.id
                }
                
                # Find country
                if address.get('country_code'):
                    country = env['res.country'].search([
                        ('code', '=', address['country_code'])
                    ], limit=1)
                    if country:
                        addr_vals['country_id'] = country.id
                
                # Find state
                if address.get('state_code') and 'country_id' in addr_vals:
                    state = env['res.country.state'].search([
                        ('code', '=', address['state_code']),
                        ('country_id', '=', addr_vals['country_id'])
                    ], limit=1)
                    if state:
                        addr_vals['state_id'] = state.id
                
                # Create address
                env['res.partner'].create(addr_vals)
    
    # 4. Import orders
    for order in ecommerce_data.get('orders', []):
        # Find customer
        if order.get('customer_id') not in customer_map:
            continue
            
        partner_id = customer_map[order['customer_id']]
        
        # Create order
        sale_vals = {
            'partner_id': partner_id,
            'date_order': order.get('created_at', fields.Datetime.now()),
            'client_order_ref': order.get('reference', ''),
            'note': order.get('customer_note', '')
        }
        
        # Set shipping address
        if order.get('shipping_address_id'):
            shipping_partner = env['res.partner'].search([
                ('parent_id', '=', partner_id),
                ('type', '=', 'delivery')
            ], limit=1)
            if shipping_partner:
                sale_vals['partner_shipping_id'] = shipping_partner.id
        
        sale_order = env['sale.order'].create(sale_vals)
        
        # Create order lines
        for line in order.get('lines', []):
            if line.get('product_id') not in product_map:
                continue
                
            product_tmpl_id = product_map[line['product_id']]
            product = env['product.product'].search([
                ('product_tmpl_id', '=', product_tmpl_id)
            ], limit=1)
            
            if not product:
                continue
                
            # Create order line
            line_vals = {
                'order_id': sale_order.id,
                'product_id': product.id,
                'name': line.get('name', product.name),
                'product_uom_qty': float(line.get('quantity', 1.0)),
                'price_unit': float(line.get('price', 0.0))
            }
            
            env['sale.order.line'].create(line_vals)
        
        # Set order status
        if order.get('status'):
            self._set_order_status(env, sale_order, order['status'])
    
    # Commit changes
    env.cr.commit()
    
    return {
        'categories_created': len(category_map),
        'products_created': len(product_map),
        'customers_created': len(customer_map),
        'orders_created': len(ecommerce_data.get('orders', []))
    }

def _create_product_attributes(env, product_template, attributes):
    """Create product attributes and variants"""
    # Implementation for handling product attributes and variants
    pass

def _attach_product_images(env, product_template, images):
    """Attach images to products"""
    # Implementation for handling product images
    pass

def _set_order_status(env, sale_order, status):
    """Set the proper status on imported orders"""
    # Implementation for mapping external status to Odoo status
    pass
```

## Knowledge Resources

1. **Official Documentation**
   - [Odoo 18 Migration Guide](https://www.odoo.com/documentation/18.0/developer/reference/upgrade_api.html)
   - [PostgreSQL Data Migration Tools](https://www.postgresql.org/docs/current/migration.html)
   - [Odoo ORM API Reference](https://www.odoo.com/documentation/18.0/developer/reference/orm.html)

2. **Community Resources**
   - [Odoo Migration Forum](https://www.odoo.com/forum/help-1/migration-19)
   - [OCA Migration Tools](https://github.com/OCA/openupgrade)
   - [Odoo Migration Case Studies](https://www.odoo.com/blog/business-case-studies-6)

3. **Books and Articles**
   - "Odoo 18 Development: Migration and Upgrade Guide"
   - "Large-Scale Data Migration Best Practices"
   - "Database Migration Patterns and Anti-Patterns"

---

This role documentation serves as a comprehensive guide for Data Migration Specialists working with the Neodoo18Framework and Odoo 18+ applications. It covers all aspects of planning, executing, and validating data migrations between different Odoo versions or from external systems to Odoo 18+.