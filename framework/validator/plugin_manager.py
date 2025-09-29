"""Discovery and lifecycle management for validator plugins."""

from __future__ import annotations

import importlib.util
import sys
import uuid
from pathlib import Path
from typing import List

from .plugin import BaseValidatorPlugin, ValidatorPlugin


class PluginLoadError(Exception):
    """Raised when a plugin fails to load."""


class PluginManager:
    """Keeps track of validator plugins and can discover external ones."""

    def __init__(self) -> None:
        self._plugins: List[ValidatorPlugin] = []
        self._load_errors: List[str] = []

    @property
    def plugins(self) -> List[ValidatorPlugin]:
        return list(self._plugins)

    @property
    def load_errors(self) -> List[str]:
        return list(self._load_errors)

    def register(self, plugin: ValidatorPlugin) -> None:
        self._plugins.append(plugin)

    def register_many(self, plugins: List[ValidatorPlugin]) -> None:
        for plugin in plugins:
            self.register(plugin)

    def load_directory(self, directory: Path) -> None:
        directory = directory.expanduser().resolve()
        if not directory.exists() or not directory.is_dir():
            self._load_errors.append(f"Plugin directory not found: {directory}")
            return

        for path in sorted(directory.glob('*.py')):
            if path.name.startswith('_'):
                continue
            try:
                self._load_module(path)
            except Exception as exc:  # pragma: no cover - defensive
                self._load_errors.append(f"Failed to load plugin '{path}': {exc}")

    def describe_plugins(self) -> List[str]:
        descriptions = []
        for plugin in self._plugins:
            desc = getattr(plugin, 'description', '').strip()
            descriptions.append(f"{plugin.name}: {desc}" if desc else plugin.name)
        return descriptions

    # ------------------------------------------------------------------
    def _load_module(self, file_path: Path) -> None:
        module_name = f"neodoo_validator_plugin_{file_path.stem}_{uuid.uuid4().hex}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            raise PluginLoadError(f"Cannot create import spec for {file_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        plugins: List[ValidatorPlugin] = []
        if hasattr(module, 'register'):
            registered = module.register()
            if isinstance(registered, (list, tuple)):
                plugins.extend(registered)
            elif registered:
                plugins.append(registered)  # type: ignore[arg-type]
        else:
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, BaseValidatorPlugin) and obj is not BaseValidatorPlugin:
                    plugins.append(obj())

        if not plugins:
            raise PluginLoadError(f"No plugins found in {file_path}")

        for plugin in plugins:
            if not hasattr(plugin, 'name'):
                raise PluginLoadError(f"Plugin {plugin} missing 'name' attribute")
            self.register(plugin)
