# Implementation Plan: Specify Grill Extension

**Branch**: `001-specify-grill-extension` | **Date**: 2026-10-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-specify-grill-extension/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Build a Spec Kit extension, id `grill-specify`, that grills every new spec straight after
specify. It registers one mandatory `after_specify` hook at priority 5, ahead of the
default, whose entry-point command starts the grill as a nested run. The grill command
carries upstream `speckit.grill.with-docs` v1.0.1 verbatim between markers, inside a
wrapper that adds the grill setting (on, strict, off), the opening and its skip choice,
the non-interactive exit, the nested-run hook rule, the grilled-on label and the outcome
block for specify's report. Two small Bash scripts decide what can be decided
mechanically: the run context and the label. The extension is released under MIT from
`github.com/leejsinclair/speckit-grill-specify`, installable from a local directory or by
tag-archive URL.

## Technical Context

**Language/Version**: Markdown agent commands (Spec Kit extension schema 1.0); Bash for
the two shipped scripts, written to run on the Bash 3.2 that macOS ships; Python 3.9 or
later for tests only

**Primary Dependencies**: Spec Kit CLI 1.1.3 or later; an AI coding agent integration
(Claude Code is the tested one); upstream `yoshi1220/speckit-grill-me` v1.0.1, vendored,
not installed

**Storage**: Files in the installing project only: the grill setting file, the active
spec and its requirements checklist, and the knowledge docs. No database and no progress
file

**Testing**: Python `unittest` (standard library), run through `make`; live-agent tests
drive `claude -p` with Haiku by default

**Target Platform**: macOS and Linux with Bash; Windows and PowerShell unsupported,
matching upstream

**Project Type**: Spec Kit extension: a package of agent commands, scripts and a manifest,
with no build step

**Performance Goals**: None stated in the spec. The scripts are single-pass text
operations; interview length is set by the developer

**Constraints**: Upstream text verbatim apart from one recorded change (FR-022); writes
limited to spec, checklist checkboxes and knowledge docs (FR-008); no core template
overrides and no change to the interview algorithm (FR-020); no hook `condition`
(FR-005); nothing at user level and no subagent (FR-019); a spec the grill did not touch
stays byte-for-byte as specify left it (SC-002)

**Scale/Scope**: 2 commands, 2 scripts, 1 config template, 1 hook; about 480 vendored
lines and an estimated 150 lines of wrapper; four test levels

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Checked against constitution 1.0.0, ratified 2026-10-11. The constitution was ratified
after this plan's research and design, by promoting this feature's own constraints, so
both columns record the same evaluation, made on 2026-10-11.

| Gate | Before research | After design |
|------|-----------------|--------------|
| I. Upstream Fidelity | Pass | Pass: upstream v1.0.1 is carried verbatim between markers, the one change is `upstream/nested-hooks.patch`, and provenance ships in `upstream/UPSTREAM.md` (FR-004, FR-020, FR-022; VO-003, VO-004) |
| II. Narrow Write Boundary | Pass | Pass: writes are limited to the spec, checklist checkbox states and knowledge docs, and nothing is written before the first answer (FR-008, FR-011, SC-002; VO-007, VO-015, VO-031) |
| III. Test-First with Recorded Evidence | Pass | Pass: the Verification Plan below holds an obligation for every requirement and acceptance scenario, and the one manual check is recorded as an exemption |
| IV. Self-Contained and Non-Invasive | Pass | Pass: no core template override, no dependency on upstream being installed, nothing at user level and no subagent; removal leaves produced documents in place (FR-010, FR-016, FR-017, FR-019, FR-020; VO-012, VO-013, VO-034) |
| V. Never Block, Never Invent | Pass | Pass: an unattended run exits without asking or writing, on explicit signals only, and every run ends with one stated outcome (FR-007, FR-014; VO-006, VO-028) |
| Platform and licence | Pass | Pass: MIT with upstream's notice, macOS and Linux, scripts checked for Bash 3.2 (FR-018, FR-025; VO-004, VO-038) |

No violation to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-specify-grill-extension/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── architecture.md      # Phase 1 output (/speckit-plan command, c4 extension)
├── contracts/           # Phase 1 output (/speckit-plan command)
│   ├── extension.yml        # Design copy of the manifest
│   ├── commands.md          # The two commands and the wrapper's rules
│   ├── scripts.md           # grill-context.sh and grill-label.sh
│   └── outcome-report.md    # The outcome block
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
extension.yml                        # Manifest: 2 commands, 2 scripts, config, after_specify hook
config-template.yml                  # Installed as grill-specify-config.yml; one line: grill: "on"
commands/
├── speckit.grill-specify.auto.md        # Hook entry point: nested run
└── speckit.grill-specify.with-docs.md   # Wrapper around the marked upstream region
scripts/
├── bash/
│   ├── grill-context.sh             # Setting and non-interactive signals to JSON; read-only
│   └── grill-label.sh               # Writes or refreshes the grilled-on label
└── dev/
    └── sync-upstream.sh             # Rebuilds the upstream region; not installed
