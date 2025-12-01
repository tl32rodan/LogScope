import tempfile
import unittest
from pathlib import Path

from logscope.app.runner import ConfigBundle, run_application, run_pipeline
from logscope.integrations.cassandra_client import InMemoryIssueStore


class RunnerTest(unittest.TestCase):
    def test_run_pipeline_creates_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log_path = root / "app.log"
            log_path.write_text("[ERROR] failed", encoding="utf-8")

            csv_path = root / "rules.csv"
            csv_path.write_text("pattern,owner,action\nERROR,team-a,investigate\n", encoding="utf-8")

            output_path = root / "summary.json"
            summary = run_pipeline(root, csv_path, output_path, ["**/*.log"], filters=())

            self.assertEqual(len(summary), 1)
            data = output_path.read_text(encoding="utf-8")
            self.assertIn("team-a", data)

    def test_run_application_stores_per_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log_dir = root / "logs"
            log_dir.mkdir()
            (log_dir / "first.log").write_text("[ERROR] one", encoding="utf-8")
            (log_dir / "second.log").write_text("[ERROR] two", encoding="utf-8")

            csv_path = root / "rules.csv"
            csv_path.write_text("pattern,owner,action\nERROR,team-a,investigate\n", encoding="utf-8")

            bundles = [
                ConfigBundle(
                    name="conf-a",
                    config_path=csv_path,
                    log_root=log_dir,
                    patterns=["**/*.log"],
                )
            ]
            store = InMemoryIssueStore()
            result = run_application(bundles, store)
            self.assertEqual(len(result["conf-a"].to_rows()), 1)
            stored = store.fetch()["conf-a"]
            self.assertEqual(len(stored), 1)


if __name__ == "__main__":
    unittest.main()
