import unittest
from pathlib import Path

from logscope.model.issue import Issue
from logscope.reporter.summary_table import SummaryTable


class SummaryTableTest(unittest.TestCase):
    def test_summary_builds_rows(self):
        issue = Issue(Path("/tmp/log"), 1, "err", "PAT", "owner", "action")
        table = SummaryTable([issue])
        rows = table.to_rows()
        self.assertEqual(len(table), 1)
        self.assertEqual(rows[0]["message"], "err")


if __name__ == "__main__":
    unittest.main()
