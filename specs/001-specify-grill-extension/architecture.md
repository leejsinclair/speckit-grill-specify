# Architecture: Specify Grill Extension

**Feature**: `001-specify-grill-extension` | **Date**: 2026-10-11
**Feature docs**: [Spec](./spec.md) | [Plan](./plan.md) |
[Data model](./data-model.md) | [Contracts](./contracts/)
**System views**: [Context](../../docs/architecture/context.md) |
[Containers](../../docs/architecture/containers.md) | [ERD](../../docs/architecture/erd.md)
(none of the three exists yet; every element below is new)

## Components

The extension is two containers: the command prompts an AI coding agent follows, and the
Bash scripts those prompts call. The files they read and write live in the project that
installed the extension and are shown as data stores.

### Grill Commands

```mermaid
C4Component
    title Component View for Grill Commands - Specify Grill Extension

    Person(developer, "Developer", "Runs specify and answers skips or stops the grill")

    Container_Boundary(grillCommands, "Grill Commands") {
        Component(hookEntryPoint, "Hook Entry Point", "Markdown agent command", "Starts the grill as a nested run when specify finishes")
        Component(runWrapper, "Run Wrapper", "Markdown agent command", "Applies the grill setting and the opening and reports the outcome")
        Component(upstreamInterview, "Upstream Interview", "Markdown agent command", "Asks one question at a time and saves each settled answer")
    }

    Container(grillScripts, "Grill Scripts", "Bash", "Reads the run context and writes the grilled-on label")
    ContainerDb(featureSpec, "Feature Spec", "Markdown files", "The active spec and its requirements checklist")
    ContainerDb(knowledgeDocs, "Knowledge Docs", "Markdown files", "Context file topic documents and decision records")
    System_Ext(specKit, "Spec Kit", "Runs specify and dispatches after-specify hooks")
    System_Ext(codingAgent, "AI Coding Agent", "Executes the commands and holds the conversation")

    Rel(specKit, hookEntryPoint, "Dispatches after specify", "after_specify hook")
    Rel(codingAgent, hookEntryPoint, "Executes", "Project skill")
    Rel(hookEntryPoint, runWrapper, "Invokes as a nested run", "Skill call with --nested")
    Rel(developer, runWrapper, "Runs standalone and answers", "Chat")
    Rel(runWrapper, grillScripts, "Gets run context and sets label through", "Bash and JSON")
    Rel(runWrapper, upstreamInterview, "Runs the interview in")
    Rel(upstreamInterview, featureSpec, "Reads and updates", "File I/O")
    Rel(upstreamInterview, knowledgeDocs, "Reads and updates", "File I/O")
    Rel(runWrapper, specKit, "Returns the outcome block to", "Chat output")
```

| Component | Responsibility | Technology | Status | Source location |
|-----------|----------------|------------|--------|-----------------|
| Hook Entry Point | Receives the after-specify dispatch and starts the grill with `--nested`; hands the outcome block back to specify | Markdown agent command | New | `commands/speckit.grill-specify.auto.md` |
| Run Wrapper | Decides nested or standalone, reads the run context, exits when switched off or unattended, presents the opening and skip choice, keeps the label current, prints the outcome | Markdown agent command | New | `commands/speckit.grill-specify.with-docs.md` (outside the upstream markers) |
| Upstream Interview | The with-docs interview from upstream v1.0.1, verbatim apart from the nested-run hook rule | Markdown agent command | New (vendored) | `commands/speckit.grill-specify.with-docs.md` (between the upstream markers); source in `upstream/` |

### Grill Scripts

```mermaid
C4Component
    title Component View for Grill Scripts - Specify Grill Extension

    Person(techLead, "Tech Lead", "Chooses the project grill setting")

    Container(grillCommands, "Grill Commands", "Markdown agent commands", "The hook entry point the wrapper and the interview")

    Container_Boundary(grillScripts, "Grill Scripts") {
        Component(contextReader, "Context Reader", "Bash", "Reports the grill setting and whether a human is present")
        Component(labelWriter, "Label Writer", "Bash", "Writes or refreshes the grilled-on label")
    }

    ContainerDb(grillSettingFile, "Grill Setting File", "YAML file", "The one-line project grill setting")
    ContainerDb(featureSpec, "Feature Spec", "Markdown files", "The active spec and its requirements checklist")
    System_Ext(automatedHarness, "Automated Harness", "Runs specify with no human present")

    Rel(techLead, grillSettingFile, "Edits the setting in", "Text editor")
    Rel(grillCommands, contextReader, "Asks for the run context from", "Bash and JSON")
    Rel(grillCommands, labelWriter, "Sets the label through", "Bash")
    Rel(contextReader, grillSettingFile, "Reads", "File I/O")
    Rel(automatedHarness, contextReader, "Signals no human present to", "Environment variable")
    Rel(labelWriter, featureSpec, "Writes the label into", "File I/O")
```

