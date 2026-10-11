"""VO-028: with no human present the nested grill returns at once and changes nothing."""
import re
import shutil
import unittest

from tests.behaviour.test_setting import setup
from tests.support import project as proj
from tests.support.agent import Session, outcome_block


class Unattended(unittest.TestCase):
    def check(self, setting, env):
        project, feature = setup('grill: "%s"' % setting)
        self.addCleanup(shutil.rmtree, project.parent, True)
        before = proj.snapshot(project)
        reply = Session(project, env=env).say("/speckit-grill-specify-auto")
        block = outcome_block(reply)
        self.assertIsNotNone(block, reply)
        self.assertEqual(block.splitlines()[0].strip(),
                         "GRILL OUTCOME: not run (no human present)")
        self.assertRegex(block, r"(?m)^Reason: .*has not been clarified")
        self.assertEqual(proj.snapshot(project), before)

    def test_all_settings_with_the_documented_switch(self):
        for setting in ("on", "strict", "off"):
            with self.subTest(setting=setting):
                self.check(setting, {"SPECKIT_GRILL_NONINTERACTIVE": "1"})

    def test_all_settings_with_only_the_agents_own_indicator(self):
        for setting in ("on", "strict", "off"):
            with self.subTest(setting=setting):
                self.check(setting, {"SPECKIT_GRILL_NONINTERACTIVE": None,
                                     "CLAUDE_CODE_ENTRYPOINT": "sdk-cli"})


if __name__ == "__main__":
    unittest.main()
