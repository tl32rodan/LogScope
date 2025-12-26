import json
import tempfile
import unittest
from pathlib import Path

from logscope.reporter.output_json import write_summary_to_json


class OutputJsonTest(unittest.TestCase):
    def test_write_summary_to_json(self):
        data = {"rules": [{"owner": "team-a", "count": 2}]}
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "out.json"
            write_summary_to_json(data, path)
            loaded = json.loads(path.read_text())
            self.assertEqual(loaded["rules"][0]["owner"], "team-a")

    def test_write_summary_creates_parent_directories(self):
        data = {"rules": []}
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = Path(tmpdir) / "nested" / "out.json"
            self.assertFalse(nested_path.parent.exists())

            write_summary_to_json(data, nested_path)

            self.assertTrue(nested_path.exists())
            loaded = json.loads(nested_path.read_text())
            self.assertEqual(loaded["rules"], [])

    def test_write_summary_creates_parent_directories(self):
        data = {"issues": []}
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = Path(tmpdir) / "nested" / "out.json"
            self.assertFalse(nested_path.parent.exists())

            write_summary_to_json(data, nested_path)

            self.assertTrue(nested_path.exists())
            loaded = json.loads(nested_path.read_text())
            self.assertEqual(loaded["issues"], [])


if __name__ == "__main__":
    unittest.main()
