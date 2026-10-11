"""VO-005, VO-006, VO-007: the run-context script (scripts/bash/grill-context.sh)."""
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.support.project import snapshot

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "bash" / "grill-context.sh"
SIGNALS = ("SPECKIT_GRILL_NONINTERACTIVE", "CLAUDE_CODE_SESSION_ATTENDED",
           "CLAUDE_CODE_ENTRYPOINT", "SPECKIT_GRILL_CONFIG")


def run_script(cwd, env=None):
    clean = {k: v for k, v in os.environ.items() if k not in SIGNALS}
    clean.update(env or {})
    proc = subprocess.run([os.environ.get("GRILL_TEST_BASH", "bash"), str(SCRIPT), "--json"], cwd=str(cwd), env=clean,
                          capture_output=True, text=True)
    return proc


def context(cwd, env=None):
    proc = run_script(cwd, env)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


class SettingTable(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def read(self, content=None, make_unreadable=False):
        cfg = self.dir / "config.yml"
        if content is not None:
            cfg.write_text(content)
            if make_unreadable:
                cfg.chmod(0)
        return context(self.dir, {"SPECKIT_GRILL_CONFIG": str(cfg)})

    def test_file_missing_gives_on_without_warning(self):
        result = self.read(None)
        self.assertEqual((result["setting"], result["setting_source"], result["warning"]),
                         ("on", "default", ""))

    def test_no_grill_line_gives_on_default(self):
        result = self.read("# only a comment\nother: 1\n")
        self.assertEqual((result["setting"], result["setting_source"], result["warning"]),
                         ("on", "default", ""))

    def test_valid_values_are_read_in_every_written_form(self):
        cases = {
            'grill: on\n': "on", 'grill: "on"\n': "on", "grill: 'on'\n": "on",
            'grill: ON\n': "on", 'grill: strict\n': "strict", 'grill: "Strict"\n': "strict",
            'grill: off\n': "off", 'grill: off   # not today\n': "off",
            '# grill: off\ngrill: strict\n': "strict",
            'grill: strict\ngrill: off\n': "strict",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                result = self.read(text)
                self.assertEqual(result["setting"], expected)
                self.assertEqual(result["setting_source"], "config")
                self.assertEqual(result["warning"], "")

    def test_unknown_value_falls_back_with_one_line_warning(self):
        result = self.read("grill: of\n")
        self.assertEqual(result["setting"], "on")
        self.assertEqual(result["setting_source"], "default")
        self.assertEqual(result["warning"],
                         'Grill setting "of" is not one of on, strict, off; using on.')

    @unittest.skipIf(os.geteuid() == 0, "root can read any file")
    def test_unreadable_file_falls_back_with_warning(self):
        result = self.read("grill: off\n", make_unreadable=True)
        self.assertEqual(result["setting"], "on")
        self.assertEqual(result["warning"], "Grill setting file could not be read; using on.")


class Interactivity(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def check(self, env, interactive, reason):
        result = context(self.dir, env)
        self.assertEqual((result["interactive"], result["interactive_reason"]),
                         (interactive, reason), env)

    def test_switch_says_unattended(self):
        for value in ("1", "true", "yes", "TRUE", "Yes"):
            self.check({"SPECKIT_GRILL_NONINTERACTIVE": value}, False, "switch")

    def test_switch_says_attended(self):
        for value in ("0", "false", "no", "FALSE", "No"):
            self.check({"SPECKIT_GRILL_NONINTERACTIVE": value}, True, "switch")

    def test_agent_indicators_mark_an_unattended_run(self):
        self.check({"CLAUDE_CODE_SESSION_ATTENDED": "0"}, False, "agent")
        self.check({"CLAUDE_CODE_ENTRYPOINT": "sdk-cli"}, False, "agent")

    def test_switch_off_overrides_the_agent_indicator(self):
        self.check({"SPECKIT_GRILL_NONINTERACTIVE": "0", "CLAUDE_CODE_ENTRYPOINT": "sdk-cli"},
                   True, "switch")

    def test_no_signal_is_interactive(self):
        self.check({}, True, "no-signal")
        self.check({"CLAUDE_CODE_ENTRYPOINT": "cli", "CLAUDE_CODE_SESSION_ATTENDED": "1"},
                   True, "no-signal")

    def test_unrecognised_switch_value_is_ignored(self):
        self.check({"SPECKIT_GRILL_NONINTERACTIVE": "maybe"}, True, "no-signal")
        self.check({"SPECKIT_GRILL_NONINTERACTIVE": "maybe", "CLAUDE_CODE_ENTRYPOINT": "sdk-cli"},
                   False, "agent")


class ReadOnly(unittest.TestCase):
    """DC-01: the script creates, changes and removes nothing, whatever the setting state."""

    def test_project_directory_is_identical_after_every_setting_state(self):
        states = [None, "# nothing\n", "grill: on\n", "grill: strict\n", "grill: off\n",
                  "grill: of\n"]
        for content in states:
            for readonly in (False, True):
                with self.subTest(content=content, readonly=readonly):
                    with tempfile.TemporaryDirectory() as tmp:
                        project = Path(tmp)
                        cfg_dir = project / ".specify" / "extensions" / "grill-specify"
                        cfg_dir.mkdir(parents=True)
                        (project / "specs").mkdir()
                        (project / "specs" / "spec.md").write_text("spec\n")
                        if content is not None:
                            cfg = cfg_dir / "grill-specify-config.yml"
                            cfg.write_text(content)
                            if readonly:
                                cfg.chmod(0o444)
                        before = snapshot(project)
                        listing_before = sorted(p.name for p in project.rglob("*"))
                        proc = run_script(project)
                        self.assertEqual(proc.returncode, 0)
                        self.assertEqual(snapshot(project), before)
                        self.assertEqual(sorted(p.name for p in project.rglob("*")),
                                         listing_before)


if __name__ == "__main__":
    unittest.main()
