# 🗺️ NAVIGATION MAP - Neodoo18Framework v2.0

> **Complete Hierarchical Map of All Resources**
>
> Navigate the framework like a pro. Every file, every tool, every doc - organized and explained.

---

## 📍 You Are Here

```
neodoo18framework/ (ROOT)
│
├── 🚀 LLM_START_HERE.md ← START HERE if you're an AI assistant
├── 📖 README.md ← START HERE if you're a human
├── 📊 NAVIGATION_MAP.md ← YOU ARE HERE
└── ... (see full structure below)
```

---

## 🎯 Quick Navigation by Purpose

### I Want To...

| Goal | Primary Resource | Secondary Resources |
|------|------------------|---------------------|
| **Understand the framework** | [README.md](README.md) | [FUSION_GUIDE.md](FUSION_GUIDE.md), [PROJECT_STATUS.md](PROJECT_STATUS.md) |
| **Start as LLM** | [LLM_START_HERE.md](LLM_START_HERE.md) | [SOIL_CORE.md](framework/standards/SOIL_CORE.md) |
| **Create a project** | `./neodoo create` | [templates/](templates/) |
| **Learn Odoo 18+** | [knowledge/README.md](knowledge/README.md) | [best_practices.md](knowledge/guides/best_practices.md) |
| **Migrate from 17** | [migration_guide.md](knowledge/guides/migration_guide.md) | [api_changes.md](knowledge/reference/api_changes.md) |
| **See examples** | [examples/advanced/](examples/advanced/) | [examples/basic/](examples/basic/) |
| **Validate code** | `python framework/validator/validate.py` | [VALIDATOR_BEST_PRACTICES.md](docs/VALIDATOR_BEST_PRACTICES.md) |
| **Understand roles** | [framework/roles/](framework/roles/) | [ROLE_SELECTOR.md](ROLE_SELECTOR.md) *(if exists)* |
| **Troubleshoot** | [common_issues.md](knowledge/reference/common_issues.md) | `./neodoo doctor` |
| **Deploy** | [DEPLOYMENT.md](DEPLOYMENT.md) | [docs/guides/](docs/guides/) |

---

## 📂 Complete Directory Structure

### Level 1: Root Files

```
neodoo18framework/
│
├── 📄 Core Documentation (13 files)
│   ├── README.md ⭐⭐⭐ Main entry point
│   ├── LLM_START_HERE.md ⭐⭐⭐ LLM entry point
│   ├── NAVIGATION_MAP.md ⭐ (this file)
│   ├── CANONICAL_SOURCES.md ⭐ Canonical file index
│   ├── FUSION_GUIDE.md → Framework integration guide
│   ├── PROJECT_STATUS.md → v2.0 status
│   ├── CHANGELOG.md → Version history
│   ├── CHANGELOG_V2.md → v2.0 specific changes
│   ├── DEPLOYMENT.md → Production deployment
│   ├── CONTRIBUTING.md → How to contribute
│   ├── CODE_OF_CONDUCT.md → Community rules
│   ├── SECURITY.md → Security policy
│   └── TODO.md → Roadmap
│
├── 📄 Analysis & References (3 files)
│   ├── LLM_FRIENDLINESS_ANALYSIS.md → LLM usability analysis
│   ├── EXECUTIVE_SUMMARY.md → Executive summary
│   ├── IMPLEMENTATION_GUIDE.md → Implementation details
│   └── VALIDATOR_QUICK_REFERENCE.txt → Quick validator reference
│
├── 📄 Platform Specific (1 file)
│   └── WINDOWS.md → Windows setup instructions
│
├── 🐍 Python Requirements (2 files)
│   ├── requirements.txt → Core dependencies
│   └── requirements-dev.txt → Development dependencies
│
├── 🔧 Scripts (4 files)
│   ├── neodoo ⭐ Main CLI (Linux/macOS)
│   ├── neodoo.bat → Windows batch
│   ├── neodoo.ps1 → Windows PowerShell
│   └── validate_neo_sempre.sh → Corporate validation script
│
├── 📁 Main Directories (8 directories)
│   ├── framework/ ⭐⭐⭐ Core framework tools
│   ├── knowledge/ ⭐⭐⭐ Knowledge base (400+ KB)
│   ├── examples/ ⭐⭐⭐ Code examples (15k+ lines)
│   ├── templates/ ⭐⭐ Project templates
│   ├── docs/ ⭐⭐ Framework documentation
│   ├── corporate_plugins/ → Custom validation rules
│   ├── .github/ → GitHub workflows
│   └── .neodoo/ → Framework state files
```

