# 🚀 Neodoo18Framework

> **The Ultimate Complete Odoo 18+ Development Environment**

**Create production-ready Odoo 18+ projects with a single command!**

## ⚡ **QUICK START - 30 SECONDS TO ODOO**

```bash
# Clone and create complete Odoo project
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework
./neodoo create  # interactive wizard (recommended)

# Or use legacy quick start defaults
./quick-start.sh

# ✅ Complete Odoo 18+ source code
# ✅ OCA modules (web_responsive included)
# ✅ Virtual environment configured
# ✅ Database ready
# ✅ Browser opens automatically at http://localhost:8069
```

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

💡 **[Practical Examples](./examples/README.md)** - Real-world use cases and templates

## 🛠️ **COMPLETE PROJECT MANAGEMENT**

### Create Projects
```bash
# New single-command CLI (recommended)
./neodoo create           # Create new complete project (wizard)
./neodoo create --from-config /path/to/.neodoo.yml  # Reproduce from config (non-interactive)
./neodoo list             # List all projects
./neodoo delete           # Delete a project

# Legacy scripts (still available)
./quick-start.sh          # Create with defaults
./setup.sh create         # Legacy interactive creation
./setup.sh                # Legacy guided setup
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

### Manage Projects
```bash
# With the new CLI
./neodoo list
./neodoo delete
./neodoo doctor                    # Check environment (python, git, ports)
./neodoo doctor --path /my/project # Check a specific project structure/venv
./neodoo update --path /my/project # Update Odoo/OCA repos and venv deps

# Legacy
./setup.sh list
./setup.sh delete
./setup.sh help
```
- Estrutura personalizada

## 🧠 **Projetado para LLMs e Desenvolvedores**

Este framework elimina confusão e impõe os padrões mais modernos do Odoo 18+:

- **Sistema SOIL**: Orientação integrada para LLMs
- **Validadores Inteligentes**: Verificação e correção automática
- **Templates Testados**: Estruturas prontas para diversos casos de uso
- **Configuração Zero**: Projeto funcionando em minutos

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
- Generator lists templates and creates modules from the minimal template that pass the validator in strict mode.
- Filenames with placeholders are auto-renamed during generation (e.g., views/{{MODULE_TECHNICAL_NAME}}_views.xml → views/<module>_views.xml).

Re-run the quick checks locally:

```bash
# 1) List templates
python3 framework/generator/create_project.py --name tmp --list-templates

# 2) Create a temp project without venv for speed
./neodoo create --name sanity_proj --base-dir /tmp/neodoo_sanity --module sanity_mod --template minimal --no-venv

# 3) Run doctor and validator (strict)
./neodoo doctor --path /tmp/neodoo_sanity/sanity_proj
python3 framework/validator/validate.py /tmp/neodoo_sanity/sanity_proj/custom_addons/sanity_mod --strict --auto-fix
```

## 📦 **Deploy Instructions**
See our [Deployment Guide](./DEPLOYMENT.md) for production deployment of created projects.

## 🤝 Community

- **License**: LGPL-3 (following Odoo licensing)
- **Contributions**: Welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Issues**: Use GitHub Issues for bugs and feature requests

## � **Por Que Usar?**

- **Desenvolvedores**: Configure ambientes Odoo em minutos, não horas
- **Empresas**: Garanta consistência entre projetos e desenvolvedores
- **LLMs**: Receba orientação clara para desenvolvimento Odoo 18+

## 🛡️ **Padrões Rigorosos**

- Conformidade Odoo 18+ (sem padrões legados)
- Práticas modernas de Python
- Estrutura amigável para LLMs
- Padrões de segurança empresarial

## 🤝 **Comunidade**

- **Licença**: MIT (máxima liberdade para desenvolvedores)
- **Contribuições**: Bem-vindas! Veja CONTRIBUTING.md
- **Issues**: Use GitHub Issues para bugs e solicitações de recursos

---

**Construído com experiência real. Testado em produção.**