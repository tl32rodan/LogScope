from pathlib import Path
from typing import Iterable, List


def scan_logs(root: Path, patterns: Iterable[str]) -> List[Path]:
    """Return all log file paths matching provided glob patterns under root."""
    matched: List[Path] = []
    for pattern in patterns:
        matched.extend(root.glob(pattern))
    return sorted({path.resolve() for path in matched if path.is_file()})
