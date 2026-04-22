from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from git_commit_fortune.git_reader import read_commits


class GitReaderTest(unittest.TestCase):
    def test_read_commits_passes_since_to_git(self):
        completed = Mock()
        completed.returncode = 0
        completed.stdout = ""
        completed.stderr = ""

        with patch("git_commit_fortune.git_reader.subprocess.run", return_value=completed) as run:
            commits = read_commits(Path("/repo"), 10, "2 weeks ago")

        self.assertEqual([], commits)
        command = run.call_args.args[0]
        self.assertIn("--since=2 weeks ago", command)


if __name__ == "__main__":
    unittest.main()
