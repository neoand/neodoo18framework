# Exemplos de Componentes OWL para Odoo 18

Este diretório contém exemplos completos e bem documentados de componentes OWL 2.0 para Odoo 18, incluindo componentes básicos, avançados e dashboards completos.

## 📁 Estrutura de Arquivos

```
examples/
├── static/src/js/
│   ├── component_basic_example.js      # Componente básico com fundamentos OWL
│   ├── component_advanced_example.js   # Componente avançado com ORM e services
│   ├── component_list_dashboard.js     # Dashboard completo com filtros e charts
│   └── registry.js                     # Registro de componentes no Odoo
│
├── views/
│   ├── templates.xml                   # Templates QWeb para os componentes
│   └── manifest_assets.xml             # Guia de como registrar assets
│
└── README.md                           # Este arquivo
```

## 🎯 Componentes Incluídos

### 1. ComponentBasicExample (`component_basic_example.js`)

**Componente básico demonstrando:**
- ✅ Props validation com `static props` (OWL 2.0)
- ✅ State management com `useState`
- ✅ Lifecycle hooks (`onWillStart`, `onMounted`, `onWillUnmount`)
- ✅ Event handling
- ✅ Computed properties (getters)
- ✅ Form handling e two-way binding
- ✅ Lista dinâmica de items

**Props aceitas:**
```javascript
{
    title: String,              // Obrigatório
    subtitle: String,           // Opcional
    maxCount: Number,           // Opcional (padrão: 100)
    initialCounter: Number,     // Opcional (padrão: 0)
    onSave: Function,          // Callback opcional
}
```

**Como usar:**
```xml
<t t-component="ComponentBasicExample"
   title="'Meu Título'"
   maxCount="50"
   onSave="onSaveHandler" />
```

---

### 2. ComponentAdvancedExample (`component_advanced_example.js`)

**Componente avançado demonstrando:**
- ✅ `useService` (ORM, action, notification, rpc)
- ✅ `useRef` para manipulação de DOM
- ✅ `useEffect` para side effects
- ✅ Operações CRUD completas (create, read, update, delete)
- ✅ Comunicação entre componentes (props/events)
- ✅ Integração com backend via ORM
- ✅ Search com debounce
- ✅ Paginação
- ✅ Error handling robusto

**Props aceitas:**
```javascript
{
    resModel: String,              // Model do Odoo (obrigatório)
    domain: Array,                 // Domain de filtro (opcional)
    context: Object,               // Context adicional (opcional)
    viewMode: String,              // Modo de visualização (opcional)
    onRecordSelected: Function,    // Callback ao selecionar (opcional)
    onRecordCreated: Function,     // Callback ao criar (opcional)
    onRecordDeleted: Function,     // Callback ao deletar (opcional)
    allowCreate: Boolean,          // Permite criar (opcional)
    allowEdit: Boolean,            // Permite editar (opcional)
    allowDelete: Boolean,          // Permite deletar (opcional)
}
```

**Como usar:**
```xml
<ComponentAdvancedExample
    resModel="'res.partner'"
    domain="[[['customer_rank', '>', 0]]]"
    allowCreate="true"
    onRecordSelected="onRecordSelected" />
```

---

### 3. ComponentListDashboard (`component_list_dashboard.js`)

**Dashboard completo demonstrando:**
- ✅ Busca de dados via ORM com múltiplos models
- ✅ Filtros avançados (search, categoria, parceiro, datas)
- ✅ Lista de cards interativos
- ✅ Visualizações múltiplas (cards, list, kanban)
- ✅ Estatísticas em tempo real
- ✅ Gráficos (preparado para Chart.js)
- ✅ Actions (`doAction`) para drill-down
- ✅ Auto-refresh configurável
- ✅ Export de dados
- ✅ Ordenação e paginação avançada

**Props aceitas:**
```javascript
{
    resModel: String,           // Model principal (obrigatório)
    title: String,              // Título do dashboard (opcional)
    domain: Array,              // Domain base (opcional)
    context: Object,            // Context (opcional)
    fields: Array,              // Campos a buscar (opcional)
    showStatistics: Boolean,    // Mostrar estatísticas (opcional)
    showCharts: Boolean,        // Mostrar gráficos (opcional)
    showFilters: Boolean,       // Mostrar filtros (opcional)
    onRecordClick: Function,    // Callback ao clicar (opcional)
}
```