---

### Level 2: framework/ (Core Tools)

```
framework/
│
├── 📂 standards/ ⭐⭐⭐ (2 files)
│   ├── SOIL_CORE.md ← LLM orientation system (CRITICAL)
│   └── ODOO18_CORE_STANDARDS.md ← Odoo 18+ standards (CRITICAL)
│
├── 📂 roles/ ⭐⭐ (11 files - Role definitions)
│   ├── BACKEND_DEVELOPER.md
│   ├── OWL_SPECIALIST.md
│   ├── INTEGRATION_SPECIALIST.md
│   ├── DATA_MIGRATION_SPECIALIST.md
│   ├── SECURITY_EXPERT.md
│   ├── DEVOPS_ENGINEER.md
│   ├── UXUI_DESIGNER.md
│   ├── BUSINESS_ANALYST.md
│   ├── PROJECT_MANAGER.md
│   ├── FULL_STACK_DEVELOPER.md (if exists)
│   └── README.md (if exists)
│
├── 📂 validator/ ⭐⭐⭐ (Validation engine)
│   ├── validate.py ← Main validator script
│   ├── plugin_manager.py
│   ├── plugin.py
│   ├── __init__.py
│   └── plugins/
│       ├── core.py ← Core validation rules
│       └── __init__.py
│
├── 📂 generator/ ⭐⭐ (Project generation)
│   └── create_project.py ← Project generator
│
├── 📂 migration/ ⭐ (Migration tools)
│   ├── analyzer.py ← Analyze modules for migration
│   ├── cli.py ← Migration CLI
│   ├── data_pipeline.py ← Data migration pipeline
│   ├── rules.py ← Migration rules 17→18
│   └── __init__.py
│
└── 📂 cli/ ⭐⭐⭐ (Command-line interface)
    └── neodoo.py ← Main CLI implementation
```

**Usage Examples:**
```bash
# Validation
python framework/validator/validate.py /path/to/module/ --strict

# Project Generation
python framework/generator/create_project.py --name=my_project

# Migration
python framework/migration/cli.py --source=/path/ --from=17 --to=18
```

---

### Level 2: knowledge/ (Knowledge Base - 400+ KB)

```
knowledge/
│
├── README.md ⭐⭐⭐ Knowledge base index
│
├── 📂 guides/ (5 files - How-to documentation)
│   ├── migration_guide.md ⭐⭐⭐ (40.9 KB) Migrate 15/16/17 → 18
│   ├── best_practices.md ⭐⭐⭐ (35.2 KB) Odoo 18+ best practices
│   ├── workflow_state_machine.md ⭐⭐ (28.5 KB) State machines & workflows
│   ├── external_api_integration.md ⭐⭐ (32.1 KB) API integration patterns
│   └── cheatsheet.md ⭐ (12.3 KB) Quick reference
│
├── 📂 reference/ (5 files - Technical reference)
│   ├── api_changes.md ⭐⭐⭐ (45.6 KB) Complete API changelog
│   ├── view_syntax.md ⭐⭐⭐ (38.4 KB) XML view reference
│   ├── common_issues.md ⭐⭐ (25.7 KB) Troubleshooting
│   ├── tips_python_odoo18.md ⭐⭐ (22.3 KB) Modern Python patterns
│   └── owl_notes.md ⭐⭐⭐ (52.8 KB) OWL 2.0 comprehensive guide
│
└── 📂 owl/ (1 file - OWL specific)
    └── owl_version_check.md ⭐ (8.9 KB) Version compatibility
```

