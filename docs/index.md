# Neodoo18Framework - Complete Documentation# Neodoo18Framework - Documentação Principal



![[neodoo_logo.png]]![[neodoo_logo.png]]



> [!NOTE] Welcome to Neodoo18Framework> [!NOTE] Sobre este documento

> The Ultimate Odoo 18+ Development Framework designed for LLMs and Developers. This central documentation provides everything you need to understand, use, and master the framework.> Este é o arquivo master de documentação do Neodoo18Framework, otimizado para navegação no Obsidian. Utilize os links abaixo para navegar por toda a documentação do framework.



## 🌟 What is Neodoo18Framework?## 🌟 Introdução



Neodoo18Framework is a **LLM-first** development framework for Odoo 18+ that provides:O Neodoo18Framework é um framework de desenvolvimento para Odoo 18+ com design LLM-first, que fornece ferramentas, padrões e guias para desenvolvimento rápido e eficiente. Este framework impõe padrões modernos do Odoo 18+ e fornece validadores, geradores e templates para desenvolvimento acelerado.



- **🎯 Zero-Config Setup**: Working Odoo project in minutes- [[../README|Página Principal]] - Visão geral do projeto

- **🤖 AI-Optimized**: Designed specifically for Large Language Models- [[quick-guide|Guia Rápido]] - Introdução rápida ao framework

- **✅ Smart Validation**: Automatic Odoo 18+ compliance checking- [[quick-dev-guide|Guia de Desenvolvimento Rápido]] - Dicas e exemplos práticos

- **📋 Battle-Tested Templates**: Ready-to-use project structures- [[faq|Perguntas Frequentes]] - Respostas para dúvidas comuns

- **🔄 Modern Standards**: Enforces latest Odoo 18+ best practices- [[../CONTRIBUTING|Guia de Contribuição]] - Como contribuir para o projeto

- [[contributing-to-docs|Contribuir para Documentação]] - Como melhorar esta documentação
- [[oca-digests/README|OCA Digests & Rollups]] - Resumos diários e consolidação semanal de mudanças OCA

## 🚀 Quick Start- [[../CHANGELOG|Histórico de Mudanças]] - Registro de alterações no projeto

- [[../CODE_OF_CONDUCT|Código de Conduta]] - Regras para participação na comunidade

### 1. Setup Environment- [[../SECURITY|Política de Segurança]] - Políticas e práticas de segurança

```bash

git clone https://github.com/neoand/neodoo18framework.git## 🏗️ Arquitetura

cd neodoo18framework

./env.sh setupA estrutura do Neodoo18Framework é organizada da seguinte forma:

./env.sh activate

```- `framework/` - Ferramentas principais, padrões e orientação LLM

  - `validator/` - Ferramentas de validação do Odoo 18+

### 2. Create Your First Project  - `generator/` - Ferramentas de geração de projetos

```bash- `templates/` - Boilerplates de projetos por tipo

# Quick method  - `minimal/` - Estrutura básica de projeto

./quick_start.sh my_project  - `advanced/` - Módulos avançados completos (renomeado de 'enterprise')

  - `ecommerce/` - Módulos específicos para e-commerce

# Interactive setup with full configuration- `examples/` - Padrões de implementação do mundo real

./setup.sh  - `demo_project/` - Projeto de demonstração

```  - `library_system/` - Sistema de biblioteca exemplo

- `docs/` - Documentação unificada

### 3. Validate Your Code  - `standards/` - Padrões de desenvolvimento

```bash  - `roles/` - Definições de papéis especializados

python framework/validator/validate.py my_project/  - `guides/` - Guias em múltiplos idiomas

```

## 📚 Padrões e Diretrizes

## 📚 Choose Your Language

Esta seção contém os padrões e diretrizes para o desenvolvimento com o Neodoo18Framework:

Select your preferred language for detailed guides:

- [[standards/ODOO18_CORE_STANDARDS|Padrões Principais do Odoo 18]] - Padrões de desenvolvimento para Odoo 18+

### 🇺🇸 English (Complete Guide)- [[standards/SOIL_CORE|SOIL Core]] - Sistema de Orientação Integrada LLM

[[guides/en/COMPLETE_GUIDE|📖 English Complete Guide]] - Full documentation in English- [[workflows|Workflows e Processos]] - Fluxos de trabalho recomendados

- [[glossary|Glossário de Termos]] - Definições dos termos utilizados

## 📚 Knowledge Base (v2.0)

**Nova seção adicionada na versão 2.0 com documentação completa do Odoo 18+:**

- [[../knowledge/README|📖 Knowledge Base Index]] - Índice completo da base de conhecimento (20 documentos, 400+ KB)

