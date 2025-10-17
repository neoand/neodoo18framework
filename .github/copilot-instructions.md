````instructions
# Neodoo18Framework – AI Agent Guide

## Architecture Overview
This is a **complete Odoo 18+ development framework** that provisions full project environments (not just modules). It's designed for AI agents with a plugin-based validation system enforcing modern Odoo 18+ standards.

### Core Components & Data Flow
- **`framework/cli/neodoo.py`** (1046 lines) - Cross-platform CLI orchestrator
  - Commands: `create`, `list`, `delete`, `doctor`, `update`, `migrate`
  - Creates projects under `~/odoo_projects/` with full Odoo source, OCA modules, venv
  - Clones from: `https://github.com/odoo/odoo.git` (branch: `18.0`)
  - OCA modules: `https://github.com/OCA/web.git` + configurable repos
  
- **`framework/generator/create_project.py`** - Module scaffolding engine
  - Templates: `minimal/`, `advanced/`, `ecommerce/`, `*-project/` variants
  - Placeholder system: `{{MODULE_NAME}}`, `{{AUTHOR}}`, `{{CATEGORY}}`, etc.
  - Output: Complete module structure with `__manifest__.py`, `models/`, `views/`, `security/`
  
- **`framework/validator/`** - Extensible validation pipeline
  - **`validate.py`**: Orchestrates plugin loading and execution
  - **`plugin.py`**: `BaseValidatorPlugin` protocol, `ValidationContext`, `ValidationResult`
  - **`plugin_manager.py`**: Dynamic plugin discovery from `corporate_plugins/` or `$NEODOO_VALIDATOR_PLUGINS`
  - **`plugins/core.py`**: Core Odoo 18+ rules (XML `<list>`, manifest structure, security headers)
  
- **`framework/migration/analyzer.py`** - Migration assessment tool
  - Detects deprecated dependencies, legacy JS patterns, outdated XML tags
  - Runs core validator on target to identify Odoo 18+ incompatibilities
  - Generates `MigrationReport` with categorized tasks (mandatory/manual/optional)
  
- **`corporate_plugins/`** - Domain-specific rule examples
  - `acme_corporate_rules.py`: Enforces company prefix (`acme_`), forbidden patterns, docstring requirements
  - `neo_sempre_rules.py`: INSS domain rules (CPF as `vat`, margin fields, multiple prefixes)

### Project Structure Pattern (Created by CLI)
```
~/odoo_projects/project_name/
├── odoo_source/         # Full Odoo 18+ source (cloned from GitHub odoo/odoo.git@18.0)
├── custom_addons/       # Your modules - PRIMARY DEVELOPMENT TARGET
├── community_addons/    # OCA modules (web, l10n-brazil, server-tools)
│   └── web/            # Includes web_responsive and other UI enhancements
├── .venv/              # Isolated Python environment (created via virtualenv)
├── odoo.conf           # Pre-configured: database, addons_path, ports (8069, 8072)
├── run.sh              # One-click startup: sources .venv, runs odoo-bin -c odoo.conf
├── filestore/          # Odoo file attachments (auto-created on first run)
└── logs/               # odoo.log (configure in odoo.conf)
```
**Key insight**: The framework separates concerns - `odoo_source/` is immutable, `custom_addons/` is where you work.

## Essential Workflows

### Cross-Platform CLI Launchers (Choose by Platform)
```bash
# Linux/macOS - Direct shell execution
./neodoo                        # Interactive menu (recommended, color output)
./neodoo create --name my_project --template minimal --base-dir ~/odoo_projects
./neodoo doctor --path ~/odoo_projects/my_project  # Environment health check
./neodoo migrate custom_addons/my_module --from-version 17

# Windows Command Prompt/PowerShell
neodoo.bat create               # Same args as Linux/macOS
neodoo.bat doctor --path C:\odoo_projects\my_project

# Windows PowerShell Alternative
.\neodoo.ps1 create             # PowerShell script with same interface

# Universal Fallback (if above fail)
python framework/cli/neodoo.py create  # Direct Python invocation
```
**Pre-flight checks**: CLI validates Python ≥3.8 and PostgreSQL ≥12 before execution (see `neodoo` bash script, lines 9-17).

