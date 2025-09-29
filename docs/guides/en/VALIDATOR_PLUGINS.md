# Validator Plugin Guide

The validator now uses a plugin architecture so you can add new compliance checks without editing `framework/validator/validate.py`. This guide explains how to load plugins, structure them, and share them across teams.

## Loading Plugins

Out of the box the validator ships with the `core_rules` plugin. You can bring in additional plugins from the command line or environment:

```bash
# Run validator and load plugins from a custom folder
python framework/validator/validate.py my_module --plugins-dir ./validator_plugins

# List which plugins are active
python framework/validator/validate.py --list-plugins

# Discover plugins from multiple locations (system-wide)
export NEODOO_VALIDATOR_PLUGINS="$HOME/.neodoo/plugins:$PWD/extra_plugins"
python framework/validator/validate.py my_module
```

> Use your operating system path separator (`:` on Linux/macOS, `;` on Windows) when chaining multiple directories.

Every directory supplied via `--plugins-dir` or `NEODOO_VALIDATOR_PLUGINS` is scanned for `*.py` files that either:

1. expose a `register()` function returning plugin instances, or
2. define subclasses of `BaseValidatorPlugin`.

Any errors while loading plugins are reported once and do not stop the validation run.

## Plugin Interface

Plugins inherit from `BaseValidatorPlugin` (or implement the `ValidatorPlugin` protocol). The lifecycle is:

1. `setup(context)` – called once before validation starts. Use this to prepare caches.
2. `validate_directory(directory, context)` – optional module-level checks. Return a list of `ValidationResult` objects.
3. `supports(file_path, context)` – decide whether to inspect a given file.
4. `validate_file(file_path, context)` – run file-level checks and return a `ValidationResult` (or `None`).
5. `finalize(context)` – optional post-processing once all files are handled.

Each `ValidationResult` has `add_error`, `add_warning` and `add_auto_fix` helpers. When strict mode is enabled the core plugin already promotes critical warnings to errors; custom plugins can read `context.strict`, `context.auto_fix`, or `context.template_mode` to apply their own strategy.

### Minimal Plugin Example

Create `validator_plugins/sample.py` with:

```python
from pathlib import Path
from framework.validator.plugin import BaseValidatorPlugin, ValidationContext, ValidationResult


class SamplePlugin(BaseValidatorPlugin):
    name = "sample_plugin"
    description = "Warn about TODO markers in Python files"

    def supports(self, file_path: Path, context: ValidationContext) -> bool:
        return file_path.suffix == ".py"

    def validate_file(self, file_path: Path, context: ValidationContext):
        text = file_path.read_text(encoding="utf-8")
        if "TODO" not in text:
            return None

        result = ValidationResult()
        result.add_warning(f"TODO markers found in {file_path}")
        return result
```

Run it with:

```bash
python framework/validator/validate.py my_module --plugins-dir validator_plugins
```

You can also expose multiple plugins by returning them from a module-level `register()` function:

```python
def register():
    return [SamplePlugin(), AnotherPlugin()]
```

## Sharing Plugins with Agents

- Store reusable plugins under `.neodoo/plugins/validator/` and set the `NEODOO_VALIDATOR_PLUGINS` environment variable globally.
- Extend the VSCode tasks to include `--plugins-dir` so every agent runs the same extra checks.
- Document plugin responsibilities inside `framework/roles/` so each role knows which checks they own.

This architecture keeps the core validator lean while making it easy to evolve your internal quality gates.
