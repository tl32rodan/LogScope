import json
import tempfile
import unittest
from pathlib import Path

from logscope.integrations.issue_store import InMemoryIssueStore, JsonIssueStore


class JsonIssueStoreTest(unittest.TestCase):
    def test_store_and_fetch_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = JsonIssueStore(root)

            written = store.store("alpha", [{"rule": "ERROR"}])

            self.assertTrue(written.exists())
            payload = json.loads(written.read_text(encoding="utf-8"))
            self.assertEqual(payload["rules"], [{"rule": "ERROR"}])
            self.assertEqual(store.fetch("alpha"), {"alpha": [{"rule": "ERROR"}]})

    def test_store_merges_same_config_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = JsonIssueStore(root)

            store.store("alpha", [{"rule": "ERROR"}])
            store.store("alpha", [{"rule": "WARN"}])

            payload = json.loads((root / "alpha" / "issues.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["rules"], [{"rule": "ERROR"}, {"rule": "WARN"}])
            self.assertEqual(
                store.fetch("alpha"),
                {"alpha": [{"rule": "ERROR"}, {"rule": "WARN"}]},
            )

    def test_fetch_handles_missing_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JsonIssueStore(Path(tmp) / "missing")
            self.assertEqual(store.fetch(), {})


class InMemoryIssueStoreTest(unittest.TestCase):
    def test_store_merges_same_config_id(self):
        store = InMemoryIssueStore()
        store.store("alpha", [{"rule": "ERROR"}])
        store.store("alpha", [{"rule": "WARN"}])
        self.assertEqual(
            store.fetch("alpha"),
            {"alpha": [{"rule": "ERROR"}, {"rule": "WARN"}]},
        )


if __name__ == "__main__":
    unittest.main()
