"""VO-019: the skip choice leaves the project exactly as specify left it."""
import re
import shutil
import unittest

from tests.behaviour.test_setting import setup
from tests.support import project as proj
from tests.support.agent import Session, outcome_block


class Skip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project, cls.feature = setup(None)  # no `grill:` line: nothing chosen
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        cls.before = proj.snapshot(cls.project)
        session = Session(cls.project)
        cls.opening = session.say("/speckit-grill-specify-auto")
        cls.after_skip = session.say("skip")

    def test_opening_offers_a_skip_choice_and_no_warning(self):
        self.assertRegex(self.opening, r"(?i)\bskip\b")
        self.assertNotRegex(self.opening, r"(?i)\bwarning\b")
        self.assertIsNone(outcome_block(self.opening))

    def test_skipping_changes_nothing_and_reports_skipped(self):
        block = outcome_block(self.after_skip)
        self.assertIsNotNone(block, self.after_skip)
        self.assertEqual(block.splitlines()[0].strip(), "GRILL OUTCOME: skipped")
        for field in ("Reason", "Resume with"):
            self.assertRegex(block, r"(?m)^%s:" % re.escape(field))
        self.assertEqual(proj.snapshot(self.project), self.before)
        self.assertNotIn("**Grilled on**", (self.feature / "spec.md").read_text())


if __name__ == "__main__":
    unittest.main()
