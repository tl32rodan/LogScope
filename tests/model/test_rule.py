import unittest

from logscope.model.rule import Rule


class RuleModelTest(unittest.TestCase):
    def test_compiled_returns_pattern(self):
        rule = Rule(pattern=r"ERROR", owner="team-a", action="fix")
        compiled = rule.compiled()
        self.assertTrue(compiled.search("[ERROR] something"))

    def test_invalid_regex_raises_value_error(self):
        rule = Rule(pattern=r"(", owner="team-a", action="fix")
        with self.assertRaises(ValueError) as context:
            rule.compiled()
        self.assertIn("Invalid regex pattern", str(context.exception))


if __name__ == "__main__":
    unittest.main()
