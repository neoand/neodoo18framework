# Índice de Exemplos OWL - Odoo 18

## 📋 Arquivos Criados

### 📁 Componentes JavaScript

#### 1. **component_basic_example.js**
**Localização:** `/examples/static/src/js/component_basic_example.js`

**Conteúdo:**
- Props validation com `static props` (OWL 2.0)
- State management com `useState`
- Lifecycle hooks: `onWillStart`, `onMounted`, `onWillUnmount`
- Event handlers
- Computed properties (getters)
- Form handling e two-way binding
- Manipulação de listas dinâmicas

**Props:**
```javascript
{
    title: String,              // Obrigatório
    subtitle: String,           // Opcional
    maxCount: Number,           // Opcional (padrão: 100)
    initialCounter: Number,     // Opcional (padrão: 0)
    onSave: Function,          // Callback opcional
}
```

---

#### 2. **component_advanced_example.js**
**Localização:** `/examples/static/src/js/component_advanced_example.js`

**Conteúdo:**
- `useService`: ORM, action, notification, rpc
- `useRef` para manipulação de DOM
- `useEffect` para side effects
- Operações CRUD completas (create, read, update, delete)
- Comunicação entre componentes (props/events)
- Integração com backend via ORM
- Search com debounce automático
- Paginação avançada
- Error handling robusto

**Props:**
```javascript
{
    resModel: String,              // Model do Odoo (obrigatório)
    domain: Array,                 // Domain de filtro
    context: Object,               // Context adicional
    viewMode: String,              // Modo de visualização
    onRecordSelected: Function,    // Callbacks
    allowCreate: Boolean,          // Permissões
    allowEdit: Boolean,
    allowDelete: Boolean,
}
```

---

#### 3. **component_list_dashboard.js**
**Localização:** `/examples/static/src/js/component_list_dashboard.js`

**Conteúdo:**
- Dashboard completo e funcional
- Busca de dados via ORM com múltiplos models
- Filtros avançados (search, categoria, parceiro, datas)
- Cards interativos com múltiplas views
- Estatísticas em tempo real
- Gráficos (preparado para Chart.js)
- Actions (doAction) para drill-down
- Auto-refresh configurável
- Export de dados
- Ordenação e paginação customizável

**Props:**
```javascript
{
    resModel: String,           // Model principal (obrigatório)
    title: String,              // Título do dashboard
    domain: Array,              // Domain base
    fields: Array,              // Campos a buscar
    showStatistics: Boolean,    // Mostrar estatísticas
    showCharts: Boolean,        // Mostrar gráficos
    showFilters: Boolean,       // Mostrar filtros
    onRecordClick: Function,    // Callbacks
}
```

---

#### 4. **registry.js**
**Localização:** `/examples/static/src/js/registry.js`

**Conteúdo:**
- Registro de componentes no Odoo registry
- Exemplos de diferentes tipos de registry:
  - Client Actions
  - Field Widgets
  - Systray Items
  - Services
  - Views customizadas
  - Command Palette Providers
- Utility functions para gerenciar registros
- Documentação completa de debugging

**Funções principais:**
```javascript
registerComponents(components, category)
isComponentRegistered(tag, category)
getRegisteredComponents(category)
```

---

### 📁 Templates XML

#### 5. **templates.xml**
**Localização:** `/examples/views/templates.xml`

**Conteúdo:**
- Template completo para ComponentBasicExample
- Template completo para ComponentAdvancedExample
- Template completo para ComponentListDashboard
- Exemplos de:
  - Data binding (`t-esc`, `t-out`, `t-att-*`)
  - Loops (`t-foreach`, `t-as`, `t-key`)
  - Condicionais (`t-if`, `t-elif`, `t-else`)
  - Event handlers (`t-on-click`, `t-on-submit`)
  - Refs (`t-ref`)
  - Classes dinâmicas
  - Bootstrap 5 components

---

#### 6. **menu_actions.xml**
**Localização:** `/examples/views/menu_actions.xml`

**Conteúdo:**
- 8 Client Actions completas de exemplo
- Estrutura de menus hierárquica
- Exemplos de diferentes targets:
  - `current` - View principal
  - `new` - Modal
  - `fullscreen` - Tela cheia
- Exemplos de params e context
- Documentação inline de como usar actions programaticamente
- Exemplos de segurança e permissões

**Actions incluídas:**
1. Componente Básico (current)
2. Componente Avançado - Partners
3. Componente Avançado - Products
4. Dashboard - Sales
5. Dashboard - Invoices
6. Dashboard - Tasks
7. Componente Modal
8. Dashboard Fullscreen

---

#### 7. **manifest_assets.xml**
**Localização:** `/examples/views/manifest_assets.xml`

**Conteúdo:**
- Guia completo de como configurar __manifest__.py
- 4 exemplos diferentes de manifests:
  1. Básico
  2. Avançado com organização
  3. Com lazy loading
  4. Menu actions
- Estrutura de pastas recomendada
- Dicas de performance
- Explicação de target options
- Diferença entre params e context
- Comandos de instalação e debug

