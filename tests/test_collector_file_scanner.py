import tempfile
import unittest
from pathlib import Path

from logscope.collector.file_scanner import scan_logs


class FileScannerTest(unittest.TestCase):
    def test_scan_logs_with_patterns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.log").write_text("first", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "b.log").write_text("second", encoding="utf-8")
            (root / "ignore.txt").write_text("nope", encoding="utf-8")

            results = scan_logs(root, ["**/*.log"])
            self.assertEqual(len(results), 2)
            self.assertTrue(all(path.suffix == ".log" for path in results))


if __name__ == "__main__":
    unittest.main()
