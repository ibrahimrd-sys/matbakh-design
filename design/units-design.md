# Units: three authored, metric and kitchen shown

*Written 21 October 2026 by Claude, at Ibrahim's request: show quantities in metric
and kitchen units together. He chose (option "2a") to keep `philosophy.md` §30 as
written — three unit values authored per ingredient, no computed conversion — and to
show the pair on the shopping list and the import check sheet only.*

> **Approved by Ibrahim, 21 October 2026, all six decisions in §7 as proposed**
> (`philosophy.md`, addendum to §30 of 21 Oct). The text below is kept as proposed.

**Last updated:** 2026-10-22

---

## 1. What is decided already

- **Three values per ingredient, authored, none derived** (§30, 20 Sept): imperial
  (oz, lb, fl oz), metric (g, ml), kitchen (cup, spoon, and — proposed below — piece).
- **The cook chooses two, in settings; no toggle mid-recipe** (§30).
- **Default pair: metric and kitchen** (Ibrahim, 21 Oct).
- **Where:** the shopping list and the import check sheet (Ibrahim, 21 Oct). The
  imported recipe's own lines stay as published (§44); Matbakh's recipe pages are not
  touched by this.

## 2. What "three authored values" means — proposed

One **equivalence** per ingredient, entered by a person: *this much in metric is this
much in kitchen measure is this much in imperial, for this ingredient.*

```yaml
red_lentils:
  …
  units: { metric: 190 g, kitchen: 1 cup, imperial: 6.7 oz }
onion:
  units: { metric: 110 g, kitchen: 1 piece, imperial: 3.9 oz }
salt:
  units: { metric: 6 g, kitchen: 1 tsp, imperial: 0.2 oz }
```

A line in one of the three is shown in the cook's two by **scaling that authored
equivalence** — 2 cups of red lentils is 2 × 190 g. That is the one arithmetic step
§30 cannot avoid; what it forbids, and what this does not do, is deriving the
equivalence itself from a generic table (a cup of anything = 240 ml = N g).

**The overlap with §11's `convert`** (`cup_g`, `piece_g`): the same fact, recorded
twice, would be two numbers that can disagree — the thing §11 was written to prevent.
**Proposed:** `units` becomes the one record; where an entry has both, the validator
refuses a disagreement; and `convert` is retired entry by entry as `units` is filled
(the estimate reads `units` first, then `convert`).

## 3. Showing it — proposed

- **Every item on the list and the check sheet shows the cook's pair, metric first:**
  *370 g · 2 cups*, *220 g · 2 onions*. The recipe's own unit is one of the two where it
  can be; a line in imperial shows metric and kitchen.
- **Rounded by §6.3's ladder**, kitchen measures to ¼ cup, ½ tbsp, ¼ tsp; **≈ where
  rounding moves it more than 5%**, as now.
- **An ingredient with no `units` shows its one amount, as today** — and with the
  testing switch on, says *no units authored*, so gaps are seen.
- **Blanks:** a unit with no sensible value (imperial for a pinch; kitchen for a whole
  chicken) is left out of the record, and that item shows the units it has.
- **Units outside the three** (*1 can*, *1 bunch*) are shown as published.
- **The prototype and the app together:** `basket.py` gains the same display, so the
  parity tests keep holding the two identical.

## 4. Liquids — proposed

For an ingredient measured in ml, kitchen to metric is a volume and does not depend on
the ingredient — only on what size *cup* Matbakh means. **Proposed:** one stated rule,
authored once — *a Matbakh cup is 240 ml, a tablespoon 15 ml, a teaspoon 5 ml* —
instead of the same 240 typed into 82 entries. It is still an authored value, not a
generic conversion; it is the definition of the kitchen unit.

## 5. Settings

The cook's choice of two of the three needs a settings screen the app does not have
yet. **Proposed:** metric + kitchen fixed for now; the setting comes with the settings
screen.

## 6. Authoring — the cost

Today **409 of 555** entries have neither a cup nor a piece weight; 146 have one or
both (Claude's first-pass values, not yet reviewed — hanging decision 6, 20–21 Oct).

**Proposed:** a review workbook in the format Ibrahim has used, one row per entry,
**ranked by how often the entry is used** (samples 4–6 and the pilot recipes), with
Claude's *suggested* triple from standard kitchen references in its own column, marked
as a suggestion. Ibrahim accepts, corrects or blanks each value; **only his answers
enter `units`.** First round: the 150 most-used entries; the rest show one unit until
done.

### What actually happened — 22 October 2026

The ranked workbook (`04-research/units-review-2026-10-21.xlsx`) is still out. The
authoring arrived by another route instead: **Ibrahim's own cup-to-gram table**, 69
ingredients, filed at `03-catalogue/ref/conversion-to-weight.xlsx`. The rule above is
unchanged and was met — only his answers entered. **37 entries now carry `units`**; four
counted things took the cup weight into `convert` and keep `units` free for their piece
equivalence; fifteen ml-measured entries were left to §4's stated rule. Three rows
(coriander ground, allspice, baking soda) differ from the stored guess by 50% or more and
are **held back** as likely doubled or halved rows, and nine have no entry or need a
mapping call. The ranked workbook still covers the rest, and the counts in §6 above are
from 21 October.

**One thing §2 did not foresee:** `shop()` reads `convert.cup_g` alone to decide that
something sold by weight is listed in grams, so the retirement it prescribes breaks the
list display for every entry that completes it (`recipe_core/basket.py:395`, and the app's
`lib/shopping/compute.dart:125`). Open, with one case failing.

## 7. Decisions this needs from Ibrahim

1. **The shape:** one authored equivalence per ingredient, scaled for a line's amount
   (§2).
2. **`convert`:** retired into `units`, one record, the validator refusing a
   disagreement in between (§2).
3. **Kitchen measure includes *piece*** for counted things (onions, eggs) (§2).
4. **Liquids:** one stated rule for the cup and spoons, not 82 typed values (§4).
5. **Settings:** metric + kitchen fixed until the settings screen (§5).
6. **Authoring:** the ranked workbook with Claude's suggestions marked, only his
   answers entering the reference; first round 150 entries (§6).
