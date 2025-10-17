# 🤖 LLM START HERE - Neodoo18Framework v2.0

> **Single Entry Point for AI Assistants and Large Language Models**
>
> This document provides the **fastest path** to accomplish any task in the Neodoo18Framework.

---

## 🎯 What's Your Task?

**Click the task that matches your goal:**

### 📦 Project Creation & Setup

#### → **Create a new Odoo 18+ project from scratch**
- **Read First:** [SOIL_CORE.md](framework/standards/SOIL_CORE.md) (5 min)
- **CLI Command:** `./neodoo create` (interactive wizard)
- **Template:** [templates/minimal/](templates/minimal/) for basic, [templates/production/](templates/production/) for enterprise
- **Token Budget:** ~800 tokens
- **Expected Result:** Complete Odoo 18+ environment ready to run

#### → **Create a single custom module**
- **Read First:** [SOIL_CORE.md lines 22-45](framework/standards/SOIL_CORE.md#padrões-obrigatórios)
- **Reference Example:** [examples/basic/demo_project/](examples/basic/demo_project/)
- **Validation:** `python framework/validator/validate.py my_module/`
- **Token Budget:** ~500 tokens

---

### 🔄 Migration & Upgrades

#### → **Migrate module from Odoo 17 to 18**
- **Read First:** [knowledge/guides/migration_guide.md](knowledge/guides/migration_guide.md) (15 min)
- **Reference:** [knowledge/reference/api_changes.md](knowledge/reference/api_changes.md)
- **CLI Tool:** `./neodoo migrate /path/to/module --from-version 17`
- **Token Budget:** ~2000 tokens
- **Key Changes:** `<tree>` → `<list>`, field API changes, OWL 1 → OWL 2

#### → **Migrate from Odoo 15 or 16**
- **Read First:** [knowledge/guides/migration_guide.md#migração-15-16](knowledge/guides/migration_guide.md)
- **Multiple Steps:** 15→16→17→18 (guide covers all)
- **Token Budget:** ~3000 tokens

---

### 🏗️ Development Tasks

#### → **Create a Python model**
- **Quick Template:** [SOIL_CORE.md lines 34-45](framework/standards/SOIL_CORE.md#python-models)
- **Basic Example:** [examples/basic/demo_project/models/template_model.py](examples/basic/demo_project/models/template_model.py)
- **Advanced Example:** [examples/advanced/complete_module/models/model_complete_example.py](examples/advanced/complete_module/models/model_complete_example.py) (1334 lines, all patterns)
- **Must Read:** `@api.depends` is REQUIRED for computed fields
- **Token Budget:** 500 (simple) | 1500 (advanced)

#### → **Create XML views (List, Form, Search)**
- **Rules:** ALWAYS use `<list>` NEVER `<tree>`
- **Quick Reference:** [SOIL_CORE.md lines 49-54](framework/standards/SOIL_CORE.md#xml-views)
- **Basic Example:** [examples/basic/demo_project/views/](examples/basic/demo_project/views/)
- **Advanced Example:** [examples/advanced/complete_module/views/](examples/advanced/complete_module/views/) (5 view types)
- **Token Budget:** ~700 tokens

#### → **Create OWL 2.0 component (JavaScript)**
- **Read First:** [knowledge/owl/owl_notes.md](knowledge/owl/owl_notes.md) (comprehensive guide)
- **Basic Example:** [examples/advanced/complete_module/static/src/js/component_basic_example.js](examples/advanced/complete_module/static/src/js/component_basic_example.js)
- **Advanced Example:** [examples/advanced/complete_module/static/src/js/component_advanced_example.js](examples/advanced/complete_module/static/src/js/component_advanced_example.js)
- **OWL Version Check:** [knowledge/owl/owl_version_check.md](knowledge/owl/owl_version_check.md)
- **Token Budget:** ~1200 tokens

#### → **Implement workflow / state machine**
- **Guide:** [knowledge/guides/workflow_state_machine.md](knowledge/guides/workflow_state_machine.md)
- **Example:** [examples/advanced/complete_module/models/model_complete_example.py lines 120-180](examples/advanced/complete_module/models/model_complete_example.py)
- **Pattern:** Selection field + button actions + `@api.depends`
- **Token Budget:** ~1000 tokens

#### → **Create security rules (access rights, record rules)**
- **Must Have:** Every model MUST have `ir.model.access.csv`
- **Reference:** [examples/advanced/complete_module/security/](examples/advanced/complete_module/security/)
- **Best Practices:** [knowledge/guides/best_practices.md#security](knowledge/guides/best_practices.md)
- **Token Budget:** ~600 tokens

#### → **Create reports (QWeb, PDF, Excel)**
- **QWeb Report:** [examples/advanced/complete_module/reports/qweb_report_example.xml](examples/advanced/complete_module/reports/qweb_report_example.xml)
- **Excel Report:** [examples/advanced/complete_module/reports/excel_report_example.py](examples/advanced/complete_module/reports/excel_report_example.py)
- **Templates:** [examples/advanced/complete_module/reports/report_template_example.xml](examples/advanced/complete_module/reports/report_template_example.xml)
- **Token Budget:** ~1000 tokens

#### → **Create wizard**
- **Example:** [examples/advanced/complete_module/wizards/wizard_example.py](examples/advanced/complete_module/wizards/wizard_example.py)
- **Pattern:** TransientModel + action methods
- **Token Budget:** ~800 tokens

#### → **Write tests (unit, integration, UI)**
- **Examples:** [examples/advanced/complete_module/tests/](examples/advanced/complete_module/tests/)
- **Unit Tests:** [test_model.py](examples/advanced/complete_module/tests/test_model.py)
- **UI Tests:** [test_ui.py](examples/advanced/complete_module/tests/test_ui.py)
- **Performance:** [test_performance.py](examples/advanced/complete_module/tests/test_performance.py)
- **Token Budget:** ~900 tokens

---

### 🔌 Integration & APIs

#### → **Integrate external API (REST, SOAP, GraphQL)**
- **Complete Guide:** [knowledge/guides/external_api_integration.md](knowledge/guides/external_api_integration.md)
- **Patterns:** Authentication, error handling, rate limiting
- **Token Budget:** ~1500 tokens

#### → **Create HTTP controller / route**
- **Example:** [examples/advanced/complete_module/controllers/controller_example.py](examples/advanced/complete_module/controllers/controller_example.py)
- **Token Budget:** ~700 tokens

---

### 🐛 Debugging & Troubleshooting

#### → **Fix common Odoo 18 errors**
- **Troubleshooting Guide:** [knowledge/reference/common_issues.md](knowledge/reference/common_issues.md)
- **Validation:** Run `python framework/validator/validate.py --strict`
- **Most Common Issues:**
  - Using `<tree>` instead of `<list>`
  - Missing `@api.depends` on computed fields
  - Missing security files
  - Wrong encoding headers

#### → **Validate module compliance**
- **Tool:** `python framework/validator/validate.py /path/to/module/ --strict`
- **Auto-fix:** Add `--auto-fix` flag when possible
- **Corporate Rules:** Check `corporate_plugins/` for custom rules

---

### 📚 Learning & Reference

#### → **Learn Odoo 18+ best practices**
- **Main Guide:** [knowledge/guides/best_practices.md](knowledge/guides/best_practices.md)
- **Core Standards:** [framework/standards/ODOO18_CORE_STANDARDS.md](framework/standards/ODOO18_CORE_STANDARDS.md)
- **Quick Cheatsheet:** [knowledge/guides/cheatsheet.md](knowledge/guides/cheatsheet.md)

#### → **Understand what changed in Odoo 18**
- **API Changes:** [knowledge/reference/api_changes.md](knowledge/reference/api_changes.md)
- **View Syntax:** [knowledge/reference/view_syntax.md](knowledge/reference/view_syntax.md)
- **Python Tips:** [knowledge/reference/tips_python_odoo18.md](knowledge/reference/tips_python_odoo18.md)

---

## 🎭 Choose Your Role

**Different roles have different focus areas. Choose yours:**

### Development Roles
- **[Backend Developer](framework/roles/BACKEND_DEVELOPER.md)** - Python models, business logic, workflows
- **[OWL Specialist](framework/roles/OWL_SPECIALIST.md)** - Frontend components, JavaScript, UI interactions
- **[Full Stack Developer](framework/roles/)** - Both backend + frontend

### Specialized Roles
- **[Integration Specialist](framework/roles/INTEGRATION_SPECIALIST.md)** - APIs, external systems, webhooks
- **[Data Migration Specialist](framework/roles/DATA_MIGRATION_SPECIALIST.md)** - Data import/export, ETL, migration scripts
- **[Security Expert](framework/roles/SECURITY_EXPERT.md)** - Access control, encryption, security audits
- **[DevOps Engineer](framework/roles/DEVOPS_ENGINEER.md)** - Deployment, CI/CD, infrastructure

### Business & Design
- **[Business Analyst](framework/roles/BUSINESS_ANALYST.md)** - Requirements analysis, process design
- **[UX/UI Designer](framework/roles/UXUI_DESIGNER.md)** - User experience, interface design

### Management
- **[Project Manager](framework/roles/PROJECT_MANAGER.md)** - Project planning, team coordination

**Don't know which role?** → See [ROLE_SELECTOR.md](ROLE_SELECTOR.md) for task-to-role mapping

---

## 📖 Full Documentation Index

### Essential Docs (Read These First)
1. **[SOIL_CORE.md](framework/standards/SOIL_CORE.md)** - LLM orientation system ⭐
2. **[ODOO18_CORE_STANDARDS.md](framework/standards/ODOO18_CORE_STANDARDS.md)** - Odoo 18+ standards ⭐
3. **[README.md](README.md)** - Framework overview and quick start

### Navigation & Organization
- **[NAVIGATION_MAP.md](NAVIGATION_MAP.md)** - Complete hierarchical map of all resources
- **[CANONICAL_SOURCES.md](CANONICAL_SOURCES.md)** - Definitive list of canonical vs duplicate files
- **[LLM_FRIENDLINESS_ANALYSIS.md](LLM_FRIENDLINESS_ANALYSIS.md)** - Framework analysis for LLMs

### Knowledge Base (400+ KB, 20 docs, 80+ topics)
- **[knowledge/README.md](knowledge/README.md)** - Knowledge base index
- **Guides:** migration, best practices, workflows, API integration, cheatsheet
- **Reference:** API changes, view syntax, common issues, Python tips
- **OWL:** Complete OWL 2.0 guide, version check

### Examples (15,000+ lines)
- **[examples/basic/](examples/basic/)** - Simple demos for learning
- **[examples/advanced/README.md](examples/advanced/README.md)** - Production-ready examples index
- **[examples/advanced/complete_module/](examples/advanced/complete_module/)** - Full module with all components

### By Language
- **English:** [docs/guides/en/COMPLETE_GUIDE.md](docs/guides/en/COMPLETE_GUIDE.md)
- **Português:** [docs/guides/pt/GUIA_COMPLETO.md](docs/guides/pt/GUIA_COMPLETO.md)
- **Español:** [docs/guides/es/GUIA_COMPLETA.md](docs/guides/es/GUIA_COMPLETA.md)

---

## ⚡ Quick Commands Reference

### CLI Commands
```bash
# Project Management
./neodoo create              # Create new project (interactive)
./neodoo list                # List all projects
./neodoo run my_project      # Run specific project
./neodoo doctor              # Health check

# Migration
./neodoo migrate /path/to/module --from-version 17

# Validation
python framework/validator/validate.py /path/ --strict
python framework/validator/validate.py /path/ --auto-fix

# Generation
python framework/generator/create_project.py --name=my_project --type=minimal
```

### File Structure Quick Reference
```
neodoo18framework/
├── framework/              # Core tools (validator, generator, CLI)
│   ├── standards/          # SOIL_CORE, ODOO18_CORE_STANDARDS
│   ├── roles/              # Role definitions (11 roles)
│   ├── validator/          # Validation engine + plugins
│   └── cli/                # neodoo command
├── knowledge/              # Knowledge base (400+ KB, 20 docs)
│   ├── guides/             # How-to guides (5 files)
│   ├── reference/          # Technical reference (5 files)
│   └── owl/                # OWL 2.0 specific (2 files)
├── examples/               # Code examples
│   ├── basic/              # Simple demos
│   └── advanced/           # Production-ready (36 files, 15k+ lines)
├── templates/              # Project templates
│   ├── minimal/            # Basic module
│   ├── standard/           # Standard module
│   └── production/         # Full enterprise
└── docs/                   # Framework documentation
    └── guides/             # EN, PT, ES guides
```

---

## 🎯 Decision Tree: What to Read

```
START
  │
  ├─ Never used framework before?
  │    → Read README.md (5 min)
  │    → Read SOIL_CORE.md (5 min)
  │    → Try: ./neodoo create
  │
  ├─ Need to create something new?
  │    ├─ Simple module → examples/basic/ + SOIL_CORE.md
  │    ├─ Complex module → examples/advanced/ + best_practices.md
  │    └─ Specific feature → Search in "What's Your Task?" above
  │
  ├─ Need to migrate?
  │    → knowledge/guides/migration_guide.md
  │    → knowledge/reference/api_changes.md
  │
  ├─ Having errors?
  │    ├─ Run validator first → python framework/validator/validate.py
  │    └─ Check common_issues.md
  │
  └─ Learning / Reference?
       ├─ Best practices → knowledge/guides/best_practices.md
       ├─ Quick lookup → knowledge/guides/cheatsheet.md
       └─ Deep dive → knowledge/ (full knowledge base)
```

---

## 🚨 Critical Rules (NEVER Violate)

### XML Views
- ✅ **ALWAYS** use `<list>` for list views
- ❌ **NEVER** use `<tree>` (deprecated in Odoo 18+)
- ✅ **ALWAYS** use `view_mode="list,form"`
- ❌ **NEVER** use `view_mode="tree,form"`

### Python Models
- ✅ **ALWAYS** include `# -*- coding: utf-8 -*-` header
- ✅ **ALWAYS** use `@api.depends()` on computed fields
- ✅ **ALWAYS** include `_description` attribute
- ✅ **ALWAYS** create `ir.model.access.csv` for security

### Validation
- ✅ **ALWAYS** run validator before completing task
- ✅ **ALWAYS** fix all errors and warnings
- ✅ **NEVER** ignore security warnings

**Full rules:** [SOIL_CORE.md#regras-invioláveis](framework/standards/SOIL_CORE.md#🛡️-regras-invioláveis)

---

## 💡 Pro Tips for LLMs

### Token Efficiency
- **Use progressive reading:** Start with SOIL_CORE.md, expand as needed
- **Reference examples by path:** `examples/advanced/.../model.py:45-60` (specific lines)
- **Leverage validator:** Let it find issues instead of reading all standards

### Context Optimization
- **For simple tasks (<500 tokens):** SOIL_CORE.md + basic example
- **For complex tasks (500-1500 tokens):** + best_practices.md + advanced example
- **For migrations (1500+ tokens):** + migration_guide.md + api_changes.md

### Accuracy Boosters
1. **Always validate** with `framework/validator/validate.py`
2. **Copy working patterns** from examples/ (don't reinvent)
3. **Check common_issues.md** if something doesn't work
4. **Use --strict mode** for production code

---

## 📞 Need Help?

### Troubleshooting Steps
1. **Run validator:** `python framework/validator/validate.py /path/ --strict`
2. **Check common issues:** [knowledge/reference/common_issues.md](knowledge/reference/common_issues.md)
3. **Review role docs:** Your [role document](framework/roles/) may have specific guidance
4. **Search knowledge base:** [knowledge/README.md](knowledge/README.md) has comprehensive index

### Community & Support
- **GitHub Issues:** [neoand/neodoo18framework/issues](https://github.com/neoand/neodoo18framework/issues)
- **Documentation:** [docs/](docs/) for framework guides
- **Knowledge Base:** [knowledge/](knowledge/) for Odoo-specific help

---

## 🎉 You're Ready!

This framework is designed to make your job **easier and faster**. Key advantages:

- ✅ **Single command setup:** `./neodoo create`
- ✅ **Auto validation:** Catch errors before they happen
- ✅ **Production examples:** 15,000+ lines of real code
- ✅ **Complete docs:** 400+ KB knowledge base
- ✅ **LLM-optimized:** Clear patterns, no ambiguity

**Choose your task above and start building!** 🚀

---

**Document Version:** 1.0 (2025-10-17)

**Framework Version:** v2.0

**Maintained By:** NeoAnd Development Team

**License:** LGPL-3

---

**🤖 Happy Coding!**
