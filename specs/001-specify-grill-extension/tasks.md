---

description: "Task list for the Specify Grill extension"
---

# Tasks: Specify Grill Extension

**Input**: Design documents from `/specs/001-specify-grill-extension/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md, architecture.md

**Tests**: Required. The plan's Verification Plan holds 38 obligations; each has a test task placed before the task that delivers its behaviour.

**Organization**: Tasks are grouped by user story so each story can be implemented and tested on its own.

## Format: `[ID] [P?] [Story] [Label] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story the task belongs to (US1 to US6)
- **[Label]**: `[VO-nnn]` or `[NT: reason]`, as "Verification labels" at the end describes
- Every description names the file it creates or changes

## Path Conventions

The repository root is the extension root (plan.md, Project Structure). Shipped files:
`extension.yml`, `config-template.yml`, `commands/`, `scripts/bash/`, `upstream/`.
Tests live in `tests/<level>/` and are not installed.

Working rules for every task:

- Run tests only through the declared commands: `make test-one T=<selector>`, `make test`,
  `make test-live`, `make test-release`.
- Install and live tests create their project in a temporary directory outside this
  repository, never in this repository's own `.specify/`.
- Live tests assert on files and on the first line of the outcome block, never on
  interview wording. They use `GRILL_TEST_MODEL` (default `haiku`) and set
  `SPECKIT_GRILL_NONINTERACTIVE=0` unless the test is about an unattended run.
- Where a live test of upstream behaviour passes on its first run because the vendored
  interview already delivers it, record a `no-meaningful-red` exception as the process
  rules describe; do not weaken the test to make it fail.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: A project that can be versioned, installed and tested

