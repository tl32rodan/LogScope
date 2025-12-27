import unittest
from pathlib import Path

from logscope.model.issue import Issue, LogEntry


class IssueModelTest(unittest.TestCase):
    def test_to_dict_contains_all_fields_and_logs(self):
        issue = Issue(
            rule_pattern="ERROR",
            owner="team-a",
            action="investigate",
            category="runtime",
            description="Runtime error",
        )
        issue.add_log(LogEntry(Path("/tmp/log.txt"), 10, "Error occurred"))
        issue.add_log(LogEntry(Path("/tmp/other.log"), 20, "Another error"))
        result = issue.to_dict()
        self.assertEqual(result["category"], "runtime")
        self.assertEqual(result["description"], "Runtime error")
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["log_files"], ["/tmp/log.txt", "/tmp/other.log"])
        self.assertEqual(result["sample_message"], "Error occurred")

    def test_sample_message_uses_earliest_file_and_line(self):
        issue = Issue(
            rule_pattern="ERROR",
            owner="team-a",
            action="investigate",
        )
        issue.add_log(LogEntry(Path("/tmp/z.log"), 1, "later file"))
        issue.add_log(LogEntry(Path("/tmp/a.log"), 5, "earlier file"))
        issue.add_log(LogEntry(Path("/tmp/a.log"), 2, "earliest line"))
        result = issue.to_dict()
        self.assertEqual(result["sample_message"], "earliest line")


if __name__ == "__main__":
    unittest.main()
