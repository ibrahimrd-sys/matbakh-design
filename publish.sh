#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Matbakh design — publish.
#
#   ./publish.sh "moved the timer band to the right edge"
#
# Runs preflight, regenerates index.html, then commits and pushes. Refuses to
# push if preflight finds an error, and refuses to push anything the vault was
# meant to hold. One command, so "keep it updated" does not depend on
# remembering four.
#
# On Windows, run this from Git Bash (installed with Git for Windows), not from
# PowerShell or cmd.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"

MSG="${1:-}"
if [ -z "$MSG" ]; then
  echo "usage: ./publish.sh \"what changed\""
  exit 1
fi

# Python is python3 on macOS and Linux, often just python on Windows, and
# sometimes only reachable through the py launcher.
find_python() {
  for c in python3 python py; do
    if command -v "$c" >/dev/null 2>&1; then
      if [ "$c" = "py" ]; then echo "py -3"; else echo "$c"; fi
      return 0
    fi
  done
  return 1
}
PY=$(find_python) || { echo "no Python found on PATH — install Python 3 and retry"; exit 1; }

echo "── 1/5  preflight and build"
$PY build.py

echo
echo "── 2/5  release stamp"
REL=$(date +%Y.%m.%d)
if ! grep -q "release: \"$REL\"" manifest.yaml; then
  echo "   manifest release is not today's date ($REL)."
  echo "   Bump 'release:' in manifest.yaml and add a CHANGELOG entry, then rerun."
  exit 1
fi

echo
echo "── 3/5  leak check"
# Belt and braces behind .githooks/pre-commit. Deliberately written with plain
# grep -v rather than a negative lookahead: lookaheads are not valid in POSIX
# ERE, and an invalid pattern makes a guard that silently never fires.
STAGE=$(git status --porcelain 2>/dev/null | sed 's/^...//' || true)
BLOCKED=""
add_blocked() { [ -n "$1" ] && BLOCKED="${BLOCKED}$1
"; return 0; }

add_blocked "$(echo "$STAGE" | grep -Ei '\.(xlsx|xlsm|xls|docx|doc|pptx|ppt)$' || true)"
add_blocked "$(echo "$STAGE" | grep -Ei '(^|/)\.env|\.pem$|\.p12$|id_rsa|secret|credential|password' || true)"
add_blocked "$(echo "$STAGE" | grep -Ei 'matbakh-private|DO-NOT-COMMIT' || true)"
add_blocked "$(echo "$STAGE" | grep -E '^content/recipes/' \
                             | grep -vE '_template\.yaml$|molokhia_bil_farakh\.yaml$|README\.md$' || true)"

BLOCKED=$(echo "$BLOCKED" | grep -v '^$' || true)
if [ -n "$BLOCKED" ]; then
  echo "   REFUSING TO PUBLISH — these belong in ../matbakh-private/:"
  echo "$BLOCKED" | sed 's/^/     /'
  exit 1
fi
echo "   clear"

echo
echo "── 4/5  commit"
if [ -z "$(git status --porcelain)" ]; then
  echo "   nothing changed; already published"
  exit 0
fi
git add -A
# The pre-commit hook runs here and is the real gate. If it stops the commit,
# set -e stops this script, and nothing is pushed.
git commit -q -m "$MSG" -m "Release $REL"
echo "   committed: $MSG"

echo
echo "── 5/5  push"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git push -q origin "$BRANCH"
echo "   pushed to origin/$BRANCH"
echo
echo "Pages will rebuild in about a minute."
git remote get-url origin 2>/dev/null \
  | sed -E 's#.*github.com[:/]([^/]+)/(.+)(\.git)?$#   https://\1.github.io/\2/#' || true
