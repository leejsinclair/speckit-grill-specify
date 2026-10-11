# Contract: Commands

Two commands, both in the extension's own namespace. In Claude Code they are installed as
the project skills `speckit-grill-specify-with-docs` and `speckit-grill-specify-auto`.

## `speckit.grill-specify.auto`

The `after_specify` hook entry point. Not meant to be typed by a developer.

| Aspect | Contract |
|--------|----------|
| Invoked by | specify's Mandatory Post-Execution Hooks, as `EXECUTE_COMMAND: speckit.grill-specify.auto` |
| Arguments | None |
| Does | Invokes `speckit.grill-specify.with-docs` in the same session with the argument `--nested`, and waits for it to finish |
| Returns to specify | The outcome block of [outcome-report.md](./outcome-report.md), to be carried into specify's Completion Report unchanged |
| Writes | Nothing itself |
| Must not | Invoke any specify hook, ask the developer anything itself, or stop the remaining after-specify hooks (FR-006, FR-023) |

## `speckit.grill-specify.with-docs`

The grill. Runs standalone, and nested when called by the entry point.

### Arguments

| Form | Meaning |
|------|---------|
| *(empty)* | Standalone run |
| `<area>` | Standalone run; `<area>` is passed to upstream's User Input as the area to prioritise |
| `--nested` | Nested run. The token must be first; anything after it is ignored |

### Steps the wrapper adds before the upstream interview

1. Decide the kind of run from the arguments, and remove `--nested` from them.
2. Run `grill-context.sh --json` once and read the run context.
3. If `interactive` is false: ask nothing, change nothing, report
   `not run (no human present)` and end (FR-007). This applies to both kinds of run.
4. Nested only: if `setting` is `off`, change nothing, report `switched off` and end
   (FR-012).
5. Run upstream's Prerequisites and Step 1 scan and Step 2 fact gate **without writing
   any file**. Facts that investigation would write into the spec (upstream Step 4B) are
   held until the developer's first answer (FR-011).
6. Open: state how many points were found to settle and present the first question in
   upstream's question format.
   - Nested with `setting` `on`: add a skip choice to the opening, with one line saying
     the spec is left untouched and how to run the grill later.
   - Nested with `setting` `strict`, and every standalone run: no skip choice (FR-012,
     FR-013).
   - Nothing to settle: say so and go to upstream's satisfaction gate (FR-024). The skip
     choice, where it applies, is still offered.
7. If the developer takes the skip choice: change nothing, report `skipped`, end.
8. If the developer stops before answering anything: change nothing, report
   `stopped early` with every point outstanding, end (FR-014).

### Rules the wrapper adds during and after the interview

- After each answer that upstream saves (Step 4A), run
  `grill-label.sh --state stopped --open <n>` with the current number of open points
  (FR-021). The held Step 4B facts are written with the first answer.
- When the developer confirms satisfaction at upstream's Step 6 gate, run
  `grill-label.sh --state complete` (FR-021, FR-024).
- If `warning` in the run context is not empty, repeat it as one line in the report
  (FR-012).
- Nested run: do not process `before_clarify` or `after_clarify` hooks, on the normal
  path or the interrupted path, and do not process any specify hook. Standalone run:
  process the clarify hooks exactly as upstream does (FR-006).
- Nested run: finish with the outcome block. Standalone run: finish with upstream's Step
  8 completion report, with the label line and any warning added.
- Write only the active spec, the checkbox states of its requirements checklist, and the
  resolved knowledge docs (FR-008).

### The one change inside the upstream region

Upstream's section "Extension hooks (same processing as clarify)" begins with one added
paragraph: in a nested run this section does not apply and no clarify hook is processed;
in a standalone run it applies as written. Step 5 of upstream's Interrupted completion
path and its Step 8 refer to that section and so inherit the rule. Nothing else between
the markers differs from upstream v1.0.1 (FR-022).

### Errors

| Condition | Behaviour |
|-----------|-----------|
| No active feature, or no spec | Stops with a clear message and changes nothing (upstream Prerequisites 2 and 3) |
| Not macOS or Linux, or no `bash` | Stops as unsupported (upstream Prerequisite 1) |
| A knowledge doc cannot be saved or verified | Upstream's Persistence incomplete rules: the point is not Resolved, the failure is reported, the run stops |
| The spec has no `**Status**:` line | The label cannot be placed; the failure is reported and the answer's point is not counted as labelled |
