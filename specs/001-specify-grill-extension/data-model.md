# Data Model: Specify Grill Extension

**Feature**: `001-specify-grill-extension` | **Date**: 2026-10-11

The extension has no database. Its data is a handful of files in the project that
installs it, plus values that exist only for the length of one run. Persistent items are
marked **stored**; the rest are **transient** and are never written to a file.

## Grill setting (stored)

One line in `.specify/extensions/grill-specify/grill-specify-config.yml`.

| Field | Type | Rules |
|-------|------|-------|
| `grill` | string | One of `on`, `strict`, `off`; compared without regard to case, quotes optional |

- Missing file or missing key: treated as `on`, no warning.
- Any other value, or an unreadable file: treated as `on`, with a one-line warning that
  names the bad value (FR-012).
- Governs only a nested run (FR-013). Never written by the extension (FR-008).

## Run context (transient)

The JSON object printed by `grill-context.sh`; see
[contracts/scripts.md](./contracts/scripts.md).

| Field | Type | Rules |
|-------|------|-------|
| `setting` | string | `on`, `strict` or `off`, after the fallback rules above |
| `setting_source` | string | `config` or `default` |
| `warning` | string | Empty, or the one-line warning for a bad value |
| `interactive` | boolean | False only when an explicit signal says so (FR-007) |
| `interactive_reason` | string | `switch`, `agent` or `no-signal` |

## Grill run (transient)

| Field | Type | Rules |
|-------|------|-------|
| kind | enum | `nested` (started by specify) or `standalone` |
| setting | enum | From the run context; ignored when kind is `standalone` |
| open points | integer | Decision points not yet at a final status; shown at the opening and in the label |
| saved answers | integer | Count of answers saved in this run; the label exists once this is 1 or more |
| outcome | enum | See Grill outcome |

**State transitions**

```text
start ──setting off (nested)──────────────────────────▶ switched off
start ──non-interactive────────────────────────────────▶ not run (no human present)
start ──▶ opening ──skip choice (nested, setting on)───▶ skipped
          opening ──stop before first answer───────────▶ stopped early   (no file changed)
          opening ──first answer saved──▶ interviewing  (label written, stopped-early form)
          opening ──nothing to settle──▶ satisfaction gate
interviewing ──answer saved──▶ interviewing             (label refreshed)
interviewing ──stop──────────────────────────────────▶ stopped early   (label kept)
interviewing ──all points final──▶ satisfaction gate
satisfaction gate ──explore further──▶ interviewing
satisfaction gate ──concerns remain, stop here────────▶ stopped early
satisfaction gate ──finish────────────────────────────▶ completed       (label, plain form)
```

A standalone run has no `switched off` or `skipped` transition and reports through
upstream's completion report.

## Grill outcome (transient, reported)

Exactly one per nested run (FR-014); see
[contracts/outcome-report.md](./contracts/outcome-report.md).

| Outcome | Files changed | Label after the run | Report must include |
|---------|---------------|---------------------|---------------------|
| completed | spec, checklist checkboxes, knowledge docs as settled | Plain form | Coverage summary, knowledge docs changed |
| stopped early | As above, up to the stop; none if stopped before the first answer | Stopped-early form, or none if no answer was saved | Coverage summary, knowledge docs changed, outstanding points, how to resume |
| skipped | None | None | That the developer skipped, how to run later |
| switched off | None | None | That the grill setting is off |
| not run (no human present) | None | None | Why, and that the spec is not clarified |

## Grilled-on label (stored)

One line in the spec header, directly under `**Status**:` (FR-021).

| Field | Type | Rules |
|-------|------|-------|
| date | date | `YYYY-MM-DD`, the day of the run that last wrote it |
| state | enum | `complete` (no suffix) or `stopped early` |
| open points | integer | Present only in the stopped-early state; 0 or more |

- Forms: `**Grilled on**: 2026-10-11` and
  `**Grilled on**: 2026-10-11 (stopped early, 4 points open)`.
- At most one per spec. A later run replaces it.
- Absent on a spec that was skipped, switched off, not run, or stopped before the first
  answer.

## Clarifications record (stored, upstream's format)

In the spec, under `## Clarifications` and `### Session YYYY-MM-DD`: one line per accepted
answer, `- Q: <question> → A: <settled answer>`. It is the basis for resuming: what it
settles is not asked again (FR-015).

## Coverage summary (transient, reported)

Upstream's coverage map as reported: for each of the ten categories an aggregate status
(`Clear`, `Resolved`, `Outstanding`, `Deferred`) with a per-point breakdown. Not written
to any file.

## Canonical knowledge docs (stored, upstream's rules)

At the project's resolved location, by default `docs/domain_knowledge/`.

| Item | Location | Rules |
|------|----------|-------|
| Context file | `CONTEXT.md` | Glossary and entry point; one canonical definition per term |
| Topic document | `<kebab-case-topic>.md` | Only when the glossary cannot hold the rules; linked from the context file |
| Decision record | `adr/NNNN-<kebab-case-decision>.md` | Only when all three recording conditions hold; numbered one above the highest |

Created only when the first item is settled; never pre-created empty.

## Upstream provenance record (stored, shipped)

`upstream/UPSTREAM.md` in the extension.

| Field | Value at first release |
|-------|------------------------|
| Upstream repository | `https://github.com/yoshi1220/speckit-grill-me` |
| Upstream version | `v1.0.1` |
| Vendored file | `upstream/with-docs.v1.0.1.md`, with its SHA-256 |
| Recorded change | `upstream/nested-hooks.patch` |
| Licence | MIT, notice in `upstream/LICENSE.upstream` |
| Spec Kit release verified | `v1.1.3` on 2026-10-11 |
| Update procedure | Steps to fetch a later upstream tag, re-apply the patch and rebuild the region |

## Release (stored, published)

| Field | Rules |
|-------|-------|
| version | Semantic version in `extension.yml`; equals the Git tag without its `v` |
| archive URL | `https://github.com/leejsinclair/speckit-grill-specify/archive/refs/tags/v<version>.zip` |
| changelog entry | Latest entry in `CHANGELOG.md` names the same version |
| licence | MIT |

## Relationships

- A **spec** has zero or one **grilled-on label** and zero or more **Clarifications**
  lines.
- A **grill run** reads one **grill setting** (nested only) and produces exactly one
  **grill outcome** (nested only) and one **coverage summary** (when an interview ran).
- A **Clarifications** line may settle zero or more **knowledge doc** entries.
- A **release** carries exactly one **upstream provenance record**.
