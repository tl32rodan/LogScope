import csv
from pathlib import Path
from typing import Iterable


def write_summary_to_csv(rows: Iterable[dict], output_path: Path) -> None:
    """Write summary rows to a CSV file."""
    rows_list = list(rows)
    if not rows_list:
        output_path.write_text("", encoding="utf-8")
        return

    headers = list(rows_list[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows_list)
