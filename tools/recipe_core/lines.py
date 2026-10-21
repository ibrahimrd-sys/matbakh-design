"""Split an ingredient line into quantity, unit, name and note — moved unchanged from
ingredient-lines.py (import step 2). See that script's docstring for what it returns."""

import re, unicodedata


# ── numbers ────────────────────────────────────────────────────────────────

VULGAR = {"½": "1/2", "⅓": "1/3", "⅔": "2/3", "¼": "1/4", "¾": "3/4", "⅕": "1/5",
          "⅖": "2/5", "⅗": "3/5", "⅘": "4/5", "⅙": "1/6", "⅚": "5/6", "⅛": "1/8",
          "⅜": "3/8", "⅝": "5/8", "⅞": "7/8"}
DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")

WORDS = {
    # English
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "half": 0.5, "dozen": 12, "a dozen": 12, "half a": 0.5, "a half": 0.5,
    # French
    "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6,
    "sept": 7, "huit": 8, "neuf": 9, "dix": 10, "douze": 12, "demi": 0.5, "demie": 0.5,
    "une demi": 0.5, "un demi": 0.5, "une demie": 0.5,
    # Arabic
    "واحد": 1, "واحدة": 1, "اثنان": 2, "اثنين": 2, "اثنتان": 2, "اثنتين": 2,
    "ثلاث": 3, "ثلاثة": 3, "أربع": 4, "أربعة": 4, "اربع": 4, "اربعة": 4,
    "خمس": 5, "خمسة": 5, "ست": 6, "ستة": 6, "سبع": 7, "سبعة": 7, "ثمان": 8,
    "ثماني": 8, "ثمانية": 8, "تسع": 9, "تسعة": 9, "عشر": 10, "عشرة": 10,
    "نصف": 0.5, "ربع": 0.25, "ثلث": 1 / 3, "ثلاثة أرباع": 0.75, "ثلثين": 2 / 3,
}
WORD_RE = "|".join(sorted((re.escape(w) for w in WORDS), key=len, reverse=True))
NUM = r"\d+(?:[.,]\d+)?(?:\s+\d+/\d+)?|\d+/\d+"
RANGE_SEP = r"\s*(?:-|–|—|to|à|a|ou|or|إلى|الى|او|أو)\s*"


def _num(tok):
    tok = tok.strip()
    if tok.lower() in WORDS:
        return WORDS[tok.lower()]
    if re.fullmatch(r"\d+\s+\d+/\d+", tok):
        whole, frac = tok.split()
        a, b = frac.split("/")
        return int(whole) + int(a) / int(b)
    if "/" in tok:
        a, b = tok.split("/")
        return int(a) / int(b) if int(b) else None
    return float(tok.replace(",", "."))


# ── units ──────────────────────────────────────────────────────────────────
# (canonical key, multiplier for a dual form, pattern). Longest patterns first.

