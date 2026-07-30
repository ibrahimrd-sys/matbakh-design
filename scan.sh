#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Matbakh — leak audit. Run before making the repository public, and any time
# you are unsure.
#
#     ./scan.sh
#
# Checks three places, because they fail differently:
#
#   the working folder — what is sitting here right now
#   what git is tracking — ignored files are invisible until they are not
#   the commit history — the one that cannot be fixed by deleting a file
# ─────────────────────────────────────────────────────────────────────────────
set -uo pipefail
cd "$(dirname "$0")"

RED="$(printf '\033[31m')"; GRN="$(printf '\033[32m')"; YEL="$(printf '\033[33m')"; OFF="$(printf '\033[0m')"
ISSUES=0
bad()  { echo "${RED}  FOUND ${OFF} $1"; ISSUES=$((ISSUES+1)); }
good() { echo "${GRN}  clear ${OFF} $1"; }
warn() { echo "${YEL}  check ${OFF} $1"; }

DOC_RE='\.(xlsx|xlsm|xls|docx|doc|pptx|ppt|numbers|pages)$'
CRED_RE='(^|/)\.env|secret|credential|password|api[-_]?key|\.pem$|\.p12$|id_rsa'
SECRET_RE='BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}'

echo "═══ 1. the working folder ═══"
HITS=$(find . -path ./.git -prune -o -type f -print 2>/dev/null | grep -Ei "$DOC_RE" || true)
[ -n "$HITS" ] && echo "$HITS" | while read -r f; do bad "$f — move to ../matbakh-private/"; done || good "no business documents present"
[ -n "$HITS" ] && ISSUES=$((ISSUES+1))

HITS=$(find . -path ./.git -prune -o -type f -print 2>/dev/null | grep -Ei "$CRED_RE" || true)
[ -n "$HITS" ] && echo "$HITS" | while read -r f; do bad "$f — credential-shaped filename"; done || good "no credential-shaped filenames"

N=$(find content/recipes -name '*.yaml' 2>/dev/null | grep -vE '_template|molokhia_bil_farakh' | wc -l | tr -d ' ')
if [ "${N:-0}" -gt 0 ]; then bad "$N recipe file(s) beyond template + demo — catalogue belongs in the vault"
else good "recipe catalogue not present (template + demo only)"; fi

if [ -d ../matbakh-private ]; then
  if [ -d ../matbakh-private/.git ]; then bad "the vault is a git repository — rm -rf ../matbakh-private/.git"
  else good "vault sits outside this folder and is not a repository"; fi
else warn "no ../matbakh-private/ found — is the vault where it should be?"; fi

echo
echo "═══ 2. what git is tracking ═══"
if [ ! -d .git ]; then
  warn "no repository yet — nothing tracked, nothing pushed. This is the safest"
  warn "moment to get the layout right."
else
  T=$(git ls-files | grep -Ei "$DOC_RE|$CRED_RE" || true)
  [ -n "$T" ] && echo "$T" | while read -r f; do bad "TRACKED: $f"; done || good "nothing sensitive is tracked"

  T=$(git ls-files | grep -E '^content/recipes/' | grep -vE '_template|molokhia_bil_farakh' || true)
  [ -n "$T" ] && echo "$T" | while read -r f; do bad "TRACKED: $f"; done || good "no catalogue files tracked"

  for f in $(git ls-files); do
    case "$f" in *.png|*.jpg|*.jpeg|*.webm|*.woff*|.githooks/*|scan.sh|publish.sh|README.md) continue ;; esac
    [ -f "$f" ] || continue
    sed -E 's#data:[a-z/+.-]+;base64,[A-Za-z0-9+/=_-]*#<base64-payload>#g' "$f" 2>/dev/null \
      | grep -Eqi "$SECRET_RE" && bad "TRACKED: $f contains a secret-shaped string"
  done

  if [ "$(git config core.hooksPath)" = ".githooks" ]; then good "pre-commit hook is active"
  else bad "pre-commit hook NOT active — run ./setup-guards.sh"; fi
fi

echo
echo "═══ 3. commit history ═══"
if [ ! -d .git ]; then
  good "no history to audit"
else
  H=$(git log --all --pretty=format: --name-only --diff-filter=A 2>/dev/null | sort -u | grep -Ei "$DOC_RE|$CRED_RE" || true)
  if [ -n "$H" ]; then
    echo "$H" | while read -r f; do bad "IN HISTORY: $f"; done
    cat <<'EOF'

  A file in history is still retrievable after you delete it. If any of the
  above ever reached GitHub, treat the contents as public: rotate every key,
  and rewrite history with git-filter-repo before making the repo public.
EOF
  else good "history contains nothing sensitive"; fi
fi

echo
if [ "$ISSUES" -eq 0 ]; then
  echo "${GRN}Audit clean.${OFF} Safe to publish as far as this script can tell."
else
  echo "${RED}$ISSUES issue(s).${OFF} Resolve before making the repository public."
  exit 1
fi