| Component | Responsibility | Technology | Status | Source location |
|-----------|----------------|------------|--------|-----------------|
| Context Reader | Reads the grill setting with its fallback rules and the non-interactive signals; prints one JSON object; writes nothing | Bash | New | `scripts/bash/grill-context.sh` |
| Label Writer | Inserts or replaces the single grilled-on label under the spec's Status line and changes nothing else | Bash | New | `scripts/bash/grill-label.sh` |

## Flows

### Flow 1: Grill starts automatically and completes (User Story 1)

```mermaid
sequenceDiagram
    autonumber
    actor developer as Developer
    participant specKit as Spec Kit
    participant hookEntryPoint as Hook Entry Point
    participant runWrapper as Run Wrapper
    participant grillScripts as Grill Scripts
    participant upstreamInterview as Upstream Interview
    participant featureSpec as Feature Spec
    participant knowledgeDocs as Knowledge Docs

    developer->>specKit: Run specify
    specKit->>featureSpec: Write spec and checklist
    specKit->>hookEntryPoint: EXECUTE_COMMAND speckit.grill-specify.auto
    hookEntryPoint->>runWrapper: speckit.grill-specify.with-docs --nested
    runWrapper->>grillScripts: grill-context.sh --json
    grillScripts-->>runWrapper: setting on and interactive true
    runWrapper->>upstreamInterview: Scan the spec without writing
    upstreamInterview->>featureSpec: Read spec
    upstreamInterview-->>runWrapper: Points to settle
    runWrapper-->>developer: Point count and first question with skip choice
    loop Each question until every point is final
        developer->>upstreamInterview: Answer
        upstreamInterview->>featureSpec: Save Clarifications line and updated section
        opt Cross-feature term or qualifying decision
            upstreamInterview->>knowledgeDocs: Save and read back
        end
        runWrapper->>grillScripts: grill-label.sh --state stopped --open n
        grillScripts->>featureSpec: Write stopped-early label
        upstreamInterview-->>developer: Next question
    end
    upstreamInterview-->>developer: Satisfaction gate
    developer->>upstreamInterview: Finish and proceed
    runWrapper->>grillScripts: grill-label.sh --state complete
    grillScripts->>featureSpec: Write plain label
    upstreamInterview->>featureSpec: Revalidate checklist checkboxes
    runWrapper-->>specKit: GRILL OUTCOME completed
    specKit-->>developer: Completion report with coverage and knowledge docs
```

**Covers**: FR-001, FR-003, FR-011, FR-014, FR-021; US1-AS1 to US1-AS6
**Notes**: Nothing is written between steps 3 and 10. The label is written in its
stopped-early form with the first saved answer, so a session that ends abruptly leaves a
truthful spec. Clarify hooks are not processed in this nested run (FR-006).

### Flow 2: The grill setting decides the start (User Story 2)

```mermaid
sequenceDiagram
    autonumber
    actor techLead as Tech Lead
    actor developer as Developer
    participant grillSettingFile as Grill Setting File
    participant specKit as Spec Kit
    participant runWrapper as Run Wrapper
    participant contextReader as Context Reader

    techLead->>grillSettingFile: Set grill to on strict or off
    developer->>specKit: Run specify
    specKit->>runWrapper: Nested run through the hook entry point
    runWrapper->>contextReader: grill-context.sh --json
    contextReader->>grillSettingFile: Read grill line
    alt Setting off
        contextReader-->>runWrapper: setting off
        runWrapper-->>specKit: GRILL OUTCOME switched off
    else Setting strict
        contextReader-->>runWrapper: setting strict
        runWrapper-->>developer: Point count and first question with no skip choice
    else Setting on or missing
        contextReader-->>runWrapper: setting on
        runWrapper-->>developer: Point count and first question with skip choice
    else Setting unusable
        contextReader-->>runWrapper: setting on with warning naming the bad value
        runWrapper-->>developer: Point count and first question with skip choice
        runWrapper-->>specKit: Warning line in the outcome block
    end
```

