# Research: Specify Grill Extension

**Feature**: `001-specify-grill-extension` | **Date**: 2026-10-11

Evidence was gathered on 2026-10-11 from the installed Spec Kit CLI source
(`specify_cli/extensions/__init__.py`, version 1.0.2.dev0), the Spec Kit repository,
upstream `yoshi1220/speckit-grill-me` at tag `v1.0.1`, the sibling extensions installed in
this project (`c4`, `know-your-spec`, `integrated-tdd`) and Claude Code 2.1.296.

## R1. Package shape and repository layout

- **Decision**: The repository root is the extension root: `extension.yml` sits at the top
  level, next to `commands/`, `scripts/bash/`, `upstream/` and `config-template.yml`.
  Everything that must not be installed (`specs/`, `docs/`, `tests/`, `scripts/dev/`,
  `.specify/`, `.claude/`, `.agents/`, `skills-lock.json`, `Makefile`) is listed in
  `.extensionignore`.
- **Rationale**: A GitHub tag archive then installs directly with
  `specify extension add grill-specify --from <archive url>`, and a local tree installs
  with `specify extension add --dev <path>` (FR-025). Both sibling extensions use this
  shape. `.extensionignore` takes gitignore-style patterns and is honoured by the CLI's
  copy step.
- **Alternatives considered**: A `spec-kit-extension/` subdirectory, as upstream uses.
  Rejected because a tag archive would then need a separately built zip uploaded to each
  release, which adds a build step for no gain.

## R2. Hook registration and ordering

- **Decision**: Register one `after_specify` hook with `optional: false`, no `condition`,
  and `priority: 5`.
- **Rationale**: `get_hooks_for_event` sorts enabled hooks by `priority` ascending, with
  ties kept in insertion order; `DEFAULT_HOOK_PRIORITY` is 10 and a manifest priority
  must be an integer of 1 or more. A priority of 5 therefore runs before every hook that
  takes the default (the Comprehension Checkpoint is registered at 10 in this project),
  whatever the install order, and leaves 1 to 4 free for a hook that must precede the
  grill (FR-009). `optional: false` makes specify invoke the hook without asking
  (FR-011). Core command templates skip any hook with a non-empty `condition`, so the
  grill setting cannot live there (FR-005).
- **Reinstall and uninstall**: `register_hooks` purges the extension's own entries for
  an event before re-adding them, so a reinstall or upgrade leaves exactly one entry;
  `unregister_hooks` removes only entries whose `extension` is this id (FR-010).
- **Alternatives considered**: Documentation only, with the project owner editing
  priorities by hand: rejected in clarification. Priority 1: rejected because it leaves
  no room for a hook that legitimately has to run first.
