---
description: Execute the implementation planning workflow using the plan template
  to generate design artifacts, including C4 component, sequence and ER diagrams.
handoffs:
- label: Create Tasks
  agent: speckit.tasks
  prompt: Break the plan into tasks
  send: true
- label: Create Checklist
  agent: speckit.checklist
  prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
  py: scripts/python/setup_plan.py --json
---


<!-- markdownlint-disable-file MD041 -->

> **C4 Model preset: additional Phase 1 deliverable.** This planning run must also
> produce the feature's architecture document, `architecture.md`, as described in
> "C4 Architecture Diagrams" at the end of this command. It is a Phase 1 output
> alongside `data-model.md`, `contracts/` and `quickstart.md`: generate it before
> the post-design Constitution Check, the post-execution hooks and the Completion
> Report, and treat the command as incomplete without it.


<!-- markdownlint-disable-file MD041 -->

> **Integrated TDD: additional Phase 1 deliverable.**
>
> First check that `.specify/extensions/integrated-tdd/scripts/python/tdd_check.py`
> exists. If it does not exist, the `integrated-tdd` extension is not installed: say so
> now and again in the Completion Report, ignore the rest of this note and the
> "Verification Plan" section at the end of this command, and carry on as core Spec Kit
> would.
>
> Otherwise read `.specify/extensions/integrated-tdd/templates/tdd-process-rules.md` in
> full before planning. This planning run must also fill the `## Verification Plan`
> section of the plan, as described in "Verification Plan" at the end of this command.
> It is a Phase 1 output alongside `data-model.md`, `contracts/` and `quickstart.md`:
> fill it before the post-design Constitution Check, the post-execution hooks and the
> Completion Report, and do not report the plan complete while its check fails.


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before planning)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_plan` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Outline.
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Re-evaluate Constitution Check post-design

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.specify/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_plan`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_plan` key.
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue to the Completion Report.
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Mandatory hook** (`optional: false`) — **You MUST emit `EXECUTE_COMMAND:` for each mandatory hook**:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

## Completion Report

Command ends after Phase 1 design. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Define interface contracts** (if project has external interfaces) → `/contracts/`:
   - Identify what interfaces the project exposes to users or other systems
   - Document the contract format appropriate for the project type
   - Examples: public APIs for libraries, command schemas for CLI tools, endpoints for web services, grammars for parsers, UI contracts for applications
   - Skip if project is purely internal (build scripts, one-off tools, etc.)

3. **Create quickstart validation guide** → `quickstart.md`:
   - Document runnable validation scenarios that prove the feature works end-to-end
   - Include prerequisites, setup commands, test/run commands, and expected outcomes
   - Use links or references to contracts and data model details instead of duplicating them
   - Do not include full implementation code, model/service/controller bodies, migrations, or complete test suites
   - Keep this artifact as a validation/run guide; implementation details belong in `tasks.md` and the implementation phase

**Output**: data-model.md, /contracts/*, quickstart.md

## Key rules

- Use absolute paths for filesystem operations; use project-relative paths for references in documentation
- ERROR on gate failures or unresolved clarifications

## Done When

- [ ] Plan workflow executed and design artifacts generated
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with branch, plan path, and generated artifacts


## Verification Plan

This section adds a step to **Phase 1: Design & Contracts**. Run it after `data-model.md`
and `contracts/` are written, because verification takes account of them. Skip it when
the extension is not installed, as the note at the top of this command says.

`IMPL_PLAN` already ends with a `## Verification Plan` section holding three tables. Keep
the heading, the three sub-headings and the three header rows exactly as they are, and
replace the example rows. Follow the "Verification intent" rules in the process rules.

1. **Verification commands**: find how the project already runs its tests, in its package
   scripts, Makefile, CI configuration or contributor documentation. Record each command
   with a short id, the command line in backticks (with `{select}` where a test selector
   goes), a scope of `focused` or `broad`, and where the project defines it. Declare at
   least one `broad` command. If the project has no runnable test command, leave the table
   empty, tell the developer this is a gap to resolve, and do not invent a command or
   choose a test framework.

2. **Verification obligations**: for every functional requirement (`FR-`) and every
   acceptance scenario (`USn-ASm`, scenario `m` of user story `n`) in FEATURE_SPEC, write
   the scenarios that verify it and what must be observed, stated without reference to the
   implementation. Add obligations for edge cases and failure conditions, and for the
   interfaces, data integrity rules, security requirements and integration boundaries in
   the design, in proportion to the scope, risk and complexity of the change. Choose a
   level for each. Number them `VO-001`, `VO-002`, ... and set Origin to `planned`. For a
   small, low-risk change write one obligation per requirement and per acceptance
   scenario, and no more: not one per assertion, and not for a property the specification
   does not state.

