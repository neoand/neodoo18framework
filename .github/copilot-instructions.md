# Neodoo18Framework - AI Coding Agent Instructions# Neodoo18Framework - AI Coding Agent Instructions



## Architecture Overview## Architecture Overview



This is an **Odoo 18+ development framework** with LLM-first design that scaffolds complete projects and enforces modern patterns.This is an **Odoo 18+ development framework** with LLM-first design. The framework enforces modern Odoo 18+ standards and provides templates, validators, and generators for rapid development.



### Key Components### Key Components

- `framework/` - Core tools, standards, and LLM guidance- `framework/` - Core tools, standards, and LLM guidance

  - `cli/neodoo.py` - Unified CLI for project management  - `validator/` - Odoo 18+ validation tools

  - `generator/create_project.py` - Creates modules from templates    - `generator/` - Project generation tools

  - `validator/validate.py` - Checks and auto-fixes Odoo 18+ compliance  - `standards/` - Odoo 18+ compliance standards (includes SOIL)

  - `standards/ODOO18_CORE_STANDARDS.md` - Non-negotiable rules  - `roles/` - Role definitions for LLM agents

  - `standards/SOIL_CORE.md` - LLM workflow and checklist- `templates/` - Project boilerplates by type

  - `roles/` - Role-specific guidance for different development areas  - `minimal/` - Basic project structure

- `templates/` - Project scaffolds: `minimal`, `advanced`, `ecommerce` (+ `-project` variants)  ## Neodoo18Framework – Copilot Instructions (Odoo 18+)



## Essential Reading (Do This First)  Purpose: This repo scaffolds complete Odoo 18+ projects and enforces modern patterns with a generator, validator, and templates. Follow these rules to be productive fast.

1. Read `framework/standards/ODOO18_CORE_STANDARDS.md` - Critical Odoo 18+ patterns

2. Scan `framework/standards/SOIL_CORE.md` - LLM-specific workflow guidance  Big picture

  - framework/: tools and standards for LLMs and devs

## Core Workflows    - generator/create_project.py: creates modules from templates

    - validator/validate.py: checks and auto-fixes Odoo 18+ rules

### Project Creation    - standards/: Odoo 18 core rules and SOIL guidance

```bash  - templates/: minimal, advanced, ecommerce (+ “-project” variants)

# Preferred: New unified CLI  - setup.sh, quick-start.sh: interactive or fast project creation

./neodoo create                                    # Interactive wizard

./neodoo create --from-config .neodoo.yml        # Non-interactive from config  Start here (read once)

./neodoo list                                     # List existing projects  - standards/ODOO18_CORE_STANDARDS.md (non‑negotiable rules)

./neodoo doctor --path /project                   # Health check  - standards/SOIL_CORE.md (LLM workflow and checklist)



# Legacy (still works)  Core workflows

python framework/generator/create_project.py --name my_module --type minimal  - Create module: python framework/generator/create_project.py --name my_module --type minimal

./quick-start.sh                                  # Fast defaults  - Full project: ./setup.sh create (guided) or ./quick-start.sh (defaults)

```  - Validate (always): python framework/validator/validate.py <path> --auto-fix

  - Strict mode: add --strict to promote key warnings to errors (e.g., missing data files, bad access.csv header, debug prints)

### Validation (Always Required)

```bash  Try it (quick start)

# Auto-fix most issues  - Minimal module + validate:

python framework/validator/validate.py <path> --auto-fix --verbose    - python framework/generator/create_project.py --name inventory_system --type minimal

    - python framework/validator/validate.py inventory_system --auto-fix --verbose

# Strict mode (promotes warnings to errors)    - python framework/validator/validate.py inventory_system --strict  # stricter rules

python framework/validator/validate.py <path> --strict  - Full project, then validate custom_addons:

```    - ./setup.sh create

    - python framework/validator/validate.py "$HOME/odoo_projects/<seu_projeto>/custom_addons" --auto-fix

## Critical Odoo 18 Rules (Auto-fixed by Validator)

  Enforced Odoo 18 rules (validator auto-fixes most)

### XML Views - Never Use Legacy Patterns  - XML: use <list> (never <tree>); actions: view_mode="list,form"

