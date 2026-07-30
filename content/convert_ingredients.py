#!/usr/bin/env python3
"""
Convert BirdRock's ingredients table into Matbakh's ref/ingredients.yaml.

    python3 convert_ingredients.py birdrock.db > ref/ingredients.yaml

Decisions encoded here, and why:

  cost_per_unit / pack_price / supplier are DROPPED. Matbakh prices come from
  the market feed at render time. BirdRock's costs are one institution's
  purchase prices and would be wrong and stale in a consumer app.

  cls is derived from `type`, never from the name. "Bell pepper" and "Green
  pepper" contain "pepper" but are vegetables that scale linearly; a name rule
  would class them as seasoning and quietly under-scale them.

  The 12 hand-curated entries are preserved exactly. BirdRock measures onion,
  garlic and lemon in grams, which suits an institutional kitchen; a home cook
  reads "2 onions", so the curated count-based versions win.

  nutrition is per 100 g or 100 ml, matching BirdRock's USDA basis. This is
  what lets per-serving nutrition be computed from step data instead of
  hand-entered 500 times.
"""

import sqlite3
import sys

# BirdRock name → existing curated key. These keep their curated definitions.
CURATED = {
    "Chicken, whole bone-in": "chicken_whole",
    "Jute Mallow (Molokheya)": "molokhia_frozen",
    "Rice": "rice",
    "Ghee": "ghee",
    "Onion": "onion",
    "Garlic": "garlic",
    "Coriander, fresh": "coriander_fresh",
    "Coriander, dry": "coriander_ground",
    "Lemon": "lemon",
    "Bay leaves": "bay_leaf",
    "Salt": "salt",
    "Water": "water",
}

# type → default glyph
GLYPH = {
    "Produce": "vegetable", "Pantry": "jar", "Spice": "spice", "Baking": "flour",
    "Dairy": "dairy", "Legumes & Grains": "grain", "Proteins": "meat",
    "Meat": "meat", "Fat": "fat", "Frozen": "frozen", "Sub-recipe": "pot",
    "General": "jar", "Other": "jar",
}

# type → scaling class. Spices scale sub-linearly; everything else linearly
# unless the unit says otherwise.
SEASONING_TYPES = {"Spice"}
FIXED_NAMES = {"Water"}

# Whole items that can sensibly be halved.
DIVISIBLE = {"apple", "baguette", "lemon", "onion"}

# type → bilingual buy hint, used when pack size gives no better answer.
BUY = {
    "Produce": ("loose", "بالوزن"),
    "Spice": ("from jar", "من البرطمان"),
    "Dairy": ("from the chiller", "من التلاجة"),
    "Proteins": ("from the butcher", "من الجزار"),
    "Meat": ("from the butcher", "من الجزار"),
    "Frozen": ("frozen aisle", "من المجمدات"),
    "Fat": ("from jar", "من البرطمان"),
    "Baking": ("baking aisle", "قسم المخبوزات"),
    "Legumes & Grains": ("dry goods", "بقالة جافة"),
    "Pantry": ("pantry staple", "من البقالة"),
    "Sub-recipe": ("made at home", "يُحضّر بالبيت"),
    "General": ("pantry staple", "من البقالة"),
    "Other": ("pantry staple", "من البقالة"),
}

UNIT = {"g": "g", "kg": "g", "ml": "ml", "each": "count"}


def key_for(name):
    out = []
    for ch in name.lower():
        out.append(ch if ch.isalnum() else "_")
    k = "".join(out)
    while "__" in k:
        k = k.replace("__", "_")
    return k.strip("_")


def q(s):
    """Quote a YAML scalar only when it needs it."""
    s = str(s)
    if any(c in s for c in ":#{}[],&*?|-<>=!%@`'\"") or s != s.strip():
        return '"' + s.replace('"', '\\"') + '"'
    return s


