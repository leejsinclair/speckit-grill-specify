"""VO-014: install from the local directory and from the published tag archive agree."""
import shutil
import unittest

import yaml

from tests.support import project as proj

REPO_URL = "https://github.com/leejsinclair/speckit-grill-specify"


def version():
    return yaml.safe_load((proj.REPO / "extension.yml").read_text())["extension"]["version"]


def install_from_archive(project):
    url = "%s/archive/refs/tags/v%s.zip" % (REPO_URL, version())
    return proj.run([proj.SPECIFY, "extension", "add", "grill-specify", "--from", url],
                    cwd=project)


def summary(project):
    hooks = proj.read_extensions_yml(project).get("hooks", {}).get("after_specify", [])
    ours = [h for h in hooks if h.get("extension") == "grill-specify"]
    skills = sorted(s for s in proj.list_skills(project) if s.startswith("speckit-grill-specify"))
    ext = project / ".specify" / "extensions" / "grill-specify"
    return {
        "skills": skills,
        "hook_count": len(ours),
        "provenance": (ext / "upstream" / "UPSTREAM.md").is_file(),
        "licence": (ext / "upstream" / "LICENSE.upstream").is_file(),
    }


class ReleaseInstall(unittest.TestCase):
    def test_local_and_archive_installs_agree(self):
        local = proj.new_project()
        archive = proj.new_project()
        self.addCleanup(shutil.rmtree, local.parent, True)
        self.addCleanup(shutil.rmtree, archive.parent, True)
        proj.add_extension(local, proj.REPO)
        install_from_archive(archive)
        a, b = summary(local), summary(archive)
        self.assertEqual(a, b)
        self.assertEqual(a["hook_count"], 1)
        self.assertEqual(a["skills"], ["speckit-grill-specify-auto", "speckit-grill-specify-with-docs"])
        self.assertTrue(a["provenance"] and a["licence"])


if __name__ == "__main__":
    unittest.main()
