# Feature Specification: Specify Grill Extension

**Feature Branch**: `001-specify-grill-extension` *(feature directory; the project is not under version control, so no branch was created)*

**Created**: 2026-10-11

**Status**: Draft

**Input**: User description: "Build a Spec Kit extension, "Specify Grill" (extension id: grill-specify), that automatically runs the "grill with docs" interview straight after /speckit.specify. The goal is that no feature spec leaves the specify stage with unresolved ambiguity, and that domain terms and architecture decisions settled during the interview are saved into the project's canonical knowledge docs." *(The full brief also supplied background, users, six scenarios, FR-1 to FR-10, non-functional requirements, SC-1 to SC-5 and out-of-scope items; all are carried into the sections below. FR-001 to FR-010 and SC-001 to SC-005 keep the brief's numbering.)*

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Grill starts automatically after specify (Priority: P1)

A developer runs the specify command for a new feature. As soon as the spec and its requirements checklist have been written and validated, the grill-with-docs interview begins in the same session, without the developer typing another command. The interview asks one question at a time with no question limit, updates the spec after every answer, saves settled cross-feature terms and qualifying decisions to the project's canonical knowledge docs, and ends only when the developer confirms they are satisfied. The specify completion report then shows the coverage summary and lists every knowledge doc that was changed.

**Why this priority**: This is the reason the extension exists. Today the grill is opt-in and developers forget it, skip it, or run the five-question core clarify instead, so specs reach planning with unresolved ambiguity.

**Independent Test**: In a fresh project with only this extension installed, run specify with a reference feature description, answer the interview, confirm satisfaction, and check that the interview started unprompted, the spec gained a Clarifications section, and the completion report contains the coverage summary and the list of changed knowledge docs.

**Acceptance Scenarios**:

1. **Given** a project with the extension installed and the grill setting left at its default, **When** a developer runs specify, **Then** the grill starts in the same session with no further command and without first asking permission, after the spec and checklist are written and specify's own validation has finished.
2. **Given** an interview in progress, **When** the developer answers a question, **Then** the spec is updated and saved before the next question is asked.
3. **Given** an answer that settles a term used beyond this feature, **When** the answer is incorporated, **Then** the term has exactly one canonical definition in the project's knowledge docs.
4. **Given** an answer that settles a decision meeting all three recording conditions (costly to reverse, surprising without context, a real alternative was rejected for a reason), **When** the answer is incorporated, **Then** a decision record is created; if any condition fails, none is created.
5. **Given** every decision point has reached a final status, **When** the developer confirms satisfaction, **Then** the requirements checklist is revalidated and the specify completion report shows the coverage summary and the knowledge docs created or updated.
6. **Given** the grill has started in an interactive session, **When** it opens, **Then** it has already read the spec, states how many points it found to settle, and presents the first question; nothing has been written to any file at that moment.

---

### User Story 2 - Project-level grill setting: on, strict or off (Priority: P2)

A tech lead chooses one project-level grill setting by editing a single line in the extension's own configuration file. With **on** (the default), the grill starts after specify without asking permission, and its opening question carries a skip choice for specs simple enough not to need it. With **strict**, the grill starts the same way but offers no skip choice. With **off**, the grill never starts from specify. Because the setting lives in the project's files, it is visible, reviewable and the same for every developer on the project.

**Why this priority**: The tech lead's goal — every spec reaches planning clarified — depends on the grill running by default and on being able to remove the skip choice, while teams still need an off switch.

**Independent Test**: Run specify three times against the same description with the grill setting at each value and confirm: on starts the grill with a skip choice at the opening, strict starts it with none, off does not start it and says so in the report.

**Acceptance Scenarios**:

1. **Given** no grill setting has been chosen, **When** specify finishes, **Then** the grill starts with a skip choice at its opening (on behaviour) and no warning is shown.
2. **Given** the grill setting is strict, **When** specify finishes in an interactive session, **Then** the grill starts and its opening offers no skip choice.
3. **Given** the grill setting is off, **When** specify finishes, **Then** the grill does not run, the spec is byte-for-byte identical to plain specify, and the completion report says the grill is switched off.
4. **Given** the grill setting is present but unreadable or not one of the three values, **When** specify finishes, **Then** the grill runs as on and the report carries a one-line warning naming the bad value.

---

### User Story 3 - Skip a simple spec (Priority: P2)

A developer only needs a quick spike, or the spec is simple. When the grill opens it says how many points it found and offers a skip choice alongside the first question. The developer skips. The spec stays exactly as specify left it and the completion report clearly says the grill was skipped.

**Why this priority**: An unavoidable interview would push developers to bypass the extension altogether; an informed, clean, visible skip keeps running-by-default acceptable.

**Independent Test**: With the grill setting at on, run specify, choose skip at the opening, and compare the resulting spec with one produced by plain specify from the same description.

**Acceptance Scenarios**:

1. **Given** the grill setting is on, **When** the developer chooses skip at the opening, **Then** no file is created or changed by the grill, the spec carries no grilled-on label, and it is byte-for-byte identical to plain specify.
2. **Given** the developer skipped, **When** the specify completion report is shown, **Then** it states that the grill was skipped by the developer and how to run it later.

---

### User Story 4 - Stop partway and resume later (Priority: P2)

The developer stops partway through the interview. Every answer already settled is kept in the spec and knowledge docs, the points still open are listed, and the developer can later run the grill as a standalone command and continue from where they left off, without being re-asked what is already settled.

**Why this priority**: Exhaustive interviews are long. Losing settled answers, or having to start again, would make developers avoid the grill.

**Independent Test**: Start the interview, answer some questions, say "stop", check the spec and report, then run the grill as a standalone command and confirm it asks only about the points left open.

**Acceptance Scenarios**:

1. **Given** an interview with some answers settled, **When** the developer signals they want to stop, **Then** no new question is asked, all settled answers remain saved, the spec's grilled-on label says the grill was stopped early with the number of open points, and the report lists each outstanding point with the reason it is open.
2. **Given** a previously interrupted spec, **When** the developer runs the grill as a standalone command, **Then** it continues from the open points and does not re-ask settled ones.
3. **Given** a spec that has never been grilled, **When** the developer runs the grill as a standalone command, **Then** the full interview runs regardless of the grill setting, and its opening states how many points are open and offers no skip choice.
4. **Given** a nested run that the developer stops early, **When** the grill ends, **Then** the remaining after-specify hooks still run.

---

### User Story 5 - No human present (Priority: P2)

Specify runs from an automated harness with nobody available to answer. The grill does not block the run and does not invent answers. It reports that it was not run and leaves the spec and knowledge docs untouched.

**Why this priority**: A hook that hangs an automated pipeline, or that fabricates clarifications, is worse than no grill at all.

**Independent Test**: Run specify from a non-interactive harness with the grill setting at strict and confirm the run finishes, the spec is identical to plain specify, and the report states the grill was not run because no one was available to answer.

**Acceptance Scenarios**:

1. **Given** a non-interactive run and any grill setting, **When** specify finishes, **Then** the grill exits without asking a question and without changing any file.
2. **Given** a non-interactive run, **When** the completion report is produced, **Then** it states that the grill was not run and why, and that the spec has not been clarified.

---

### User Story 6 - Coexist with the upstream grill and other extensions (Priority: P3)

A project already has the upstream "grill" extension installed, and may also have other extensions that act after specify (such as one that refreshes agent context or one that prompts for a commit). Both grill extensions keep working, neither overwrites or shadows the other's commands, and the grill runs before any after-specify step that reads the finished spec.

**Why this priority**: Teams adopting this extension will often already have upstream installed; breaking it, or producing context snapshots of an un-grilled spec, would block adoption.

**Independent Test**: Install upstream grill, then this extension, plus the git and agent-context extensions; confirm all commands from both grill extensions are still invocable and that a specify run grills before context is refreshed.

**Acceptance Scenarios**:

1. **Given** the upstream grill extension is installed, **When** this extension is installed, **Then** every upstream command remains present and unchanged and this extension's commands are invocable under its own namespace.
2. **Given** other after-specify hooks are registered, **When** specify finishes, **Then** the grill runs before hooks that consume the finished spec (for example the Comprehension Checkpoint) with no manual reordering after install.
3. **Given** this extension is installed, **When** it is uninstalled, **Then** its after-specify registration and commands are removed, other extensions' registrations are untouched, and all specs and knowledge docs it produced remain in place.

---

### Edge Cases

- **Knowledge doc cannot be saved**: the affected decision point is not reported as resolved; the failure is surfaced to the developer and in the report, as upstream does. The run's outcome is stopped early (FR-014).
- **Specify itself ends with open `[NEEDS CLARIFICATION]` markers or failed checklist items**: the grill starts only after specify's own clarification and validation loop has finished; remaining failures are inputs to the interview, not blockers.
- **Grill invoked standalone with no active feature or no spec**: it stops with a clear message and changes nothing.
- **Session ends abruptly mid-question** (window closed, not a polite "stop"): because every settled answer is saved before the next question and the grilled-on label is kept current in its stopped-early form, the spec truthfully shows a partial grill and a later standalone run resumes from the saved state.
- **A harness runs specify unattended but sets no signal**: the run is treated as interactive (FR-007); setting the documented switch is the harness owner's responsibility.
- **Grill setting is strict but the developer interrupts**: the interruption is honoured as in Story 4; the grilled-on label and the report mark the grill as stopped early.
- **Developer stops at the first question, before answering anything** (any setting): the outcome is stopped early, not skipped; the report lists every point as outstanding and how to resume; no file is changed, so the spec carries no grilled-on label and is byte-for-byte identical to plain specify.
- **Grill setting is off, or the developer skipped, then the developer runs the standalone command**: the interview runs, with no skip choice at its opening; the grill setting governs only the automatic start.
- **The project resolves its knowledge docs to a non-default location**: the grill uses the project's resolved location and existing conventions, as upstream does, and never pre-creates an empty knowledge base.
- **Both grill extensions installed and the developer runs upstream's command on a spec already grilled by this one** (or the reverse): each treats the existing Clarifications as settled; neither corrupts the other's output.
- **The grill finds nothing to settle**: it says so, asks the satisfaction question, and on confirmation the spec is labelled as grilled (FR-024); with the setting on, the developer may still skip at the opening instead, leaving the spec unlabelled.
- **Extension reinstalled or upgraded**: the hook is registered exactly once.

## Clarifications

### Session 2026-10-11

- Q: When the grill runs, should before-clarify/after-clarify hooks fire? → A: Standalone only — suppressed when nested inside specify, fired as upstream does when run standalone.
- Q: Which agent integrations must be in the tested set? → A: Claude Code only; use Haiku during testing where possible to balance confidence against token cost.
- Q: Where do this project's own glossary and decision records live? → A: `docs/domain_knowledge/CONTEXT.md` and `docs/domain_knowledge/adr/`, created only when the first item is settled.
- Q: Is it acceptable that a skipped or unattended spec carries no trace of the grill outcome? → A: A grilled spec carries a dated "grilled on" label; a spec that was not grilled carries none and stays byte-for-byte identical to plain specify.
- Q: Is the no-skip setting meant to block planning or fail unattended runs? → A: No. It means the grill always starts, with no skip choice, when a human is present; it does not force completion, block later stages, or fail an unattended run.
- Q: How is "no human present" decided? → A: By explicit signals only; with no signal the run is treated as interactive.
- Q: Where does the grill sit among other after-specify hooks? → A: Before the Comprehension Checkpoint, and before any other hook that consumes the finished spec.
- Q: Which runs earn the grilled-on label, and where does it sit? → A: Completed and stopped-early runs; a stopped-early label says so and gives the count of open points; a re-run replaces it; it sits in the header directly under Status.
- Q: If the developer stops early inside specify, do the other after-specify hooks still run? → A: Yes; stopping ends only the grill.
- Q: How is the upstream interview carried? → A: Upstream's text is kept verbatim; this extension's additions live in a wrapper around it.
- Q: What values does the project setting have, and what is the default? → A: Three: on (default; starts without asking, with a skip choice at the opening), strict (starts with no skip choice) and off. This replaces the brief's required / offered / off.
- Q: What does the developer see when the grill opens? → A: The grill has already read the spec; it states how many points it found and presents the first question, with the skip choice when the setting is on. Nothing is written before the developer answers.
- Q: What happens when the setting is missing or broken? → A: Missing means on, silently. Present but unusable means on, with a one-line warning naming the bad value; a typo never switches the grill off.
- Q: What is the setting called? → A: The grill setting; "mode" is avoided because it collides with other modes in the toolchain.
- Q: What are the three values called? → A: `on`, `strict` and `off`.
- Q: Is a spec in which the grill finds nothing to ask "grilled"? → A: Yes. The grill says it found nothing, asks the closing satisfaction question, and on confirmation writes the label and reports completed.
- Q: When is the grilled-on label first written? → A: With the first saved answer, in its stopped-early form, refreshed after each answer; it becomes the plain form only when the developer confirms satisfaction.
- Q: What does the opening of a standalone run look like? → A: The same at every grill setting: it states how many points are open and presents the first question, with no skip choice.
- Q: What is reported when the developer stops at the first question, before answering anything? → A: Stopped early, at every setting, with every point listed as outstanding and how to resume; nothing is written, so the spec carries no label and stays byte-for-byte identical to plain specify.
- Q: Does a plain install put the grill ahead of the other after-specify hooks, or is that left to written guidance? → A: The extension registers itself to run ahead of default-priority hooks, so a plain install gives the right order; the documentation covers only clashes with another extension that also claims an early position.
- Q: How does the extension reach other projects? → A: It is installable from a local directory and is also released as a versioned archive from a public repository, installable by URL; creating that repository is in scope, a community catalogue entry is not.
- Q: Under what licence is the extension released? → A: MIT, matching upstream.
- Q: What exactly does the locked-down devcontainer of FR-019 block? → A: Only user-level skills and agents; project skills installed by Spec Kit still load, so the extension must depend on nothing at user level and on no subagent.
- Q: Where does the public repository live, and which Spec Kit release is the minimum? → A: `github.com/leejsinclair/speckit-grill-specify`; the minimum is 1.1.3, the current release verified on 2026-10-11, so the local CLI is upgraded before implementation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The extension MUST register an after-specify hook that triggers the grill only once the spec exists and specify's own validation has finished.
- **FR-002**: The extension MUST provide the grill as a command in its own namespace (`speckit.grill-specify.with-docs`) that also works standalone, for re-runs and for resuming an interrupted interview.
- **FR-003**: The grill MUST preserve the artefacts and side effects of upstream `speckit.grill.with-docs` v1.0.1: the Clarifications section, incremental spec updates after every answer, requirements-checklist revalidation, the canonical context file, topic-document and decision-record rules (including the three-condition recording gate), persistence-failure handling, and the explicit satisfaction gate.
- **FR-004**: The extension MUST record which upstream version was vendored or adapted, retain upstream's MIT attribution, and document the procedure for pulling in later upstream changes.
- **FR-005**: The extension MUST read the grill setting (on / strict / off) from its own configuration file. The setting MUST NOT be expressed as a hook condition, because current command templates skip conditional hooks.
- **FR-006**: When the grill runs from the after-specify hook it MUST NOT re-trigger any specify hooks. Clarify hooks (before-clarify and after-clarify, for example the git extension's commit prompt) MUST be suppressed in that nested run, because the remaining after-specify hooks already follow it (FR-023); in a standalone run they MUST fire as upstream's command fires them. This behaviour MUST be documented.
- **FR-007**: The grill MUST detect a non-interactive run and exit without asking questions, inventing answers, or changing any file. Detection MUST rely on explicit signals only: a documented switch that a harness sets, and the agent's own known indicators that it is running unattended. With no such signal the run MUST be treated as interactive, so a present developer is never silently skipped.
- **FR-008**: The grill MUST write only to the active feature's spec, the checkbox states of its requirements checklist, and the project's resolved knowledge-docs location. It MUST NOT touch plans, tasks, code, or configuration (including its own).
- **FR-009**: The extension MUST coexist with other after-specify hooks (for example agent-context refresh) and MUST register its own hook to run ahead of hooks registered at the default priority, so that after a plain install, with no manual reordering, the grill runs before hooks that consume the finished spec, including the Comprehension Checkpoint, commit prompts and agent-context refresh. It MUST document what to do when another extension also claims an early position.
- **FR-010**: Uninstalling the extension MUST remove its hook registration and commands and MUST leave every generated spec and knowledge doc in place.
- **FR-011**: In an interactive nested run with the grill setting **on** or **strict**, the grill MUST start without first asking permission. It MUST read the spec before its opening, state how many points it found to settle, and present the first question. Nothing may be written to any file before the developer's first answer.
- **FR-012**: With the grill setting **on**, the opening MUST include a skip choice; choosing it MUST end the grill without changing any file. With **strict**, the opening MUST NOT include a skip choice. With **off**, the automatic start MUST do nothing. When no setting has been chosen the grill MUST behave as **on** with no warning; when the setting is present but unusable it MUST behave as **on** and the report MUST carry a one-line warning naming the bad value.
- **FR-013**: The grill setting MUST govern only the automatic start after specify. A standalone run MUST run the interview whatever the setting (subject to FR-007). Its opening MUST be the same at every setting: it reads the spec, states how many points are open and presents the first question, and MUST NOT include a skip choice.
- **FR-014**: Every automatic start MUST end with exactly one clearly stated outcome that appears in the specify completion report: **completed**, **stopped early**, **skipped**, **switched off**, or **not run (no human present)**. For completed and stopped-early outcomes the report MUST include the coverage summary and the list of knowledge docs created or updated; for stopped-early it MUST also list outstanding points and how to resume. Stopping before the first answer MUST be reported as stopped early (never as skipped; skipped means only the skip choice of FR-012), with every point listed as outstanding; in that case no file is changed and no label is written. A run that ends because a knowledge doc could not be saved MUST also be reported as stopped early, with the affected point listed as outstanding.
- **FR-015**: When the developer stops partway, all answers settled so far MUST remain saved, and a later standalone run MUST continue from the open points without re-asking settled ones. Resume state MUST be derivable from the spec and knowledge docs alone (see FR-008).
- **FR-016**: The extension MUST install alongside the upstream "grill" extension without overwriting, renaming, or shadowing any upstream command, and upstream MUST NOT shadow this extension's commands.
- **FR-017**: The extension MUST NOT require the upstream extension to be installed; everything it needs to run the interview ships with it.
- **FR-018**: The extension MUST support macOS and Linux with Bash, matching upstream, and MUST declare as its minimum the Spec Kit release that was current when the extension was planned, as verified against the Spec Kit repository (1.1.3, verified on 2026-10-11).
- **FR-019**: The installed grill command MUST be invocable, both automatically and standalone, in a Claude Code devcontainer whose managed settings block custom user skills and agents. The extension MUST therefore rely only on what Spec Kit installs into the project, and MUST NOT depend on any user-level skill or agent or on a subagent.
- **FR-020**: The extension MUST NOT change the interview algorithm, MUST NOT override core specify or clarify templates, and MUST NOT include the Serena variant.
- **FR-021**: A spec on which the grill has saved at least one answer, or whose grill the developer has confirmed as complete, MUST carry exactly one dated label in its header, directly under Status. The label MUST be written together with the first saved answer in its stopped-early form, giving the number of points still open (for example "Grilled on: 2026-10-11 (stopped early, 4 points open)"), and MUST be refreshed after each further answer. It MUST change to the plain form "Grilled on: YYYY-MM-DD" only when the developer confirms satisfaction. A later run MUST replace the label with the new date and state. A spec whose grill was skipped, switched off or not run MUST NOT carry the label.
- **FR-022**: The extension MUST carry upstream's interview text verbatim and keep its own additions (grill-setting check, opening and skip choice, non-interactive exit, nested-hook rule, grilled-on label, outcome report) in a wrapper around it; the only change inside the upstream text is the hook rule that FR-006 requires to differ.
- **FR-023**: When the developer stops the interview early in a nested run, only the grill ends; the remaining after-specify hooks MUST still run, against the partly clarified spec.
- **FR-024**: When the grill finds no points to settle, it MUST say so and go straight to the satisfaction gate; on confirmation it MUST write the plain grilled-on label and report the outcome as completed. A standalone re-run on a fully settled spec behaves the same way, changing only the label's date.
- **FR-025**: The extension MUST be installable from a local directory and from a versioned release archive, by URL, published from a public repository. Creating that public repository and publishing the first versioned release are part of this feature. The release version MUST match the version the extension declares, and the published archive MUST contain the upstream provenance record and attribution of FR-004. The extension MUST be released under the MIT licence, with its own licence file alongside upstream's copyright notice.

### Key Entities

- **Grill setting**: The project-level setting with values on (default), strict and off; governs only the automatic start.
- **Grill outcome**: The single result of an automatic start — completed, stopped early, skipped, switched off, or not run — shown in the specify completion report.
- **Clarifications record**: The section of the spec that holds each question asked and its settled answer; the basis for resuming.
- **Coverage summary**: The per-category status of every decision point (clear, resolved, outstanding, deferred) reported at the end of an interview.
- **Canonical knowledge docs**: The project's context file, topic documents and decision records, at the location the project resolves; the only place cross-feature terms and qualifying decisions are defined.
- **Release**: A versioned archive of the extension published from the public repository; what other projects install by URL.
- **Upstream provenance record**: The statement of which upstream version was adapted, its licence attribution, and the update procedure.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a fresh project, running specify launches the grill automatically with zero manual steps in 100% of tested agent integrations. The tested set is Claude Code only, including the locked-down devcontainer of FR-019; other integrations are best-effort and untested.
- **SC-002**: With the grill setting off, or when the grill is skipped at its opening or stopped before the first answer, or when no human is present, the resulting spec is byte-for-byte identical to the one plain specify produces from the same description, and no other file is created or changed.
- **SC-003**: For the same answers on a reference feature, the extension's output is equivalent to upstream `speckit.grill.with-docs` v1.0.1: the same sections changed (apart from the grilled-on label of FR-021), the same clarifications recorded, the same knowledge docs created or updated, and the same coverage statuses.
- **SC-004**: After any completed or stopped-early interview, every settled cross-feature term has exactly one canonical definition, and 100% of decision records created pass upstream's three-condition gate.
- **SC-005**: Tests exist and pass at all four levels: manifest and structure validation; install and hook registration; behaviour against representative specs, including an interrupted run and a non-interactive run; and regression with the git and agent-context extensions, including removal.
- **SC-006**: After an interrupted interview, a standalone re-run re-asks none of the previously settled questions.
- **SC-007**: With the upstream grill extension installed before or after this one, 100% of both extensions' commands remain invocable and unchanged.
- **SC-008**: After uninstall, no after-specify registration for this extension remains and 100% of previously generated specs and knowledge docs are unchanged.
- **SC-009**: A non-interactive specify run with the extension installed completes without waiting for input at every grill setting.
- **SC-010**: 100% of specs holding at least one answer saved by the grill carry exactly one grilled-on label whose state (stopped early with open-point count, or complete) matches the spec; 0% of skipped, switched-off or not-run specs, or specs whose grill was stopped before the first answer, carry one.
- **SC-011**: In a fresh project, installing the extension by URL from the published release archive and installing it from a local directory both yield the same commands and the same single after-specify registration.

## Assumptions

- "Vendored or adapted" means the interview instructions are shipped inside this extension, because an extension cannot declare a dependency on another. The only intended differences from upstream are the grill-setting check, the opening and its skip choice (which includes holding any spec edit upstream would make before its first question until the developer's first answer, as FR-011 requires), non-interactive detection, the nested-hook rules, the grilled-on label and the outcome report.
- With the **strict** setting there is no skip choice at the opening, but a developer who asks to stop mid-interview is still honoured (upstream's interruption path is preserved behaviour); the grilled-on label and the report mark the grill as stopped early. Strict does not make an un-grilled spec fail later stages — enforcement beyond the label and report is out of scope.
- In a non-interactive run the outcome is "not run" at every grill setting, including strict; the run is not failed.
- "Equivalent to upstream" (SC-003) is judged on structure and recorded content, not on byte-identical wording, since interview phrasing varies between runs.
- Resuming relies on what is already saved in the spec and knowledge docs; no separate progress file is kept, consistent with the write boundary in FR-008.
- The grill setting is changed by editing one line in the extension's configuration file in the project; no command for changing it is included. It is project-wide, with no per-developer or per-feature override, and anyone who can edit the project's files can change it.
- The default knowledge-docs location and the rules for honouring a project's own location are upstream's, unchanged.
- Hook ordering relative to other extensions is achieved through this extension's own registration, which claims a position ahead of default-priority hooks; other extensions' registrations are never modified. Written guidance covers only a clash with another extension that claims an equally early position.
- "Current Spec Kit release" was determined at planning time from the Spec Kit repository: 1.1.3, verified on 2026-10-11. This project's local CLI ran 1.0.2.dev0 at that time and is upgraded before implementation; upstream declares a minimum of 0.16.2.
- Windows/PowerShell is not supported, matching upstream.
- This project is not under version control today; putting it under version control and creating the public repository are prerequisites of the release in FR-025. The repository is `github.com/leejsinclair/speckit-grill-specify`.
- Behaviour tests that drive a live agent use the lowest-cost Claude model that still gives trustworthy results (Haiku where possible), trading some confidence for token cost; a more capable model is used only where the cheaper one proves unreliable.

## Out of Scope

- Testing agent integrations other than Claude Code.
- Changing core specify or clarify templates, including any preset that overrides specify.
- Serena integration (the with_serena variant).
- Changing the interview algorithm itself.
- The upstream `speckit.grill.me` (no-docs) variant.
- Submitting the extension to the Spec Kit community catalogue (install by name).

<!-- markdownlint-disable-file MD041 -->

## System Context *(when the feature involves people or external systems)*

**System context view**: [context.md](../../docs/architecture/context.md) (not yet created)

| Actor or external system | Type | Role in this feature | In context view? |
|--------------------------|------|----------------------|------------------|
| Developer | Person | Runs specify, answers or skips the grill, resumes it later | New |
| Tech lead | Person | Chooses the project-level grill setting; relies on clarified specs and visible decision records | New |
| Automated harness | External system | Runs specify with no human present; must not be blocked | New |
| Spec Kit | External system | Hosts the extension, runs specify and dispatches after-specify hooks | New |
| Upstream grill extension | External system | Source of the adapted interview; may be installed side by side | New |
| Other after-specify extensions (git, agent-context, comprehension check) | External system | Run after specify alongside the grill; ordering matters | New |
| AI coding agent integration | External system | Executes the commands and conducts the interview with the developer | New |

**Changes to the system context**: Adds all of the above; no project-level context view exists yet.
