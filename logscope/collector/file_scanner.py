from glob import glob
from pathlib import Path
from typing import Iterable, List


def scan_logs(patterns: Iterable[str]) -> List[Path]:
    """Return all log file paths matching provided absolute glob patterns."""
    matched: List[Path] = []
    for pattern in patterns:
        matched.extend(Path(path) for path in glob(pattern, recursive=True))
    unique_files = {path for path in matched if path.is_file()}
    return sorted(unique_files, key=lambda path: path.as_posix())
