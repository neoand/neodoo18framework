# -*- coding: utf-8 -*-
{
    'name': 'OWL Examples - Odoo 18',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Exemplos completos de componentes OWL 2.0 para Odoo 18',
    'description': """
        Odoo 18 - OWL Components Examples
        ==================================

        Este módulo contém exemplos completos e bem documentados de componentes
        OWL 2.0 para Odoo 18, incluindo:

        Componentes Básicos:
        -------------------
        * Props validation (OWL 2.0)
        * State management com useState
        * Lifecycle hooks (onWillStart, onMounted, onWillUnmount)
        * Event handling
        * Computed properties
        * Form handling e two-way binding

        Componentes Avançados:
        --------------------
        * useService (ORM, action, notification, rpc)
        * useRef para DOM manipulation
        * useEffect para side effects
        * Operações CRUD completas
        * Comunicação entre componentes
        * Integração com backend
        * Search com debounce
        * Paginação e filtros

        Dashboards:
        ----------
        * Busca de dados via ORM
        * Filtros avançados (search, categoria, parceiro, datas)
        * Lista de cards interativos
        * Visualizações múltiplas (cards, list, kanban)
        * Estatísticas em tempo real
        * Gráficos (Chart.js ready)
        * Actions para drill-down
        * Auto-refresh configurável
        * Export de dados

        Funcionalidades:
        ---------------
        * Todos os componentes seguem boas práticas OWL 2.0
        * Código extensamente comentado em português
        * Exemplos de uso incluídos
        * Templates QWeb completos
        * Guia de registro de assets
        * Documentação completa no README.md

        Requisitos:
        ----------
        * Odoo 18.0+
        * OWL 2.0 (incluído no Odoo 18)

        Autor: Odoo Community
        Licença: LGPL-3
    """,
    'author': 'Odoo Community',
    'website': 'https://www.odoo.com',
    'license': 'LGPL-3',

    # Dependências
    'depends': [
        'base',          # Módulo base do Odoo
        'web',           # Framework web e OWL
        'mail',          # Para chatter (opcional)
        'sale',          # Para exemplos de dashboard (opcional)
        'account',       # Para exemplos de faturas (opcional)
        'project',       # Para exemplos de tarefas (opcional)
    ],

    # Dados XML
    'data': [
        # Segurança (se houver models)
        # 'security/ir.model.access.csv',

        # Views
        'views/templates.xml',
        'views/menu_actions.xml',
    ],

    # Assets JS/CSS/XML
    'assets': {
        # ========================================
        # Backend Assets (Interface Principal)
        # ========================================
        'web.assets_backend': [
            # === CORE ===
            # Registry deve ser carregado PRIMEIRO
            'odoo_examples/static/src/js/registry.js',

            # === COMPONENTS ===
            # Componentes em ordem de dependência
            'odoo_examples/static/src/js/component_basic_example.js',
            'odoo_examples/static/src/js/component_advanced_example.js',
            'odoo_examples/static/src/js/component_list_dashboard.js',

            # === TEMPLATES XML ===
            # Templates devem vir DEPOIS dos componentes JS
            'odoo_examples/static/src/xml/templates.xml',

            # === STYLES (se houver) ===
            # 'odoo_examples/static/src/scss/main.scss',
            # 'odoo_examples/static/src/css/dashboard.css',
        ],

        # ========================================
        # Frontend Assets (Portal/Website)
        # ========================================
        'web.assets_frontend': [
            # Assets para o website público (se necessário)
            # 'odoo_examples/static/src/js/frontend/*.js',
            # 'odoo_examples/static/src/css/frontend.css',
        ],

        # ========================================
        # Assets de Testes
        # ========================================
        'web.assets_tests': [
            # Testes JavaScript (se houver)
            # 'odoo_examples/static/tests/**/*.js',
        ],

        # ========================================
        # Assets Específicos de Produção
        # ========================================
        'web.assets_backend_prod_only': [
            # Assets apenas para produção (analytics, etc)
            # 'odoo_examples/static/src/js/analytics.js',
        ],
    },

    # Demonstração/Demo data
    'demo': [
        # 'demo/demo_data.xml',
    ],

    # Imagens
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/screenshot_basic.png',
        'static/description/screenshot_advanced.png',
        'static/description/screenshot_dashboard.png',
    ],

    # Configurações do módulo
    'installable': True,
    'application': True,  # Aparece como app no Apps menu
    'auto_install': False,
    'sequence': 100,

    # Preço (se for módulo pago)
    # 'price': 0.00,
    # 'currency': 'EUR',

    # External dependencies
    'external_dependencies': {
        'python': [
            # 'requests',  # exemplo
        ],
        'bin': [
            # 'wkhtmltopdf',  # exemplo
        ],
    },

    # Post init hook (executado após instalação)
    # 'post_init_hook': '_post_init_hook',

    # Uninstall hook (executado antes de desinstalar)
    # 'uninstall_hook': '_uninstall_hook',
}


