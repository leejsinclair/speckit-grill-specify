"""VO-013: the upstream grill extension and this one install side by side."""
import hashlib
import shutil
import unittest
from pathlib import Path

from tests.support import project as proj

UPSTREAM = proj.FIXTURES / "upstream-grill"
UPSTREAM_SKILLS = ("speckit-grill-me", "speckit-grill-with-docs")
OURS = ("speckit-grill-specify-auto", "speckit-grill-specify-with-docs")


def digest(project, skill):
    return hashlib.sha256(
        (Path(project) / ".claude" / "skills" / skill / "SKILL.md").read_bytes()).hexdigest()


class Coexist(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        alone = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, alone.parent, True)
        proj.add_extension(alone, UPSTREAM)
        cls.alone = {s: digest(alone, s) for s in UPSTREAM_SKILLS}

    def install(self, first, second):
        project = proj.new_project()
        self.addCleanup(shutil.rmtree, project.parent, True)
        proj.add_extension(project, first)
        proj.add_extension(project, second)
        return project

    def check(self, project):
        skills = proj.list_skills(project)
        for name in UPSTREAM_SKILLS + OURS:
            self.assertIn(name, skills)
        for name in UPSTREAM_SKILLS:
            self.assertEqual(digest(project, name), self.alone[name], name)

    def test_upstream_first(self):
        self.check(self.install(UPSTREAM, proj.REPO))

    def test_this_extension_first(self):
        self.check(self.install(proj.REPO, UPSTREAM))


if __name__ == "__main__":
    unittest.main()