**Covers**: FR-005, FR-012, FR-013; US2-AS1 to US2-AS4
**Notes**: The setting is read once per run. A standalone run does not consult it.

### Flow 3: Skip a simple spec (User Story 3)

```mermaid
sequenceDiagram
    autonumber
    actor developer as Developer
    participant specKit as Spec Kit
    participant runWrapper as Run Wrapper
    participant upstreamInterview as Upstream Interview
    participant featureSpec as Feature Spec

    specKit->>runWrapper: Nested run with setting on
    runWrapper->>upstreamInterview: Scan the spec without writing
    upstreamInterview->>featureSpec: Read spec
    upstreamInterview-->>runWrapper: Points to settle
    runWrapper-->>developer: Point count and first question with skip choice
    developer->>runWrapper: Skip
    runWrapper-->>specKit: GRILL OUTCOME skipped with how to run later
    specKit-->>developer: Completion report says the grill was skipped
```

**Covers**: FR-012, FR-014; US3-AS1, US3-AS2; SC-002
**Notes**: No write happens on this path, so the spec is byte-for-byte what specify
produced and carries no label.

### Flow 4: Stop partway and resume later (User Story 4)

```mermaid
sequenceDiagram
    autonumber
    actor developer as Developer
    participant specKit as Spec Kit
    participant runWrapper as Run Wrapper
    participant upstreamInterview as Upstream Interview
    participant grillScripts as Grill Scripts
    participant featureSpec as Feature Spec

    Note over developer,featureSpec: Nested run with some answers already saved and labelled
    developer->>upstreamInterview: Stop
    upstreamInterview->>featureSpec: Final validation and checklist revalidation
    runWrapper->>grillScripts: grill-label.sh --state stopped --open n
    grillScripts->>featureSpec: Refresh stopped-early label
    runWrapper-->>specKit: GRILL OUTCOME stopped early with outstanding points
    specKit-->>developer: Remaining after-specify hooks then completion report
    Note over developer,featureSpec: Later in a new session
    developer->>runWrapper: speckit.grill-specify.with-docs
    runWrapper->>upstreamInterview: Scan the spec without writing
    upstreamInterview->>featureSpec: Read spec and Clarifications
    upstreamInterview-->>runWrapper: Open points only
    runWrapper-->>developer: Open point count and first open question with no skip choice
    developer->>upstreamInterview: Answers until finished
    runWrapper->>grillScripts: grill-label.sh --state complete
    grillScripts->>featureSpec: Replace label with plain form
```

**Covers**: FR-002, FR-013, FR-015, FR-021, FR-023; US4-AS1 to US4-AS4; SC-006
**Notes**: Resume state is only what the spec and knowledge docs hold; there is no
progress file. Stopping ends the grill alone, so specify goes on to its other hooks.

### Flow 5: No human present (User Story 5)

```mermaid
sequenceDiagram
    autonumber
    participant automatedHarness as Automated Harness
    participant specKit as Spec Kit
    participant runWrapper as Run Wrapper
    participant contextReader as Context Reader

    automatedHarness->>specKit: Run specify unattended
    specKit->>runWrapper: Nested run through the hook entry point
    runWrapper->>contextReader: grill-context.sh --json
    contextReader-->>runWrapper: interactive false with the reason
    runWrapper-->>specKit: GRILL OUTCOME not run - no human present
    specKit-->>automatedHarness: Completion report says the spec is not clarified
```

**Covers**: FR-007, FR-014; US5-AS1, US5-AS2; SC-009
**Notes**: Interactivity is checked before the setting, so the result is the same at
`on`, `strict` and `off`. No question is asked and no file is read for writing.

### Flow 6: Ordering among after-specify hooks (User Story 6)

```mermaid
sequenceDiagram
    autonumber
    actor developer as Developer
    participant specKit as Spec Kit
    participant hookEntryPoint as Hook Entry Point
    participant otherHooks as Other After-Specify Extensions

    developer->>specKit: Run specify
    specKit->>specKit: Sort after_specify hooks by priority ascending
    specKit->>hookEntryPoint: Priority 5 - run the grill
    hookEntryPoint-->>specKit: Outcome block
    specKit->>otherHooks: Priority 10 - comprehension check and others
    otherHooks-->>specKit: Done
    specKit-->>developer: Completion report
```

