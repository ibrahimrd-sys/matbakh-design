#!/usr/bin/env python3
"""
export-for-app — what the Flutter app (~/Develop/matbakh) takes from the vault and
from recipe_core, for import step 7 (design/shopping-list-design.md §6).

    python3 tools/export-for-app.py                 # into ~/Develop/matbakh
    python3 tools/export-for-app.py --app PATH
    python3 tools/export-for-app.py --sample        # only the made-up sample, committed in the app

Writes, in the app:
  assets/ref/ingredients.json     the vault's reference, as JSON (gitignored there:
                                  vault data stays out of git until Ibrahim says otherwise)
  assets/recipes/<id>.json        the authored catalogue recipes' shopping items,
                                  from `matbakh.py build` at their base servings (gitignored)
  test/parity/fixtures.json       basket.shop() on the made-up fixture pages and on the
                                  §48 test lines; each case carries the reference entries
                                  it uses (so gitignored, like everything here)
  test/parity/lines.json          every saved ingredient line in the vault's 04-research
                                  (steps 2 and 3, English, Arabic, French): lines.parse()
                                  and Matcher.match() on its name — for the app's parser
                                  and matcher (gitignored)
  test/parity/corpus.json         the same on every saved page of fresh samples 4–6
                                  (vault `04-research/step3-fresh{4,5,6}-lines-*.csv`) —
                                  real sites' text, so gitignored

--sample writes, from tests/fixtures/app-sample.yaml (made up: 12 ingredients,
3 invented recipes, 3 invented import pages), what the app commits so a fresh copy
builds and tests without the vault:
  assets/sample/ingredients.json, assets/sample/recipes/<id>.json, test/sample/parity.json,
  test/sample/lines.json (made-up lines covering each parser rule, on the sample)

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


def est(lines, factor, servings, ref):
    """basket.estimate() and rounded(), as JSON: what the app's estimate must give."""
    e = basket.estimate(lines, factor, servings, ref)
    return dict(factor=factor, servings=servings, total=e["total"], per_serving=e["per_serving"],
                counted=e["counted"], of=e["of"], not_counted=[list(x) for x in e["not_counted"]],
                ranges_at_middle=e["ranges_at_middle"], alternatives=[list(x) for x in e["alternatives"]],
                confidence=e["confidence"], shown_total=basket.rounded(e["total"]),
                shown_per_serving=basket.rounded(e["per_serving"]) if e["per_serving"] else None)


def case(name, raw, lang, m, ref):
    lines = basket.read(raw, m, ref, parse)
    shop = basket.shop(lines, 1.0, lang)
    ids = sorted({p["id"] for p in lines if p["id"]})
    return dict(name=name, lang=lang, lines=[given(p) for p in lines],
                estimates=[est(lines, 1.0, 4, ref), est(lines, 2.0, 8, ref)],
                entries={i: entry(ref[i]) for i in ids},
                expect=dict(items=[{k: it.get(k) for k in ("id", "name", "amount", "lines", "buy", "staple",
                                                          "aisle", "unclear", "purchase")}
                                   for it in shop["items"]],
                            notMatched=shop["not_matched"]))


# Made-up lines, one or more for each rule the parser has, for the sample's parse cases.
LINE_RULES = [
    "2 cups flour", "1 1/2 cups milk", "½ cup sugar", "1¼ tsp salt", "2-3 tbsp olive oil", "1 T sugar",
    "1 t salt", "2 to 3 onions", "a pinch of salt", "Pinch of salt", "dashes pepper", "3 cloves garlic, minced",
    "1 (14 oz) can tomatoes", "2 - 15.5 ounce cans chickpeas", "10 tablespoons (1 1/4 sticks) butter",
    "1 heaping tablespoon flour", "salt to taste", "salt and pepper, to taste", "For the sauce:", "Ingredients",
    "1 large onion, diced", "2 stalks celery", "500g rice", "1 kg lamb", "250 ml water", "1 l stock",
    "1 rice cup water", "4 cups chicken broth", "1 lemon (juiced)", "zest of 1 lemon", "1 dozen eggs",
    "half a lemon", "2 1/2 cups flour", "1,5 kg potatoes", "3/4 cup yogurt", "1 cup frobnicated zizzle",
    "كوب أرز", "2 كوب أرز", "كوبان دقيق", "ملعقتان كبيرتان زيت زيتون", "ملعقة صغيرة ملح", "نصف كوب لبن",
    "كوب ونصف سكر", "2 ونصف بيضة", "بصلة", "جزرتين", "3 فصوص ثوم", "مكعب مرقة", "ملح - حسب الرغبة",
    "ملح حسب الرغبة", "مطحون نصف ملعقة صغيرة زنجبيل", "٢ كوب دقيق", "١٫٥ كيلو لحمة", "المكونات",
    "شرائح لوز", "ثلاث بصلات", "معلقتين كبيرة سمنة", "1 م.ك زيت",
    "2 cuillères à soupe d'huile d'olive", "1 c. à c. de sel", "200 g de farine", "une pincée de sel",
    "3 gousses d'ail", "1 noix de beurre", "sel - au goût", "1 verre de lait",
]


