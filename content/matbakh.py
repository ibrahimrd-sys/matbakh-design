#!/usr/bin/env python3
"""
Matbakh content toolchain.

    python3 matbakh.py check                    # validate every recipe
    python3 matbakh.py check recipes/x.yaml     # validate one
    python3 matbakh.py build recipes/x.yaml ar  # resolve for a locale
    python3 matbakh.py lexicon                  # audit the closed vocabulary
    python3 matbakh.py gaps                     # translation manifest

Design contract: a recipe file holds STRUCTURE, IDS, NUMBERS and the small
amount of prose that is genuinely unique to it. Repeated vocabulary lives in
lexicon/. Adding a language means translating the lexicon once, plus the prose
fields of each recipe — never the vocabulary again.
"""

import sys, os, glob, math, json, pathlib
import yaml

ROOT = pathlib.Path(__file__).parent
# Locales a recipe must cover before it can be marked published. Dialects are
# lexicon-only — per-recipe prose stays in `ar`, because dialectising 5,000
# prose strings is a second content project the size of the first.
SHIPPING_LOCALES = ["en", "ar"]


def load(p):
    with open(ROOT / p, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── VAULT RESOLUTION ────────────────────────────────────────────────────────
# The ingredient reference and the recipe catalogue are work product and live
# outside the repository. Resolution order, first hit wins:
#
#   1. --vault PATH on the command line
#   2. MATBAKH_VAULT in the environment
#   3. content/vault.path — a one-line file holding the path (gitignored)
#   4. ../../matbakh-private/03-catalogue — the default sibling layout
#
# With no vault reachable, the tracked sample is used instead and the run says
# so. That keeps the repo self-contained for anyone reviewing the schema.

def _vault():
    argv = sys.argv
    if "--vault" in argv:
        return pathlib.Path(argv[argv.index("--vault") + 1]).expanduser()
    if os.environ.get("MATBAKH_VAULT"):
        return pathlib.Path(os.environ["MATBAKH_VAULT"]).expanduser()
    cfg = ROOT / "vault.path"
    if cfg.exists():
        line = cfg.read_text(encoding="utf-8").strip().splitlines()
        if line and line[0].strip() and not line[0].startswith("#"):
            return pathlib.Path(line[0].strip()).expanduser()
    return ROOT / ".." / ".." / "matbakh-private" / "03-catalogue"


VAULT = _vault()
VAULT_OK = (VAULT / "ref" / "ingredients.yaml").exists()

ACT = load("lexicon/activities.yaml")
CHROME = load("lexicon/chrome.yaml")
if VAULT_OK:
    with open(VAULT / "ref" / "ingredients.yaml", encoding="utf-8") as f:
        ING = yaml.safe_load(f)
else:
    ING = load("ref/ingredients.sample.yaml")
STATIONS, NOTES = CHROME["stations"], CHROME["note_kinds"]
UNITS, CLASSES = CHROME["units"], CHROME["scaling_classes"]


# ---------------------------------------------------------------- validation

class Report:
    def __init__(self, name):
        self.name, self.errors, self.warnings = name, [], []
        self.note = None
        self.stub = False

    def err(self, m):
        self.errors.append(m)

    def warn(self, m):
        self.warnings.append(m)

    @property
    def ok(self):
        return not self.errors

    def show(self):
        mark = "FAIL" if self.errors else ("STUB" if self.stub else "PASS")
        print(f"\n{mark}  {self.name}")
        for e in self.errors:
            print(f"  error    {e}")
        for w in self.warnings:
            print(f"  warning  {w}")
        if self.note:
            print(f"  {self.note}")
        if self.ok and not self.warnings:
            print("  clean")


def all_recipes():
    """Every recipe reachable, keyed by id — the repo's tracked ones plus the
    vault catalogue. A parent needs this to resolve `uses:` references."""
    out = {}
    paths = sorted(glob.glob("recipes/*.yaml")) + sorted(glob.glob(str(VAULT / "recipes" / "*.yaml")))
    for f in paths:
        if "_template" in f:
            continue
        try:
            with open(f, encoding="utf-8") as fh:
                rec = yaml.safe_load(fh)
            if rec and rec.get("id"):
                out[rec["id"]] = rec
        except Exception:
            continue
    return out


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
        # `steps: []` satisfies "the key is present", so the required-field loop
        # above does not catch a scaffolded stub — it would report PASS, clean.
        # A run over the fifteen pilot stubs would then announce
        # "15 recipe(s) - 0 failing", which reads as a finished catalogue.
        # A stub is not an error (it must not block publish.sh while the pilot
        # runs) but it is not a pass either, so it gets its own state.
        if "steps" in rec:
            r.stub = True
            r.warn("steps is empty — scaffolded stub, not an authored recipe")
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

    # SUB-RECIPES.
    # A recipe may consume another. The sub-recipe is a first-class recipe,
    # authored and tested once; the parent references it by id and states how
    # much it takes. Its ingredients roll up into the parent's shopping list,
    # scaled by (amount taken / sub-recipe yield), so a parent needing 150 ml of
    # a 400 ml sauce buys 150 ml worth — not a whole batch.
    catalogue = all_recipes()
    for u in rec.get("uses") or []:
        sid = u.get("id")
        if not sid:
            r.err("uses: entry with no id")
            continue
        sub = catalogue.get(sid)
        if not sub:
            r.err(f"uses '{sid}' — no recipe with that id is reachable")
            continue
        if sid == rec.get("id"):
            r.err(f"uses '{sid}' — a recipe cannot use itself")
        if not (sub.get("yield") or {}).get("amount"):
            r.err(f"uses '{sid}' — that recipe has no yield, so the amount taken "
                  f"cannot be scaled. Add a yield to {sid}.")
        if u.get("amt") is None:
            r.err(f"uses '{sid}' — no amount. State how much of it this recipe takes.")
        if (sub.get("tags") or {}).get("course") not in ("component", "sauce", "dip", None):
            r.warn(f"uses '{sid}' — that recipe is a "
                   f"{(sub.get('tags') or {}).get('course')}, not a component. "
                   f"Check it is meant to be consumed by another recipe.")

    sv = rec.get("servings") or {}
    if "base" not in sv:
        r.err("servings.base is required — nothing can scale without it")
    y = rec.get("yield") or {}
    if y and not y.get("amount"):
        r.err("yield needs an amount")
    if y and not y.get("unit"):
        r.err("yield needs a unit")

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

                # Conversions are what let a counted or spooned amount become
                # grams, and grams are what nutrition is computed from.
                conv = ING[iid].get("convert") or {}
                if ING[iid].get("nutrition"):
                    u = ING[iid].get("unit")
                    if u == "count" and conv.get("piece_g") is None:
                        r.warn(f"{ta}: '{iid}' is counted with no weight per item, "
                               f"so it contributes nothing to computed nutrition")
                    elif u in ("tsp", "tbsp", "cup") and conv.get("cup_g") is None:
                        r.warn(f"{ta}: '{iid}' is measured in {u} with no cup weight, "
                               f"so it contributes nothing to computed nutrition")

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

    contains, flags, unknown = derive_diet(rec)
    if unknown:
        r.warn(f"no dietary tags: {len(unknown)} ingredient(s) have no diet field — "
               f"{', '.join(unknown[:5])}{' …' if len(unknown) > 5 else ''}")
    elif flags:
        claims = [k for k, v in flags.items() if v]
        r.note = (f"contains {', '.join(contains) or 'nothing flagged'}"
                  + (f" · {', '.join(claims)}" if claims else ""))

    if rec.get("status") == "published":
        gaps = [w for w in r.warnings if "translation yet" in w]
        if gaps:
            r.err(f"status:published with {len(gaps)} untranslated strings")
    return r



# ──────────────────────────────────────────────────────────── derived tags

def derive_diet(rec, _seen=None):
    """Dietary status computed from the ingredient list, never authored.

    Returns (contains, flags, unknown). If ANY ingredient lacks a `diet` field
    the flags are withheld entirely — a vegetarian claim that is wrong once
    costs a guest their dinner and the filter its credibility, so silence is the
    correct failure. `unknown` names what to fix.
    """
    contains, unknown = set(), []

    # Sub-recipes must contribute. A tahini sauce that hides its sesame would
    # make the parent's allergen list a lie, which is the one failure this
    # whole derivation exists to prevent.
    _seen = _seen or set()
    _seen.add(rec.get("id"))
    catalogue = all_recipes()
    for u in rec.get("uses") or []:
        sub = catalogue.get(u.get("id"))
        if not sub or sub.get("id") in _seen:
            continue
        sc, _, su = derive_diet(sub, _seen)
        contains.update(sc)
        unknown += su

    for step in rec.get("steps") or []:
        for tile in tiles_of(step):
            for it in items_of(tile):
                iid = it.get("id", "")
                if not iid or iid.startswith("@"):
                    continue
                ref = ING.get(iid)
                if not ref:
                    continue
                d = ref.get("diet")
                if d is None:
                    unknown.append(iid)
                else:
                    contains.update(d)

    for extra in rec.get("contains_override") or []:
        contains.add(extra)

    if unknown:
        return sorted(contains), None, sorted(set(unknown))

    flags = {
        "vegetarian": not (contains & {"meat", "poultry", "fish", "shellfish", "pork"}),
        "vegan": not (contains & {"meat", "poultry", "fish", "shellfish", "pork",
                                  "dairy", "egg", "honey"}),
        "gluten_free": "gluten" not in contains,
    }
    return sorted(contains), flags, []

# ------------------------------------------------------------------- builder

def build_items(rec, factor=1.0, scale_fixed=False):
    """Purchasable ingredients from a recipe's steps, at a given scale.

    Shared by `build` and by sub-recipe roll-up, so a parent's list is assembled
    the same way as a standalone one. Returns raw amounts; snapping to sensible
    quantities happens once, after everything is summed — snapping twice would
    round a half-batch up and then up again.
    """
    seen, out = {}, []
    for step in rec.get("steps") or []:
        for tile in tiles_of(step):
            for it in items_of(tile):
                iid = it.get("id", "")
                if not iid or iid.startswith("@") or it.get("carried") or "amt" not in it:
                    continue
                if iid in seen:
                    continue
                ref = ING.get(iid)
                if not ref:
                    continue
                seen[iid] = True
                cls = it.get("cls") or tile.get("cls") or ref.get("cls") or "continuous"
                # `fixed` means "does not scale with servings" — water for
                # boiling stays the same for two people or eight. But taking a
                # share of a sub-recipe is not a servings change: 37.5% of a
                # sauce genuinely contains 37.5% of its water. So a roll-up
                # share applies to everything, including fixed.
                amount = it["amt"] * (factor if scale_fixed else eff(cls, factor))
                out.append(dict(id=iid, item=dict(
                    id=iid, name=ref.get("name", {}), glyph=ref.get("glyph"),
                    unit=ref.get("unit"), cls=cls,
                    divisible=bool(ref.get("divisible")),
                    buy=ref.get("buy", {}), pack=ref.get("pack")),
                    raw=amount))
    return out


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
    """Resolve a per-locale string, walking `falls_back_to` from chrome.yaml.
    ar_gulf → ar_eg → ar → en, so a missing dialect word shows a comprehensible
    one rather than a blank."""
    if not isinstance(node, dict):
        return node or ""
    seen = set()
    cur = loc
    while cur and cur not in seen:
        if node.get(cur):
            return node[cur]
        seen.add(cur)
        cur = (CHROME.get("locales", {}).get(cur) or {}).get("falls_back_to")
    return node.get(fallback) or ""


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
            # Icons carry ACTIONS (philosophy §5.1) — the activity glyph wins.
            # An explicit tile glyph still overrides it, because a bespoke `verb:`
            # has no activity to draw from. The ingredient glyph is only a last
            # resort: ingredient glyphs are coarse categories (45 ingredients
            # share `jar`, 38 share `vegetable`), so drawing one in place of the
            # action loses the action and barely identifies the object.
            glyph = tile.get("glyph") or glyph or (its[0]["glyph"] if its else None)

            shown = next((k for k, i in enumerate(raw) if "amt" in i), None)
            amount = None
            if shown is not None:
                r0, i0 = raw[shown], its[shown]
                v = r0["amt"] * eff(i0["cls"], factor)
                amount = dict(value=snap(v, i0["unit"], i0.get("divisible")),
                              unit=i0["unit"], cls=i0["cls"])

            # Per-item detail. The tile's headline `amount` stays as it was; this
            # adds every item with its own scaled quantity and its own glyph, which
            # a reader needs when one action takes several ingredients at once.
            detail = []
            for k, i0 in enumerate(its):
                r0 = raw[k]
                d = dict(name=i0["name"], glyph=i0.get("glyph"),
                         carried=bool(r0.get("carried")), amount=None,
                         # The cut is a picture, not a word: `chop` says the act,
                         # the cut glyph says what this particular item should end
                         # up looking like. `cut_mm` carries the one thing a glyph
                         # cannot show — absolute size.
                         cut=r0.get("cut"), cut_mm=r0.get("cut_mm"))
                if "amt" in r0:
                    v = r0["amt"] * eff(i0["cls"], factor)
                    d["amount"] = dict(value=snap(v, i0["unit"], i0.get("divisible")),
                                       unit=i0["unit"], cls=i0["cls"])
                detail.append(d)

            tiles.append(dict(glyph=glyph, verb=verb,
                              noun=" + ".join(i["name"] for i in its) or None,
                              amount=amount, items=detail,
                              into=tile.get("into"),
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

    # Roll sub-recipe ingredients into this list, scaled by how much of it this
    # recipe actually takes. 150 ml drawn from a 400 ml sauce buys 150 ml worth.
    catalogue = all_recipes()
    for u in rec.get("uses") or []:
        sub = catalogue.get(u.get("id"))
        if not sub:
            continue
        y = (sub.get("yield") or {}).get("amount")
        if not y or u.get("amt") is None:
            continue
        share = (u["amt"] / y) * factor
        sub_built = build_items(sub, share, scale_fixed=True)
        for si in sub_built:
            prev = purchases.get(si["id"])
            if prev:
                prev["amt"] += si["raw"]
            else:
                purchases[si["id"]] = dict(item=si["item"], amt=si["raw"], via=sub["id"])

    items = []
    for iid, p in purchases.items():
        i0 = p["item"]
        v = p["amt"] * eff(i0["cls"], factor)
        items.append(dict(id=iid, name=i0["name"],
                          amount=snap(v, i0["unit"], i0.get("divisible")),
                          unit=i0["unit"], cls=i0["cls"], buy=i0["buy"],
                          pack=i0.get("pack")))

    contains, flags, _ = derive_diet(rec)
    cfg = CHROME["locales"][loc]
    return dict(
        contains=contains, **(flags or {}),
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



# ─────────────────────────────────────────────────────────────────── lexicon

def lexicon_audit():
    """The lexicon only pays for itself while it stays small and consistent.
    This surfaces the three ways it rots: two keys that mean the same thing,
    entries nothing uses, and gaps that appear when a language is added."""
    rows, errs, warns = [], [], []
    locales = list(CHROME.get("locales", {}))

    # what the catalogue actually uses
    used_acts, used_stations, used_notes, bespoke = set(), set(), set(), 0
    files = sorted(glob.glob("recipes/*.yaml")) + sorted(glob.glob(str(VAULT / "recipes" / "*.yaml")))
    files = [f for f in files if "_template" not in f]
    for f in files:
        try:
            rec = load(f) if not os.path.isabs(f) else yaml.safe_load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for step in rec.get("steps") or []:
            used_stations.add(step.get("station"))
            if step.get("note"):
                used_notes.add(step["note"].get("kind"))
            for tile in step.get("tiles") or []:
                if tile.get("do"):
                    used_acts.add(tile["do"])
                elif tile.get("verb"):
                    bespoke += 1

    print(f"\n{len(ACT)} activities · {len(CHROME['stations'])} stations · "
          f"{len(CHROME['note_kinds'])} note kinds · {len(CHROME['units'])} units")
    print(f"locales: {', '.join(locales)}")
    print(f"read from {len(files)} recipe(s)\n")

    # 1. duplicate verbs — two keys a cook cannot tell apart
    seen = {}
    for k, v in ACT.items():
        for loc in locales:
            w = (v.get("verb") or {}).get(loc)
            if not w:
                warns.append(f"activity '{k}' has no {loc} verb")
                continue
            prev = seen.get((loc, w.strip().lower()))
            if prev:
                errs.append(f"'{k}' and '{prev}' both read \"{w}\" in {loc} — "
                            f"a cook cannot tell them apart")
            else:
                seen[(loc, w.strip().lower())] = k
        if not v.get("glyph"):
            errs.append(f"activity '{k}' has no glyph, so it cannot be drawn")

    # 2. entries nothing uses — a translation bill with no return
    unused = [k for k in ACT if k not in used_acts]
    if unused:
        # With a handful of recipes loaded, "unused" means "not written yet" and
        # naming 70 of them buries everything else. Past 40 recipes it starts to
        # mean "probably does not need an icon", so the list appears then.
        if len(files) >= 40:
            for k in unused:
                warns.append(f"activity '{k}' is defined but no recipe uses it")
        else:
            print(f"  {len(unused)} activities unused so far — expected with "
                  f"{len(files)} recipe(s) loaded; listed once past 40")
    # Same reasoning for stations and note kinds: with one recipe loaded, an
    # unused oven means no recipe uses an oven yet, not that the station is wrong.
    if len(files) >= 40:
        for k in CHROME["stations"]:
            if k not in used_stations:
                warns.append(f"station '{k}' is defined but no recipe uses it")
        for k in CHROME["note_kinds"]:
            if k not in used_notes:
                warns.append(f"note kind '{k}' is defined but no recipe uses it")

    # 3. translation gaps, per locale
    for loc in locales:
        missing = [k for k, v in ACT.items() if not (v.get("verb") or {}).get(loc)]
        missing += [f"station:{k}" for k, v in CHROME["stations"].items()
                    if not (v.get("name") or {}).get(loc)]
        missing += [f"note:{k}" for k, v in CHROME["note_kinds"].items()
                    if not (v.get("label") or {}).get(loc)]
        if missing:
            verbs = [m for m in missing if not m.startswith(("station:", "note:"))]
            chrome_gaps = [m for m in missing if m.startswith(("station:", "note:"))]
            bits = []
            if verbs:
                bits.append(f"{len(verbs)} verb(s)")
            if chrome_gaps:
                # Stations and note labels appear on every screen of every
                # recipe, so a gap here costs more than any single verb.
                bits.append(f"{len(chrome_gaps)} station/note label(s) — "
                            f"these show on every screen")
            print(f"  {loc}: {' · '.join(bits)}")
            if verbs:
                print(f"       {', '.join(verbs[:8])}"
                      + (" …" if len(verbs) > 8 else ""))
        else:
            print(f"  {loc}: complete")

    print(f"\n  {len(used_acts)}/{len(ACT)} activities in use · "
          f"{bespoke} bespoke verb(s) across {len(files)} recipe(s)")
    # No ceiling warning. 81 is the reviewed count from the August 2026 merge —
    # 294 candidate verbs sorted into 81 that get an icon and 124 rendered as an
    # activity plus a qualifier. The check that matters is collisions, above:
    # two verbs reading alike is a real defect, a large vocabulary is not.

    for e in errs:
        print(f"  error    {e}")
    for w in warns:
        print(f"  warning  {w}")
    if not errs and not warns:
        print("  clean")
    return 1 if errs else 0

# ----------------------------------------------------------------------- cli

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    # The catalogue lives in the vault, outside the repository. Point at it with
    # --catalogue PATH or the MATBAKH_CATALOGUE environment variable; with
    # neither, only the demo recipe tracked in the repo is checked.
    # status goes to stderr so `build` can be piped as clean JSON
    if VAULT_OK:
        print(f"ingredients: {len(ING)} from the vault", file=sys.stderr)
    else:
        print(f"ingredients: {len(ING)} from the tracked sample — vault not found",
              file=sys.stderr)
        print(f"             looked in {VAULT}", file=sys.stderr)

    files = [f for f in sys.argv[2:] if f.endswith(".yaml")]
    if not files:
        files = sorted(glob.glob("recipes/*.yaml"))
        files += sorted(glob.glob(str(VAULT / "recipes" / "*.yaml")))
    files = [f for f in files if "_template" not in f]

    if cmd == "check":
        reps = [check(f) for f in files]
        for r in reps:
            r.show()
        bad = sum(1 for r in reps if not r.ok)
        stubs = sum(1 for r in reps if r.stub and r.ok)
        authored = len(reps) - bad - stubs
        warn = sum(len(r.warnings) for r in reps)
        parts = [f"{len(reps)} recipe(s)", f"{authored} authored"]
        if stubs:
            parts.append(f"{stubs} stub(s)")
        parts += [f"{bad} failing", f"{warn} warning(s)"]
        print("\n" + " · ".join(parts))
        sys.exit(1 if bad else 0)

    if cmd == "build":
        loc = next((a for a in sys.argv[2:] if a in CHROME["locales"]), "en")
        n = next((int(a) for a in sys.argv[2:] if a.isdigit()), None)
        print(json.dumps(build(files[0], loc, n), ensure_ascii=False, indent=2))
        return

    if cmd == "lexicon":
        sys.exit(lexicon_audit())

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
