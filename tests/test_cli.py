import contextlib
from io import StringIO
import unittest
from unittest.mock import patch

from git_commit_fortune.cli import main
from git_commit_fortune.models import Commit


class CliTest(unittest.TestCase):
    def test_cli_rejects_invalid_limit(self):
        stderr = StringIO()

        with contextlib.redirect_stderr(stderr):
            exit_code = main(["--limit", "0"])

        self.assertEqual(2, exit_code)
        self.assertIn("--limit must be greater than 0", stderr.getvalue())

    def test_json_and_one_line_are_rejected_together(self):
        stderr = StringIO()

        with contextlib.redirect_stderr(stderr):
            exit_code = main(["--json", "--one-line"])

        self.assertEqual(2, exit_code)
        self.assertIn("--json cannot be used with --one-line", stderr.getvalue())

    def test_strict_mode_returns_failure_for_high_risk_history(self):
        commits = [
            Commit("a", 1_704_024_000, "Alice", "wip auth"),
            Commit("b", 1_704_096_000, "Alice", "temporary state"),
            Commit("c", 1_704_182_400, "Alice", "hack parser"),
            Commit("d", 1_704_268_800, "Alice", "docs"),
        ]
        stderr = StringIO()

        with patch("git_commit_fortune.cli.read_commits", return_value=commits):
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(StringIO()):
                exit_code = main(["--strict"])

        self.assertEqual(1, exit_code)
        self.assertIn("strict:", stderr.getvalue())

    def test_strict_mode_allows_low_risk_history(self):
        commits = [
            Commit("a", 1_704_024_000, "Alice", "add repository reader"),
            Commit("b", 1_704_096_000, "Alice", "document command output"),
            Commit("c", 1_704_182_400, "Alice", "refactor formatter module"),
        ]

        with patch("git_commit_fortune.cli.read_commits", return_value=commits):
            with contextlib.redirect_stderr(StringIO()), contextlib.redirect_stdout(StringIO()):
                exit_code = main(["--strict"])

        self.assertEqual(0, exit_code)


if __name__ == "__main__":
    unittest.main()
