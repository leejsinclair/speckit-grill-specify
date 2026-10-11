"""VO-032: the standalone grill matches upstream v1.0.1 on the same scripted answers."""
import os
import re
import shutil
import unittest
from pathlib import Path

from tests.support import project as proj
from tests.support.agent import Session

REFERENCE = proj.FIXTURES / "reference-feature"
UPSTREAM = proj.FIXTURES / "upstream-grill"

# Scripted answers keyed by topic: the first pattern found in the question wins.
ANSWERS = [
    (r"(?i)retention|how long|expire|keep", "Option A, 30 days of inactivity."),
    (r"(?i)how many|limit|cap\b", "Option A, a cap of 50 distinct products."),
    (r"(?i)canonical|shopper|customer|called", "Option A: 'Shopper' is the canonical term; "
                                                  "'customer' and 'user' are avoided."),
]
DEFAULT = "Option A, the recommended one."


def answer_for(reply):
    for pattern, answer in ANSWERS:
        if re.search(pattern, reply):
            return answer
    return DEFAULT


# R15: Haiku is too unreliable for a comparison of two interviews; use a stronger model here.
MODEL = os.environ.get("GRILL_EQUIVALENCE_MODEL", "sonnet")


def run_grill(project, command):
    session = Session(project, model=MODEL)
    reply = session.say(command)
    replies = [reply]
    for _ in range(26):
        if "Finish and proceed" in reply:
            reply = session.say("Finish and proceed")
            replies.append(reply)
            break
        reply = session.say(answer_for(reply))
        replies.append(reply)
    return replies


def sections(text):
    """Map each level-2 heading to its whole body, sub-headings included."""
    parts = re.split(r"(?m)^(## .*)$", text)
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def changed_sections(before, after):
    strip = lambda t: re.sub(r"(?m)^\*\*Grilled on\*\*:.*$", "", t)
    b, a = sections(strip(before)), sections(strip(after))
    return sorted(h for h in set(a) | set(b) if a.get(h) != b.get(h))


def coverage(replies):
    found = {}
    for line in "\n".join(replies).splitlines():
        m = re.match(r"\s*\|?\s*([A-Za-z][A-Za-z /&,-]+?)\s*\|\s*\**(Clear|Resolved|Outstanding|Deferred)\**\b", line)
        if m:
            found[m.group(1).strip().lower()] = m.group(2)
    return found


def prepare(extension_path):
    project = proj.new_project()
    proj.add_extension(project, proj.REPO)
    if extension_path:
        proj.add_extension(project, extension_path)
    feature = project / "specs" / "001-demo"
    shutil.copytree(REFERENCE, feature)
    (project / ".specify" / "feature.json").write_text('{"feature_directory": "specs/001-demo"}')
    return project, feature


class Equivalence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = (REFERENCE / "spec.md").read_text()
        up_project, cls.up_feature = prepare(UPSTREAM)
        our_project, cls.our_feature = prepare(None)
        cls.addClassCleanup(shutil.rmtree, up_project.parent, True)
        cls.addClassCleanup(shutil.rmtree, our_project.parent, True)
        cls.up_project, cls.our_project = up_project, our_project
        cls.up_replies = run_grill(up_project, "/speckit-grill-with-docs")
        cls.our_replies = run_grill(our_project, "/speckit-grill-specify-with-docs")

    def test_same_sections_clarifications_knowledge_docs_and_coverage(self):
        up_text = (self.up_feature / "spec.md").read_text()
        our_text = (self.our_feature / "spec.md").read_text()
        self.assertEqual(changed_sections(self.original, our_text),
                         changed_sections(self.original, up_text))
        count = lambda t: len([l for l in t.splitlines() if l.startswith("- Q:")])
        self.assertEqual(count(our_text), count(up_text))
        docs = lambda p: sorted(str(f.relative_to(p)) for f in
                                (p / "docs" / "domain_knowledge").rglob("*.md")) \
            if (p / "docs" / "domain_knowledge").exists() else []
        self.assertEqual(docs(self.our_project), docs(self.up_project))
        self.assertEqual(coverage(self.our_replies), coverage(self.up_replies))


if __name__ == "__main__":
    unittest.main()
