"""VO-034 (FR-019, DC): nothing at user level, no subagent, and both grills open without it."""
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.support import project as proj
from tests.support.agent import Session

REPO = proj.REPO
CREDENTIALS = Path.home() / ".claude" / ".credentials.json"


def command_text():
    return "\n".join(p.read_text() for p in sorted((REPO / "commands").glob("*.md")))


class PackageIsProjectLevelOnly(unittest.TestCase):
    def test_command_text_names_no_user_level_skill_agent_or_subagent_delegation(self):
        text = command_text()
        self.assertNotRegex(text, r"~/\.claude|\$HOME/\.claude|user-level skill|user-level agent")
        # Upstream's own sentence forbidding delegation is allowed; no instruction to delegate.
        self.assertNotRegex(text, r"(?i)\b(launch|spawn|start|use|invoke|delegate to)\b[^.\n]{0,40}\bsub-?agents?\b(?![^.\n]{0,40}\b(not|never)\b)")

    def test_install_writes_only_inside_the_project(self):
        project = proj.new_project()
        self.addCleanup(shutil.rmtree, project.parent, True)
        before = proj.snapshot(project.parent, ignore=("project",))
        home_marker = Path.home() / ".claude" / "skills"
        home_before = sorted(p.name for p in home_marker.iterdir()) if home_marker.is_dir() else []
        proj.add_extension(project, REPO)
        self.assertEqual(proj.snapshot(project.parent, ignore=("project",)), before)
        home_after = sorted(p.name for p in home_marker.iterdir()) if home_marker.is_dir() else []
        self.assertEqual(home_after, home_before)


@unittest.skipUnless(CREDENTIALS.exists(), "no credentials file to build an empty config dir")
class OpensWithEmptyUserConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = Path(tempfile.mkdtemp(prefix="grill-config-"))
        cls.addClassCleanup(shutil.rmtree, cls.config, True)
        shutil.copy(CREDENTIALS, cls.config / ".credentials.json")
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, REPO)
        proj.install_feature(cls.project, "ambiguous")

    def opening(self, command):
        session = Session(self.project, config_dir=self.config)
        return session.say(command)

    def test_nested_grill_opens(self):
        self.assertRegex(self.opening("/speckit-grill-specify-auto"),
                         r"(?i)\b\d+\b[^\n]{0,60}\b(point|question|decision)")

    def test_standalone_grill_opens(self):
        self.assertRegex(self.opening("/speckit-grill-specify-with-docs"),
                         r"(?i)\b\d+\b[^\n]{0,60}\b(point|question|decision)")


if __name__ == "__main__":
    unittest.main()