# ================================================================
# HOOKS (se necessário)
# ================================================================

# def _post_init_hook(cr, registry):
#     """
#     Executado após instalação do módulo.
#     Útil para:
#     - Inicializar dados
#     - Configurações iniciais
#     - Migrações
#     """
#     from odoo import api, SUPERUSER_ID
#
#     env = api.Environment(cr, SUPERUSER_ID, {})
#
#     # Exemplo: criar registros iniciais
#     # env['res.partner'].create({
#     #     'name': 'Demo Partner',
#     #     'is_company': True,
#     # })
#
#     print("OWL Examples: Post-install hook executed")


# def _uninstall_hook(cr, registry):
#     """
#     Executado antes de desinstalar o módulo.
#     Útil para:
#     - Cleanup de dados
#     - Remoção de configurações
#     """
#     from odoo import api, SUPERUSER_ID
#
#     env = api.Environment(cr, SUPERUSER_ID, {})
#
#     print("OWL Examples: Uninstall hook executed")


# ================================================================
# NOTAS IMPORTANTES
# ================================================================

"""
ESTRUTURA DE PASTAS:
-------------------
odoo_examples/
├── __init__.py
├── __manifest__.py  # Este arquivo
│
├── models/
│   ├── __init__.py
│   └── example_model.py  # Models Python (se houver)
│
├── views/
│   ├── templates.xml
│   └── menu_actions.xml
│
├── security/
│   └── ir.model.access.csv
│
├── static/
│   ├── description/
│   │   ├── icon.png
│   │   ├── banner.png
│   │   └── index.html  # Descrição do módulo
│   │
│   └── src/
│       ├── js/
│       │   ├── registry.js
│       │   ├── component_basic_example.js
│       │   ├── component_advanced_example.js
│       │   └── component_list_dashboard.js
│       │
│       ├── xml/
│       │   └── templates.xml
│       │
│       ├── scss/
│       │   └── main.scss
│       │
│       └── css/
│           └── styles.css
│
├── demo/
│   └── demo_data.xml
│
└── tests/
    ├── __init__.py
    └── test_components.py


ORDEM DE CARREGAMENTO DOS ASSETS:
--------------------------------
1. registry.js (SEMPRE PRIMEIRO)
   - Registra componentes no Odoo

2. Componentes JS
   - Em ordem de dependência
   - Componentes base antes dos complexos

3. Templates XML
   - SEMPRE APÓS os componentes JS
   - Templates precisam dos componentes registrados

4. Styles (SCSS/CSS)
   - Por último
   - Não afetam funcionalidade


BOAS PRÁTICAS:
-------------
1. Use XML ID único e descritivo:
   - odoo_examples.ComponentBasicExample ✓
   - basic_example ✗ (muito genérico)

2. Organize assets por funcionalidade:
   - Agrupe componentes relacionados
   - Use wildcards com cuidado (* pode incluir arquivos não desejados)

3. Minimize dependências:
   - Só inclua 'depends' necessários
   - Dependências desnecessárias deixam o módulo mais pesado

4. Versionamento:
   - Use semver: 18.0.1.0.0
   - Versão Odoo + versão do módulo

5. Documentação:
   - Mantenha 'description' atualizado
   - Inclua README.md
   - Comente código complexo


INSTALAÇÃO:
----------
# Desenvolvimento (sem cache)
odoo-bin -c odoo.conf -d mydb -i odoo_examples --dev=all

# Produção
odoo-bin -c odoo.conf -d mydb -i odoo_examples

# Atualizar
odoo-bin -c odoo.conf -d mydb -u odoo_examples

# Atualizar apenas assets
odoo-bin -c odoo.conf -d mydb -u odoo_examples --dev=xml,js


DEBUGGING:
---------
# No browser (com ?debug=assets):
console.log(odoo.__DEBUG__.services.registry.category("actions").getEntries());

# Ver componentes registrados
const { registry } = odoo.__DEBUG__.services;
console.log(registry.category("actions").get("odoo_examples.ComponentBasicExample"));

# Forçar reload de assets
- Adicionar ?debug=assets na URL
- Ctrl+F5 (hard refresh)
- Atualizar módulo com --dev=all


TROUBLESHOOTING:
---------------
Problema: Componente não aparece
Solução:
1. Verificar se está em 'assets' do manifest
2. Verificar se está registrado no registry.js
3. Limpar cache: --dev=all
4. Ver console do browser para erros

Problema: Templates não carregam
Solução:
1. Em Odoo 18, templates vão em web.assets_backend
2. Verificar t-name único
3. Atualizar com --dev=xml

Problema: Props não funcionam
Solução:
1. Verificar static props definition
2. Props em XML: title="'String'" (note as aspas)
3. Arrays precisam eval: domain="[[]]"

Problema: State não atualiza
Solução:
1. Usar useState()
2. Para arrays/objects: criar nova referência
3. Não mutar state diretamente
"""
