# Migration Guide: Odoo 15/16/17 → 18

The Neodoo18Framework now bundles a migration assistant that scans your modules, highlights risky patterns, and enumerates mandatory tasks for upgrading from earlier Odoo versions to 18.

## Quick Start

```bash
# Run from the framework root
python framework/migration/cli.py /path/to/module --from-version 16

# Or via the main CLI
./neodoo migrate /path/to/module --from-version 17

# Generate a JSON report
python framework/migration/cli.py /path/to/module --from-version 15 --json > migration_report.json
```

### Interactive Menu

From the visual CLI menu select **🧭 Assistente de Migração**. You will be prompted for:

1. The module/project path to analyze
2. The original Odoo major version (15/16/17)
3. Whether to allow safe auto-fixes (delegated to the validator)

The assistant prints a summary of detected errors/warnings, detailed findings, and a list of mandatory/manual tasks tailored to the source version.

## What the Analyzer Checks

The migration heuristics combine several layers:

- **Manifest inspection** – validates version numbers, dependency lists, and asset bundles.
- **Source scanning** – detects legacy front-end directories, AMD/`odoo.define` JavaScript modules, deprecated Python decorators, and `<tree>` templates.
- **Validator integration** – reuses the strict Odoo 18 validator to catch architectural regressions.
- **Task playbook** – appends mandatory and manual follow-up items (e.g., OWL refactors, mail/discuss updates, data migration rehearsals).

All results are aggregated into a structured `MigrationReport` object that you can convert to JSON for dashboards or CI integration.

## Extending the Rules

Rules live under `framework/migration/rules.py` and can be customised or extended:

- Add deprecated dependencies to `DEPRECATED_DEPENDENCIES`
- Extend `LEGACY_JS_PATTERNS` / `LEGACY_DIRECTORIES`
- Append new `MigrationTask` entries for organisation-specific workflows

For deeper inspections you can subclass `MigrationAnalyzer` or run additional scans before serialising the report.

## Data Migration Helpers

`framework/migration/data_pipeline.py` ships a `MigrationMixin` that provides:

- Context-managed logging with execution timings (`migration_step`)
- Structured record logging (`log_record`)
- Chunked iterators for bulk ETL processes (`chunked`)

Use the mixin inside Odoo server actions or custom scripts when migrating databases between major versions.

## Recommended Workflow

1. Run the migration analyzer on every custom module.
2. Fix blocking errors (deprecated decorators, manifest versions, legacy XML tags).
3. Address warnings by refactoring JS assets and reviewing manual SQL usage.
4. Generate migration tasks and assign them to the relevant roles (Backend, OWL specialist, Data migration specialist).
5. Re-run `./neodoo migrate` and `./neodoo doctor` until the report is clean.
6. Execute data migration scripts leveraging `MigrationMixin` in a staging environment before touching production.

Pair the analyzer with CI to prevent regressions: add a workflow step executing `./neodoo migrate <module> --from-version 17 --json` and parse the resulting JSON for blockers.
