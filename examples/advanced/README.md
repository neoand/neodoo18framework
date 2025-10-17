# 🎯 Advanced Examples - Complete Odoo 18 Module

> **Exemplos Completos e Funcionais para Odoo 18+**
> 36 arquivos | 15.000+ linhas de código | 6.000+ linhas de comentários

---

## 📊 Visão Geral

Este diretório contém exemplos **avançados e completos** de desenvolvimento Odoo 18, cobrindo todos os aspectos desde models até frontend OWL components.

### Estatísticas:
- ✅ **36 arquivos** funcionais
- ✅ **15.000+ linhas** de código
- ✅ **6.000+ linhas** de comentários
- ✅ **80+ padrões** documentados
- ✅ **100% testado** e validado

---

## 📁 Estrutura

```
advanced/
└── complete_module/     # Módulo exemplo completo
    ├── models/          # 4 Python files
    ├── views/           # 5 XML files
    ├── security/        # 2 files
    ├── reports/         # 3 files
    ├── data/            # 2 files (automation)
    ├── wizards/         # 1 file
    ├── controllers/     # 1 file
    ├── tests/           # 3 Python files
    └── static/src/js/   # 7 files (OWL 2.0)
```

---

## 🎯 Complete Module

### 🐍 Models (4 arquivos Python)

#### 1. [model_complete_example.py](complete_module/models/model_complete_example.py) - 1334 linhas
**O exemplo mais completo de model Odoo 18:**
- 15+ field types (Char, Text, Html, Boolean, Integer, Float, Monetary, Date, etc.)
- Relational fields (Many2one, One2many, Many2many) com todos os parâmetros
- Computed fields (store, inverse, depends, recursive)
- SQL constraints (unique, check, date validation)
- 10+ compute methods com @api.depends
- 5+ constraint methods com validações complexas
- Onchange methods com warnings
- CRUD overrides (create, write, unlink, copy)
- 10+ action methods (state machine completo)
- Mail thread integration completa
- Multi-company support

#### 2. [res_config_settings_example.py](complete_module/models/res_config_settings_example.py)
**Configuration Settings completo:**
- Company settings
- Config parameters
- Computed fields
- Onchange methods
- get_values() e set_values()
- Action methods
- Helper methods

---

### 📋 Views (5 arquivos XML)

#### 1. [form_view_complete_example.xml](complete_module/views/form_view_complete_example.xml) - 485 linhas
Form view com TODOS os recursos:
- Smart buttons com statinfo
- Statusbar com states
- Web ribbon
- Button box
- Notebook com múltiplas pages
- Chatter completo
- 20+ widgets

#### 2. [list_view_example.xml](complete_module/views/list_view_example.xml) - 512 linhas
10+ tipos de list views:
- Basic, Complete, Editable
- Grouping, Readonly
- Com widgets, decorations
- Control panel buttons
- Best practices guide

#### 3. [kanban_view_example.xml](complete_module/views/kanban_view_example.xml) - 356 linhas
Kanban completo com:
- Drag and drop
- Progress bars
- Badges
- Actions

#### 4. [search_view_example.xml](complete_module/views/search_view_example.xml) - 338 linhas
Search avançado:
- Filters complexos
- Group by
- Search fields

#### 5. [chatter_usage_example.xml](complete_module/views/chatter_usage_example.xml) - 350 linhas
5 tipos de chatter:
- Basic, Customized
- Minimal, Tracked fields
- Portal view
- Python API methods

---

### 🔒 Security (2 arquivos)

#### 1. [ir.model.access.csv](complete_module/security/ir.model.access.csv)
Access rights completo:
- Public, Portal, User, Manager
- Comentários explicativos

#### 2. [record_rules.xml](complete_module/security/record_rules.xml) - 293 linhas
Record rules demonstrando:
- Global rules (multi-company)
- User rules (own + team)
- Manager rules (all access)
- Portal rules (customer)
- 8+ padrões comuns

---

### 📊 Reports (3 arquivos)

#### 1. [qweb_report_example.xml](complete_module/reports/qweb_report_example.xml) - 600+ linhas
QWeb report PDF completo:
- External layout (header/footer)
- Internal layout
- Tabelas formatadas
- Totalizadores
- Múltiplas páginas

#### 2. [report_template_example.xml](complete_module/reports/report_template_example.xml) - 800+ linhas
Template QWeb genérico:
- 5 tipos de layouts
- Todas as diretivas QWeb
- Formatação de dados completa
- CSS e estilos

#### 3. [excel_report_example.py](complete_module/reports/excel_report_example.py) - 1000+ linhas
Excel report usando xlsxwriter:
- Wizard parametrização
- Classe base reutilizável
- 14 formatos de célula
- 3 tipos de relatórios
- Gráficos (pizza, linha, coluna)

---

### 🤖 Data/Automation (2 arquivos)

#### 1. [automated_actions.xml](complete_module/data/automated_actions.xml)
11 exemplos de Automated Actions:
- Action on create, write, delete
- Python code action
- Send email action
- Create/Update record
- Multi-step actions
- Batch processing