UNITS = [
    # Arabic duals: the unit word itself carries "two"
    ("cup", 2, r"كوبان|كوبين|كأسان|كأسين"),
    ("tbsp", 2, r"ملعقتان كبيرتان|ملعقتين كبيرتين|ملعقتان كبيرة|ملعقتين كبيرة|ملعقتا طعام|ملعقتين طعام"),
    ("tsp", 2, r"ملعقتان صغيرتان|ملعقتين صغيرتين|ملعقتان صغيرة|ملعقتين صغيرة|ملعقتا شاي|ملعقتين شاي"),
    ("tbsp", 2, r"معلقت(?:ين|ان) كبير(?:ة|ه|تين|تان)"),
    ("tsp", 2, r"معلقت(?:ين|ان) صغير(?:ة|ه|تين|تان)"),
    ("spoon", 2, r"ملعقتان|ملعقتين|معلقتان|معلقتين"),
    ("l", 2, r"لتران|لترين|ليتران|ليترين"),
    ("piece", 2, r"حبتان|حبتين"),
    ("clove", 2, r"فصان|فصين"),
    ("can", 2, r"علبتان|علبتين"),
    ("pinch", 2, r"رشتان|رشتين"),
    # Arabic
    ("tbsp", 1, r"(?:ملاعق|معالق) كبير[ةه]|(?:ملعق|معلق)[ةه] كبير[ةه]|ملاعق طعام|(?:ملعق|معلق)[ةه] طعام|م\.?\s?ك(?:بار|بير[ةه])?\b|م\s?كبار"),
    ("tsp", 1, r"(?:ملاعق|معالق) صغير[ةه]|(?:ملعق|معلق)[ةه] صغير[ةه]|ملاعق شاي|(?:ملعق|معلق)[ةه] شاي|م\.?\s?ص(?:غار|غير[ةه])?\b|م\s?صغار"),
    ("spoon", 1, r"ملاعق|معالق|ملعقة|ملعقه|معلقة|معلقه"),
    ("cube", 1, r"مكعبات|مكعب"),          # مكعب مرقة: a stock cube
    ("cup", 1, r"أكواب|اكواب|كوب|كأس|كاس|فنجان"),
    ("kg", 1, r"كيلوغرامات|كيلوغرام|كيلو جرام|كيلوجرام|كيلو غرام|كيلو|كجم|كغ"),
    ("g", 1, r"غرامات|غرام|جرامات|جرام|غم|جم|غ\b|جـم"),
    ("ml", 1, r"مليلتر|ملليلتر|ميليلتر|مل\b"),
    ("l", 1, r"لترات|لتر|ليتر"),
    ("pinch", 1, r"رشات|رش[ةه]|قرص[ةه]"),
    ("clove", 1, r"فصوص|فص"),
    ("piece", 1, r"حبات|حبة|حبه|قطع|قطعة"),
    ("can", 1, r"علب|علبة|علبه"),
    ("packet", 1, r"أكياس|كيس|ظرف|ظروف|باكيت"),
    ("bunch", 1, r"باقات|باقة|ربطة|حزمة|حزمه"),
    ("slice", 1, r"شرائح|شريحة"),
    ("stick", 1, r"أعواد|عود|أصابع|إصبع"),
    ("head", 1, r"رؤوس|رأس|راس"),
    # French
    ("moka", 1, r"cuill?\.?\s*à\s*moka|cuill[eè]res?\s+à\s+moka"),
    ("tbsp", 1, r"cuill?\.?\s*à\s*(?:soupe|s\.?)(?![a-z])|cuill[eè]res?\s+à\s+soupe|c\.?\s?à\.?\s?s(?:oupe)?\.?|c\.?s\.?(?=\s)|cas\b|càs\b"),
    ("tsp", 1, r"cuill?\.?\s*à\s*(?:caf[ée]|c\.?)(?![a-z])|cuill[eè]res?\s+à\s+caf[ée]|c\.?\s?à\.?\s?c(?:af[ée])?\.?|c\.?c\.?(?=\s)|cac\b|càc\b"),
    ("pinch", 1, r"pinc[ée]es?"),
    ("clove", 1, r"gousses?"),
    ("slice", 1, r"tranches?"),
    ("can", 1, r"bo[iî]tes?(?:\s+de\s+conserve)?"),
    ("packet", 1, r"sachets?"),
    ("glass", 1, r"verres?"),
    ("bunch", 1, r"bottes?|bouquets?"),
    ("sprig", 1, r"brins?"),
    ("leaf", 1, r"feuilles?"),
    ("piece", 1, r"morceaux?|pi[eè]ces?"),
    ("cl", 1, r"cl\b|centilitres?"),
    ("dl", 1, r"dl\b|décilitres?"),
    ("knob", 1, r"noix(?=\s+de\s+beurre)"),
    # English
    ("tbsp", 1, r"tablespoons?|tbsps?\.?|tbs\.?|tbl\.?|(?-i:T)\b"),    # capital T is a tablespoon
    ("tsp", 1, r"teaspoons?|tsps?\.?|(?-i:t)\b"),                      # small t is a teaspoon
    ("cup", 1, r"cups?|c\.(?=\s)"),
    ("fl_oz", 1, r"fl\.?\s?oz\.?|fluid ounces?"),
    ("oz", 1, r"ounces?|oz\.?"),
    ("lb", 1, r"pounds?|lbs?\.?"),
    ("quart", 1, r"quarts?|qts?\.?"),
    ("pint", 1, r"pints?|pts?\.?"),
    ("pinch", 1, r"pinch(?:es)?|dash(?:es)?"),
    ("clove", 1, r"cloves?"),
    ("can", 1, r"cans?|tins?"),
    ("packet", 1, r"packages?|packets?|pkgs?\.?|envelopes?|sachets?"),
    ("bunch", 1, r"bunch(?:es)?"),
    ("sprig", 1, r"sprigs?"),
    ("slice", 1, r"slices?"),
    ("stick", 1, r"sticks?|stalks?"),
    ("head", 1, r"heads?"),
    ("handful", 1, r"handfuls?"),
    ("piece", 1, r"pieces?"),
    ("jar", 1, r"jars?"),
    ("inch", 1, r"inch(?:es)?|\""),
    # metric, any language
    ("kg", 1, r"kg\b|kilos?\b|kilogrammes?|kilograms?"),
    ("mg", 1, r"mg\b"),
    ("g", 1, r"g\b|gr\.?\b|grammes?|grams?|gm\b"),
    ("ml", 1, r"ml\b|millilitres?|milliliters?"),
    ("l", 1, r"l\b|litres?|liters?"),
]
UNIT_RES = [(key, mult, re.compile(r"(?:" + pat + r")(?![^\W\d_])", re.I)) for key, mult, pat in UNITS]

