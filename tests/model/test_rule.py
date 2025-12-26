import unittest

from logscope.model.rule import Rule


class RuleModelTest(unittest.TestCase):
    def test_compiled_returns_pattern(self):
        rule = Rule(pattern=r"ERROR", owner="team-a", action="fix")
        compiled = rule.compiled()
        self.assertTrue(compiled.search("[ERROR] something"))


if __name__ == "__main__":
    unittest.main()
