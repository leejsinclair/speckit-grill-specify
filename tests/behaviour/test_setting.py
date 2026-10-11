"""VO-020, VO-021, VO-022: the grill setting decides the start and the skip choice."""
import re
import shutil
import unittest
from pathlib import Path

from tests.support import project as proj
from tests.support.agent import Session, outcome_block, outcome_first_line

CONFIG = Path(".specify/extensions/grill-specify/grill-specify-config.yml")


def setup(setting_line):
    """A fresh project with the ambiguous spec; the grill line is replaced, or removed if None."""
    project = proj.new_project()
    proj.add_extension(project, proj.REPO)
    feature = proj.install_feature(project, "ambiguous")
    config = project / CONFIG
    lines = [l for l in config.read_text().splitlines() if not l.startswith("grill:")]
    if setting_line is not None:
        lines.append(setting_line)
    config.write_text("\n".join(lines) + "\n")
    return project, feature


class Strict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project, cls.feature = setup('grill: "strict"')
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        session = Session(cls.project)
        cls.reply = session.say("/speckit-grill-specify-auto")
        cls.after_skip = session.say("skip")

    def test_opens_with_points_and_a_question(self):
        self.assertRegex(self.reply, r"(?i)\b\d+\b[^\n]{0,60}\b(point|question|decision)")
        self.assertIn("?", self.reply)

    def test_no_skip_choice_exists(self):
        # Wording-independent: asking to skip must not end the run as skipped.
        self.assertNotEqual(outcome_first_line(self.after_skip), "GRILL OUTCOME: skipped")


class Off(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project, cls.feature = setup('grill: "off"')
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        cls.before = proj.snapshot(cls.project)
        cls.reply = Session(cls.project).say("/speckit-grill-specify-auto")

    def test_nothing_is_asked_and_nothing_changes(self):
        self.assertEqual(outcome_first_line(self.reply), "GRILL OUTCOME: switched off")
        self.assertNotIn("?", outcome_block(self.reply))
        self.assertEqual(proj.snapshot(self.project), self.before)


class UnknownValue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project, cls.feature = setup('grill: "of"')
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        session = Session(cls.project)
        cls.opening = session.say("/speckit-grill-specify-auto")
        cls.after_skip = session.say("skip")

    def test_falls_back_to_on_and_reports_the_bad_value(self):
        block = outcome_block(self.after_skip)
        self.assertIsNotNone(block, self.after_skip)
        self.assertEqual(block.splitlines()[0].strip(), "GRILL OUTCOME: skipped")
        warnings = [l for l in block.splitlines() if l.startswith("Warning:")]
        self.assertEqual(len(warnings), 1, block)
        self.assertIn("of", warnings[0])


if __name__ == "__main__":
    unittest.main()