### Code Validation Pipeline (Critical for Quality)
```bash
# 1. Core Odoo 18+ validation with auto-fixes
python framework/validator/validate.py custom_addons/module --strict --auto-fix
# Checks: <list> tags, UTF-8 headers, _description fields, @api.depends, security structure
# --auto-fix: Corrects spacing, imports, some formatting (use cautiously on large files)

# 2. Corporate rules validation (see corporate_plugins/ for examples)
python framework/validator/validate.py custom_addons/module \
  --plugins-dir corporate_plugins --strict
# Example plugins: acme_corporate_rules.py (prefix enforcement), neo_sempre_rules.py (domain rules)

# 3. Migration analysis (before upgrading from 15/16/17)
./neodoo migrate path/to/module --from-version 17
# Detects: deprecated dependencies, legacy XML tags, outdated JS patterns
# Outputs: MigrationReport with categorized tasks (mandatory/manual/optional)

# 4. Environment health check (run FIRST before any work)
./neodoo doctor --path ~/odoo_projects/my_project
# Validates: Python/PostgreSQL versions, port availability (8069/8072), project structure
```
**Plugin discovery order**: 1. `$NEODOO_VALIDATOR_PLUGINS` env var, 2. `--plugins-dir` arg, 3. Built-in `CoreRulesPlugin`.

### VSCode Integration & Agent Brief System
**VSCode Tasks** (`.vscode/tasks.json`):
- `Neodoo: Open Interactive Menu` - Default build task (Ctrl+Shift+B)
- `Neodoo: Doctor` - Environment validation
- `Neodoo: Strict Validator` - Prompts for target path
- `Neodoo: Corporate Validator (AcmeCorp)` - Runs corporate plugins
- `Neodoo: Migration Analyzer` - Prompts for module path and source version
- `Neodoo: Development Workflow Complete` - Sequential: doctor → strict → corporate
- `Neodoo: Export Agent Brief` - Generates snapshot for AI context sharing

**Agent Brief Workflow** (`scripts/dev/export_agent_brief.sh`):
```bash
# Generate comprehensive project snapshot for AI agent handoffs
./scripts/dev/export_agent_brief.sh ~/odoo_projects/my_project
# Creates: docs/agent-brief.md with:
#   - Recent validation results (core + corporate)
#   - Doctor output (environment state)
#   - Command history with exit codes
#   - Project metadata (name, path, primary addons directory)
```
**Environment variable**: `NEODOO_FRAMEWORK_ROOT` auto-injected in tasks for relative paths.

## Critical Odoo 18+ Standards (Breaking Changes)

### XML Views - REQUIRED Changes from Odoo 17
**Breaking change**: `<tree>` tags deprecated, use `<list>` exclusively.
```xml
<!-- ❌ WRONG (Odoo 17 and earlier) -->
<tree string="Template Models">
    <field name="name"/>
</tree>

<!-- ✅ CORRECT (Odoo 18+) -->
<list string="Template Models">
    <field name="name"/>
</list>
```
**Actions**: Use `view_mode="list,form"` (not `"tree,form"`).
```python
# In window actions (__manifest__.py or XML)
'view_mode': 'list,form,kanban'  # ✅ Correct
'view_mode': 'tree,form,kanban'  # ❌ Will cause errors
```
**Validator enforcement**: All `<tree>` occurrences are **errors** (not warnings) in strict mode.

