# Contract: Outcome Report

Every nested run ends by printing one outcome block. The entry-point command tells the
agent to place it in specify's Completion Report unchanged (FR-014). A standalone run
does not print this block; it ends with upstream's completion report.

## Form

````text
```text
GRILL OUTCOME: <outcome>
<field>: <value>
...
```
````

The first line is fixed and is what tests look for. `<outcome>` is exactly one of:

- `completed`
- `stopped early`
- `skipped`
- `switched off`
- `not run (no human present)`

## Fields by outcome

| Field | completed | stopped early | skipped | switched off | not run |
|-------|:---------:|:-------------:|:-------:|:------------:|:-------:|
| `Spec` (path) | yes | yes | yes | yes | yes |
| `Label` (the label line, or `none`) | yes | yes | `none` | `none` | `none` |
| `Questions answered` | yes | yes | - | - | - |
| `Coverage` (category: status, one per line) | yes | yes | - | - | - |
| `Knowledge docs changed` (paths, or `none`) | yes | yes | - | - | - |
| `Checklist` (before → after pass counts) | yes | yes | - | - | - |
| `Outstanding points` (point: reason, one per line) | if any | yes | - | - | - |
| `Resume with` (the standalone command) | - | yes | yes | - | yes |
| `Reason` | - | - | `skipped by the developer` | `the grill setting is off` | the signal that marked the run, and `the spec has not been clarified` |
| `Warning` (bad setting value) | if any | if any | if any | - | if any |

`Resume with` names the standalone command as the current agent spells it, for example
`/speckit-grill-specify-with-docs` in Claude Code.

## Guarantees

- Exactly one block per nested run, with exactly one outcome.
- `skipped`, `switched off` and `not run` are reported only when the grill changed no
  file.
- `stopped early` before the first answer reports `Label: none`,
  `Questions answered: 0`, `Knowledge docs changed: none` and lists every point as
  outstanding.
- The block is the last thing the grill prints, so the remaining after-specify hooks run
  after it (FR-023).
