"""Base tooling for data migrations between Odoo versions."""

from __future__ import annotations

import contextlib
import logging
import time
from typing import Iterable, Protocol


_logger = logging.getLogger(__name__)


class BaseDataMigration(Protocol):
    """Common interface for migration services executed inside Odoo."""

    name: str

    def run(self) -> None:
        """Execute the migration workflow."""


class MigrationMixin:
    """Utility helpers shared by migration scripts."""

    def __init__(self, env):
        self.env = env

    @contextlib.contextmanager
    def migration_step(self, description: str):
        """Context manager that logs the runtime of a migration step."""
        start = time.time()
        _logger.info("[migration] starting: %s", description)
        try:
            yield
        except Exception as exc:  # pragma: no cover - defensive logging only
            elapsed = time.time() - start
            _logger.exception("[migration] failed: %s (%.2fs)", description, elapsed)
            raise exc
        else:
            elapsed = time.time() - start
            _logger.info("[migration] completed: %s (%.2fs)", description, elapsed)

    def log_record(self, model: str, record_id: int | str, action: str, message: str | None = None) -> None:
        """Persist a migration log entry if the auxiliary model exists."""
        if not self.env.registry.models.get('migration.log'):
            _logger.debug("migration.log model not installed; skipping log entry")
            return
        self.env['migration.log'].create({
            'model': model,
            'res_id': record_id,
            'action': action,
            'message': message,
        })

    def chunked(self, iterable: Iterable, size: int):
        """Yield items from ``iterable`` in chunks of ``size``."""
        bucket = []
        for item in iterable:
            bucket.append(item)
            if len(bucket) >= size:
                yield bucket
                bucket = []
        if bucket:
            yield bucket