- [X] T001 [NT: tool upgrade on the developer machine] Upgrade the local Spec Kit CLI to 1.1.3 or later with `uv tool upgrade specify-cli`, confirm with `specify --version`, and record the version found in specs/001-specify-grill-extension/research.md under R11; then read the specify command template that version installs and record under R2 whether it tells the agent to run after-specify hooks in priority order or in the file order of `.specify/extensions.yml`. If it is file order, open a Decision listing T065, T066, T071 and T072 before starting them, because priority alone would then not satisfy FR-009
- [X] T002 [NT: version control setup] Run `git init` on branch `main` at the repository root and create .gitignore covering `__pycache__/`, `*.pyc`, `.DS_Store` and test temporary directories; make no commit unless the developer asks
- [X] T003 [NT: test command definitions with no product behaviour] Create Makefile with targets `test` (unittest discover over tests/structure and tests/install), `test-one` (`python3 -B -m unittest $(T)`), `test-live` (tests/behaviour and tests/regression) and `test-release` (tests/release), each exiting non-zero on any failure
- [X] T004 [P] [NT: test scaffolding] Create the test package skeleton: `__init__.py` files in tests/, tests/structure/, tests/install/, tests/behaviour/, tests/regression/, tests/release/ and tests/support/, plus one trivially passing sanity test in tests/structure/test_sanity.py so `make test` runs before any product file exists
- [X] T005 [P] [NT: packaging exclusions, exercised by the install tests] Create .extensionignore excluding `specs/`, `docs/`, `tests/`, `scripts/dev/`, `.specify/`, `.claude/`, `.agents/`, `skills-lock.json`, `Makefile`, `CONTRIBUTING.md` and `.gitignore`
- [X] T006 [P] [NT: vendoring third-party text unchanged] Vendor upstream v1.0.1: fetch `spec-kit-extension/commands/with-docs.md` and `spec-kit-extension/LICENSE` from `yoshi1220/speckit-grill-me` at tag `v1.0.1` with `gh api` and the raw Accept header, and save them unchanged as upstream/with-docs.v1.0.1.md and upstream/LICENSE.upstream; also save the whole `spec-kit-extension/` directory at that tag, unchanged, as tests/fixtures/upstream-grill/, so that tests install upstream from the repository and `make test` needs no network
- [X] T007 [NT: test helper] Write tests/support/project.py: helpers that create a temporary Spec Kit project (`specify init --integration claude`), install an extension from a path with `specify extension add --dev`, read `.specify/extensions.yml`, list installed skills, and snapshot a directory tree as a path-to-SHA-256 map for before and after comparison
- [X] T008 [NT: test helper] Write tests/support/agent.py: a scripted-developer helper that starts a `claude -p` session in a project with a chosen model and environment, sends one message per turn with `--resume`, returns each turn's text, and extracts the outcome block whose first line starts `GRILL OUTCOME:`
- [X] T009 [P] [NT: test fixtures] Create fixtures: tests/fixtures/specs/ with three prepared feature directories (`ambiguous` with several open points, `settled` with nothing left to settle, `no-status` lacking a Status line), each a spec.md plus checklists/requirements.md; and tests/fixtures/marker-hooks/, a minimal extension whose after_specify, before_clarify and after_clarify commands each append one line to `.marker-log` in the project root

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The manifest, the vendored interview and the two scripts. Every story needs them.

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 [VO-001] Write the failing test in tests/structure/test_manifest.py that reads extension.yml and expects exactly one `after_specify` hook naming `speckit.grill-specify.auto`, with `optional: false`, no `condition` and an integer priority below 10
- [X] T011 [VO-001] Create extension.yml from specs/001-specify-grill-extension/contracts/extension.yml: the `extension` block and the `hooks.after_specify` entry with `optional: false` and `priority: 5`
- [X] T012 [VO-002] Add the failing test to tests/structure/test_manifest.py that expects every command name to start `speckit.grill-specify.`, no aliases, `speckit.grill-specify.with-docs` present, `bash` required, `speckit_version` equal to `>=1.1.3`, and no mention of the upstream extension id as a requirement
- [X] T013 [VO-002] Complete extension.yml with `requires`, `provides.commands`, `provides.scripts`, `provides.config` and `tags`, and create config-template.yml holding a short comment and the single line `grill: "on"`
- [X] T014 [VO-003] Write the failing test in tests/structure/test_upstream_region.py: the text between `<!-- BEGIN UPSTREAM grill v1.0.1 -->` and `<!-- END UPSTREAM -->` in commands/speckit.grill-specify.with-docs.md equals the body of upstream/with-docs.v1.0.1.md (after its frontmatter) with upstream/nested-hooks.patch applied; the vendored file's SHA-256 equals the one in upstream/UPSTREAM.md; the repository has no `preset.yml`, no shipped template named like a core template, and no `serena` in shipped command text outside the upstream region
- [X] T015 [VO-003] Write upstream/nested-hooks.patch: one added paragraph at the top of the section "Extension hooks (same processing as clarify)" saying the section does not apply in a nested run and applies as written in a standalone run (contracts/commands.md)
- [X] T016 [VO-003] Write scripts/dev/sync-upstream.sh, which rebuilds the marked region of commands/speckit.grill-specify.with-docs.md from upstream/with-docs.v1.0.1.md and upstream/nested-hooks.patch and leaves text outside the markers untouched; create the command file with frontmatter, the two markers and the generated region; create upstream/UPSTREAM.md with the upstream repository, version and vendored SHA-256
- [X] T017 [P] [VO-005] Write the failing test in tests/structure/test_grill_context.py for the setting table of contracts/scripts.md: file missing, no `grill:` line, `on`, `strict`, `off`, quoted and upper-case forms, a trailing comment, an unknown value `of`, and an unreadable file, using `SPECKIT_GRILL_CONFIG` to point at each case
- [X] T018 [VO-005] Implement the setting half of scripts/bash/grill-context.sh: `--json` output with `setting`, `setting_source` and `warning`, the textual read and fallback rules of contracts/scripts.md, exit 0 always, Bash 3.2 compatible
- [X] T019 [VO-006] Add the failing test to tests/structure/test_grill_context.py for the interactivity table: switch `1`/`true`/`yes`, switch `0`/`false`/`no`, `CLAUDE_CODE_SESSION_ATTENDED=0`, `CLAUDE_CODE_ENTRYPOINT=sdk-cli`, switch `0` together with the agent indicator, no signal, and an unrecognised switch value
- [X] T020 [VO-006] Implement the interactivity half of scripts/bash/grill-context.sh: `interactive` and `interactive_reason` decided in the order of contracts/scripts.md
- [X] T021 [VO-007] Add the failing test to tests/structure/test_grill_context.py that snapshots a temporary project directory, including a read-only setting file, runs the script in every setting state, and expects an identical snapshot
- [X] T022 [VO-007] Make scripts/bash/grill-context.sh strictly read-only: no temporary files in the project, no writes to the setting file, output on standard output only
- [X] T023 [P] [VO-008] Write the failing test in tests/structure/test_grill_label.py: on a spec with no label, `--state complete`, `--state stopped --open 4` and `--state stopped --open 1` each insert the exact line of contracts/scripts.md directly under `**Status**:` with the header's blank-line spacing, change no other byte, and give the same file when repeated
- [X] T024 [VO-008] Implement scripts/bash/grill-label.sh insertion: argument parsing for `--spec`, `--state`, `--open`, `--date`, the two label forms with singular wording, an atomic write, and printing the label line, Bash 3.2 compatible
- [X] T025 [VO-009] Add the failing test to tests/structure/test_grill_label.py: a spec with an existing label gets it replaced in place with the new date and state and holds exactly one label; tests/fixtures/specs/no-status gives exit 3 and an unchanged file; missing or contradictory arguments give exit 2 and an unchanged file
- [X] T026 [VO-009] Implement replacement and failure handling in scripts/bash/grill-label.sh: replace an existing `**Grilled on**:` line, exit 2 on bad arguments, exit 3 when the spec is missing, unwritable or has no Status line, writing nothing in either case, Bash 3.2 compatible
- [X] T027 [VO-011] Write the failing test in tests/install/test_install.py: every command, script and config template file that extension.yml declares exists in the package; after `specify extension add --dev` into a fresh project, `.specify/extensions/grill-specify/grill-specify-config.yml` exists and the installed context script reports `on`; after adding again with `--force`, `.specify/extensions.yml` still has exactly one `after_specify` entry for `grill-specify`
- [X] T028 [VO-011] Create commands/speckit.grill-specify.auto.md as a minimal valid command (frontmatter and a one-line body) so the package installs, and correct extension.yml, config-template.yml or .extensionignore until install and reinstall behave as the test requires

