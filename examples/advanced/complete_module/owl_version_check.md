# OWL Version in Odoo 18

## Quick Version Check

```bash
# Check OWL version in Odoo installation
cd /path/to/odoo
grep -r "OWL_VERSION\|owl.*version" addons/web/static/src/core/
```

## OWL Version in Odoo 18

**Odoo 18 uses OWL 2.0** (complete rewrite from OWL 1.x)

### Major Changes from Odoo 17 (OWL 1.x) to Odoo 18 (OWL 2.x)

#### 1. Component Definition

**Odoo 17 (OWL 1.x):**
```javascript
const { Component } = owl;

class MyComponent extends Component {
    static template = 'my_module.MyComponent';
    static components = { OtherComponent };
}
```

**Odoo 18 (OWL 2.x):**
```javascript
import { Component } from "@odoo/owl";

class MyComponent extends Component {
    static template = "my_module.MyComponent";
    static components = { OtherComponent };

    // NEW: static props definition required
    static props = {
        title: String,
        count: { type: Number, optional: true },
    };
}
```

#### 2. Props Validation (NEW in OWL 2.0)

```javascript
// Props must be declared with types
static props = {
    // Required prop
    name: String,

    // Optional prop
    age: { type: Number, optional: true },

    // With default value
    role: { type: String, optional: true },

    // Multiple types
    value: [String, Number],

    // Object shape
    user: {
        type: Object,
        shape: {
            id: Number,
            name: String,
        }
    },

    // Array
    items: Array,

    // Wildcard (accepts any props)
    "*": true,
};
```

#### 3. Template Syntax Changes

**Odoo 17:**
```xml
<t t-name="MyComponent" owl="1">
    <div t-on-click="onClick">
        <t t-esc="state.value"/>
    </div>
</t>
```

**Odoo 18:**
```xml
<t t-name="MyComponent">
    <div t-on-click="onClick">
        <t t-esc="state.value"/>
    </div>
</t>
```

#### 4. Hooks Changes

**useState:**
```javascript
// Odoo 17
import { useState } from "@odoo/owl";
setup() {
    this.state = useState({ count: 0 });
}

// Odoo 18 (same)
import { useState } from "@odoo/owl";
setup() {
    this.state = useState({ count: 0 });
}
```

**useRef:**
```javascript
// Odoo 17
import { useRef } from "@odoo/owl";
setup() {
    this.inputRef = useRef("input");
}

// Odoo 18 (same)
import { useRef } from "@odoo/owl";
setup() {
    this.inputRef = useRef("input");
}
```

#### 5. Event Handling

**Odoo 17:**
```javascript
onWillStart() {
    // Called before component starts
}

onMounted() {
    // Called when component is mounted
}

onWillUnmount() {
    // Called before component is unmounted
}
```

**Odoo 18:**
```javascript
setup() {
    onWillStart(() => {
        // Called before component starts
    });

    onMounted(() => {
        // Called when component is mounted
    });

    onWillUnmount(() => {
        // Called before component is unmounted
    });
}
```

#### 6. Component Registration

**Odoo 17:**
```javascript
// Register in registry
import { registry } from "@web/core/registry";

registry.category("actions").add("my_action", MyComponent);
```

**Odoo 18 (same):**
```javascript
// Register in registry
import { registry } from "@web/core/registry";

registry.category("actions").add("my_action", MyComponent);
```

## Complete Migration Example

### Odoo 17 Component

```javascript
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class TaskCard extends Component {
    static template = "project.TaskCard";

    static components = { };

    setup() {
        this.orm = useService("orm");
    }

    async onWillStart() {
        await this.loadData();
    }

    async loadData() {
        this.tasks = await this.orm.searchRead(
            "project.task",
            [],
            ["name", "state"]
        );
    }

    onTaskClick(taskId) {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "project.task",
            res_id: taskId,
            views: [[false, "form"]],
        });
    }
}
```

### Odoo 18 Component (Migrated)

