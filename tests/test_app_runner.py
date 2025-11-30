import csv
import tempfile
import unittest
from pathlib import Path

from logscope.app.runner import run_pipeline


class RunnerTest(unittest.TestCase):
    def test_run_pipeline_creates_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log_path = root / "app.log"
            log_path.write_text("[ERROR] failed", encoding="utf-8")

            csv_path = root / "rules.csv"
            csv_path.write_text("pattern,owner,action\nERROR,team-a,investigate\n", encoding="utf-8")

            output_path = root / "summary.csv"
            summary = run_pipeline(root, csv_path, output_path, ["**/*.log"], filters=())

            self.assertEqual(len(summary), 1)
            with output_path.open() as handle:
                reader = list(csv.DictReader(handle))
                self.assertEqual(len(reader), 1)
                self.assertEqual(reader[0]["owner"], "team-a")


if __name__ == "__main__":
    unittest.main()
