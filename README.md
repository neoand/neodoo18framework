
# 🚀 Neodoo18Framework

> **The Ultimate Complete Odoo 18+ Development Environment**

---
> ⚠️ **ATTENTION:**
> To run Neodoo18Framework, you MUST have **Python 3.8+** and **PostgreSQL 12+** installed and available in your system PATH.
>
> If either is missing, the system will show an alert and will not proceed.
>
> - [How to install Python](https://www.python.org/downloads/)
> - [How to install PostgreSQL](https://www.postgresql.org/download/)
>
> *Recommended: Install both before starting the framework!*
---

**Create production-ready Odoo 18+ projects with a single command!**

## ⚡ **QUICK START - 30 SECONDS TO ODOO**

### � **Linux/macOS**
```bash
# Clone and create complete Odoo project
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework
./neodoo create  # interactive wizard (recommended)
```

### 🪟 **Windows**
```batch
# Clone and create complete Odoo project
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# Option 1: Command Prompt/PowerShell
neodoo.bat create      # interactive wizard

# Option 2: PowerShell
.\neodoo.ps1 create    # interactive wizard

# Option 3: Direct Python (if above don't work)
python framework\cli\neodoo.py create
```

**What you get:**
- ✅ Complete Odoo 18+ source code
- ✅ OCA modules (web_responsive included)
- ✅ Virtual environment configured
- ✅ Database ready
- ✅ Browser opens automatically at http://localhost:8069

## 🎯 **WHAT YOU GET**

This framework creates **complete Odoo development environments**, not just modules:

```
~/odoo_projects/your_project/
├── 📦 odoo_source/         # Complete Odoo 18+ source
├── 🔧 custom_addons/       # Your custom modules
├── 🌐 community_addons/    # OCA modules (web, server-tools, etc.)
├── 🐍 .venv/              # Python virtual environment
├── ⚙️  odoo.conf           # Pre-configured settings
├── 🚀 run.sh              # One-click startup
└── 📖 README.md           # Project documentation
```

## 📚 **COMPLETE DOCUMENTATION**

**[📖 Central Documentation](./docs/index.md)** - Complete framework documentation

### Choose Your Language:
- 🇺🇸 [English Guide](./docs/guides/en/COMPLETE_GUIDE.md)
- 🇧🇷 [Guia em Português](./docs/guides/pt/GUIA_COMPLETO.md)
- 🇪🇸 [Guía en Español](./docs/guides/es/GUIA_COMPLETA.md)
- 🧠 [VSCode Agent Playbook](./docs/guides/en/VSCODE_AGENT_PLAYBOOK.md) - Use VSCode as the multi-role command center
- 🧩 [Validator Plugin Guide](./docs/guides/en/VALIDATOR_PLUGINS.md) - Extend the validator with custom checks
- 🧭 [Migration Guide](./docs/guides/en/MIGRATION_GUIDE.md) - Plan upgrades from 15/16/17 to 18

### Platform-Specific:
- 🪟 **[Windows Setup Guide](./WINDOWS.md)** - Complete Windows installation and usage guide

💡 **[Practical Examples](./examples/README.md)** - Real-world use cases and templates

## 🛠️ **COMPLETE PROJECT MANAGEMENT**

### 🎨 **New Visual CLI Interface**

#### 🐧 **Linux/macOS**
```bash
./neodoo                  # Interactive menu with visual interface (recommended!)
```

#### 🪟 **Windows**
```batch
# Command Prompt/PowerShell
neodoo.bat                # Interactive menu with visual interface

# PowerShell
.\neodoo.ps1              # Interactive menu with visual interface

# Direct Python (fallback)
python framework\cli\neodoo.py    # Interactive menu
```

**Menu Options:**
- 🚀 **Create new project** - Interactive wizard with template selection
- 📋 **List projects** - Visual project overview with details  
- ▶️ **Run project** - Start Odoo with real-time status info
- 🗑️ **Delete project** - Safe project removal with confirmation
- 🔧 **Environment check** - System health verification
- 🔄 **Update project** - Update Odoo source and dependencies
- ❓ **Help** - Detailed usage information

### Direct Commands (Alternative)

#### 🐧 **Linux/macOS**
```bash
./neodoo create           # Create new complete project (wizard)
./neodoo list             # List all projects
./neodoo run              # Run project with visual feedback
./neodoo delete           # Delete a project safely
./neodoo doctor           # Check environment health
./neodoo update           # Update project components
./neodoo migrate path/to/module --from-version 17  # Migration assistant report
```

#### 🪟 **Windows**
```batch
# Command Prompt/PowerShell
neodoo.bat create         # Create new complete project (wizard)
neodoo.bat list           # List all projects
neodoo.bat run            # Run project with visual feedback
neodoo.bat delete         # Delete a project safely
neodoo.bat doctor         # Check environment health
neodoo.bat update         # Update project components
neodoo.bat migrate path\to\module --from-version 17  # Migration assistant report

# PowerShell (alternative)
.\neodoo.ps1 create       # Create new complete project (wizard)
.\neodoo.ps1 list         # List all projects
```

## 🧪 Try it

Jump straight to the language guide and follow the CLI-first flow:

- 🇺🇸 English: ./docs/guides/en/COMPLETE_GUIDE.md
- 🇧🇷 Português: ./docs/guides/pt/GUIA_COMPLETO.md
- 🇪🇸 Español: ./docs/guides/es/GUIA_COMPLETA.md

Minimal .neodoo.yml example for reproducible project creation:

```yaml
# .neodoo.yml
version: 1
name: my_odoo18_project
base_dir: ~/odoo_projects
module: my_module
template: minimal
venv: true
odoo_branch: 18.0
```

Then run:

```bash
./neodoo create --from-config ./docs/.neodoo.yml
```

### Visual Project Management
```bash
# Interactive menu (recommended)
./neodoo                           # Beautiful visual menu interface

# Direct commands with enhanced visual feedback
./neodoo list                      # Enhanced project list with colors
./neodoo delete                    # Safe deletion with confirmation dialog
./neodoo run                       # Run with detailed startup information
./neodoo run --path /my/project    # Run specific project with status
./neodoo doctor                    # Environment check with visual results
./neodoo doctor --path /my/project # Project-specific health check
./neodoo update --path /my/project # Update with progress indicators
./neodoo migrate /my/module --from-version 17 # Migration assistant report
```

**Enhanced Features:**
- 🎨 **Colorful output** with emoji indicators
- 📊 **Progress indicators** for long operations  
- 🛡️ **Safe confirmations** for destructive actions
- 📱 **Responsive interface** adapts to terminal size
- 🎯 **Smart port detection** automatically finds available ports
- Estrutura personalizada

## 🧠 **Projetado para LLMs e Desenvolvedores**

Este framework elimina confusão e impõe os padrões mais modernos do Odoo 18+:

- **Sistema SOIL**: Orientação integrada para LLMs
- **Validadores Inteligentes**: Verificação e correção automática
- **Templates Testados**: Estruturas prontas para diversos casos de uso
- **Configuração Zero**: Projeto funcionando em minutos
- **VSCode Agent Workspace**: Tasks, launchers e extensões recomendadas para cada papel definido no framework
- **Plataforma de Plugins de Validação**: Arquitetura extensível para checks internos e de comunidade
- **Assistente de Migração**: Scanner interativo para migrar código 15/16/17 → 18 com relatório em JSON

## 📦 **Componentes Principais**

- `framework/` - Ferramentas essenciais e padrões
  - `validator/` - Ferramentas de validação Odoo 18+
  - `generator/` - Ferramentas de geração de projetos
  - `standards/` - Padrões de conformidade (inclui SOIL)
  - `roles/` - Definições de papéis para LLMs
- `templates/` - Modelos de projetos por tipo
- `examples/` - Implementações de referência
- `docs/` - Documentação multilíngue
```

### Start Developing
```bash
# After project creation, start Odoo
cd ~/odoo_projects/your_project
./run.sh

# Automatically opens browser at http://localhost:8069
# Database is pre-configured
# OCA web_responsive module is auto-installed
```

## 🎯 **What is Neodoo18Framework?**

A comprehensive development framework that creates **complete Odoo 18+ environments**, not just modules:

- **Complete Environment**: Full Odoo source + OCA modules + virtual environment
- **SOIL System**: LLM guidance for consistent Odoo 18+ development
- **Smart Validators**: Automatic compliance checking (no more `<tree>` vs `<list>` errors!)
- **Project Lifecycle**: Create, manage, and delete complete projects
- **Zero-Config Setup**: Working Odoo instance in under 5 minutes

## 🏗️ **Environment Architecture**

```
Framework creates isolated, complete environments:

~/odoo_projects/
├── project_a/           # Complete Odoo environment
│   ├── odoo_source/     # Odoo 18+ source code
│   ├── custom_addons/   # Your modules
│   ├── community_addons/ # OCA modules
│   ├── .venv/          # Isolated Python environment
│   └── run.sh          # One-click startup
├── project_b/           # Another complete environment
└── project_c/           # Yet another environment
```

## 🧠 **For LLMs & AI Assistants**

This framework is specifically designed for AI assistants to understand and follow Odoo 18+ standards:

**Entry Point**: Always start with `framework/llm-guidance/SOIL_CORE.md`
- Contains mandatory patterns and enforcement rules
- Eliminates common Odoo 18+ migration errors
- Provides clear guidance for code generation

## �️ **Development Tools**

```bash
# Complete project management (recommended)
./neodoo create        # Create new complete project (wizard)
./neodoo list          # List all projects
./neodoo delete        # Delete project + database

# Legacy tools
./quick-start.sh       # Create project with defaults
./setup.sh help        # Show legacy help and options

# Framework tools
./env.sh setup         # Setup framework environment
python framework/validator/validate.py path/  # Validate Odoo 18+ compliance
# Use strict mode to enforce stricter rules (promote key warnings to errors)
python framework/validator/validate.py path/ --strict

# Generator flags
python framework/generator/create_project.py --name my_module --type minimal --dry-run  # preview
python framework/generator/create_project.py --name my_module --type minimal --no-all-placeholders  # conservative replacement
```

## ✅ QA / Status

- CLI help, doctor, list, create, and update verified on macOS.
- GitHub Actions CI runs `neodoo doctor --no-input` and the strict validator on every push/pull request.
- Generator lists templates and creates modules from the minimal template that pass the validator in strict mode.
- Filenames with placeholders are auto-renamed during generation (e.g., views/{{MODULE_TECHNICAL_NAME}}_views.xml → views/<module>_views.xml).

Re-run the quick checks locally:

```bash
# 1) List templates
python3 framework/generator/create_project.py --name tmp --list-templates

# 2) Create a temp project without venv for speed
./neodoo create --name sanity_proj --base-dir /tmp/neodoo_sanity --module sanity_mod --template minimal --no-venv

# 3) Run doctor and validator (strict)
./neodoo doctor --path /tmp/neodoo_sanity/sanity_proj --no-input  # drop --no-input for interactive mode
python3 framework/validator/validate.py /tmp/neodoo_sanity/sanity_proj/custom_addons/sanity_mod --strict --auto-fix
```

## 📦 **Deploy Instructions**
See our [Deployment Guide](./DEPLOYMENT.md) for production deployment of created projects.

## 🤝 Community

- **License**: LGPL-3 (following Odoo licensing)
- **Contributions**: Welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Issues**: Use GitHub Issues for bugs and feature requests

## 💡 Why Use Neodoo18Framework?

- **Developers**: Set up Odoo environments in minutes, not hours
- **Companies**: Ensure consistency across projects and teams
- **LLMs**: Get clear guidance for Odoo 18+ development

## 🛡️ Strict Standards

- Odoo 18+ compliance (no legacy patterns)
- Modern Python practices
- LLM-friendly structure
- Enterprise-grade security standards

## 🤝 Community

- **License**: MIT (maximum freedom for developers)
- **Contributions**: Welcome! See CONTRIBUTING.md
- **Issues**: Use GitHub Issues for bugs and feature requests

---

**Built with real experience. Tested in production.**
