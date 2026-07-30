#!/usr/bin/env python3
"""
Matbakh content toolchain.

    python3 matbakh.py check                    # validate every recipe
    python3 matbakh.py check recipes/x.yaml     # validate one
    python3 matbakh.py build recipes/x.yaml ar  # resolve for a locale
    python3 matbakh.py gaps                     # translation manifest

Design contract: a recipe file holds STRUCTURE, IDS, NUMBERS and the small
amount of prose that is genuinely unique to it. Repeated vocabulary lives in
lexicon/. Adding a language means translating the lexicon once, plus the prose
fields of each recipe — never the vocabulary again.
"""

import sys, os, glob, math, json, pathlib
import yaml

ROOT = pathlib.Path(__file__).parent
SHIPPING_LOCALES = ["en", "ar"]


def load(p):
    with open(ROOT / p, encoding="utf-8") as f:
        return yaml.safe_load(f)


ACT = load("lexicon/activities.yaml")
CHROME = load("lexicon/chrome.yaml")
ING = load("ref/ingredients.yaml")
STATIONS, NOTES = CHROME["stations"], CHROME["note_kinds"]
UNITS, CLASSES = CHROME["units"], CHROME["scaling_classes"]


# ---------------------------------------------------------------- validation

class Report:
    def __init__(self, name):
        self.name, self.errors, self.warnings = name, [], []

    def err(self, m):
        self.errors.append(m)

    def warn(self, m):
        self.warnings.append(m)

    @property
    def ok(self):
        return not self.errors

    def show(self):
        mark = "PASS" if self.ok else "FAIL"
        print(f"\n{mark}  {self.name}")
        for e in self.errors:
            print(f"  error    {e}")
        for w in self.warnings:
            print(f"  warning  {w}")
        if self.ok and not self.warnings:
            print("  clean")


def tiles_of(step):
    return step.get("tiles") or []


def items_of(tile):
    """Normalise the single-item and multi-item tile forms into one list."""
    if "items" in tile:
        return tile["items"]
    if "item" in tile:
        it = {"id": tile["item"]}
        if "amt" in tile:
            it["amt"] = tile["amt"]
        if tile.get("carried"):
            it["carried"] = True
        return [it]
    return []