**Reading Recommendations:**
- **Beginners:** Start with `cheatsheet.md`, then `best_practices.md`
- **Migrating:** Read `migration_guide.md` + `api_changes.md`
- **OWL Development:** Read `owl/owl_notes.md` (comprehensive)
- **Troubleshooting:** Check `reference/common_issues.md`

---

### Level 2: examples/ (Code Examples - 15,000+ lines)

```
examples/
│
├── 📂 basic/ ⭐ (Simple demos for learning)
│   ├── demo_project/ ← Basic module structure
│   │   ├── __manifest__.py
│   │   ├── models/
│   │   │   └── template_model.py ← Simple model example
│   │   ├── views/
│   │   │   ├── demo_project_views.xml
│   │   │   └── demo_project_menus.xml
│   │   ├── security/
│   │   │   ├── ir.model.access.csv
│   │   │   └── demo_project_security.xml
│   │   ├── tests/
│   │   └── wizard/
│   │
│   └── library_system/ ← Library management example
│       └── README.md
│
└── 📂 advanced/ ⭐⭐⭐ (Production-ready examples)
    ├── README.md ⭐⭐ Advanced examples index
    │
    └── complete_module/ ⭐⭐⭐ (36 files, 15k+ lines)
        ├── __manifest__.py ← Complete manifest example
        ├── README.md → Module documentation
        ├── INDEX.md → File index
        ├── ESTRUTURA.txt → Structure overview
        ├── ARQUIVOS_CRIADOS.md → Creation log
        ├── RESUMO.md → Summary
        │
        ├── 📂 models/ ⭐⭐⭐ (4 Python files - 5,000+ lines)
        │   ├── model_complete_example.py (1,334 lines)
        │   │   → All patterns: computed fields, constraints,
        │   │      workflows, state machines, methods
        │   ├── model_state_machine.py
        │   ├── model_custom_methods.py
        │   └── res_config_settings_example.py
        │
        ├── 📂 views/ ⭐⭐⭐ (7 XML files - 2,500+ lines)
        │   ├── list_view_example.xml ← List view patterns
        │   ├── form_view_complete_example.xml ← Form with all widgets
        │   ├── kanban_view_example.xml ← Kanban view
        │   ├── search_view_example.xml ← Advanced search
        │   ├── menu_actions.xml ← Menu structure
        │   ├── templates.xml ← QWeb templates
        │   └── manifest_assets.xml ← Asset bundles
        │
        ├── 📂 static/src/js/ ⭐⭐⭐ (4 OWL files - 4,000+ lines)
        │   ├── component_basic_example.js ← Basic OWL component
        │   ├── component_advanced_example.js ← Advanced patterns
        │   ├── component_list_dashboard.js ← Dashboard component
        │   └── registry.js ← Component registry
        │
        ├── 📂 security/ ⭐⭐ (2 files)
        │   ├── ir.model.access.csv ← Access rights
        │   └── record_rules.xml ← Record-level security
        │
        ├── 📂 reports/ ⭐⭐ (3 files - 1,000+ lines)
        │   ├── qweb_report_example.xml ← QWeb report template
        │   ├── report_template_example.xml ← PDF template
        │   └── excel_report_example.py ← Excel generation
        │
        ├── 📂 wizards/ ⭐ (2 files - 600+ lines)
        │   ├── wizard_example.py ← Wizard model
        │   └── (wizard views in views/)
        │
        ├── 📂 tests/ ⭐⭐ (4 files - 1,200+ lines)
        │   ├── test_model.py ← Unit tests
        │   ├── test_ui.py ← UI/integration tests
        │   ├── test_performance.py ← Performance tests
        │   └── (test helpers)
        │
        ├── 📂 data/ (2 files - 400+ lines)
        │   ├── demo_data.xml ← Demo data
        │   ├── automated_actions.xml ← Automated actions
        │   └── scheduled_actions.xml ← Cron jobs
        │
        ├── 📂 controllers/ (1 file - 300+ lines)
        │   └── controller_example.py ← HTTP routes
        │
        └── 📄 Additional Docs (3 files)
            ├── chatter_usage_example.xml
            ├── list_view_example.xml
            └── owl_version_check.md
```

