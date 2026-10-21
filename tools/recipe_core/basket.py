"""From a recipe's ingredient lines to a shopping list and a nutrition estimate.

    lines = read(ingredient_lines, matcher, ref)        # parse + match each line
    shopping = shop(lines, factor)                       # one entry per reference id
    est = estimate(lines, factor, servings)              # labelled تقدير by the caller

The rules (tools/RecipeCoreDesign.md):
  - a line the reference does not know stays on the list as text — never dropped;
  - quantities are added only when their units can be: mass to mass, volume to
    volume, a count to a count; anything else is shown beside the total, never
    folded into it;
  - the purchase is rounded up to the entry's `pack`, or counted in what one unit
    `makes` (stock cubes, philosophy §47);
  - the estimate counts a line only when its weight AND its nutrition are known,
    and lists every other line by name with the reason. It never guesses a weight.
A range ("2–3 cups") stays a range on the list; the estimate takes its middle and
says so.
"""

import math, re

# grams per unit of mass, millilitres per unit of volume
MASS = {"g": 1, "kg": 1000, "mg": 0.001, "oz": 28.35, "lb": 453.6}
VOLUME = {"ml": 1, "l": 1000, "cl": 10, "dl": 100, "cup": 240, "tbsp": 15, "tsp": 5,
          "spoon": 15, "fl_oz": 29.57, "pint": 473, "quart": 946,
          "rice_cup": 180}        # a rice cooker's cup
COUNTED = {"", "piece", "clove"} # "2 eggs", "1 piece ginger", "2 cloves garlic" (garlic is counted in cloves)
PACKED = {"packet", "can", "jar", "stick"}   # weighed by the size the line gives: "1 (16 ounce) package tofu"
TOO_SMALL = {"pinch"}           # a pinch counts for nothing in an estimate

NUTRIENTS = ("kcal", "protein", "carb", "fat")
# the reference's `aisle`, in the order a shop is walked (philosophy §48)
AISLES = ("produce", "butcher", "chiller", "freezer", "bakery", "dry_goods", "jars_tins", "spices", "drinks")


def by_aisle(items):
    """Items in aisle order, recipe order kept within an aisle; no aisle last."""
    return sorted(items, key=lambda it: AISLES.index(it["aisle"]) if it.get("aisle") in AISLES else len(AISLES))

# unit words as a shopper reads them, by the recipe's language
UNIT_WORDS = {
    "en": {"rice_cup": "rice cup", "fl_oz": "fl oz"},
    "ar": {"g": "جم", "kg": "كجم", "mg": "مجم", "ml": "مل", "L": "لتر", "l": "لتر", "cl": "سل", "dl": "دل",
           "cup": "كوب", "tbsp": "م.ك", "tsp": "م.ص", "spoon": "ملعقة", "pinch": "رشة", "clove": "فص",
           "piece": "حبة", "can": "علبة", "packet": "كيس", "jar": "برطمان", "bunch": "حزمة",
           "slice": "شريحة", "stick": "عود", "head": "رأس", "sprig": "عرق", "leaf": "ورقة",
           "handful": "حفنة", "cube": "مكعب", "oz": "أونصة", "lb": "رطل", "rice_cup": "كوب أرز",
           "fl_oz": "أونصة سائلة", "pint": "باينت", "quart": "كوارت", "inch": "بوصة", "glass": "كوب"},
}
PHRASES = {
    "en": {"as_needed": "as needed", "pack": "{n} × {size} {unit} pack", "pack_count": "{n} × pack of {size}",
           "cubes": "{n} × {per} (1 per {ml} ml)"},
    "ar": {"as_needed": "حسب الحاجة", "pack": "{n} × عبوة {size} {unit}", "pack_count": "{n} × عبوة {size} حبات",
           "cubes": "{n} × مكعب (مكعب لكل {ml} مل)"},
}
_OR = re.compile(r"\b(?:or)\b|أو|(?<![ء-ي])او(?![ء-ي])", re.I)


def _f(x):
    try:
        return float(x) if x not in (None, "") else None
    except ValueError:
        return None


