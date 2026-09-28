# Activity attendance — DRAFT classification

**Status: DRAFT, 28 September 2026. Not a decision.** It is not written into
`content/lexicon/activities.yaml` until Ibrahim confirms it. Filed with
`philosophy.md` §34, which decides the rule this draft applies: a timer is a
per-activity attribute, and only activities that can run without attendance
get one.

**The test.** *Could the cook leave the pan for the whole duration without
ruining the dish or being hurt?* Yes → unattended, gets a timer. No → attended,
gets ≈ guidance and no timer. The ≈ is derived from this class, never authored
(§34).

**Checked against `activities.yaml` on 28 September 2026:** all 81 activities
are classified exactly once. No verb below is missing from the lexicon, none is
duplicated, and none of the 81 is left out. `flip` (§35, class N once added)
and `cover` (§35, open) are not in the lexicon and not in the counts below.

---

## U — unattended (18): timer, and time shown

brine, chill, cool, cure, ferment, freeze, infuse, marinate, rest, set, soak,
boil, braise, pressure_cook, simmer, steam, bake, roast.

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

## Context-dependent (5): per-page override at authoring

dry, poach, stir, bain_marie, do_not_stir — `do_not_stir` inherits from what it
modifies.

---

## Validator warnings, once confirmed

- A timer on an A or N verb.
- A long U activity with no timer — a threshold, so *bring to a boil* untimed
  does not warn.

Tracked as engineering scope in the PM log (WS4). Nothing is built.
