from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Sequence

from logscope.collector.file_scanner import scan_logs
from logscope.collector.log_reader import read_log_lines
from logscope.config.csv_loader import load_rules_from_csv
from logscope.matcher.filters import apply_filters
from logscope.matcher.regex_engine import RegexEngine
from logscope.reporter.summary_table import SummaryTable


@dataclass
class ConfigBundle:
    config_id: str
    config_path: Path
    patterns: Sequence[str]


def run_pipeline(
    rule_csv_path: Path,
    patterns: Sequence[str],
    filters: Iterable = (),
) -> SummaryTable:
    """Execute the end-to-end pipeline from logs to summarized issues."""
    rules = load_rules_from_csv(rule_csv_path)
    log_paths = scan_logs(patterns)
    log_lines = read_log_lines(log_paths)
    engine = RegexEngine(rules)
    issues = engine.match(log_lines)
    filtered_issues = list(apply_filters(issues, filters))
    summary = SummaryTable(filtered_issues)
    return summary


def run_application(
    bundles: Sequence[ConfigBundle],
    issue_store,
    filters: Iterable = (),
) -> Dict[str, SummaryTable]:
    """Run multiple config pipelines and persist their issues."""

    results: Dict[str, SummaryTable] = {}
    for bundle in bundles:
        summary = run_pipeline(
            rule_csv_path=bundle.config_path,
            patterns=bundle.patterns,
            filters=filters,
        )
        issue_store.store(bundle.config_id, summary.to_rows())
        results[bundle.config_id] = summary
    return results
