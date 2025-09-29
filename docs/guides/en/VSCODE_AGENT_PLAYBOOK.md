# VSCode Agent Playbook

This playbook explains how to drive the Neodoo18Framework from Visual Studio Code when you are collaborating with autonomous agents or LLM copilots. The goal is to give each role a predictable toolbox that matches the tasks exposed by the framework.

## Objectives

- Provide a zero-configuration VSCode workspace that exposes the main CLI flows as tasks.
- Offer launch configurations so agents can debug or automate project creation with arguments.
- Map the existing role definitions in `framework/roles/` to concrete editor actions.

## Workspace Layout

The `.vscode/` folder contains four coordinated files:

| File | Purpose |
| --- | --- |
| `extensions.json` | Recommends Python, YAML, XML, Docker and spell-check extensions that the roles tend to use. |
| `settings.json` | Defines shared environment variables (`NEODOO_FRAMEWORK_ROOT`) and formatting preferences tuned for Odoo development. |
| `tasks.json` | Exposes curated commands (`Neodoo: Open Interactive Menu`, `Neodoo: Doctor`, validator and generator helpers). |
| `launch.json` | Adds ready-to-run debug entries for the CLI interactive menu and the config-driven project creator. |

Agents can rely on the workspace existing as soon as the repository is opened inside VSCode—no manual setup required.

## Recommended Flow

1. **Open the interactive menu** via the `Neodoo: Open Interactive Menu` task when a role needs to explore projects or run guided operations.
2. **Validate deliverables** with the `Neodoo: Strict Validator` task. The input prompt lets the agent target any project or addon path.
3. **Prototype generators** using `Neodoo: Dry-run Module Generator`; agents can iterate on module names and template types without touching disk.
4. **Perform health checks** through `Neodoo: Doctor` before handing work to another specialized role.
5. **Debug scripted flows** by launching `Neodoo CLI: Create from docs/.neodoo.yml` (reads the example configuration shipped with the docs) or the interactive launcher if a transcript is required.
6. **Plan migrations** with `Neodoo: Migration Analyzer`, feeding the module path and source version to receive a JSON-ready report.

The shared environment variable `NEODOO_FRAMEWORK_ROOT` is automatically injected into the integrated terminal for macOS, Linux and Windows, so shell scripts can reference the framework root consistently.

## Role-to-Action Mapping

Each role documented in `framework/roles/` can adopt a default toolkit inside VSCode:

- **Backend Developer** → run generator dry-runs, validate addons in strict mode and keep the interactive menu handy for migrations.
- **DevOps Engineer** → trigger `Neodoo: Doctor`, inspect docker-compose templates and extend tasks with deployment commands.
- **Security Expert** → combine strict validation with custom scripts launched from the integrated terminal using the shared environment variable.
- **Data Migration Specialist** → use the launch configuration to rehearse scripted project creation before running migrations.
- **Business Analyst / UX roles** → open the interactive menu to inspect demo projects and hand off validated requirements.

Encourage agents to log their actions (for example, in a shared scratchpad) so handovers remain auditable.

## Customising for Teams

- Duplicate the tasks and launch entries to add organisation-specific flows (for example, QA smoke tests or lint pipelines).
- Extend `settings.json` with additional file associations or formatters when introducing new languages.
- Use VSCode "Command Runner" style extensions (recommended in the list) to bind the tasks to keyboard shortcuts for an even smoother vibecoding experience.

With this playbook in place, VSCode becomes the orchestration cockpit for your multi-role agent setup while staying aligned with the framework’s validated workflows.