**Como usar:**
```xml
<ComponentListDashboard
    resModel="'sale.order'"
    title="'Dashboard de Vendas'"
    showStatistics="true"
    showCharts="true" />
```

---

## 🚀 Como Usar os Exemplos

### Passo 1: Copiar arquivos para seu módulo

```bash
# Estrutura mínima necessária
your_module/
├── __init__.py
├── __manifest__.py
├── static/src/
│   ├── js/
│   │   ├── component_basic_example.js
│   │   ├── component_advanced_example.js
│   │   ├── component_list_dashboard.js
│   │   └── registry.js
│   └── xml/
│       └── templates.xml
└── views/
    └── menu_actions.xml
```

### Passo 2: Configurar `__manifest__.py`

```python
{
    'name': 'Seu Módulo',
    'version': '18.0.1.0.0',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'views/menu_actions.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # JavaScript
            'your_module/static/src/js/registry.js',
            'your_module/static/src/js/component_basic_example.js',
            'your_module/static/src/js/component_advanced_example.js',
            'your_module/static/src/js/component_list_dashboard.js',

            # Templates
            'your_module/static/src/xml/templates.xml',
        ],
    },
}
```

### Passo 3: Criar Client Actions (XML)

```xml
<!-- views/menu_actions.xml -->
<odoo>
    <data>
        <!-- Action para Dashboard -->
        <record id="action_dashboard" model="ir.actions.client">
            <field name="name">Meu Dashboard</field>
            <field name="tag">odoo_examples.ComponentListDashboard</field>
            <field name="params" eval="{
                'resModel': 'sale.order',
                'title': 'Dashboard de Vendas',
                'showStatistics': True,
                'showCharts': True,
            }"/>
        </record>

        <!-- Menu -->
        <menuitem id="menu_dashboard"
                  name="Dashboard"
                  action="action_dashboard"/>
    </data>
</odoo>
```

### Passo 4: Instalar/Atualizar módulo

```bash
# Modo desenvolvimento (sem cache)
odoo-bin -c odoo.conf -d mydb -u your_module --dev=all

# Ou modo normal
odoo-bin -c odoo.conf -d mydb -u your_module
```

---

## 📚 Conceitos Importantes do OWL 2.0

### 1. Setup Method
No OWL 2.0, toda lógica de inicialização vai no método `setup()`:

```javascript
setup() {
    // State
    this.state = useState({ ... });

    // Services
    this.orm = useService("orm");

    // Refs
    this.myRef = useRef("myElement");

    // Effects
    useEffect(() => { ... }, () => [dependencies]);

    // Lifecycle
    onWillStart(async () => { ... });
    onMounted(() => { ... });
}
```

### 2. Props Validation
Props são validadas estaticamente:

```javascript
static props = {
    title: { type: String },                    // Obrigatório
    count: { type: Number, optional: true },    // Opcional
    items: { type: Array, optional: true },     // Array opcional
    onSave: { type: Function, optional: true }, // Callback
};
```

### 3. State Management
Use `useState` para state reativo:

```javascript
setup() {
    this.state = useState({
        counter: 0,
        items: [],
    });
}

// Atualização automática de UI
increment() {
    this.state.counter++;  // UI atualiza automaticamente
}

// Arrays: criar nova referência
addItem(item) {
    this.state.items = [...this.state.items, item];
}
```

### 4. Services (Hooks)
Principais services do Odoo 18:

```javascript
setup() {
    // ORM - operações de banco
    this.orm = useService("orm");

    // Action - executar actions
    this.action = useService("action");

    // Notification - notificações
    this.notification = useService("notification");

    // RPC - chamadas customizadas
    this.rpc = useService("rpc");

    // User - info do usuário
    this.user = useService("user");

    // Dialog - diálogos
    this.dialog = useService("dialog");
}
```

### 5. ORM Operations

```javascript
// Search & Read
const records = await this.orm.searchRead(
    "res.partner",
    [["customer_rank", ">", 0]],
    ["name", "email"],
    { limit: 10, order: "name" }
);

// Create
const id = await this.orm.create("res.partner", [values]);

// Write
await this.orm.write("res.partner", [id], values);

// Unlink
await this.orm.unlink("res.partner", [id]);

// Call method
const result = await this.orm.call(
    "res.partner",
    "my_method",
    [args],
    { kwargs }
);

// Read Group
const groups = await this.orm.readGroup(
    "sale.order",
    domain,
    ["partner_id", "amount_total:sum"],
    ["partner_id"]
);
```