---

### 📁 Documentação

#### 8. **README.md**
**Localização:** `/examples/README.md`

**Conteúdo:**
- Visão geral completa do projeto
- Descrição detalhada de cada componente
- Guia de instalação passo a passo
- Conceitos importantes do OWL 2.0:
  - Setup method
  - Props validation
  - State management
  - Services (hooks)
  - ORM operations
  - useEffect
  - useRef
- Templates QWeb
- Troubleshooting
- Recursos adicionais

---

#### 9. **__manifest__.py**
**Localização:** `/examples/__manifest__.py`

**Conteúdo:**
- Manifest completo e funcional
- Configuração de assets correta
- Dependencies necessárias
- Metadata do módulo
- Assets organizados por categoria
- Comentários explicativos
- Hooks de exemplo
- Notas de instalação e debugging

---

#### 10. **INDEX.md** (este arquivo)
**Localização:** `/examples/INDEX.md`

**Conteúdo:**
- Índice de todos os arquivos criados
- Resumo do conteúdo de cada arquivo
- Links de navegação rápida

---

## 🗂️ Estrutura Completa de Pastas

```
examples/
├── __init__.py                                    # (criar se necessário)
├── __manifest__.py                                # Manifest do módulo ✅
├── README.md                                      # Documentação principal ✅
├── INDEX.md                                       # Este arquivo ✅
│
├── static/
│   └── src/
│       ├── js/
│       │   ├── registry.js                        # Registry dos componentes ✅
│       │   ├── component_basic_example.js         # Componente básico ✅
│       │   ├── component_advanced_example.js      # Componente avançado ✅
│       │   └── component_list_dashboard.js        # Dashboard ✅
│       │
│       └── xml/
│           └── templates.xml                      # Templates QWeb ✅
│
└── views/
    ├── menu_actions.xml                           # Actions e menus ✅
    └── manifest_assets.xml                        # Guia de assets ✅
```

---

## 🚀 Como Usar

### 1. Copiar para seu módulo Odoo

```bash
# Copiar estrutura completa
cp -r examples/ /path/to/odoo/addons/odoo_examples/

# Ou copiar arquivos individualmente conforme necessário
```

### 2. Ajustar paths no __manifest__.py

Se você mudar o nome do módulo de `odoo_examples` para outro:

```python
# Trocar todas as ocorrências de 'odoo_examples' por 'seu_modulo'
'assets': {
    'web.assets_backend': [
        'seu_modulo/static/src/js/registry.js',
        # ...
    ],
}
```

### 3. Ajustar XML IDs no registry.js

```javascript
// Trocar prefixo
actionRegistry.add("seu_modulo.ComponentBasicExample", ComponentBasicExample);
```

### 4. Instalar módulo

```bash
# Modo desenvolvimento
odoo-bin -c odoo.conf -d mydb -i seu_modulo --dev=all

# Modo produção
odoo-bin -c odoo.conf -d mydb -i seu_modulo
```

---

## 📚 Guias Rápidos

### Criar novo componente básico

1. Copiar `component_basic_example.js`
2. Renomear classe e modificar props
3. Criar template XML correspondente
4. Registrar no `registry.js`
5. Adicionar ao manifest em `assets`
6. Criar client action no XML

### Criar dashboard customizado

1. Copiar `component_list_dashboard.js`
2. Ajustar `resModel` e fields
3. Customizar filtros específicos
4. Ajustar estatísticas e charts
5. Registrar e criar action

### Integrar com backend

1. Ver exemplos em `component_advanced_example.js`
2. Usar `useService("orm")` para operações
3. Implementar error handling
4. Adicionar notificações

---

## 🔍 Conceitos por Arquivo

### Registry (registry.js)
- ✅ Como registrar componentes
- ✅ Diferentes categorias de registry
- ✅ Utility functions
- ✅ Debugging

### Básico (component_basic_example.js)
- ✅ Props e validation
- ✅ State management
- ✅ Lifecycle hooks
- ✅ Event handling
- ✅ Computed properties

### Avançado (component_advanced_example.js)
- ✅ Services (ORM, action, notification, rpc)
- ✅ useRef e DOM manipulation
- ✅ useEffect e dependencies
- ✅ CRUD operations
- ✅ Error handling

### Dashboard (component_list_dashboard.js)
- ✅ Multi-model data loading
- ✅ Advanced filtering
- ✅ Multiple view modes
- ✅ Statistics
- ✅ Charts integration
- ✅ Auto-refresh
- ✅ Export

### Templates (templates.xml)
- ✅ QWeb syntax
- ✅ Data binding
- ✅ Loops e condicionais
- ✅ Event handlers
- ✅ Bootstrap integration

### Actions (menu_actions.xml)
- ✅ Client actions
- ✅ Menu structure
- ✅ Params vs Context
- ✅ Target options
- ✅ Security

---

## 📊 Estatísticas

### Linhas de Código