### Python Models - Mandatory Conventions
```python
# -*- coding: utf-8 -*-  # ✅ REQUIRED: UTF-8 header on every .py file

from odoo import models, fields, api

class MyModel(models.Model):
    _name = 'my.module.model'
    _description = 'Model Description'  # ✅ REQUIRED: _description field
    
    amount = fields.Monetary(
        currency_field='currency_id'  # ✅ REQUIRED for Monetary fields
    )
    
    @api.depends('line_ids.price')  # ✅ REQUIRED: @api.depends for compute
    def _compute_total(self):
        for record in self:
            record.total = sum(record.line_ids.mapped('price'))
    
    def action_confirm(self):
        self.ensure_one()  # ✅ REQUIRED in action/button methods
        self.state = 'confirmed'
```

### Manifest Requirements (`__manifest__.py`)
```python
{
    'name': 'My Module',
    'version': '18.0.1.0.0',  # ✅ REQUIRED format: 18.0.x.y.z
    'category': 'Sales',      # ✅ REQUIRED
    'summary': 'Short description',
    'author': 'Your Company',
    'website': 'https://yoursite.com',
    'depends': ['base', 'sale'],  # ✅ At minimum ['base']
    'data': [
        'security/ir.model.access.csv',  # ✅ Always first
        'views/views.xml',
    ],
    'installable': True,      # ✅ REQUIRED
    'application': False,     # ✅ REQUIRED (True if standalone app)
    'license': 'LGPL-3',     # ✅ REQUIRED
}
```

### Security Patterns (Critical for Installation)
**`security/ir.model.access.csv`** - REQUIRED headers (comma-separated):
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,0,0,0
```
**Module initialization**: `models/__init__.py` MUST import all model files:
```python
from . import my_model
from . import my_other_model
```

### Forbidden Patterns (Caught by Validator)
```python
print("Debug message")    # ❌ Use _logger.info() instead
breakpoint()              # ❌ Remove before commit
import pdb; pdb.set_trace()  # ❌ Use Odoo's debug mode
```

## Plugin System Architecture

### Plugin Lifecycle & Discovery
1. **Registration**: Plugins discovered via dynamic import from `--plugins-dir` or `$NEODOO_VALIDATOR_PLUGINS`
2. **Setup Phase**: `plugin.setup(context)` called once before validation
3. **File Iteration**: For each file, `plugin.supports(file_path, context)` determines eligibility
4. **Validation**: `plugin.validate_file(file_path, context)` returns `ValidationResult` or `None`
5. **Finalization**: `plugin.finalize(context)` for cross-file validations (e.g., dependency checks)

### Creating Corporate Rules - Complete Example
**File**: `corporate_plugins/acme_corporate_rules.py`
```python
from pathlib import Path
from framework.validator.plugin import BaseValidatorPlugin, ValidationContext, ValidationResult

class AcmeCorporateRulesPlugin(BaseValidatorPlugin):
    name = "acme_corporate_rules"
    description = "AcmeCorp specific validation rules for Odoo"
    
    def __init__(self):
        # Company-specific configuration
        self.company_prefix = "acme_"
        self.required_author = "AcmeCorp"
        self.forbidden_patterns = ["print(", "breakpoint(", "pdb.set_trace"]
        self.required_docstring_methods = ["action_", "button_", "compute_"]
    
    def supports(self, file_path: Path, context: ValidationContext) -> bool:
        """Only process Python, XML, CSV, and manifest files"""
        return file_path.suffix in {'.py', '.xml', '.csv'} or file_path.name == '__manifest__.py'
    
    def validate_file(self, file_path: Path, context: ValidationContext):
        result = ValidationResult()
        content = file_path.read_text(encoding='utf-8')
        
        # Example: Enforce model naming convention
        if file_path.suffix == '.py' and 'models.Model' in content:
            if f"_name = '{self.company_prefix}" not in content:
                result.add_error(
                    f"Model in {file_path} must use '{self.company_prefix}' prefix"
                )
        
        # Example: Manifest must include company as author
        if file_path.name == '__manifest__.py':
            if f"'{self.required_author}'" not in content:
                result.add_warning(
                    f"Manifest should include '{self.required_author}' as author"
                )
        
        return result if result.has_messages() else None

