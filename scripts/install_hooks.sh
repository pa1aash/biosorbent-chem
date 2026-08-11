#!/usr/bin/env bash
# Install the Chem-151 git hooks. Run once after a fresh clone:
#     bash scripts/install_hooks.sh
#
# Hooks live in .git/hooks/, which git does not track, so they do not survive a clone.
# This script is the mechanism that makes them survive.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOK_DIR="$REPO_ROOT/.git/hooks"
mkdir -p "$HOOK_DIR"

# ── commit-msg ────────────────────────────────────────────────────────────────
# Strips any line attributing authorship or co-authorship to an assistant.
# Every commit in this repository is authored by Palaash Gang alone.
cat > "$HOOK_DIR/commit-msg" <<'HOOK'
#!/usr/bin/env bash
# Chem-151 commit-msg hook.
# Removes attribution lines. See CLAUDE.md section 2.1 (ABSOLUTE RULE - ATTRIBUTION).
set -euo pipefail

MSG_FILE="$1"
[ -f "$MSG_FILE" ] || exit 0

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

# Drop any line matching an attribution pattern (case-insensitive).
#   Co-Authored-By:      trailer form
#   Generated with       "Generated with [Claude Code]" form
#   the robot emoji      the marker that precedes it
#   Claude / Anthropic   any residual mention
grep -viE \
  -e '^[[:space:]]*co-authored-by:' \
  -e 'generated with' \
  -e $'\xf0\x9f\xa4\x96' \
  -e 'claude' \
  -e 'anthropic' \
  "$MSG_FILE" > "$TMP" || true

# Collapse any trailing blank lines the removal left behind.
awk 'BEGIN{n=0} {lines[NR]=$0} END{ last=NR; while(last>0 && lines[last] ~ /^[[:space:]]*$/) last--; for(i=1;i<=last;i++) print lines[i] }' "$TMP" > "$MSG_FILE"

exit 0
HOOK

chmod +x "$HOOK_DIR/commit-msg"
echo "installed: $HOOK_DIR/commit-msg"

# ── self-test ─────────────────────────────────────────────────────────────────
# Prove the hook works rather than assuming it does.
TESTMSG="$(mktemp)"
trap 'rm -f "$TESTMSG"' EXIT
cat > "$TESTMSG" <<'EOF'
Add the isotherm fitting module

Implements non-linear Langmuir and Freundlich regression.

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
EOF

"$HOOK_DIR/commit-msg" "$TESTMSG"

if grep -qiE 'co-authored-by|generated with|claude|anthropic' "$TESTMSG"; then
    echo "SELF-TEST FAILED: attribution survived the hook." >&2
    cat "$TESTMSG" >&2
    exit 1
fi

echo "self-test passed: attribution lines are stripped."
echo
echo "Resulting message body:"
sed 's/^/    | /' "$TESTMSG"
