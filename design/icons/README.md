# design/icons

**These are placeholders, not the production set.** They were drawn on
18 August 2026 for the bolognese worked example, to `design/asset-spec.md` §1:
24 × 24 viewBox, 2px stroke, round caps and joins, `stroke="currentColor"`,
no `fill`, no width/height on the root, three strokes or fewer where possible,
nothing finer than 2px.

The production set is **Tabler Icons (MIT)**. When it lands, replace these and
add Tabler's licence text at `design/icons/LICENSE` — MIT requires it be
retained. These files are original geometry and carry no third-party licence,
so nothing is owed for them.

## What is here

**Activity glyphs** — the action, per §5.1 and the asset-spec rule *"Draw the
action, not the ingredient"*:

`chop` · `add` · `fry` · `sear` · `deglaze` · `pot` · `steam-low` · `bubbles` ·
`salt` · `strain` · `toss` · `grater`

**Ingredient-category glyphs** — the fallback, only reached when an activity has
no glyph of its own:

`onion` · `vegetable` · `meat` · `jar` · `grain` · `dairy` · `water` · `spice`

## Before commissioning the real set

Two things this example surfaced, both open in C-05:

- **Silhouettes must differ at 17px.** These were drawn to differ by overall
  shape — diagonal blade, horizontal slab, tall vessel, cross, bowl — because
  the arc strip is the binding constraint. Squint at the arc in the bolognese
  prototype: if two adjacent pages read alike, the cook loses their place.
- **Four activity pairs still share one glyph** in `activities.yaml`:
  `chop`/`mince`, `baste`/`brush`, `season`/`to_taste`, and — until it was fixed
  — `cut_wedges`/`zest`. A shared glyph is fine only where the two never co-occur
  in one recipe. `season` and `to_taste` co-occur in molokhia.
