from typing import Generator, Iterable, List, Sequence

from logscope.collector.log_reader import LogLine
from logscope.model.issue import Issue
from logscope.model.rule import Rule


class RegexEngine:
    """Applies regex-based rules to log lines and yields issues."""

    def __init__(self, rules: Sequence[Rule]):
        self._rules = list(rules)
        self._compiled = [(rule, rule.compiled()) for rule in self._rules]

    def match(self, lines: Iterable[LogLine]) -> Generator[Issue, None, None]:
        for log_line in lines:
            for rule, compiled in self._compiled:
                if compiled.search(log_line.text):
                    yield Issue(
                        file_path=log_line.file_path,
                        line_number=log_line.line_number,
                        message=log_line.text,
                        rule_pattern=rule.pattern,
                        owner=rule.owner,
                        action=rule.action,
                        category=rule.category,
                        description=rule.description,
                    )


def match_rules(lines: Iterable[LogLine], rules: Sequence[Rule]) -> List[Issue]:
    """Convenience function to return all issues for given lines and rules."""
    engine = RegexEngine(rules)
    return list(engine.match(lines))
