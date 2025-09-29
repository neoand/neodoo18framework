# Neodoo18Framework – AI Agent Guide
## Fast Changelog
- 2025-09-29: Initial agent brief + snapshot automation added (see workspace README for quick links).
## Know the Layout
- `framework/cli/neodoo.py` powers the cross-platform CLI (create/list/run/delete/doctor/update/migrate) and provisions projects under `~/odoo_projects/` with ready-to-run Odoo 18 stacks.
- `framework/generator/create_project.py` applies the scaffolds in `templates/{minimal,advanced,ecommerce,*-project}` and renames placeholders across files and paths.
- `framework/validator` is plugin-based (`plugins/core.py` ships defaults; add-ons live under `corporate_plugins/` or `NEODOO_VALIDATOR_PLUGINS`).
- `framework/migration/analyzer.py` reuses the validator to surface deprecated APIs, manifest issues, and task checklists when upgrading 15/16/17 modules.
## First Steps
- Read `framework/standards/ODOO18_CORE_STANDARDS.md` and `framework/standards/SOIL_CORE.md` before editing any addon.
- Ensure Python ≥3.8 and PostgreSQL ≥12; run `./env.sh setup` once, then `./env.sh activate` to reuse the virtualenv.
- Browse `docs/guides/en/COMPLETE_GUIDE.md` (or localized variants) for end-to-end project walkthroughs.
- Check the workspace-level `README.md` at repo root for project map, active modules, and latest snapshots before exploring directories.
## Daily Commands
- Use `./neodoo` for the interactive dashboard; add `NEODOO_SKIP_PAUSE=1` when scripting agents.
- Create projects non-interactively with `./neodoo create --name my_project --module my_module --template minimal --base-dir ~/odoo_projects --no-venv` (or `--from-config .neodoo.yml`).
- Run health checks via `./neodoo doctor --path ~/odoo_projects/my_project` before debugging failures.
- Validate addons with `python framework/validator/validate.py custom_addons/my_module --strict --auto-fix` and re-run after edits.
- Generate migration reports with `./neodoo migrate path/to/module --from-version 17` for structured upgrade tasks.
## Coding Rules the Validator Enforces
- XML views must use `<list>` and window actions must declare `view_mode="list,form"`; deprecated `<tree>` markers auto-error.
- Python models require the UTF-8 header, `_description`, `@api.depends` on compute methods, and no `print()`/`breakpoint()` leftovers.
- Button/action methods should call `self.ensure_one()`; the plugin flags missing calls as warnings (errors in strict mode).
- Manifest files must target `18.0.*`, include `license`, list `security/ir.model.access.csv`, and keep `depends` as a list.
- Each module needs a properly headed `ir.model.access.csv` and `models/__init__.py` importing every Python file.
## Generator & Templates
- Run `python framework/generator/create_project.py --name foo --type minimal` for CLI-less scaffolding; add `--dry-run --no-all-placeholders` to preview replacements.
- Templates ship setup scripts like `init_project.sh`; keep them executable after copying.
- Use `.neodoo.yml` (see docs examples) to capture reproducible project definitions consumed by `./neodoo create --from-config`.
- Check `examples/` for validated reference modules before introducing new patterns.
## Tooling & Automation
- `.vscode/tasks.json` exposes `Neodoo: Open Interactive Menu`, `Neodoo: Strict Validator`, `Neodoo: Migration Analyzer`, and a corporate validator bundle—rely on these when running inside VS Code.
- `NEODOO_FRAMEWORK_ROOT` is injected by `.vscode/settings.json`; use it to build relative paths in tasks or shell scripts.
- `scripts/dev/export_agent_brief.sh <project>` gera `docs/agent-brief.md` com logs recentes (VSCode task "Neodoo: Export Agent Brief" automatiza o processo).
- Load extra validation rules with `python framework/validator/validate.py <path> --plugins-dir corporate_plugins` or by exporting `NEODOO_VALIDATOR_PLUGINS`.
## Before You Finish
- Run `scripts/dev/quick_sanity.sh` to smoke-test template listing, project creation, doctor, and strict validation in one pass.
- Atualize ou leia `docs/agent-brief.md` para saber o estado recente sem rerodar comandos longos.
- Deliver only after `./neodoo doctor` and the validator succeed (core + corporate plugins) and no legacy `<tree>` markers remain.
