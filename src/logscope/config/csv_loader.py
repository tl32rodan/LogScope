import csv
from pathlib import Path
from typing import Iterable, List, Optional

from logscope.model.rule import Rule
from logscope.config import schema


def load_rules_from_csv(csv_path: Path) -> List[Rule]:
    """Load rules from a CSV file.

    The CSV is expected to have headers matching schema.REQUIRED_FIELDS and any
    optional fields listed in schema.OPTIONAL_FIELDS.
    """
    rules: List[Rule] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            _raise_with_path(ValueError("CSV file must have headers"), csv_path)
        _ensure_required_headers(reader.fieldnames, schema.REQUIRED_FIELDS, csv_path)
        for row in reader:
            if _is_empty_row(row):
                continue
            try:
                schema.validate_row(row)
            except ValueError as exc:
                _raise_with_path(exc, csv_path)
            rule = Rule(
                pattern=row["pattern"],
                owner=row["owner"],
                action=row["action"],
                description=_normalize_optional(row.get("description")),
                category=_normalize_optional(row.get("category")),
            )
            rules.append(rule)
    return rules


def _ensure_required_headers(
    headers: Iterable[str],
    required_fields: Iterable[str],
    csv_path: Path,
) -> None:
    missing = [field for field in required_fields if field not in headers]
    if missing:
        _raise_with_path(ValueError(f"Missing required headers: {', '.join(missing)}"), csv_path)


def _normalize_optional(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None
    return value


def _is_empty_row(row: dict) -> bool:
    return not any(str(value).strip() for value in row.values() if value is not None)


def _raise_with_path(error: ValueError, csv_path: Path) -> None:
    raise ValueError(f"{error} (csv_path={csv_path})") from error
