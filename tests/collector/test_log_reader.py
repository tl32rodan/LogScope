import tempfile
import unittest
from pathlib import Path

from logscope.collector.log_reader import LogLine, read_log_lines


class LogReaderTest(unittest.TestCase):
    def test_read_log_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.log"
            path.write_text("first\nERROR second\nthird", encoding="utf-8")
            lines = list(read_log_lines([path]))
            self.assertEqual(
                lines[0],
                LogLine(file_path=path, line_number=2, text="ERROR second"),
            )
            self.assertEqual(len(lines), 1)

    def test_read_log_lines_respects_path_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "b.log"
            second = root / "a.log"
            first.write_text("first", encoding="utf-8")
            second.write_text("ERROR second", encoding="utf-8")

            lines = list(read_log_lines([first, second]))
            self.assertEqual(lines[0].file_path, second)


if __name__ == "__main__":
    unittest.main()
