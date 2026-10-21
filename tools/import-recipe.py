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
ingredient reference, and prints, in the recipe's language (Arabic or English):

  - the recipe as published — title, author, a link, the image's address, the
    ingredient lines and method as written (imports stay in source format,
    philosophy §44), under the badge *imported — not tested by Matbakh*;
  - a SHOPPING LIST in the mock-up's three groups (screen 4): recognised, with
    amounts and what to buy (whole packs, stock cubes, §47); recognised but with no
    amount; and not recognised — kept as written, never dropped. Staples (the
    reference's `staple`: salt, pepper, water, the cooking oils, sugar, flour) are
    on the list, set apart and unticked (philosophy §48). Within a group, items run
    in aisle order. The source line shows under every item, so a wrong match can
    be seen;
  - an ESTIMATE, labelled تقدير (screen 5): calories, protein, carbohydrate and fat,
    each ≈, calories rounded to 10 (25 above 500); a 1–3 dot confidence marker from
    the share of lines counted; every line it could not count, named, with why; and
    the footer saying what it is not.

A page with no recipe data gets a plain refusal, never a guess. It keeps nothing,
writes nothing, downloads no image, and sends nothing anywhere except the page
request (robots.txt respected). Shares its parts with capture-prefilter.py:
tools/recipe_core/. Step 6's fixes, 21 October 2026: 04-research/step6-review-2026-10-21.md.
"""

import argparse, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # tools/, for recipe_core
import yaml
from recipe_core import basket
from recipe_core.lines import parse
from recipe_core.match import Matcher
from recipe_core.page import PageError, parse_html, read_recipe

T = {
    "en": dict(
        badge="IMPORTED — not tested by Matbakh", by="by", image="image", servings="servings",
        not_given="not given", page_says="the page says", scaled="scaled linearly from {n} servings",
        no_base="the page gives no servings, so the recipe is shown as written",
        redirected="the page redirected to {u} — check it is the recipe you meant",
        ingredients="INGREDIENTS, as written", method="METHOD, as written",
        no_steps="METHOD: the page's data has no steps — read them on the page",
        shopping="SHOPPING LIST", g1="Recognised", g2="Recognised — the recipe gives no amount",
        g3="Not recognised — goes to Other, as written", staples="Staples you probably have — on the list, unticked",
        buy="buy", estimate="ESTIMATE — تقدير", per_serving="per serving", whole="whole recipe",
        kcal="kcal", protein="protein", carb="carbs", fat="fat", g="g",
        conf={3: "●●● high", 2: "●●○ medium", 1: "●○○ low"}, confidence="confidence",
        counted="{c} of {n} lines counted", middle="ranges taken at their middle",
        not_counted="not counted", as_alt="counted as {x}, an alternative the line names",
        nothing="nothing could be counted",
        footer="Estimated from the imported text, not tested by Matbakh. Sodium and vitamins are not shown."),
    "ar": dict(
        badge="وصفة مستوردة — لم يختبرها مطبخ", by="من", image="الصورة", servings="عدد الأشخاص",
        not_given="غير مذكور", page_says="الصفحة تقول", scaled="محسوبة بالتناسب من {n} أشخاص",
        no_base="الصفحة لا تذكر عدد الأشخاص، فالوصفة كما هي",
        redirected="الصفحة حوّلت إلى {u} — تأكد أنها الوصفة المقصودة",
        ingredients="المكونات، كما وردت", method="الطريقة، كما وردت",
        no_steps="الطريقة: بيانات الصفحة لا تحتوي على الخطوات — اقرأها في الصفحة",
        shopping="قائمة التسوق", g1="معروفة", g2="معروفة — الوصفة لا تذكر الكمية",
        g3="غير معروفة — تُضاف إلى «غير مصنف» كما وردت", staples="أساسيات غالباً عندك — في القائمة، بدون علامة",
        buy="اشترِ", estimate="تقدير — لم تختبره مطبخ", per_serving="للشخص", whole="الوصفة كاملة",
        kcal="سعرة", protein="بروتين", carb="كربوهيدرات", fat="دهون", g="جم",
        conf={3: "●●● عالية", 2: "●●○ متوسطة", 1: "●○○ منخفضة"}, confidence="الثقة",
        counted="حُسب {c} من {n} سطراً", middle="المدى محسوب من منتصفه",
        not_counted="لم يُحسب", as_alt="حُسب كـ{x}، بديل تذكره الوصفة",
        nothing="لم يمكن حساب شيء",
        footer="تقدير من النص المستورد، لم تختبره مطبخ. الصوديوم والفيتامينات غير معروضة."),
}
WHY_AR = {"too small to count": "كمية صغيرة لا تُحسب", "no quantity": "بلا كمية",
          "not in the reference": "غير موجود في قائمة مطبخ",
          "no nutrition data for this ingredient": "لا بيانات غذائية له",
          "no weight per cup for this ingredient": "لا وزن للكوب منه",
          "no weight per item for this ingredient": "لا وزن للحبة منه"}


def build(rec, matcher, ref, servings=None):
    lang = "ar" if rec.get("language") == "ar" else "en"
    base = rec.get("servings")
    factor = (servings / base) if (servings and base) else 1.0
    lines = basket.read(rec["ingredients"], matcher, ref, parse)
    shop = basket.shop(lines, factor, lang)
    est = basket.estimate(lines, factor, servings or base, ref)
    # the alternative counted, named in the recipe's language
    alt_name = {p["line"]: (ref[p["alt"]].get("name") or {}).get(lang) or (ref[p["alt"]].get("name") or {}).get("en")
                for p in lines if p.get("alt")}
    est["alternatives"] = [(l, alt_name.get(l, x)) for l, x in est["alternatives"]]
    est["shown"] = dict(total=basket.rounded(est["total"]),
                        per_serving=basket.rounded(est["per_serving"]) if est["per_serving"] else None)
    return dict(lang=lang,
                recipe={k: rec.get(k) for k in ("title", "author", "url", "final_url", "redirected", "image",
                                                 "source", "language", "yield_text", "servings",
                                                 "ingredients", "steps")},
                scaled_to=servings if (servings and base) else None,
                scale_note=("" if not servings else "scaled" if base else "no_base"),
                shopping=shop, estimate=est)


def as_text(r):
    L, rec, est, sh = T[r["lang"]], r["recipe"], r["estimate"], r["shopping"]
    ar = r["lang"] == "ar"
    out = [rec["title"] or "—", (f"{L['by']} {rec['author']} · " if rec["author"] else "") + (rec["url"] or ""), L["badge"]]
    if rec.get("image"):
        out.append(f"{L['image']}: {rec['image']}")
    if rec.get("redirected"):
        out.append(L["redirected"].format(u=rec["final_url"]))
    note = {"scaled": L["scaled"].format(n=rec["servings"]), "no_base": L["no_base"], "": ""}[r["scale_note"]]
    out.append(f"{L['servings']}: {r['scaled_to'] or rec['servings'] or L['not_given']}"
               + (f" ({note})" if note else "")
               + (f" — {L['page_says']} “{rec['yield_text']}”" if rec["yield_text"] else ""))
    out += ["", L["ingredients"]] + ["  " + l for l in rec["ingredients"]]
    if rec["steps"]:
        out += ["", L["method"]] + [f"  {i}. {s}" for i, s in enumerate(rec["steps"], 1)]
    else:
        out += ["", L["no_steps"]]

    def item(it):
        line = f"  {it['name']} — {it['amount']}"
        if it.get("purchase"):
            line += f"  → {L['buy']} {it['purchase']}"
        return [line] + [f"      ↳ {l}" for l in it["lines"]]

    items = sh["items"]
    items = basket.by_aisle(items)
    g1 = [it for it in items if not it["staple"] and not it["unclear"]]
    g2 = [it for it in items if not it["staple"] and it["unclear"]]
    st = [it for it in items if it["staple"]]
    out += ["", L["shopping"]]
    for head, group in ((L["g1"], g1), (L["g2"], g2)):
        if group:
            out.append(f" {head}")
            for it in group:
                out += item(it)
    if sh["not_matched"]:
        out.append(f" {L['g3']}")
        out += [f"  {t}" for t in sh["not_matched"]]
    if st:
        out.append(f" {L['staples']}")
        for it in st:
            out += item(it)

    out += ["", L["estimate"]]
    if est["counted"] == 0:
        out.append("  " + L["nothing"])
    else:
        g = L["g"]
        fmt = lambda d: (f"≈ {d['kcal']} {L['kcal']} · {L['protein']} ≈ {d['protein']} {g} · "
                         f"{L['carb']} ≈ {d['carb']} {g} · {L['fat']} ≈ {d['fat']} {g}")
        if est["shown"]["per_serving"]:
            out.append(f"  {L['per_serving']}: " + fmt(est["shown"]["per_serving"]))
        out.append(f"  {L['whole']}: " + fmt(est["shown"]["total"]))
    out.append(f"  {L['confidence']}: {L['conf'][est['confidence']]} — "
               + L["counted"].format(c=est["counted"], n=est["of"])
               + (f" ({L['middle']})" if est["ranges_at_middle"] else ""))
    for line, x in est["alternatives"]:
        out.append(f"  {line} — " + L["as_alt"].format(x=x))
    if est["not_counted"]:
        out.append(f"  {L['not_counted']}:")
        out += [f"    {l} — {WHY_AR.get(w, w) if ar else w}" for l, w in est["not_counted"]]
    out += ["", L["footer"]]
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
