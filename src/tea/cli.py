from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .loader import load_tasks
from .planner import sequence_tasks, write_plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tea", description="Temporal Executive Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="Generate a simple plan from tasks")
    plan_parser.add_argument("--tasks", required=True, type=Path, help="Path to tasks.json")
    plan_parser.add_argument("--out", default=Path("out"), type=Path, help="Output directory (default: out)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "plan":
        tasks = load_tasks(args.tasks)
        ordered = sequence_tasks(tasks)
        state_path, plan_path = write_plan(ordered, args.out)
        print(f"State written to {state_path}")
        print(f"Plan written to {plan_path}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