def register():  # REQUIRED: Entry point for plugin manager
    return [AcmeCorporateRulesPlugin()]
```

### Loading & Using Custom Plugins
```bash
# Method 1: Via environment variable (persistent)
export NEODOO_VALIDATOR_PLUGINS=/path/to/corporate_plugins
python framework/validator/validate.py custom_addons/

# Method 2: Via CLI argument (per-run)
python framework/validator/validate.py custom_addons/ \
  --plugins-dir corporate_plugins --strict

# Method 3: List available plugins
python framework/validator/validate.py --list-plugins
python framework/validator/validate.py --plugins-dir corporate_plugins --list-plugins
```

### Plugin Context & State Management
**`ValidationContext`** provides shared state:
```python
def validate_file(self, file_path: Path, context: ValidationContext):
    # Access project metadata
    module_name = context.module_name  # Inferred from path
    
    # Store state for cross-file validation
    context.scratch['seen_models'] = context.scratch.get('seen_models', set())
    context.scratch['seen_models'].add(parsed_model_name)
    
    # Check mode flags
    if context.strict:
        # More aggressive validation
    if context.auto_fix and fixable:
        # Apply automatic corrections (use cautiously)
```

### Real-World Plugin Examples
- **`acme_corporate_rules.py`**: Enforces company prefix, forbidden debug code, docstring requirements
- **`neo_sempre_rules.py`**: Domain-specific (INSS beneficiaries), multiple allowed prefixes, CPF field standardization

## Template System & Project Configuration

### Available Templates (in `templates/` directory)
**Module Templates** (generate single module):
- **`minimal/`** - Basic CRUD module
  - Structure: `__manifest__.py`, `models/template_model.py`, `views/views.xml`, `security/`
  - Use case: Simple business objects, lightweight customizations
  - Example: Customer feedback form, internal notes tracker
  
- **`advanced/`** - Full-featured module
  - Includes: Tests (`tests/test_template_model.py`), wizards, reports, complex workflows
  - Structure: Inherits minimal + `wizards/`, `reports/`, `static/`
  - Use case: Complex business logic, multi-step processes, reporting
  
- **`ecommerce/`** - E-commerce specific
  - Extends: Product, sale_order, website integration patterns
  - Use case: Online store customizations, payment gateways

**Project Templates** (generate full Odoo project):
- **`minimal-project/`** - Complete project scaffold with basic module
  - Creates: Entire `~/odoo_projects/` structure with venv, odoo.conf, run.sh
  - Use case: Greenfield Odoo projects, learning environments

### Placeholder Replacement System
**Available placeholders** (case-sensitive):
- `{{MODULE_NAME}}` - Display name (e.g., "My Custom Module")
- `{{MODULE_TECHNICAL_NAME}}` - Python-safe name (e.g., "my_custom_module")
- `{{AUTHOR}}` - Developer/company name
- `{{WEBSITE}}` - Company URL
- `{{CATEGORY}}` - Odoo app category (Sales, Inventory, etc.)
- `{{SUMMARY}}` - One-line description
- `{{DESCRIPTION}}` - Multi-line detailed description
- `{{IS_APPLICATION}}` - `True` or `False` (boolean)

**Example transformation** (`templates/minimal/__manifest__.py`):
```python
# Template file content:
{
    'name': '{{MODULE_NAME}}',
    'version': '18.0.1.0.0',
    'author': '{{AUTHOR}}',
    'category': '{{CATEGORY}}',
    'application': {{IS_APPLICATION}},
}

