# 📚 CANONICAL SOURCES - Neodoo18Framework v2.0

> **Definitive List of Canonical Files vs Duplicates**
>
> When multiple files have similar content, this doc tells you which one is the **source of truth**.

---

## 🎯 Purpose

This document resolves ambiguity by declaring:
1. **Which file is canonical** (source of truth)
2. **Which files are duplicates** or outdated
3. **Recommendations** for consolidation

---

## ⭐ Golden Rule for LLMs

**ALWAYS read the CANONICAL source first. Ignore duplicates unless specifically needed.**

---

## 📋 Canonical Files by Category

### 1. Core Framework Documentation

| Topic | Canonical Source | Status | Duplicates/Related |
|-------|------------------|--------|-------------------|
| **Framework Overview** | [README.md](README.md) | ✅ Canonical | None |
| **LLM Entry Point** | [LLM_START_HERE.md](LLM_START_HERE.md) | ✅ Canonical | None |
| **Navigation** | [NAVIGATION_MAP.md](NAVIGATION_MAP.md) | ✅ Canonical | None |
| **Canonical Index** | [CANONICAL_SOURCES.md](CANONICAL_SOURCES.md) | ✅ Canonical (this file) | None |
| **Fusion Guide** | [FUSION_GUIDE.md](FUSION_GUIDE.md) | ✅ Canonical | None |
| **Project Status** | [PROJECT_STATUS.md](PROJECT_STATUS.md) | ✅ Canonical | None |
| **LLM Analysis** | [LLM_FRIENDLINESS_ANALYSIS.md](LLM_FRIENDLINESS_ANALYSIS.md) | ✅ Canonical | None |

---

### 2. Standards & Rules

| Topic | Canonical Source | Status | Duplicates/Related |
|-------|------------------|--------|-------------------|
| **SOIL System** | [framework/standards/SOIL_CORE.md](framework/standards/SOIL_CORE.md) | ✅ Canonical | ⚠️ Was in `framework/llm-guidance/SOIL_CORE.md` (deleted in v2.0) |
| **Odoo 18+ Standards** | [framework/standards/ODOO18_CORE_STANDARDS.md](framework/standards/ODOO18_CORE_STANDARDS.md) | ✅ Canonical | None |

---

### 3. Role Definitions

| Role | Canonical Source | Status | Duplicates |
|------|------------------|--------|------------|
| **Backend Developer** | [framework/roles/BACKEND_DEVELOPER.md](framework/roles/BACKEND_DEVELOPER.md) | ✅ Canonical | ⚠️ `docs/roles/` may have copy |
| **OWL Specialist** | [framework/roles/OWL_SPECIALIST.md](framework/roles/OWL_SPECIALIST.md) | ✅ Canonical | ⚠️ `docs/roles/` may have copy |
| **Integration Specialist** | [framework/roles/INTEGRATION_SPECIALIST.md](framework/roles/INTEGRATION_SPECIALIST.md) | ✅ Canonical | ⚠️ `docs/roles/` may have copy |
| **Data Migration Specialist** | [framework/roles/DATA_MIGRATION_SPECIALIST.md](framework/roles/DATA_MIGRATION_SPECIALIST.md) | ✅ Canonical | ⚠️ `docs/roles/` may have copy |
| **Security Expert** | [framework/roles/SECURITY_EXPERT.md](framework/roles/SECURITY_EXPERT.md) | ✅ Canonical | ⚠️ `docs/roles/` may have copy |
| **DevOps Engineer** | [framework/roles/DEVOPS_ENGINEER.md](framework/roles/DEVOPS_ENGINEER.md) | ✅ Canonical | ⚠️ `docs/roles/DEVOPS_ENGINEER.md` |
| **UX/UI Designer** | [framework/roles/UXUI_DESIGNER.md](framework/roles/UXUI_DESIGNER.md) | ✅ Canonical | ⚠️ `docs/roles/` may have copy |
| **Business Analyst** | [framework/roles/BUSINESS_ANALYST.md](framework/roles/BUSINESS_ANALYST.md) | ✅ Canonical | ⚠️ `docs/roles/` may have copy |
| **Project Manager** | [framework/roles/PROJECT_MANAGER.md](framework/roles/PROJECT_MANAGER.md) | ✅ Canonical | ⚠️ `docs/roles/PROJECT_MANAGER.md` |

