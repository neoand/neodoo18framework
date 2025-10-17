# OWL 3 Framework no Odoo 18

## Introducao ao OWL 3

O Odoo Web Library (OWL) versao 3 e o framework JavaScript reativo usado no Odoo 18 para criar componentes de interface. OWL 3 traz mudancas significativas em relacao ao OWL 2, incluindo melhor performance, API simplificada e maior compatibilidade com padoes modernos do JavaScript.

---

## Diferencas: OWL 2 vs OWL 3

### 1. Mudancas na API de Hooks

**OWL 2:**
```javascript
import { useState, useRef } from "@odoo/owl";

class MyComponent extends Component {
    setup() {
        this.state = useState({ count: 0 });
        this.inputRef = useRef("input");
    }
}
```

**OWL 3:**
```javascript
import { Component, useState, useRef } from "@odoo/owl";

class MyComponent extends Component {
    static template = "my_module.MyComponent";

    setup() {
        this.state = useState({ count: 0 });
        this.inputRef = useRef("input");
    }
}
```

### 2. Importacao de Component

**OWL 2:**
```javascript
const { Component } = owl;
```

**OWL 3:**
```javascript
import { Component } from "@odoo/owl";
```

### 3. Registro de Componentes

**OWL 2:**
```javascript
import { registry } from "@web/core/registry";

registry.category("main_components").add("MyComponent", {
    Component: MyComponent,
});
```

**OWL 3 (mais simplificado):**
```javascript
import { registry } from "@web/core/registry";

registry.category("main_components").add("MyComponent", MyComponent);
```

### 4. Props Validation

**OWL 3 tem validacao de props mais rigorosa:**
```javascript
class MyComponent extends Component {
    static props = {
        title: String,
        count: { type: Number, optional: true },
        items: Array,
        user: Object,
        onSave: Function,
        "*": true, // Permite props adicionais
    };
}
```

### 5. Event Handling

**OWL 2:**
```javascript
<button t-on-click="onClick">Click</button>

onClick(ev) {
    // handler
}
```

**OWL 3 (mesma sintaxe, mas melhor performance):**
```javascript
<button t-on-click="onClick">Click</button>

onClick(ev) {
    // handler com melhor performance
}
```

---

## Estrutura de Componentes OWL 3

### Estrutura Basica

```javascript
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class MyComponent extends Component {
    static template = "my_module.MyComponent";

    static props = {
        title: String,
        subtitle: { type: String, optional: true },
    };

    setup() {
        // Inicializacao do componente
        this.state = useState({
            counter: 0,
        });
    }

    increment() {
        this.state.counter++;
    }
}

registry.category("actions").add("my_component", MyComponent);
```

### Template XML Correspondente

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="my_module.MyComponent">
        <div class="my-component">
            <h1><t t-esc="props.title"/></h1>
            <h2 t-if="props.subtitle">
                <t t-esc="props.subtitle"/>
            </h2>
            <p>Counter: <t t-esc="state.counter"/></p>
            <button t-on-click="increment">Increment</button>
        </div>
    </t>
</templates>
```

---

## Hooks Disponiveis no OWL 3

### 1. useState - Estado Reativo

Cria estado reativo que automaticamente re-renderiza o componente quando modificado.

```javascript
import { Component, useState } from "@odoo/owl";

class TodoList extends Component {
    static template = "my_module.TodoList";

    setup() {
        this.state = useState({
            todos: [],
            filter: "all",
        });
    }

    addTodo(text) {
        this.state.todos.push({
            id: Date.now(),
            text: text,
            done: false,
        });
    }

    toggleTodo(id) {
        const todo = this.state.todos.find(t => t.id === id);
        if (todo) {
            todo.done = !todo.done;
        }
    }

    removeTodo(id) {
        const index = this.state.todos.findIndex(t => t.id === id);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }
}
```

**Template:**
```xml
<t t-name="my_module.TodoList">
    <div class="todo-list">
        <input t-ref="input" placeholder="Add todo..."/>
        <button t-on-click="() => this.addTodo(this.inputRef.el.value)">
            Add
        </button>

        <ul>
            <li t-foreach="state.todos" t-as="todo" t-key="todo.id">
                <input type="checkbox"
                       t-att-checked="todo.done"
                       t-on-click="() => this.toggleTodo(todo.id)"/>
                <span t-att-class="{ 'done': todo.done }">
                    <t t-esc="todo.text"/>
                </span>
                <button t-on-click="() => this.removeTodo(todo.id)">X</button>
            </li>
        </ul>
    </div>
