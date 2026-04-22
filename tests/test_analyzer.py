import unittest

from git_commit_fortune.analyzer import analyze, generate_fortune
from git_commit_fortune.models import Commit


class AnalyzerTest(unittest.TestCase):
    def test_analyze_counts_keywords_and_time_patterns(self):
        commits = [
            Commit("a", 1_704_024_000, "Alice", "fix login bug"),
            Commit("b", 1_704_096_000, "Bob", "temporary hotfix"),
            Commit("c", 1_704_182_400, "Alice", "final release"),
        ]

        stats = analyze(commits)

        self.assertEqual(3, stats.total)
        self.assertEqual(2, stats.authors)
        self.assertEqual(2, stats.keyword_counts["fix"])
        self.assertEqual(1, stats.keyword_counts["bug"])
        self.assertEqual(1, stats.keyword_counts["temporary"])
        self.assertEqual(1, stats.keyword_counts["hotfix"])
        self.assertEqual(1, stats.keyword_counts["final"])

    def test_generate_fortune_for_empty_history(self):
        stats = analyze([])

        fortune = generate_fortune(stats)

        self.assertEqual("silent but suspicious", fortune.mood)
        self.assertEqual("uncommitted timeline", fortune.omen)
        self.assertEqual("unreadable", fortune.fortune_level)
        self.assertEqual(["no commits were found"], fortune.signs)

    def test_generate_fortune_prefers_chaos_when_wip_is_common(self):
        commits = [
            Commit("a", 1_704_024_000, "Alice", "wip auth"),
            Commit("b", 1_704_096_000, "Alice", "temporary state"),
            Commit("c", 1_704_182_400, "Alice", "hack parser"),
            Commit("d", 1_704_268_800, "Alice", "docs"),
        ]

        fortune = generate_fortune(analyze(commits))

        self.assertIn("temporary", fortune.prediction)
        self.assertIn("raccoon", fortune.spirit_animal)
        self.assertEqual("The Temporary Permanent", fortune.omen)
        self.assertEqual("cursed but deployable", fortune.fortune_level)
        self.assertIn("git grep", fortune.lucky_command)

    def test_generate_fortune_detects_repeated_final_commits(self):
        commits = [
            Commit("a", 1_704_024_000, "Alice", "final docs"),
            Commit("b", 1_704_096_000, "Alice", "final release"),
            Commit("c", 1_704_182_400, "Alice", "update readme"),
        ]

        fortune = generate_fortune(analyze(commits))

        self.assertEqual("The Final That Was Not Final", fortune.omen)
        self.assertEqual("cursed but deployable", fortune.fortune_level)
        self.assertIn("final final", fortune.prediction)


if __name__ == "__main__":
    unittest.main()
