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

            results = scan_logs([str(root / "**" / "*.log")])
            self.assertEqual(len(results), 2)
            self.assertTrue(all(path.suffix == ".log" for path in results))

    def test_scan_logs_aggregates_unique_sorted_patterns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "b.log").write_text("second", encoding="utf-8")
            (root / "a.log").write_text("first", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "c.log").write_text("third", encoding="utf-8")

            results = scan_logs([str(root / "**" / "*.log"), str(root / "*.log")])
            result_paths = [path.as_posix() for path in results]

            self.assertEqual(
                result_paths,
                sorted(set(result_paths)),
            )
            self.assertEqual(len(result_paths), 3)

    def test_scan_logs_supports_absolute_patterns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            logs_dir = root / "logs"
            logs_dir.mkdir()
            (logs_dir / "app.log").write_text("line", encoding="utf-8")

            results = scan_logs([str(logs_dir / "*.log")])

            self.assertEqual(results, [logs_dir / "app.log"])


if __name__ == "__main__":
    unittest.main()
