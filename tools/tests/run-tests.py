#!/usr/bin/env python3
"""
run-tests — the import prototype's and the capture pre-filter's repeatable checks.

    python3 tools/tests/run-tests.py            # offline: the made-up pages in fixtures/
    python3 tools/tests/run-tests.py --online   # also a missing page and a redirect, over the network

Each case states what the tool must give (import plan step 5; CaptureDraftRunReadme
§7). The fixtures are made up for these tests — no one's recipe text. They match
against the vault's reference, so the cases test behaviour, not exact numbers:
a reference that grows should not break them. Exit code 1 if any case fails.
"""

import pathlib, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))   # tools/
import yaml
from recipe_core import basket, checks
from recipe_core.lines import parse
from recipe_core.match import Matcher
from recipe_core.page import PageError, parse_html, read_recipe

HERE = pathlib.Path(__file__).resolve().parent
FX = HERE / "fixtures"
m = Matcher()
ref = yaml.safe_load(open(m.path, encoding="utf-8"))
results = []


def case(name, ok, detail=""):
    ok = bool(ok)
    results.append(ok)
    print(("PASS  " if ok else "FAIL  ") + name + ("" if ok else f"  — {detail}"))


def imported(fixture, servings=None):
    rec = parse_html((FX / fixture).read_bytes(), "utf-8")
    lines = basket.read(rec["ingredients"], m, ref, parse)
    base = rec["servings"]
    factor = servings / base if servings and base else 1.0
    lang = "ar" if rec["language"] == "ar" else "en"
    return rec, lines, basket.shop(lines, factor, lang), basket.estimate(lines, factor, servings or base)


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")

    # ── import: an English page with full data ──
    rec, lines, shop, est = imported("en-full.html")
    case("EN: the recipe is read (title, author, 4 servings)",
         rec["title"] == "Matbakh test stew" and rec["author"] == "Test Kitchen" and rec["servings"] == 4)
    case("EN: an unknown ingredient stays on the list as text, never dropped",
         "1 cup frobnicated zizzle" in shop["not_matched"], shop["not_matched"])
    case("EN: a range stays a range on the list",
         any("–" in it["amount"] for it in shop["items"] if it["id"] == "chicken_stock"),
         [it["amount"] for it in shop["items"] if it["id"] == "chicken_stock"])
    case("EN: stock is bought in cubes (§47)",
         any("cube" in it.get("purchase", "") for it in shop["items"] if it["id"] == "chicken_stock"))
    case("EN: the pinch is on the list, and not counted in the estimate",
         any(it["id"] == "salt" for it in shop["items"])
         and any(l.startswith("1 pinch salt") and "too small" in w for l, w in est["not_counted"]))
    case("EN: one ingredient on two lines is added up: olive oil 2 + 1 tbsp = 3 tbsp",
         any(it["id"] == "olive_oil" and it["amount"] == "3 tbsp" for it in shop["items"]),
         [it["amount"] for it in shop["items"] if it["id"] == "olive_oil"])
    case("EN: a package's size is read: 1 (16 ounce) package tofu = 16 oz",
         any(it["id"] == "tofu" and it["amount"] == "16 oz" for it in shop["items"]))
    case("EN: double-encoded text is cleaned: 8&quot; pita reads as 8\" pita",
         any('8"' in l for l in rec["ingredients"]), rec["ingredients"])
    case("EN: the estimate counts something and lists what it could not count",
         est["counted"] > 0 and est["not_counted"] and est["per_serving"])
    rec2, _, shop2, est2 = imported("en-full.html", servings=8)
    case("EN: scaling to 8 servings doubles the beef",
         any(it["id"] == "beef" and it["amount"] == "1 kg" for it in shop2["items"]),
         [it["amount"] for it in shop2["items"] if it["id"] == "beef"])

    # ── Arabic ──
    rec, lines, shop, est = imported("ar-full.html")
    case("AR: Arabic-Indic digits are read (٢ كوب أرز = 2 cups; ٤ أشخاص = 4 servings)",
         rec["servings"] == 4 and any(l["id"] == "rice" and l["q"] == 2 for l in lines),
         [(l["line"], l["q"], l["id"]) for l in lines])
    case("AR: the list uses the Arabic names", any(it["name"] == "أرز" for it in shop["items"]),
         [it["name"] for it in shop["items"]])
    case("AR: a plain-text method is split into steps", len(rec["steps"]) == 2, rec["steps"])

    # ── Egyptian ways of writing amounts ──
    rec, lines, shop, est = imported("eg-full.html")
    by = {l["line"]: l for l in lines}
    case("EG: معلقه صغيرة (the Egyptian spelling) is a teaspoon",
         by["0.5 معلقه صغيرة قرفه"]["unit"] == "tsp" and by["معلقة صغيرة بابريكا"]["q"] == 1)
    case("EG: a dual is two — جزرتين = 2 carrots", by["جزرتين كبار"]["q"] == 2 and by["جزرتين كبار"]["id"] == "carrots")
    case("EG: a counted item's singular is one — بصلايه = 1 onion",
         by["بصلايه كبيره"]["q"] == 1 and by["بصلايه كبيره"]["id"] == "onion")
    case("EG: a mass noun's singular is not one — قرفة alone has no quantity", by["قرفة"]["q"] is None)
    case("EG: مكعب مرقة is one stock cube = 500 ml, bought as one cube",
         by["مكعب مرقة دجاج"]["unit"] == "ml" and by["مكعب مرقة دجاج"]["q"] == 500
         and any("cube" in it.get("purchase", "") for it in shop["items"] if it["id"] == "chicken_stock"))
    case("EG: معلقتين كبيرة is two tablespoons", by["معلقتين كبيرة زيت"]["unit"] == "tbsp" and by["معلقتين كبيرة زيت"]["q"] == 2)

    case("EG: a descriptor before the amount is matched with the name — ناشفة كزبرة is ground coriander",
         by["ناشفة ملعقة كبيرة كزبرة"]["id"] == "coriander_ground" and by["مفرومة ملعقتان كبيرتان كزبرة"]["id"] == "coriander_fresh")
    case("EG: a markdown link in a step keeps its words", rec["steps"][-1].endswith("طرق أخرى"), rec["steps"])
    rec_e, lines_e, _, _ = imported("en-full.html")
    be = {l["line"]: l["id"] for l in lines_e}
    case("EN: a note naming the thing differently does not change it — cornstarch (corn flour) stays cornstarch",
         be["2 tablespoons cornstarch (corn flour)"] == "cornstarch", be["2 tablespoons cornstarch (corn flour)"])
    case("EN: a note that describes it does — Coriander (ground) is ground coriander",
         be["1 tsp Coriander (ground)"] == "coriander_ground", be["1 tsp Coriander (ground)"])

    _, lines_s, shop_s, _ = imported("en-full.html")
    case("EN: cups and spoons of something sold by weight are listed in grams — sugar 1 cup + 1 tbsp = 212 g",
         any(it["id"] == "granulated_sugar" and it["amount"] == "212 g" for it in shop_s["items"]),
         [it["amount"] for it in shop_s["items"] if it["id"] == "granulated_sugar"])
    case("EN: 'a tiny pinch' is a pinch", any(l["line"] == "1 tiny pinch cinnamon" and l["unit"] == "pinch" for l in lines_s))

    case("EN: a rice cooker's cup is a unit — '1.9 rice cup water' is water, not rice",
         any(l["line"] == "1.9 rice cup water" and l["id"] == "water" and l["unit"] == "rice_cup" for l in lines_s)
         and any(it["id"] == "jasmine_rice" and it["amount"] == "2 rice cups" for it in shop_s["items"]),
         [(l["line"], l["id"], l["unit"]) for l in lines_s if "rice cup" in l["line"]])

    # ── French ──
    rec, lines, shop, est = imported("fr-full.html")
    case("FR: a list comes back; nothing is dropped",
         len(shop["items"]) + len(shop["not_matched"]) >= 3, shop)

    # ── no recipe data ──
    case("A page with no recipe data is refused, never guessed",
         parse_html((FX / "no-data.html").read_bytes(), "utf-8") is None)

    # ── pre-filter ──
    d = checks.load(FX / "draft-flags.txt")
    f = checks.run(d, m, ref, parse)
    case("Pre-filter A: an ingredient with no quantity is flagged", any("parsley" in x for x in f["A"]), f["A"])
    case("Pre-filter D: an unknown ingredient is flagged", any("zizzle" in x for x in f["D"]), f["D"])
    case("Pre-filter E: the source is carried forward", any("example.com" in x for x in f["E"]), f["E"])
    case("Pre-filter F: butter 1 + 2 = 3 tbsp", any("1 tbsp + 2 tbsp = 3 tbsp" in x for x in f["F"]), f["F"])
    case("Pre-filter F: beef stock and broth are one ingredient (by the reference)",
         any("cup + 0.5 cup" in x for x in f["F"]), f["F"])
    case("Pre-filter G: 450° has no unit; 325°F is not °C",
         any("450°" in x and "no unit" in x for x in f["G"]) and any("325°F" in x for x in f["G"]), f["G"])
    case("Pre-filter H: the steps use more butter than the list",
         any("butter" in x.lower() and "more" in x for x in f["H"]), f["H"])
    case("Pre-filter H: '10 minutes' is not read as a quantity of flour",
         not any("flour" in x.lower() for x in f["H"]), f["H"])

    # ── online: a missing page and a redirect ──
    if "--online" in sys.argv:
        try:
            read_recipe("https://example.com/no-such-recipe-page")
            case("Online: a missing page gives a clear error", False, "no error raised")
        except PageError as e:
            case("Online: a missing page gives a clear error", "404" in str(e) or "exist" in str(e), str(e))
        try:
            read_recipe("http://example.com/")
            case("Online: a page with no recipe is refused", False, "no error raised")
        except PageError as e:
            case("Online: a page with no recipe is refused", "no recipe" in str(e), str(e))

    n, ok = len(results), sum(results)
    print(f"\n{ok} of {n} cases pass")
    sys.exit(0 if ok == n else 1)


if __name__ == "__main__":
    main()
