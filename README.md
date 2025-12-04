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

## Design analysis (responsibility & SOLID alignment)

- **Single responsibility & clear boundaries**: Each package owns one concern—`config` only loads/validates rule definitions, `collector` only finds/streams log lines, `matcher` only applies rules and filtering, `reporter` only shapes results for export, and `integrations` isolates external systems (e.g., Cassandra). Domain models in `model` stay data-only and avoid IO.
- **Open/closed for extensions**: Rule loading, storage backends, and filters are pluggable. For example, adding a YAML loader, new filters, or a different persistence layer does not change the matcher or reporter code paths.
- **Dependency direction**: Application code (`app`) orchestrates the lower layers without inverting dependencies; lower layers avoid depending on application wiring. External adapters live behind interfaces to keep the core pipeline testable.
- **TDD support**: Every module has dedicated unit tests under `tests/`, and the pipeline is exercised end-to-end through the CLI tests to protect integration behavior.

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
