#!/usr/bin/env python3
"""
ingredient-match — find which reference ingredient an imported ingredient name means.

    python3 ingredient-match.py "huile d'olive" "حليب سائل" "2 large eggs"
    python3 ingredient-match.py --csv parsed.csv --out matched.csv     # a column named `name`

Import step 3 (PM log §11 item 9, D-19): after `ingredient-lines.py` has split
a line into quantity, unit and ingredient, this matches the ingredient against
the vault's `ref/ingredients.yaml` — every entry's English and Arabic `name`
and its `aliases` (philosophy §45). A match is the reference id, or empty.

How it matches: both sides are lower-cased and normalised (Arabic diacritics
and letter variants — أ إ آ → ا, ة → ه, ى → ي — the Arabic article ال, Arabic
dual and plural endings, English plurals), then a reference name matches when
**all its words appear in the ingredient's words**. The longest such name wins,
so *garlic powder* finds `garlic_powder`, not `garlic`. **A match is refused**
when the ingredient has a word that makes it a different food — *broth*,
*powder*, *extract*, *syrup*, *sauce*, *paste*, *flakes*, *vinegar* … (FORM) —
and the matched name does not, so *chicken broth* never becomes a chicken. An
alias written with a leading = (*=pepper*) matches only the whole name. It
never guesses beyond that: no fuzzy spelling, no translation, no AI. An
ingredient it cannot match comes back empty, and an importer keeps it on the
shopping list as plain text.

The reference is found the way `content/matbakh.py` finds it: --ref PATH,
then MATBAKH_VAULT, then content/vault.path, then ../../matbakh-private/03-catalogue.
"""

import argparse, csv, sys

import pathlib as _pathlib, sys as _sys
_sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))   # tools/, for recipe_core
from recipe_core.match import Matcher


def main():
    ap = argparse.ArgumentParser(description="Match imported ingredient names to the reference.")
    ap.add_argument("names", nargs="*")
    ap.add_argument("--csv", help="read names from this CSV's `name` column")
    ap.add_argument("--out", help="write the input rows plus `match` and `matched_on`")
    ap.add_argument("--ref", help="path to ingredients.yaml (default: the vault)")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    m = Matcher(a.ref)
    print(f"reference: {m.size} ingredients from {m.path}", file=sys.stderr)
    rows = [{"name": n} for n in a.names]
    if a.csv:
        with open(a.csv, encoding="utf-8-sig") as fh:
            rows += list(csv.DictReader(fh))
    if not rows:
        ap.error("give names, or --csv")
    for r in rows:
        r["match"], r["matched_on"] = m.match(r.get("name", ""))
    if a.out:
        with open(a.out, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"written {len(rows)} rows to {a.out}")
    else:
        for r in rows:
            print(f"{r['match'] or '—':<22} {r['name']}" + (f"   (on: {r['matched_on']})" if r["match"] else ""))


if __name__ == "__main__":
    main()
