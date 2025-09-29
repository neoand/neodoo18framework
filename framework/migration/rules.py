"""Static rule definitions to assist migration planning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class MigrationTask:
    ref: str
    title: str
    description: str
    category: str  # e.g. "mandatory", "manual", "optional"
    applies_to: Iterable[str]  # versions ("15", "16", "17")


MIGRATION_TASKS: List[MigrationTask] = [
    MigrationTask(
        ref="manifest_version",
        title="Update module manifest to 18.0.x",
        description="Ensure the __manifest__.py version value uses the 18.0 series and review depends for deprecated modules.",
        category="mandatory",
        applies_to=["15", "16", "17"],
    ),
    MigrationTask(
        ref="qweb_owl_refactor",
        title="Audit QWeb/JS assets for legacy framework usage",
        description="Modules targeting Odoo 17- must replace legacy WebClient widgets with OWL components and migrate assets to the new bundler API (web._assets_*).",
        category="manual",
        applies_to=["15", "16", "17"],
    ),
    MigrationTask(
        ref="python_deprecations",
        title="Review deprecated Python APIs",
        description="Check for removed decorators (api.one/api.multi), direct cr executions, and renamed helpers per the official Odoo migration notes.",
        category="mandatory",
        applies_to=["15", "16"],
    ),
    MigrationTask(
        ref="mail_realtime",
        title="Update mail/channel integrations",
        description="Odoo 18 consolidates real-time features; ensure mail.thread overrides adopt the new discuss real-time services.",
        category="manual",
        applies_to=["15", "16", "17"],
    ),
    MigrationTask(
        ref="data_migration",
        title="Plan database migration",
        description="Use the BaseDataMigration helpers to script ETL steps, ensure staging rehearsals, and validate reconciliation reports after migrating to 18.",
        category="mandatory",
        applies_to=["15", "16", "17"],
    ),
]


DEPRECATED_DEPENDENCIES = {
    "web_enterprise": "Odoo 18 consolidates the web client; remove this dependency.",
    "bus": "Real-time bus services moved to discuss for 18. Use 'mail'/'discuss' services instead.",
}

LEGACY_JS_PATTERNS = [
    "odoo.define(",
    "require('web.core')",
    "owl.Component.extend(",
]

LEGACY_DIRECTORIES = [
    "static/src/js/legacy",
    "static/src/js/widgets",
    "static/src/xml",
]
