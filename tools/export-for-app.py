#!/usr/bin/env python3
"""
export-for-app — what the Flutter app (~/Develop/matbakh) takes from the vault and
from recipe_core, for import step 7 (design/shopping-list-design.md §6).

    python3 tools/export-for-app.py                 # into ~/Develop/matbakh
    python3 tools/export-for-app.py --app PATH

Writes, in the app:
  assets/ref/ingredients.json     the vault's reference, as JSON (gitignored there:
                                  vault data stays out of git until Ibrahim says otherwise)
  assets/recipes/<id>.json        the authored catalogue recipes' shopping items,
                                  from `matbakh.py build` at their base servings (gitignored)
  test/parity/fixtures.json       basket.shop() on the made-up fixture pages and on the
                                  §48 test lines; each case carries the reference entries
                                  it uses (so gitignored, like everything here)
  test/parity/corpus.json         the same on every saved page of fresh samples 4–6
                                  (vault `04-research/step3-fresh{4,5,6}-lines-*.csv`) —
                                  real sites' text, so gitignored

A case's lines are what the list is given: the parser's quantity, with a package's
stated size already applied ("1 (16 ounce) package tofu" → 16 oz), so the phone's
list is tested on its own job — adding up, rounding, packs — and not the parser's.
"""

import argparse, csv, json, os, pathlib, subprocess, sys
from collections import OrderedDict

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import yaml
from recipe_core import basket
from recipe_core.lines import parse
from recipe_core.match import Matcher
from recipe_core.page import parse_html

FIELDS = ("glyph", "name", "aliases", "diet", "unit", "cls", "divisible", "pack", "convert",
          "makes", "buy", "aisle", "staple", "nutrition")
SAMPLES = ("step3-fresh4-lines-2026-10-19.csv", "step3-fresh5-lines-2026-10-20.csv",
           "step3-fresh6-lines-2026-10-20.csv")
TEST_LINES = ["237 g beef", "13 g butter", "103 g flour", "1/3 tsp salt", "1 tsp black pepper",
              "2 onions", "1.5 cups buttermilk", "12 tortillas", "2 1/2 cups chicken broth",
              "1 cup sugar", "1 tablespoon sugar", "1.5 kg rice", "2-3 cups water", "salt to taste",
              "1 pinch cinnamon", "1 cup frobnicated zizzle", "2 (14 oz) cans crushed tomatoes"]


def entry(e):
    return {k: e[k] for k in FIELDS if k in e}


def given(p):
    """The line as the list receives it: id, text, quantity, unit, a package's size applied."""
    q, q_max, unit = p["q"], p["q_max"], p["unit"]
    size = basket._pack_size(p)
    if size and q is not None:
        q, q_max, unit = q * size[0], (q_max or 0) * size[0] or None, size[1]
    return dict(id=p["id"] or None, text=p["line"], q=q, qMax=q_max, unit=unit)


def case(name, raw, lang, m, ref):
    lines = basket.read(raw, m, ref, parse)
    shop = basket.shop(lines, 1.0, lang)
    ids = sorted({p["id"] for p in lines if p["id"]})
    return dict(name=name, lang=lang, lines=[given(p) for p in lines],
                entries={i: entry(ref[i]) for i in ids},
                expect=dict(items=[{k: it.get(k) for k in ("id", "name", "amount", "lines", "buy", "staple",
                                                          "aisle", "unclear", "purchase")}
                                   for it in shop["items"]],
                            notMatched=shop["not_matched"]))


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--app", default=str(pathlib.Path.home() / "Develop" / "matbakh"))
    a = ap.parse_args()
    app = pathlib.Path(a.app)
    if not (app / "pubspec.yaml").exists():
        sys.exit(f"no Flutter app at {app}")

    m = Matcher()
    ref = yaml.safe_load(open(m.path, encoding="utf-8"))
    vault = pathlib.Path(m.path).parent.parent          # 03-catalogue

    def write(rel, obj):
        p = app / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        print(f"  {rel}  ({p.stat().st_size // 1024} KB)")

    print(f"into {app}")
    write("assets/ref/ingredients.json", {k: entry(v) for k, v in ref.items()})

    # the catalogue's authored recipes, as the list receives them
    content = HERE.parent / "content"
    for f in sorted((vault / "recipes").glob("*.yaml")):
        rec = yaml.safe_load(open(f, encoding="utf-8")) or {}
        if not rec.get("steps"):
            continue                                     # a stub
        out = {}
        for loc in ("en", "ar"):
            r = subprocess.run([sys.executable, "matbakh.py", "build", str(f), loc], cwd=content,
                               capture_output=True, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
            if r.returncode:
                sys.exit(f"build failed for {f.name}: {r.stderr.decode('utf-8', 'replace')[-400:]}")
            out[loc] = json.loads(r.stdout.decode("utf-8"))
        b = out["en"]
        write(f"assets/recipes/{rec['id']}.json", dict(
            id=rec["id"], title={l: out[l].get("title") for l in out},
            servings=rec["servings"]["base"],
            items=[dict(id=i["id"], amount=i["amount"], unit="" if i["unit"] == "count" else i["unit"])
                   for i in b["items"]]))

    fx = HERE / "tests" / "fixtures"
    cases = []
    for name in ("en-full.html", "ar-full.html", "eg-full.html", "fr-full.html"):
        rec = parse_html((fx / name).read_bytes(), "utf-8")
        lang = "ar" if rec["language"] == "ar" else "en"
        cases.append(case(name, rec["ingredients"], lang, m, ref))
        if lang == "en":
            cases.append(case(name + " (ar words)", rec["ingredients"], "ar", m, ref))
    cases.append(case("§48 test lines", TEST_LINES, "en", m, ref))
    cases.append(case("§48 test lines (ar words)", TEST_LINES, "ar", m, ref))
    write("test/parity/fixtures.json", cases)

    research = vault.parent / "04-research"
    pages = OrderedDict()
    for s in SAMPLES:
        with open(research / s, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                pages.setdefault((row["url"], row["lang"]), []).append(row["line"])
    corpus = [case(url, raw, "ar" if lang == "ar" else "en", m, ref) for (url, lang), raw in pages.items()]
    write("test/parity/corpus.json", corpus)
    print(f"{len(cases)} fixture cases, {len(corpus)} saved pages "
          f"({sum(len(c['lines']) for c in corpus)} lines)")


if __name__ == "__main__":
    main()