**Checkpoint**: `make test` passes. The package installs and the scripts are complete.

---

## Phase 3: User Story 1 - Grill starts automatically after specify (Priority: P1) 🎯 MVP

**Goal**: Running specify starts the grill in the same session; the interview saves each answer, records terms and decisions, and ends with a completed outcome in specify's report.

**Independent Test**: In a fresh project with only this extension, run specify, answer the interview, confirm satisfaction, and check the automatic start, the Clarifications section, the label and the outcome block.

- [X] T029 [US1] [VO-015] Write the failing live test in tests/behaviour/test_nested_start.py: in a fresh project with only this extension, one specify turn ends at the grill's opening with a point count and one question, no permission request and no second command; at that moment the spec has no `## Clarifications` and no label, and no knowledge-docs directory exists
- [X] T030 [US1] [VO-015] Write commands/speckit.grill-specify.auto.md per contracts/commands.md: invoke `__SPECKIT_COMMAND_GRILL_SPECIFY_WITH_DOCS__` with `--nested` in the same session, wait, carry the outcome block into specify's Completion Report unchanged, ask nothing itself and invoke no specify hook
- [X] T031 [US1] [VO-015] Write the wrapper's opening in commands/speckit.grill-specify.with-docs.md, above the upstream region: decide nested or standalone from `--nested`, run `scripts/bash/grill-context.sh --json` once, run upstream's Prerequisites, Step 1 and Step 2 without writing any file while holding Step 4B facts until the first answer, then state the point count and present the first question, adding the skip choice only for a nested run with setting `on`
- [X] T032 [US1] [VO-016] Write the failing live test in tests/behaviour/test_interview_saves.py: starting the nested grill on tests/fixtures/specs/ambiguous through the entry point, after each of three scripted answers the spec holds one more Clarifications line by the time the next question is presented, and carries the label in its stopped-early form `**Grilled on**: <today> (stopped early, N points open)`
- [X] T033 [US1] [VO-017] Write the failing live test in tests/behaviour/test_knowledge_docs.py (a separate file, so the fingerprint of T032's test file is unchanged between its Red and Green runs): scripted answers settle one term used beyond the feature, one decision meeting all three recording conditions and one decision failing a condition; expect the term defined exactly once in the context file and exactly one decision record, for the qualifying decision
- [X] T034 [US1] [VO-016] [VO-017] Write the wrapper's during-interview rules in commands/speckit.grill-specify.with-docs.md, below the upstream region: after each answer saved by upstream Step 4A write the held Step 4B facts if any, then run `scripts/bash/grill-label.sh --state stopped --open <n>`; never alter upstream's save, knowledge-doc or recording-gate rules; write only the spec, checklist checkbox states and resolved knowledge docs
- [X] T035 [US1] [VO-018] Write the failing live test in tests/behaviour/test_completion.py: a nested interview answered to the end and confirmed leaves the plain label `**Grilled on**: <today>`, a revalidated checklist, and an outcome block reading `GRILL OUTCOME: completed` with `Coverage`, `Knowledge docs changed` and `Checklist` fields
- [X] T036 [US1] [VO-018] Write the wrapper's completion rules in commands/speckit.grill-specify.with-docs.md: at upstream's Step 6 on "Finish and proceed" run `scripts/bash/grill-label.sh --state complete`, let Step 7 revalidate the checklist, and in a nested run end with the outcome block of contracts/outcome-report.md for `completed` instead of upstream's Step 8 report
- [X] T037 [US1] [VO-031] Add the failing live test to tests/behaviour/test_completion.py: after a completed nested run that settled a term and a decision, the changed paths are only the spec, checklists/requirements.md and files under the knowledge-docs location; the checklist differs only in checkbox markers; the setting file and every other file are byte-for-byte unchanged
- [X] T038 [US1] [VO-031] Tighten the write boundary in the wrapper of commands/speckit.grill-specify.with-docs.md: state the three permitted write targets once, forbid touching the grill setting file, plans, tasks and code, and remove any wrapper step found to write elsewhere
- [X] T039 [US1] [VO-030] Write the failing live test in tests/behaviour/test_nothing_to_settle.py: the nested grill on tests/fixtures/specs/settled says it found nothing, asks only the satisfaction question, and on confirmation writes the plain label and reports `completed`; a standalone run on the result leaves every byte of the spec unchanged except the label line; with no setting chosen, the nested opening still offers the skip choice
- [X] T040 [US1] [VO-030] Write the nothing-to-settle rule in the wrapper of commands/speckit.grill-specify.with-docs.md: when the scan finds no point to settle, say so, go straight to upstream's satisfaction gate, and on confirmation label and report as completed; in a nested run with setting `on` the skip choice is still offered at that opening
- [X] T041 [US1] [VO-033] Write the failing live test in tests/behaviour/test_persistence_failure.py: with the knowledge-docs directory made read-only, an answer that settles a cross-feature term is not reported as resolved, the failure is stated in the transcript and in the report, and no knowledge doc appears anywhere else in the project
- [X] T042 [US1] [VO-033] Make the wrapper in commands/speckit.grill-specify.with-docs.md defer to upstream's Persistence failure handling: on Persistence incomplete do not print a `completed` outcome; in a nested run report `stopped early` with the failed point, the files saved and the recovery step

**Checkpoint**: User Story 1 works on its own. Run `make test-live` as the phase checkpoint.

---

## Phase 4: User Story 2 - Project-level grill setting: on, strict or off (Priority: P2)

**Goal**: One line in the setting file decides whether the grill starts and whether it offers a skip choice.

**Independent Test**: Start the nested grill on the same prepared spec at each setting value and at a bad value. The default case (no setting chosen, skip choice offered, no warning) is verified with User Story 3 by VO-019.

- [X] T043 [US2] [VO-020] Write the failing live test in tests/behaviour/test_setting.py: with `grill: "strict"` the nested grill on tests/fixtures/specs/ambiguous opens with a point count and a question and offers no skip choice
- [X] T044 [US2] [VO-020] Write the strict rule in the wrapper of commands/speckit.grill-specify.with-docs.md: with setting `strict` the opening carries no skip choice, and a later request to stop is still honoured
- [X] T045 [US2] [VO-021] Add the failing live test to tests/behaviour/test_setting.py: with `grill: "off"` the nested grill asks nothing, the project tree snapshot is identical before and after, and the outcome block reads `GRILL OUTCOME: switched off`
- [X] T046 [US2] [VO-021] Write the off rule in the wrapper of commands/speckit.grill-specify.with-docs.md: in a nested run with setting `off`, read nothing further, change nothing and end with the `switched off` outcome block
- [X] T047 [US2] [VO-022] Add the failing live test to tests/behaviour/test_setting.py: with `grill: "of"` the nested grill opens with a skip choice, and after skipping the outcome block has a `Warning` line naming `of`
- [X] T048 [US2] [VO-022] Write the warning rule in the wrapper of commands/speckit.grill-specify.with-docs.md: when the run context's `warning` is not empty, repeat it as the one-line `Warning` field of the outcome block, or in the standalone completion report

**Checkpoint**: The three setting values and the bad-value fallback behave as specified.

---

## Phase 5: User Story 3 - Skip a simple spec (Priority: P2)

**Goal**: With the setting on, the developer can skip at the opening and the spec stays exactly as specify left it.

**Independent Test**: With no setting chosen, start the nested grill, take the skip choice, and compare the project tree before and after.

- [X] T049 [US3] [VO-019] Write the failing live test in tests/behaviour/test_skip.py: with the setting file's `grill:` line removed, the nested grill on tests/fixtures/specs/ambiguous opens with a skip choice and no warning; after the developer skips, the project tree snapshot is identical to the one taken before the grill started, the spec has no label, and the outcome block reads `GRILL OUTCOME: skipped` with `Reason` and `Resume with` fields
- [X] T050 [US3] [VO-019] Write the skip rule in the wrapper of commands/speckit.grill-specify.with-docs.md: on the skip choice change no file, discard the held Step 4B facts, and end with the `skipped` outcome block naming the standalone command to run later

**Checkpoint**: A skipped spec is byte-for-byte what specify produced.

---

## Phase 6: User Story 4 - Stop partway and resume later (Priority: P2)

**Goal**: Stopping keeps every settled answer and labels the spec truthfully; the standalone command resumes from the open points; stopping ends only the grill.

**Independent Test**: Start the interview, answer some questions, say "stop", check the spec and report, then run the standalone command and confirm it asks only about open points.

- [X] T051 [US4] [VO-023] Write the failing live test in tests/behaviour/test_stop_resume.py: a nested interview stopped after two answers asks no further question, keeps both Clarifications lines, carries `**Grilled on**: <today> (stopped early, N points open)`, and ends with `GRILL OUTCOME: stopped early` listing `Outstanding points` with reasons and a `Resume with` field
- [X] T052 [US4] [VO-023] Write the stopped-early rules in the wrapper of commands/speckit.grill-specify.with-docs.md: on upstream's Interrupted completion path, or option 3 of the satisfaction gate, refresh the label with the final open count and, in a nested run, end with the `stopped early` outcome block
- [X] T053 [US4] [VO-029] Add the failing live test to tests/behaviour/test_stop_resume.py: with setting `strict`, and again with setting `on` where the skip choice is offered and not taken, saying stop at the opening before any answer gives `GRILL OUTCOME: stopped early` (not `skipped`) with every point outstanding, `Label: none`, and an identical project tree snapshot
- [X] T054 [US4] [VO-029] Write the stop-before-first-answer rule in the wrapper of commands/speckit.grill-specify.with-docs.md: change no file, write no label, discard held facts, and report `stopped early` with `Questions answered: 0`, never `skipped`, at every setting including `on`
- [X] T055 [US4] [VO-024] Add the failing live test to tests/behaviour/test_stop_resume.py: the standalone grill run on the spec left by a stopped interview states the open-point count, re-asks no question already in Clarifications (no Clarifications question recorded before the resume appears twice afterwards), and when answered to the end leaves the plain label
- [X] T056 [US4] [VO-024] Write the resume rule in the wrapper of commands/speckit.grill-specify.with-docs.md: on a spec with a label or a Clarifications section, treat what Clarifications and the knowledge docs settle as settled, open with the count of points still open, and replace the label on completion
- [X] T057 [P] [US4] [VO-025] Write the failing live test in tests/behaviour/test_standalone.py: the standalone grill on tests/fixtures/specs/ambiguous runs the interview with the setting at `off` and again at `on`, and both openings state the point count and offer no skip choice
- [X] T058 [US4] [VO-025] Write the standalone rules in the wrapper of commands/speckit.grill-specify.with-docs.md: without `--nested` ignore the grill setting, never offer a skip choice, and finish with upstream's Step 8 completion report plus the label line
- [X] T059 [US4] [VO-026] Write the failing live test in tests/behaviour/test_nested_hooks.py: with tests/fixtures/marker-hooks installed, a specify run whose nested grill is stopped early leaves `.marker-log` holding the after_specify marker written after the grill ended, no before_clarify or after_clarify marker, and no second run of any specify hook
- [X] T060 [US4] [VO-026] Write the nested hook rules in commands/speckit.grill-specify.with-docs.md and commands/speckit.grill-specify.auto.md: a nested run processes no clarify hook on the normal or interrupted path and no specify hook, and after the outcome block control returns to specify so its remaining after-specify hooks run
- [X] T061 [US4] [VO-027] Add the failing live test to tests/behaviour/test_standalone.py: with tests/fixtures/marker-hooks installed, a standalone grill run to completion leaves `.marker-log` holding the before_clarify marker written before the first question and the after_clarify marker written before the completion report
- [X] T062 [US4] [VO-027] Confirm the standalone hook path in commands/speckit.grill-specify.with-docs.md: the wrapper adds nothing that suppresses upstream's clarify-hook section in a standalone run, and the nested-run paragraph from upstream/nested-hooks.patch is worded so it cannot be read as applying to a standalone run

**Checkpoint**: Stop, resume and standalone runs work. Run `make test-live` as the phase checkpoint.

---

## Phase 7: User Story 5 - No human present (Priority: P2)

**Goal**: An unattended specify run is never blocked and never gets invented answers.

**Independent Test**: Start the nested grill unattended at each setting and confirm it returns at once, changes nothing and reports that it was not run.

- [X] T063 [US5] [VO-028] Write the failing live test in tests/behaviour/test_unattended.py: at each of `on`, `strict` and `off`, once with `SPECKIT_GRILL_NONINTERACTIVE=1` and once with the switch unset under `claude -p`, the nested grill returns in a single turn with no question, the project tree snapshot is identical, and the outcome block reads `GRILL OUTCOME: not run (no human present)` with a `Reason` naming the signal and saying the spec has not been clarified
- [X] T064 [US5] [VO-028] Write the non-interactive rule in the wrapper of commands/speckit.grill-specify.with-docs.md: when the run context's `interactive` is false, before consulting the setting and before any scan, ask nothing, change nothing and end with the `not run (no human present)` outcome block; apply the same exit to a standalone run

**Checkpoint**: Unattended runs complete without waiting at every setting.

---

## Phase 8: User Story 6 - Coexist with the upstream grill and other extensions (Priority: P3)

**Goal**: The extension installs beside upstream grill and other after-specify extensions, runs first, and removes cleanly.

**Independent Test**: Install upstream grill, this extension and other after-specify extensions; confirm all commands remain, the grill is ordered first, and removal leaves everything else in place.

- [ ] T065 [P] [US6] [VO-010] Write the failing test in tests/install/test_ordering.py: with this extension and the Comprehension Checkpoint extension (copied from .specify/extensions/know-your-spec) installed in both orders, `.specify/extensions.yml` has one `after_specify` entry for `grill-specify`, and the hooks that the installed Spec Kit CLI's own hook resolution returns for `after_specify` list the grill first. The order is taken from the CLI (`get_hooks_for_event`, called with the CLI's own Python interpreter through a helper in tests/support/project.py), never from a sort written in the test
- [ ] T066 [US6] [VO-010] Correct the hook entry in extension.yml until the ordering test passes in both install orders, and write the "Hook ordering" section of README.md: the grill registers at priority 5, the default is 10, and what to do when another extension also claims an early position
- [X] T067 [P] [US6] [VO-012] Write the failing test in tests/install/test_remove.py: in a project with this extension, the marker-hooks extension, a spec carrying a label and Clarifications, and a knowledge-docs directory, `specify extension remove grill-specify` leaves no `grill-specify` hook entry and no `speckit-grill-specify-*` skill, leaves the marker extension's entries unchanged, and leaves the spec and knowledge docs byte-for-byte unchanged
- [X] T068 [US6] [VO-012] Make removal clean: ensure extension.yml declares every installed file so the CLI removes it, that nothing is installed outside `.specify/extensions/grill-specify/` and the agent's command directory, and document removal in README.md
- [X] T069 [P] [US6] [VO-013] Write the failing test in tests/install/test_coexist.py: installing the upstream `grill` extension (from tests/fixtures/upstream-grill/ with `specify extension add --dev`, never by download) and this extension in both orders succeeds, every command of both is present, and upstream's installed command files have the same SHA-256 as when upstream is installed alone
- [X] T070 [US6] [VO-013] Resolve any install conflict the coexistence test exposes in extension.yml (command names, aliases, script and config names) and add a "Using alongside upstream grill" section to README.md
- [ ] T071 [US6] [VO-035] Write the failing live test in tests/regression/test_with_other_extensions.py: with the Comprehension Checkpoint extension installed first, then the bundled git and agent-context extensions, then this extension last, a specify run grills before the Comprehension Checkpoint, before the agent-context refresh and before the commit prompt, and removing this extension leaves their registrations unchanged
- [ ] T072 [US6] [VO-035] Correct the hook entry in extension.yml or the hand-back to specify in commands/speckit.grill-specify.auto.md until the live ordering test passes; if the order already holds on the test's first run, record a `no-meaningful-red` exception as the process rules describe

