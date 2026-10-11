# Contract: Scripts

Both scripts are Bash, need only standard POSIX tools, run on macOS and Linux, and are
called from the repository root of the project that installed the extension.

## `grill-context.sh`

```text
bash .specify/extensions/grill-specify/scripts/bash/grill-context.sh --json
```

Reads the grill setting and the non-interactive signals. Writes no file. Always exits 0
and prints exactly one JSON object on standard output.

```json
{
  "setting": "on",
  "setting_source": "default",
  "warning": "",
  "interactive": true,
  "interactive_reason": "no-signal"
}
```

### Setting

Read from `.specify/extensions/grill-specify/grill-specify-config.yml`, or from the path
in `SPECKIT_GRILL_CONFIG` when that is set (used by tests).

| Config state | `setting` | `setting_source` | `warning` |
|--------------|-----------|------------------|-----------|
| File missing, or no `grill:` line | `on` | `default` | empty |
| `grill: on`, `"on"`, `'on'`, `ON` | `on` | `config` | empty |
| `grill: strict` | `strict` | `config` | empty |
| `grill: off` | `off` | `config` | empty |
| Any other value, for example `grill: of` | `on` | `default` | `Grill setting "of" is not one of on, strict, off; using on.` |
| File exists but cannot be read | `on` | `default` | `Grill setting file could not be read; using on.` |

Only the first `grill:` line outside comments counts. Quotes, surrounding space and a
trailing `# comment` are removed before comparison.

### Interactivity

| Signal, checked in this order | `interactive` | `interactive_reason` |
|-------------------------------|---------------|----------------------|
| `SPECKIT_GRILL_NONINTERACTIVE` is `1`, `true` or `yes` | `false` | `switch` |
| `SPECKIT_GRILL_NONINTERACTIVE` is `0`, `false` or `no` | `true` | `switch` |
| `CLAUDE_CODE_SESSION_ATTENDED` is `0`, or `CLAUDE_CODE_ENTRYPOINT` begins `sdk-` | `false` | `agent` |
| None of the above | `true` | `no-signal` |

Switch values are compared without regard to case. Any other value of the switch is
ignored, as though it were unset.

## `grill-label.sh`

```text
bash .specify/extensions/grill-specify/scripts/bash/grill-label.sh \
    --spec <path to spec.md> --state stopped --open <n>
bash .specify/extensions/grill-specify/scripts/bash/grill-label.sh \
    --spec <path to spec.md> --state complete
```

Writes or refreshes the grilled-on label in the named spec and changes nothing else in
it.

| Option | Rules |
|--------|-------|
| `--spec` | Required; an existing file |
| `--state` | Required; `stopped` or `complete` |
| `--open` | Required with `stopped`, a whole number of 0 or more; not allowed with `complete` |
| `--date` | Optional `YYYY-MM-DD`; defaults to today (used by tests) |

### Result

- `--state complete` writes `**Grilled on**: 2026-10-11`.
- `--state stopped --open 4` writes
  `**Grilled on**: 2026-10-11 (stopped early, 4 points open)`; with `--open 1` the word
  is `point`.
- If the spec already has a `**Grilled on**:` line, that line is replaced in place.
- Otherwise the label is inserted directly under the first `**Status**:` line, separated
  from it by one blank line and followed by one blank line, matching the header's own
  spacing.
- Every other byte of the spec is unchanged. Running the same command twice gives the
  same file.

### Exit status

| Status | Meaning |
|--------|---------|
| 0 | Label written; prints the label line |
| 2 | Bad arguments; nothing written |
| 3 | Spec not found, not writable, or has no `**Status**:` line; nothing written |