### 6. useEffect Hook
Para side effects e dependências:

```javascript
setup() {
    // Effect executado quando searchTerm muda
    useEffect(
        () => {
            console.log("Search changed:", this.state.searchTerm);

            // Cleanup (opcional)
            return () => {
                console.log("Cleanup");
            };
        },
        () => [this.state.searchTerm]  // Dependencies
    );
}
```

### 7. useRef Hook
Para acessar elementos DOM:

```javascript
setup() {
    this.inputRef = useRef("myInput");

    onMounted(() => {
        // Acessa elemento DOM
        if (this.inputRef.el) {
            this.inputRef.el.focus();
        }
    });
}
```

Template:
```xml
<input t-ref="myInput" type="text"/>
```

---

## 🎨 Templates QWeb

### Binding de dados
```xml
<!-- Texto simples -->
<t t-esc="state.name"/>

<!-- HTML (cuidado com XSS) -->
<t t-out="state.htmlContent"/>

<!-- Atributos -->
<div t-att-class="state.isActive ? 'active' : ''"/>
<button t-att-disabled="!canSave"/>
```

### Loops
```xml
<t t-foreach="state.items" t-as="item" t-key="item.id">
    <div><t t-esc="item.name"/></div>
</t>
```

### Condicionais
```xml
<t t-if="state.loading">Carregando...</t>
<t t-elif="state.error">Erro!</t>
<t t-else="">Conteúdo normal</t>
```

### Event Handlers
```xml
<!-- Método simples -->
<button t-on-click="onSave">Salvar</button>

<!-- Com parâmetros (arrow function) -->
<button t-on-click="() => this.onDelete(record.id)">Deletar</button>

<!-- Prevenir default -->
<form t-on-submit="onSubmit">...</form>

<!-- Stop propagation -->
<button t-on-click.stop="onClick">Click</button>
```

---

## 🔧 Troubleshooting

### Componente não aparece
1. Verificar se está registrado no `registry.js`
2. Verificar se o arquivo está em `assets` do manifest
3. Limpar cache: `--dev=all` ou `?debug=assets`
4. Verificar console do browser para erros

### Props não funcionam
1. Verificar `static props` definition
2. Props em XML devem usar sintaxe correta: `title="'String'"`
3. Arrays/Objects precisam de `eval` ou serem JSON válido

### State não atualiza UI
1. Usar `useState()` para criar state
2. Para arrays/objects, criar nova referência: `[...array]`
3. Não mutar state diretamente em nested objects

### ORM operations falham
1. Verificar permissões do usuário
2. Verificar domain syntax
3. Verificar se model existe
4. Ver logs do Odoo para erros Python

### Templates não carregam
1. Em Odoo 18, templates vão em `web.assets_backend`
2. Verificar `t-name` é único
3. Recarregar assets: atualizar módulo com `--dev=xml`

---

## 📖 Recursos Adicionais

### Documentação Oficial
- [OWL Framework](https://github.com/odoo/owl)
- [Odoo JS Framework](https://www.odoo.com/documentation/18.0/developer/reference/frontend/javascript_reference.html)

### Debugging
```javascript
// No console do browser (com ?debug=assets)
const { registry } = odoo.__DEBUG__.services;

// Ver componentes registrados
console.log(registry.category("actions").getEntries());

// Testar ORM
const { orm } = odoo.__DEBUG__.services;
await orm.searchRead("res.partner", [], ["name"]);
```

### Performance Tips
1. Use `useEffect` com dependencies corretas
2. Memoize computed properties caras
3. Lazy load componentes grandes
4. Use `readGroup` em vez de `searchRead` + reduce
5. Limite fields no `searchRead`

---

## 🤝 Contribuindo

Estes exemplos são de código aberto. Sinta-se livre para:
- Reportar issues
- Sugerir melhorias
- Adicionar mais exemplos
- Fazer fork e adaptar

---

## 📝 Licença

LGPL-3 (mesma do Odoo)

---

## 📞 Suporte

Para dúvidas sobre Odoo 18 e OWL:
- Fórum Odoo: https://www.odoo.com/forum
- GitHub OWL: https://github.com/odoo/owl/discussions
- Odoo Documentation: https://www.odoo.com/documentation/18.0

---

**Desenvolvido para a comunidade Odoo 🚀**
