"""VO-017: a term used beyond the feature and a qualifying decision reach the knowledge docs."""
import re
import shutil
import unittest
from pathlib import Path

from tests.support import project as proj
from tests.support.agent import Session

TERM_ANSWER = (
    "Option A. And this is settled for the whole company, not only this feature: the person "
    "who buys is always called a 'Shopper'. The words 'customer' and 'user' must not be used "
    "for this person anywhere in our products (checkout, accounts, support)."
)
DECISION_ANSWER = (
    "Option A. Also a company-wide architecture decision that is costly to reverse: all carts "
    "are stored server-side in our PostgreSQL database. We considered browser-only storage and "
    "Redis and rejected both because carts must be auditable and shared across devices. Please "
    "record this as a decision."
)
DETAIL_ANSWER = (
    "Option A. This one is only a detail of this feature: show totals with two decimals. It "
    "is not a project-wide decision and needs no decision record."
)


class KnowledgeDocs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = proj.new_project()
        cls.addClassCleanup(shutil.rmtree, cls.project.parent, True)
        proj.add_extension(cls.project, proj.REPO)
        proj.install_feature(cls.project, "ambiguous")
        cls.session = Session(cls.project)
        cls.session.say("/speckit-grill-specify-auto")
        for answer in (TERM_ANSWER, DECISION_ANSWER, DETAIL_ANSWER):
            cls.session.say(answer)

    def test_term_is_defined_once_and_one_decision_record_exists(self):
        root = self.project / "docs" / "domain_knowledge"
        context = (root / "CONTEXT.md").read_text()
        definitions = re.findall(r"(?im)^[\s\-*#>]*\**shopper\**\s*[:—–-]", context)
        self.assertEqual(len(definitions), 1, context)
        records = sorted((root / "adr").glob("*.md"))
        self.assertEqual(len(records), 1, [r.name for r in records])
        record = records[0].read_text()
        self.assertRegex(record, r"(?i)postgres")
        self.assertNotRegex(record, r"(?i)two decimals")


if __name__ == "__main__":
    unittest.main()