**Example Usage Patterns:**
- **Learn basics:** `examples/basic/demo_project/models/template_model.py`
- **Copy production pattern:** `examples/advanced/complete_module/models/model_complete_example.py`
- **OWL component:** `examples/advanced/complete_module/static/src/js/component_basic_example.js`
- **Security:** `examples/advanced/complete_module/security/`

---

### Level 2: templates/ (Project Templates)

```
templates/
│
├── 📂 minimal/ ⭐ Basic module template
│   ├── README.md
│   ├── __manifest__.py.template
│   ├── models/
│   ├── views/
│   └── security/
│
├── 📂 standard/ ⭐⭐ Standard module template
│   ├── README.md
│   ├── __manifest__.py.template
│   ├── models/
│   ├── views/
│   ├── security/
│   ├── reports/
│   └── tests/
│
├── 📂 production/ ⭐⭐⭐ Enterprise-grade template
│   ├── README.md
│   ├── __manifest__.py.template
│   ├── models/
│   ├── views/
│   ├── security/
│   ├── reports/
│   ├── wizards/
│   ├── controllers/
│   ├── static/
│   ├── tests/
│   └── data/
│
└── 📂 ecommerce/ ⭐⭐ E-commerce specific
    └── (specialized structure for e-commerce)
```

**Usage:**
```bash
./neodoo create --template minimal    # For simple modules
./neodoo create --template production # For enterprise apps
```

---

### Level 2: docs/ (Framework Documentation)

```
docs/
│
├── index.md ⭐⭐ Main documentation index (Obsidian-optimized)
├── README.md → Documentation overview
│
├── 📂 guides/ ⭐⭐⭐ (Multilingual framework guides)
│   ├── en/ (English)
│   │   ├── COMPLETE_GUIDE.md ⭐⭐⭐ Complete English guide
│   │   ├── VALIDATOR_PLUGINS.md → Extend validator
│   │   └── MIGRATION_GUIDE.md → Migration 15/16/17→18
│   │
│   ├── pt/ (Português)
│   │   ├── GUIA_COMPLETO.md ⭐⭐⭐ Complete Portuguese guide
│   │   ├── COMO_USAR_VALIDATOR_NEO_SEMPRE.md → Validator usage
│   │   ├── GUIA_RAPIDO_VALIDATOR.md → Quick validator reference
│   │   └── README.md
│   │
│   └── es/ (Español)
│       └── GUIA_COMPLETA.md ⭐⭐ Complete Spanish guide
│
├── 📂 roles/ (Role definitions - may duplicate framework/roles/)
│   ├── README.md
│   ├── DEVOPS_ENGINEER.md
│   ├── PROJECT_MANAGER.md
│   └── ...
│
├── 📂 examples/ (Documentation examples)
│   ├── IMPLEMENTATION_GUIDE_PARTNER_VIEW.md
│   └── semprereal_partner_view_refactored.xml
│
├── 📂 oca-digests/ (OCA repository digests)
│   ├── OCA-OpenUpgrade.md
│   ├── OCA-account-financial-tools.md
│   └── ... (auto-generated)
│
├── 📂 llm/ (LLM prompts - legacy?)
│   └── prompts/
│       └── assume_integration_specialist.md
│
└── 📄 Standalone Docs (10 files)
    ├── quick-guide.md → Quick start guide
    ├── quick-dev-guide.md → Quick development guide
    ├── workflows.md → Workflow documentation
    ├── glossary.md → Terminology glossary
    ├── faq.md → Frequently asked questions
    ├── roles.md → Roles overview
    ├── VALIDATOR_BEST_PRACTICES.md → Validation best practices
    ├── PLANO_REORGANIZACAO_DOCS.md → Doc reorganization plan
    ├── IMPLEMENTATION_GUIDE.md → Implementation guidelines
    └── IMPACT_ANALYSIS.md → Impact analysis
```