TO_TASTE = re.compile(
    r"\b(?:to taste|as needed|as required|for serving|for garnish|selon (?:le |votre )?go[uû]ts?|"
    r"au go[uû]t|à volonté|selon besoin|facultatif)\b|"
    r"(?:حسب|بحسب)\s+(?:الرغبة|الحاجة|الذوق|الطلب)|للتزيين|للتقديم|حسب الرغبه",
    re.I)
HEADING = re.compile(r"^(?:.*:|ingr[ée]dients?|المكونات|المقادير)$", re.I)
SIZE = re.compile(r"(?:heaping|heaped|level|rounded|scant|generous|large|small|medium|big|tiny|good|"
                  r"belles?|grosses?|gros|petites?|petits?|bonnes?|bons?)\s+", re.I)
AFTER_UNIT = re.compile(r"^(?:rases?|bomb[ée]es?|pleines?|heaping|level|rounded)\b\s*", re.I)
AR_PLURAL = re.compile(r"(?:شرائح|أكواب|اكواب|ملاعق|معالق|مكعبات|فصوص|حبات|علب|أكياس|ظروف|باقات|أعواد|أصابع|رؤوس|قطع|غرامات|جرامات|لترات)(?![؀-ۿ])")
OF = re.compile(r"^(?:of\s+|de\s+|d['’]\s*|du\s+|des\s+|de la\s+|من\s+|\s)+", re.I)


def _norm(s):
    for k, v in VULGAR.items():          # before NFKC, which turns "1¼" into "11⁄4"
        s = s.replace(k, " " + v)
    s = unicodedata.normalize("NFKC", s)
    s = s.translate(DIGITS).replace("٫", ".").replace("،", ",").replace("⁄", "/")
    s = re.sub(r"(\d)\s*/\s*(\d)", r"\1/\2", s)
    s = re.sub(r"^[\s\-•*·▢]+", "", s)
    return " ".join(s.split())


def _take_qty(s):
    """Quantity at the start of s: (qty, qty_max, rest) or (None, None, s)."""
    tok = rf"(?:{NUM})(?![\d/])|(?:{WORD_RE})(?![^\W\d_])"
    m = re.match(rf"({tok})(?:{RANGE_SEP}({tok}))?", s, re.I)
    if not m:
        return None, None, s
    lo = _num(m.group(1))
    hi = _num(m.group(2)) if m.group(2) else None
    rest = s[m.end():].strip()
    # "1 1/2" already handled; Arabic "كوب ونصف" / "2 ونصف"
    return lo, hi, rest


def _take_unit(s):
    for key, mult, rx in UNIT_RES:
        m = rx.match(s)
        # the unit must end at a word boundary: "g" is not the start of "garlic"
        if m and m.end() > 0 and (m.end() == len(s) or not s[m.end()].isalpha()):
            rest = s[m.end():]
            extra = 0.0
            mm = re.match(r"\s*و\s*(نصف|ربع)(?![^\W\d_])", rest)   # كوب ونصف
            if mm:
                extra = WORDS[mm.group(1)]
                rest = rest[mm.end():]
            return key, mult, extra, rest.strip()
    return None, 1, 0.0, s


def _split_note(name):
    m = re.search(r"\s*[,(;]\s*|\s+[-–]\s+", name)
    if not m:
        return name.strip(), ""
    return name[:m.start()].strip(), name[m.start():].strip(" ,;-–")


