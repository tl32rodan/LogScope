"""Issue store implementations decoupled from persistence backends."""

import json
from pathlib import Path
from typing import Dict, List, Optional


class InMemoryIssueStore:
    """Lightweight issue store for testing and offline usage."""

    def __init__(self):
        self._storage: Dict[str, List[dict]] = {}

    def store(self, config_id: str, issues: List[dict]) -> None:
        existing = self._storage.get(config_id, [])
        self._storage[config_id] = list(existing) + list(issues)

    def fetch(self, config_id: Optional[str] = None) -> Dict[str, List[dict]]:
        if config_id is None:
            return dict(self._storage)
        return {config_id: list(self._storage.get(config_id, []))}


class JsonIssueStore:
    """Persist issues as JSON files rooted at a configured directory."""

    def __init__(self, root: Path):
        self._root = Path(root)

    def _issue_path(self, config_id: str) -> Path:
        return self._root / config_id / "issues.json"

    def store(self, config_id: str, issues: List[dict]) -> Path:
        output_path = self._issue_path(config_id)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        existing = self._load_issues(output_path)
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump({"rules": list(existing) + list(issues)}, handle, indent=2)
        return output_path

    def fetch(self, config_id: Optional[str] = None) -> Dict[str, List[dict]]:
        if config_id:
            return {config_id: self._load_issues(self._issue_path(config_id))}

        results: Dict[str, List[dict]] = {}
        if not self._root.exists():
            return results

        for issue_file in self._root.glob("*/issues.json"):
            results[issue_file.parent.name] = self._load_issues(issue_file)
        return results

    @staticmethod
    def _load_issues(path: Path) -> List[dict]:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return list(payload.get("rules", []))