</t>
```

### 2. useRef - Referencia a Elementos DOM

```javascript
import { Component, useRef } from "@odoo/owl";

class SearchBar extends Component {
    static template = "my_module.SearchBar";

    setup() {
        this.inputRef = useRef("searchInput");
    }

    onMounted() {
        // Acessa elemento DOM apos montagem
        this.inputRef.el.focus();
    }

    search() {
        const query = this.inputRef.el.value;
        console.log("Searching for:", query);
    }
}
```

**Template:**
```xml
<t t-name="my_module.SearchBar">
    <div class="search-bar">
        <input t-ref="searchInput"
               type="text"
               placeholder="Search..."/>
        <button t-on-click="search">Search</button>
    </div>
</t>
```

### 3. useEffect - Efeitos Colaterais

Executa codigo quando dependencias mudam.

```javascript
import { Component, useState, useEffect } from "@odoo/owl";

class DataFetcher extends Component {
    static template = "my_module.DataFetcher";

    setup() {
        this.state = useState({
            data: null,
            loading: false,
            filter: "all",
        });

        // Executa quando filter muda
        useEffect(
            () => {
                this.fetchData();
            },
            () => [this.state.filter]
        );
    }

    async fetchData() {
        this.state.loading = true;
        try {
            const response = await fetch(`/api/data?filter=${this.state.filter}`);
            this.state.data = await response.json();
        } finally {
            this.state.loading = false;
        }
    }
}
```

### 4. useEnv - Acesso ao Environment

```javascript
import { Component, useEnv } from "@odoo/owl";

class NotificationButton extends Component {
    static template = "my_module.NotificationButton";

    setup() {
        this.env = useEnv();
    }

    showNotification() {
        this.env.services.notification.add("Success!", {
            type: "success",
        });
    }

    async saveRecord() {
        const orm = this.env.services.orm;
        await orm.create("res.partner", [{
            name: "New Partner",
        }]);
        this.showNotification();
    }
}
```

### 5. useService - Acesso a Servicos

```javascript
import { Component, useService } from "@odoo/owl";

class RecordEditor extends Component {
    static template = "my_module.RecordEditor";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
    }

    async loadRecord(resModel, resId) {
        const record = await this.orm.read(resModel, [resId], ["name", "email"]);
        return record[0];
    }

    async saveRecord(resModel, resId, values) {
        await this.orm.write(resModel, [resId], values);
        this.notification.add("Record saved!", { type: "success" });
    }

    openFormView(resModel, resId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: resModel,
            res_id: resId,
            views: [[false, "form"]],
            target: "current",
        });
    }
}
```

### 6. useSubEnv - Criar Sub-Environment

```javascript
import { Component, useSubEnv, useState } from "@odoo/owl";

class ThemeProvider extends Component {
    static template = "my_module.ThemeProvider";

    setup() {
        this.state = useState({
            theme: "light",
        });

        // Adiciona theme ao environment para componentes filhos
        useSubEnv({
            theme: this.state.theme,
            toggleTheme: this.toggleTheme.bind(this),
        });
    }

    toggleTheme() {
        this.state.theme = this.state.theme === "light" ? "dark" : "light";
    }
}

// Componente filho pode acessar
class ThemedButton extends Component {
    setup() {
        this.theme = this.env.theme;
        this.toggleTheme = this.env.toggleTheme;
    }
}
```

### 7. useComponent - Auto-referencia

```javascript
import { Component, useComponent } from "@odoo/owl";

class SelfAwareComponent extends Component {
    setup() {
        this.component = useComponent();
        console.log("Component instance:", this.component);
    }
}
```

### 8. onWillStart, onMounted, onWillUnmount

Lifecycle hooks para controlar ciclo de vida do componente.

```javascript
import { Component, onWillStart, onMounted, onWillUnmount } from "@odoo/owl";

class LifecycleComponent extends Component {
    static template = "my_module.LifecycleComponent";

    setup() {
        // Antes de renderizar (pode ser async)
        onWillStart(async () => {
            console.log("Component will start");
            this.data = await this.loadData();
        });

        // Apos montagem no DOM
        onMounted(() => {
            console.log("Component mounted");
            this.setupEventListeners();
        });

        // Antes de destruir componente
        onWillUnmount(() => {
            console.log("Component will unmount");
            this.cleanup();
        });
    }

