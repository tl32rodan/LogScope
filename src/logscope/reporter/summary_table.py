from typing import Dict, Iterable, List

from logscope.model.issue import Issue


class SummaryTable:
    """Container for issue summaries."""

    def __init__(self, issues: Iterable[Issue]):
        self.rows: List[dict] = [issue.to_dict() for issue in issues]

    def to_rows(self) -> List[dict]:
        return list(self.rows)

    def to_mapping(self) -> Dict[str, List[dict]]:
        return {"issues": self.to_rows()}

    def __len__(self) -> int:
        return len(self.rows)
