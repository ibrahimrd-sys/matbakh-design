#!/usr/bin/env python3
"""
Matbakh — patch the leak guards.

Fixes a false positive: generated media bundles like assets/media.js are one
enormous line of base64 image data, and random substrings inside a payload that
large match a loose secret pattern by chance. Both guards now blank the base64
payload before scanning, so a real secret elsewhere in the same file is still
caught.

Also fixes build.py writing index.html with CRLF endings on Windows, which
contradicts the eol=lf rule in .gitattributes and makes git warn on every add.

Run from inside the matbakh-design folder:

    python patch-guards.py

Safe to run twice — it reports what was already done and changes nothing.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
STRIP = ("        | sed -E 's#data:[a-z/+.-]+;base64,"
         "[A-Za-z0-9+/=_-]*#<base64-payload>#g' \\\n")

PATCHES = [
    (
        ".githooks/pre-commit",
        '  HIT=$(git show ":$f" 2>/dev/null | grep -Ein "$SECRET_RE" | head -2 || true)',
        '  # Generated media bundles are one huge line of base64. Random substrings\n'
        '  # in a payload that large match a loose pattern by chance, so the payload\n'
        '  # is blanked before scanning. A real secret elsewhere is still caught.\n'
        '  HIT=$(git show ":$f" 2>/dev/null \\\n'
        + STRIP +
        '        | grep -Ein "$SECRET_RE" | head -2 || true)',
    ),
    (
        "scan.sh",
        '    grep -Eqi "$SECRET_RE" "$f" 2>/dev/null && bad "TRACKED: $f contains a secret-shaped string"',
        "    sed -E 's#data:[a-z/+.-]+;base64,[A-Za-z0-9+/=_-]*#<base64-payload>#g' \"$f\" 2>/dev/null \\\n"
        '      | grep -Eqi "$SECRET_RE" && bad "TRACKED: $f contains a secret-shaped string"',
    ),
    (
        "build.py",
        '    (ROOT / "index.html").write_text(generate(), encoding="utf-8")',
        '    # newline="\\n" is required: Python\'s default text mode writes CRLF on\n'
        '    # Windows, which contradicts the eol=lf rule in .gitattributes.\n'
        '    with open(ROOT / "index.html", "w", encoding="utf-8", newline="\\n") as fh:\n'
        '        fh.write(generate())',
    ),
]

if not (ROOT / "manifest.yaml").exists():
    print("This does not look like the matbakh-design folder — manifest.yaml is")
    print("missing. Move this file into matbakh-design and run it from there.")
    sys.exit(1)

changed = skipped = 0
for rel, old, new in PATCHES:
    p = ROOT / rel
    if not p.exists():
        print(f"  MISSING  {rel} — skipped")
        continue
    text = p.read_text(encoding="utf-8")
    n = text.count(old)
    if n == 0:
        print(f"  already  {rel}")
        skipped += 1
        continue
    if n > 1:
        print(f"  AMBIGUOUS  {rel} — target line appears {n} times, not patching")
        continue
    # newline="" preserves whatever endings the file already has
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(text.replace(old, new))
    print(f"  patched  {rel}")
    changed += 1

print(f"\n{changed} patched, {skipped} already current.")
if changed:
    print("\nNext:")
    print("    python build.py")
    print("    git add -A")
    print('    git commit -m "Design repository, first publish"')
