"""VO-004: provenance, licences, changelog and README agree."""
import re
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]


class Provenance(unittest.TestCase):
    def test_provenance_record(self):
        text = (REPO / "upstream" / "UPSTREAM.md").read_text()
        self.assertIn("https://github.com/yoshi1220/speckit-grill-me", text)
        self.assertIn("v1.0.1", text)
        self.assertRegex(text, r"(?i)spec kit[^\n]*verified[^\n]*\d{4}-\d{2}-\d{2}")
        self.assertRegex(text, r"(?m)^#+ Updating from upstream")

    def test_licences(self):
        self.assertEqual((REPO / "upstream" / "LICENSE.upstream").read_text(),
                         (REPO / "tests" / "fixtures" / "upstream-grill" / "LICENSE").read_text())
        licence = (REPO / "LICENSE").read_text()
        self.assertIn("MIT License", licence)
        self.assertIn("Permission is hereby granted, free of charge", licence)

    def test_versions_agree(self):
        version = yaml.safe_load((REPO / "extension.yml").read_text())["extension"]["version"]
        headings = re.findall(r"(?m)^## \[?(\d+\.\d+\.\d+)\]?", (REPO / "CHANGELOG.md").read_text())
        self.assertTrue(headings, "CHANGELOG.md has no version heading")
        self.assertEqual(headings[0], version)
        readme = (REPO / "README.md").read_text()
        tags = re.findall(r"archive/refs/tags/v(\d+\.\d+\.\d+)\.zip", readme)
        self.assertTrue(tags, "README.md has no archive URL")
        self.assertEqual(set(tags), {version})


if __name__ == "__main__":
    unittest.main()