```xml  - Python: ensure # -*- coding: utf-8 -*-; computed methods need @api.depends

<!-- ✅ CORRECT: Odoo 18+ -->  - Models: include _description; typical mixins: mail.thread, mail.activity.mixin

<list string="Items">                    <!-- Always <list>, never <tree> -->  - Security: every module must include security/ir.model.access.csv

  <field name="name"/>

</list>  Concrete patterns in this repo

  - XML list view: templates/advanced/views/views.xml uses <list> and action view_mode="list,form"

<field name="view_mode">list,form</field>  <!-- Always list,form, never tree,form -->  - Model: templates/advanced/models/template_model.py shows logging, mixins, actions, depends

  - Manifest: version ‘18.0.1.0.0’; see templates/*/__manifest__.py

<!-- ❌ WRONG: Legacy patterns -->  - Access: templates/advanced/security/ir.model.access.csv has base.group_user example

<tree string="Items">                    <!-- DEPRECATED -->

<field name="view_mode">tree,form</field> <!-- DEPRECATED -->  Generator facts (be precise)

```  - Types: minimal, advanced, ecommerce (also "*-project" folders)

  - Replaces placeholders across .py, .xml, .csv, .md, .rst, .txt by default; flags: --dry-run and --no-all-placeholders (default replaces all)

### Python Models - Required Structure

```python  Project layout produced by templates

# -*- coding: utf-8 -*-              # Required UTF-8 header  my_module/

class MyModel(models.Model):    __init__.py, __manifest__.py, models/, views/, security/, (demo/, wizard/, report/ where applicable)

    _name = 'my.model'

    _description = 'My Model'         # Required _description  Acceptance for AI-generated changes

    _inherit = ['mail.thread', 'mail.activity.mixin']  # Common pattern  - Run validator with --auto-fix and ensure it passes (no errors)

      - No <tree> anywhere; all actions use list,form; access CSV present

    @api.depends('field_name')        # Required for computed fields  - Python files have UTF‑8 header; computed fields have @api.depends; models have _description

    def _compute_something(self):

        pass  Tip: Created full projects include run.sh and Odoo/OCA sources (via setup.sh). For details and options, see README.md and docs/ (en/pt/es).

```

  New unified CLI (preferred)

### Manifest - Standard Template  - Create project (wizard): ./neodoo create

```python  - Create from config: ./neodoo create --from-config /path/to/.neodoo.yml

{  - List/Delete: ./neodoo list | ./neodoo delete

    'name': 'Module Name',  - Doctor (env+project health): ./neodoo doctor [--path /project]

    'version': '18.0.1.0.0',          # Always 18.0.x.x.x  - Update repos+deps: ./neodoo update --path /project
    'depends': ['base', 'mail'],       # Common base dependencies
    'data': [
        'security/ir.model.access.csv', # Required security file
        'views/module_views.xml',
    ],
    'license': 'LGPL-3',              # Standard license
}
```

## Template System Usage

### Generator Patterns
- Template types: `minimal`, `advanced`, `ecommerce` 
- Fallback: `minimal-project`, `advanced-project` variants exist
- Placeholder replacement: `{{MODULE_NAME}}`, `{{MODULE_TECHNICAL_NAME}}`, etc.
- Default extensions: `.py`, `.xml`, `.csv`, `.md`, `.rst`, `.txt`

### Project Structure Generated
```
my_module/
├── __init__.py, __manifest__.py
├── models/              # Business logic
├── views/               # XML views and menus  
├── security/            # Access control (required)
├── demo/                # Sample data (optional)
└── wizard/              # Transient models (optional)
```

## Key File References
- Working XML patterns: `templates/*/views/*.xml` 
- Model examples: `templates/*/models/*.py`
- Security templates: `templates/*/security/ir.model.access.csv`
- Complete project config: Check generated `.neodoo.yml` files

## Validation Acceptance Criteria
Before considering any code complete, ensure:
- Validator passes with `--auto-fix` (no errors)
- Strict mode passes with `--strict` (production-ready)
- No `<tree>` tags anywhere in XML
- All actions use `view_mode="list,form"`
- Python files have UTF-8 headers
- All models have `_description` field
- Security access file exists and is properly formatted