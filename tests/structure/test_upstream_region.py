"""VO-003: the grill command carries upstream v1.0.1 verbatim between markers."""
import hashlib
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
COMMAND = REPO / "commands" / "speckit.grill-specify.with-docs.md"
VENDORED = REPO / "upstream" / "with-docs.v1.0.1.md"
PATCH = REPO / "upstream" / "nested-hooks.patch"
PROVENANCE = REPO / "upstream" / "UPSTREAM.md"
BEGIN = "<!-- BEGIN UPSTREAM grill v1.0.1 -->"
END = "<!-- END UPSTREAM -->"


def upstream_body(text):
    """The text after the frontmatter's closing `---` line, without surrounding blank lines."""
    lines = text.split("\n")
    assert lines[0] == "---"
    close = lines.index("---", 1)
    return "\n".join(lines[close + 1:]).strip("\n")


def patched_body():
    body = upstream_body(VENDORED.read_text())
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "body.md"
        out = Path(tmp) / "patched.md"
        src.write_text(body + "\n")
        subprocess.run(
            ["patch", "--quiet", "-o", str(out), str(src), str(PATCH)],
            check=True, capture_output=True,
        )
        return out.read_text().strip("\n")


def marked_region(text):
    start = text.index(BEGIN) + len(BEGIN)
    end = text.index(END)
    return text[start:end].strip("\n")


class UpstreamRegion(unittest.TestCase):
    def test_region_equals_vendored_body_with_recorded_patch(self):
        self.assertEqual(marked_region(COMMAND.read_text()), patched_body())

    def test_vendored_file_hash_matches_provenance(self):
        digest = hashlib.sha256(VENDORED.read_bytes()).hexdigest()
        self.assertIn(digest, PROVENANCE.read_text())

    def test_the_patch_changes_only_the_hooks_section(self):
        original = upstream_body(VENDORED.read_text()).split("\n")
        patched = patched_body().split("\n")
        added = [l for l in patched if l not in original]
        removed = [l for l in original if l not in patched]
        self.assertEqual(removed, [], "the patch must only add text")
        self.assertTrue(added, "the patch must add the nested-run paragraph")
        idx = patched.index("## Extension hooks (same processing as clarify)")
        first_added = patched.index(added[0])
        self.assertLess(idx, first_added)
        self.assertLess(first_added, idx + 6, "paragraph sits at the top of the hooks section")

    def test_package_has_no_preset_core_template_override_or_serena_variant(self):
        self.assertFalse((REPO / "preset.yml").exists())
        self.assertFalse((REPO / "templates").exists(), "no shipped template overrides")
        text = COMMAND.read_text()
        outside = text[: text.index(BEGIN)] + text[text.index(END):]
        self.assertIsNone(re.search("serena", outside, re.IGNORECASE))
        for path in list((REPO / "commands").glob("*")) + list(REPO.glob("*serena*")):
            self.assertNotIn("serena", path.name.lower())


if __name__ == "__main__":
    unittest.main()