**Recommendation:** Consolidate `docs/roles/` into `framework/roles/` or create symlinks.

---

### 4. Knowledge Base (Odoo 18+ Documentation)

| Topic | Canonical Source | Size | Duplicates |
|-------|------------------|------|------------|
| **Knowledge Base Index** | [knowledge/README.md](knowledge/README.md) | 9KB | None |
| **Migration Guide 15/16/17→18** | [knowledge/guides/migration_guide.md](knowledge/guides/migration_guide.md) | 41KB | ⚠️ `docs/guides/en/MIGRATION_GUIDE.md` (may differ) |
| **Best Practices** | [knowledge/guides/best_practices.md](knowledge/guides/best_practices.md) | 35KB | None |
| **Workflow State Machines** | [knowledge/guides/workflow_state_machine.md](knowledge/guides/workflow_state_machine.md) | 29KB | None |
| **External API Integration** | [knowledge/guides/external_api_integration.md](knowledge/guides/external_api_integration.md) | 32KB | None |
| **Cheatsheet** | [knowledge/guides/cheatsheet.md](knowledge/guides/cheatsheet.md) | 12KB | None |
| **API Changes** | [knowledge/reference/api_changes.md](knowledge/reference/api_changes.md) | 46KB | None |
| **View Syntax** | [knowledge/reference/view_syntax.md](knowledge/reference/view_syntax.md) | 38KB | None |
| **Common Issues** | [knowledge/reference/common_issues.md](knowledge/reference/common_issues.md) | 26KB | None |
| **Python Tips Odoo 18** | [knowledge/reference/tips_python_odoo18.md](knowledge/reference/tips_python_odoo18.md) | 22KB | None |
| **OWL Notes** | [knowledge/owl/owl_notes.md](knowledge/owl/owl_notes.md) | 53KB | ❌ **DUPLICATE:** `knowledge/reference/owl_notes.md` (same file) |
| **OWL Version Check** | [knowledge/owl/owl_version_check.md](knowledge/owl/owl_version_check.md) | 9KB | ⚠️ `examples/advanced/complete_module/owl_version_check.md` (may differ) |

**Issues Identified:**
- `owl_notes.md` exists in TWO locations (knowledge/owl/ and knowledge/reference/)
- Recommendation: **Keep only** `knowledge/owl/owl_notes.md`, delete `knowledge/reference/owl_notes.md`

---

### 5. Code Examples

| Type | Canonical Source | Lines | Duplicates |
|------|------------------|-------|------------|
| **Basic Examples Index** | [examples/basic/](examples/basic/) | N/A | None |
| **Advanced Examples Index** | [examples/advanced/README.md](examples/advanced/README.md) | 9KB | None |
| **Complete Module** | [examples/advanced/complete_module/](examples/advanced/complete_module/) | 15K+ | None |
| **Simple Model** | [examples/basic/demo_project/models/template_model.py](examples/basic/demo_project/models/template_model.py) | ~100 | None |
| **Complete Model** | [examples/advanced/complete_module/models/model_complete_example.py](examples/advanced/complete_module/models/model_complete_example.py) | 1334 | None |
| **OWL Basic Component** | [examples/advanced/complete_module/static/src/js/component_basic_example.js](examples/advanced/complete_module/static/src/js/component_basic_example.js) | ~300 | None |
| **OWL Advanced Component** | [examples/advanced/complete_module/static/src/js/component_advanced_example.js](examples/advanced/complete_module/static/src/js/component_advanced_example.js) | ~800 | None |

---

### 6. Framework Guides (Multilingual)

