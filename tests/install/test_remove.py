"""VO-012: removing the extension leaves other extensions and produced documents alone."""
import shutil
import unittest

from tests.support import project as proj

MARKERS = proj.FIXTURES / "marker-hooks"
SPEC = ("# Feature\n\n**Status**: Draft\n\n**Grilled on**: 2026-10-11\n\n"
        "## Clarifications\n\n### Session 2026-10-11\n\n- Q: A? → A: B\n")


def hook_entries(project):
    hooks = proj.read_extensions_yml(project).get("hooks", {})
    return {event: [h for h in entries] for event, entries in hooks.items()}


class Remove(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, proj.REPO)
        proj.add_extension(cls.project, MARKERS)
        feature = cls.project / "specs" / "001-demo"
        feature.mkdir(parents=True)
        (feature / "spec.md").write_text(SPEC)
        knowledge = cls.project / "docs" / "domain_knowledge"
        knowledge.mkdir(parents=True)
        (knowledge / "CONTEXT.md").write_text("# Context\n\n- **Shopper**: the buyer\n")
        cls.docs_before = proj.snapshot(cls.project / "specs"), proj.snapshot(
            cls.project / "docs")
        cls.markers_before = [
            h for hs in hook_entries(cls.project).values() for h in hs
            if h.get("extension") == "marker-hooks"]
        cls.result = proj.remove_extension(cls.project, "grill-specify")

    def test_removal_succeeds_and_leaves_no_registration_or_command(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr + self.result.stdout)
        grill = [h for hs in hook_entries(self.project).values() for h in hs
                 if h.get("extension") == "grill-specify"]
        self.assertEqual(grill, [])
        self.assertEqual([s for s in proj.list_skills(self.project)
                          if s.startswith("speckit-grill-specify")], [])

    def test_other_extension_and_documents_are_unchanged(self):
        markers = [h for hs in hook_entries(self.project).values() for h in hs
                   if h.get("extension") == "marker-hooks"]
        self.assertEqual(markers, self.markers_before)
        self.assertEqual((proj.snapshot(self.project / "specs"),
                          proj.snapshot(self.project / "docs")), self.docs_before)


if __name__ == "__main__":
    unittest.main()