```javascript
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";

export class TaskCard extends Component {
    static template = "project.TaskCard";

    static components = { };

    // NEW: Props definition required
    static props = {
        projectId: { type: Number, optional: true },
        "*": true, // Accept any additional props
    };

    setup() {
        this.orm = useService("orm");

        // NEW: Use onWillStart hook instead of method
        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        this.tasks = await this.orm.searchRead(
            "project.task",
            this.props.projectId ? [["project_id", "=", this.props.projectId]] : [],
            ["name", "state"]
        );
    }

    onTaskClick(taskId) {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "project.task",
            res_id: taskId,
            views: [[false, "form"]],
        });
    }
}
```

## OWL 2.0 Key Features

### 1. Better TypeScript Support
```typescript
interface TaskCardProps {
    projectId?: number;
}

class TaskCard extends Component<TaskCardProps> {
    static template = "project.TaskCard";
    static props = {
        projectId: { type: Number, optional: true },
    };
}
```

### 2. Improved Performance
- Faster rendering
- Better memory management
- Optimized reactivity system

### 3. Better Error Messages
- Props validation errors are more descriptive
- Template errors show exact location
- Component lifecycle errors are clearer

### 4. New Hooks

```javascript
import { onWillStart, onWillRender, onRendered } from "@odoo/owl";

setup() {
    onWillStart(() => {
        // Before first render
    });

    onWillRender(() => {
        // Before each render
    });

    onRendered(() => {
        // After each render
    });
}
```

## Checking OWL Version in Code

```javascript
/** @odoo-module **/

import { Component } from "@odoo/owl";

// Check if we're using OWL 2.0 features
const isOWL2 = typeof Component.prototype.setup !== "undefined";

console.log("OWL Version:", isOWL2 ? "2.x" : "1.x");
```

## Migration Checklist

- [ ] Add `static props` definition to all components
- [ ] Convert lifecycle methods to hooks (`onWillStart`, `onMounted`, etc.)
- [ ] Update component imports from `owl` to `@odoo/owl`
- [ ] Validate all props are properly typed
- [ ] Test component rendering with new props validation
- [ ] Update templates if using deprecated syntax
- [ ] Review and update event handlers
- [ ] Test all hooks and lifecycle methods
- [ ] Update tests to work with OWL 2.0

## Common Issues

### Issue 1: Missing Props Definition
```javascript
// Error: Component MyComponent should define static props
// Fix: Add props definition
static props = {
    "*": true, // Allow all props temporarily
};
```

### Issue 2: Lifecycle Methods Not Working
```javascript
// Old (won't work):
onWillStart() {
    // ...
}

// New:
setup() {
    onWillStart(() => {
        // ...
    });
}
```

### Issue 3: Props Validation Errors
```javascript
// Error: Invalid prop 'count' (expected number, got string)
// Fix: Ensure props match declared types or update type definition
static props = {
    count: [Number, String], // Allow both
};
```

## Resources

- **OWL 2.0 Documentation**: https://github.com/odoo/owl
- **Odoo 18 JavaScript Guide**: See `owl_notes.md` in this repository
- **Migration Guide**: See `migration_guide.md` for complete Odoo 17→18 migration

## Quick Reference

| Feature | OWL 1.x (Odoo 17) | OWL 2.x (Odoo 18) |
|---------|-------------------|-------------------|
| Props validation | Optional | Required |
| Lifecycle methods | Methods | Hooks in setup() |
| Import path | `@odoo/owl` | `@odoo/owl` |
| Template syntax | Same | Same |
| Component registration | Same | Same |
| TypeScript support | Basic | Enhanced |
| Error messages | Basic | Detailed |

## File Locations in Odoo Installation

```
odoo/
└── addons/
    └── web/
        └── static/
            └── src/
                ├── core/
                │   └── owl/
                │       └── ...owl core files...
                ├── views/
                │   └── ...view components...
                └── ...other modules...
```

## Testing OWL Version

Create a simple test component:

```javascript
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class OWLVersionTest extends Component {
    static template = "web.OWLVersionTest";

    // This will error in OWL 2.0 if missing
    static props = {};

    setup() {
        console.log("OWL 2.0 detected: Props validation is active");
    }
}

registry.category("actions").add("owl_version_test", OWLVersionTest);
```

If you see props validation errors, you're using OWL 2.0!
