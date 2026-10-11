"""VO-023, VO-029, VO-024: stopping early and resuming."""
import re
import shutil
from datetime import date
import unittest

from tests.behaviour.test_setting import setup
from tests.support import project as proj
from tests.support.agent import Session, outcome_block, drive_standalone

ANSWER = "Option A, the recommended one."
LABEL = re.compile(
    r"^\*\*Grilled on\*\*: \d{4}-\d{2}-\d{2} \(stopped early, (\d+) points? open\)$", re.M)


def clarification_lines(text):
    return [l for l in text.splitlines() if l.startswith("- Q:")]


class StopAfterTwoAnswers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project, cls.feature = setup('grill: "on"')
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        cls.session = Session(cls.project)
        cls.session.say("/speckit-grill-specify-auto")
        cls.session.say(ANSWER)
        cls.session.say(ANSWER)
        cls.stop_reply = cls.session.say("stop")

    def test_both_answers_stay_and_the_label_shows_open_points(self):
        text = (self.feature / "spec.md").read_text()
        self.assertEqual(len(clarification_lines(text)), 2)
        self.assertIsNotNone(LABEL.search(text), text[:600])
        self.assertEqual(len(LABEL.findall(text)), 1)

    def test_outcome_is_stopped_early_with_outstanding_points_and_resume(self):
        block = outcome_block(self.stop_reply)
        self.assertIsNotNone(block, self.stop_reply)
        self.assertEqual(block.splitlines()[0].strip(), "GRILL OUTCOME: stopped early")
        for field in ("Outstanding points", "Resume with", "Questions answered"):
            self.assertRegex(block, r"(?m)^%s:" % re.escape(field))


class StopBeforeFirstAnswer(unittest.TestCase):
    def check(self, setting):
        project, feature = setup(setting)
        self.addCleanup(shutil.rmtree, project.parent, True)
        before = proj.snapshot(project)
        session = Session(project)
        session.say("/speckit-grill-specify-auto")
        reply = session.say("stop")
        block = outcome_block(reply)
        self.assertIsNotNone(block, reply)
        self.assertEqual(block.splitlines()[0].strip(), "GRILL OUTCOME: stopped early")
        self.assertRegex(block, r"(?m)^Label: none$")
        self.assertRegex(block, r"(?m)^Questions answered: 0$")
        self.assertEqual(proj.snapshot(project), before)

    def test_strict(self):
        self.check('grill: "strict"')

    def test_on_where_skip_is_offered_and_not_taken(self):
        self.check('grill: "on"')


class ResumeStandalone(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project, cls.feature = setup('grill: "on"')
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        cls.session = Session(cls.project)
        cls.session.say("/speckit-grill-specify-auto")
        cls.session.say(ANSWER)
        cls.session.say(ANSWER)
        cls.session.say("stop")
        cls.before_lines = clarification_lines((cls.feature / "spec.md").read_text())
        cls.replies, cls.final = drive_standalone(cls.session, "/speckit-grill-specify-with-docs")

    def test_no_recorded_question_is_asked_again_and_label_becomes_plain(self):
        self.assertIsNotNone(self.final, "the resumed grill did not reach its end")
        text = (self.feature / "spec.md").read_text()
        after = clarification_lines(text)
        self.assertEqual(after[:len(self.before_lines)], self.before_lines)
        questions = [l.split("→")[0] for l in after]
        self.assertEqual(len(questions), len(set(questions)), "a question was recorded twice")
        self.assertIn("**Grilled on**: %s\n" % date.today().isoformat(), text)
        self.assertNotIn("stopped early", text)
        self.assertEqual(text.count("**Grilled on**:"), 1)


if __name__ == "__main__":
    unittest.main()
