#!/usr/bin/env bash
# Rebuild the marked upstream region of the grill command from the vendored upstream copy
# and the recorded patch. Text outside the markers is left untouched. If the command file
# does not exist yet, it is created with frontmatter and the two markers.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENDORED="$ROOT/upstream/with-docs.v1.0.1.md"
PATCH="$ROOT/upstream/nested-hooks.patch"
TARGET="$ROOT/commands/speckit.grill-specify.with-docs.md"
BEGIN='<!-- BEGIN UPSTREAM grill v1.0.1 -->'
END='<!-- END UPSTREAM -->'

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Upstream body: everything after the frontmatter's closing --- line, trimmed of blank lines.
awk 'BEGIN{n=0} n>=2{print} /^---$/{n++}' "$VENDORED" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}' > "$TMP/body.raw"
awk 'NF{started=1} started{print}' "$TMP/body.raw" > "$TMP/body.md"
patch --quiet -o "$TMP/region.md" "$TMP/body.md" "$PATCH"

if [ ! -f "$TARGET" ]; then
  mkdir -p "$(dirname "$TARGET")"
  {
    printf -- '---\n'
    printf 'description: "Grill the active feature spec with no question limit and save settled terms and decisions to the knowledge docs; also resumes a grill that was stopped early"\n'
    printf -- '---\n\n'
    printf '%s\n\n' "$BEGIN"
    printf '%s\n\n' "$END"
  } > "$TARGET"
fi

grep -q -F "$BEGIN" "$TARGET" || { echo "missing begin marker" >&2; exit 1; }
grep -q -F "$END" "$TARGET" || { echo "missing end marker" >&2; exit 1; }

awk -v begin="$BEGIN" -v end="$END" -v region="$TMP/region.md" '
  $0 == begin { print; print ""; while ((getline line < region) > 0) print line; print ""; skipping = 1; next }
  $0 == end   { skipping = 0 }
  !skipping   { print }
' "$TARGET" > "$TMP/out.md"
cat "$TMP/out.md" > "$TARGET"
echo "region rebuilt in $TARGET"