def main():
    con = sqlite3.connect(sys.argv[1] if len(sys.argv) > 1 else "birdrock.db")
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT * FROM ingredients ORDER BY type, name_en").fetchall()

    review = {"no_arabic": [], "no_nutrition": [], "discrete": [], "generic_buy": []}
    used, out = set(CURATED.values()), []

    for r in rows:
        name = (r["name_en"] or "").strip()
        if not name or name in CURATED:
            continue

        k = key_for(name)
        base, n = k, 2
        while k in used:
            k, n = f"{base}_{n}", n + 1
        used.add(k)

        typ = r["type"] or "General"
        unit = UNIT.get(r["unit"], "g")

        if name in FIXED_NAMES:
            cls = "fixed"
        elif typ in SEASONING_TYPES:
            cls = "seasoning"
        elif unit == "count":
            cls = "discrete"
        else:
            cls = "continuous"

        lines = [f"{k}:"]
        lines.append(f"  glyph: {GLYPH.get(typ, 'jar')}")
        ar = (r["name_ar"] or "").strip()
        if not ar:
            review["no_arabic"].append(name)
            ar = ""
        lines.append(f"  name: {{ en: {q(name)}, ar: {q(ar)} }}")
        lines.append(f"  unit: {unit}")
        lines.append(f"  cls: {cls}")

        if cls == "discrete":
            div = key_for(name).split("_")[0] in DIVISIBLE
            lines.append(f"  divisible: {'true' if div else 'false'}")
            review["discrete"].append(f"{name} → divisible: {div}")

        pack = r["pack_size"]
        if pack and float(pack) > 0:
            p = int(float(pack))
            lines.append(f"  pack: {p}")
            en = f"{p} {unit} pack" if unit != "count" else f"pack of {p}"
            lines.append(f"  buy: {{ en: {q(en)}, ar: {q(f'عبوة {p}')} }}")
        else:
            be, ba = BUY.get(typ, BUY["General"])
            lines.append(f"  buy: {{ en: {q(be)}, ar: {q(ba)} }}")
            review["generic_buy"].append(name)

        nut = {}
        for src, dst in (("nutrition_kcal", "kcal"), ("nutrition_protein", "protein"),
                         ("nutrition_carbs", "carb"), ("nutrition_fat", "fat"),
                         ("nutrition_fiber", "fiber")):
            v = r[src]
            if v is not None:
                nut[dst] = round(float(v), 2)
        if nut:
            lines.append("  # per 100 " + unit.replace("count", "g"))
            lines.append("  nutrition: { " +
                         ", ".join(f"{a}: {b}" for a, b in nut.items()) + " }")
        else:
            review["no_nutrition"].append(name)

        out.append((typ, name, "\n".join(lines)))

    print("# INGREDIENT REFERENCE — generated from BirdRock, then curated.")
    print("# Regenerate with: python3 convert_ingredients.py birdrock.db")
    print("#")
    print("# NO COST FIELD. Prices come from the market feed, keyed on the id.")
    print("# nutrition is per 100 g / 100 ml, USDA basis, and lets per-serving")
    print("# figures be computed from step data rather than hand-entered.")
    print()
    print("# ── Curated entries. Hand-written, count-based where a cook counts")
    print("#    rather than weighs. Do not regenerate these from BirdRock.")
    print("#    (kept verbatim from the existing file — see git history)")
    print()

    last = None
    for typ, name, block in sorted(out):
        if typ != last:
            print(f"\n# ── {typ} " + "─" * (56 - len(typ)))
            last = typ
        print(block)

    sys.stderr.write(f"\n{len(out)} generated + 12 curated = {len(out) + 12}\n")
    sys.stderr.write(f"\nNEEDS REVIEW\n")
    sys.stderr.write(f"  no Arabic name ({len(review['no_arabic'])}): "
                     + ", ".join(review["no_arabic"]) + "\n")
    sys.stderr.write(f"  no nutrition ({len(review['no_nutrition'])}): "
                     + ", ".join(review["no_nutrition"][:12]) + "\n")
    sys.stderr.write(f"  discrete items ({len(review['discrete'])}): "
                     + "; ".join(review["discrete"]) + "\n")
    sys.stderr.write(f"  generic buy hint ({len(review['generic_buy'])}) — "
                     "fine as a default, worth refining for common items\n")


if __name__ == "__main__":
    main()