def read(raw_lines, matcher, ref, parse):
    """Each line parsed and matched: dicts with the parser's fields plus id, entry."""
    out = []
    for raw in raw_lines:
        p = parse(raw)
        p["line"] = raw
        if p["kind"] == "heading":
            continue
        iid, on = matcher.match(p["name"]) if p["name"] else ("", "")
        iid, on = _with_descriptor(p, iid, on, matcher)
        e = ref.get(iid) if iid else None
        p.update(id=iid, matched_on=on, entry=e, q=_f(p["qty"]), q_max=_f(p["qty_max"]))
        if e:
            _one_by_singular(p, e)
            _cube_to_ml(p, e)
            _stalk_is_one(p, e)
        if not _has_nutrition(e):
            p["alt"] = _alternative(p, matcher, ref)
        out.append(p)
    return out


def _has_nutrition(e):
    return bool(e) and any(k in (e.get("nutrition") or {}) for k in NUTRIENTS)


def _alternative(p, matcher, ref):
    """'mirin, rice vinegar, or cider vinegar': when the first has no nutrition, the first
    alternative the line itself names that does — for the estimate only; the list keeps
    the line as written. Only on a line that offers alternatives ("or", أو)."""
    if not _OR.search(p["line"]):
        return None
    text = p["name"] + ", " + (p.get("note") or "")
    for frag in re.split(r"\s*(?:,|،|;|/|\bor\b|أو|(?<![ء-ي])او(?![ء-ي]))\s*", text, flags=re.I):
        frag = frag.strip(" ()")
        if not frag:
            continue
        iid, _ = matcher.match(frag)
        if iid and iid != p["id"] and _has_nutrition(ref.get(iid)):
            return iid
    return None


_SIZE = re.compile(r"(\d+(?:[.,]\d+)?)\s*-?\s*(ounces?|oz|grams?|g|kg|pounds?|lbs?|lb|ml|milliliters?|l|liters?)\b", re.I)
_SIZE_UNIT = {"ounce": "oz", "ounces": "oz", "oz": "oz", "gram": "g", "grams": "g", "g": "g", "kg": "kg",
              "pound": "lb", "pounds": "lb", "lbs": "lb", "lb": "lb", "ml": "ml", "milliliter": "ml",
              "milliliters": "ml", "l": "l", "liter": "l", "liters": "l"}


def _pack_size(p):
    """For "1 (16 ounce) package tofu": the size inside one package, as (qty, unit), or None."""
    if p["unit"] not in PACKED:
        return None
    m = _SIZE.search(p.get("note") or "") or _SIZE.search(p["line"])
    return (float(m.group(1).replace(",", ".")), _SIZE_UNIT[m.group(2).lower()]) if m else None


_AR_UNITY = re.compile(r"^[ء-ي]{2,}(?:ة|ه|اية|ايه)(?![ء-ي])")


def _with_descriptor(p, iid, on, matcher):
    """Some sites put a short descriptor before the amount — "ناشفة ملعقة كبيرة كزبرة"
    (dried coriander) — and the parser sets it aside in the note. Match the name with
    it too, and keep that match when it finds a longer, more specific name: كزبرة
    ناشفة is ground coriander, not the fresh coriander a bare كزبرة means."""
    seg = (p.get("note") or "").split(";")[0].strip()
    if not seg or len(seg.split()) > 2 or not p["name"]:
        return iid, on
    i2, on2 = matcher.match(p["name"] + " " + seg)
    if iid and i2 and matcher.match(seg)[0] == i2:
        return iid, on   # "cornstarch (corn flour)": the note is another name, not a description
    if i2 and i2 != iid and len(on2.lstrip("=").split()) > len((on or "").lstrip("=").split()):
        return i2, on2
    return iid, on


def _one_by_singular(p, e):
    """Arabic names one counted item by its singular: بصلة / بصلايه is one onion. Only for an
    entry counted one by one (unit count, or a weight per item) and a word with the singular
    ending — قرفة (cinnamon) is not one of anything, and it has no weight per item."""
    if p["q"] is None and not p["unit"] and p["kind"] == "no_quantity" and             (e.get("unit") == "count" or (e.get("convert") or {}).get("piece_g")) and _AR_UNITY.match(p["name"]):
        p.update(q=1.0, qty="1", kind="count", implied=True)


def _stalk_is_one(p, e):
    """'2 stalks scallions', '2 sticks celery': a stalk of something counted by the piece
    is one piece. A stick with a stated size ('1 (4 oz) stick butter') keeps its size."""
    if p["unit"] == "stick" and (e.get("convert") or {}).get("piece_g") and not _pack_size(p):
        p["unit"] = ""


