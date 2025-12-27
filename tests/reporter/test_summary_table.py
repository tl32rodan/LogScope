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

    def test_summary_rows_are_sorted(self):
        issue_b = Issue("B", "owner", "action", category="b", description="b")
        issue_b.add_log(LogEntry(Path("/tmp/log-b"), 1, "b"))
        issue_a = Issue("A", "owner", "action", category="a", description="a")
        issue_a.add_log(LogEntry(Path("/tmp/log-a"), 1, "a"))
        issue_a_owner = Issue("A", "owner-2", "action", category="a", description="a")
        issue_a_owner.add_log(LogEntry(Path("/tmp/log-c"), 1, "c"))

        table = SummaryTable([issue_b, issue_a_owner, issue_a])
        rows = table.to_rows()

        self.assertEqual([row["rule_pattern"] for row in rows], ["A", "A", "B"])
        self.assertEqual([row["owner"] for row in rows], ["owner", "owner-2", "owner"])


if __name__ == "__main__":
    unittest.main()