# After generation (./neodoo create --name "Sales Report" --author "AcmeCorp"):
{
    'name': 'Sales Report',
    'version': '18.0.1.0.0',
    'author': 'AcmeCorp',
    'category': 'Sales',
    'application': False,
}
```

### Configuration-Driven Project Creation
**YAML config file** (`.neodoo.yml`):
```yaml
version: 1
name: my_odoo18_project       # Project directory name
base_dir: ~/odoo_projects     # Parent directory
module: my_custom_module      # Initial module name
template: advanced            # Template to use
venv: true                   # Create virtual environment
odoo_branch: 18.0            # Odoo source branch
oca_repos:                   # Additional OCA repositories
  - web
  - server-tools
  - l10n-brazil
```
**Usage**: `./neodoo create --from-config ./docs/.neodoo.yml`

### Template Customization & Dry Run
```bash
# Preview changes without writing files
python framework/generator/create_project.py \
  --name my_module --type minimal --dry-run --no-all-placeholders

# Generate with custom placeholders
./neodoo create --name "Inventory Plus" \
  --template advanced \
  --category "Inventory/Management" \
  --author "YourCompany" \
  --website "https://example.com"
```
**Template documentation**: Each template has `TEMPLATE_INFO.md` explaining conventions.

## Automation & Continuous Integration

### Agent Brief System (AI Context Sharing)
**Purpose**: Generate comprehensive project snapshot for AI agent handoffs and debugging sessions.

**Script**: `scripts/dev/export_agent_brief.sh <project_path>`
```bash
./scripts/dev/export_agent_brief.sh ~/odoo_projects/my_project
# Output: docs/agent-brief.md
```

**Generated content** (example from `docs/agent-brief.md`):
```markdown
# Agent Brief
_Gerado em 2025-09-29 11:13:38 CST_

## Projeto
- Nome: semprereal
- Caminho: /Users/.../odoo_projects/semprereal
- Target validator: .../custom_addons

## Comandos Executados
- `./neodoo doctor --path .../semprereal` (exit: 0)
- `python3 framework/validator/validate.py .../custom_addons --strict --auto-fix` (exit: 0)
- `python3 framework/validator/validate.py .../custom_addons --plugins-dir corporate_plugins` (exit: 1)

## Resumo Doctor
✅ Ambiente saudável! Python 3.12, PostgreSQL 14, portas livres

## Resumo Validator
WARNING: 18 warnings (código funcional, padrões não críticos)

## Resumo Corporate Plugins
ERROR: 4 errors (prefixo 'acme_' ausente em modelos)
```
**VSCode integration**: Task `Neodoo: Export Agent Brief` automates this workflow.

### OCA Watch System (Automated Dependency Monitoring)
**Daily monitoring** (`scripts/oca_watch.py`):
- Checks configured OCA repos for new commits
- Generates/updates digests in `docs/oca-digests/`
- Creates auto-PRs with changes
- **Scheduled**: GitHub Actions at 02:00 UTC daily (`.github/workflows/oca-watch.yml`)

**Weekly rollup** (`scripts/oca_rollup.py`):
- Consolidates week's changes across all monitored repos
- Highlights breaking changes, new features
- **Scheduled**: GitHub Actions weekly (`.github/workflows/oca-weekly-rollup.yml`)

**Configuration** (`.neodoo/oca_watch.yml`):
```yaml
repositories:
  - name: web
    url: https://github.com/OCA/web.git
    branch: 18.0
  - name: server-tools
    url: https://github.com/OCA/server-tools.git
    branch: 18.0
```

### Quality Gates & Pre-Commit Hooks
**Smoke test suite** (`scripts/dev/quick_sanity.sh`):
```bash
./scripts/dev/quick_sanity.sh
# Runs: CLI help, validator on templates/, doctor on test project
# Exit code: 0 if all pass, non-zero otherwise
```

**Doctor checks** (`./neodoo doctor`):
- ✅ Python ≥3.8 in PATH
- ✅ PostgreSQL ≥12 accessible via `psql`
- ✅ Git, Docker optional checks
- ✅ Ports 8069 (HTTP) and 8072 (WebSocket) available
- ✅ Project structure integrity (`odoo_source/`, `custom_addons/`, `odoo.conf`)

**Validation pipeline** (run before every commit):
```bash
# Standard flow
python framework/validator/validate.py custom_addons/ --strict --auto-fix
python framework/validator/validate.py custom_addons/ --plugins-dir corporate_plugins --strict

