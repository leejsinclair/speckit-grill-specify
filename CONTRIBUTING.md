# Contributing

## Prerequisites

- Spec Kit CLI 1.1.3 or later (`specify --version`), Python 3.9+, Bash, `patch`.
- For live tests: the `claude` CLI, signed in.

## Tests

| Command | Covers |
|---------|--------|
| `make test` | Structure and install levels; no agent, no network |
| `make test-one T=tests.structure.test_manifest` | One module, class or test |
| `make test-live` | Behaviour and regression levels; drives Claude Code with `claude -p` |
| `make test-release` | Installs from the published tag archive; needs network |

Live tests use Haiku unless `GRILL_TEST_MODEL` names another model, and set
`SPECKIT_GRILL_NONINTERACTIVE=0` unless a test is about an unattended run. Set
`GRILL_TEST_LOG=<file>` to append every scripted turn to a file. `GRILL_TEST_BASH` names a
Bash binary, for example a Bash 3.2, to run the script tests through.

Install and live tests create their project in a temporary directory outside the
repository. Never edit the text between the upstream markers by hand: change
`upstream/nested-hooks.patch` and run `scripts/dev/sync-upstream.sh`.

## Release

1. Update `extension.yml`, `CHANGELOG.md` and the tag in README's archive URL together.
2. Run `make test` and `make test-live`.
3. Commit, tag `v<version>`, push the tag, then run `make test-release`.
