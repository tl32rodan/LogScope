from pathlib import Path
from typing import Iterable, Sequence

from logscope.collector.file_scanner import scan_logs
from logscope.collector.log_reader import read_log_lines
from logscope.config.csv_loader import load_rules_from_csv
from logscope.matcher.filters import apply_filters
from logscope.matcher.regex_engine import RegexEngine
from logscope.model.issue import Issue
from logscope.model.rule import Rule
from logscope.reporter.output_csv import write_summary_to_csv
from logscope.reporter.summary_table import SummaryTable


def run_pipeline(
    log_root: Path,
    rule_csv_path: Path,
    output_csv_path: Path,
    patterns: Sequence[str],
    filters: Iterable = (),
) -> SummaryTable:
    """Execute the end-to-end pipeline from logs to summary CSV."""
    rules = load_rules_from_csv(rule_csv_path)
    log_paths = scan_logs(log_root, patterns)
    log_lines = read_log_lines(log_paths)
    engine = RegexEngine(rules)
    issues = engine.match(log_lines)
    filtered_issues = list(apply_filters(issues, filters))
    summary = SummaryTable(filtered_issues)
    write_summary_to_csv(summary.to_rows(), output_csv_path)
    return summary
