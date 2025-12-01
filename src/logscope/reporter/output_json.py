import json
from pathlib import Path
from typing import Mapping


def write_summary_to_json(mapping: Mapping[str, object], output_path: Path) -> None:
    """Write summary mapping to a JSON file."""
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(mapping, handle, indent=2)