def parse(line):
    raw = line
    s = _norm(line)
    out = {"line": raw, "qty": "", "qty_max": "", "unit": "", "name": "", "note": "", "kind": ""}
    if HEADING.match(s.strip()):          # "For the sauce:", "Ingrédients", "لتحضير الصوص:"
        return {**out, "name": s.strip(" :"), "kind": "heading"}
    to_taste = bool(TO_TASTE.search(s))
    # "2 - 15.5 ounce cans chickpeas": a count of packages of a stated size
    m = re.match(rf"(\d+)\s*[-–x×]\s*({NUM})\s*([a-z.]+)\s+(cans?|jars?|packages?|bottles?|tins?)\s+(.*)", s, re.I)
    if m and _take_unit(m.group(3))[0]:
        return {**out, "qty": m.group(1), "unit": "can" if m.group(4).lower().startswith(("can", "tin")) else
                _take_unit(m.group(4))[0] or "piece", "name": m.group(5).split(",")[0].strip(),
                "note": f"{m.group(2)} {m.group(3)} each", "kind": "measured"}

    # Arabic and some French sites write "ingredient - quantity"
    parts = re.split(r"\s+[-–:]\s+", s, maxsplit=1)
    if len(parts) == 2:
        left, right = parts
        lq = _take_qty(left)[0] is not None or _take_unit(left)[0]
        rq = _take_qty(right)[0] is not None or _take_unit(right)[0] or TO_TASTE.search(right)
        if rq and not lq:
            s = right + " " + left if not TO_TASTE.fullmatch(right.strip()) else left + " - " + right

    qty, qty_max, rest = _take_qty(s)
    unit, mult, extra, rest2 = _take_unit(rest)
    size = ""
    if not unit:                      # "1 heaping tablespoon", "2 belles tranches"
        mm = SIZE.match(rest)
        if mm:
            u = _take_unit(rest[mm.end():])
            if u[0]:
                unit, mult, extra, rest2 = u
                size = mm.group(0).strip()
    if qty is None and not unit and re.search(r"[\u0600-\u06FF]", s):
        # Arabic sites sometimes put the preparation first: "مطحون نصف ملعقة صغيرة زنجبيل"
        words = s.split()
        for i in range(1, len(words)):
            tail = " ".join(words[i:])
            q = _take_qty(tail)
            u = _take_unit(q[2] if q[0] is not None else tail)
            if q[0] is not None or (u[0] and not AR_PLURAL.match(tail)):
                qty, qty_max, rest = q
                unit, mult, extra, rest2 = u
                size = " ".join(words[:i])
                break
    if qty is None and not unit:      # جزرتين, بصلتان: an Arabic dual is a quantity of two
        mm = re.match(r"([ء-ي]{2,})[ت](?:ين|ان)(?![ء-ي])\s*", rest)
        if mm:
            qty, rest2 = 2.0, mm.group(1) + "ة " + rest[mm.end():]
            rest = rest2
    if qty is None and unit:          # a bare singular unit means one ("كوب سكر", "Pinch of salt")
        matched = rest[:len(rest) - len(rest2)].strip()
        if AR_PLURAL.search(matched) or re.search(r"[a-z]{3,}[sx]\.?$", matched, re.I):
            unit, rest2 = None, rest   # "شرائح لوز", "dashes pepper": a plural is not a quantity
        else:
            qty = 1.0
    if qty is not None:
        qty = qty * mult + extra
        if qty_max is not None:
            qty_max = qty_max * mult + extra
    if qty is not None and not unit:   # "2 ونصف بيضة"
        mm = re.match(r"و\s*(نصف|ربع)\s+", rest)
        if mm:
            qty += WORDS[mm.group(1)]
            rest2 = rest[mm.end():]
    # a parenthesised size between quantity and unit: "1 (14 oz) can tomatoes"
    if qty is not None and not unit:
        mm = re.match(r"\(([^)]*)\)\s*", rest2)
        if mm:
            u2 = _take_unit(rest2[mm.end():])
            if u2[0]:
                unit, rest2 = u2[0], u2[3]
                out["note"] = mm.group(1)
    if unit:
        rest2 = AFTER_UNIT.sub("", rest2)
        mm = re.match(r"\(([^)]*)\)\s*", rest2)    # "10 tablespoons (1 1/4 sticks) butter"
        if mm:
            out["note"] = (out["note"] + "; " if out["note"] else "") + mm.group(1)
            rest2 = rest2[mm.end():]
    rest2 = OF.sub("", rest2)
    name, note = _split_note(rest2)
    if size:
        note = (size + "; " + note).strip("; ")
    name = TO_TASTE.sub("", name).strip(" ,-–")
    note = (out["note"] + "; " + note).strip("; ") if out["note"] else note

    def fmt(x):
        return "" if x is None else (str(int(x)) if float(x).is_integer() else f"{x:.3g}")

    out.update(qty=fmt(qty), qty_max=fmt(qty_max), unit=unit or "", name=name, note=note)
    if qty is not None and unit:
        out["kind"] = "measured"
    elif qty is not None:
        out["kind"] = "count"
    elif to_taste:
        out["kind"] = "to_taste"
    elif name:
        out["kind"] = "no_quantity"
    else:
        out.update(kind="unparsed", name=raw.strip())
    return out