3. **Verification exemptions**: for a requirement that cannot sensibly be verified
   automatically, add a row with the reason and how it is verified instead. Write a single
   `None` row when there are no exemptions.

4. **Material ambiguity**: if a requirement is ambiguous, or contradicts another, in a way
   that changes what a test should assert, stop and ask the developer. Do not choose an
   interpretation. Leave that requirement without an obligation until the question is
   answered, record the answer under `## Clarifications` in FEATURE_SPEC, and then write
   the obligation.

5. **Check**: from the repository root run

   ```bash
   python3 .specify/extensions/integrated-tdd/scripts/python/tdd_check.py plan
   ```

   Each finding names a rule and a requirement or obligation. Correct the Verification
   Plan and run the check again until it exits 0. Do not report the plan complete while it
   exits non-zero: say which findings remain and why, for example a question waiting for
   the developer or a project with no test command.

In the Completion Report, state the number of obligations and exemptions, the verification
commands found and where they came from, and the result of the check.


## C4 Architecture Diagrams

This section adds a step to **Phase 1: Design & Contracts**. Run it after
`data-model.md` and `contracts/` are written, because the diagrams are derived from
them.

**Locations.** Read `.specify/extensions/c4/c4-config.yml` if it exists; otherwise
use `architecture_dir: docs/architecture`, `feature_file: architecture.md` and
`mermaid_cli: mmdc`.
`ARCH_DIR` is `architecture_dir` from the repository root. `FEATURE_ARCH` is
`<feature_file>` in the feature directory, next to IMPL_PLAN.

**If `.specify/extensions/c4/templates/` does not exist**, the `c4` extension is not
installed. Skip this section, leave the plan's `## Architecture` section as
`Not generated: c4 extension not installed`, and say so in the Completion Report.

1. **Read the rules**: read `.specify/extensions/c4/templates/c4-conventions.md` in
   full. Every diagram must follow it.

2. **Load the system views**: read `ARCH_DIR/context.md`, `ARCH_DIR/containers.md`
   and `ARCH_DIR/erd.md` when they exist and reuse their element aliases, labels and
   technologies exactly. If they do not exist, treat every container and entity as
   new.

3. **Generate `FEATURE_ARCH`** from
   `.specify/extensions/c4/templates/c4-feature-architecture-template.md`:
   - **Header**: feature name, branch, date, and relative links to the spec, plan,
     data model, contracts and the three system views. Drop links to artifacts this
     run did not produce.
   - **Components**: one `C4Component` diagram and component table per container
     this feature adds or changes, consistent with Technical Context and the source
     tree in Project Structure. Choose each diagram's declaration order with the
     "Layout optimisation" procedure in the conventions, using
     `python3 .specify/extensions/c4/scripts/python/c4_layout.py optimise` with
     `--mmdc "<mermaid_cli>"`.
   - **Flows**: one `sequenceDiagram` per user story's primary path, in priority
     order, plus architecturally significant alternate or failure paths. Message
     labels match `contracts/`. Name the user story and the requirements covered.
   - **Data**: one `erDiagram` with every entity in `data-model.md`, with
     attributes, keys and relationships. Write `Not applicable: [reason]` if the
     feature has no persistent data.
   - **Architecture Impact**: every difference between these diagrams and the system
     views.
   - Leave no placeholder text and none of the template's example content.

4. **Fill the plan's `## Architecture` section** in IMPL_PLAN: correct relative
   links and a one-line impact per view.

5. **Fill the spec's `## System Context` section** in FEATURE_SPEC only if it still
   contains unfilled placeholders: set the link to `ARCH_DIR/context.md` and list
   the people and external systems from the spec. Make no other change to the spec.

6. **Extend the outputs**:
   - Add `architecture.md` to the documentation tree under "Project Structure" in
     IMPL_PLAN, as a Phase 1 output.
   - Include `FEATURE_ARCH` among the generated artifacts in the Completion Report,
     with the count of component, sequence and ER diagrams and, per component
     diagram, whether its layout was rendered and already sufficient, rendered and
     optimised, or not checked.

Do not edit the project-level views in `ARCH_DIR` during planning. They are updated
from the Architecture Impact table by `__SPECKIT_COMMAND_C4_SYSTEM__` once the
feature is implemented.
