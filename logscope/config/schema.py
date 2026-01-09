from typing import Dict, Iterable, List

REQUIRED_FIELDS: List[str] = ["pattern", "owner", "action"]
OPTIONAL_FIELDS: List[str] = ["description", "category"]


def validate_row(row: Dict[str, str], required_fields: Iterable[str] = REQUIRED_FIELDS) -> None:
    """Validate that a CSV row contains required fields and non-empty values.

    Raises:
        ValueError: If a required field is missing or empty.
    """

    for field in required_fields:
        if field not in row:
            raise ValueError(f"Missing required field: {field}")
        if not str(row[field]).strip():
            raise ValueError(f"Field '{field}' must not be empty")