def check(path):
    r = Report(path)
    try:
        rec = load(path)
    except Exception as e:
        r.err(f"will not parse: {e}")
        return r

    for f in ("id", "source_locale", "title", "servings", "steps"):
        if f not in rec:
            r.err(f"missing required field: {f}")
    if not rec.get("steps"):
        return r

    src = rec.get("source_locale", "en")
    inter = rec.get("intermediates") or {}
    shorts = rec.get("shorts") or {}
    made, used_shorts, purchases = set(), set(), {}

    def prose(node, label):
        """Every translatable field must exist in the source locale; other
        shipping locales missing it is a warning, so you can author fast and
        translate in a later pass."""
        if not isinstance(node, dict):
            r.err(f"{label}: expected per-locale text, got a bare string")
            return
        if src not in node:
            r.err(f"{label}: missing source locale '{src}'")
        for loc in SHIPPING_LOCALES:
            if loc not in node:
                r.warn(f"{label}: no {loc} translation yet")

    prose(rec["title"], "title")
    if "why" in rec:
        prose(rec["why"], "why")

    sv = rec.get("servings") or {}
    if "base" not in sv:
        r.err("servings.base is required — nothing can scale without it")
    if "max_scale" not in sv:
        r.warn("no servings.max_scale — the reader cannot warn on batch size")
    if sv.get("presets") and sv.get("base") not in (sv.get("presets") or []):
        r.warn(f"base {sv.get('base')} is not one of the presets {sv.get('presets')}")

    for k, s in shorts.items():
        prose(s.get("title", {}), f"short '{k}' title")
        if "clip" not in s:
            r.warn(f"short '{k}' has no clip yet — will render as TO BE SHOT")

    for i, step in enumerate(rec["steps"], 1):
        at = f"step {i}"
        st = step.get("station")
        if st not in STATIONS:
            r.err(f"{at}: unknown station '{st}'")
        if "qualifier" in step:
            prose(step["qualifier"], f"{at} station qualifier")

        tl = tiles_of(step)
        if not tl:
            r.err(f"{at}: no tiles")
        if step.get("ordered") and len(tl) < 2:
            r.warn(f"{at}: ordered:true with {len(tl)} tile — ordering is meaningless")

        has_photo, has_done = "photo" in step, "doneness" in step
        if has_photo != has_done:
            missing = "doneness cue" if has_photo else "photo"
            r.warn(f"{at}: has one but not the other — no {missing}")
        if has_done:
            prose(step["doneness"], f"{at} doneness")

        if "note" in step:
            n = step["note"]
            if n.get("kind") not in NOTES:
                r.err(f"{at}: unknown note kind '{n.get('kind')}'")
            prose(n.get("text", {}), f"{at} note")

        step_classes = []
        for j, tile in enumerate(tl, 1):
            ta = f"{at} tile {j}"
            if "do" in tile:
                if tile["do"] not in ACT:
                    r.err(f"{ta}: activity '{tile['do']}' is not in the lexicon")
            elif "verb" in tile:
                prose(tile["verb"], f"{ta} verb override")
                if "glyph" not in tile:
                    r.err(f"{ta}: verb override needs an explicit glyph")
            else:
                r.err(f"{ta}: needs either 'do' (lexicon) or 'verb' (bespoke)")

            if "qualifier" in tile:
                prose(tile["qualifier"], f"{ta} qualifier")

            if "short" in tile and tile["short"] not in shorts:
                r.err(f"{ta}: short '{tile['short']}' is not defined")
            used_shorts.add(tile.get("short"))

            for it in items_of(tile):
                iid = it["id"]
                if iid.startswith("@"):
                    key = iid[1:]
                    if key not in inter:
                        r.err(f"{ta}: intermediate '{iid}' is not declared")
                    elif key not in made:
                        r.err(f"{ta}: uses '{iid}' before any step makes it")
                    continue
                if iid not in ING:
                    r.err(f"{ta}: ingredient '{iid}' is not in ref/ingredients.yaml")
                    continue

                cls = it.get("cls") or tile.get("cls") or ING[iid].get("cls")
                if not cls:
                    r.err(f"{ta}: '{iid}' has no scaling class — servings would break")
                elif cls not in CLASSES:
                    r.err(f"{ta}: '{iid}' has unknown scaling class '{cls}'")
                else:
                    step_classes.append(cls)
                if cls != "discrete" and (it.get("divisible") or ING[iid].get("divisible")):
                    r.warn(f"{ta}: '{iid}' is divisible but not discrete — no effect")

                if "amt" in it and not it.get("carried"):
                    if iid in purchases:
                        r.warn(f"{ta}: '{iid}' already bought in {purchases[iid]} — "
                               f"mark carried:true or the list double-counts")
                    else:
                        purchases[iid] = at

        if "makes" in step:
            if step["makes"] not in inter:
                r.err(f"{at}: makes '{step['makes']}' which is not declared")
            made.add(step["makes"])

        t = step.get("timer")
        if t:
            if "minutes" not in t:
                r.err(f"{at}: timer without minutes")
            prose(t.get("label", {}), f"{at} timer label")
            if t.get("mass_sensitive") and "continuous" not in step_classes:
                r.warn(f"{at}: timer is mass_sensitive but nothing here scales "
                       f"continuously — it will never change")

    for k in inter:
        if k not in made:
            r.err(f"intermediate '{k}' is declared but no step makes it")
        prose(inter[k].get("name", {}), f"intermediate '{k}' name")
    for k in shorts:
        if k not in used_shorts:
            r.warn(f"short '{k}' is defined but no tile references it")

    if rec.get("status") == "published":
        gaps = [w for w in r.warnings if "translation yet" in w]
        if gaps:
            r.err(f"status:published with {len(gaps)} untranslated strings")
    return r