| Arquivo | Linhas | Comentários | Código |
|---------|--------|-------------|--------|
| component_basic_example.js | ~500 | ~250 | ~250 |
| component_advanced_example.js | ~850 | ~400 | ~450 |
| component_list_dashboard.js | ~1000 | ~400 | ~600 |
| registry.js | ~600 | ~400 | ~200 |
| templates.xml | ~800 | ~100 | ~700 |
| menu_actions.xml | ~600 | ~400 | ~200 |
| manifest_assets.xml | ~600 | ~500 | ~100 |
| __manifest__.py | ~300 | ~150 | ~150 |
| README.md | ~600 | - | - |
| **TOTAL** | **~5,850** | **~2,600** | **~2,650** |

### Cobertura de Conceitos

#### OWL 2.0
- [x] setup() method
- [x] static props
- [x] useState
- [x] useRef
- [x] useEffect
- [x] useService
- [x] onWillStart
- [x] onMounted
- [x] onWillUnmount
- [x] Computed properties
- [x] Event handling

#### Odoo Services
- [x] ORM (searchRead, create, write, unlink, call, readGroup)
- [x] Action (doAction)
- [x] Notification
- [x] RPC
- [x] User

#### Templates QWeb
- [x] t-esc / t-out
- [x] t-att-*
- [x] t-if / t-elif / t-else
- [x] t-foreach / t-as / t-key
- [x] t-on-* (eventos)
- [x] t-ref
- [x] t-model

#### Recursos
- [x] Props validation
- [x] State management
- [x] Lifecycle management
- [x] CRUD operations
- [x] Filtering e search
- [x] Pagination
- [x] Statistics
- [x] Charts (preparado)
- [x] Auto-refresh
- [x] Error handling
- [x] Multi-view support

---

## 🎯 Casos de Uso

### 1. Criar dashboard simples
**Arquivo:** `component_list_dashboard.js`
**Tempo:** 15-30 min
**Dificuldade:** ⭐⭐

### 2. Form customizado com validação
**Arquivo:** `component_basic_example.js`
**Tempo:** 10-20 min
**Dificuldade:** ⭐

### 3. Gerenciador CRUD completo
**Arquivo:** `component_advanced_example.js`
**Tempo:** 30-60 min
**Dificuldade:** ⭐⭐⭐

### 4. Integração com API externa
**Arquivo:** `component_advanced_example.js` (rpc)
**Tempo:** 20-40 min
**Dificuldade:** ⭐⭐⭐

### 5. Systray customizado
**Arquivo:** `registry.js` (exemplo comentado)
**Tempo:** 15-25 min
**Dificuldade:** ⭐⭐

### 6. Field widget customizado
**Arquivo:** `registry.js` (exemplo comentado)
**Tempo:** 20-30 min
**Dificuldade:** ⭐⭐

---

## 🐛 Debugging

### Console do Browser

```javascript
// Ver todos os componentes registrados
const { registry } = odoo.__DEBUG__.services;
console.log(registry.category("actions").getEntries());

// Ver componente específico
console.log(registry.category("actions").get("odoo_examples.ComponentBasicExample"));

// Testar ORM
const { orm } = odoo.__DEBUG__.services;
await orm.searchRead("res.partner", [], ["name"]);
```

### Odoo CLI

```bash
# Modo debug completo
odoo-bin --dev=all

# Debug apenas XML/JS
odoo-bin --dev=xml,js

# Ver logs detalhados
odoo-bin --log-level=debug
```

### Browser DevTools

1. Abrir DevTools (F12)
2. Sources → encontrar arquivo em `odoo_examples/static/src/js/`
3. Adicionar breakpoints
4. Recarregar página
5. Inspecionar state/props

---

## ✅ Checklist de Implementação

### Setup Inicial
- [ ] Copiar arquivos para addons
- [ ] Ajustar nome do módulo
- [ ] Configurar __manifest__.py
- [ ] Criar __init__.py se necessário

### Desenvolvimento
- [ ] Escolher componente base
- [ ] Customizar props
- [ ] Implementar lógica
- [ ] Criar template XML
- [ ] Registrar no registry
- [ ] Adicionar ao manifest

### Testing
- [ ] Instalar módulo (--dev=all)
- [ ] Testar funcionalidades
- [ ] Verificar console para erros
- [ ] Testar em diferentes browsers
- [ ] Validar responsividade

### Deploy
- [ ] Remover console.logs
- [ ] Otimizar assets
- [ ] Atualizar documentação
- [ ] Testar em produção
- [ ] Monitorar logs

---

## 📞 Recursos Adicionais

### Documentação Oficial
- [OWL Framework](https://github.com/odoo/owl)
- [Odoo 18 Docs](https://www.odoo.com/documentation/18.0/)
- [JavaScript Framework](https://www.odoo.com/documentation/18.0/developer/reference/frontend/javascript_reference.html)

### Community
- [Odoo Forum](https://www.odoo.com/forum)
- [OCA GitHub](https://github.com/OCA)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/odoo)

### Tutoriais
- README.md neste repositório
- Comentários inline nos arquivos JS
- Exemplos XML documentados

---

**Desenvolvido para a comunidade Odoo 🚀**

*Última atualização: 2025-10-17*