**Checkpoint**: All six user stories work. Run `make test` and `make test-live`.

---

## Phase 9: Release, Polish & Cross-Cutting Concerns

**Purpose**: Provenance, licence, documentation, the cross-cutting guarantees and the first public release

- [X] T073 [VO-004] Write the failing test in tests/structure/test_provenance.py: upstream/UPSTREAM.md names the upstream repository, `v1.0.1`, the Spec Kit release verified with its date, and has an "Updating from upstream" procedure; upstream/LICENSE.upstream equals upstream's notice; LICENSE is the MIT licence; the version in extension.yml equals the latest heading in CHANGELOG.md and the tag in README.md's archive URL
- [X] T074 [VO-004] Complete upstream/UPSTREAM.md with the update procedure (fetch the new tag, replace the vendored file and tests/fixtures/upstream-grill/, re-apply or revise the patch, run scripts/dev/sync-upstream.sh, run `make test`) and create LICENSE (MIT, this project's notice) and CHANGELOG.md with a `0.1.0` entry
- [X] T075 [VO-004] Write README.md: what the extension does, install by local path and by tag-archive URL for `v0.1.0`, the grill setting and its three values, the five outcomes, the grilled-on label, the `SPECKIT_GRILL_NONINTERACTIVE` switch, nested and standalone clarify-hook behaviour, and attribution to upstream
- [X] T076 [P] [NT: contributor documentation] Write CONTRIBUTING.md: prerequisites, the four `make` commands and what each level covers, the rule that live tests use Haiku unless `GRILL_TEST_MODEL` is set, and the release steps
- [X] T077 [VO-032] Write the failing live test in tests/behaviour/test_equivalence.py with tests/fixtures/reference-feature/ (a fixed spec and a scripted answer list keyed by topic): grill one copy with upstream `speckit.grill.with-docs` v1.0.1 (installed from tests/fixtures/upstream-grill/) and one with this extension's standalone grill, and expect the same set of changed spec sections apart from the label, the same number of Clarifications lines, the same knowledge-doc paths and the same coverage statuses
- [ ] T078 [VO-032] Remove any difference the equivalence test exposes by correcting the wrapper in commands/speckit.grill-specify.with-docs.md, never the upstream region; if Haiku proves too unreliable for this comparison, set the model for this test alone and record the reason in specs/001-specify-grill-extension/research.md under R15
- [X] T079 [VO-034] Write the failing test in tests/regression/test_user_level_isolation.py: the shipped files install nothing outside the project and the command text names no user-level skill, agent or subagent; with `CLAUDE_CONFIG_DIR` pointing at a directory holding only credentials, the nested and standalone grills both reach their opening
- [X] T080 [VO-034] Remove any dependency the isolation test exposes from commands/speckit.grill-specify.with-docs.md and commands/speckit.grill-specify.auto.md, and state in README.md that the extension needs only project-level installation
- [X] T081 [VO-036] Write the failing live test in tests/behaviour/test_open_markers.py, with a new fixture tests/fixtures/specs/markers (a spec.md holding one `[NEEDS CLARIFICATION: ...]` marker and a checklists/requirements.md with one unchecked item): the nested grill opens with a question rather than stopping or refusing, and after the scripted answers and confirmation the spec holds no `[NEEDS CLARIFICATION` text and its Clarifications section records the answer
- [X] T082 [VO-036] Write the open-marker rule in the wrapper of commands/speckit.grill-specify.with-docs.md: markers and failed checklist items left by specify are counted among the points to settle and never stop the grill; if upstream's scan already delivers this and the test passes on its first run, add nothing and record a `no-meaningful-red` exception
- [X] T083 [VO-037] Write the failing live test in tests/regression/test_cross_grill.py: with the upstream `grill` extension (installed from tests/fixtures/upstream-grill/) and this extension both installed, a spec completed by this extension's standalone grill is then grilled with upstream's `speckit.grill.with-docs`, and a spec completed by upstream's command is then grilled with this extension's standalone grill; in both directions no question recorded in Clarifications by the first run is recorded again, every earlier Clarifications line is unchanged, and the spec holds exactly one `**Grilled on**:` line, directly under Status
- [X] T084 [VO-037] Correct the resume rule or the label handling in the wrapper of commands/speckit.grill-specify.with-docs.md, never the upstream region, until the cross-grill test passes in both directions; if it passes on its first run, record a `no-meaningful-red` exception
- [X] T085 [VO-038] Write the failing test in tests/structure/test_bash32.py: no file under scripts/bash/ uses a construct that Bash 3.2 lacks (`declare -A` or `local -A`, `mapfile`, `readarray`, `coproc`, `${var,,}` or `${var^^}` case conversion, `|&`, `&>>`, `[[ -v`, a negative array index, `printf '%(...)T'`, `read -i`); and when `GRILL_TEST_BASH` names a Bash binary, the cases of tests/structure/test_grill_context.py and tests/structure/test_grill_label.py pass with the scripts run through that binary. With `GRILL_TEST_BASH` unset the second part is reported as skipped, never as passed
- [X] T086 [VO-038] Replace any construct the test names in scripts/bash/grill-context.sh and scripts/bash/grill-label.sh, make the two script test files run the scripts through the interpreter `GRILL_TEST_BASH` names (default `bash`), and describe the variable in CONTRIBUTING.md; if the test passes on its first run, record a `no-meaningful-red` exception
- [ ] T087 [NT: manual check in an environment that cannot be reproduced locally] Ask the developer to run quickstart step 8 in the locked-down devcontainer and record the result and date in specs/001-specify-grill-extension/research.md under R12; do not start the release tasks until this result is recorded as passing
- [X] T088 [VO-014] Write the failing test in tests/release/test_release_install.py: installing with `specify extension add --dev <repo>` and with `--from https://github.com/leejsinclair/speckit-grill-specify/archive/refs/tags/v<version>.zip` (version read from extension.yml) into two fresh projects yields the same command list, the same single `after_specify` registration, and installed upstream/UPSTREAM.md and upstream/LICENSE.upstream in both
- [ ] T089 [VO-014] Publish the first release, only on the developer's explicit instruction at each step: make the initial commit, create the public repository `leejsinclair/speckit-grill-specify` with `gh repo create`, push `main`, tag `v0.1.0` and push the tag; then run `make test-release` against extension.yml's version
- [ ] T090 [NT: manual validation of documentation] Run every scenario in specs/001-specify-grill-extension/quickstart.md in a throwaway project and correct README.md or the quickstart where they disagree with what is observed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies. T001 must finish before any install test runs.
- **Foundational (Phase 2)**: Depends on Setup. Blocks every user story.
- **User Story 1 (Phase 3)**: Depends on Foundational. Builds the entry point and the wrapper's opening that every later story extends.
- **User Stories 2 to 5 (Phases 4 to 7)**: Each depends on User Story 1's opening (T029 to T031). They are independent of one another in behaviour but all edit `commands/speckit.grill-specify.with-docs.md`, so their behaviour tasks are done one at a time.
- **User Story 6 (Phase 8)**: T065 to T070 depend on Foundational only; T071 and T072 also need User Story 1.
- **Release and polish (Phase 9)**: Depends on all stories. T089 depends on T088, on a passing result recorded by T087 (the devcontainer check) and on the developer's instruction.

### Within Each User Story

- Each test task comes first and must be recorded as failing before its behaviour task starts.
- Behaviour tasks that edit the same command file are sequential.
- Three obligations are delivered by a pair of behaviour tasks, and the test passes only when both are done: T015 with T016 (VO-003), T030 with T031 (VO-015), T074 with T075 (VO-004). Record the Green run after the second task of the pair and mark both complete then.
- Run `make test` at the end of every phase, and `make test-live` as a checkpoint at the end of Phases 3, 6 and 8.

### Parallel Opportunities

- Setup: T004, T005, T006 and T009 touch different files.
- Foundational: the context-script chain (T017 to T022) and the label-script chain (T023 to T026) are independent of each other and of the manifest chain (T010 to T016).
- User Story 6: T065, T067 and T069 are separate test files.
- Test files for different stories can be written in parallel; the wrapper edits cannot.

---

## Parallel Example: Foundational

```bash
# Two developers, or two sessions:
Task: "T017 to T022 - grill-context.sh and its tests in tests/structure/test_grill_context.py"
Task: "T023 to T026 - grill-label.sh and its tests in tests/structure/test_grill_label.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **Stop and validate**: run quickstart steps 2 and 3 in a throwaway project
5. The extension is usable from a local install at this point, with the default setting only

### Incremental Delivery

1. Setup and Foundational: the package installs and the scripts pass
2. User Story 1: the grill starts by itself and completes (MVP)
3. User Stories 2 and 3: the setting and the skip choice
4. User Story 4: stop, resume and standalone
5. User Story 5: unattended runs
6. User Story 6: coexistence, ordering and removal
7. Phase 9: provenance, documentation, equivalence with upstream and the first release

---

## Notes

- [P] tasks touch different files and have no unfinished dependency
- Live tests cost tokens: run the single test with `make test-one` while working, and the whole live suite only at checkpoints
- Never edit text between the upstream markers by hand; change `upstream/nested-hooks.patch` and run `scripts/dev/sync-upstream.sh`
- Commit, push, tag and create the repository only when the developer asks


## Verification labels

<!--
  Added by the Integrated TDD preset. These conventions apply to every task above.
  Keep this section in the generated tasks.md so a reviewer can read the labels.
-->

Every task carries a verification label, placed after the story label and before the
description. The rest of the task line is unchanged.

| Label | Meaning |
|-------|---------|
| `[VO-nnn]` | The task satisfies this obligation from the plan's Verification Plan. Repeat the label for several obligations |
| `[NT: reason]` | The task has no behaviour to verify. The reason is required |

```markdown
- [ ] T011 [P] [US1] [VO-001] Write the failing test for an empty cart total in tests/test_cart.py
- [ ] T012 [US1] [VO-001] Implement the cart total in src/cart.py
- [ ] T013 [US1] [NT: README wording only] Document the cart total in README.md
```

A task's kind follows from its labels and its position in this file:

| Kind | Rule |
|------|------|
| `no-test` | Carries `[NT: reason]` and no `[VO-nnn]` |
| `test` | The first task in the file to name a given obligation |
| `behaviour` | Any later task naming that obligation |

- Test tasks are required for every task that delivers behaviour. They are not optional.
- Every obligation needs a `test` task and at least one `behaviour` task, so it is named
  by at least two tasks.
- The first task to name an obligation is its test task whatever its description says, so
  the test task must be written first: the task that writes the failing test comes before
  the task that implements the behaviour.
- A task naming several obligations is a `test` task only when it is the first to name
  all of them.