# ------------------------------------------------------------------- builder

def eff(cls, factor):
    if cls == "fixed":
        return 1.0
    if cls == "seasoning":
        return math.pow(factor, 0.75)
    return factor


def snap(v, unit, divisible):
    if unit in ("g", "ml"):
        s = 1 if v < 10 else 5 if v < 100 else 10 if v < 500 else 25
        return round(v / s) * s
    if unit == "tsp":
        return round(v * 4) / 4
    if unit == "tbsp":
        return round(v * 2) / 2
    return round(v * 2) / 2 if divisible else max(1, round(v))


def t(node, loc, fallback="en"):
    if not isinstance(node, dict):
        return node or ""
    return node.get(loc) or node.get(fallback) or ""


def build(path, loc, servings=None):
    rec = load(path)
    inter = rec.get("intermediates") or {}
    shorts = rec.get("shorts") or {}
    base = rec["servings"]["base"]
    servings = servings or base
    factor = servings / base

    def resolve_item(it):
        iid = it["id"]
        if iid.startswith("@"):
            d = inter[iid[1:]]
            return dict(name=t(d.get("name"), loc), glyph=d.get("glyph"),
                        unit=d.get("unit"), cls="continuous", intermediate=True)
        d = ING[iid]
        return dict(id=iid, name=t(d.get("name"), loc), glyph=d.get("glyph"),
                    unit=it.get("unit") or d.get("unit"),
                    cls=it.get("cls") or d.get("cls"),
                    divisible=bool(d.get("divisible")),
                    buy=t(d.get("buy"), loc), pack=d.get("pack"))

    pages, arc, purchases = [], [], {}
    for step in rec["steps"]:
        sd = STATIONS[step["station"]]
        name = t(sd["name"], loc)
        if "qualifier" in step:
            name += " · " + t(step["qualifier"], loc)

        tiles = []
        for tile in tiles_of(step):
            its = [resolve_item(i) for i in items_of(tile)]
            raw = items_of(tile)

            if "do" in tile:
                a = ACT[tile["do"]]
                verb, glyph = t(a["verb"], loc), a["glyph"]
            else:
                verb, glyph = t(tile["verb"], loc), tile["glyph"]
            if "qualifier" in tile:
                verb += " " + t(tile["qualifier"], loc)
            glyph = tile.get("glyph") or (its[0]["glyph"] if its else glyph) or glyph

            shown = next((k for k, i in enumerate(raw) if "amt" in i), None)
            amount = None
            if shown is not None:
                r0, i0 = raw[shown], its[shown]
                v = r0["amt"] * eff(i0["cls"], factor)
                amount = dict(value=snap(v, i0["unit"], i0.get("divisible")),
                              unit=i0["unit"], cls=i0["cls"])

            tiles.append(dict(glyph=glyph, verb=verb,
                              noun=" + ".join(i["name"] for i in its) or None,
                              amount=amount,
                              short=shorts.get(tile.get("short")) and dict(
                                  title=t(shorts[tile["short"]]["title"], loc),
                                  secs=shorts[tile["short"]]["secs"],
                                  poster=shorts[tile["short"]].get("poster"),
                                  clip=shorts[tile["short"]].get("clip"),
                                  shot=bool(shorts[tile["short"]].get("clip")))))

            for r0, i0 in zip(raw, its):
                if i0.get("intermediate") or r0.get("carried") or "amt" not in r0:
                    continue
                purchases.setdefault(i0["id"], dict(item=i0, amt=r0["amt"]))

        page = dict(station=name, ordered=bool(step.get("ordered")),
                    heat=step.get("heat"), photo=step.get("photo"), tiles=tiles)
        if "doneness" in step:
            page["doneness"] = t(step["doneness"], loc)
        if "note" in step:
            n = step["note"]
            page["note"] = dict(kind=n["kind"], label=t(NOTES[n["kind"]]["label"], loc),
                                severity=NOTES[n["kind"]]["severity"],
                                text=t(n["text"], loc))
        if step.get("timer"):
            tm = step["timer"]
            mins = tm["minutes"] * (factor if tm.get("mass_sensitive") else 1)
            page["timer"] = dict(minutes=round(mins), label=t(tm.get("label"), loc),
                                 mass_sensitive=bool(tm.get("mass_sensitive")))
        pages.append(page)
        arc.append(dict(glyphs=[x["glyph"] for x in tiles],
                        timer=page.get("timer", {}).get("minutes")))

    items = []
    for iid, p in purchases.items():
        i0 = p["item"]
        v = p["amt"] * eff(i0["cls"], factor)
        items.append(dict(id=iid, name=i0["name"],
                          amount=snap(v, i0["unit"], i0.get("divisible")),
                          unit=i0["unit"], cls=i0["cls"], buy=i0["buy"],
                          pack=i0.get("pack")))

    cfg = CHROME["locales"][loc]
    return dict(
        id=rec["id"], locale=loc, dir=cfg["dir"], numerals=cfg["numerals"],
        title=t(rec["title"], loc), why=t(rec.get("why"), loc),
        servings=servings, base=base, presets=rec["servings"].get("presets"),
        max_scale=rec["servings"].get("max_scale"),
        over_scale=factor > (rec["servings"].get("max_scale") or 99),
        hands_on_minutes=rec.get("hands_on_minutes"),
        waits=[p["timer"]["minutes"] for p in pages if p.get("timer")],
        hero=rec.get("hero"), price_source=rec.get("price_source"),
        nutrition=rec.get("nutrition_per_serving"),
        pages=pages, arc=arc, items=items,
        shorts=[dict(key=k, title=t(s["title"], loc), secs=s["secs"],
                     poster=s.get("poster"), shot=bool(s.get("clip")))
                for k, s in shorts.items()])