def _cube_to_ml(p, e):
    """مكعب مرقة: one stock cube is what it makes (philosophy §47)."""
    mk = e.get("makes")
    if p["unit"] == "cube" and mk and mk.get("per") == "cube" and p["q"] is not None:
        p.update(q=p["q"] * mk["ml"], q_max=(p["q_max"] or 0) * mk["ml"] or None, unit="ml")


def _dim(unit):
    if unit in MASS:
        return "mass"
    if unit in VOLUME:
        return "volume"
    if unit in COUNTED:
        return "count"
    return "other"


def _base(q, unit):
    """q in grams, millilitres or items, by the unit's dimension."""
    return q * MASS.get(unit, VOLUME.get(unit, 1))


def _fmt(x):
    if x is None:
        return ""
    x = round(x, 2)
    return str(int(x)) if float(x).is_integer() else f"{x:g}"


def _ladder(v):
    """philosophy §6.3: grams and millilitres to what a kitchen can measure — 1 under 10,
    5 to 100, 10 to 500, 25 above."""
    step = 1 if v < 10 else 5 if v < 100 else 10 if v < 500 else 25
    return max(step, round(v / step) * step) if v > 0 else v


def _spoon(v, unit):
    """¼ tsp, ½ tbsp (§6.3)."""
    step = 0.25 if unit == "tsp" else 0.5
    return max(step, round(v / step) * step)


def _off(exact, shown):
    """§6.3's ≈: the shown figure is more than 5% from the exact one."""
    return bool(exact) and abs(shown - exact) / exact > 0.05


# English plurals: abbreviations (g, tbsp, oz) never take one; one cup, 1.5 cups.
EN_PLURAL = {"cup": "cups", "rice cup": "rice cups", "spoon": "spoons", "pinch": "pinches",
             "clove": "cloves", "piece": "pieces", "can": "cans", "packet": "packets", "jar": "jars",
             "bunch": "bunches", "slice": "slices", "stick": "sticks", "head": "heads",
             "sprig": "sprigs", "leaf": "leaves", "handful": "handfuls", "cube": "cubes",
             "pint": "pints", "quart": "quarts", "inch": "inches", "glass": "glasses"}
# Arabic: (dual, 3–10, 11–99) beside the singular; abbreviations (جم، مل، م.ك) never change.
# A fraction takes the singular: ½ كوب، 1.5 كوب.
AR_FORMS = {
    "كوب": ("كوبان", "أكواب", "كوبًا"), "لتر": ("لتران", "لترات", "لترًا"),
    "ملعقة": ("ملعقتان", "ملاعق", "ملعقةً"), "رشة": ("رشتان", "رشات", "رشةً"),
    "فص": ("فصان", "فصوص", "فصًا"), "حبة": ("حبتان", "حبات", "حبةً"),
    "علبة": ("علبتان", "علب", "علبةً"), "كيس": ("كيسان", "أكياس", "كيسًا"),
    "برطمان": ("برطمانان", "برطمانات", "برطمانًا"), "حزمة": ("حزمتان", "حزم", "حزمةً"),
    "شريحة": ("شريحتان", "شرائح", "شريحةً"), "عود": ("عودان", "أعواد", "عودًا"),
    "رأس": ("رأسان", "رؤوس", "رأسًا"), "عرق": ("عرقان", "عروق", "عرقًا"),
    "ورقة": ("ورقتان", "أوراق", "ورقةً"), "حفنة": ("حفنتان", "حفنات", "حفنةً"),
    "مكعب": ("مكعبان", "مكعبات", "مكعبًا"), "أونصة": ("أونصتان", "أونصات", "أونصةً"),
    "رطل": ("رطلان", "أرطال", "رطلًا"), "كوب أرز": ("كوبا أرز", "أكواب أرز", "كوبًا من الأرز"),
    "أونصة سائلة": ("أونصتان سائلتان", "أونصات سائلة", "أونصةً سائلة"),
    "باينت": ("باينتان", "باينتات", "باينتًا"), "كوارت": ("كوارتان", "كوارتات", "كوارتًا"),
    "بوصة": ("بوصتان", "بوصات", "بوصةً"),
}


def _ar_form(w, n):
    """The Arabic word for n of it: 1 كوب، 2 كوبان، 3–10 أكواب، 11–99 كوبًا; past 99 by the
    last two digits (103 أكواب، 111 كوبًا), and 100 or 101 or 102 take the singular."""
    forms = AR_FORMS.get(w)
    if not forms or n is None or abs(n - round(n)) > 1e-9:
        return w
    k = int(round(n))
    if k == 2:
        return forms[0]
    r = k % 100
    return forms[1] if 3 <= r <= 10 else forms[2] if r >= 11 else w


