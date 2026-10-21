#!/usr/bin/env python3
"""
ingredient-lines — split a recipe's ingredient line into quantity, unit and ingredient.

    python3 ingredient-lines.py "2 c. à soupe d'huile d'olive"
    python3 ingredient-lines.py --csv lines.csv --out parsed.csv     # a column named `line`

Import step 2 (PM log §11 item 9, D-19): can ingredient lines from Arabic,
English and French recipe sites be read reliably without AI? This is the
parser being measured. For each line it returns:

    qty, qty_max   a number, or a range (2–3 cups gives 2 and 3); empty if none
    unit           one key per unit — g, kg, ml, l, tsp, tbsp, cup, oz, lb,
                   pinch, clove, can, … — or empty for a counted item (2 eggs)
    name           the ingredient, without quantity, unit or notes
    note           what follows: a comma clause, a parenthesis
    kind           measured · count · to_taste · no_quantity · unparsed

It never guesses. A line it cannot split is returned as `unparsed` with the
whole line as the name, so an importer can still put it on a shopping list as
plain text. Standard library only; no AI, no network.
"""

import argparse, csv, sys

import pathlib as _pathlib, sys as _sys
_sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))   # tools/, for recipe_core
from recipe_core.lines import parse

FIELDS = ["line", "qty", "qty_max", "unit", "name", "note", "kind"]


def main():
    ap = argparse.ArgumentParser(description="Split ingredient lines into quantity, unit and ingredient.")
    ap.add_argument("lines", nargs="*", help="ingredient lines to parse")
    ap.add_argument("--csv", help="read lines from this CSV's `line` column")
    ap.add_argument("--out", help="write the parsed rows (with the input's other columns) here")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    rows = [{"line": l} for l in a.lines]
    if a.csv:
        with open(a.csv, encoding="utf-8-sig") as fh:
            rows += list(csv.DictReader(fh))
    if not rows:
        ap.error("give lines, or --csv")
    parsed = [{**r, **parse(r["line"])} for r in rows]
    if a.out:
        extra = [k for k in rows[0] if k not in FIELDS]
        with open(a.out, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, extra + FIELDS)
            w.writeheader()
            w.writerows(parsed)
        print(f"written {len(parsed)} rows to {a.out}")
    else:
        for p in parsed:
            q = p["qty"] + ("–" + p["qty_max"] if p["qty_max"] else "")
            print(f"{p['kind']:<12} {q:>6} {p['unit']:<7} {p['name']}" + (f"  [{p['note']}]" if p["note"] else ""))


if __name__ == "__main__":
    main()
