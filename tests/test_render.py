import json
import unittest

from git_commit_fortune.analyzer import analyze, generate_fortune
from git_commit_fortune.models import Commit
from git_commit_fortune.render import render_json, render_one_line, render_text


def _fortune():
    commits = [
        Commit("a", 1_704_024_000, "Alice", "fix login bug"),
        Commit("b", 1_704_096_000, "Bob", "temporary hotfix"),
    ]
    return generate_fortune(analyze(commits))


class RenderTest(unittest.TestCase):
    def test_render_text_includes_repository_and_sections(self):
        fortune = _fortune()

        output = render_text(fortune, "/work/demo")

        self.assertIn("Git Commit Fortune", output)
        self.assertIn("Repository: /work/demo", output)
        self.assertIn(f"Omen: {fortune.omen}", output)
        self.assertIn("Signs:", output)
        self.assertIn(fortune.prediction, output)

    def test_render_one_line_is_compact(self):
        fortune = _fortune()

        output = render_one_line(fortune)

        self.assertNotIn("\n", output)
        self.assertIn(fortune.omen, output)
        self.assertIn(fortune.spirit_animal, output)

    def test_render_json_is_valid_and_complete(self):
        fortune = _fortune()

        payload = json.loads(render_json(fortune, "/work/demo"))

        self.assertEqual("/work/demo", payload["repository"])
        self.assertEqual(fortune.omen, payload["fortune"]["omen"])
        self.assertEqual(fortune.stats.total, payload["stats"]["total"])


if __name__ == "__main__":
    unittest.main()