#### 2. [scheduled_actions.xml](complete_module/data/scheduled_actions.xml)
10 cron jobs:
- Daily/Hourly/Weekly/Monthly
- Custom intervals
- Error handling
- Multi-company support

---

### 🧙 Wizards (1 arquivo)

#### [wizard_example.py](complete_module/wizards/wizard_example.py) - 709 linhas
4 tipos de wizards:
- Simple wizard
- Multi-step wizard (3 steps)
- CSV Import wizard
- Batch actions wizard

---

### 🌐 Controllers (1 arquivo)

#### [controller_example.py](complete_module/controllers/controller_example.py) - 614 linhas
HTTP Controllers demonstrando:
- Public routes
- Authenticated routes
- JSON-RPC endpoints
- CRUD completo via API
- File upload/download
- Webhooks

---

### 🧪 Tests (3 arquivos Python)

#### 1. [test_model.py](complete_module/tests/test_model.py) - 573 linhas
Unit tests completos:
- CRUD tests
- Computed fields tests
- Constraint tests
- Access rights tests

#### 2. [test_ui.py](complete_module/tests/test_ui.py) - 478 linhas
UI/Tour tests:
- Form interaction
- List view tests

#### 3. [test_performance.py](complete_module/tests/test_performance.py) - 527 linhas
Performance tests:
- Benchmarks
- Query optimization
- Load tests

---

### 💻 JavaScript/OWL (7 arquivos)

#### 1. [component_basic_example.js](complete_module/static/src/js/component_basic_example.js)
Componente básico com:
- Props validation (OWL 2.0)
- State management
- Lifecycle hooks
- Event handling

#### 2. [component_advanced_example.js](complete_module/static/src/js/component_advanced_example.js)
Componente avançado com:
- useService (ORM, action, notification)
- useRef
- useEffect
- CRUD completo

#### 3. [component_list_dashboard.js](complete_module/static/src/js/component_list_dashboard.js)
Dashboard completo:
- Filtros avançados
- Auto-refresh
- Charts ready

#### 4-7. templates.xml, menu_actions.xml, manifest_assets.xml, registry.js
Configuração completa de OWL components

---

## 🎯 Como Usar

### Referência Rápida:
```bash
# Ver estrutura completa
tree complete_module/

# Copiar arquivo específico para seu módulo
cp complete_module/models/model_complete_example.py my_module/models/

# Estudar padrões
grep -r "@api.depends" complete_module/
```

### Desenvolvimento:
1. Abra os arquivos em seu IDE
2. Estude os comentários inline
3. Copy/paste os padrões que precisa
4. Adapte para seu caso de uso

### Validação:
```bash
# Validar com neodoo validator
python3 ../../framework/validator/validate.py complete_module/

# Validar XML
xmllint --noout complete_module/views/*.xml
```

---

## 📚 Documentação Relacionada

Para teoria e guias completos, veja:
- [Knowledge Base](../../knowledge/README.md)
- [Best Practices](../../knowledge/guides/best_practices.md)
- [Cheatsheet](../../knowledge/guides/cheatsheet.md)
- [OWL Notes](../../knowledge/reference/owl_notes.md)

---

## ✅ Padrões Implementados

### Backend:
- ✅ Models completos
- ✅ Computed fields
- ✅ Constraints
- ✅ CRUD overrides
- ✅ State machines
- ✅ Mail integration
- ✅ Multi-company

### Frontend:
- ✅ Form views completas
- ✅ List views (10+ tipos)
- ✅ Kanban views
- ✅ Search views
- ✅ Chatter (5 tipos)
- ✅ OWL 2.0 components

### Reports:
- ✅ QWeb PDF
- ✅ Excel (xlsxwriter)
- ✅ Templates reutilizáveis

### Automation:
- ✅ Automated actions (11)
- ✅ Cron jobs (10)

### Security:
- ✅ Access rights
- ✅ Record rules (8+ padrões)

### Tests:
- ✅ Unit tests
- ✅ UI tests
- ✅ Performance tests

---

## 🌟 Diferenciais

### Completude:
- Cobre TODOS os aspectos do Odoo 18
- Do básico ao avançado
- Backend e frontend
- Funcional e testado

### Qualidade:
- Copy/paste ready
- Comentários inline
- Docstrings completos
- PEP 8 compliant
- Odoo 18 guidelines

### Praticidade:
- Exemplos funcionais
- Patterns reutilizáveis
- Debugging helpers
- Performance tips

---

## 🤝 Contribuindo

Quer adicionar mais exemplos? Veja [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

## 📝 Licença

LGPL-3 (seguindo Odoo licensing)

---

**Criado com ❤️ para a comunidade Odoo**
**Data de criação:** 2025-10-16
**Data de integração:** 2025-10-17
**Versão:** 2.0

---

> [!TIP]
> **Comece por:** model_complete_example.py → views/ → OWL components

> [!NOTE]
> Todos os arquivos são copy/paste ready!
