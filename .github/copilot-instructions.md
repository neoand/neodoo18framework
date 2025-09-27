# Neodoo18Framework - AI Coding Agent Instructions

## Architecture Overview

This is an **Odoo 18+ development framework** with LLM-first design. The framework enforces modern Odoo 18+ standards and provides templates, validators, and generators for rapid development.

### Key Components
- `framework/` - Core tools, standards, and LLM guidance
  - `validator/` - Odoo 18+ validation tools
  - `generator/` - Project generation tools
  - `standards/` - Odoo 18+ compliance standards (includes SOIL)
  - `roles/` - Role definitions for LLM agents
- `templates/` - Project boilerplates by type
  - `minimal/` - Basic project structure
  ## Neodoo18Framework – Copilot Instructions (Odoo 18+)

  Purpose: This repo scaffolds complete Odoo 18+ projects and enforces modern patterns with a generator, validator, and templates. Follow these rules to be productive fast.

  Big picture
  - framework/: tools and standards for LLMs and devs
    - generator/create_project.py: creates modules from templates
    - validator/validate.py: checks and auto-fixes Odoo 18+ rules
    - standards/: Odoo 18 core rules and SOIL guidance
  - templates/: minimal, advanced, ecommerce (+ “-project” variants)
  - setup.sh, quick-start.sh: interactive or fast project creation

  Start here (read once)
  - standards/ODOO18_CORE_STANDARDS.md (non‑negotiable rules)
  - standards/SOIL_CORE.md (LLM workflow and checklist)

  Core workflows
  - Create module: python framework/generator/create_project.py --name my_module --type minimal
  - Full project: ./setup.sh create (guided) or ./quick-start.sh (defaults)
  - Validate (always): python framework/validator/validate.py <path> --auto-fix
  - Strict mode: add --strict to promote key warnings to errors (e.g., missing data files, bad access.csv header, debug prints)

  Try it (quick start)
  - Minimal module + validate:
    - python framework/generator/create_project.py --name inventory_system --type minimal
    - python framework/validator/validate.py inventory_system --auto-fix --verbose
    - python framework/validator/validate.py inventory_system --strict  # stricter rules
  - Full project, then validate custom_addons:
    - ./setup.sh create
    - python framework/validator/validate.py "$HOME/odoo_projects/<seu_projeto>/custom_addons" --auto-fix

  Enforced Odoo 18 rules (validator auto-fixes most)
  - XML: use <list> (never <tree>); actions: view_mode="list,form"
  - Python: ensure # -*- coding: utf-8 -*-; computed methods need @api.depends
  - Models: include _description; typical mixins: mail.thread, mail.activity.mixin
  - Security: every module must include security/ir.model.access.csv

  Concrete patterns in this repo
  - XML list view: templates/advanced/views/views.xml uses <list> and action view_mode="list,form"
  - Model: templates/advanced/models/template_model.py shows logging, mixins, actions, depends
  - Manifest: version ‘18.0.1.0.0’; see templates/*/__manifest__.py
  - Access: templates/advanced/security/ir.model.access.csv has base.group_user example

  Generator facts (be precise)
  - Types: minimal, advanced, ecommerce (also "*-project" folders)
  - Replaces placeholders across .py, .xml, .csv, .md, .rst, .txt by default; flags: --dry-run and --no-all-placeholders (default replaces all)

  Project layout produced by templates
  my_module/
    __init__.py, __manifest__.py, models/, views/, security/, (demo/, wizard/, report/ where applicable)

  Acceptance for AI-generated changes
  - Run validator with --auto-fix and ensure it passes (no errors)
  - No <tree> anywhere; all actions use list,form; access CSV present
  - Python files have UTF‑8 header; computed fields have @api.depends; models have _description

  Tip: Created full projects include run.sh and Odoo/OCA sources (via setup.sh). For details and options, see README.md and docs/ (en/pt/es).

  New unified CLI (preferred)
  - Create project (wizard): ./neodoo create
  - Create from config: ./neodoo create --from-config /path/to/.neodoo.yml
  - List/Delete: ./neodoo list | ./neodoo delete
  - Doctor (env+project health): ./neodoo doctor [--path /project]
  - Update repos+deps: ./neodoo update --path /project