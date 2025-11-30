from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Iterable


@dataclass(frozen=True)
class LogLine:
    file_path: Path
    line_number: int
    text: str


def read_log_lines(paths: Iterable[Path]) -> Generator[LogLine, None, None]:
    """Yield LogLine objects for each line in given file paths."""
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for idx, line in enumerate(handle, start=1):
                yield LogLine(file_path=path, line_number=idx, text=line.rstrip("\n"))
