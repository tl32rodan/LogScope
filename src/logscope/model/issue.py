from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Set


@dataclass
class LogEntry:
    file_path: Path
    line_number: int
    message: str

@dataclass
class Issue:
    """Represents a matched finding that can include multiple log entries."""

    rule_pattern: str
    owner: str
    action: str
    category: Optional[str] = None
    description: Optional[str] = None
    log_files: Set[Path] = field(default_factory=set)
    first_message: Optional[str] = None
    count: int = 0

    def add_log(self, entry: LogEntry) -> None:
        if self.first_message is None:
            self.first_message = entry.message
        self.log_files.add(entry.file_path)
        self.count += 1

    def to_dict(self) -> dict:
        """Return a dictionary representation useful for reporting."""
        return {
            "rule_pattern": self.rule_pattern,
            "owner": self.owner,
            "action": self.action,
            "category": self.category or "",
            "description": self.description or "",
            "log_files": sorted(str(path) for path in self.log_files),
            "sample_message": self.first_message or "",
            "count": self.count,
        }
