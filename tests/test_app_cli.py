import csv
import tempfile
import unittest
from pathlib import Path

from logscope.app.cli import build_parser, main


class CliTest(unittest.TestCase):
    def test_build_parser_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["/logs", "rules.csv", "out.csv"])
        self.assertEqual(args.patterns, None)

    def test_main_runs_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "logs").mkdir()
            log_path = root / "logs" / "app.log"
            log_path.write_text("[ERROR] failed", encoding="utf-8")

            csv_path = root / "rules.csv"
            csv_path.write_text("pattern,owner,action\nERROR,team-a,investigate\n", encoding="utf-8")

            output_path = root / "summary.csv"
            exit_code = main([str(root), str(csv_path), str(output_path), "--pattern", "**/*.log"])
            self.assertEqual(exit_code, 0)
            with output_path.open() as handle:
                reader = list(csv.DictReader(handle))
                self.assertEqual(len(reader), 1)


if __name__ == "__main__":
    unittest.main()
