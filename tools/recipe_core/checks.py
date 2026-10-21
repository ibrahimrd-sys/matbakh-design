"""The capture pre-filter's checks (CaptureDraftRunReadme.md §7): structural flags on a
capture-draft, for a chef reviewing it. **Flags only** — nothing is corrected, scored,
merged, converted or hidden, and nothing decides whether a chef sees the draft.

Built: A completeness · D unmapped ingredients · E source carryforward · F duplicate
entries · G temperatures · H list against method. Not built: B (needs a chef's
thresholds), C (needs a larger catalogue). Two ingredients are "the same" when they
match the same reference entry (check D's mapping) — or, unmatched, the same name.
"""

import json, re

from . import basket
from .match import words

UNREADABLE = re.compile(r"[½⅓⅔¼¾⅛⅜⅝⅞]\d|\d[½⅓⅔¼¾⅛⅜⅝⅞]\d|\bhalf\s+\d")
QSTART = re.compile(r"(?:(?<=[\s(])|^)(?:\d|[½⅓⅔¼¾⅛⅜⅝⅞]|half\b|a\s+(?:pinch|handful|dash)\b)", re.I)
TEMP = re.compile(r"(\d{2,3})\s*(°|º|degrees?|درجة)\s*(?:(?:C|Celsius|centigrade|مئوية)\b|(F|Fahrenheit|فهرنهايت))?", re.I)
TEMP_BARE_F = re.compile(r"\b(\d{2,3})\s*F\b")


# ── reading a draft: capture-draft's JSON, or its --format text ─────────────

def load(path):
    raw = open(path, encoding="utf-8").read()
    if raw.lstrip().startswith("{"):
        doc = json.loads(raw)
        r, d = doc["recipe"], doc.get("_draft", {})
        ings = [i.get("original_line") or " ".join(x for x in (i["quantity"], i["unit"], i["name"]) if x)
                + (", " + i["note"] if i.get("note") else "") for i in r["ingredients"]]
        return dict(title=r["title"], servings=r["servings_as_given"], ingredients=ings, steps=r["steps"],
                    notes=r["extraction_notes"], source=d.get("source", ""),
                    page_recipe_data=d.get("page_recipe_data"), redirected_to=d.get("redirected_to"),
                    found=r.get("found_recipe", True))
    out = dict(title="", servings="", ingredients=[], steps=[], notes=[], source="",
               page_recipe_data=None, redirected_to=None, found=True)
    section = None
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("# source:"):
            out["source"] = s.split(":", 1)[1].strip()
        elif s.startswith("TITLE:"):
            out["title"] = s.split(":", 1)[1].strip()
        elif s.startswith("SERVINGS"):
            out["servings"] = s.split(":", 1)[1].strip()
        elif s == "NO RECIPE FOUND":
            out["found"] = False
        elif s in ("INGREDIENTS", "STEPS", "NOTES FOR THE CHEF"):
            section = s
        elif section == "INGREDIENTS" and s.startswith("- "):
            out["ingredients"].append(s[2:])
        elif section == "STEPS" and re.match(r"\d+\.\s", s):
            out["steps"].append(re.sub(r"^\d+\.\s*", "", s))
        elif section == "NOTES FOR THE CHEF" and s.startswith("- "):
            out["notes"].append(s[2:])
    return out


# ── the checks ─────────────────────────────────────────────────────────────

def _amount(p):
    q = basket._fmt(p["q"]) + ("–" + basket._fmt(p["q_max"]) if p["q_max"] else "")
    return (q + " " + p["unit"]).strip()


def _total(ps):
    """'1 tbsp + 2 tbsp = 3 tbsp' — or the entries alone when they cannot be added."""
    parts = " + ".join(_amount(p) if p["q"] is not None else "(no quantity)" for p in ps)
    if any(p["q"] is None for p in ps):
        return parts + " — no total: an entry has no quantity"
    units = {p["unit"] for p in ps}
    if len(units) == 1:
        lo = sum(p["q"] for p in ps); hi = sum(p["q_max"] or p["q"] for p in ps)
        u = units.pop()
        return f"{parts} = {basket._fmt(lo)}{'–' + basket._fmt(hi) if hi != lo else ''} {u}".rstrip()
    dims = {basket._dim(u) for u in units}
    if len(dims) == 1 and dims <= {"mass", "volume"}:
        d = dims.pop()
        lo = sum(basket._base(p["q"], p["unit"]) for p in ps)
        hi = sum(basket._base(p["q_max"] or p["q"], p["unit"]) for p in ps)
        return f"{parts} = {basket._show(lo, hi, d)}"
    return parts + " — no total: the units cannot be added"


def _key(p):
    return p["id"] or ("~" + p["name"].lower().strip())