| Language | Canonical Source | Status | Duplicates |
|----------|------------------|--------|------------|
| **English Complete Guide** | [docs/guides/en/COMPLETE_GUIDE.md](docs/guides/en/COMPLETE_GUIDE.md) | ✅ Canonical | None |
| **English Validator Plugins** | [docs/guides/en/VALIDATOR_PLUGINS.md](docs/guides/en/VALIDATOR_PLUGINS.md) | ✅ Canonical | None |
| **Portuguese Complete Guide** | [docs/guides/pt/GUIA_COMPLETO.md](docs/guides/pt/GUIA_COMPLETO.md) | ✅ Canonical | None |
| **Portuguese Validator Guide** | [docs/guides/pt/COMO_USAR_VALIDATOR_NEO_SEMPRE.md](docs/guides/pt/COMO_USAR_VALIDATOR_NEO_SEMPRE.md) | ✅ Canonical | None |
| **Portuguese Validator Quick** | [docs/guides/pt/GUIA_RAPIDO_VALIDATOR.md](docs/guides/pt/GUIA_RAPIDO_VALIDATOR.md) | ✅ Canonical | ⚠️ `VALIDATOR_QUICK_REFERENCE.txt` (root, may overlap) |
| **Spanish Complete Guide** | [docs/guides/es/GUIA_COMPLETA.md](docs/guides/es/GUIA_COMPLETA.md) | ✅ Canonical | None |

---

### 7. Documentation Index Files

| Purpose | Canonical Source | Status | Duplicates |
|---------|------------------|--------|------------|
| **Main Docs Index (Obsidian)** | [docs/index.md](docs/index.md) | ✅ Canonical | None |
| **Docs README** | [docs/README.md](docs/README.md) | ✅ Canonical | None |
| **Quick Start Guide** | [docs/quick-guide.md](docs/quick-guide.md) | ✅ Canonical | ⚠️ May overlap with README.md |
| **Quick Dev Guide** | [docs/quick-dev-guide.md](docs/quick-dev-guide.md) | ✅ Canonical | None |
| **Workflows** | [docs/workflows.md](docs/workflows.md) | ✅ Canonical | None |
| **Glossary** | [docs/glossary.md](docs/glossary.md) | ✅ Canonical | None |
| **FAQ** | [docs/faq.md](docs/faq.md) | ✅ Canonical | None |
| **Roles Overview** | [docs/roles.md](docs/roles.md) | ✅ Canonical | ⚠️ `docs/roles/README.md` may overlap |

---

### 8. Validator Documentation

| Topic | Canonical Source | Status | Duplicates |
|-------|------------------|--------|------------|
| **Validator Best Practices** | [docs/VALIDATOR_BEST_PRACTICES.md](docs/VALIDATOR_BEST_PRACTICES.md) | ✅ Canonical | None |
| **Validator Quick Reference** | [VALIDATOR_QUICK_REFERENCE.txt](VALIDATOR_QUICK_REFERENCE.txt) | ✅ Canonical | ⚠️ `docs/guides/pt/GUIA_RAPIDO_VALIDATOR.md` (may overlap) |
| **Validator Plugin Guide** | [docs/guides/en/VALIDATOR_PLUGINS.md](docs/guides/en/VALIDATOR_PLUGINS.md) | ✅ Canonical | None |
| **Corporate Plugin Example** | [corporate_plugins/neo_sempre/neo_sempre_rules.py](corporate_plugins/neo_sempre/neo_sempre_rules.py) | ✅ Canonical | ⚠️ `corporate_plugins/neo_sempre_rules.py` (standalone copy) |

---

### 9. Changelog & History

| Topic | Canonical Source | Status | Notes |
|-------|------------------|--------|-------|
| **Main Changelog** | [CHANGELOG.md](CHANGELOG.md) | ✅ Canonical | Full version history |
| **v2.0 Changelog** | [CHANGELOG_V2.md](CHANGELOG_V2.md) | ✅ Canonical (v2.0 specific) | Supplement to main |

**Recommendation:** Eventually merge `CHANGELOG_V2.md` into `CHANGELOG.md` as a v2.0 section.

---

### 10. Deployment & Operations

| Topic | Canonical Source | Status | Duplicates |
|-------|------------------|--------|------------|
| **Deployment Guide** | [DEPLOYMENT.md](DEPLOYMENT.md) | ✅ Canonical | None |
| **Windows Setup** | [WINDOWS.md](WINDOWS.md) | ✅ Canonical | None |
| **Security Policy** | [SECURITY.md](SECURITY.md) | ✅ Canonical | None |
| **Contributing Guide** | [CONTRIBUTING.md](CONTRIBUTING.md) | ✅ Canonical | None |
| **Code of Conduct** | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | ✅ Canonical | None |

