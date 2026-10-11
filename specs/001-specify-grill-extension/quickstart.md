# Quickstart: Validating the Specify Grill Extension

**Feature**: `001-specify-grill-extension` | **Date**: 2026-10-11

How to prove the extension works end to end. Contracts are in
[contracts/](./contracts/); entities are in [data-model.md](./data-model.md).

## Prerequisites

- macOS or Linux with `bash`, `python3` and `git`
- `specify` CLI 1.1.3 or later (`specify --version`). This machine has 1.0.2.dev0 and
  must be upgraded first: `uv tool upgrade specify-cli`
- `claude` (Claude Code), signed in, for the behaviour and regression levels
- `<repo>` below is the absolute path of this repository's root

## 1. Automated checks

```bash
make test          # structure + install levels: offline, no agent, under a minute
make test-live     # behaviour + regression levels: drives Claude Code, uses tokens
```

`make test-live` uses Haiku by default. Set `GRILL_TEST_MODEL` to use another model.

Expected: both exit 0. `make test` passing shows the manifest, the upstream region, the
scripts and install, reinstall and removal are correct. `make test-live` passing shows
the nested and standalone behaviour in the scenarios below.

## 2. Install into a throwaway project

Use a temporary directory outside this repository.

```bash
specify init <tmp-project> --integration claude
cd <tmp-project>
specify extension add --dev <repo>
specify extension list
```

Expected:

- `grill-specify` is listed with 2 commands and 1 hook.
- `.specify/extensions.yml` has one `after_specify` entry for `grill-specify`, with
  `optional: false` and `priority: 5`.
- `.specify/extensions/grill-specify/grill-specify-config.yml` exists and reads
  `grill: "on"`.
- `.claude/skills/` contains `speckit-grill-specify-with-docs` and
  `speckit-grill-specify-auto`.

## 3. Nested run, setting on (User Stories 1 and 3)

In Claude Code, in the throwaway project:

```text
/speckit-specify Add a "remember me" option to the sign-in page
```

Expected: once the spec and checklist are written, the grill starts with no further
command. It states how many points it found, asks its first question and offers a skip
choice. No file has changed yet.

- **Answer until done, then choose "Finish and proceed"**: the spec has a
  `## Clarifications` section and `**Grilled on**: <today>` under Status; specify's
  report contains `GRILL OUTCOME: completed`, a coverage summary and the knowledge docs
  changed.
- **Or take the skip choice**: `git status` (or a file comparison) shows nothing changed
  after specify's own output; the report contains `GRILL OUTCOME: skipped`.

## 4. Stop early and resume (User Story 4)

Run specify again on a new feature, answer two questions, then say `stop`.

Expected: the spec keeps both answers; the label reads
`**Grilled on**: <today> (stopped early, N points open)`; the report contains
`GRILL OUTCOME: stopped early` and lists the outstanding points. Then:

```text
/speckit-grill-specify-with-docs
```

Expected: it states how many points are open, offers no skip choice, and asks nothing
that the Clarifications section already settles.

## 5. The grill setting (User Story 2)

Edit `.specify/extensions/grill-specify/grill-specify-config.yml` and run specify after
each change.

| Setting line | Expected |
|--------------|----------|
| `grill: "strict"` | The grill starts; its opening has no skip choice |
| `grill: "off"` | No grill; report contains `GRILL OUTCOME: switched off`; spec identical to plain specify |
| `grill: "of"` | The grill starts as `on`; the report carries a one-line warning naming `of` |

## 6. Nobody present (User Story 5)

```bash
claude -p "/speckit-specify Add a remember-me option to the sign-in page"
```

Expected: the command returns without waiting; the output contains
`GRILL OUTCOME: not run (no human present)`; the spec has no Clarifications section and
no label. The same holds with `SPECKIT_GRILL_NONINTERACTIVE=1` in an interactive
session.

## 7. Coexistence and removal (User Story 6)

```bash
specify extension add grill          # upstream, from the community catalogue
specify extension list
specify extension remove grill-specify
```

Expected: after the add, the commands of both extensions are listed and both
`/speckit-grill-with-docs` and `/speckit-grill-specify-with-docs` run. After the remove,
`.specify/extensions.yml` has no `grill-specify` entry, other extensions' entries are
unchanged, and every spec and knowledge doc is still in place.

## 8. Locked-down devcontainer (FR-019, manual)

In the Claude Code devcontainer whose managed settings block user-level skills and
agents, repeat steps 2, 3 and 4. Expected: identical results. This step is manual
because the container's managed settings cannot be reproduced on a developer machine;
the automated stand-in runs the same scenarios with an empty user configuration
directory.

## 9. Install from the published release (FR-025)

After the first tag is pushed:

```bash
specify extension add grill-specify --from https://github.com/leejsinclair/speckit-grill-specify/archive/refs/tags/v0.1.0.zip
```

Expected: the same commands and the same single hook registration as step 2.

## 10. Standalone run with no feature or no spec (edge case, manual)

In a project with the extension installed and no feature directory, run
`/speckit-grill-specify-with-docs`. Repeat with an active feature directory that has no
`spec.md`. Expected: each run stops with a clear message, asks no question and creates
or changes no file. This step is manual by decision of 2026-10-11: the behaviour is
upstream's Prerequisites, and no automated test covers it.