    async loadData() {
        // Carrega dados
        return { items: [] };
    }

    setupEventListeners() {
        // Configura listeners
    }

    cleanup() {
        // Limpa recursos
    }
}
```

### 9. onWillUpdateProps, onWillPatch, onPatched

```javascript
import {
    Component,
    onWillUpdateProps,
    onWillPatch,
    onPatched
} from "@odoo/owl";

class ReactiveComponent extends Component {
    setup() {
        // Quando props vao mudar
        onWillUpdateProps((nextProps) => {
            console.log("Props will update:", nextProps);
        });

        // Antes do patch (re-render)
        onWillPatch(() => {
            console.log("Component will patch");
        });

        // Apos patch
        onPatched(() => {
            console.log("Component patched");
        });
    }
}
```

---

## Props e Reatividade

### Definicao de Props

```javascript
class UserCard extends Component {
    static template = "my_module.UserCard";

    // Props com validacao
    static props = {
        // Tipo simples
        name: String,

        // Opcional
        email: { type: String, optional: true },

        // Com valor padrao
        role: { type: String, optional: true },

        // Array
        tags: Array,

        // Object
        address: Object,

        // Number
        age: Number,

        // Boolean
        active: Boolean,

        // Function
        onSave: Function,

        // Aceitar props adicionais
        "*": true,
    };

    static defaultProps = {
        role: "user",
        active: true,
    };
}
```

### Props Complexas

```javascript
class DataTable extends Component {
    static props = {
        // Array de objetos com formato especifico
        columns: {
            type: Array,
            element: {
                type: Object,
                shape: {
                    name: String,
                    label: String,
                    type: { type: String, optional: true },
                },
            },
        },

        // Objeto com estrutura definida
        config: {
            type: Object,
            shape: {
                sortable: Boolean,
                filterable: Boolean,
                pageSize: Number,
            },
            optional: true,
        },

        // Union types (aceita multiplos tipos)
        value: [String, Number, Boolean],

        // Validacao customizada
        status: {
            validate: (value) => ["draft", "posted", "cancel"].includes(value),
        },
    };
}
```

### Reatividade com useState

```javascript
import { Component, useState } from "@odoo/owl";

class ReactiveForm extends Component {
    static template = "my_module.ReactiveForm";

    setup() {
        // Estado reativo simples
        this.state = useState({
            name: "",
            email: "",
            age: 0,
        });

        // Estado reativo aninhado
        this.formState = useState({
            values: {
                firstName: "",
                lastName: "",
                address: {
                    street: "",
                    city: "",
                    country: "",
                },
            },
            errors: {},
            touched: {},
        });
    }

    updateField(field, value) {
        // Atualizacao reativa
        this.state[field] = value;
    }

    updateNestedField(path, value) {
        // Atualiza campo aninhado
        const keys = path.split(".");
        let obj = this.formState.values;

        for (let i = 0; i < keys.length - 1; i++) {
            obj = obj[keys[i]];
        }

        obj[keys[keys.length - 1]] = value;
    }
}
```

---

## Comunicacao entre Componentes

### 1. Props (Pai -> Filho)

```javascript
// Componente Pai
class ParentComponent extends Component {
    static template = "my_module.ParentComponent";
    static components = { ChildComponent };

    setup() {
        this.state = useState({
            message: "Hello from parent",
        });
    }
}

// Componente Filho
class ChildComponent extends Component {
    static template = "my_module.ChildComponent";
    static props = {
        message: String,
    };
}
```

**Template Pai:**
```xml
<t t-name="my_module.ParentComponent">
    <div>
        <ChildComponent message="state.message"/>
    </div>
</t>
```

**Template Filho:**
```xml
<t t-name="my_module.ChildComponent">
    <div>
        <p t-esc="props.message"/>
    </div>
</t>
```

### 2. Events (Filho -> Pai)

```javascript
// Componente Filho
class ChildComponent extends Component {
    static template = "my_module.ChildComponent";
    static props = {
        onItemClick: Function,
    };

    handleClick(item) {
        // Emite evento para pai
        this.props.onItemClick(item);
    }
}

// Componente Pai
class ParentComponent extends Component {
    static template = "my_module.ParentComponent";
    static components = { ChildComponent };

