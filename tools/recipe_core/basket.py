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
          "spoon": 15, "fl_oz": 29.57, "pint": 473, "quart": 946}
COUNTED = {"", "piece", "clove"} # "2 eggs", "1 piece ginger", "2 cloves garlic" (garlic is counted in cloves)
PACKED = {"packet", "can", "jar", "stick"}   # weighed by the size the line gives: "1 (16 ounce) package tofu"
TOO_SMALL = {"pinch"}           # a pinch counts for nothing in an estimate

NUTRIENTS = ("kcal", "protein", "carb", "fat")


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
        out.append(p)
    return out


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


def _show(lo, hi, dim):
    """A total in the unit a shopper reads: g or kg, ml or L, items."""
    unit, div = {"mass": ("g", 1), "volume": ("ml", 1), "count": ("", 1)}[dim]
    if dim == "mass" and lo >= 1000:
        unit, div = "kg", 1000
    if dim == "volume" and lo >= 1000:
        unit, div = "L", 1000
    r = (lambda x: round(x)) if div == 1 and dim != "count" and lo >= 10 else (lambda x: x)
    amt = _fmt(r(lo / div)) + ("–" + _fmt(r(hi / div)) if hi and hi != lo else "")
    return (amt + " " + unit).strip()


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
                extras.append((q + " " + p["unit"]).strip() if q else "as needed")
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
                k = MASS.get(only, VOLUME.get(only, 1))
                amounts.append((_fmt(lo / k) + ("–" + _fmt(hi / k) if hi != lo else "") + " " + only).strip())
            else:
                amounts.append(_show(lo, hi, d))
        item = dict(id=iid, name=name, amount=" + ".join(amounts + extras),
                    lines=[p["line"] for p in ps], buy=((e.get("buy") or {}).get(lang) or ""))
        # what to buy: whole packs, or the cubes that make this much stock (§47)
        mk, pack = e.get("makes"), e.get("pack")
        if mk and "volume" in sums:
            item["purchase"] = f"{max(1, math.ceil(sums['volume'][1] / mk['ml'] - 1e-9))} × {mk['per']} (1 per {mk['ml']} ml)"
        elif pack and e.get("unit") == "g" and "mass" in sums:
            item["purchase"] = f"{max(1, math.ceil(sums['mass'][1] / pack - 1e-9))} × {pack} g pack"
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


def estimate(lines, factor=1.0, servings=None):
    """Totals for the recipe (scaled by factor) and per serving, with every line it
    could not count and why. The caller labels it تقدير."""
    tot = dict.fromkeys(NUTRIENTS, 0.0)
    counted, skipped, ranged = 0, [], False
    for p in lines:
        e = p["entry"]
        if not e:
            skipped.append((p["line"], "not in the reference"))
            continue
        if e.get("glyph") == "water":
            counted += 1                      # water: nothing to count, and nothing missing
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
    return dict(total=tot, per_serving=per, counted=counted, of=len(lines),
                not_counted=skipped, ranges_at_middle=ranged)