---

### Level 2: corporate_plugins/ (Custom Validation)

```
corporate_plugins/
│
├── neo_sempre/ ← Example corporate plugin
│   └── neo_sempre_rules.py ← Custom validation rules
│
└── neo_sempre_rules.py ← Standalone version
```

**Usage:**
```bash
python framework/validator/validate.py --plugin corporate_plugins/neo_sempre/
```

---

### Level 2: .github/ (GitHub Automation)

```
.github/
│
├── workflows/ ← GitHub Actions
│   ├── oca_watch.yml → OCA repository monitoring
│   └── ... (other workflows)
│
└── copilot-instructions.md → GitHub Copilot instructions
```

---

## 🎯 Resource Types by Function

### For Learning

| Resource | Type | Size | Audience | Topic |
|----------|------|------|----------|-------|
| [README.md](README.md) | Overview | 15KB | All | Framework intro |
| [knowledge/guides/best_practices.md](knowledge/guides/best_practices.md) | Guide | 35KB | Beginners | Odoo 18+ patterns |
| [knowledge/guides/cheatsheet.md](knowledge/guides/cheatsheet.md) | Reference | 12KB | All | Quick lookup |
| [examples/basic/](examples/basic/) | Code | ~1K lines | Beginners | Simple patterns |
| [docs/guides/en/COMPLETE_GUIDE.md](docs/guides/en/COMPLETE_GUIDE.md) | Guide | ~30KB | All | Framework usage |

### For Development

| Resource | Type | Lines | Use Case |
|----------|------|-------|----------|
| [SOIL_CORE.md](framework/standards/SOIL_CORE.md) | Standards | ~200 | All development |
| [examples/advanced/complete_module/models/](examples/advanced/complete_module/models/) | Code | 5K+ | Model patterns |
| [examples/advanced/complete_module/views/](examples/advanced/complete_module/views/) | XML | 2.5K+ | View patterns |
| [examples/advanced/complete_module/static/](examples/advanced/complete_module/static/) | JS | 4K+ | OWL components |

### For Migration

| Resource | Type | Size | From→To |
|----------|------|------|---------|
| [knowledge/guides/migration_guide.md](knowledge/guides/migration_guide.md) | Guide | 41KB | 15/16/17→18 |
| [knowledge/reference/api_changes.md](knowledge/reference/api_changes.md) | Reference | 46KB | All versions |
| [framework/migration/](framework/migration/) | Tools | ~1K lines | Automated migration |

### For Troubleshooting

| Resource | Type | Focus |
|----------|------|-------|
| [knowledge/reference/common_issues.md](knowledge/reference/common_issues.md) | Guide | Error solutions |
| `./neodoo doctor` | Tool | Environment check |
| `python framework/validator/validate.py` | Tool | Code validation |

---

## 📊 File Count by Directory

```
Total Project Files: 216+

framework/          ~30 files
knowledge/          12 files (400+ KB)
examples/           ~70 files (15,000+ lines)
templates/          ~40 files
docs/               ~60 files
corporate_plugins/  2 files
.github/            ~5 files
root/               ~20 files
```

---

## 🔍 Search Strategies

### By Topic

**Workflows & State Machines:**
- [knowledge/guides/workflow_state_machine.md](knowledge/guides/workflow_state_machine.md)
- [examples/advanced/complete_module/models/model_complete_example.py](examples/advanced/complete_module/models/model_complete_example.py) (lines 120-180)

**OWL 2.0:**
- [knowledge/owl/owl_notes.md](knowledge/owl/owl_notes.md) (comprehensive)
- [knowledge/reference/owl_notes.md](knowledge/reference/owl_notes.md) (same content)
- [examples/advanced/complete_module/static/src/js/](examples/advanced/complete_module/static/src/js/)

