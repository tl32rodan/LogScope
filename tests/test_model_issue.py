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
        self.assertEqual(result["logs"][0]["file_path"], "/tmp/log.txt")
        self.assertEqual(result["logs"][1]["message"], "Another error")


if __name__ == "__main__":
    unittest.main()
