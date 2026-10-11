"""VO-036 (EC-05): markers and failed checklist items left by specify do not stop the grill."""
import shutil
import unittest

from tests.support import project as proj
from tests.support.agent import Session, drive_to_end


class OpenMarkers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, proj.REPO)
        cls.feature = proj.install_feature(cls.project, "markers")
        cls.session = Session(cls.project)
        cls.replies, cls.block = drive_to_end(
            cls.session, "/speckit-grill-specify-auto",
            answer="Option A: every visitor, signed in or not, sees the banner.")

    def test_opens_with_a_question_and_does_not_stop_or_refuse(self):
        self.assertIn("?", self.replies[0])
        self.assertNotRegex(self.replies[0], r"(?i)(cannot|can't|unable to) (proceed|continue|run)")

    def test_marker_is_gone_and_answer_is_recorded(self):
        self.assertIsNotNone(self.block, "the run did not finish")
        text = (self.feature / "spec.md").read_text()
        self.assertNotIn("[NEEDS CLARIFICATION", text)
        self.assertIn("## Clarifications", text)
        self.assertIn("- Q:", text)


if __name__ == "__main__":
    unittest.main()