def line_case(raw, m):
    p = parse(raw)
    return dict(line=raw, parse={k: p[k] for k in ("qty", "qty_max", "unit", "name", "note", "kind")},
                match=list(m.match(p["name"])) if p["name"] else ["", ""])


def entities(app):
    """lib/import/html_entities.dart: Python's own HTML5 entity table and its rules for
    invalid references, so the app decodes &amp;, &#39;, &eacute; exactly as html.unescape."""
    import html
    def lit(v):
        return "'" + "".join(c if c.isalnum() or c in " -_.,:;!?()[]{}#%&*+/<=>@^|~`\"" else
                             "\\u{%x}" % ord(c) for c in v) + "'"
    out = ["// GENERATED by matbakh-design/tools/export-for-app.py from Python "
           + sys.version.split()[0] + "'s html module. Do not edit.", "",
           "const htmlEntities = <String, String>{"]
    out += [f"  {lit(k)}: {lit(v)}," for k, v in html.entities.html5.items()]
    out += ["};", "", "const invalidCharrefs = <int, String>{"]
    out += [f"  {k}: {lit(v)}," for k, v in sorted(html._invalid_charrefs.items())]
    out += ["};", "", "const invalidCodepoints = <int>{"]
    out += [f"  {k}," for k in sorted(html._invalid_codepoints)]
    out += ["};", ""]
    f = app / "lib/import/html_entities.dart"
    f.write_text("\n".join(out), encoding="utf-8", newline="\n")
    print(f"  lib/import/html_entities.dart  ({len(html.entities.html5)} entities)")


APP_UA = "Matbakh/0.1 (recipe import)"     # the app's, as lib/import/reader.dart names it


def page_cases(app, write):
    """test/sample/pages.json: page.py's answers on made-up pages (the test fixtures and
    tests/fixtures/app-pages.yaml), robots.txt files and addresses — for the app's reader."""
    import urllib.robotparser
    from recipe_core import page as pg
    fx = HERE / "tests" / "fixtures"
    src = yaml.safe_load(open(fx / "app-pages.yaml", encoding="utf-8"))
    html = [(f.name, f.read_text(encoding="utf-8")) for f in sorted(fx.glob("*.html"))]
    html += [(x["name"], x["html"]) for x in src["pages"]]
    out = dict(pages=[dict(name=n, html=h, expect=pg.parse_html(h.encode("utf-8"), "utf-8")) for n, h in html],
               robots=[], urls=[dict(url=u, expect=pg._encode(u)) for u in src["urls"]], user_agent=APP_UA)
    for r in src["robots"]:
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(r["text"].splitlines())
        out["robots"].append(dict(name=r["name"], text=r["text"],
                                  expect={u: rp.can_fetch(APP_UA, u) for u in src["robot_urls"]}))
    write("test/sample/pages.json", out)


def sample(app, write):
    """The made-up sample (tests/fixtures/app-sample.yaml), for the app's git."""
    import tempfile
    src = yaml.safe_load(open(HERE / "tests" / "fixtures" / "app-sample.yaml", encoding="utf-8"))
    ref = src["reference"]
    with tempfile.TemporaryDirectory() as d:
        path = pathlib.Path(d) / "ingredients.yaml"
        path.write_text(yaml.safe_dump(ref, allow_unicode=True), encoding="utf-8")
        m = Matcher(str(path))
    write("assets/sample/ingredients.json", {k: entry(v) for k, v in ref.items()})
    for r in src["recipes"]:
        write(f"assets/sample/recipes/{r['id']}.json", r)
    cases = [case(c["name"], c["lines"], c["lang"], m, ref) for c in src["imports"]]
    write("test/sample/parity.json", cases)
    write("test/sample/lines.json", [line_case(l, m) for l in LINE_RULES])
    print(f"sample: {len(ref)} ingredients, {len(src['recipes'])} recipes, {len(cases)} cases — made up")


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--app", default=str(pathlib.Path.home() / "Develop" / "matbakh"))
    ap.add_argument("--sample", action="store_true", help="only the made-up sample")
    a = ap.parse_args()
    app = pathlib.Path(a.app)
    if not (app / "pubspec.yaml").exists():
        sys.exit(f"no Flutter app at {app}")


    def write(rel, obj):
        p = app / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        print(f"  {rel}  ({p.stat().st_size // 1024} KB)")

    print(f"into {app}")
    entities(app)
    sample(app, write)
    page_cases(app, write)
    if a.sample:
        return

    m = Matcher()
    ref = yaml.safe_load(open(m.path, encoding="utf-8"))
    vault = pathlib.Path(m.path).parent.parent          # 03-catalogue
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

    seen = {}
    for f in sorted(research.glob("step[23]-*.csv")):
        with open(f, encoding="utf-8-sig", newline="") as fh:
            rd = csv.DictReader(fh)
            if "line" not in (rd.fieldnames or []):
                continue
            for row in rd:
                if row["line"] and row["line"] not in seen:
                    seen[row["line"]] = None
    write("test/parity/lines.json", [line_case(l, m) for l in seen])
    print(f"{len(seen)} saved lines for the parser and matcher")
    print(f"{len(cases)} fixture cases, {len(corpus)} saved pages "
          f"({sum(len(c['lines']) for c in corpus)} lines)")


if __name__ == "__main__":
    main()
