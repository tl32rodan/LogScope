# LogScope

LogScope is a log-driven rule engine that scans log files, applies owner-defined regular expressions, and builds a summary table of rules that matched.
Each rule captures the log files where it appeared, alongside the first matching message as an example, and is exported as JSON for easy downstream integration.

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

The sample rules aggregate matching lines into a single rule entry keyed by the regex, summarizing affected log files and the first observed message for lightweight reporting.

Example JSON summary output:

```json
{
  "rules": [
    {
      "rule_pattern": "ERROR",
      "owner": "team-a",
      "action": "investigate",
      "category": "runtime",
      "description": "Runtime error",
      "log_files": ["example/logs/demo.log"],
      "sample_message": "[ERROR] database unavailable",
      "count": 2
    }
  ]
}
```

Sample logs for the demo live at `example/logs/demo.log` and include two matching `ERROR` entries along with surrounding context to exercise the rule in `example/rules.csv`.

## Makefile shortcuts

Common tasks are available via `make`:

```bash
make run   # Execute the demo pipeline defined in example/config.json using the repository's Python
make test  # Run the full unittest suite
```

Sample logs for the demo live at `example/logs/demo.log` and include two matching `ERROR` entries along with surrounding context to exercise the rule in `example/rules.csv`.

## Makefile shortcuts

Common tasks are available via `make`:

```bash
make run   # Execute the demo pipeline defined in example/config.json using the repository's Python
make test  # Run the full unittest suite
```

## Testing

```bash
PYTHONPATH=src python -m unittest discover
```
