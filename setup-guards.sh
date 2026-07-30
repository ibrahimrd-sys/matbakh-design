#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Matbakh — install the guards. Run once, from inside matbakh-design/.
#
#     ./setup-guards.sh
#
# Sets three independent nets. Independent matters: any one of them can be
# misconfigured without the others failing with it.
#
#   1. .gitignore        — stops the obvious things being staged at all
#   2. pre-commit hook   — stops a commit whatever tool made it
#   3. global gitignore  — applies to every repo on this machine, so a stray
#                          `git init` in the vault is still partly covered
#
# The strongest protection is not any of these. It is that the vault sits
# outside the repository folder, so git never sees it in the first place.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"

echo "── 0/4  executable bits"
# Downloads, zip extraction and some archive tools drop the +x bit. Restore it
# here so this is the only script that ever needs `bash` in front of it.
chmod +x publish.sh scan.sh setup-guards.sh .githooks/pre-commit 2>/dev/null || true
echo "   publish.sh, scan.sh, setup-guards.sh, .githooks/pre-commit"

echo
echo "── 1/4  repository check"
if [ ! -d .git ]; then
  echo "   no git repository here yet — run 'git init' first, then rerun this."
  exit 1
fi
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "   git will not read this repository. Its own message:"
  git rev-parse --is-inside-work-tree 2>&1 | sed 's/^/     /'
  echo
  echo "   Usually this is 'dubious ownership' — the files belong to a different"
  echo "   user than the one running git, which happens after extracting an"
  echo "   archive as root or working on a network drive. Fix with the command"
  echo "   git suggests above, or move the folder somewhere you own."
  exit 1
fi
echo "   ok"

echo
echo "── 2/4  pre-commit hook"
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
echo "   hooksPath → .githooks (tracked in the repo, so it survives a fresh clone)"

echo
echo "── 3/4  global ignore rules"
GI="${HOME}/.gitignore_global"
touch "$GI"
add() { grep -qxF "$1" "$GI" || echo "$1" >> "$GI"; }
add "# Matbakh — added by setup-guards.sh"
add "matbakh-private/"
add "DO-NOT-COMMIT*"
add "*.xlsx"
add "*.xlsm"
add "*.docx"
add "*.pptx"
add ".env"
add ".env.*"
add "*.pem"
add "*.p12"
add "id_rsa*"
git config --global core.excludesfile "$GI"
echo "   $GI applies to every repository on this machine"

echo
echo "── 4/4  vault check"
VAULT="../matbakh-private"
if [ ! -d "$VAULT" ]; then
  echo "   WARNING: $VAULT not found. The vault should sit beside this folder,"
  echo "   not inside it. See ../README.md."
elif [ -d "$VAULT/.git" ]; then
  echo "   WARNING: $VAULT contains a .git folder. The vault must never be a"
  echo "   git repository. Remove it: rm -rf $VAULT/.git"
else
  echo "   vault present, and correctly not a git repository"
fi

echo
echo
echo "── 5/5  environment"
if command -v python3 >/dev/null 2>&1; then echo "   python3 found"
elif command -v python >/dev/null 2>&1; then echo "   python found (no python3 — normal on Windows)"
elif command -v py >/dev/null 2>&1; then echo "   py launcher found"
else echo "   WARNING: no Python on PATH. build.py will not run."; fi
python3 -c "import yaml" 2>/dev/null || python -c "import yaml" 2>/dev/null \
  || echo "   WARNING: PyYAML missing. Install it:  pip install pyyaml"
case "$(uname -s 2>/dev/null)" in
  MINGW*|MSYS*|CYGWIN*)
    echo "   Git Bash detected — correct shell for these scripts on Windows" ;;
esac

echo
echo "Guards installed. Verify with:  ./scan.sh"