# Expected outcome: 0 errors (warnings acceptable in dev, must address before release)
```

### CI/CD Integration Example (GitHub Actions)
**File**: `.github/workflows/ci.yml` (example snippet):
```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Run Validator
        run: |
          python framework/validator/validate.py custom_addons/ --strict
      - name: Run Corporate Rules
        run: |
          python framework/validator/validate.py custom_addons/ \
            --plugins-dir corporate_plugins --strict
```

## Before Starting Work (Pre-flight Checklist)

### 1. Environment Validation
```bash
./neodoo doctor --path ~/odoo_projects/your_project
```
**Must pass**: Python ≥3.8, PostgreSQL ≥12, ports 8069/8072 available, project structure intact.

### 2. Review Agent Brief (if available)
```bash
cat docs/agent-brief.md  # Check recent validation results, command history
```
**Look for**: Recent errors, corporate plugin violations, migration warnings.

### 3. Understand Odoo 18+ Breaking Changes
**Critical differences from Odoo 17**:
- XML: `<list>` replaces `<tree>` (breaking change)
- Actions: `view_mode="list,form"` not `"tree,form"`
- Python: `_description` mandatory, `self.ensure_one()` in actions

### 4. Template Selection Strategy
| Complexity | Template | Use Case |
|------------|----------|----------|
| Simple CRUD | `minimal` | Contact forms, basic trackers |
| Business logic | `advanced` | Approval workflows, reports, wizards |
| Web integration | `ecommerce` | Product catalog, payment flows |
| Full project | `*-project` | Greenfield Odoo installations |

### 5. Corporate Rules Awareness
```bash
# Check active plugins
python framework/validator/validate.py --list-plugins
python framework/validator/validate.py --plugins-dir corporate_plugins --list-plugins
```
**Review**: `corporate_plugins/` for domain-specific rules (prefixes, naming, field standards).

### 6. Migration Assessment (if upgrading)
```bash
./neodoo migrate path/to/legacy_module --from-version 17
```
**Act on**: Mandatory tasks in `MigrationReport` before proceeding.

## Common Pitfalls & Debugging

### Pitfall 1: XML View Tags (Most Frequent Error)
**Problem**: Using `<tree>` in Odoo 18+ views.
```xml
<!-- ❌ WRONG - Causes runtime error -->
<tree string="My List">
    <field name="name"/>
</tree>
```
**Solution**: Always use `<list>`.
```xml
<!-- ✅ CORRECT -->
<list string="My List">
    <field name="name"/>
</list>
```
**Detection**: Run `python framework/validator/validate.py module/ --strict` before testing.

### Pitfall 2: Manifest Version Mismatch
**Problem**: Odoo won't install module with wrong version format.
```python
# ❌ WRONG
'version': '1.0.0',        # Missing Odoo version
'version': '17.0.1.0.0',   # Outdated Odoo version
```
**Solution**: Use Odoo 18+ format.
```python
# ✅ CORRECT
'version': '18.0.1.0.0',   # Format: <odoo>.<major>.<minor>.<patch>.<hotfix>
```

### Pitfall 3: Missing `self.ensure_one()` in Actions
**Problem**: Action methods fail on recordsets with multiple records.
```python
def action_confirm(self):
    self.state = 'confirmed'  # ❌ Fails if self has multiple records
```
**Solution**: Add `self.ensure_one()`.
```python
def action_confirm(self):
    self.ensure_one()  # ✅ Raises error if called on multiple records
    self.state = 'confirmed'