---

### 11. Tools & Scripts

| Tool | Canonical Source | Status | Duplicates |
|------|------------------|--------|------------|
| **Main CLI (Linux/macOS)** | [neodoo](neodoo) | ✅ Canonical | Wrapper for `framework/cli/neodoo.py` |
| **CLI Implementation** | [framework/cli/neodoo.py](framework/cli/neodoo.py) | ✅ Canonical | None |
| **Windows Batch** | [neodoo.bat](neodoo.bat) | ✅ Canonical | None |
| **Windows PowerShell** | [neodoo.ps1](neodoo.ps1) | ✅ Canonical | None |
| **Validator** | [framework/validator/validate.py](framework/validator/validate.py) | ✅ Canonical | None |
| **Project Generator** | [framework/generator/create_project.py](framework/generator/create_project.py) | ✅ Canonical | None |
| **Migration Tool** | [framework/migration/cli.py](framework/migration/cli.py) | ✅ Canonical | None |
| **Corporate Validator Script** | [validate_neo_sempre.sh](validate_neo_sempre.sh) | ✅ Canonical | None |

---

## 🔴 Known Duplicates & Issues

### Issue #1: OWL Notes Duplication

**Problem:**
```
knowledge/owl/owl_notes.md (53 KB) ← CANONICAL
knowledge/reference/owl_notes.md (53 KB) ← DUPLICATE (same content)
```

**Resolution:**
- **Keep:** `knowledge/owl/owl_notes.md`
- **Delete:** `knowledge/reference/owl_notes.md`
- **Reason:** OWL-specific docs should be in `knowledge/owl/` subdirectory

**Action Required:** ✅ TODO (Phase 2)

---

### Issue #2: Role Definitions Duplication

**Problem:**
```
framework/roles/ ← CANONICAL (11 files)
docs/roles/ ← POTENTIAL DUPLICATES (unknown count)
```

**Investigation Needed:**
```bash
diff framework/roles/DEVOPS_ENGINEER.md docs/roles/DEVOPS_ENGINEER.md
# If different: Merge or declare one canonical
# If same: Delete docs/roles/, keep only framework/roles/
```

**Resolution TBD:** ⚠️ Requires diff check

**Action Required:** ⏳ TODO (Phase 2)

---

### Issue #3: Corporate Plugin Standalone Copy

**Problem:**
```
corporate_plugins/neo_sempre/neo_sempre_rules.py ← CANONICAL (in directory)
corporate_plugins/neo_sempre_rules.py ← STANDALONE COPY
```

**Resolution:**
- **Keep:** `corporate_plugins/neo_sempre/neo_sempre_rules.py` (organized)
- **Delete or Document:** `corporate_plugins/neo_sempre_rules.py` (if truly identical)
- **Alternative:** If standalone is for convenience, add comment explaining relationship

**Action Required:** ⏳ TODO (Phase 2)

---

### Issue #4: Migration Guide Potential Duplication

**Problem:**
```
knowledge/guides/migration_guide.md ← CANONICAL (Odoo-focused, 41KB)
docs/guides/en/MIGRATION_GUIDE.md ← FRAMEWORK migration? (unknown size)
```

**Investigation Needed:**
- Check if `docs/guides/en/MIGRATION_GUIDE.md` covers framework migration or Odoo migration
- If both cover Odoo 17→18: Consolidate
- If different scopes: Clarify and document

**Action Required:** ⏳ TODO (Phase 2)

---

### Issue #5: Validator Quick Reference Multiple Formats

**Problem:**
```
VALIDATOR_QUICK_REFERENCE.txt ← Root, TXT format
docs/guides/pt/GUIA_RAPIDO_VALIDATOR.md ← Portuguese, MD format
```

**Overlap:** Both may cover same content in different formats/languages

**Resolution:**
- **Keep both** if serving different audiences:
  - `.txt` for quick CLI reference (English)
  - `.md` for Portuguese comprehensive guide
- **Cross-reference** each other
- **Clarify** which is more comprehensive

**Action Required:** ⏳ TODO (Phase 2)

