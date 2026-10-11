<!--
Sync Impact Report
- Version change: none (unfilled template) → 1.0.0
- Modified principles: none renamed; all five are new
  - I. Upstream Fidelity
  - II. Narrow Write Boundary
  - III. Test-First with Recorded Evidence
  - IV. Self-Contained and Non-Invasive
  - V. Never Block, Never Invent
- Added sections: Platform and Licence Constraints; Development Workflow; Governance
- Removed sections: none
- Deferred items: none
- Source: principles promoted from the constraints of specs/001-specify-grill-extension
  (spec.md, plan.md Technical Context, integrated-tdd process rules)
-->

# Specify Grill Extension Constitution

## Core Principles

### I. Upstream Fidelity

- Text vendored from an upstream project MUST be carried verbatim.
- Every change inside vendored text MUST be recorded as a patch file kept in the repository,
  and the shipped text MUST be reproducible from the pristine copy plus those patches.
- The vendored version, its source repository, its licence notice and the procedure for
  updating it MUST be recorded and shipped with the extension.
- The upstream interview algorithm MUST NOT be changed. Behaviour the extension adds lives in
  a wrapper around the vendored text.

Rationale: the extension's value rests on behaving as upstream does. Undocumented drift makes
later upstream changes impossible to merge and equivalence impossible to show.

### II. Narrow Write Boundary

- The extension MUST write only to the active feature's spec, the checkbox states of that
  feature's requirements checklist, and the project's resolved knowledge-docs location.
- It MUST NOT write to plans, tasks, code or configuration, including its own setting file.
- A spec the grill did not change MUST remain byte-for-byte as the specify stage left it.
- Nothing may be written before the developer's first answer.

Rationale: a tool that runs automatically after another stage must be predictable in what it
touches, so that a skipped, switched-off or unattended run leaves no trace to review.

### III. Test-First with Recorded Evidence

- Verification MUST be derived from the requirements and design before implementation.
- Each behaviour MUST go through Red, Green, Refactor, with each result taken from a real
  test run and recorded. A result MUST NOT be stated unless a run recorded it.
- A test MUST NOT be removed, weakened, skipped or bypassed to obtain a pass.
- A requirement that cannot be verified automatically MUST be recorded as an exemption with
  its reason and the verification used instead.

Rationale: most of this extension is agent instructions, where behaviour is easy to assert and
hard to prove. Only recorded runs show that an instruction does what it says.

### IV. Self-Contained and Non-Invasive

- The extension MUST NOT override core Spec Kit templates or commands.
- It MUST NOT require another extension to be installed; everything it needs ships with it.
- It MUST depend on nothing at user level (skills, agents, settings) and on no subagent.
- It MUST NOT modify, shadow or rename another extension's commands or registrations.
- Uninstalling it MUST remove its commands and registrations and leave every document it
  produced in place.

Rationale: teams adopt the extension alongside others and in locked-down environments. It has
to install, coexist and uninstall without side effects on anything it does not own.

### V. Never Block, Never Invent

- A run with no person present MUST end without waiting for input and without changing a file.
- An answer MUST NOT be fabricated on the developer's behalf.
- Absence of a person MUST be decided from explicit signals only; with no signal the run is
  treated as interactive.
- Every run MUST end with exactly one outcome, stated truthfully in the report. Incomplete or
  failed work MUST NOT be reported as complete.

Rationale: a hook that hangs a pipeline, or that records clarifications nobody gave, is worse
than no hook at all.

## Platform and Licence Constraints

- The extension is released under the MIT licence, with upstream's copyright notice retained.
- Supported platforms are macOS and Linux. Shipped scripts MUST run on Bash 3.2.
- Windows and PowerShell are not supported.
- The declared minimum Spec Kit version MUST be one the extension has been tested against.
- The published release version MUST match the version the extension's manifest declares.

## Development Workflow

- Features follow the Spec Kit lifecycle: specify, plan, tasks, analyze, implement.
- Tests are run only through the commands the project declares in its Makefile.
- Live-agent tests use the lowest-cost model that gives trustworthy results; a more capable
  model is used only where the cheaper one proves unreliable, with the reason recorded.
- Commits, pushes, tags, repository creation and releases happen only on the developer's
  explicit instruction.

## Governance

- This constitution takes precedence over other project practices. A conflict between it and
  a spec, plan or task list is resolved by changing that artifact, not by reinterpreting a
  principle.
- Amendments are made only through an explicit constitution update that records what changed
  and why, and that states the effect on features in progress.
- Versioning follows semantic versioning: MAJOR for removing or redefining a principle, MINOR
  for adding a principle or section or materially expanding guidance, PATCH for clarification
  and wording.
- Each plan's Constitution Check MUST evaluate the feature against every principle, and the
  analyze stage MUST report any conflict as critical.

**Version**: 1.0.0 | **Ratified**: 2026-10-11 | **Last Amended**: 2026-10-11
