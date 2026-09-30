# Activity attendance — the classification

**Status: CONFIRMED by Ibrahim, 30 September 2026** (`philosophy.md` §42), with
one change from the 28 September draft: **`boil` moved from unattended to
context-dependent.** Filed as `activity-attendance-draft.md` on 28 September and
renamed on confirmation. **Not yet written into
`content/lexicon/activities.yaml`.** That is E-14's work, and it waits on
Ibrahim's go, because the pilot freezes the lexicon.

It applies `philosophy.md` §34's rule: a timer is a per-activity attribute, and
only activities that can run without attendance get one.

**The test.** *Could the cook leave the pan for the whole duration without
ruining the dish or being hurt?* Yes → unattended, gets a timer. No → attended,
gets ≈ guidance and no timer. The ≈ is derived from this class, never authored
(§34).

**Checked against `activities.yaml`** on 28 September, and again with `boil`
moved: all 81 activities are classified exactly once, none missing and none
duplicated. `flip` (§35) will be class N once it is added. `cover` (§35) is
open. Neither is in the counts below.

---

## U — unattended (17): timer, and time shown

brine, chill, cool, cure, ferment, freeze, infuse, marinate, rest, set, soak,
braise, pressure_cook, simmer, steam, bake, roast.

## A — attended (14): ≈ guidance, no timer

blend, knead, whisk, blanch, deep_fry, fry, reduce, stir_fry, sweat, broil,
toast, char, grill, sear.

`deep_fry`, `broil`, `char` and `grill` are attended **for safety** and are not
overridable.

## N — no time by default (44)

add, pour, season, chop, crush, cut_wedges, dice, grate, mince, peel, shred,
slice, zest, brush, coat, drain, flatten, fold, grind, inject, layer, mash, mix,
roll, shape, sift, squeeze, strip, stuff, toss, wash, wrap, deglaze, flambe,
ladle, skim, baste, skewer, drizzle, dust, garnish, serve, sprinkle, to_taste.

## Context-dependent (6): per-page override at authoring

boil, dry, poach, stir, bain_marie, do_not_stir — `do_not_stir` inherits from
what it modifies.

**`boil` is here because the same verb covers both cases.** Pasta water can be
left alone; milk, or a starchy pot, boils over. The author sets it per page,
knowing which pot this is.

---

## Validator warnings, once E-14 is built

- A timer on an A or N verb.
- A long U activity with no timer. It is a threshold, so a short U activity
  untimed does not warn. `boil` is now context-dependent, so *bring to a boil*
  warns only if the author has marked that page unattended.

Tracked as E-14 in the PM log. Nothing is built.
