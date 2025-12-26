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
- `src/logscope/integrations`: External adapters (e.g., filesystem-backed issue stores).
- `tests`: Unit tests for each module.

## Quickstart

1. Create a CSV rules file (headers: `pattern,owner,action,description,category`) and place your log files under a root directory.
2. Define a JSON config map describing the log roots and configs to process, for example (see `example/config.json`):

```json
[
  {
    "id": "core",
    "config": "./rules.csv",
    "log_root": "./logs",
    "patterns": ["**/*.log"]
  }
]
```

3. Run the pipeline via CLI:

```bash
PYTHONPATH=src python -m logscope analysis config.json ./issues
```

### End-to-end demo

An executable example is provided under `example/`:

```bash
# From the repo root
# Defaults to running the analysis subcommand with example inputs
make run

# Override the config or the issue store root if needed
make run RUN_ARGS="analysis example/config.json ./example/output"

# The command generates ./example/issues/demo/issues.json
cat example/issues/demo/issues.json | python -m json.tool
```

The sample rules aggregate matching lines into a single rule entry keyed by the regex, summarizing affected log files and the first observed message for lightweight reporting.

Example JSON summary output:

```json
{
  "rules": [
    {
      "rule_pattern": "ERROR (?P<code>\\w+)",
      "owner": "platform",
      "action": "investigate",
      "category": "runtime",
      "description": "Capture error code from logs",
      "log_files": [
        "example/logs/demo.log",
        "example/logs/demo2.log"
      ],
      "sample_message": "2024-05-10 10:00:01,150 ERROR ZX81 Failed to connect to database",
      "count": 4
    }
  ]
}
```

Sample logs for the demo live at `example/logs/demo.log` and `example/logs/demo2.log`, illustrating how multiple files contributing similar `ERROR` entries are aggregated into a single rule driven by `example/rules.csv`.

## Makefile shortcuts

Common tasks are available via `make`:

```bash
make run   # Execute the pipeline with RUN_ARGS (defaults to example/config.json)
make test  # Run the full unittest suite
```

## Testing

```bash
PYTHONPATH=src python -m unittest discover
```