```

### Pitfall 4: Template Placeholders Not Replaced
**Problem**: Generated files contain `{{MODULE_NAME}}` literally.
**Cause**: Incorrect generator invocation or missing CLI arguments.
**Solution**: Use full command with all required placeholders:
```bash
./neodoo create --name "My Module" --author "Company" --category "Sales"
# Or use interactive menu: ./neodoo (select "Create new project")
```

### Pitfall 5: Corporate Plugin Violations Ignored
**Problem**: Code passes core validation but fails in production due to corporate rules.
**Solution**: Always run both validators:
```bash
# Step 1: Core validation
python framework/validator/validate.py custom_addons/ --strict

# Step 2: Corporate validation (don't skip this!)
python framework/validator/validate.py custom_addons/ \
  --plugins-dir corporate_plugins --strict
```

### Debugging Commands
```bash
# Check validation in verbose mode
python framework/validator/validate.py module/ --strict --verbose

# List loaded plugins (verify corporate plugins detected)
python framework/validator/validate.py --list-plugins
python framework/validator/validate.py --plugins-dir corporate_plugins --list-plugins

# Dry-run module generation (preview output)
python framework/generator/create_project.py \
  --name test_module --type minimal --dry-run

# Check environment health
./neodoo doctor --path ~/odoo_projects/project_name

# Export full project state for debugging
./scripts/dev/export_agent_brief.sh ~/odoo_projects/project_name
```

### Error Message Patterns
| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `Found deprecated <tree> tag` | Using Odoo 17 XML syntax | Replace with `<list>` |
| `Missing required manifest key` | Incomplete `__manifest__.py` | Add `version`, `category`, `license`, etc. |
| `Model must have _description` | Python model missing field | Add `_description = 'Model Name'` |
| `Module prefix violation` | Corporate plugin rule | Add company prefix (e.g., `acme_my_model`) |
| `Port 8069 already in use` | Another Odoo instance running | Stop other instance or use `--odoo-port` |

## Quick Reference Commands

### Project Lifecycle
```bash
# Create new project (interactive)
./neodoo create

# Create with specific template (non-interactive)
./neodoo create --name my_project --template advanced --base-dir ~/odoo_projects

# List existing projects
./neodoo list

# Delete project (with confirmation)
./neodoo delete --name my_project

# Update project dependencies
./neodoo update --path ~/odoo_projects/my_project
```

### Validation Workflow
```bash
# Full validation pipeline (run before every commit)
python framework/validator/validate.py custom_addons/ --strict --auto-fix
python framework/validator/validate.py custom_addons/ --plugins-dir corporate_plugins --strict

# Single module validation
python framework/validator/validate.py custom_addons/my_module --strict

# List available plugins
python framework/validator/validate.py --list-plugins
```

### Migration & Health Checks
```bash
# Analyze migration from Odoo 17
./neodoo migrate custom_addons/my_module --from-version 17

# Environment health check
./neodoo doctor --path ~/odoo_projects/my_project

# Generate AI agent brief
./scripts/dev/export_agent_brief.sh ~/odoo_projects/my_project
```

### Development Shortcuts
```bash
# Start Odoo server (from project directory)
./run.sh

# Or manually
source .venv/bin/activate
python3 odoo_source/odoo-bin -c odoo.conf

# VSCode: Ctrl+Shift+B (runs "Neodoo: Open Interactive Menu")
```

### Key File Locations
- **CLI entry**: `framework/cli/neodoo.py`
- **Core validator**: `framework/validator/validate.py`
- **Plugin base**: `framework/validator/plugin.py`
- **Templates**: `templates/minimal/`, `templates/advanced/`, `templates/ecommerce/`
- **Corporate plugins**: `corporate_plugins/acme_corporate_rules.py`, `corporate_plugins/neo_sempre_rules.py`
- **Migration rules**: `framework/migration/rules.py`
- **VSCode tasks**: `.vscode/tasks.json`

````

`````

````
