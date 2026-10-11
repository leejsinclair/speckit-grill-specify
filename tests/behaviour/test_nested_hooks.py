"""VO-026: a nested grill processes no clarify hook and no specify hook of its own."""
import shutil
import unittest
from pathlib import Path

from tests.behaviour.test_nested_start import DESCRIPTION
from tests.support import project as proj
from tests.support.agent import Session

MARKERS = proj.FIXTURES / "marker-hooks"


def marker_lines(project):
    log = Path(project) / ".marker-log"
    return [l.strip() for l in log.read_text().splitlines() if l.strip()] if log.exists() else []


class NestedHooks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, proj.REPO)
        proj.add_extension(cls.project, MARKERS)
        session = Session(cls.project)
        session.say("/speckit-specify " + DESCRIPTION)
        cls.during = marker_lines(cls.project)
        session.say("stop")
        cls.after = marker_lines(cls.project)

    def test_marker_after_specify_hook_runs_once_and_only_after_the_grill_ends(self):
        self.assertEqual(self.during, [], "a specify hook ran before the grill ended")
        self.assertEqual(self.after, ["after-specify"])


if __name__ == "__main__":
    unittest.main()