- **Finding at implementation (T001, 2026-10-11, specify 1.1.3)**: the installed
  `specify` command template (`core_pack/commands/specify.md`, "Mandatory Post-Execution
  Hooks") tells the agent to read `hooks.after_specify` from `.specify/extensions.yml` and
  run each hook; it does not mention priority or sorting. `register_hooks` appends
  entries without sorting. Only `get_hooks_for_event` sorts by priority. So the order the
  agent follows is the **file order**, which is install order, and `priority: 5` alone
  does not satisfy FR-009 when another extension is installed first. Decision opened
  for T065, T066, T071 and T072.

## R3. Two commands: a hook entry point and the grill itself

- **Decision**: Ship two commands.
  - `speckit.grill-specify.with-docs`: the grill. Works standalone. Treats the run as
    nested only when its arguments begin with the token `--nested`.
  - `speckit.grill-specify.auto`: the hook entry point, a few lines long. It invokes
    `speckit.grill-specify.with-docs` with `--nested` in the same session, waits, and
    hands the outcome block back to specify.
- **Rationale**: A hook entry in `.specify/extensions.yml` carries a command id and
  nothing else, so a hook cannot pass an argument. The grill must behave differently
  when nested (setting check, skip choice, clarify hooks suppressed, outcome block for
  specify's report). A dedicated entry point makes "nested" an explicit, testable input
  instead of something the agent infers from the conversation, and keeps a single copy
  of the interview.
- **Alternatives considered**: One command that infers nesting from the preceding
  `EXECUTE_COMMAND` line: rejected because the inference is unreliable on a small model
  and cannot be tested structurally. Two full copies of the interview: rejected because
  two copies must be kept identical.

## R4. Carrying the upstream interview

- **Decision**: `commands/speckit.grill-specify.with-docs.md` holds this extension's
  wrapper text before and after one marked region,
  `<!-- BEGIN UPSTREAM grill v1.0.1 -->` to `<!-- END UPSTREAM -->`. The region is the
  body of upstream's `commands/with-docs.md` (everything after its frontmatter) with a
  single change: the "Extension hooks (same processing as clarify)" section gains the
  nested-run rule. A pristine copy is vendored at `upstream/with-docs.v1.0.1.md`, the
  change is stored as `upstream/nested-hooks.patch`, and `scripts/dev/sync-upstream.sh`
  rebuilds the region from the two. A structure test rebuilds it and compares.
- **Rationale**: This is the recorded decision in
  `docs/domain_knowledge/adr/0001-carry-upstream-interview-verbatim-in-a-wrapper.md`
  and FR-022. One installed file means the agent always has the interview in context,
  with no second file to read at run time. Equivalence with upstream is shown by a diff.
- **Upstream facts used**: v1.0.1 declares `speckit_version: ">=0.16.2"`, requires
  `bash`, registers no hooks, and is MIT licensed (copyright notice in its `LICENSE`).
  Its with-docs command is 476 lines. Its hook section processes `before_clarify` before
  asking and `after_clarify` before the completion report.
- **Alternatives considered**: A command that tells the agent to read a vendored file at
  run time: rejected because a missed read silently drops the whole interview. A freely
  edited merged copy: rejected by ADR 0001.

## R5. Where the wrapper's rules run: scripts for what can be decided mechanically

- **Decision**: Two Bash scripts ship with the extension and are called by the wrapper.
  - `scripts/bash/grill-context.sh --json` reads the grill setting and the
    non-interactive signals and prints one JSON object. It writes nothing.
  - `scripts/bash/grill-label.sh` writes or refreshes the grilled-on label in the
    active spec, and nothing else.
- **Rationale**: Setting parsing, signal detection and the label's exact form are
  deterministic rules with exact acceptance criteria (FR-005, FR-007, FR-012, FR-021).
  Putting them in scripts makes them unit-testable without an agent and removes the
  cases where a model mis-parses a config line or mis-formats a date. The interview,
  the opening, the skip choice and the outcome report stay in the prompt, because they
  are conversation.
- **Alternatives considered**: Prompt-only rules: rejected because the byte-for-byte
  guarantees (SC-002) and the label format (SC-010) would then depend on model
  behaviour in every run.

## R6. The grill setting file

- **Decision**: `config-template.yml` is installed as
  `.specify/extensions/grill-specify/grill-specify-config.yml` through
  `provides.config`. It holds one setting line, `grill: "on"`. `grill-context.sh` reads
  that line textually: the first line matching `grill:` outside comments, with quotes,
  surrounding space and a trailing comment removed, compared without regard to case.
- **Rationale**: One reviewable line in the project's files (User Story 2). A textual
  read avoids a YAML library and avoids YAML 1.1 turning a bare `on` or `off` into a
  boolean. A missing file or missing key means `on` with no warning; any other value,
  or a file that cannot be read, means `on` with a warning naming the bad value
  (FR-012).
- **Alternatives considered**: `config.defaults` in the manifest only: rejected because
  the setting must be visible and editable in the project. A setter command: out of
  scope by the spec's assumptions.

## R7. Detecting a non-interactive run

- **Decision**: `grill-context.sh` decides in this order.
  1. `SPECKIT_GRILL_NONINTERACTIVE` set to `1`, `true` or `yes`: non-interactive.
  2. `SPECKIT_GRILL_NONINTERACTIVE` set to `0`, `false` or `no`: interactive, whatever
     the agent indicates.
  3. Claude Code's own indicator `CLAUDE_CODE_SESSION_ATTENDED=0`, or
     `CLAUDE_CODE_ENTRYPOINT` beginning `sdk-`: non-interactive.
  4. Otherwise interactive.
- **Rationale**: FR-007 allows explicit signals only. Measured on Claude Code 2.1.296:
  an interactive session has `CLAUDE_CODE_SESSION_ATTENDED=1` and
  `CLAUDE_CODE_ENTRYPOINT=cli`; `claude -p` has `CLAUDE_CODE_SESSION_ATTENDED=0` and
  `CLAUDE_CODE_ENTRYPOINT=sdk-cli`. The override in step 2 is needed because the
  behaviour tests drive the interview through `claude -p` with a scripted developer,
  and a harness that does supply answers must be able to say so.
- **Alternatives considered**: `CI=true` or a terminal check on standard input:
  rejected, because neither is an explicit statement that nobody can answer, and a
  developer in a CI-like shell would be silently skipped.

## R8. The grilled-on label

- **Decision**: The label is one line directly under the `**Status**:` line of the
  spec header, separated by a blank line as the other header lines are:
  `**Grilled on**: 2026-10-11` or
  `**Grilled on**: 2026-10-11 (stopped early, 4 points open)`. `grill-label.sh`
  replaces an existing label line or inserts a new one, and exits non-zero without
  writing if the spec has no Status line.
- **Rationale**: FR-021 fixes the position, the two forms and the one-label rule. The
  wrapper calls the script after each saved answer with the current open-point count
  and once more at the satisfaction gate. Because the stopped-early form is written
  with the first answer, a session that ends abruptly still leaves a truthful label.
- **Resume**: No progress file is kept (FR-008, FR-015). A later run reads the spec's
  Clarifications and the knowledge docs, and upstream's scan treats what they settle as
  Clear or Resolved.

## R9. Outcome reporting to specify

- **Decision**: The grill ends every nested run by printing one fenced outcome block
  with a fixed first line, `GRILL OUTCOME: <completed|stopped early|skipped|switched
  off|not run (no human present)>`, followed by the fields each outcome requires
  (FR-014). The entry-point command tells the agent to carry that block into specify's
  Completion Report. See [contracts/outcome-report.md](./contracts/outcome-report.md).
- **Rationale**: The core specify template cannot be changed (FR-020), and its
  Completion Report is produced after the hooks finish. A fixed block is the only
  channel, and a fixed first line lets a behaviour test find it in a transcript.

## R10. Coexistence with upstream

- **Decision**: Extension id `grill-specify`, commands `speckit.grill-specify.*`, no
  aliases, no templates. Nothing is named in upstream's `speckit.grill.*` namespace.
- **Rationale**: `_validate_install_conflicts` rejects an install that would collide
  with an installed command or alias, and neither extension's names overlap in either
  install order (FR-016, SC-007). The extension ships the interview itself, so upstream
  is not needed (FR-017). In Claude Code the commands become the project skills
  `speckit-grill-specify-with-docs` and `speckit-grill-specify-auto`, distinct from
  upstream's `speckit-grill-with-docs`.

## R11. Minimum Spec Kit version

- **Decision**: `requires.speckit_version: ">=1.1.3"`. The first implementation task
  upgrades the local `specify` CLI from 1.0.2.dev0.
- **Rationale**: FR-018 requires the current release as verified against the Spec Kit
  repository. `gh api repos/github/spec-kit/releases/latest` returned `v1.1.3`
  (published 2026-10-09) on 2026-10-11. Confirmed with the developer on 2026-10-11.
- **Found on 2026-10-11 (T001)**: `uv tool upgrade specify-cli` installed `specify 1.1.3`;
  `specify --version` confirms it.
- **Consequence**: Install tests cannot run on this machine until the CLI is upgraded.
  The value is re-verified at release time and the date recorded in `upstream/UPSTREAM.md`
  alongside the upstream provenance.

## R12. The locked-down devcontainer (FR-019)

- **Decision**: The extension depends only on what Spec Kit installs into the project
  (project skills under `.claude/skills/` and files under `.specify/`). It ships no
  user-level skill, no subagent definition and no Claude Code hook, and the wrapper
  never delegates to a subagent (upstream already forbids it).
- **Rationale**: The developer confirmed on 2026-10-11 that in the target devcontainer
  only user-level skills and agents are blocked and project skills installed by Spec
  Kit load normally. Claude Code's stricter managed setting
  `strictPluginOnlyCustomization` (which also blocks project skills) is not what that
  container uses; under it Spec Kit's own commands would not load either.
- **How it is verified**: A structure test asserts the package ships nothing outside
  the project install and that the command text names no subagent or user-level skill.
  A live test runs the nested and standalone grill with an empty user configuration
  directory. A run in the real devcontainer is a manual step in the quickstart.

## R13. Release and licence

- **Decision**: Public repository `https://github.com/leejsinclair/speckit-grill-specify`.
  The release artefact is GitHub's tag archive,
  `https://github.com/leejsinclair/speckit-grill-specify/archive/refs/tags/v<version>.zip`.
  First release `v0.1.0`. Licence MIT: `LICENSE` holds this project's notice, and
  `upstream/LICENSE.upstream` holds upstream's notice verbatim.
- **Rationale**: Confirmed with the developer on 2026-10-11; matches the sibling
  extensions' release process (set the version, add a changelog entry, tag, push). A
  structure test asserts the manifest version, the changelog's latest entry and the
  README's install URL agree (FR-025).
- **Prerequisite**: This project is not under version control. `git init`, the first
  commit and creating the public repository are tasks of this feature. Pushing and
  tagging are outward-facing and are done only on the developer's instruction.

## R14. Testing approach

- **Decision**: Python `unittest`, standard library only, chosen by the developer on
  2026-10-11. Commands are defined in a `Makefile` and repeated in `CONTRIBUTING.md`.
  Four directories match the four levels of SC-005.

  | Level | Directory | Needs | What it does |
  |-------|-----------|-------|--------------|
  | Structure | `tests/structure/` | python3, bash | Manifest fields, command files, upstream region against the vendored copy and patch, licence and provenance, version agreement, script unit tests |
  | Install | `tests/install/` | `specify` 1.1.3 or later | `specify init` in a temporary project, add, re-add, remove; reads `.specify/extensions.yml` and the installed skills |
  | Behaviour | `tests/behaviour/` | `claude`, network, tokens | Drives specify and the grill through `claude -p` with a scripted developer; compares files before and after |
  | Regression | `tests/regression/` | `specify`, `claude` | Installs alongside upstream grill, git, agent-context and know-your-spec; checks ordering, coexistence and removal |

- **Live-agent tests**: use `--model haiku` by default (spec assumption), read the model
  from `GRILL_TEST_MODEL`, and resume one session per scripted answer with
  `claude -p --resume`. They assert on files and on the outcome block's first line,
  never on interview wording. They are a separate command so the fast suite stays
  offline.
- **Alternatives considered**: pytest (a dependency to install) and Bats (awkward for
  driving an agent and comparing files); both offered to the developer and declined.

## R15. Reference feature for upstream equivalence (SC-003)

- **Decision**: `tests/fixtures/reference-feature/` holds a fixed feature description, a
  spec produced from it, and a scripted list of answers. The behaviour test runs
  upstream `speckit.grill.with-docs` v1.0.1 and this extension's standalone grill on
  copies of the same spec with the same answers, then compares: the set of spec
  sections changed (ignoring the label), the number of Clarifications lines, the set of
  knowledge-doc paths created or updated, and the coverage statuses in the report.
- **Rationale**: The spec judges equivalence on structure and recorded content, not
  wording. The scripted answers are chosen so that at least one settles a cross-feature
  term and one passes the three-condition recording gate.
- **Risk**: Two live runs can differ in how many questions they ask. The script answers
  by question topic, not position, and the test compares sets, not sequences. If the
  comparison proves unreliable on Haiku, the spec's assumption allows a more capable
  model for this one test.
- **Found at implementation (T078, 2026-10-11)**: on Haiku the comparison failed twice on
  differences that were the model's own wording or choice of sections (a renamed
  user-story heading; one run also rewrote User Scenarios), not wrapper behaviour. The
  comparison is narrowed to level-2 sections and the test alone runs on `sonnet`
  (override with `GRILL_EQUIVALENCE_MODEL`).

## Open items

None blocking. Two things are deliberately left to implementation and are named in the
plan: the exact wording of the wrapper prompts, and whether the reference-feature
comparison needs a model above Haiku.
