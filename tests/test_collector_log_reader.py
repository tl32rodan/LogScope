import tempfile
import unittest
from pathlib import Path

from logscope.collector.log_reader import LogLine, read_log_lines


class LogReaderTest(unittest.TestCase):
    def test_read_log_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.log"
            path.write_text("first\nsecond", encoding="utf-8")
            lines = list(read_log_lines([path]))
            self.assertEqual(lines[0], LogLine(file_path=path, line_number=1, text="first"))
            self.assertEqual(lines[1].line_number, 2)
            self.assertEqual(lines[1].text, "second")


if __name__ == "__main__":
    unittest.main()