### Guias Práticos
- [[../knowledge/guides/migration_guide|🔄 Guia de Migração]] - Migração de Odoo 15/16/17 para 18
- [[../knowledge/guides/best_practices|✨ Melhores Práticas]] - Padrões recomendados para Odoo 18+
- [[../knowledge/guides/workflow_state_machine|⚙️ Máquinas de Estado]] - Implementação de workflows
- [[../knowledge/guides/external_api_integration|🔌 Integração de APIs]] - Como integrar APIs externas
- [[../knowledge/guides/cheatsheet|📋 Cheatsheet]] - Referência rápida

### Referência Técnica
- [[../knowledge/reference/api_changes|🔧 Mudanças de API]] - Changelog completo de APIs Odoo 18
- [[../knowledge/reference/view_syntax|📐 Sintaxe de Views]] - Referência XML completa
- [[../knowledge/reference/common_issues|🐛 Problemas Comuns]] - Troubleshooting e soluções
- [[../knowledge/reference/tips_python_odoo18|🐍 Dicas Python]] - Python moderno para Odoo 18+

### OWL 2.0 Framework
- [[../knowledge/owl/owl_notes|🦉 OWL 2.0 Completo]] - Guia definitivo de OWL 2.0
- [[../knowledge/owl/owl_version_check|✅ Verificação de Versão]] - Como verificar compatibilidade OWL

## 🎯 Exemplos Avançados (v2.0)

**Nova coleção de exemplos production-ready:**

- [[../examples/advanced/README|📦 Advanced Examples]] - 36 arquivos com 15,000+ linhas de código
- [[../examples/advanced/complete_module|🏗️ Complete Module]] - Módulo completo com todos os componentes
  - 4 modelos Python (1,334+ linhas cada)
  - 5 views XML (List, Form, Calendar, Kanban, Pivot)
  - 7 componentes OWL 2.0 (4,000+ linhas JavaScript)
  - Security, Reports, Wizards, Tests

### 🇧🇷 Português (Guia Completo)

[[guides/pt/GUIA_COMPLETO|📖 Guia Completo em Português]] - Documentação completa em português
[[guides/pt/COMO_USAR_VALIDATOR_NEO_SEMPRE|🔍 Como Usar o Validator Neo Sempre]] - Guia completo de uso do validator
[[guides/pt/GUIA_RAPIDO_VALIDATOR|⚡ Guia Rápido - Validator]] - Referência rápida para validação## 👤 Papéis Especializados



### 🇪🇸 Español (Guía Completa)O Neodoo18Framework define papéis especializados para desenvolvimento organizado e eficiente:

[[guides/es/GUIA_COMPLETA|📖 Guía Completa en Español]] - Documentación completa en español

- [[roles|Visão Geral dos Papéis]] - Estrutura completa dos papéis especializados

## 🏗️ Framework Architecture

### Desenvolvimento Frontend e Backend

```

neodoo18framework/- [[../framework/roles/OWL_SPECIALIST|OWL Specialist]] - Especialista no framework OWL para desenvolvimento de interfaces

├── framework/           # Core tools and standards- [[../framework/roles/BACKEND_DEVELOPER|Backend Developer]] - Desenvolvedor especializado no backend do Odoo 18+

│   ├── validator/       # Code validation tools- [[../framework/roles/UXUI_DESIGNER|UX/UI Designer]] - Designer de experiência e interface do usuário

│   └── generator/       # Project generation tools

├── templates/           # Project templates### Infraestrutura e Segurança

│   ├── minimal/         # Basic project structure

│   ├── advanced/        # Full-featured modules- [[../framework/roles/DEVOPS_ENGINEER|DevOps Engineer]] - Engenheiro de operações de desenvolvimento

│   └── ecommerce/       # E-commerce specific- [[../framework/roles/SECURITY_EXPERT|Security Expert]] - Especialista em segurança para aplicações Odoo

├── examples/            # Real-world examples

│   ├── demo_project/    # Basic demo### Integração e Migração

│   └── library_system/  # Complete example

└── docs/               # This documentation- [[../framework/roles/INTEGRATION_SPECIALIST|Integration Specialist]] - Especialista em integrações com sistemas externos

    └── guides/         # Language-specific guides- [[../framework/roles/DATA_MIGRATION_SPECIALIST|Data Migration Specialist]] - Especialista em migração de dados

```

### Análise e Requisitos

## 🛠️ Essential Tools

- [[../framework/roles/BUSINESS_ANALYST|Business Analyst]] - Analista de negócios para traduzir requisitos em soluções técnicas

### Environment Management