def _word(unit, n=1, lang="en"):
    """A unit key as a shopper reads it, in the list's language, agreeing with the number
    shown beside it (the top of a range): cup → cups, كوب → كوبان / أكواب / كوبًا."""
    words = UNIT_WORDS.get(lang, UNIT_WORDS["en"])
    w = words.get(unit, UNIT_WORDS["en"].get(unit, unit))
    if lang == "ar":
        return _ar_form(w, n)
    return EN_PLURAL.get(w, w) if n is not None and n > 1 + 1e-9 else w


def _show(lo, hi, dim, lang="en"):
    """A total in the unit a shopper reads: g or kg, ml or L, items."""
    unit, div = {"mass": ("g", 1), "volume": ("ml", 1), "count": ("", 1)}[dim]
    if dim == "mass" and lo >= 1000:
        unit, div = "kg", 1000
    if dim == "volume" and lo >= 1000:
        unit, div = "L", 1000
    if dim == "count":
        return _fmt(lo) + ("–" + _fmt(hi) if hi and hi != lo else "")
    ends = [lo] + ([hi] if hi and hi != lo else [])
    shown = [_ladder(x) for x in ends]
    approx = "≈" if any(_off(x, y) for x, y in zip(ends, shown)) else ""
    amt = "–".join(_fmt(y / div) for y in shown)
    return (approx + amt + " " + _word(unit, round(shown[-1] / div, 2), lang)).strip()


def shop(lines, factor=1.0, lang="en"):
    """The shopping list: matched entries first, in recipe order, then unmatched lines."""
    items, order, text = {}, [], []
    for p in lines:
        if not p["id"]:
            text.append(p["line"])
            continue
        if p["id"] not in items:
            items[p["id"]] = []
            order.append(p["id"])
        items[p["id"]].append(p)
    out = []
    for iid in order:
        ps, e = items[iid], items[iid][0]["entry"] or {}
        name = (e.get("name") or {}).get(lang) or (e.get("name") or {}).get("en") or iid
        sums, extras, units = {}, [], {}
        for p in ps:
            ps_ = _pack_size(p)
            if ps_ and p["q"] is not None:
                p = dict(p, q=p["q"] * ps_[0], q_max=(p["q_max"] or 0) * ps_[0] or None, unit=ps_[1])
            dim = _dim(p["unit"])
            if p["q"] is None or dim == "other":
                q = (_fmt(p["q"] * factor) + ("–" + _fmt(p["q_max"] * factor) if p["q_max"] else "")
                     if p["q"] is not None else "")
                extras.append((q + " " + _word(p["unit"], round((p["q_max"] or p["q"]) * factor, 2), lang)).strip() if q
                              else PHRASES.get(lang, PHRASES["en"])["as_needed"])
                continue
            lo, hi = sums.get(dim, (0.0, 0.0))
            b = _base(p["q"] * factor, p["unit"])
            bh = _base((p["q_max"] or p["q"]) * factor, p["unit"])
            sums[dim] = (lo + b, hi + bh)
            units.setdefault(dim, set()).add(p["unit"])
        amounts = []
        for d, (lo, hi) in sums.items():
            only = units[d].pop() if len(units[d]) == 1 else None
            if only and d != "count" and not (only in ("g", "ml") and lo >= 1000):
                # all in one unit: say it the way the recipe does (but 1500 g reads as 1.5 kg)
                # in the recipe's own unit, on §6.3's ladder where it has one
                k = MASS.get(only, VOLUME.get(only, 1))
                if only in ("g", "ml"):
                    amounts.append(_show(lo, hi, d, lang))
                    continue
                ends = [lo / k] + ([hi / k] if hi != lo else [])
                shown = [_spoon(x, only) for x in ends] if only in ("tsp", "tbsp") else ends
                approx = "≈" if any(_off(x, y) for x, y in zip(ends, shown)) else ""
                amounts.append((approx + "–".join(_fmt(y) for y in shown) + " "
                                + _word(only, round(shown[-1], 2), lang)).strip())
            elif d == "volume" and e.get("unit") != "ml" and (e.get("convert") or {}).get("cup_g"):
                # cups and spoons mixed, of something sold by weight: say it in grams
                k = e["convert"]["cup_g"] / 240
                amounts.append(_show(lo * k, hi * k, "mass", lang))
            else:
                amounts.append(_show(lo, hi, d, lang))
        ph = PHRASES.get(lang, PHRASES["en"])
        item = dict(id=iid, name=name, amount=" + ".join(amounts + extras),
                    lines=[p["line"] for p in ps], buy=((e.get("buy") or {}).get(lang) or ""),
                    staple=e.get("staple") is True, aisle=e.get("aisle"),
                    unclear=not amounts)        # recognised, but the source gives no amount
        # what to buy: whole packs, or the cubes that make this much stock (§47)
        mk, pack = e.get("makes"), e.get("pack")
        if mk and "volume" in sums:
            item["purchase"] = ph["cubes"].format(n=max(1, math.ceil(sums["volume"][1] / mk["ml"] - 1e-9)),
                                                  per=mk["per"], ml=mk["ml"])
        elif pack:
            # whole packs, for every unit the reference sells by (§48); a range buys for its top
            dim = {"g": "mass", "ml": "volume", "count": "count"}.get(e.get("unit"))
            if dim in sums:
                n = max(1, math.ceil(sums[dim][1] / pack - 1e-9))
                item["purchase"] = (ph["pack_count"].format(n=n, size=pack) if dim == "count" else
                                    ph["pack"].format(n=n, size=pack, unit=_word(e["unit"], 1, lang)))
        out.append(item)
    return dict(items=out, not_matched=text)


