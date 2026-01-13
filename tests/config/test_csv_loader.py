import tempfile
import unittest
from pathlib import Path

from logscope.config.csv_loader import load_rules_from_csv


class CsvLoaderTest(unittest.TestCase):
    def test_loads_rules(self):
        content = "pattern,owner,action,description\nERROR,team-a,investigate,Runtime error\n"
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "rules.csv"
            csv_path.write_text(content, encoding="utf-8")
            rules = load_rules_from_csv(csv_path)
            self.assertEqual(len(rules), 1)
            self.assertEqual(rules[0].owner, "team-a")
            self.assertEqual(rules[0].description, "Runtime error")

    def test_optional_fields_empty_become_none(self):
        content = "pattern,owner,action,description,category\nERROR,team-a,fix,   ,\n"
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "rules.csv"
            csv_path.write_text(content, encoding="utf-8")
            rules = load_rules_from_csv(csv_path)
            self.assertIsNone(rules[0].description)
            self.assertIsNone(rules[0].category)

    def test_empty_rows_are_skipped(self):
        content = (
            "pattern,owner,action,description\n"
            "ERROR,team-a,investigate,Runtime error\n"
            "\n"
            "WARN,team-b,monitor,Warning\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "rules.csv"
            csv_path.write_text(content, encoding="utf-8")
            rules = load_rules_from_csv(csv_path)
            self.assertEqual(len(rules), 2)
            self.assertEqual(rules[0].owner, "team-a")
            self.assertEqual(rules[1].owner, "team-b")


if __name__ == "__main__":
    unittest.main()