upstream/
├── with-docs.v1.0.1.md              # Pristine vendored copy
├── nested-hooks.patch               # The one recorded change
├── LICENSE.upstream                 # Upstream's MIT notice
└── UPSTREAM.md                      # Provenance record and update procedure
tests/                               # Not installed
├── structure/                       # Manifest, upstream region, licence, versions, script unit tests
├── install/                         # specify init, add, re-add, remove in a temporary project
├── behaviour/                       # Live agent: nested and standalone scenarios
├── regression/                      # Live agent: with upstream grill, git, agent-context, know-your-spec
├── release/                         # Install from the published tag archive
├── fixtures/                        # Reference feature, sample specs, marker-hook extension
└── support/                         # Temporary-project and scripted-developer helpers
Makefile                             # test, test-one, test-live, test-release
README.md
CHANGELOG.md
CONTRIBUTING.md
LICENSE                              # MIT
.extensionignore                     # Keeps specs/, docs/, tests/, scripts/dev/ and tooling out of installs
.gitignore
docs/domain_knowledge/               # Existing: this project's own glossary and decision records
specs/                               # Existing: Spec Kit feature directories
```

**Structure Decision**: The repository root is the extension root, as in the sibling `c4`
and `know-your-spec` extensions, so a GitHub tag archive installs without a build step
(research R1). Shipped scripts live under `scripts/bash/`, the path Spec Kit rewrites in
command files. Tests are split into directories by the four levels of SC-005 so that the
offline levels run without an agent. The existing `.specify/`, `.claude/`, `.agents/`,
`docs/` and `specs/` directories stay where they are and are excluded from installs.

## Design Notes

Decisions are recorded with their evidence in [research.md](./research.md). The ones that
shape the task list:

- **Nested is an explicit input.** A hook entry cannot carry an argument, so the hook
  points at a short entry-point command that calls the grill with `--nested` (R3).
- **Nothing is written before the first answer.** The wrapper runs upstream's scan and
  fact gate read-only and holds investigated facts until the developer answers (FR-011).
- **The label is written by a script, with the first answer.** It starts in its
  stopped-early form and becomes plain only at the satisfaction gate (R8).
- **Interactivity is checked before the setting**, so an unattended run reports "not run"
  at every setting (R7). `SPECKIT_GRILL_NONINTERACTIVE=0` forces interactive, which the
  live tests need.
- **The local CLI must be upgraded first.** The manifest requires 1.1.3 and this machine
  has 1.0.2.dev0 (R11).
- **Version control and the public repository are part of the work**, and pushing or
  tagging happens only on the developer's instruction (R13).

Left to implementation: the exact wording of the wrapper prompts, and whether the
upstream-equivalence test needs a model above Haiku (R15).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations of constitution 1.0.0.


## Verification Plan

<!--
  Added by the Integrated TDD preset and filled by the plan stage as a Phase 1 output.
  The heading text, the three sub-headings and the three header rows are fixed: a check
  script reads them. Replace the example rows. This section holds no status: what is
  verified is derived from the evidence in tdd-evidence.md, never written here.
-->

### Verification commands

<!--
  The ways this project already runs its tests, taken from what the project defines
  (package scripts, a Makefile, CI configuration, contributor documentation).
  ID: short, lowercase letters, digits and hyphens. Command: in backticks, with at most
  one {select} where a test selector goes. Scope: focused (run per increment) or broad
  (run at checkpoints). Source: where the project defines the command.
  If the project has no runnable test command, leave the table empty and raise the gap.
-->

| ID | Command | Scope | Source |
|----|---------|-------|--------|
| one | `make test-one T={select}` | focused | `Makefile`, created by this feature's setup task; runner chosen by the developer on 2026-10-11 (research R14) |
| fast | `make test` | broad | `Makefile`, as above: structure and install levels, no agent |
| live | `make test-live` | broad | `Makefile`, as above: behaviour and regression levels, drives Claude Code |
| release | `make test-release` | broad | `Makefile`, as above: install from the published tag archive |

### Verification obligations

<!--
  One row per scenario that must be verified. ID: VO- and three digits, numbered in
  order of creation and never reused. Requirements: the FR-, SC- and acceptance scenario
  ids (USn-ASm, scenario m of user story n) from spec.md that the row verifies, with
  DC-nn for a design constraint and EC-nn for an edge case, each stated in the Scenario
  cell. Expected outcome: what must be observed, stated without reference to how the code
  will be written. Level: unit, integration, contract, end-to-end or other. Origin:
  planned, or discovered when added during implementation.
-->

| ID | Requirements | Scenario | Expected outcome | Level | Origin |
|----|--------------|----------|------------------|-------|--------|
| VO-001 | FR-001, FR-005, FR-009, FR-011 | The manifest's hook declaration is read | Exactly one `after_specify` hook, naming the entry-point command, mandatory, with no condition, and a priority lower than the default of 10 | contract | planned |
| VO-002 | FR-002, FR-016, FR-017, FR-018 | The manifest's commands and requirements are read | Every command is in the `speckit.grill-specify` namespace with no alias; `speckit.grill-specify.with-docs` is present; nothing names or requires the upstream extension; Bash is required; the minimum Spec Kit version is 1.1.3 | contract | planned |
| VO-003 | FR-003, FR-020, FR-022 | The marked upstream region of the grill command is compared with the vendored v1.0.1 copy | The region equals the vendored body with only the recorded hook-rule change applied; the vendored file's hash equals the one in the provenance record; the package contains no preset, no template named like a core template and no Serena variant | contract | planned |
| VO-004 | FR-004, FR-025 | The provenance record, licence files, changelog and README are read | The record names upstream v1.0.1, its repository and an update procedure; upstream's MIT notice is present verbatim; the project licence is MIT; the manifest version, the latest changelog entry and the README's archive URL agree | contract | planned |
| VO-005 | FR-005, FR-012, US2-AS4 | The context script is run against each setting state: file missing, key missing, `on`, `strict`, `off`, quoted and upper-case forms, an unknown value, an unreadable file | Missing gives `on` with no warning; valid values are returned as written; an unknown value or unreadable file gives `on` with a one-line warning that names the bad value | unit | planned |
| VO-006 | FR-007 | The context script is run with each signal combination: switch on, switch off, agent unattended indicator, switch off together with the agent indicator, no signal, an unrecognised switch value | Non-interactive only when the switch says so or the agent indicator says so and the switch does not override; no signal and an unrecognised value are interactive | unit | planned |
| VO-007 | FR-008, DC-01 | DC-01: the context script is read-only. It is run in a project directory whose full contents are recorded before and after | No file is created, changed or removed, including the setting file | unit | planned |
| VO-008 | FR-021 | The label script is run on a spec with no label, for the complete state, the stopped state with several open points and with one | One label line appears directly under Status in the stated form, with singular wording for one point; every other byte of the spec is unchanged; repeating the command changes nothing | unit | planned |
| VO-009 | FR-021, EC-01 | The label script is run on a spec that already has a label, with a new date and state. EC-01: it is run on a spec with no Status line, and with invalid arguments | The existing label is replaced in place and exactly one label remains; with no Status line or invalid arguments it reports failure and the spec is unchanged | unit | planned |
| VO-010 | FR-001, FR-009, US6-AS2 | The extension is installed into a fresh project together with the Comprehension Checkpoint extension, in both install orders | The project has one `after_specify` registration for this extension, and the hooks Spec Kit returns for after-specify list the grill first in both orders | integration | planned |
| VO-011 | FR-005, EC-02 | EC-02: reinstall. The extension is installed, its setting is read, and it is installed again over itself | The setting file exists after the first install and reads `on`; after the reinstall there is still exactly one hook registration | integration | planned |
| VO-012 | FR-010, SC-008, US6-AS3 | A project with this extension, another extension's hook, a grilled spec and knowledge docs has this extension removed | Its registration and its commands are gone; the other extension's registration is unchanged; the spec and knowledge docs are byte-for-byte unchanged | integration | planned |
| VO-013 | FR-016, SC-007, US6-AS1 | The upstream grill extension and this one are installed together, in both orders | Both installs succeed; every command of both extensions is present; upstream's installed command files are byte-for-byte what upstream alone installs | integration | planned |
| VO-014 | FR-025, SC-011 | The extension is installed from the local directory, and from the published tag archive by URL | Both installs yield the same commands and the same single hook registration, and the installed provenance record and licence files are present | end-to-end | planned |
| VO-015 | FR-001, FR-011, FR-017, SC-001, US1-AS1, US1-AS6 | In a fresh project with only this extension and the default setting, specify is run and the session is observed at the grill's opening | The grill opens in the same session with no further command and no request for permission; the opening states a number of points and presents one question; at that moment the spec has no Clarifications section and no label, and no knowledge doc exists | end-to-end | planned |
| VO-016 | FR-003, FR-021, US1-AS2 | A nested interview is answered one question at a time, and the spec is read each time the next question is presented | After each answer the spec holds one more Clarifications line than before, already saved when the next question appears, and carries the label in its stopped-early form with a count of open points | end-to-end | planned |
| VO-017 | FR-003, SC-004, US1-AS3, US1-AS4 | Scripted answers settle a term used beyond the feature, a decision that meets all three recording conditions, and a decision that fails one | The term has exactly one definition in the context file; exactly one decision record exists and it is for the qualifying decision | end-to-end | planned |
| VO-018 | FR-014, FR-021, US1-AS5 | A nested interview is answered to the end and satisfaction is confirmed | The checklist's checkbox states reflect the updated spec; the label is in its plain form; the outcome block reads completed and includes a coverage summary and the knowledge docs changed | end-to-end | planned |
| VO-019 | FR-012, FR-014, SC-002, US2-AS1, US3-AS1, US3-AS2 | On a prepared spec with no setting chosen, the nested grill opens and the developer takes the skip choice | The opening offers a skip choice and shows no warning; after skipping, every file in the project is byte-for-byte as before the grill started and the spec has no label; the outcome block reads skipped and says how to run the grill later | end-to-end | planned |
| VO-020 | FR-012, US2-AS2 | On a prepared spec with the setting at strict, the nested grill opens | The opening states the point count and a question and offers no skip choice | end-to-end | planned |
| VO-021 | FR-012, FR-014, SC-002, US2-AS3 | On a prepared spec with the setting at off, the nested grill is started | No question is asked; every file is byte-for-byte unchanged; the outcome block reads switched off | end-to-end | planned |
| VO-022 | FR-012, US2-AS4 | On a prepared spec with an unknown setting value, the nested grill is started and skipped | The grill opens with a skip choice, and the outcome block carries a one-line warning naming the bad value | end-to-end | planned |
| VO-023 | FR-014, FR-015, FR-021, SC-010, US4-AS1 | A nested interview is stopped after two answers | No further question is asked; both answers remain in the spec; the label is in its stopped-early form with a count of open points; the outcome block reads stopped early, lists each outstanding point with a reason and says how to resume | end-to-end | planned |
| VO-024 | FR-002, FR-015, SC-006, US4-AS2 | The standalone grill is run on the spec left by a stopped interview and answered to the end | Its opening states the open-point count; no Clarifications question recorded before the resume is asked again; the label ends in its plain form with the resume date | end-to-end | planned |
| VO-025 | FR-013, US4-AS3 | The standalone grill is run on a spec never grilled, with the setting at off and again at on | The interview runs both times; the opening states the point count and offers no skip choice | end-to-end | planned |
| VO-026 | FR-006, FR-023, US4-AS4 | A nested interview is stopped early in a project that also has a marker after-specify hook at default priority and marker before-clarify and after-clarify hooks | The marker after-specify hook runs after the grill ends; neither clarify marker runs; no specify hook is run a second time | end-to-end | planned |
| VO-027 | FR-006 | The standalone grill is run and completed in a project with marker before-clarify and after-clarify hooks | Both clarify markers run, before the first question and before the completion report respectively | end-to-end | planned |
| VO-028 | FR-007, FR-014, SC-002, SC-009, US5-AS1, US5-AS2 | The nested grill is started with no human present, at each of the three settings, by the documented switch and by the agent's own indicator | Each run returns without waiting for input and asks nothing; every file is byte-for-byte unchanged; the outcome block reads not run, gives the reason and says the spec has not been clarified | end-to-end | planned |
| VO-029 | FR-014, SC-002, SC-010, EC-03 | EC-03: stop before the first answer. With the setting at strict, and again at on where a skip choice is offered, the developer says stop at the opening | Both times the outcome block reads stopped early, not skipped, and lists every point as outstanding; every file is byte-for-byte unchanged and the spec has no label | end-to-end | planned |
| VO-030 | FR-024 | The nested grill is run on a spec with nothing left to settle and satisfaction is confirmed; the standalone grill is then run on it again | The grill says it found nothing and asks only the satisfaction question; on confirmation the spec carries the plain label and the outcome is completed; the second run changes only the label's date | end-to-end | planned |
| VO-031 | FR-008 | The paths changed by a completed nested run that settled a term and a decision are listed | Only the spec, the requirements checklist and files under the knowledge-docs location changed; the checklist differs only in checkbox markers; the setting file, plans, tasks and code are unchanged | end-to-end | planned |
| VO-032 | FR-003, SC-003 | The reference feature is grilled with the same scripted answers by upstream v1.0.1 and by this extension's standalone grill | Both change the same spec sections apart from the label, record the same number of clarifications, create or update the same knowledge-doc paths and report the same coverage statuses | end-to-end | planned |
| VO-033 | FR-003, EC-04 | EC-04: a knowledge doc cannot be saved. An answer settles a cross-feature term while the knowledge-docs location is read-only | The point is not reported as resolved, the failure is stated to the developer and in the report, and no other location is written instead | end-to-end | planned |
| VO-034 | FR-019 | The package contents and command text are inspected, and the nested and standalone grills are started with an empty user configuration directory | The package installs nothing outside the project and names no user-level skill, agent or subagent; both grills open normally | end-to-end | planned |
| VO-035 | FR-009, SC-005, US6-AS2 | A specify run in a project where the Comprehension Checkpoint, git and agent-context extensions were installed before this extension; this extension is then removed | The grill runs before the Comprehension Checkpoint, before the agent-context refresh and before the commit prompt; after removal the other extensions' registrations are unchanged | end-to-end | planned |
| VO-036 | FR-001, EC-05 | EC-05: specify left open markers. The nested grill is started on a prepared spec that still holds a `[NEEDS CLARIFICATION]` marker and an unchecked checklist item, and the marker's question is answered | The grill opens with a question and does not stop or refuse; after the answers the marker is gone from the spec and the answer is recorded in Clarifications | end-to-end | planned |
| VO-037 | FR-016, EC-06 | EC-06: both grill extensions on one spec. With both installed, a spec completed by this extension's grill is grilled again with upstream's command, and a spec completed by upstream's command is grilled again with this extension's standalone grill | In both directions no question already recorded in Clarifications is recorded again, every earlier Clarifications line is unchanged, and the spec holds exactly one label line, directly under Status | end-to-end | planned |
| VO-038 | FR-018, DC-02 | DC-02: the shipped scripts run on the Bash 3.2 that macOS ships. The two scripts are inspected for constructs Bash 3.2 lacks, and their unit scenarios are run again through a Bash 3.2 binary when one is supplied | No such construct is present; where a Bash 3.2 binary is supplied every script scenario gives the same result as under the default Bash, and where none is supplied that part is reported as not run | unit | planned |

### Verification exemptions

<!--
  One row per requirement that will not be verified automatically, with the reason and
  how it is verified instead (or none, with why). A single row reading None in the
  Requirement column when there are no exemptions.
-->

| Requirement | Reason | Alternative verification |
|-------------|--------|--------------------------|
| SC-001 | Only the part of SC-001 that names the locked-down devcontainer of FR-019. Its managed settings cannot be reproduced on a developer machine (research R12), so no automated run inside it is possible. The rest of SC-001 is verified by VO-015, and FR-019 by VO-034 with an empty user configuration directory as a stand-in | The developer runs quickstart step 8 in the real devcontainer and the result and date are recorded in research.md under R12. This is a task in tasks.md placed before the release tasks, so the first release is not published until it has passed |


<!-- markdownlint-disable-file MD041 -->

## Architecture

**Feature architecture**: [architecture.md](./architecture.md) (C4 component views,
sequence diagrams, ER diagram)

**System views**: [Context](../../docs/architecture/context.md) |
[Containers](../../docs/architecture/containers.md) | [ERD](../../docs/architecture/erd.md)
(not yet created; `/speckit-c4-system` writes them after implementation)

| View | Impact of this feature |
|------|------------------------|
| Context | Adds the system itself, two people (Developer, Tech Lead) and five external systems (Spec Kit, AI Coding Agent, Automated Harness, Upstream Grill Extension, Other After-Specify Extensions) |
| Containers | Adds Grill Commands, Grill Scripts, Grill Setting File, Feature Spec and Knowledge Docs, with their relationships |
| Components | Grill Commands: Hook Entry Point, Run Wrapper, Upstream Interview. Grill Scripts: Context Reader, Label Writer. All new |
| Flows | Six, one per user story: automatic start to completion, setting decides the start, skip, stop and resume, no human present, hook ordering |
| ERD | Adds GRILL_SETTING, GRILLED_ON_LABEL, RELEASE and UPSTREAM_PROVENANCE; records the existing SPEC, CLARIFICATION and KNOWLEDGE_DOC |
