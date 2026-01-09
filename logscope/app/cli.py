import argparse
import json
from pathlib import Path

from logscope.app.runner import ConfigBundle, run_application
from logscope.integrations.issue_store import JsonIssueStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="LogScope pipeline runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analysis = subparsers.add_parser(
        "analysis", help="Run analysis for a config map and persist issues as JSON"
    )
    analysis.add_argument(
        "config_map",
        type=Path,
        help="JSON file describing configs (list of {id, config, patterns}); patterns must be absolute",
    )
    analysis.add_argument(
        "issue_store_root",
        type=Path,
        help="Filesystem root where issues are stored by configuration id",
    )
    return parser


def load_bundles(config_map_path: Path):
    data = json.loads(config_map_path.read_text())
    bundles = []
    for entry in data:
        patterns = entry.get("patterns") or ["**/*.log"]
        for pattern in patterns:
            if not Path(pattern).is_absolute():
                raise ValueError(f"Pattern must be an absolute path: {pattern}")
        bundles.append(
            ConfigBundle(
                config_id=entry["id"],
                config_path=Path(entry["config"]),
                patterns=patterns,
            )
        )
    return bundles


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "analysis":
        bundles = load_bundles(args.config_map)
        store = JsonIssueStore(args.issue_store_root)
        run_application(bundles, store)
        return 0

    parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
