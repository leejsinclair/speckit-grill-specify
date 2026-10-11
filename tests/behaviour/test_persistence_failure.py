"""VO-033 (EC-04): a knowledge doc that cannot be saved is reported, never written elsewhere."""
import os
import shutil
import stat
import unittest
from pathlib import Path

from tests.support import project as proj
from tests.support.agent import Session, outcome_block

TERM = ("Option A. Settled for the whole company, used in every product: the buyer is always "
        "called a 'Shopper', never 'customer' or 'user'. Record it in the knowledge docs.")


@unittest.skipIf(os.geteuid() == 0, "root ignores read-only directories")
class PersistenceFailure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, proj.REPO)
        proj.install_feature(cls.project, "ambiguous")
        cls.knowledge = cls.project / "docs" / "domain_knowledge"
        cls.knowledge.mkdir(parents=True)
        cls.knowledge.chmod(stat.S_IRUSR | stat.S_IXUSR)
        cls.addClassCleanup(cls.knowledge.chmod, 0o755)
        cls.before = proj.snapshot(cls.project)
        cls.session = Session(cls.project)
        cls.session.say("/speckit-grill-specify-auto")
        cls.answer_reply = cls.session.say(TERM)
        cls.next_reply = cls.session.say("Continue.")

    def test_failure_is_stated_and_run_is_not_reported_completed(self):
        self.assertRegex(self.answer_reply + self.next_reply,
                         r"(?i)(read-only|permission|could not|cannot|unable|failed|not saved)")
        for reply in (self.answer_reply, self.next_reply):
            block = outcome_block(reply)
            if block:
                self.assertNotIn("GRILL OUTCOME: completed", block)

    def test_no_knowledge_doc_is_written_anywhere_else(self):
        after = proj.snapshot(self.project)
        new = [p for p in after if p not in self.before]
        stray = [p for p in new if not p.startswith("specs/")
                 and p.lower().endswith(".md")]
        self.assertEqual(stray, [])


if __name__ == "__main__":
    unittest.main()
