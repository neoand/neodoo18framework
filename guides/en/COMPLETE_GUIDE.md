# 🚀 Complete Guide: Neodoo18Framework

> **Universal Framework for Odoo 18+ Development with SOIL System**

## 📚 **TABLE OF CONTENTS**

1. [Quick Installation](#quick-installation)
2. [First Project](#first-project)  
3. [AI Development](#ai-development)
4. [Mandatory Standards](#mandatory-standards)
5. [Automated Validation](#automated-validation)
6. [Practical Examples](#practical-examples)
7. [Odoo Integration](#odoo-integration)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 **QUICK INSTALLATION**

### 🐍 Method 1: Complete Setup with Python Environment (RECOMMENDED)
```bash
# 1. Clone the framework
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# 2. Automatic Python environment setup
./setup-env.sh
# ✅ Creates virtual environment (.venv/)
# ✅ Installs all Odoo 18+ dependencies
# ✅ Configures development tools

# 3. Create first project
./activate-env.sh
./quick-start.sh my_first_project

# 4. Validate quality
python3 framework/validator.py my_first_project/
# Expected: 100% compliance ✅
```

### ⚡ Method 2: Project with Automatic Environment
```bash
# Clone + project + environment in one sequence
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework
./quick-start.sh my_project --full-setup
```

### 📦 Method 3: Framework Only (No Environment)
```bash
# Basic setup without Python environment
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework
chmod +x *.sh
./quick-start.sh my_project
```

### 🔧 Python Environment Options:
```bash
# Complete environment setup
./setup-env.sh

# Project with virtual environment
./quick-start.sh project --setup-venv

# Project with Odoo dependencies
./quick-start.sh project --install-deps

# Project with complete setup
./quick-start.sh project --full-setup
```

### Verify Installation:
```bash
# Framework
python3 framework/validator.py --version
# Expected: Neodoo18Framework Validator v1.0.0

# Python Environment (if configured)
source .venv/bin/activate
python --version
# Expected: Python 3.8+
```

---

## 🏗️ **FIRST PROJECT**

### 🚀 Create Basic Project in 10 Seconds:
```bash
./quick-start.sh my_first_module
```

### 🐍 Create Project with Python Environment:
```bash
# With virtual environment
./quick-start.sh my_project --setup-venv

# With Odoo dependencies installed
./quick-start.sh my_project --install-deps

# Complete setup (venv + dependencies)
./quick-start.sh my_project --full-setup
```

### 🔧 Manage Python Environment:
```bash
# Activate environment
./activate-env.sh

# Check status
source .venv/bin/activate && python -c "import odoo; print('✅ Odoo OK')"

# Deactivate
./deactivate-env.sh
```

### What Was Created:
```
my_first_module/
├── __init__.py                 # Python initialization
├── __manifest__.py             # Odoo configuration
├── models/                     # Data models
│   ├── __init__.py
│   └── template_model.py       # Example model
├── views/                      # Interfaces (created on demand)
├── security/                   # Access control
├── tests/                      # Unit tests
├── wizard/                     # Wizards
├── demo/                       # Demo data
└── README.md                   # Documentation
```

### Check Quality:
```bash
python3 framework/validator.py my_first_module/
# Expected: 100% compliance
```

---

## 🤖 **AI DEVELOPMENT**

### For ChatGPT/Claude/Gemini:

#### 1. Prepare Context:
```bash
# Copy SOIL context for AI
cat framework/SOIL_CORE.md
```

#### 2. Example Prompt:
```
Using Neodoo18Framework, develop a library management module with:

📚 REQUIREMENTS:
- Model: bjj.book (title, author, isbn, category)
- Views: list, form, kanban following Odoo 18+
- Menu: "Library" in main menu
- Security: Basic access rules

⚠️ CRITICAL:
- Use <list> NEVER <tree> 
- Use "list,form" NEVER "tree,form"
- Validate with: python3 framework/validator.py

📋 BASE:
Use framework templates as reference
```

#### 3. Develop and Validate:
```bash
# After AI generates code
python3 framework/validator.py library/
# If 100% = ready for production!
```

---

## ⚠️ **MANDATORY STANDARDS**

### ✅ XML Views (Odoo 18+):
```xml
<!-- CORRECT -->
<record id="book_view_tree" model="ir.ui.view">
    <field name="name">book.view.list</field>
    <field name="model">bjj.book</field>
    <field name="arch" type="xml">
        <list string="Books">
            <field name="title"/>
            <field name="author"/>
        </list>
    </field>
</record>

<!-- CORRECT - Action -->
<record id="book_action" model="ir.actions.act_window">
    <field name="name">Books</field>
    <field name="res_model">bjj.book</field>
    <field name="view_mode">list,form</field>
</record>
```

### ❌ Deprecated XML (Odoo ≤17):
```xml
<!-- WRONG - Don't use anymore -->
<tree string="Books">  <!-- Use <list> -->
    <field name="title"/>
</tree>

<!-- WRONG - Action -->
<field name="view_mode">tree,form</field>  <!-- Use list,form -->
```

### ✅ Python Models:
```python
# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class Book(models.Model):
    _name = 'bjj.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'title asc'
    
    title = fields.Char(
        string='Title', 
        required=True, 
        tracking=True
    )
    author = fields.Char(string='Author', required=True)
    isbn = fields.Char(string='ISBN', size=13)
    
    @api.constrains('isbn')
    def _check_isbn(self):
        for record in self:
            if record.isbn and len(record.isbn) != 13:
                raise ValidationError(_('ISBN must have 13 digits'))
```

---

## ✅ **AUTOMATED VALIDATION**

### Basic Command:
```bash
python3 framework/validator.py my_project/
```

### Example Output:
```
🚀 Neodoo18Framework Validator
==================================================

📊 Summary:
   Files checked: 8
   Errors: 0
   Warnings: 0
   Auto-fixes applied: 0
   Average compliance: 100.0%

✅ All checks passed! Ready for production.
```

### Validation with Auto-Fix:
```bash
python3 framework/validator.py my_project/ --auto-fix
```

### Detailed Validation:
```bash
python3 framework/validator.py my_project/ --verbose
```

---

## 💡 **PRACTICAL EXAMPLES**

### Example 1: Simple E-commerce
```bash
./quick-start.sh online_store
cd online_store

# Develop with AI using SOIL context
# Result: Module with products, categories, orders
```

### Example 2: Custom CRM  
```bash
./quick-start.sh my_crm
cd my_crm

# Develop: customers, opportunities, activities
# Validate: python3 ../framework/validator.py .
```

### Example 3: School System
```bash
./quick-start.sh school_system
cd school_system

# Models: students, teachers, classes, grades
# Integration: res.partner inheritance
```

---

## 🔗 **ODOO INTEGRATION**

### Method 1: Direct Copy
```bash
# Copy module to Odoo addons
cp -r my_project /opt/odoo/addons/
sudo chown -R odoo:odoo /opt/odoo/addons/my_project
sudo systemctl restart odoo
```

### Method 2: Symlink (Development)
```bash
# Create symbolic link
ln -s $(pwd)/my_project /opt/odoo/addons/
# Restart Odoo
```

### Method 3: Odoo.sh / SaaS
```bash
# Zip module
zip -r my_project.zip my_project/
# Upload via Odoo.sh interface
```

### Activation in Odoo:
1. **Apps** → **Update Apps List**
2. **Search**: Your module name  
3. **Install**
4. **Verify**: Menu appears in interface

---

## 🛠️ **TROUBLESHOOTING**

### ❌ Error: "Invalid view mode 'tree'"
**Solution:**
```bash
python3 framework/validator.py my_project/ --auto-fix
# Automatically fixes tree → list
```

### ❌ Error: "Module not found"  
**Check:**
```bash
# 1. Does __init__.py exist?
ls my_project/__init__.py

# 2. Correct imports?
cat my_project/models/__init__.py
# Should contain: from . import model_name
```

### ❌ Error: "XML Syntax Error"
**Validate XML:**
```bash
python3 framework/xml_validator.py my_project/views/
```

### ❌ Error: "Access Rights"
**Check Security:**
```bash
# 1. Does ir.model.access.csv exist?
ls my_project/security/

# 2. Groups defined?
grep "group_" my_project/security/*.xml
```

---

## 📋 **QUALITY CHECKLIST**

### Before Deploy:
- [ ] `python3 framework/validator.py project/` = 100%
- [ ] XML uses `<list>` not `<tree>`  
- [ ] Actions use `"list,form"` not `"tree,form"`
- [ ] Models inherit `mail.thread`
- [ ] Security rules defined
- [ ] Basic tests created
- [ ] README updated

### Minimum Structure:
- [ ] Complete `__manifest__.py`
- [ ] `models/__init__.py` with imports
- [ ] `security/ir.model.access.csv`
- [ ] `views/` with menus and actions
- [ ] Basic documentation

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