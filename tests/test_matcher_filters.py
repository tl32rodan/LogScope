import unittest
from pathlib import Path

from logscope.matcher.filters import apply_filters, exclude_by_owner
from logscope.model.issue import Issue


class FiltersTest(unittest.TestCase):
    def test_apply_filters(self):
        issue_a = Issue(Path("/tmp/log"), 1, "err", "PAT", "a", "fix")
        issue_b = Issue(Path("/tmp/log"), 2, "err", "PAT", "b", "fix")
        filtered = list(apply_filters([issue_a, issue_b], [exclude_by_owner("a")]))
        self.assertEqual(filtered, [issue_b])


if __name__ == "__main__":
    unittest.main()
