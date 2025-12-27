import json
import tempfile
import unittest
from pathlib import Path

from logscope.app.cli import load_bundles
from logscope.app.runner import run_application
from logscope.integrations.issue_store import JsonIssueStore


class ExampleRegressionTest(unittest.TestCase):
    def test_example_pipeline_matches_golden_output(self):
        repo_root = Path(__file__).resolve().parents[2]
        config_path = repo_root / "example" / "config.json"
        expected_path = repo_root / "example" / "logs" / "demo_summary.json"

        bundles = load_bundles(config_path)

        with tempfile.TemporaryDirectory() as tmp:
            store = JsonIssueStore(Path(tmp))
            run_application(bundles, store)
            output_path = Path(tmp) / "demo" / "issues.json"

            output_payload = json.loads(output_path.read_text(encoding="utf-8"))
            expected_payload = json.loads(expected_path.read_text(encoding="utf-8"))

            self.assertEqual(output_payload, expected_payload)


if __name__ == "__main__":
    unittest.main()
