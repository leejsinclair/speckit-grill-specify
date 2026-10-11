"""VO-016: each answer is saved before the next question appears, with a stopped-early label."""
import re
import shutil
import unittest
from pathlib import Path

from tests.support import project as proj
from tests.support.agent import Session, outcome_block

LABEL = re.compile(
    r"^\*\*Grilled on\*\*: \d{4}-\d{2}-\d{2} \(stopped early, (\d+) points? open\)$", re.M)
ANSWER = "Option A, the recommended one."


def clarification_lines(text):
    return [l for l in text.splitlines() if l.startswith("- Q:")]


class InterviewSaves(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, proj.REPO)
        cls.feature = proj.install_feature(cls.project, "ambiguous")
        cls.session = Session(cls.project)
        cls.opening = cls.session.say("/speckit-grill-specify-auto")

    def test_each_answer_is_saved_before_the_next_question(self):
        spec = self.feature / "spec.md"
        self.assertEqual(clarification_lines(spec.read_text()), [], "nothing before the first answer")
        for n in (1, 2, 3):
            reply = self.session.say(ANSWER)
            self.assertIsNone(outcome_block(reply), "the interview must still be running")
            text = spec.read_text()
            self.assertEqual(len(clarification_lines(text)), n, "after answer %d" % n)
            self.assertIn("## Clarifications", text)
            match = LABEL.search(text)
            self.assertIsNotNone(match, "stopped-early label missing after answer %d" % n)
            self.assertEqual(len(LABEL.findall(text)), 1)


if __name__ == "__main__":
    unittest.main()
