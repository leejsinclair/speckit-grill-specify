"""VO-038 (DC-02): the shipped scripts avoid constructs that Bash 3.2 lacks."""
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = sorted((REPO / "scripts" / "bash").glob("*.sh"))

FORBIDDEN = [
    (r"\bdeclare\s+-[a-zA-Z]*A", "declare -A (associative array)"),
    (r"\blocal\s+-[a-zA-Z]*A", "local -A (associative array)"),
    (r"\bmapfile\b", "mapfile"),
    (r"\breadarray\b", "readarray"),
    (r"\bcoproc\b", "coproc"),
    (r"\$\{[A-Za-z_][A-Za-z0-9_]*(,,|\^\^)", "case conversion expansion"),
    (r"\|&", "|&"),
    (r"&>>", "&>>"),
    (r"\[\[\s+-v\b", "[[ -v"),
    (r"\$\{[A-Za-z_][A-Za-z0-9_]*\[-\d+\]\}", "negative array index"),
    (r"printf\s+'%\([^)]*\)T", "printf %()T"),
    (r"\bread\s+(-[a-zA-Z]+\s+)*-i\b", "read -i"),
]


class NoNewerBashConstructs(unittest.TestCase):
    def test_scripts_exist(self):
        self.assertEqual([p.name for p in SCRIPTS], ["grill-context.sh", "grill-label.sh"])

    def test_no_construct_bash_3_2_lacks(self):
        problems = []
        for script in SCRIPTS:
            for number, line in enumerate(script.read_text().splitlines(), 1):
                code = line.split("#", 1)[0] if not re.search(r"['\"].*#", line) else line
                for pattern, label in FORBIDDEN:
                    if re.search(pattern, code):
                        problems.append("%s:%d uses %s" % (script.name, number, label))
        self.assertEqual(problems, [])


class RunsUnderNamedBash(unittest.TestCase):
    def test_script_unit_cases_pass_under_the_named_bash(self):
        bash = os.environ.get("GRILL_TEST_BASH")
        if not bash:
            self.skipTest("GRILL_TEST_BASH is not set: not run")
        env = dict(os.environ, GRILL_TEST_BASH=bash)
        result = subprocess.run(
            [sys.executable, "-B", "-m", "unittest",
             "tests.structure.test_grill_context", "tests.structure.test_grill_label"],
            cwd=str(REPO), env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
