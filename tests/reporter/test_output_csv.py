import csv
import tempfile
import unittest
from pathlib import Path

from logscope.reporter.output_csv import write_summary_to_csv


class OutputCsvTest(unittest.TestCase):
    def test_write_summary_to_csv(self):
        rows = [
            {"file_path": "/tmp/log", "line_number": 1, "message": "err", "rule_pattern": "PAT", "owner": "o", "action": "a", "category": "", "description": ""}
        ]
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "summary.csv"
            write_summary_to_csv(rows, output)
            with output.open() as handle:
                reader = list(csv.DictReader(handle))
                self.assertEqual(len(reader), 1)
                self.assertEqual(reader[0]["message"], "err")

    def test_write_empty_rows_creates_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "empty.csv"
            write_summary_to_csv([], output)
            self.assertEqual(output.read_text(encoding="utf-8"), "")


if __name__ == "__main__":
    unittest.main()
