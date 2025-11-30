import argparse
from pathlib import Path

from logscope.app.runner import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="LogScope pipeline runner")
    parser.add_argument("log_root", type=Path, help="Root directory containing logs")
    parser.add_argument("config", type=Path, help="CSV file containing rules")
    parser.add_argument("output", type=Path, help="Output CSV path for summary table")
    parser.add_argument(
        "--pattern",
        action="append",
        dest="patterns",
        default=None,
        help="Glob pattern for log files (can be provided multiple times). Default: **/*.log",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    patterns = args.patterns if args.patterns is not None else ["**/*.log"]
    run_pipeline(args.log_root, args.config, args.output, patterns)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
