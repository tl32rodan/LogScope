import unittest
from pathlib import Path

from logscope.collector.log_reader import LogLine
from logscope.matcher.regex_engine import RegexEngine, match_rules
from logscope.model.rule import Rule


class RegexEngineTest(unittest.TestCase):
    def setUp(self):
        self.rules = [Rule(pattern=r"ERROR", owner="team-a", action="investigate")]

    def test_engine_matches_lines(self):
        lines = [LogLine(Path("/tmp/log"), 1, "[ERROR] failed"), LogLine(Path("/tmp/log"), 2, "ok")]
        engine = RegexEngine(self.rules)
        issues = engine.match(lines)
        self.assertEqual(len(issues), 1)
        self.assertEqual(len(issues[0].log_files), 1)

    def test_match_rules_helper(self):
        lines = [LogLine(Path("/tmp/log"), 1, "[ERROR] failed"), LogLine(Path("/tmp/log"), 3, "[ERROR] again")]
        issues = match_rules(lines, self.rules)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].owner, "team-a")
        self.assertEqual(issues[0].to_dict()["count"], 2)
        self.assertEqual(issues[0].to_dict()["log_files"], ["/tmp/log"])


if __name__ == "__main__":
    unittest.main()
