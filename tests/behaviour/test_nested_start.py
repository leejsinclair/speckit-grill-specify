"""VO-015: the grill starts by itself, in the same session, straight after specify."""
import re
import shutil
import unittest
from pathlib import Path

from tests.support import project as proj
from tests.support.agent import Session, outcome_block

DESCRIPTION = (
    "Add a shopping cart to a web shop. A shopper adds and removes products and sees a "
    "running total. Carts are kept for 30 days after last activity and hold up to 50 "
    "product lines. Discounts apply only through a promo code, one code per order. Payment "
    "is handled by an external provider; shipping and tax are out of scope."
)


def find_specs(project):
    return sorted(Path(project, "specs").glob("*/spec.md"))


class NestedStart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, proj.REPO)
        cls.session = Session(cls.project)
        cls.reply = cls.session.say("/speckit-specify " + DESCRIPTION)

    def test_specify_ends_at_the_grill_opening(self):
        # The grill has opened but not finished: no outcome block yet.
        self.assertIsNone(outcome_block(self.reply), self.reply)
        # The opening states a number of points and presents a question.
        self.assertRegex(self.reply, r"(?i)\b\d+\b[^\n]{0,60}\b(point|decision|ambigu|question)")
        self.assertIn("?", self.reply)
        # It did not ask for permission to start or for a second command.
        self.assertNotRegex(self.reply, r"(?i)(shall i|should i|would you like me to) (start|run|launch)")

    def test_nothing_is_written_before_the_first_answer(self):
        specs = find_specs(self.project)
        self.assertEqual(len(specs), 1, "specify must have written one spec")
        text = specs[0].read_text()
        self.assertNotIn("## Clarifications", text)
        self.assertNotIn("**Grilled on**", text)
        self.assertFalse((self.project / "docs" / "domain_knowledge").exists())


if __name__ == "__main__":
    unittest.main()
