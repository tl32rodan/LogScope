from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Issue:
    """Represents a matched log entry based on a rule."""

    file_path: Path
    line_number: int
    message: str
    rule_pattern: str
    owner: str
    action: str
    category: Optional[str] = None
    description: Optional[str] = None

    def to_dict(self) -> dict:
        """Return a dictionary representation useful for reporting."""
        return {
            "file_path": str(self.file_path),
            "line_number": self.line_number,
            "message": self.message,
            "rule_pattern": self.rule_pattern,
            "owner": self.owner,
            "action": self.action,
            "category": self.category or "",
            "description": self.description or "",
        }
