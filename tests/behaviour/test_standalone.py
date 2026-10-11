"""VO-025, VO-027: the standalone grill ignores the setting and processes clarify hooks."""
import shutil
import unittest

from tests.behaviour.test_setting import setup
from tests.support import project as proj
from tests.behaviour.test_nested_hooks import MARKERS, marker_lines
from tests.support.agent import Session, outcome_block, drive_standalone


class StandaloneIgnoresSetting(unittest.TestCase):
    def check(self, setting):
        project, feature = setup(setting)
        self.addCleanup(shutil.rmtree, project.parent, True)
        session = Session(project)
        opening = session.say("/speckit-grill-specify-with-docs")
        self.assertRegex(opening, r"(?i)\b\d+\b[^\n]{0,60}\b(point|question|decision)")
        self.assertIn("?", opening)
        self.assertIsNone(outcome_block(opening), "a standalone run prints no outcome block")
        # Wording-independent: asking to skip must not end the interview as skipped.
        after = session.say("skip")
        block = outcome_block(after)
        self.assertTrue(block is None or "skipped" not in block.splitlines()[0], after)

    def test_setting_off(self):
        self.check('grill: "off"')

    def test_setting_on(self):
        self.check('grill: "on"')


class StandaloneClarifyHooks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project, cls.feature = setup('grill: "on"')
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, MARKERS)
        session = Session(cls.project)
        session.say("/speckit-grill-specify-with-docs")
        cls.during = marker_lines(cls.project)
        cls.replies, cls.final = drive_standalone(session, "Option A, the recommended one.")
        cls.after = marker_lines(cls.project)

    def test_before_clarify_ran_before_the_first_question(self):
        self.assertEqual(self.during, ["before-clarify"])

    def test_after_clarify_ran_before_the_completion_report(self):
        self.assertIsNotNone(self.final)
        self.assertEqual(self.after, ["before-clarify", "after-clarify"])


if __name__ == "__main__":
    unittest.main()
