import json
import tempfile
import unittest
from pathlib import Path

from logscope.reporter.output_json import write_summary_to_json


class OutputJsonTest(unittest.TestCase):
    def test_write_summary_to_json(self):
        data = {"issues": [{"owner": "team-a", "count": 2}]}
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "out.json"
            write_summary_to_json(data, path)
            loaded = json.loads(path.read_text())
            self.assertEqual(loaded["issues"][0]["owner"], "team-a")


if __name__ == "__main__":
    unittest.main()
