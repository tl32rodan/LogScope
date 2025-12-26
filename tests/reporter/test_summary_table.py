import unittest
from pathlib import Path

from logscope.model.issue import Issue, LogEntry
from logscope.reporter.summary_table import SummaryTable


class SummaryTableTest(unittest.TestCase):
    def test_summary_builds_rows(self):
        issue = Issue("PAT", "owner", "action")
        issue.add_log(LogEntry(Path("/tmp/log"), 1, "err"))
        table = SummaryTable([issue])
        rows = table.to_rows()
        self.assertEqual(len(table), 1)
        self.assertEqual(rows[0]["sample_message"], "err")
        self.assertEqual(rows[0]["log_files"], ["/tmp/log"])
        self.assertEqual(table.to_mapping()["rules"][0]["count"], 1)


if __name__ == "__main__":
    unittest.main()
