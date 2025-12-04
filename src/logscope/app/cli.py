import argparse
import json
from pathlib import Path

from logscope.app.runner import ConfigBundle, run_application
from logscope.integrations.cassandra_client import (
    CassandraIssueStore,
    CassandraUnavailable,
    InMemoryIssueStore,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="LogScope pipeline runner")
    parser.add_argument(
        "config_map",
        type=Path,
        help="JSON file describing configs (list of {name, config, log_root, patterns})",
    )
    parser.add_argument(
        "--cassandra-hosts",
        type=str,
        default=None,
        help="Comma-separated Cassandra hosts. If omitted, an in-memory store is used.",
    )
    parser.add_argument("--cassandra-keyspace", type=str, default="logscope")
    parser.add_argument("--cassandra-table", type=str, default="issues")
    return parser


def load_bundles(config_map_path: Path):
    data = json.loads(config_map_path.read_text())
    bundles = []
    for entry in data:
        patterns = entry.get("patterns") or ["**/*.log"]
        bundles.append(
            ConfigBundle(
                name=entry["name"],
                config_path=Path(entry["config"]),
                log_root=Path(entry["log_root"]),
                patterns=patterns,
            )
        )
    return bundles


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    bundles = load_bundles(args.config_map)

    if args.cassandra_hosts:
        hosts = [host.strip() for host in args.cassandra_hosts.split(",") if host.strip()]
        try:
            store = CassandraIssueStore(hosts, args.cassandra_keyspace, args.cassandra_table)
        except CassandraUnavailable as exc:
            parser.error(str(exc))
    else:
        store = InMemoryIssueStore()

    summaries = run_application(bundles, store)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