- `./env.sh setup` - Configure Python environment## 🧰 Guias de Uso

- `./env.sh activate` - Activate environment

- `./env.sh deactivate` - Deactivate environmentGuias completos para utilização do framework em diferentes idiomas:



### Project Creation- [[guides/en/COMPLETE_GUIDE|Guia Completo (Inglês)]] - Guia completo em inglês

- `./quick_start.sh project_name` - Fast project creation- [[guides/pt/GUIA_COMPLETO|Guia Completo (Português)]] - Guia completo em português

- `./setup.sh` - Interactive full setup- [[guides/es/GUIA_COMPLETA|Guía Completa (Español)]] - Guia completo em espanhol

- `./create_odoo_project.sh` - Complete Odoo environment

## 🔎 Automação: OCA Watch & Rollups

- OCA Watch: monitoramento dos repositórios OCA configurados e geração de digests em `docs/oca-digests/` com PRs automáticos e auto-merge.
- Weekly Rollup: consolidação semanal (segunda 03:00 UTC) em `docs/oca-digests/rollups/YYYY-Www.md`.
- Execução manual na aba Actions: “OCA Watch” e “OCA Weekly Rollup”.

## 📋 Templates de Projetos

### Validation & Quality

- `python framework/validator/validate.py path/` - Validate codeTemplates prontos para criar novos projetos:
- [[guides/en/VALIDATOR_PLUGINS|Validator Plugin Guide]] - Extend the validator with custom rules
- [[guides/en/MIGRATION_GUIDE|Migration Guide 15/16/17 → 18]] - Upgrade playbook and analyzer usage

- `python framework/generator/create_project.py --name=project --type=minimal` - Generate project

- `Minimal` - Estrutura básica de projeto

## 🎯 Key Features Explained  - [[../templates/minimal/README|Documentação]]

- `Advanced` - Módulos empresariais completos

### 🤖 LLM-First Design  - [[../templates/advanced/README|Documentação]]

The framework is specifically designed for AI assistants and Large Language Models:- `E-commerce` - Módulos específicos para e-commerce

- Clear, consistent patterns  - [[../templates/ecommerce/README|Documentação]]

- SOIL (Standards-Oriented Incremental Learning) system

- Unambiguous documentation structure## 🔍 Exemplos Práticos

- AI-friendly code generation templates

Exemplos práticos para referência e aprendizado:

### ✅ Odoo 18+ Compliance

Automatically enforces modern Odoo standards:- [[../examples/README|Exemplos]] - Visão geral dos exemplos disponíveis

- Uses `<list>` instead of deprecated `<tree>` in views- [[../examples/library_system/README|Sistema de Biblioteca]] - Exemplo completo de sistema de biblioteca

- Requires `@api.depends()` decorators on computed fields

- Enforces UTF-8 encoding headers## 🛠️ Ferramentas e Utilidades

- Validates security file presence and structure

O framework fornece diversas ferramentas para facilitar o desenvolvimento:

### 📋 Template System

Three main template types:### Validação e Verificação

- **Minimal**: Basic module structure for simple needs

- **Advanced**: Complete enterprise-grade module structure- `framework/validator/validate.py` - Ferramenta de validação de arquivos e projetos

- **E-commerce**: Specialized for online commerce applications- Uso: `python framework/validator/validate.py path/to/file.py`



### 🔍 Smart Validation### Geração de Projetos

The validator checks for:

- Odoo 18+ compliance violations- `framework/generator/create_project.py` - Ferramenta para criação de novos projetos

- Missing security configurations- Uso: `python framework/generator/create_project.py --name=my_project --type=minimal`

- Deprecated patterns usage

- Code quality issues### Scripts de Configuração

- Best practices adherence

- `env.sh` - Script unificado para gerenciamento do ambiente virtual

## 🌟 Why Choose Neodoo18Framework?  - `./env.sh setup` - Configurar ambiente Python

  - `./env.sh activate` - Ativar ambiente Python

### For Developers  - `./env.sh deactivate` - Desativar ambiente Python

- **⚡ Speed**: Projects ready in minutes, not hours- `quick_start.sh` - Script para criação rápida de projetos

- **🎯 Focus**: Concentrate on business logic, not boilerplate  - `./quick_start.sh my_project` - Criar novo projeto

- **✅ Quality**: Built-in validation ensures best practices- `setup.sh` - Script interativo para configuração completa de ambiente e projeto

- **📚 Learning**: Examples and patterns teach Odoo 18+ properly- `create_odoo_project.sh` - Script para criação completa de projetos Odoo com ambiente



### For Teams## 🗂️ Estrutura de Módulos

- **🔄 Consistency**: Same structure across all projects

