# LogScope

LogScope is a log-driven rule engine that scans log files, applies owner-defined regular expressions, and builds a summary table
of issues. A single issue can aggregate multiple log entries and is exported as JSON for easy downstream integration.

## Project layout

- `src/logscope/model`: Core domain models (`Rule`, `Issue`).
- `src/logscope/config`: CSV configuration loader and schema validation.
- `src/logscope/collector`: File discovery and log reading utilities.
- `src/logscope/matcher`: Regex engine and filters.
- `src/logscope/reporter`: Summary table builder and JSON export.
- `src/logscope/app`: Pipeline runner, multi-config application runner, CLI entrypoint.
- `src/logscope/integrations`: External adapters (e.g., Cassandra issue store).
- `tests`: Unit tests for each module.

## Quickstart

1. Create a CSV rules file (headers: `pattern,owner,action,description,category`) and place your log files under a root directory.
2. Define a JSON config map describing the log roots and configs to process, for example (see `example/config.json`):

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

### End-to-end demo

An executable example is provided under `example/`:

```bash
# From the repo root
PYTHONPATH=src python -m logscope.app.cli example/config.json

# The command generates ./example/logs/demo_summary.json
cat example/logs/demo_summary.json | python -m json.tool
```

The sample rules aggregate two matching log lines into a single issue keyed by the regex rule, demonstrating multi-line issue collection and JSON output.

## Testing

```bash
PYTHONPATH=src python -m unittest discover
```
