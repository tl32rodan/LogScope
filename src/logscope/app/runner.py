from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Sequence

from logscope.collector.file_scanner import scan_logs
from logscope.collector.log_reader import read_log_lines
from logscope.config.csv_loader import load_rules_from_csv
from logscope.matcher.filters import apply_filters
from logscope.matcher.regex_engine import RegexEngine
from logscope.reporter.output_json import write_summary_to_json
from logscope.reporter.summary_table import SummaryTable


@dataclass
class ConfigBundle:
    name: str
    config_path: Path
    log_root: Path
    patterns: Sequence[str]


def run_pipeline(
    log_root: Path,
    rule_csv_path: Path,
    output_json_path: Path,
    patterns: Sequence[str],
    filters: Iterable = (),
) -> SummaryTable:
    """Execute the end-to-end pipeline from logs to summary JSON."""
    rules = load_rules_from_csv(rule_csv_path)
    log_paths = scan_logs(log_root, patterns)
    log_lines = read_log_lines(log_paths)
    engine = RegexEngine(rules)
    issues = engine.match(log_lines)
    filtered_issues = list(apply_filters(issues, filters))
    summary = SummaryTable(filtered_issues)
    write_summary_to_json(summary.to_mapping(), output_json_path)
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
            log_root=bundle.log_root,
            rule_csv_path=bundle.config_path,
            output_json_path=bundle.log_root / f"{bundle.name}_summary.json",
            patterns=bundle.patterns,
            filters=filters,
        )
        issue_store.store(bundle.name, summary.to_rows())
        results[bundle.name] = summary
    return results
