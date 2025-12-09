import tempfile
import unittest
from pathlib import Path

from logscope.app.cli import build_parser, main


class CliTest(unittest.TestCase):
    def test_build_parser_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["analysis", "/configs.json", "/issues"])
        self.assertEqual(args.config_map, Path("/configs.json"))
        self.assertEqual(args.issue_store_root, Path("/issues"))

    def test_main_runs_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            logs_dir = root / "logs"
            logs_dir.mkdir()
            log_path = logs_dir / "app.log"
            log_path.write_text("[ERROR] failed", encoding="utf-8")

            csv_path = root / "rules.csv"
            csv_path.write_text("pattern,owner,action\nERROR,team-a,investigate\n", encoding="utf-8")

            config_map = root / "config.json"
            config_map.write_text(
                '[{"id": "default", "config": "'
                + str(csv_path)
                + '", "log_root": "'
                + str(logs_dir)
                + '"}]',
                encoding="utf-8",
            )

            store_root = root / "issues"
            exit_code = main(["analysis", str(config_map), str(store_root)])
            self.assertEqual(exit_code, 0)
            summary_path = store_root / "default" / "issues.json"
            self.assertTrue(summary_path.exists())


if __name__ == "__main__":
    unittest.main()
