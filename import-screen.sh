#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# Matbakh — import a screen from Claude Design.
#
#     ./import-screen.sh "~/Downloads/Matbakh Discovery.dc.html" discovery-iphone
#
# The repository is the system of record for prototypes. Claude Design is a
# drafting tool: a screen is drawn there, imported ONCE, and from that moment
# the copy in prototypes/ is the real one. Never re-export over an imported
# screen — you would lose whatever changed here since.
#
# Every export needs the same four transformations. Doing them by hand means
# forgetting one, and the failure modes are quiet: a blank screen, or a draft
# that Google indexes. This does all four and tells you what it did.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"

SRC="${1:-}"
NAME="${2:-}"

if [ -z "$SRC" ] || [ -z "$NAME" ]; then
  echo "usage: ./import-screen.sh <exported-file.dc.html> <kebab-case-name>"
  echo "   eg: ./import-screen.sh \"~/Downloads/Matbakh Discovery.dc.html\" discovery-iphone"
  exit 1
fi

SRC="${SRC/#\~/$HOME}"
[ -f "$SRC" ] || { echo "not found: $SRC"; exit 1; }

# Kebab-case only. A space here becomes %20 in every link you ever share, and
# build.py treats it as a hard error.
if ! echo "$NAME" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$'; then
  echo "name must be lowercase kebab-case, no spaces or dots: $NAME"
  exit 1
fi

DEST="prototypes/${NAME}.html"
if [ -f "$DEST" ]; then
  echo "$DEST already exists."
  printf "Overwrite? Anything changed here since the last import is lost. [y/N] "
  read -r a
  case "$a" in y|Y) ;; *) echo "cancelled"; exit 1 ;; esac
fi

cp "$SRC" "$DEST"
echo "── imported to $DEST"

# ── 1. Asset paths: prototypes/ is one level down from assets/ ──────────────
n=$(grep -c '"assets/' "$DEST" || true)
sed -i 's|"assets/|"../assets/|g' "$DEST"
echo "   1/4  rewrote $n asset path(s) to ../assets/"

# ── 2. MEDIA() fallback. It resolves through an embedded map and falls back
#       to the literal path — which would resolve inside prototypes/. Silent
#       failure: fine while media.js is present, blank the day it is not.
if grep -q "window.MB_MEDIA\[p\]) || p;" "$DEST"; then
  sed -i "s@window\.MB_MEDIA\[p\]) || p;@window.MB_MEDIA[p]) || (p ? '../' + p : p);@" "$DEST"
  echo "   2/4  patched MEDIA() fallback"
else
  echo "   2/4  MEDIA() fallback not found — check by hand if photos fail to load"
fi

# ── 3. noindex, while the project is not public ────────────────────────────
if grep -q 'name="robots"' "$DEST"; then
  echo "   3/4  noindex already present"
else
  sed -i '0,/<head>/s|<head>|<head>\n<meta name="robots" content="noindex,nofollow">|' "$DEST"
  echo "   3/4  stamped noindex"
fi

# ── 4. support.js must sit beside the prototypes ───────────────────────────
SRCDIR=$(dirname "$SRC")
if [ -f "$SRCDIR/support.js" ]; then
  if ! cmp -s "$SRCDIR/support.js" prototypes/support.js; then
    cp "$SRCDIR/support.js" prototypes/support.js
    echo "   4/4  support.js differed — updated. Re-check the other screens."
  else
    echo "   4/4  support.js unchanged"
  fi
else
  echo "   4/4  no support.js beside the export; keeping the existing one"
fi

# New assets travel with new screens
if [ -d "$SRCDIR/assets" ]; then
  NEW=$(cd "$SRCDIR/assets" && ls | while read -r f; do
          [ -e "../../assets/$f" ] || echo "$f"; done | wc -l | tr -d ' ')
  cp -rn "$SRCDIR/assets/." assets/ 2>/dev/null || true
  echo "        copied assets, $NEW new file(s)"
fi

cat <<EOF

── Add to manifest.yaml, under the section you want it in:

      - file: $DEST
        title: ${NAME//-/ }
        blurb: One sentence on what this screen decides.
        tags: [NEW]

── Then:

    python build.py          # verifies assets, links and filenames
    start $DEST              # look at it before committing

── And record it in CHANGELOG.md, bumping release: in manifest.yaml.
EOF