def _grams(p, e):
    """(grams or ml, None) for a line the estimate can weigh, or (None, reason)."""
    if p["kind"] == "to_taste" or p["unit"] in TOO_SMALL:
        return None, "too small to count"
    if p["q"] is None:
        return None, "no quantity"
    q = (p["q"] + p["q_max"]) / 2 if p["q_max"] else p["q"]
    conv, unit = e.get("convert") or {}, p["unit"]
    size = _pack_size(p)
    if size:
        q, unit = q * size[0], size[1]
    if unit in MASS:
        return q * MASS[unit], None
    if unit in VOLUME:
        ml = q * VOLUME[unit]
        if e.get("unit") == "ml":
            return ml, None
        if conv.get("cup_g"):
            return ml * conv["cup_g"] / 240, None
        return None, "no weight per cup for this ingredient"
    if unit in COUNTED:
        if conv.get("piece_g"):
            return q * conv["piece_g"], None
        return None, "no weight per item for this ingredient"
    return None, f"no weight for a {unit}"


def estimate(lines, factor=1.0, servings=None, ref=None):
    """Totals for the recipe (scaled by factor) and per serving, with every line it
    could not count and why, and every line counted as an alternative it names. The
    caller labels it تقدير."""
    tot = dict.fromkeys(NUTRIENTS, 0.0)
    counted, skipped, ranged, alts = 0, [], False, []
    for p in lines:
        e = p["entry"]
        if e and e.get("glyph") == "water":
            counted += 1                      # water: nothing to count, and nothing missing
            continue
        if not _has_nutrition(e) and p.get("alt") and ref:
            e = ref[p["alt"]]                 # "mirin, rice vinegar, or cider vinegar"
            alts.append((p["line"], (e.get("name") or {}).get("en") or p["alt"]))
        if not e:
            skipped.append((p["line"], "not in the reference"))
            continue
        n = e.get("nutrition") or {}
        if not any(k in n for k in NUTRIENTS):
            skipped.append((p["line"], "no nutrition data for this ingredient"))
            continue
        g, why = _grams(p, e)
        if g is None:
            skipped.append((p["line"], why))
            continue
        ranged |= bool(p["q_max"])
        for k in NUTRIENTS:
            tot[k] += g * factor / 100 * (n.get(k) or 0)
        counted += 1
    per = {k: v / servings for k, v in tot.items()} if servings else None
    share = counted / len(lines) if lines else 0
    confidence = 3 if share >= 0.9 else 2 if share >= 0.7 else 1
    return dict(total=tot, per_serving=per, counted=counted, of=len(lines),
                not_counted=skipped, ranges_at_middle=ranged, alternatives=alts,
                confidence=confidence)


def rounded(n):
    """How the estimate is shown (the mock-up's screen 5): calories to 10, or to 25 above
    500; grams to whole numbers. Precision the data does not have is not shown."""
    k = n["kcal"]
    step = 25 if k > 500 else 10
    return dict(kcal=int(round(k / step) * step), protein=round(n["protein"]),
                carb=round(n["carb"]), fat=round(n["fat"]))