**Covers**: FR-009, FR-016, FR-023; US6-AS2
**Notes**: The order comes from this extension's own registration. No other extension's
registration is read or changed.

## Data

Only stored items appear here. The run context, the grill run, the outcome and the
coverage summary are transient and are described in [data-model.md](./data-model.md).

```mermaid
erDiagram
    SPEC ||--o| GRILLED_ON_LABEL : carries
    SPEC ||--o{ CLARIFICATION : records
    RELEASE ||--|| UPSTREAM_PROVENANCE : ships

    GRILL_SETTING {
        string grill PK "on, strict or off; missing means on"
    }
    SPEC {
        string path PK
        string status
    }
    GRILLED_ON_LABEL {
        string spec_path PK, FK
        date grilled_on
        string state "complete or stopped early"
        int open_points "stopped early only"
    }
    CLARIFICATION {
        string spec_path FK
        date session_date
        string question
        string answer
    }
    KNOWLEDGE_DOC {
        string path PK
        string kind "context file, topic document or decision record"
    }
    RELEASE {
        string version PK
        string archive_url
        string licence "MIT"
    }
    UPSTREAM_PROVENANCE {
        string release_version PK, FK
        string upstream_version "v1.0.1"
        string vendored_sha256
        string speckit_release_verified
    }
```

| Entity | Status | Stored in | Notes |
|--------|--------|-----------|-------|
| GRILL_SETTING | New | Grill Setting File | One line; read textually, never written by the extension |
| SPEC | Existing | Feature Spec | Spec Kit's own artefact; the extension adds the label and Clarifications to it |
| GRILLED_ON_LABEL | New | Feature Spec | At most one per spec, directly under Status |
| CLARIFICATION | Existing | Feature Spec | Upstream's and core clarify's format, unchanged |
| KNOWLEDGE_DOC | Existing | Knowledge Docs | Upstream's rules, unchanged; a Clarifications line may settle entries here, with no stored link between them |
| RELEASE | New | Public repository | Git tag and its archive |
| UPSTREAM_PROVENANCE | New | `upstream/UPSTREAM.md` in each release | Version, hash, licence and update procedure |

## Architecture Impact

| View | Change | Element | Detail |
|------|--------|---------|--------|
| Context | Add | Specify Grill Extension | The system itself: grills a new spec straight after specify |
| Context | Add | Developer | Person; runs specify, answers, skips, stops and resumes |
| Context | Add | Tech Lead | Person; chooses the grill setting |
| Context | Add | Automated Harness | External system; runs specify with no human present and signals it |
| Context | Add | Spec Kit | External system; hosts the extension and dispatches after-specify hooks |
| Context | Add | AI Coding Agent | External system; executes the commands and holds the conversation |
| Context | Add | Upstream Grill Extension | External system; source of the vendored interview, may be installed side by side |
| Context | Add | Other After-Specify Extensions | External system; run after the grill in priority order |
| Containers | Add | Grill Commands | Markdown agent commands: hook entry point, run wrapper, upstream interview |
| Containers | Add | Grill Scripts | Bash: context reader and label writer |
| Containers | Add | Grill Setting File | YAML file holding the one-line setting |
| Containers | Add | Feature Spec | Markdown files: the active spec and its requirements checklist |
| Containers | Add | Knowledge Docs | Markdown files: context file, topic documents, decision records |
| Containers | Add | Grill Commands to Grill Scripts | Gets run context and sets label through, Bash and JSON |
| Containers | Add | Grill Commands to Feature Spec and Knowledge Docs | Reads and updates, File I/O |
| Containers | Add | Grill Scripts to Grill Setting File and Feature Spec | Reads the setting; writes the label, File I/O |
| ERD | Add | GRILL_SETTING, GRILLED_ON_LABEL, RELEASE, UPSTREAM_PROVENANCE | New entities as in the diagram above |
| ERD | Add | SPEC, CLARIFICATION, KNOWLEDGE_DOC | Existing Spec Kit and upstream artefacts, recorded because the extension reads and writes them |
