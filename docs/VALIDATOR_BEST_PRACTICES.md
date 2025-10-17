# Validator Best Practices - Plugin Management

## Plugin Loading Behavior

The Neodoo18Framework validator uses a **directory-based plugin loading system**. Understanding how plugins are loaded is crucial for effective validation workflows.

### How Plugin Loading Works

When you specify `--plugins-dir corporate_plugins`, the validator:

1. **Scans the entire directory** for all `.py` files (excluding files starting with `_`)
2. **Loads ALL plugins** found in the directory
3. **Applies ALL loaded plugins** to the validation target
4. **Does NOT filter** by plugin name, even if a specific plugin is specified

**Example:**
```bash
# This command loads BOTH acme_corporate_rules.py AND neo_sempre_rules.py
python framework/validator/validate.py my_module --plugins-dir corporate_plugins
```

## Isolating Corporate Plugins

If you have multiple corporate plugins and need to apply only specific ones, use one of these strategies:

### Strategy 1: Dedicated Directories (Recommended)

Create separate subdirectories for each plugin set:

```bash
# Directory structure
corporate_plugins/
├── acme/
│   └── acme_corporate_rules.py
├── neo_sempre/
│   └── neo_sempre_rules.py
└── shared/
    └── common_standards.py

# Run validator with specific plugin set
python framework/validator/validate.py my_module \
    --plugins-dir corporate_plugins/neo_sempre
```

**Advantages:**
- ✅ Clear separation of concerns
- ✅ Easy to understand which plugins are active
- ✅ No need to move/rename files
- ✅ Works well with CI/CD pipelines

### Strategy 2: Temporary Disable via Underscore Prefix

Disable plugins by prefixing the filename with an underscore:

```bash
# Disable Acme plugin
mv corporate_plugins/acme_corporate_rules.py \
   corporate_plugins/_acme_corporate_rules.py.disabled

# Validator ignores files starting with underscore
python framework/validator/validate.py my_module \
    --plugins-dir corporate_plugins

# Re-enable when needed
mv corporate_plugins/_acme_corporate_rules.py.disabled \
   corporate_plugins/acme_corporate_rules.py
```

**Advantages:**
- ✅ Quick temporary disable
- ✅ No directory restructuring needed
- ✅ File stays in same location

**Disadvantages:**
- ⚠️ Easy to forget disabled plugins
- ⚠️ Clutters directory with disabled files

### Strategy 3: Environment Variables

Set project-specific plugin paths using environment variables:

```bash
# In your project's .envrc or shell config
export NEODOO_VALIDATOR_PLUGINS="$HOME/projects/neo_sempre/plugins"

# Validator automatically loads from this directory
python framework/validator/validate.py my_module
```

**Advantages:**
- ✅ No command-line arguments needed
- ✅ Project-specific configuration
- ✅ Works with multiple plugin directories (use `:` on Linux/macOS, `;` on Windows)

### Strategy 4: Multiple Plugin Directories

Chain multiple plugin directories for shared + specific rules:

```bash
# Load shared plugins AND project-specific plugins
python framework/validator/validate.py my_module \
    --plugins-dir corporate_plugins/shared \
    --plugins-dir corporate_plugins/neo_sempre

# Or via environment (colon-separated on Linux/macOS)
export NEODOO_VALIDATOR_PLUGINS="$PWD/corporate_plugins/shared:$PWD/corporate_plugins/neo_sempre"
python framework/validator/validate.py my_module
```

## Recommended Directory Structure

For teams working on multiple projects with different corporate standards:

```
neodoo18framework/
├── corporate_plugins/
│   ├── shared/                    # Common rules for all projects
│   │   ├── common_security.py
│   │   └── common_standards.py
│   ├── acme/                      # Acme-specific rules
│   │   └── acme_corporate_rules.py
│   ├── neo_sempre/                # Neo Sempre-specific rules
│   │   └── neo_sempre_rules.py
│   └── README.md                  # Plugin documentation
├── docs/
│   └── VALIDATOR_BEST_PRACTICES.md  # This file
└── ...
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Validate Odoo Module

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run Validator with Corporate Plugin
        run: |
          python framework/validator/validate.py custom_addons/my_module \
            --plugins-dir corporate_plugins/neo_sempre \
            --strict
```

### GitLab CI Example

```yaml
validate:
  image: python:3.11
  script:
    - python framework/validator/validate.py custom_addons/my_module
        --plugins-dir corporate_plugins/neo_sempre
        --strict
  only:
    - merge_requests
    - main
```

## VSCode Tasks Integration

Add project-specific validation tasks to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Validate with Neo Sempre Rules",
      "type": "shell",
      "command": "python",
      "args": [
        "framework/validator/validate.py",
        "${workspaceFolder}/custom_addons/my_module",
        "--plugins-dir",
        "corporate_plugins/neo_sempre",
        "--strict"
      ],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    }
  ]
}
```

## Troubleshooting

### Multiple Plugins Loading When Only One Expected

**Problem:** You specified `--plugins-dir corporate_plugins` but validation errors show rules from multiple plugins.

**Solution:** The validator loads ALL `.py` files in the directory. Use Strategy 1 (dedicated directories) to isolate plugins.

### Plugin Not Loading

**Problem:** Your plugin is in the directory but not being applied.

**Checklist:**
1. ✅ File does NOT start with underscore (`_`)
2. ✅ File has `.py` extension
3. ✅ Plugin class inherits from `BaseValidatorPlugin`
4. ✅ Plugin has `name` and `description` attributes
5. ✅ Plugin has `register()` function or is a class
6. ✅ `supports()` method returns `True` for target files

**Debug:**
```bash
# List all loaded plugins
python framework/validator/validate.py --list-plugins \
    --plugins-dir corporate_plugins/neo_sempre
```

### Plugin Loads but No Validation Happens

**Problem:** Plugin is listed but no errors/warnings are produced.

**Common Causes:**
1. `supports()` returns `False` for all files
2. `validate_file()` returns `None` or empty `ValidationResult`
3. Plugin logic has bugs or exceptions (check terminal output)

**Debug:**
```bash
# Run with verbose flag
python framework/validator/validate.py my_module \
    --plugins-dir corporate_plugins/neo_sempre \
    --verbose
```

## Summary

| Strategy | Use When | Pros | Cons |
|----------|----------|------|------|
| **Dedicated Directories** | Multiple plugins, production use | Clear, no file moves, CI-friendly | Requires directory setup |
| **Underscore Prefix** | Quick temporary disable | Fast, simple | Easy to forget, clutters directory |
| **Environment Variables** | Project-specific config | Automatic, no args needed | Less explicit, harder to debug |
| **Multiple Directories** | Shared + specific rules | Flexible, composable | More complex command lines |

**Recommendation:** Use **Strategy 1 (Dedicated Directories)** for production and team workflows. Use **Strategy 2 (Underscore Prefix)** only for quick local testing.

## Related Documentation

- [Validator Plugin Guide](./guides/en/VALIDATOR_PLUGINS.md) - Creating custom plugins
- [README.md](../README.md) - Framework overview and quick start
- [VSCode Agent Playbook](./guides/en/VSCODE_AGENT_PLAYBOOK.md) - Integrating validation into agent workflows
