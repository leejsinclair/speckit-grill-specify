"""VO-030: a spec with nothing left to settle goes straight to the satisfaction question."""
import re
import shutil
import unittest
from datetime import date

from tests.support import project as proj
from tests.support.agent import Session, drive_to_end

LABEL_LINE = re.compile(r"^\*\*Grilled on\*\*: .*$", re.M)


class NothingToSettle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, proj.REPO)
        cls.feature = proj.install_feature(cls.project, "settled")
        cls.session = Session(cls.project)
        cls.replies, cls.block = drive_to_end(cls.session, "/speckit-grill-specify-auto",
                                              max_turns=4)

    def test_only_the_satisfaction_question_is_asked_and_run_completes(self):
        self.assertIsNotNone(self.block, "no outcome block was printed")
        self.assertEqual(self.block.splitlines()[0].strip(), "GRILL OUTCOME: completed")
        self.assertRegex(self.block, r"(?m)^Questions answered: 0$")
        text = (self.feature / "spec.md").read_text()
        self.assertNotIn("## Clarifications", text)
        self.assertIn("**Grilled on**: %s\n" % date.today().isoformat(), text)

    def test_the_skip_choice_is_offered_at_that_opening(self):
        self.assertRegex(self.replies[0], r"(?i)skip")

    def test_standalone_run_afterwards_changes_only_the_label(self):
        spec = self.feature / "spec.md"
        before = spec.read_text()
        reply = self.session.say("/speckit-grill-specify-with-docs")
        if "Finish and proceed" in reply:
            self.session.say("Finish and proceed")
        after = spec.read_text()
        self.assertEqual(LABEL_LINE.sub("<label>", after), LABEL_LINE.sub("<label>", before))
        self.assertEqual(len(LABEL_LINE.findall(after)), 1)


if __name__ == "__main__":
    unittest.main()
