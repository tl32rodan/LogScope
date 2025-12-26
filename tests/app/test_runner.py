import tempfile
import unittest
from pathlib import Path

from logscope.app.runner import ConfigBundle, run_application, run_pipeline
from logscope.integrations.issue_store import InMemoryIssueStore, JsonIssueStore


class RunnerTest(unittest.TestCase):
    def test_run_pipeline_creates_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log_path = root / "app.log"
            log_path.write_text("[ERROR] failed", encoding="utf-8")

            csv_path = root / "rules.csv"
            csv_path.write_text("pattern,owner,action\nERROR,team-a,investigate\n", encoding="utf-8")

            summary = run_pipeline(root, csv_path, ["**/*.log"], filters=())

            self.assertEqual(len(summary), 1)

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
                    config_id="conf-a",
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

    def test_run_application_writes_json_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            logs_dir = root / "logs"
            logs_dir.mkdir()
            (logs_dir / "app.log").write_text("[ERROR] failed", encoding="utf-8")

            csv_path = root / "rules.csv"
            csv_path.write_text("pattern,owner,action\nERROR,team-a,investigate\n", encoding="utf-8")

            store_root = root / "store"
            bundles = [
                ConfigBundle(
                    config_id="conf-a",
                    config_path=csv_path,
                    log_root=logs_dir,
                    patterns=["**/*.log"],
                )
            ]

            store = JsonIssueStore(store_root)
            run_application(bundles, store)

            issues_file = store_root / "conf-a" / "issues.json"
            self.assertTrue(issues_file.exists())
            self.assertIn("team-a", issues_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
