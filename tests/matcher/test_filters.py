import unittest
from pathlib import Path

from logscope.matcher.filters import apply_filters, exclude_by_owner
from logscope.model.issue import Issue, LogEntry


class FiltersTest(unittest.TestCase):
    def test_apply_filters(self):
        issue_a = Issue("PAT", "a", "fix")
        issue_a.add_log(LogEntry(Path("/tmp/log"), 1, "err"))
        issue_b = Issue("PAT", "b", "fix")
        issue_b.add_log(LogEntry(Path("/tmp/log"), 2, "err"))
        filtered = list(apply_filters([issue_a, issue_b], [exclude_by_owner("a")]))
        self.assertEqual(filtered, [issue_b])


if __name__ == "__main__":
    unittest.main()
