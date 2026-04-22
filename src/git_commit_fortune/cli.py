"""Command-line interface for git-commit-fortune."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .analyzer import analyze, generate_fortune
from .git_reader import GitError, read_commits
from .render import render_json, render_text


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""

    parser = argparse.ArgumentParser(
        prog="git-commit-fortune",
        description="Read Git history and generate a playful repository fortune.",
    )
    parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="path to the Git repository, defaults to current directory",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=80,
        help="number of recent commits to consult, defaults to 80",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print machine-readable JSON output",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.limit <= 0:
        print("error: --limit must be greater than 0", file=sys.stderr)
        return 2

    repository = Path(args.repository).expanduser().resolve()

    try:
        commits = read_commits(repository, args.limit)
    except GitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    stats = analyze(commits)
    fortune = generate_fortune(stats)

    if args.json:
        print(render_json(fortune, str(repository)))
    else:
        print(render_text(fortune, str(repository)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

