"""VO-008, VO-009: the label script (scripts/bash/grill-label.sh)."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "bash" / "grill-label.sh"
SPECS = REPO / "tests" / "fixtures" / "specs"
DATE = "2026-10-11"

HEADER = "# Feature Specification: Demo\n\n**Status**: Draft\n\n**Input**: something\n\n## Body\n\ntext\n"


def run_label(spec, *args):
    return subprocess.run([os.environ.get("GRILL_TEST_BASH", "bash"), str(SCRIPT), "--spec", str(spec), *args],
                          capture_output=True, text=True)


class LabelInsertion(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.spec = self.dir / "spec.md"

    def expect_insert(self, args, label):
        self.spec.write_text(HEADER)
        proc = run_label(self.spec, *args, "--date", DATE)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), label)
        expected = HEADER.replace("**Status**: Draft\n\n", "**Status**: Draft\n\n%s\n\n" % label)
        self.assertEqual(self.spec.read_text(), expected)
        # repeating the same command changes nothing
        again = run_label(self.spec, *args, "--date", DATE)
        self.assertEqual(again.returncode, 0)
        self.assertEqual(self.spec.read_text(), expected)

    def test_complete_label(self):
        self.expect_insert(["--state", "complete"], "**Grilled on**: 2026-10-11")

    def test_stopped_label_with_several_points(self):
        self.expect_insert(["--state", "stopped", "--open", "4"],
                           "**Grilled on**: 2026-10-11 (stopped early, 4 points open)")

    def test_stopped_label_with_one_point_is_singular(self):
        self.expect_insert(["--state", "stopped", "--open", "1"],
                           "**Grilled on**: 2026-10-11 (stopped early, 1 point open)")

    def test_fixture_spec_changes_only_by_the_label(self):
        text = (SPECS / "ambiguous" / "spec.md").read_text()
        self.spec.write_text(text)
        self.assertEqual(run_label(self.spec, "--state", "complete", "--date", DATE).returncode, 0)
        after = self.spec.read_text().split("\n")
        before = text.split("\n")
        self.assertEqual([l for l in after if l not in before],
                         ["**Grilled on**: 2026-10-11"])


class LabelReplacementAndFailure(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.spec = self.dir / "spec.md"

    def test_existing_label_is_replaced_in_place_leaving_exactly_one(self):
        with_label = HEADER.replace("**Status**: Draft\n\n",
                                    "**Status**: Draft\n\n**Grilled on**: 2026-01-01 (stopped early, 3 points open)\n\n")
        self.spec.write_text(with_label)
        proc = run_label(self.spec, "--state", "complete", "--date", DATE)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        text = self.spec.read_text()
        self.assertEqual(text.count("**Grilled on**:"), 1)
        self.assertEqual(text, HEADER.replace("**Status**: Draft\n\n",
                                              "**Status**: Draft\n\n**Grilled on**: 2026-10-11\n\n"))
        run_label(self.spec, "--state", "stopped", "--open", "2", "--date", "2026-10-12")
        text = self.spec.read_text()
        self.assertEqual(text.count("**Grilled on**:"), 1)
        self.assertIn("**Grilled on**: 2026-10-12 (stopped early, 2 points open)", text)

    def test_spec_without_status_line_exits_3_and_is_unchanged(self):
        shutil.copy(SPECS / "no-status" / "spec.md", self.spec)
        before = self.spec.read_bytes()
        proc = run_label(self.spec, "--state", "complete", "--date", DATE)
        self.assertEqual(proc.returncode, 3)
        self.assertEqual(self.spec.read_bytes(), before)

    def test_missing_spec_exits_3(self):
        proc = run_label(self.dir / "absent.md", "--state", "complete")
        self.assertEqual(proc.returncode, 3)

    def test_bad_arguments_exit_2_and_leave_the_spec_unchanged(self):
        self.spec.write_text(HEADER)
        before = self.spec.read_bytes()
        bad = [
            [],
            ["--state", "finished"],
            ["--state", "stopped"],
            ["--state", "stopped", "--open", "x"],
            ["--state", "stopped", "--open", "-1"],
            ["--state", "complete", "--open", "2"],
            ["--state", "complete", "--date", "yesterday"],
        ]
        for args in bad:
            with self.subTest(args=args):
                proc = run_label(self.spec, *args)
                self.assertEqual(proc.returncode, 2, proc.stderr)
                self.assertEqual(self.spec.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