# ----------------------------------------------------------------------- cli

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    # The catalogue lives in the vault, outside the repository. Point at it with
    # --catalogue PATH or the MATBAKH_CATALOGUE environment variable; with
    # neither, only the demo recipe tracked in the repo is checked.
    cat = None
    if "--catalogue" in sys.argv:
        cat = sys.argv[sys.argv.index("--catalogue") + 1]
    cat = cat or os.environ.get("MATBAKH_CATALOGUE")

    files = [f for f in sys.argv[2:] if f.endswith(".yaml")]
    if not files:
        files = sorted(glob.glob("recipes/*.yaml"))
        if cat:
            extra = sorted(glob.glob(os.path.join(cat, "*.yaml")))
            if not extra:
                print(f"note: no recipes found in {cat}")
            files += extra
    files = [f for f in files if "_template" not in f]

    if cmd == "check":
        reps = [check(f) for f in files]
        for r in reps:
            r.show()
        bad = sum(1 for r in reps if not r.ok)
        warn = sum(len(r.warnings) for r in reps)
        print(f"\n{len(reps)} recipe(s) · {bad} failing · {warn} warning(s)")
        sys.exit(1 if bad else 0)

    if cmd == "build":
        loc = next((a for a in sys.argv[2:] if a in CHROME["locales"]), "en")
        n = next((int(a) for a in sys.argv[2:] if a.isdigit()), None)
        print(json.dumps(build(files[0], loc, n), ensure_ascii=False, indent=2))
        return

    if cmd == "gaps":
        for f in files:
            g = [w for w in check(f).warnings if "translation yet" in w]
            print(f"{f}: {len(g)} untranslated string(s)")
            for x in g:
                print("   " + x)
        return

    print(__doc__)


if __name__ == "__main__":
    main()
