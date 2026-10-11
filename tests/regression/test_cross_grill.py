"""VO-037 (EC-06): this extension's grill and upstream's can be run one after the other."""
import re
import shutil
import unittest

from tests.support import project as proj
from tests.support.agent import Session, drive_standalone

UPSTREAM = proj.FIXTURES / "upstream-grill"
OURS = "/speckit-grill-specify-with-docs"
THEIRS = "/speckit-grill-with-docs"
LABEL = re.compile(r"(?m)^\*\*Grilled on\*\*:.*$")


def clarifications(text):
    return [l for l in text.splitlines() if l.startswith("- Q:")]


class CrossGrill(unittest.TestCase):
    def run_pair(self, first, second):
        project = proj.new_project()
        self.addCleanup(shutil.rmtree, project.parent, True)
        proj.add_extension(project, proj.REPO)
        proj.add_extension(project, UPSTREAM)
        feature = proj.install_feature(project, "ambiguous")
        spec = feature / "spec.md"
        _, final = drive_standalone(Session(project), first)
        self.assertIsNotNone(final, "first grill did not finish")
        mid = spec.read_text()
        _, final = drive_standalone(Session(project), second)
        self.assertIsNotNone(final, "second grill did not finish")
        end = spec.read_text()
        before, after = clarifications(mid), clarifications(end)
        self.assertEqual(after[:len(before)], before, "earlier Clarifications lines changed")
        questions = [l.split("→")[0] for l in after]
        self.assertEqual(len(questions), len(set(questions)), "a question was recorded again")
        labels = LABEL.findall(end)
        self.assertEqual(len(labels), 1, labels)
        lines = end.splitlines()
        status = next(i for i, l in enumerate(lines) if l.startswith("**Status**:"))
        self.assertEqual(lines[status + 2], labels[0], "label is not directly under Status")

    def test_ours_then_upstream(self):
        self.run_pair(OURS, THEIRS)

    def test_upstream_then_ours(self):
        self.run_pair(THEIRS, OURS)


if __name__ == "__main__":
    unittest.main()
