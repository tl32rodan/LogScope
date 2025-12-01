from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class LogEntry:
    file_path: Path
    line_number: int
    message: str

    def to_dict(self) -> dict:
        return {
            "file_path": str(self.file_path),
            "line_number": self.line_number,
            "message": self.message,
        }


@dataclass
class Issue:
    """Represents a matched finding that can include multiple log entries."""

    rule_pattern: str
    owner: str
    action: str
    category: Optional[str] = None
    description: Optional[str] = None
    logs: List[LogEntry] = field(default_factory=list)

    def add_log(self, entry: LogEntry) -> None:
        self.logs.append(entry)

    def to_dict(self) -> dict:
        """Return a dictionary representation useful for reporting."""
        return {
            "rule_pattern": self.rule_pattern,
            "owner": self.owner,
            "action": self.action,
            "category": self.category or "",
            "description": self.description or "",
            "logs": [entry.to_dict() for entry in self.logs],
            "count": len(self.logs),
        }
