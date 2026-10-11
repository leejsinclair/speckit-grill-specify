"""Contract tests for the extension manifest (extension.yml at the repository root)."""
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]


def load_manifest():
    return yaml.safe_load((REPO / "extension.yml").read_text())


class ManifestHook(unittest.TestCase):
    def test_single_mandatory_after_specify_hook_ahead_of_default(self):
        hooks = load_manifest().get("hooks", {})
        self.assertEqual(
            [name for name in hooks if name == "after_specify"], ["after_specify"],
            "the manifest must declare an after_specify hook",
        )
        self.assertEqual(sorted(hooks), ["after_specify"], "no other hook may be declared")
        hook = hooks["after_specify"]
        self.assertIsInstance(hook, dict, "after_specify must be exactly one hook entry")
        self.assertEqual(hook["command"], "speckit.grill-specify.auto")
        self.assertIs(hook["optional"], False)
        self.assertNotIn("condition", hook)
        self.assertIsInstance(hook["priority"], int)
        self.assertLess(hook["priority"], 10)


class ManifestCommands(unittest.TestCase):
    def test_commands_are_namespaced_and_requirements_stated(self):
        manifest = load_manifest()
        commands = manifest["provides"]["commands"]
        names = [c["name"] for c in commands]
        for name in names:
            self.assertTrue(name.startswith("speckit.grill-specify."), name)
        for command in commands:
            self.assertNotIn("aliases", command, command["name"])
        self.assertIn("speckit.grill-specify.with-docs", names)

        requires = manifest["requires"]
        self.assertEqual(requires["speckit_version"], ">=1.1.3")
        tools = {t["name"]: t for t in requires.get("tools", [])}
        self.assertIn("bash", tools)
        self.assertIs(tools["bash"]["required"], True)

        # Nothing may name or require the upstream grill extension (id "grill").
        for key in ("extensions", "requires_extensions", "dependencies"):
            self.assertNotIn(key, requires)
        self.assertNotIn("speckit-grill-me", str(requires))
        self.assertNotIn("yoshi1220", str(requires))


if __name__ == "__main__":
    unittest.main()