---

## ✅ Consolidation Recommendations

### Priority 1 (High Impact) 🔴

1. **Delete `knowledge/reference/owl_notes.md`** (duplicate)
   - Keep only `knowledge/owl/owl_notes.md`
   - Update any links pointing to the old location

2. **Investigate and resolve `framework/roles/` vs `docs/roles/`**
   - Run diff on all matching files
   - Keep canonical in `framework/roles/`
   - Delete or symlink `docs/roles/`

### Priority 2 (Medium Impact) 🟡

3. **Clarify migration guides**
   - Document difference between `knowledge/guides/migration_guide.md` and `docs/guides/en/MIGRATION_GUIDE.md`
   - If duplicates: merge

4. **Resolve corporate plugin standalone copy**
   - Decide on `corporate_plugins/neo_sempre/` (organized) vs `corporate_plugins/neo_sempre_rules.py` (standalone)

### Priority 3 (Low Impact) 🟢

5. **Consider merging `CHANGELOG_V2.md` into `CHANGELOG.md`**
   - As v2.0 section
   - Or keep separate and cross-reference

6. **Review overlap between quick guides**
   - `docs/quick-guide.md` vs `README.md`
   - `VALIDATOR_QUICK_REFERENCE.txt` vs `docs/guides/pt/GUIA_RAPIDO_VALIDATOR.md`

---

## 🎯 Usage Guide for LLMs

### When Reading Documentation

1. **Always check this file first** to find the canonical source
2. **Read canonical sources only** unless explicitly comparing versions
3. **Ignore duplicates** unless investigating discrepancies

### When Updating Documentation

1. **Update canonical source only**
2. **Delete or sync duplicates** after canonical update
3. **Document any intentional duplicates** (e.g., different languages, different audiences)

### When Uncertain

1. **Check timestamps:** More recent = likely canonical
2. **Check file size:** Larger/more detailed = likely canonical
3. **Check location:** More organized directory structure = likely canonical
4. **Refer to this doc:** Trust the declarations in CANONICAL_SOURCES.md

---

## 📊 Statistics

### Canonical Files by Category

| Category | Canonical Count | Known Duplicates |
|----------|----------------|------------------|
| Core Framework Docs | 7 | 0 |
| Standards & Rules | 2 | 1 (deleted) |
| Role Definitions | 11 | ~11 (TBD) |
| Knowledge Base | 12 | 2 |
| Code Examples | 70+ | 0 |
| Framework Guides | 8 | 2 |
| Documentation Indexes | 9 | 2 |
| Validator Docs | 4 | 2 |
| Changelog & History | 2 | 0 |
| Deployment & Ops | 5 | 0 |
| Tools & Scripts | 9 | 0 |

**Total Canonical Files:** ~140
**Known Duplicates:** ~20
**Duplication Rate:** ~14%

---

## 🔍 How to Verify Canonical Status

### Method 1: Check This Document
Search this file for the topic/file you're interested in.

### Method 2: Check File Headers
Canonical files should have clear headers indicating their status:
```markdown
---
canonical: true
topic: validation
category: framework
---
```
*(Not yet implemented - TODO for Phase 3)*

### Method 3: Check Git History
```bash
git log --follow path/to/file.md
# Older commits = likely canonical
# Recent creation = may be duplicate
```

### Method 4: Check File Size
Usually, the canonical version is more comprehensive (larger file size).

---

## 🚨 Reporting Issues

Found a duplicate not listed here? Found canonical source is outdated?

1. **Check file contents** to verify duplication
2. **Compare timestamps** (`ls -l` or `git log`)
3. **Update this document** with findings
4. **Create issue** in GitHub (if applicable)

---

## 📝 Maintenance

This document should be updated whenever:
- New documentation is added
- Duplicates are discovered
- Consolidation is performed
- Canonical sources change location

**Last Review:** 2025-10-17

**Next Review:** After Phase 2 consolidation

---

**Document Version:** 1.0 (2025-10-17)

**Maintained By:** NeoAnd Development Team

**Related:** [NAVIGATION_MAP.md](NAVIGATION_MAP.md), [LLM_START_HERE.md](LLM_START_HERE.md)
