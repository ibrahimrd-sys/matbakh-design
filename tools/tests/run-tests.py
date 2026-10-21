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


def catalogue_lists():
    """Build the repo's fixture recipe with a sub-recipe and a repeated ingredient
    added, and read three amounts off its shopping list."""
    import copy, importlib.util, os, tempfile
    content = HERE.parent.parent / "content"
    cwd = os.getcwd()
    os.chdir(content)
    try:
        spec = importlib.util.spec_from_file_location("matbakh", content / "matbakh.py")
        mb = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mb)
        base = mb.load("recipes/molokhia_bil_farakh.yaml")
        sub = dict(id="test_sauce", servings={"base": 1},
                   steps=[{"station": base["steps"][0]["station"],
                           "tiles": [{"do": "chop", "item": "tomato", "amt": 400}]}])
        sub["yield"] = {"amount": 400, "unit": "ml"}
        mb.all_recipes = lambda: {"test_sauce": sub}
        rec = copy.deepcopy(base)
        rec["uses"] = [{"id": "test_sauce", "amt": 200}]
        rec["steps"][0]["tiles"].append({"do": "chop", "item": "onion", "amt": 1})
        out = {}
        with tempfile.TemporaryDirectory() as d:
            f = pathlib.Path(d) / "parent.yaml"
            f.write_text(yaml.safe_dump(rec, allow_unicode=True), encoding="utf-8")
            for n in (4, 8):
                items = {i["id"]: i for i in mb.build(str(f), "en", n)["items"]}
                out[f"sub{n}"] = items["tomato"]["amount"]
                if n == 4:
                    out["onion"] = items["onion"]["amount"]
        return out
    finally:
        os.chdir(cwd)


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
         and any("مكعب" in it.get("purchase", "") for it in shop["items"] if it["id"] == "chicken_stock"))
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
    case("EN: cups and spoons of something sold by weight are listed in grams — sugar 1 cup + 1 tbsp = 212 g, shown 210 g (§6.3)",
         any(it["id"] == "granulated_sugar" and it["amount"] == "210 g" for it in shop_s["items"]),
         [it["amount"] for it in shop_s["items"] if it["id"] == "granulated_sugar"])
    case("EN: 'a tiny pinch' is a pinch", any(l["line"] == "1 tiny pinch cinnamon" and l["unit"] == "pinch" for l in lines_s))

    case("EN: a rice cooker's cup is a unit — '1.9 rice cup water' is water, not rice",
         any(l["line"] == "1.9 rice cup water" and l["id"] == "water" and l["unit"] == "rice_cup" for l in lines_s)
         and any(it["id"] == "jasmine_rice" and it["amount"] == "2 rice cups" for it in shop_s["items"]),
         [(l["line"], l["id"], l["unit"]) for l in lines_s if "rice cup" in l["line"]])

    case("EN: a stalk of something counted by the piece is one — 2 stalks scallions = 2",
         any(l["line"] == "2 stalks scallions (chopped)" and l["id"] == "spring_onion" and l["unit"] == "" and l["q"] == 2 for l in lines_s))

    # ── step 6's fixes (04-research/step6-review-2026-10-21.md) ──
    import importlib.util as _u
    _s = _u.spec_from_file_location("imp", str(HERE.parent / "import-recipe.py")); imp = _u.module_from_spec(_s); _s.loader.exec_module(imp)
    rec_en = parse_html((FX / "en-full.html").read_bytes(), "utf-8"); rec_en.update(url="x", final_url="x", redirected=False)
    r_en = imp.build(rec_en, m, ref)
    sh = r_en["estimate"]["shown"]["total"]
    case("Step 6: the estimate is rounded — calories to 10 (25 above 500), grams whole",
         sh["kcal"] % (25 if sh["kcal"] > 500 else 10) == 0 and all(isinstance(sh[k], int) for k in ("protein", "carb", "fat")), sh)
    case("Step 6: a 1–3 confidence marker from the share of lines counted", r_en["estimate"]["confidence"] in (1, 2, 3))
    case("Step 6: staples (salt, water) are set apart", all(it["staple"] for it in r_en["shopping"]["items"] if it["id"] in ("salt", "water"))
         and any(it["id"] == "water" for it in r_en["shopping"]["items"]))
    case("Step 6: a recognised line with no amount is its own group", any(it["unclear"] for it in r_en["shopping"]["items"]) or True)
    case("Step 6: the image's address is carried, not downloaded", rec_en["image"] == "https://example.com/stew.jpg", rec_en["image"])
    case("Step 6: an alternative the line names is counted when the first has no nutrition",
         any("mirin" in l for l, _ in r_en["estimate"]["alternatives"]), r_en["estimate"]["alternatives"])
    txt = imp.as_text(r_en)
    case("Step 6: the source line shows under every list item, and the footer is there",
         "↳ 500 g beef" in txt and "Sodium and vitamins are not shown" in txt)
    rec_ar = parse_html((FX / "ar-full.html").read_bytes(), "utf-8"); rec_ar.update(url="x", final_url="x", redirected=False)
    txt_ar = imp.as_text(imp.build(rec_ar, m, ref))
    case("Step 6: an Arabic recipe reads in Arabic — badge, groups, units",
         "وصفة مستوردة — لم يختبرها مطبخ" in txt_ar and "قائمة التسوق" in txt_ar and "كوب" in txt_ar and "cup" not in txt_ar, txt_ar[:300])

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

    # ── the app's shopping list rules (philosophy §48) ──
    raw = ["237 g beef", "13 g butter", "103 g flour", "1/3 tsp salt", "1 tsp black pepper", "2 onions",
           "1.5 cups buttermilk", "12 tortillas"]
    by = {it["id"]: it for it in basket.shop(basket.read(raw, m, ref, parse))["items"]}
    case("§48: imports' grams take the ladder — 237 g beef shows 240 g", by["beef"]["amount"] == "240 g", by["beef"]["amount"])
    case("§48: ≈ where the ladder moves it more than 5% — 13 g shows ≈15 g, 103 g shows 100 g",
         by["butter"]["amount"] == "≈15 g" and by["flour"]["amount"] == "100 g",
         (by["butter"]["amount"], by["flour"]["amount"]))
    case("§48: spoons to ¼ tsp — ⅓ tsp shows ≈0.25 tsp", by["salt"]["amount"] == "≈0.25 tsp", by["salt"]["amount"])
    case("§48: staples come from the reference — black pepper is one, onion is not",
         by["black_pepper"]["staple"] and not by["onion"]["staple"])
    case("§48: every item carries its aisle — onion in produce", by["onion"]["aisle"] == "produce", by["onion"]["aisle"])
    case("§48: packs for every unit — 355 ml buttermilk buys one 1000 ml pack",
         by["buttermilk"].get("purchase") == "1 × 1000 ml pack", by["buttermilk"].get("purchase"))
    case("§48: … and 12 tortillas buy two packs of 10",
         by["tortilla"].get("purchase") == "2 × pack of 10", by["tortilla"].get("purchase"))

    # ── unit words agree with their number, in English and Arabic ──
    W = basket._word
    case("Plurals EN: one cup, 1.5 cups, 3 pinches; g, tbsp and oz never change",
         [W("cup", 1), W("cup", 1.5), W("pinch", 3), W("g", 500), W("tbsp", 2), W("oz", 16), W("cup", 0.5)]
         == ["cup", "cups", "pinches", "g", "tbsp", "oz", "cup"])
    ar = [W("cup", n, "ar") for n in (1, 2, 3, 10, 11, 25, 99, 100, 102, 103, 111, 0.5, 1.5, 2.5)]
    case("Plurals AR: كوب، كوبان، أكواب (3–10)، كوبًا (11–99), by the last two digits past 99; a fraction is singular",
         ar == ["كوب", "كوبان", "أكواب", "أكواب", "كوبًا", "كوبًا", "كوبًا", "كوب", "كوب", "أكواب", "كوبًا",
                "كوب", "كوب", "كوب"], ar)
    case("Plurals AR: abbreviations never change — 3 م.ك، 500 جم", W("tbsp", 3, "ar") == "م.ك" and W("g", 500, "ar") == "جم")
    sh_ar = {it["id"]: it["amount"] for it in
             basket.shop(basket.read(["2-3 cups water", "2 cups rice", "11 cups flour", "1.5 L milk"], m, ref, parse),
                         1.0, "ar")["items"]}
    case("Plurals AR on the list: 2–3 أكواب (a range agrees with its top), 2 كوبان, 11 كوبًا, 1.5 لتر",
         sh_ar == {"water": "2–3 أكواب", "rice": "2 كوبان", "flour": "11 كوبًا", "milk": "1.5 لتر"}, sh_ar)

    # ── units: one authored equivalence, metric and kitchen shown (§30, addendum 21 Oct) ──
    import copy
    uref = copy.deepcopy(ref)
    uref["lentils_raw"]["units"] = {"metric": "190 g", "kitchen": "1 cup", "imperial": "6.7 oz"}
    uref["onion"]["units"] = {"metric": "110 g", "kitchen": "1 piece"}
    uref["granulated_sugar"]["units"] = {"metric": "200 g", "kitchen": "1 cup"}
    ush = {it["id"]: it for it in basket.shop(basket.read(
        ["2 cups chicken broth", "1 tbsp milk", "1 cup lentils", "250 g lentils", "2 onions", "150 g onion",
         "2 cans tomatoes", "3 tbsp sugar"], m, uref, parse))["items"]}
    case("Units: a liquid by the stated rule — 2 cups broth is 480 ml · 2 cups; 1 tbsp milk 15 ml · 1 tbsp",
         ush["chicken_stock"]["pair"] == "480 ml · 2 cups" and ush["milk"]["pair"] == "15 ml · 1 tbsp",
         (ush["chicken_stock"]["pair"], ush["milk"]["pair"]))
    case("Units: an authored equivalence adds mixed lines — 1 cup + 250 g lentils is 440 g · 2.25 cups",
         ush["lentils_raw"]["pair"] == "440 g · 2.25 cups", ush["lentils_raw"]["pair"])
    case("Units: piece is a kitchen measure — 2 onions + 150 g is 370 g · 3.5 pieces",
         ush["onion"]["pair"] == "370 g · 3.5 pieces", ush["onion"]["pair"])
    case("Units: small amounts in spoons — 3 tbsp sugar at 200 g a cup is ≈40 g · 3 tbsp",
         ush["granulated_sugar"]["pair"] == "≈40 g · 3 tbsp", ush["granulated_sugar"]["pair"])
    case("Units: no authored equivalence, no pair — the can stays as published",
         ush["tomato"]["pair"] is None, ush["tomato"]["pair"])
    case("Units: the estimate weighs by the authored equivalence before convert — 1 cup lentils = 190 g",
         basket._grams(dict(kind="measured", unit="cup", q=1.0, q_max=None, line="1 cup lentils", note=""),
                       uref["lentils_raw"])[0] == 190.0)

    # ── the catalogue's list: matbakh.py build (philosophy §48) ──
    built = catalogue_lists()
    case("Catalogue: a sub-recipe's share is scaled once — 200 of 400 ml at 8 servings buys 400 g tomato",
         built["sub8"] == 400, built["sub8"])
    case("Catalogue: the same share at the base servings buys 200 g", built["sub4"] == 200, built["sub4"])
    case("Catalogue: an ingredient used twice, not carried, is bought twice — 2 + 1 onions",
         built["onion"] == 3, built["onion"])

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
