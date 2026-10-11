"""Helpers that build temporary Spec Kit projects and snapshot them.

Projects are always created in a temporary directory outside this repository, so a test
never touches this repository's own `.specify/`.
"""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FIXTURES = REPO / "tests" / "fixtures"
SPECIFY = shutil.which("specify") or "specify"


def run(args, cwd, env=None, check=True, timeout=300):
    merged = dict(os.environ)
    merged.update(env or {})
    proc = subprocess.run(
        args, cwd=str(cwd), env=merged, capture_output=True, text=True, timeout=timeout
    )
    if check and proc.returncode != 0:
        raise RuntimeError(
            "command failed (%d): %s\n%s\n%s" % (proc.returncode, args, proc.stdout, proc.stderr)
        )
    return proc


def new_project(integration="claude", extensions=()):
    """Create a fresh Spec Kit project in a temporary directory and return its Path."""
    base = Path(tempfile.mkdtemp(prefix="grill-test-"))
    project = base / "project"
    run(
        [SPECIFY, "init", str(project), "--integration", integration,
         "--non-interactive", "--ignore-agent-tools"],
        cwd=base,
    )
    for ext in extensions:
        add_extension(project, ext)
    return project


def add_extension(project, path, force=False):
    args = [SPECIFY, "extension", "add", "--dev", str(path)]
    if force:
        args.append("--force")
    return run(args, cwd=project)


def remove_extension(project, ext_id):
    return run([SPECIFY, "extension", "remove", ext_id, "--force"], cwd=project, check=False)


def read_extensions_yml(project):
    """Return the parsed `.specify/extensions.yml` as a dict (empty when absent)."""
    path = Path(project) / ".specify" / "extensions.yml"
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore
        return yaml.safe_load(path.read_text()) or {}
    except ImportError:
        return _cli_python_json(
            "import yaml,json,sys;print(json.dumps(yaml.safe_load(open(sys.argv[1]).read()) or {}))",
            str(path),
        )


def _cli_python():
    """The Python interpreter that runs the installed `specify` CLI."""
    first = Path(SPECIFY).read_text(errors="ignore").splitlines()[0]
    if first.startswith("#!"):
        return first[2:].strip()
    return "python3"


def _cli_python_json(code, *args):
    out = subprocess.run([_cli_python(), "-c", code, *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr)
    return json.loads(out.stdout)


def hooks_for_event(project, event):
    """Hooks for `event` in the order the installed CLI's own resolution returns them."""
    code = (
        "import sys, json\n"
        "from pathlib import Path\n"
        "from specify_cli.extensions import HookExecutor\n"
        "h = HookExecutor(Path(sys.argv[1]))\n"
        "print(json.dumps(h.get_hooks_for_event(sys.argv[2])))\n"
    )
    return _cli_python_json(code, str(project), event)


def list_skills(project):
    """Names of agent skills installed in the project (Claude layout)."""
    root = Path(project) / ".claude" / "skills"
    return sorted(p.name for p in root.iterdir() if p.is_dir()) if root.is_dir() else []


def snapshot(root, ignore=(".git", ".marker-log-ignore")):
    """Map every file path under root to its SHA-256, for before/after comparison."""
    root = Path(root)
    out = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in ignore for part in path.relative_to(root).parts):
            continue
        out[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def changed_paths(before, after):
    return sorted(
        p for p in set(before) | set(after) if before.get(p) != after.get(p)
    )


def install_feature(project, fixture_name, feature="001-demo"):
    """Copy tests/fixtures/specs/<fixture_name> into the project as a feature directory."""
    dest = Path(project) / "specs" / feature
    shutil.copytree(FIXTURES / "specs" / fixture_name, dest)
    feature_json = Path(project) / ".specify" / "feature.json"
    feature_json.parent.mkdir(parents=True, exist_ok=True)
    feature_json.write_text(json.dumps({"feature_directory": "specs/%s" % feature}))
    return dest
