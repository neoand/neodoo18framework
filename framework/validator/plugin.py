"""Plugin infrastructure for the Neodoo validator."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol


class ValidationResult:
    """Aggregates validation issues detected by plugins."""

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.auto_fixes: List[str] = []
        self.is_valid: bool = True

    def add_error(self, message: str) -> None:
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def add_auto_fix(self, message: str) -> None:
        self.auto_fixes.append(message)

    def has_messages(self) -> bool:
        return bool(self.errors or self.warnings or self.auto_fixes)


@dataclass
class ValidationContext:
    """Runtime information shared with plugins during a validation run."""

    root: Path
    auto_fix: bool
    strict: bool
    template_mode: bool
    verbose: bool = False
    module_name: Optional[str] = None
    scratch: Dict[str, Any] = field(default_factory=dict)


class ValidatorPlugin(Protocol):
    """Protocol that all validator plugins must implement."""

    name: str
    description: str

    def setup(self, context: ValidationContext) -> None:
        ...

    def validate_directory(self, directory: Path, context: ValidationContext) -> List[ValidationResult]:
        ...

    def supports(self, file_path: Path, context: ValidationContext) -> bool:
        ...

    def validate_file(self, file_path: Path, context: ValidationContext) -> Optional[ValidationResult]:
        ...

    def finalize(self, context: ValidationContext) -> List[ValidationResult]:
        ...


class BaseValidatorPlugin:
    """Convenience base class with no-op defaults."""

    name = "base"
    description = "Base plugin"

    def setup(self, context: ValidationContext) -> None:  # pragma: no cover - default noop
        return

    def validate_directory(self, directory: Path, context: ValidationContext) -> List[ValidationResult]:  # pragma: no cover - default noop
        return []

    def supports(self, file_path: Path, context: ValidationContext) -> bool:  # pragma: no cover - default noop
        return False

    def validate_file(self, file_path: Path, context: ValidationContext) -> Optional[ValidationResult]:  # pragma: no cover - default noop
        return None

    def finalize(self, context: ValidationContext) -> List[ValidationResult]:  # pragma: no cover - default noop
        return []
