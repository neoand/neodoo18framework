"""Validator package exposing the pluggable API."""

from .plugin import ValidationContext, ValidationResult, ValidatorPlugin
from .plugin_manager import PluginManager
from .validate import Odoo18Validator, validate_path

__all__ = [
    "Odoo18Validator",
    "ValidationContext",
    "ValidationResult",
    "ValidatorPlugin",
    "PluginManager",
    "validate_path",
]
