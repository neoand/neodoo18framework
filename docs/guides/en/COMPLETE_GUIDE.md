# 🚀 Complete Guide: Neodoo18Framework

> Universal Odoo 18+ development framework with SOIL and a one-command CLI.

## 📚 Table of Contents

1. Quick Start (recommended)
2. Project Anatomy
3. Core Workflows (create, manage, validate)
4. Standards You Must Follow (Odoo 18+)
5. Validator Modes: strict and template-mode
6. AI Development (LLM-friendly)
7. Update and Doctor
8. Troubleshooting and Checklist

---

## ⚡ Quick Start (30 seconds)

> [!tip]
> The new CLI is the fastest way. Legacy scripts still exist, but the CLI gives you the best UX.

```bash
# 1) Clone
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# 2) Create a full Odoo 18+ project (wizard)
./neodoo create

# 3) Start it
cd ~/odoo_projects/<your_project>
./run.sh
```

Non-interactive (reproducible) from config:
```bash
./neodoo create --from-config /path/to/.neodoo.yml
```

Minimal .neodoo.yml example
```yaml
version: 1
name: my_odoo18_project
base_dir: ~/odoo_projects
module: my_module
template: minimal
venv: true
odoo_branch: 18.0
```

You can also use the shared example directly:
```bash
./neodoo create --from-config ./docs/.neodoo.yml
```

> [!note]
> The CLI scaffolds: Odoo source, OCA/web, custom_addons, venv (optional), odoo.conf, and run.sh.

---

## 🏗 Project Anatomy

```
~/odoo_projects/your_project/
├── odoo_source/           # Odoo 18+ source (git clone)
├── community_addons/      # OCA modules (web included)
│   └── web/
├── custom_addons/         # Your modules
├── .venv/                 # Isolated Python env (optional)
├── odoo.conf              # Preconfigured for dev
├── run.sh                 # Start Odoo
└── .neodoo.yml            # Project config (for reproducible create)
```

> [!example]
> Run the validator on your custom modules directory:
> 
> ```bash
> python framework/validator/validate.py ~/odoo_projects/your_project/custom_addons --strict --auto-fix
> ```

---

## 🔁 Core Workflows

Create
```bash
./neodoo create                    # wizard
./neodoo create --from-config .neodoo.yml  # reproducible
```

Manage
```bash
./neodoo list
./neodoo delete
./neodoo run                       # run project in current directory
./neodoo run --path /path/to/project  # run specific project
./neodoo doctor                    # check env (python, git, ports)
./neodoo doctor --path /path/to/project
./neodoo update --path /path/to/project  # pull repos + update deps
```

Validate (Odoo 18+ compliance)
```bash
# From repo root
python framework/validator/validate.py path/to/module --strict --auto-fix
python framework/validator/validate.py templates/minimal --template-mode --auto-fix
```

---

## 📏 Standards You Must Follow (Odoo 18+)

> [!warning]
> Never use <tree>. Always use <list>. Actions must declare view_mode="list,form".

XML (correct)
```xml
<record id="book_view_list" model="ir.ui.view">
  <field name="name">book.view.list</field>
  <field name="model">bjj.book</field>
  <field name="arch" type="xml">
    <list string="Books">
      <field name="title"/>
      <field name="author"/>
    </list>
  </field>
  </record>

<record id="book_action" model="ir.actions.act_window">
  <field name="name">Books</field>
  <field name="res_model">bjj.book</field>
  <field name="view_mode">list,form</field>
</record>
```

Python (model basics)
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Book(models.Model):
    _name = 'bjj.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char(required=True, tracking=True)
    author = fields.Char(required=True)
    isbn = fields.Char(size=13)

    @api.constrains('isbn')
    def _check_isbn(self):
        for rec in self:
            if rec.isbn and len(rec.isbn) != 13:
                raise ValidationError(_('ISBN must have 13 digits'))
```

---

## 🧪 Validator Modes

> [!info]
> strict: promotes certain warnings to errors for user projects.
> 
> template-mode: keeps cosmetic/template placeholders as warnings for templates, while keeping essential Odoo 18+ rules as errors.

Examples
```bash
# Strict (recommended for real modules)
python framework/validator/validate.py my_module --strict --auto-fix

# Template (permissive for placeholders)
python framework/validator/validate.py templates/advanced --template-mode --auto-fix
```

---

## 🤖 AI Development

> [!tip]
> Start here: framework/standards/ODOO18_CORE_STANDARDS.md and framework/standards/SOIL_CORE.md.

Context
```bash
cat framework/standards/ODOO18_CORE_STANDARDS.md
cat framework/standards/SOIL_CORE.md
```

LLM prompt starter
```
Build a Library module following Odoo 18+ rules:
- Model: bjj.book (title, author, isbn, category)
- Views: list + form (no tree)
- Action: view_mode="list,form"
- Security: base access + access.csv
Then run: python framework/validator/validate.py <path> --strict --auto-fix
```

---

## � Update and 🩺 Doctor

```bash
./neodoo doctor                    # check python3, git, docker/psql presence, and ports 8069/8072
./neodoo doctor --path /project    # also checks odoo_source, addons folders, venv

