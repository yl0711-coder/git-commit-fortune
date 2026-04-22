import contextlib
from io import StringIO
import unittest

from git_commit_fortune.cli import main


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


if __name__ == "__main__":
    unittest.main()