**Security:**
- [knowledge/guides/best_practices.md#security](knowledge/guides/best_practices.md)
- [examples/advanced/complete_module/security/](examples/advanced/complete_module/security/)
- [framework/roles/SECURITY_EXPERT.md](framework/roles/SECURITY_EXPERT.md)

**API Integration:**
- [knowledge/guides/external_api_integration.md](knowledge/guides/external_api_integration.md)
- [framework/roles/INTEGRATION_SPECIALIST.md](framework/roles/INTEGRATION_SPECIALIST.md)

### By File Type

**Python:**
```bash
find . -name "*.py" -type f | grep -v ".venv" | grep -v ".git"
# Key: framework/, examples/
```

**XML:**
```bash
find . -name "*.xml" -type f | grep -v ".venv"
# Key: examples/advanced/complete_module/views/
```

**Markdown:**
```bash
find . -name "*.md" -type f | grep -v ".git"
# 89 files total
```

**JavaScript:**
```bash
find . -name "*.js" -type f | grep -v ".venv" | grep -v node_modules
# Key: examples/advanced/complete_module/static/src/js/
```

---

## 🚀 Quick Access Shortcuts

### Most Used Files (Top 10)

1. **[LLM_START_HERE.md](LLM_START_HERE.md)** - LLM entry point
2. **[SOIL_CORE.md](framework/standards/SOIL_CORE.md)** - Core standards
3. **[README.md](README.md)** - Human entry point
4. **[knowledge/guides/best_practices.md](knowledge/guides/best_practices.md)** - Best practices
5. **[examples/advanced/complete_module/models/model_complete_example.py](examples/advanced/complete_module/models/model_complete_example.py)** - Model patterns
6. **[knowledge/guides/migration_guide.md](knowledge/guides/migration_guide.md)** - Migration guide
7. **[knowledge/reference/api_changes.md](knowledge/reference/api_changes.md)** - API changes
8. **[knowledge/owl/owl_notes.md](knowledge/owl/owl_notes.md)** - OWL guide
9. **[knowledge/reference/common_issues.md](knowledge/reference/common_issues.md)** - Troubleshooting
10. **[knowledge/guides/cheatsheet.md](knowledge/guides/cheatsheet.md)** - Quick reference

### Most Used Commands

```bash
# Create project
./neodoo create

# Validate code
python framework/validator/validate.py /path/ --strict

# Health check
./neodoo doctor

# Migration
./neodoo migrate /path/to/module --from-version 17
```

---

## 🔗 Related Navigation Docs

- **[LLM_START_HERE.md](LLM_START_HERE.md)** - Task-based navigation for LLMs
- **[CANONICAL_SOURCES.md](CANONICAL_SOURCES.md)** - Canonical vs duplicate files
- **[LLM_FRIENDLINESS_ANALYSIS.md](LLM_FRIENDLINESS_ANALYSIS.md)** - Framework analysis
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Project status and metrics

---

## 📞 Need Help Finding Something?

### Common Questions

**Q: Where are the validation rules?**
A: `framework/validator/plugins/core.py` + `corporate_plugins/`

**Q: Where are the role definitions?**
A: `framework/roles/` (canonical) + `docs/roles/` (may be duplicate)

**Q: Where is the OWL documentation?**
A: `knowledge/owl/owl_notes.md` (primary) + `knowledge/reference/owl_notes.md` (duplicate)

**Q: Where are the examples?**
A: `examples/basic/` (simple) + `examples/advanced/` (production)

**Q: Where is the migration guide?**
A: `knowledge/guides/migration_guide.md`

**Q: Where are the templates?**
A: `templates/minimal/` | `templates/standard/` | `templates/production/`

---

**Document Version:** 1.0 (2025-10-17)

**Last Updated:** 2025-10-17

**Maintained By:** NeoAnd Development Team

**Related:** [LLM_START_HERE.md](LLM_START_HERE.md), [CANONICAL_SOURCES.md](CANONICAL_SOURCES.md)