./neodoo update --path /project    # git pull Odoo + OCA/web and update venv deps
```

> [!success]
> Use doctor before starting, and after updates, to catch port conflicts and missing tools early.

---

## � CI & Sanity Checks

This repository includes automated checks to keep the developer experience solid:

- Fast checks (CI, on push/PR):
  - Lists generator templates
  - Generates a minimal module (offline)
  - Validates the generated module with the validator in strict mode

- Smoke test (manual):
  - Trigger the "CI" workflow with "Run workflow" (workflow_dispatch)
  - Runs `scripts/dev/quick_sanity.sh` which performs a full end-to-end flow (clones Odoo and OCA/web)

Local quick sanity run:

```bash
# From repo root
bash scripts/dev/quick_sanity.sh

# Or step-by-step
python3 framework/generator/create_project.py --name tmp --list-templates
./neodoo create --name sanity_proj --base-dir /tmp/neodoo_sanity --module sanity_mod --template minimal --no-venv
./neodoo doctor --path /tmp/neodoo_sanity/sanity_proj
python3 framework/validator/validate.py /tmp/neodoo_sanity/sanity_proj/custom_addons/sanity_mod --strict --auto-fix
```

Notes:
- The "minimal" template generates a module that passes strict validation by default.
- Filenames containing placeholders are automatically renamed during generation.

---

## 🔎 OCA Watch & Weekly Rollups

Stay up-to-date with the OCA ecosystem directly from this repo:

- Daily digests: The “OCA Watch” workflow monitors selected OCA repositories and writes concise digests under `docs/oca-digests/`. When changes are detected, it opens a PR labeled and assigned automatically, with auto-merge enabled.
- Weekly rollups: Every Monday (03:00 UTC), the “OCA Weekly Rollup” workflow aggregates the last 7 days into `docs/oca-digests/rollups/YYYY-Www.md`.

Manual triggers:
- From the GitHub Actions tab, run “OCA Watch” (optionally with bootstrap on the first run) or “OCA Weekly Rollup”.

Learn more: see `docs/oca-digests/README.md`.

---

## �🧯 Troubleshooting

> [!failure] Invalid view mode 'tree'
```bash
python framework/validator/validate.py my_module --auto-fix
```

> [!question] Module not found
```bash
ls my_module/__init__.py
cat my_module/models/__init__.py  # ensure imports exist
```

> [!warning] Access rights
```bash
ls my_module/security/
grep "group_" my_module/security/*.xml || true
```

---

## ✅ Quality Checklist

- [ ] Validator passes (strict) with 0 errors
- [ ] XML uses <list>, actions use "list,form"
- [ ] Models have _description and sensible constraints
- [ ] Security: ir.model.access.csv present and listed in manifest
- [ ] README and minimal tests present

> [!tip]
> For templates, validate with --template-mode to avoid placeholder noise while still catching real issues.

---

## 🚀 **ADVANCED COMMANDS**

### Project Analysis:
```bash
# Detailed statistics
python3 framework/analyzer.py my_project/

# Dependencies
python3 framework/dependency_checker.py my_project/

# Auto documentation
python3 framework/doc_generator.py my_project/
```

### Specific Generation:
```bash
# Create specific model
python3 generator/create_model.py --name="Product" --fields="name:char,price:float"

# Create views for model
python3 generator/create_views.py --model="product" --views="list,form,kanban"

# Create wizard
python3 generator/create_wizard.py --name="ImportProducts"
```

---

## 📚 **ADDITIONAL RESOURCES**

### Technical Documentation:
- **SOIL_CORE.md**: LLM guide
- **STANDARDS.md**: Odoo 18+ standards  
- **templates/**: Ready examples
- **framework/**: Development tools

### Community:
- **GitHub**: https://github.com/neoand/neodoo18framework
- **Issues**: Report bugs and suggestions  
- **Pull Requests**: Contributions always welcome
- **Discussions**: Community help and tips

### Support:
- **Wiki**: Advanced use cases
- **Examples**: Example projects  
- **Updates**: Framework always updated

---

## 🎯 **CONCLUSION**

**Neodoo18Framework** transforms Odoo development from **weeks to minutes**:

✅ **Battle-Tested Templates** - Production-validated patterns  
✅ **100% Odoo 18+ Compliance** - No compatibility errors  
✅ **Automated Validation** - Enterprise quality guaranteed  
✅ **AI-Friendly** - SOIL system optimized for LLMs  
✅ **Open Source** - MIT License, total freedom  

**🚀 Start coding now!**

```bash
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework  
./quick-start.sh amazing_project
python3 framework/validator.py amazing_project/
# 100% = Ready for production! 🎉
```

---

**Happy Coding! 🎯**