    onItemClick(item) {
        console.log("Item clicked:", item);
    }
}
```

**Template Pai:**
```xml
<t t-name="my_module.ParentComponent">
    <ChildComponent onItemClick.bind="onItemClick"/>
</t>
```

### 3. Event Bus (Componentes Desacoplados)

```javascript
import { EventBus } from "@odoo/owl";

// Criar bus global
const messageBus = new EventBus();

// Componente Publisher
class Publisher extends Component {
    sendMessage() {
        messageBus.trigger("message-sent", {
            text: "Hello World",
            timestamp: Date.now(),
        });
    }
}

// Componente Subscriber
class Subscriber extends Component {
    setup() {
        onMounted(() => {
            messageBus.addEventListener("message-sent", this.onMessage.bind(this));
        });

        onWillUnmount(() => {
            messageBus.removeEventListener("message-sent", this.onMessage.bind(this));
        });
    }

    onMessage(event) {
        console.log("Message received:", event.detail);
    }
}
```

### 4. Environment (Estado Global)

```javascript
// No setup do app
const env = {
    services: {
        user: userService,
        notification: notificationService,
    },
    sharedState: useState({
        currentUser: null,
        settings: {},
    }),
};

// Em qualquer componente
class AnyComponent extends Component {
    setup() {
        // Acessa estado compartilhado
        this.sharedState = this.env.sharedState;
    }

    updateSettings(key, value) {
        this.sharedState.settings[key] = value;
    }
}
```

---

## Templates e QWeb

### Sintaxe QWeb no OWL 3

#### 1. Interpolacao

```xml
<!-- Escape automatico -->
<span><t t-esc="value"/></span>

<!-- Raw HTML (cuidado com XSS) -->
<div t-out="htmlContent"/>

<!-- Em atributos -->
<div t-att-class="className"/>
<div t-attf-class="btn btn-{{type}}"/>
```

#### 2. Condicionais

```xml
<!-- if simples -->
<div t-if="condition">Visible if true</div>

<!-- if/elif/else -->
<div t-if="state === 'draft'">Draft</div>
<div t-elif="state === 'posted'">Posted</div>
<div t-else="">Other</div>

<!-- Condicao complexa -->
<div t-if="user.active and user.role === 'admin'">
    Admin content
</div>
```

#### 3. Loops

```xml
<!-- Loop simples -->
<ul>
    <li t-foreach="items" t-as="item" t-key="item.id">
        <t t-esc="item.name"/>
    </li>
</ul>

<!-- Com index -->
<ul>
    <li t-foreach="items" t-as="item" t-key="item.id">
        <t t-esc="item_index"/>: <t t-esc="item.name"/>
    </li>
</ul>

<!-- Loop com objeto -->
<ul>
    <li t-foreach="Object.entries(config)" t-as="entry" t-key="entry[0]">
        <t t-esc="entry[0]"/>: <t t-esc="entry[1]"/>
    </li>
</ul>
```

#### 4. Sub-componentes

```xml
<t t-name="my_module.Parent">
    <div class="parent">
        <!-- Componente filho -->
        <ChildComponent title="'Hello'" count="state.count"/>

        <!-- Com slots -->
        <Card>
            <t t-set-slot="header">
                <h2>Card Title</h2>
            </t>
            <t t-set-slot="body">
                <p>Card content</p>
            </t>
        </Card>
    </div>
</t>
```

#### 5. Event Handlers

```xml
<!-- Click simples -->
<button t-on-click="handleClick">Click me</button>

<!-- Com argumentos -->
<button t-on-click="() => this.handleClick(item)">Click</button>

<!-- Multiplos eventos -->
<input t-on-input="onInput"
       t-on-focus="onFocus"
       t-on-blur="onBlur"/>

<!-- Modificadores -->
<form t-on-submit.prevent="onSubmit">
    <button type="submit">Submit</button>
</form>
```

#### 6. Refs

```xml
<!-- Ref simples -->
<input t-ref="myInput"/>

<!-- Ref em componente -->
<ChildComponent t-ref="childRef"/>