def run(draft, matcher, ref, parse):
    L = basket.read(draft["ingredients"], matcher, ref, parse)
    flags = {}

    # A — completeness
    a = []
    if not draft["found"]:
        a.append("the capture found no recipe")
    if not draft["ingredients"]:
        a.append("no ingredients")
    if not draft["steps"]:
        a.append("no steps")
    noq = [p["line"] for p in L if p["q"] is None]
    if noq:
        a.append(f"{len(noq)} of {len(L)} ingredients have no quantity in the source: " + "; ".join(noq))
    short = [f"step {i}" for i, s in enumerate(draft["steps"], 1) if len(s.split()) < 3]
    if short:
        a.append("steps with almost no text: " + ", ".join(short))
    if not str(draft["servings"]).strip():
        a.append("no servings given")
    flags["A"] = a

    # D — unmapped ingredients
    flags["D"] = [f"not in the reference: {p['name'] or p['line']}" for p in L if not p["id"]]

    # E — where the draft came from
    src, e = draft["source"], []
    if re.match(r"https?://", src):
        e.append(f"a web page: {src}")
        if draft["page_recipe_data"] is True:
            e.append("the page publishes schema.org recipe data")
        elif draft["page_recipe_data"] is False:
            e.append("the page publishes NO recipe data — the draft rests on the page's visible text")
        else:
            e.append("whether the page had recipe data was not recorded")
        if draft["redirected_to"]:
            e.append(f"the page redirected to {draft['redirected_to']}")
    elif src:
        e.append(f"an image: {src} — read from a photograph or screenshot")
    flags["E"] = e

    # F — the same ingredient listed more than once
    groups = {}
    for p in L:
        groups.setdefault(_key(p), []).append(p)
    flags["F"] = [f"{(ps[0]['matched_on'] or ps[0]['name'])} — {_total(ps)}"
                  for ps in groups.values() if len(ps) > 1]

    # G — temperatures with no unit, or not in °C
    g = []
    for i, s in enumerate(draft["steps"], 1):
        for m in TEMP.finditer(s):
            whole = m.group(0)
            if m.group(3):
                g.append(f"step {i}: {whole.strip()} is not °C")
            elif not re.search(r"C\b|Celsius|centigrade|مئوية", whole, re.I):
                g.append(f"step {i}: {whole.strip()} has no unit")
        for m in TEMP_BARE_F.finditer(s):
            if not TEMP.search(s[max(0, m.start() - 2):m.end()]):
                g.append(f"step {i}: {m.group(0)} is not °C")
    flags["G"] = g

    # H — what the method uses against what the list gives
    in_list = {k for k in groups}
    used, unread = {}, []
    for i, s in enumerate(draft["steps"], 1):
        for m in UNREADABLE.finditer(s):
            unread.append(f"step {i}: “{s[max(0, m.start() - 10):m.end() + 14].strip()}” — a quantity that cannot be read")
        for m in QSTART.finditer(s):
            phrase = re.split(r"[,.;:()]| and | or ", s[m.start():])[0]
            phrase = " ".join(phrase.split()[:7])
            p = parse(phrase)
            if p["kind"] not in ("measured", "count") or not p["name"]:
                continue
            iid, on = matcher.match(p["name"])
            # the ingredient must be what the quantity counts: "10 minutes for the breadcrumbs" is not 10 breadcrumbs
            if iid and not set(words(p["name"])[:2]) & set(words(on.lstrip("="))):
                continue
            p.update(line=phrase, id=iid, matched_on=on, q=basket._f(p["qty"]), q_max=basket._f(p["qty_max"]))
            if _key(p) in in_list and (p["unit"] or basket._dim(p["unit"]) == "count"):
                used.setdefault(_key(p), []).append((i, p))
    h = []
    for k, uses in used.items():
        listed = groups[k]
        if any(p["q"] is None for p in listed) or any(p["q"] is None for _, p in uses):
            continue
        def tot(ps):
            dims = {basket._dim(p["unit"]) for p in ps}
            if len(dims) != 1 or dims == {"other"}:
                units = {p["unit"] for p in ps}
                if len(units) != 1:
                    return None
            return (sum(basket._base(p["q"], p["unit"]) for p in ps),
                    sum(basket._base(p["q_max"] or p["q"], p["unit"]) for p in ps))
        lt, ut = tot(listed), tot([p for _, p in uses])
        if not lt or not ut:
            continue
        name = listed[0]["matched_on"] or listed[0]["name"]
        steps = " + ".join(f"{_amount(p)} (step {i})" for i, p in uses)
        given = " + ".join(_amount(p) for p in listed)
        if ut[1] > lt[1] + 1e-6:
            h.append(f"{name} — the steps use more than the list: list {given}; steps {steps}")
        elif ut[0] < lt[0] - 1e-6:
            h.append(f"{name} — the steps account for less than the list (the rest may be used unmeasured): list {given}; steps {steps}")
    flags["H"] = h + unread
    return flags


def as_text(draft, flags):
    names = {"A": "Completeness", "D": "Unmapped ingredients", "E": "Source",
             "F": "Duplicate ingredient entries", "G": "Temperature units", "H": "List against method"}
    out = [f"PRE-FILTER — {draft['title'] or '(untitled)'}",
           "Flags only: nothing corrected, scored or hidden. The chef reviews every draft.", ""]
    for c in "ADEFGH":
        out.append(f"{c}. {names[c]}" + ("" if flags[c] else " — nothing to flag"))
        out += [f"  - {f}" for f in flags[c]]
    out += ["", "B (plausibility) and C (duplicates against the catalogue) are not built yet."]
    return "\n".join(out) + "\n"
