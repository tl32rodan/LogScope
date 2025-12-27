from dataclasses import dataclass
from typing import Optional, Pattern
import re


@dataclass(frozen=True)
class Rule:
    """Pattern-based rule used to identify issues in log lines."""

    pattern: str
    owner: str
    action: str
    description: Optional[str] = None
    category: Optional[str] = None

    def compiled(self) -> Pattern[str]:
        """Return a compiled regex for this rule."""
        try:
            return re.compile(self.pattern)
        except re.error as exc:
            raise ValueError(f"Invalid regex pattern '{self.pattern}': {exc}") from exc
