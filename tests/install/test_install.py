"""VO-011: install and reinstall of the extension in a fresh Spec Kit project."""
import json
import shutil
import subprocess
import unittest
from pathlib import Path

import yaml

from tests.support import project as proj

REPO = proj.REPO
EXT_DIR = ".specify/extensions/grill-specify"


def declared_files(manifest):
    provides = manifest.get("provides", {})
    for kind in ("commands", "scripts"):
        for item in provides.get(kind, []):
            yield item["file"]
    for item in provides.get("config", []):
        yield item["template"]


class Install(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)

    def test_every_declared_file_exists_in_the_package(self):
        manifest = yaml.safe_load((REPO / "extension.yml").read_text())
        missing = [f for f in declared_files(manifest) if not (REPO / f).is_file()]
        self.assertEqual(missing, [])

    def test_install_creates_the_setting_file_and_reinstall_keeps_one_hook(self):
        proj.add_extension(self.project, REPO)
        config = self.project / EXT_DIR / "grill-specify-config.yml"
        self.assertTrue(config.is_file(), "setting file missing after install")

        script = self.project / EXT_DIR / "scripts" / "bash" / "grill-context.sh"
        out = subprocess.run(["bash", str(script), "--json"], cwd=self.project,
                             capture_output=True, text=True,
                             env={"PATH": "/usr/bin:/bin", "HOME": "/nonexistent"})
        self.assertEqual(json.loads(out.stdout)["setting"], "on")

        proj.add_extension(self.project, REPO, force=True)
        hooks = proj.read_extensions_yml(self.project)["hooks"]["after_specify"]
        ours = [h for h in hooks if h.get("extension") == "grill-specify"]
        self.assertEqual(len(ours), 1)


if __name__ == "__main__":
    unittest.main()
