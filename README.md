# LogScope

LogScope is a log-driven rule engine that scans log files, applies owner-defined regular expressions, and builds a summary table
of issues. A single issue can aggregate multiple log entries and is exported as JSON for easy downstream integration.

## Project layout

- `src/logscope/model`: Core domain models (`Rule`, `Issue`).
- `src/logscope/config`: CSV configuration loader and schema validation.
- `src/logscope/collector`: File discovery and log reading utilities.
- `src/logscope/matcher`: Regex engine and filters.
- `src/logscope/reporter`: Summary table builder and JSON export.
- `src/logscope/app`: Pipeline runner, multi-config application runner, CLI entrypoint, and optional PySide2 GUI launcher.
- `src/logscope/integrations`: External adapters (e.g., Cassandra issue store).
- `tests`: Unit tests for each module.

## Quickstart

1. Create a CSV rules file (headers: `pattern,owner,action,description,category`) and place your log files under a root directory.
2. Define a JSON config map describing the log roots and configs to process, for example:

```json
[
  {
    "name": "core",
    "config": "./rules.csv",
    "log_root": "./logs",
    "patterns": ["**/*.log"]
  }
]
```

3. Run the pipeline via CLI:

```bash
PYTHONPATH=src python -m logscope.app.cli config.json
```

If `--cassandra-hosts` is provided, issues are persisted via the existing Cassandra cluster; otherwise an in-memory store is used.
Use `--launch-gui` to open a PySide2-based summary view that combines current results with historical Cassandra records.

## Testing

```bash
PYTHONPATH=src python -m unittest discover
```
