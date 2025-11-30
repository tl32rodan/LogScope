# LogScope

LogScope is a log-driven rule engine that scans log files, applies owner-defined regular expressions, and builds a summary table of issues. It uses a CSV rule definition to map patterns to owners and actions, then reports matches as a CSV summary.

## Project layout

- `src/logscope/model`: Core domain models (`Rule`, `Issue`).
- `src/logscope/config`: CSV configuration loader and schema validation.
- `src/logscope/collector`: File discovery and log reading utilities.
- `src/logscope/matcher`: Regex engine and filters.
- `src/logscope/reporter`: Summary table builder and CSV export.
- `src/logscope/app`: Pipeline runner and CLI entrypoint.
- `tests`: Unit tests for each module.

## Quickstart

Create a CSV rules file (headers: `pattern,owner,action,description,category`) and place your log files under a root directory. Run the pipeline via CLI:

```bash
PYTHONPATH=src python -m logscope.app.cli <log_root> <rule_csv_path> <output_csv_path> --pattern "**/*.log"
```

Run all unit tests:

```bash
PYTHONPATH=src python -m unittest discover
```