<!-- Acesso em JavaScript -->
<script>
this.myInputRef = useRef("myInput");
// Usar: this.myInputRef.el
</script>
```

#### 7. Slots

```xml
<!-- Definicao do componente com slot -->
<t t-name="my_module.Card">
    <div class="card">
        <div class="card-header">
            <t t-slot="header"/>
        </div>
        <div class="card-body">
            <t t-slot="body"/>
        </div>
        <div class="card-footer" t-if="slots.footer">
            <t t-slot="footer"/>
        </div>
    </div>
</t>

<!-- Uso -->
<Card>
    <t t-set-slot="header">
        <h3>Title</h3>
    </t>
    <t t-set-slot="body">
        <p>Content</p>
    </t>
</Card>
```

---

## Integracao com Odoo

### 1. Componentes de Actions

```javascript
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class CustomDashboard extends Component {
    static template = "my_module.CustomDashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            stats: null,
            loading: true,
        });

        onWillStart(async () => {
            await this.loadStats();
        });
    }

    async loadStats() {
        this.state.loading = true;
        try {
            this.state.stats = await this.orm.call(
                "my.model",
                "get_dashboard_stats",
                []
            );
        } finally {
            this.state.loading = false;
        }
    }
}

// Registrar como action
registry.category("actions").add("custom_dashboard", CustomDashboard);
```

**XML Action:**
```xml
<record id="action_custom_dashboard" model="ir.actions.client">
    <field name="name">Custom Dashboard</field>
    <field name="tag">custom_dashboard</field>
</record>
```

### 2. Widgets de Formulario

```javascript
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class ColorPickerField extends Component {
    static template = "my_module.ColorPickerField";
    static props = {
        ...standardFieldProps,
    };

    get value() {
        return this.props.record.data[this.props.name];
    }

    onChange(color) {
        this.props.record.update({ [this.props.name]: color });
    }
}

// Registrar widget
registry.category("fields").add("color_picker", ColorPickerField);
```

**Uso no XML:**
```xml
<field name="color" widget="color_picker"/>
```

### 3. Systray Items

```javascript
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class NotificationIndicator extends Component {
    static template = "my_module.NotificationIndicator";

    setup() {
        this.orm = useService("orm");

        this.state = useState({
            count: 0,
        });

        onWillStart(async () => {
            await this.loadCount();
        });

        // Atualiza a cada 60 segundos
        setInterval(() => this.loadCount(), 60000);
    }

    async loadCount() {
        this.state.count = await this.orm.call(
            "mail.notification",
            "get_unread_count",
            []
        );
    }

    onClick() {
        // Abre notificacoes
    }
}

