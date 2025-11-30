import unittest
from pathlib import Path

from logscope.model.issue import Issue


class IssueModelTest(unittest.TestCase):
    def test_to_dict_contains_all_fields(self):
        issue = Issue(
            file_path=Path("/tmp/log.txt"),
            line_number=10,
            message="Error occurred",
            rule_pattern="ERROR",
            owner="team-a",
            action="investigate",
            category="runtime",
            description="Runtime error",
        )
        result = issue.to_dict()
        self.assertEqual(result["file_path"], str(issue.file_path))
        self.assertEqual(result["line_number"], 10)
        self.assertEqual(result["category"], "runtime")
        self.assertEqual(result["description"], "Runtime error")


if __name__ == "__main__":
    unittest.main()
