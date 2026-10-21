#!/usr/bin/env python3
"""
import-recipe — a recipe page in, a shopping list and a nutrition estimate out.

    python3 tools/import-recipe.py https://example.com/a-recipe
    python3 tools/import-recipe.py URL --servings 6          # scale to 6 servings
    python3 tools/import-recipe.py URL --json                # the same, as JSON
    python3 tools/import-recipe.py --html saved-page.html    # a saved page, offline

Import plan step 5 (vault 02-strategy/import-test-plan-2026-10-12.md; PM log D-19):
the first import test, on Ibrahim's machine. **No AI.** It reads the page's own
schema.org recipe data, splits each ingredient line, matches it to the vault's
ingredient reference, and prints:

  - the recipe as published — title, author, a link, the ingredient lines as
    written (imports stay in source format, philosophy §44);
  - a SHOPPING LIST: one line per reference entry with the quantities added up,
    what to buy (whole packs, or stock cubes, §47), and every line the reference
    does not know, as written — never dropped;
  - an ESTIMATE, labelled تقدير and "not tested by Matbakh": calories, protein,
    carbohydrate and fat for the recipe and per serving, with every line it could
    not count listed by name and why.

A page with no recipe data gets a plain refusal, never a guess. It keeps nothing,
writes nothing, and sends nothing anywhere except the page request (robots.txt
respected). Shares its parts with capture-prefilter.py: tools/recipe_core/.
"""

import argparse, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # tools/, for recipe_core
import yaml
from recipe_core import basket
from recipe_core.lines import parse
from recipe_core.match import Matcher
from recipe_core.page import PageError, parse_html, read_recipe

LABEL = {"en": "ESTIMATE — تقدير · not tested by Matbakh", "ar": "تقدير — لم تختبره مطبخ"}


def build(rec, matcher, ref, servings=None):
    lang = "ar" if rec.get("language") == "ar" else "en"
    base = rec.get("servings")
    factor = (servings / base) if (servings and base) else 1.0
    lines = basket.read(rec["ingredients"], matcher, ref, parse)
    shop = basket.shop(lines, factor, lang)
    est = basket.estimate(lines, factor, servings or base)
    return dict(recipe={k: rec.get(k) for k in ("title", "author", "url", "final_url", "redirected",
                                                 "source", "language", "yield_text", "servings",
                                                 "ingredients", "steps")},
                scaled_to=servings if (servings and base) else None,
                scale_note=("" if not servings else
                            f"scaled linearly from {base} servings" if base else
                            "the page gives no servings, so the recipe is shown as written"),
                shopping=shop, estimate=est, label=LABEL[lang])


def as_text(r):
    rec, est, out = r["recipe"], r["estimate"], []
    out += [rec["title"] or "(untitled)", (f"by {rec['author']} · " if rec["author"] else "") + (rec["url"] or ""),
            "IMPORTED — the source's recipe, not tested by Matbakh"]
    if rec.get("redirected"):
        out.append(f"note: the page redirected to {rec['final_url']} — check it is the recipe you meant")
    sv = rec["servings"]
    out.append(f"servings: {r['scaled_to'] or sv or 'not given'}"
               + (f" ({r['scale_note']})" if r["scale_note"] else "")
               + (f" — the page says “{rec['yield_text']}”" if rec["yield_text"] else ""))
    out += ["", "INGREDIENTS, as written"] + ["  " + l for l in rec["ingredients"]]
    if rec["steps"]:
        out += ["", "METHOD, as written"] + [f"  {i}. {s}" for i, s in enumerate(rec["steps"], 1)]
    else:
        out += ["", "METHOD: the page's data has no steps (microdata) — read them on the page"]
    out += ["", "SHOPPING LIST"]
    for it in r["shopping"]["items"]:
        line = f"  {it['name']} — {it['amount'] or 'as needed'}"
        if it.get("purchase"):
            line += f"  → buy {it['purchase']}"
        out.append(line)
    if r["shopping"]["not_matched"]:
        out += ["  not in Matbakh's list — kept as written:"] + ["    " + t for t in r["shopping"]["not_matched"]]
    out += ["", r["label"]]
    if est["counted"] == 0:
        out.append("  nothing could be counted")
    else:
        t, p = est["total"], est["per_serving"]
        fmt = lambda d: f"{d['kcal']:.0f} kcal · protein {d['protein']:.0f} g · carbs {d['carb']:.0f} g · fat {d['fat']:.0f} g"
        if p:
            out.append("  per serving: " + fmt(p))
        out.append("  whole recipe: " + fmt(t))
    out.append(f"  counted {est['counted']} of {est['of']} lines"
               + (" (ranges taken at their middle)" if est["ranges_at_middle"] else ""))
    if est["not_counted"]:
        out.append("  not counted:")
        out += [f"    {l} — {why}" for l, why in est["not_counted"]]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="A recipe page in; a shopping list and an estimate out. No AI.")
    ap.add_argument("url", nargs="?", help="the recipe page")
    ap.add_argument("--html", type=pathlib.Path, help="read a saved page instead of fetching (offline tests)")
    ap.add_argument("--servings", type=int, help="scale to this many servings")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    ap.add_argument("--ref", help="path to ingredients.yaml (default: the vault)")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    if not a.url and not a.html:
        ap.error("give a URL, or --html FILE")
    try:
        if a.html:
            rec = parse_html(a.html.read_bytes(), "utf-8")
            if rec is None:
                raise PageError("this page has no recipe Matbakh can read")
            rec.update(url=a.url or str(a.html), final_url=a.url or str(a.html), redirected=False)
        else:
            rec = read_recipe(a.url)
    except PageError as e:
        sys.exit(f"import-recipe: {e}.")
    m = Matcher(a.ref)
    ref = yaml.safe_load(open(m.path, encoding="utf-8"))
    r = build(rec, m, ref, a.servings)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(as_text(r))


if __name__ == "__main__":
    main()
