"""VO-018, VO-031: a nested interview answered to the end completes cleanly."""
import re
import shutil
import unittest
from datetime import date
from pathlib import Path

from tests.support import project as proj
from tests.support.agent import Session, drive_to_end


class Completion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, proj.REPO)
        cls.feature = proj.install_feature(cls.project, "ambiguous")
        cls.session = Session(cls.project)
        cls.replies, cls.block = drive_to_end(cls.session, "/speckit-grill-specify-auto")

    def test_completed_outcome_label_and_checklist(self):
        self.assertIsNotNone(self.block, "no outcome block was printed")
        self.assertEqual(self.block.splitlines()[0].strip(), "GRILL OUTCOME: completed")
        for field in ("Coverage", "Knowledge docs changed", "Checklist"):
            self.assertRegex(self.block, r"(?m)^%s:" % re.escape(field))
        text = (self.feature / "spec.md").read_text()
        self.assertIn("**Grilled on**: %s\n" % date.today().isoformat(), text)
        self.assertNotIn("stopped early", text)
        self.assertTrue((self.feature / "checklists" / "requirements.md").is_file())


TERM = ("Option A. Settled for the whole company: the buyer is always called a 'Shopper', "
        "never 'customer' or 'user', in all our products.")
DECISION = ("Option A. Company-wide architecture decision, costly to reverse: carts live "
            "server-side in our PostgreSQL database; we rejected browser storage and Redis "
            "because carts must be auditable. Record this as a decision.")


class WriteBoundary(unittest.TestCase):
    """VO-031: only the spec, checklist checkboxes and knowledge docs change."""

    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, proj.REPO)
        cls.feature = proj.install_feature(cls.project, "ambiguous")
        cls.checklist_before = (cls.feature / "checklists" / "requirements.md").read_text()
        cls.before = proj.snapshot(cls.project)
        cls.session = Session(cls.project)
        cls.session.say("/speckit-grill-specify-auto")
        cls.session.say(TERM)
        cls.session.say(DECISION)
        cls.replies, cls.block = drive_to_end(cls.session, "Option A, the recommended one.")

    def test_only_permitted_paths_change(self):
        self.assertIsNotNone(self.block, "the run did not complete")
        changed = proj.changed_paths(self.before, proj.snapshot(self.project))
        allowed = ("specs/001-demo/spec.md", "specs/001-demo/checklists/requirements.md")
        stray = [p for p in changed
                 if p not in allowed and not p.startswith("docs/domain_knowledge/")]
        self.assertEqual(stray, [])
        self.assertIn("specs/001-demo/spec.md", changed)
        setting = ".specify/extensions/grill-specify/grill-specify-config.yml"
        self.assertNotIn(setting, changed)

    def test_checklist_differs_only_in_checkbox_markers(self):
        after = (self.feature / "checklists" / "requirements.md").read_text()
        norm = lambda t: re.sub(r"- \[[ xX]\]", "- [ ]", t)
        self.assertEqual(norm(after), norm(self.checklist_before))


if __name__ == "__main__":
    unittest.main()