- **📋 Standards**: Enforced coding standards team-wideEstrutura padrão para módulos Odoo 18+ no framework:

- **🤝 Collaboration**: Clear patterns everyone understands

- **🚀 Productivity**: Faster development cycles```

my_module/

### For LLMs├── __init__.py

- **🎯 Clear Patterns**: Unambiguous code generation rules├── __manifest__.py          # Template com formato de versão Odoo 18+

- **📖 Structured Docs**: Easy to parse and understand├── models/

- **✅ Validation**: Immediate feedback on generated code│   ├── __init__.py

- **🔄 Consistency**: Same patterns always work│   └── template_model.py    # Segue os padrões do framework

├── security/

## 📦 Project Templates│   ├── ir.model.access.csv  # Obrigatório para todos os modelos

│   └── security.xml         # Grupos e regras de acesso

### Minimal Template├── views/

Basic Odoo module structure with:│   ├── views.xml           # Usa <list> ao invés de <tree>

- Simple model definition│   └── menu.xml

- Basic views (list, form, search)└── tests/

- Security configuration    └── __init__.py

- Menu structure```



### Advanced Template## ⚠️ Anti-padrões Críticos

Enterprise-ready module with:

- Complex model relationshipsPadrões que devem ser evitados:

- Advanced views and workflows

- Security groups and rules- Elementos `<tree>` (use `<list>`)

- Report templates- `view_mode="tree,form"` (use `view_mode="list,form"`)

- Wizard implementations- `@api.depends()` ausente em campos calculados

- Demo data- Cabeçalhos de codificação UTF-8 ausentes

- Arquivos de segurança incompletos (ir.model.access.csv)

### E-commerce Template- Padrões de herança inadequados

Specialized for online commerce:

- Product management## 📊 Mermaid Diagrams

- Order processing

- Payment integration patterns```mermaid

- Customer managementflowchart TD

- Inventory tracking    A[Início do Projeto] --> B{Tipo de Projeto}

    B -->|Minimal| C[Usar Template Minimal]

## 🔧 Development Workflow    B -->|Advanced| D[Usar Template Advanced]

    B -->|E-commerce| E[Usar Template E-commerce]

1. **Setup Environment**: `./env.sh setup && ./env.sh activate`    C --> F[Executar setup.sh]

2. **Create Project**: `./quick_start.sh my_project`    D --> F

3. **Develop Features**: Add your business logic    E --> F

4. **Validate Code**: `python framework/validator/validate.py my_project/`    F --> G[Desenvolvimento]

5. **Test & Deploy**: Use provided deployment guides    G --> H[Validação]

    H -->|Erros| G

## 📖 Additional Resources    H -->|Sucesso| I[Implantação]

```

- [[../README|🏠 Project Home]] - Main project README

- [[../DEPLOYMENT|🚀 Deployment Guide]] - How to deploy your projects## 🔄 Fluxo de Trabalho de Validação

- [[../CONTRIBUTING|🤝 Contributing Guide]] - How to contribute to the framework

- [[../CHANGELOG|📝 Changelog]] - What's new in each version```mermaid

sequenceDiagram

## 🆘 Need Help?    participant Dev as Desenvolvedor

    participant Val as Validator

- Check the language-specific guides above    participant Gen as Generator

- Review the examples in the `examples/` folder    participant Std as Standards

- Consult the deployment documentation    

- Open an issue on GitHub for bugs or feature requests    Dev->>Gen: Criar projeto

    Gen->>Dev: Estrutura inicial

---    Dev->>Val: Validar arquivo

    Val->>Std: Verificar conformidade

> [!TIP] Pro Tip    Std->>Val: Regras e padrões

> Start with the language-specific guide that matches your preference. Each guide contains complete step-by-step instructions tailored to different experience levels.    Val->>Dev: Erros e avisos
    Dev->>Val: Corrigir e revalidar
    Val->>Dev: Confirmação de validação
```

## 🧩 Tags e Categorização

- #odoo18
- #framework
- #desenvolvimento
- #validação
- #templates
- #padrões
- #llm
- #soil

## 🔗 Links Úteis

- [Documentação Oficial do Odoo 18](https://www.odoo.com/documentation/18.0/)
- [Comunidade Odoo](https://www.odoo.com/forum/help-1)
- [Repositório GitHub do Neodoo18Framework](https://github.com/neoand/neodoo18framework)

---

> [!TIP] Navegação Rápida
> Use o painel de navegação lateral do Obsidian ou os links acima para navegar rapidamente pela documentação.

---

Criado com ❤️ pela equipe Neodoo | Última atualização: 2025-09-26