registry.category("systray").add("notification_indicator", {
    Component: NotificationIndicator,
    isDisplayed: (env) => true,
});
```

### 4. Menu Items

```javascript
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class CustomMenuItem extends Component {
    static template = "my_module.CustomMenuItem";

    onClick() {
        // Acao customizada
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "my.model",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

registry.category("navbar").add("custom_menu_item", CustomMenuItem);
```

---

## Exemplos Praticos Completos

### Exemplo 1: Lista de Tarefas Completa

```javascript
/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class TaskManager extends Component {
    static template = "my_module.TaskManager";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");

        this.inputRef = useRef("taskInput");

        this.state = useState({
            tasks: [],
            filter: "all",
            loading: false,
        });

        onWillStart(async () => {
            await this.loadTasks();
        });
    }

    async loadTasks() {
        this.state.loading = true;
        try {
            this.state.tasks = await this.orm.searchRead(
                "project.task",
                [],
                ["name", "date_deadline", "stage_id", "user_id"]
            );
        } finally {
            this.state.loading = false;
        }
    }

    async addTask() {
        const name = this.inputRef.el.value.trim();
        if (!name) return;

        const id = await this.orm.create("project.task", [{
            name: name,
        }]);

        this.state.tasks.push({
            id: id,
            name: name,
            stage_id: false,
        });

        this.inputRef.el.value = "";
        this.notification.add("Task created!", { type: "success" });
    }

    async toggleTask(task) {
        // Implementacao
    }

    async deleteTask(taskId) {
        await this.orm.unlink("project.task", [taskId]);
        const index = this.state.tasks.findIndex(t => t.id === taskId);
        this.state.tasks.splice(index, 1);
        this.notification.add("Task deleted!", { type: "info" });
    }

    get filteredTasks() {
        if (this.state.filter === "all") {
            return this.state.tasks;
        }
        // Implementar outros filtros
        return this.state.tasks;
    }
}

registry.category("actions").add("task_manager", TaskManager);
```

**Template:**
```xml
<t t-name="my_module.TaskManager">
    <div class="task-manager">
        <div class="task-input">
            <input t-ref="taskInput"
                   type="text"
                   placeholder="Add new task..."
                   t-on-keyup.enter="addTask"/>
            <button t-on-click="addTask" class="btn btn-primary">
                Add Task
            </button>
        </div>

        <div class="task-filters">
            <button t-on-click="() => this.state.filter = 'all'"
                    t-att-class="{ 'active': state.filter === 'all' }">
                All
            </button>
            <button t-on-click="() => this.state.filter = 'active'"
                    t-att-class="{ 'active': state.filter === 'active' }">
                Active
            </button>
            <button t-on-click="() => this.state.filter = 'completed'"
                    t-att-class="{ 'active': state.filter === 'completed' }">
                Completed
            </button>
        </div>

        <div class="task-list">
            <t t-if="state.loading">
                <div class="spinner-border"/>
            </t>
            <t t-else="">
                <div t-foreach="filteredTasks" t-as="task" t-key="task.id"
                     class="task-item">
                    <span t-esc="task.name"/>
                    <button t-on-click="() => this.deleteTask(task.id)"
                            class="btn btn-sm btn-danger">
                        Delete
                    </button>
                </div>
            </t>
        </div>
    </div>
</t>
```

### Exemplo 2: Formulario com Validacao

```javascript
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class ValidatedForm extends Component {
    static template = "my_module.ValidatedForm";
    static props = {
        onSubmit: Function,
    };

    setup() {
        this.state = useState({
            values: {
                name: "",
                email: "",
                age: "",
            },
            errors: {},
            touched: {},
        });
    }

    validate() {
        const errors = {};

        if (!this.state.values.name.trim()) {
            errors.name = "Name is required";
        }

        if (!this.state.values.email.trim()) {
            errors.email = "Email is required";
        } else if (!this.isValidEmail(this.state.values.email)) {
            errors.email = "Invalid email format";
        }

        if (!this.state.values.age) {
            errors.age = "Age is required";
        } else if (this.state.values.age < 18) {
            errors.age = "Must be 18 or older";
        }

        this.state.errors = errors;
        return Object.keys(errors).length === 0;
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    onFieldChange(field, value) {
        this.state.values[field] = value;
        this.state.touched[field] = true;
        this.validate();
    }

    onSubmit(ev) {
        ev.preventDefault();

        // Marca todos como touched
        Object.keys(this.state.values).forEach(key => {
            this.state.touched[key] = true;
        });

        if (this.validate()) {
            this.props.onSubmit(this.state.values);
        }
    }

    getFieldError(field) {
        return this.state.touched[field] ? this.state.errors[field] : null;
    }
}
```

**Template:**
```xml
<t t-name="my_module.ValidatedForm">
    <form t-on-submit.prevent="onSubmit" class="validated-form">
        <div class="form-group">
            <label>Name</label>
            <input type="text"
                   t-att-value="state.values.name"
                   t-on-input="(ev) => this.onFieldChange('name', ev.target.value)"
                   t-att-class="{ 'is-invalid': getFieldError('name') }"/>
            <div t-if="getFieldError('name')" class="invalid-feedback">
                <t t-esc="getFieldError('name')"/>
            </div>
        </div>

        <div class="form-group">
            <label>Email</label>
            <input type="email"
                   t-att-value="state.values.email"
                   t-on-input="(ev) => this.onFieldChange('email', ev.target.value)"
                   t-att-class="{ 'is-invalid': getFieldError('email') }"/>
            <div t-if="getFieldError('email')" class="invalid-feedback">
                <t t-esc="getFieldError('email')"/>
            </div>
        </div>

        <div class="form-group">
            <label>Age</label>
            <input type="number"
                   t-att-value="state.values.age"
                   t-on-input="(ev) => this.onFieldChange('age', parseInt(ev.target.value))"
                   t-att-class="{ 'is-invalid': getFieldError('age') }"/>
            <div t-if="getFieldError('age')" class="invalid-feedback">
                <t t-esc="getFieldError('age')"/>
            </div>
        </div>

        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</t>
```

---

## Performance e Otimizacao

### 1. Memoizacao de Getters

```javascript
import { Component, useState } from "@odoo/owl";

class OptimizedList extends Component {
    setup() {
        this.state = useState({
            items: [],
            filter: "",
        });
    }

    // Getter e recalculado apenas quando dependencias mudam
    get filteredItems() {
        console.log("Filtering items..."); // Deve logar apenas quando necessario
        return this.state.items.filter(item =>
            item.name.toLowerCase().includes(this.state.filter.toLowerCase())
        );
    }
}
```

### 2. Lazy Loading de Componentes

```javascript
import { Component, useState, onWillStart } from "@odoo/owl";

class LazyContainer extends Component {
    static template = "my_module.LazyContainer";

    setup() {
        this.state = useState({
            HeavyComponent: null,
        });

        onWillStart(async () => {
            // Carrega componente apenas quando necessario
            const module = await import("./heavy_component");
            this.state.HeavyComponent = module.HeavyComponent;
        });
    }
}
```

### 3. Usar t-key para Listas

```xml
<!-- Sem t-key: OWL re-renderiza todos os items -->
<div t-foreach="items" t-as="item">
    <t t-esc="item.name"/>
</div>

<!-- Com t-key: OWL reusa elementos existentes -->
<div t-foreach="items" t-as="item" t-key="item.id">
    <t t-esc="item.name"/>
</div>
```

---

## Boas Praticas

### 1. Estrutura de Arquivos

```
my_module/
├── static/
│   └── src/
│       ├── components/
│       │   ├── task_list/
│       │   │   ├── task_list.js
│       │   │   └── task_list.xml
│       │   └── task_item/
│       │       ├── task_item.js
│       │       └── task_item.xml
│       ├── services/
│       │   └── task_service.js
│       └── views/
│           └── task_dashboard.js
```

### 2. Separacao de Responsabilidades

```javascript
// Service para logica de negocio
export const taskService = {
    dependencies: ["orm", "notification"],

    start(env, { orm, notification }) {
        return {
            async createTask(name) {
                const id = await orm.create("project.task", [{ name }]);
                notification.add("Task created!", { type: "success" });
                return id;
            },

            async getTasks() {
                return await orm.searchRead("project.task", [], ["name"]);
            },
        };
    },
};

registry.category("services").add("task", taskService);

// Componente apenas para apresentacao
class TaskList extends Component {
    setup() {
        this.taskService = useService("task");
        // ...
    }
}
```

### 3. Documentacao de Componentes

```javascript
/**
 * Task List Component
 *
 * Displays a list of tasks with filtering and sorting capabilities.
 *
 * @component
 * @props {Array} tasks - Array of task objects
 * @props {String} filter - Current filter ('all', 'active', 'completed')
 * @props {Function} onTaskClick - Callback when task is clicked
 * @props {Function} onTaskDelete - Callback when task is deleted
 *
 * @example
 * <TaskList tasks="state.tasks"
 *           filter="'all'"
 *           onTaskClick.bind="handleTaskClick"
 *           onTaskDelete.bind="handleTaskDelete"/>
 */
export class TaskList extends Component {
    static template = "my_module.TaskList";

    static props = {
        tasks: Array,
        filter: String,
        onTaskClick: Function,
        onTaskDelete: Function,
    };
}
```

---

## Migracao OWL 2 para OWL 3

### Checklist de Migracao

1. Atualizar imports
2. Atualizar definicao de props
3. Revisar lifecycle hooks
4. Testar reatividade
5. Atualizar event handlers
6. Verificar componentes filhos

### Script de Migracao Exemplo

```javascript
// Antes (OWL 2)
const { Component, useState, hooks } = owl;
const { useRef } = hooks;

class MyComponent extends Component {
    constructor(parent, props) {
        super(parent, props);
        this.state = useState({ count: 0 });
    }
}

// Depois (OWL 3)
import { Component, useState, useRef } from "@odoo/owl";

class MyComponent extends Component {
    static template = "my_module.MyComponent";
    static props = {
        // definir props
    };

    setup() {
        this.state = useState({ count: 0 });
    }
}
```

---

## Referencias e Recursos

- Documentacao Oficial OWL: https://github.com/odoo/owl/blob/master/doc/reference/readme.md
- Odoo 18 Developer Documentation: https://www.odoo.com/documentation/18.0/developer/
- OWL Playground: https://odoo.github.io/owl/playground/
- Exemplos de Componentes: https://github.com/odoo/odoo/tree/18.0/addons/web/static/src
