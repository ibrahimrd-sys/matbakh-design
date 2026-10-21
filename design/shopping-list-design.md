# The app's shopping list — one list for imports and Matbakh's recipes

*Written 21 October 2026 by Claude, opening import step 7 (vault
`02-strategy/import-test-plan-2026-10-12.md` §4): "it depends on the app's own
shopping list, which import shares with the catalogue's recipes."*

> **Proposed — not approved.** Nothing here is built. The rules already decided
> are cited to where they were decided; everything else is marked *proposed*, and
> §9 lists the decisions this needs from Ibrahim.

**Last updated:** 2026-10-21

---

## 1. What it is

The Flutter app (`~/Develop/matbakh`) has three screens on sample recipes and no
ingredients. Step 7 needs a shopping list on the phone that two things feed:

| | **A Matbakh recipe** | **An import** |
|---|---|---|
| Lines | Authored: reference id, amount, class | Published text, parsed and matched on the phone |
| Scaling | Class curve and rounding ladder (`philosophy.md` §6.2–6.3) | Linear (step 6 review; not formally decided) |
| Unmatched lines | None — the validator refuses them | Kept as text, never dropped (D-19) |
| Source | `matbakh.py build` output | `recipe_core` moved into Dart |

**Proposed: one list, built from *contributions*.** Each time a recipe or an
import is added, it adds one contribution — its lines, already scaled by its own
rules, with the servings chosen. The list is the sum of its contributions, worked
out each time it is shown. So a recipe can be taken off again as a whole, the two
scaling systems never mix (each does its own scaling before the list sees it),
and "merge with the cook's list" (left for step 7) is simply adding a
contribution.

## 2. The rules it keeps — already decided

1. **Three numbers** (§6.7): exact → displayed → **purchase**, and the purchase
   number, rounded up to the pack, exists only on the list. Cost uses the exact
   amount, never the pack.
2. **Stock in ml, bought in cubes** (§47): *stock cubes ×2 (for 1 L)*, never grams
   of powder.
3. **Carried items are bought once** (§11) and **intermediates (`@stock`) never
   reach the list** (authoring standard).
4. **Sub-recipes roll up** by ingredient id, scaled by `amt ÷ yield` (§14).
5. **Nothing is dropped** (D-19): a line Matbakh does not recognise goes under
   *غير مصنف / Other* as its own words.
6. **Add only what agrees** (`RecipeCoreDesign.md`): mass with mass, volume with
   volume, count with count; otherwise the item shows both, never a guessed sum.
   A range stays a range; *a pinch* and *as needed* have no amount.
7. **Three groups, staples apart and unticked, the source line under every item**
   (step 6 fix 2, accepted 21 October).
8. **Unit words in the recipe's language** (step 6 fix 3).
9. **A substitute changes the list for that session only** (§43.4).
10. **On the device only** until the permit (R-16, proposed): the list stays on
    the phone, with no account and no sync.

## 3. The data — proposed

```
ShoppingList
  contributions: [Contribution]
  edits: { itemKey → Edit }            # the cook's own changes, kept apart

Contribution
  id, kind (recipe | import | manual), title, servings, addedAt, lang
  lines: [Line]

Line
  ingredientId?                         # null when not recognised
  text                                  # the source line as published/authored
  amount?  { lo, hi?, unit }            # exact, after this source's own scaling
  unclear: bool                         # recognised, no usable amount

Edit
  ticked?, haveIt?, amountOverride?, removed?
```

What is worked out, never stored: the **item** (contributions summed per
ingredient id and dimension), its **group**, its **purchase** (pack or cube
count) and its **displayed** amount (the rounding ladder).

**Why exact amounts and ingredient ids are kept** (and not just the rounded text):
the retail roadmap's later phases re-match list items to a retailer's products
and price them (`matbakh-roadmap-to-retail-commerce.md`, reference only). Keeping
the id and the exact amount now costs nothing and keeps that possible.

**Proposed: stored as one JSON file on the phone** (`path_provider`). A list holds
tens of items; a database would be weight with no benefit until there is sync.

## 4. Groups and order

The step 6 groups, in this order:

1. **To buy** — recognised, with an amount; a pack or cube count where the
   reference has one (*Rice — 1 kg bag*).
2. **Amount unclear** — recognised, no usable amount; unticked, with *set amount*.
3. **Other — غير مصنف** — not recognised; ticked, as the source's words.
4. **Staples you probably have** — set apart, unticked.

**The contradiction this settles (proposed):** the mock-up says staples *arrive
unticked* on the list; the prototype prints them as *not added*. The accepted
step 6 wording is *set apart and unticked*, so **staples are on the list,
unticked** — one tap to buy them, nothing hidden. Ticking one is remembered
(*عندي* the other way: unticking a bought item).

**Which items are staples — needs a decision (§9).** Today the prototype knows
only salt and water. §16.1 names salt, oil, onion, garlic, flour, sugar — but for
discovery, where *assumed present* is harmless; on a list, an onion set apart may
be an onion not bought. **Proposed:** a `staple: true` field in the reference,
starting with salt, black pepper, water, ice, oil (the cooking oils), sugar and
flour; onion and garlic stay to buy.

**Order within a group — needs a decision (§9).** The aisle-ordered list is
accepted (MB-01, feature #29), but the reference has **no aisle field**; the
nearest is the `buy` hint (*pantry staple* 145, *from jar* 95, *loose* 80, *from
the chiller* 52, *from the butcher* 40, *baking aisle* 29, *dry goods* 25, *from
the freezer* 16). **Proposed:** an `aisle` field with a short fixed set —
produce, butcher, chiller, freezer, bakery, dry goods, jars and tins, spices,
drinks — filled in a data pass from the `buy` hints, reviewed in the ingredient
editor. Until it exists, recipe order.

## 5. Purchase rounding

**Proposed: the list rounds, nothing upstream does.** Today it is split: the
prototype rounds to packs only for gram entries (so buttermilk's litre and a
tortilla pack of 10 are ignored), and `matbakh.py build` counts cubes but passes
`pack` through uncounted. On the phone one function does it for every unit:
`ceil(amount ÷ pack)` packs, or cubes from `makes`. A range buys for its top.

The displayed amount uses the rounding ladder (§6.3) for both sources, so an
import's *237 g* reads *240 g* on the list while its source line underneath still
says *1 cup*. **Needs a decision (§9)**: imports have so far printed amounts
unrounded.

## 6. What comes to the phone

- **The reference:** `ingredients.yaml` (554 entries, 176 KB) exported to JSON by a
  script in `tools/` and bundled as an asset. The phone never edits it.
- **The list code:** `basket.py`'s summing and rounding, rewritten in Dart, with
  **parity tests**: the Python and the Dart run the same saved pages and must give
  the same list. Step 5's cases are the test set.
- **Matbakh recipes:** `matbakh.py build`'s `items` for the pilot recipe
  (molokhia bil farakh), bundled as JSON, so a catalogue recipe can be added
  before there is a backend. The dummy recipes stay as they are.
- **Later in step 7, not in this part:** the parser and matcher in Dart, the
  servings screen, *share to Matbakh*, pasted text, the 10-a-month count.

## 7. Two faults found on the way

Both in `content/matbakh.py build`, the catalogue side. Neither shows today; both
would reach the phone's list.

1. **Sub-recipe amounts are scaled twice.** A roll-up's share already includes the
   servings factor (`share = (amt / yield) * factor`), and the final loop
   multiplies every item by `eff(cls, factor)` again. Invisible at the base
   servings (factor 1) and while no recipe has `uses:` — only `_template.yaml`
   does. At 8 servings of a 4-serving recipe, a sub-recipe's ingredients would be
   bought four times over instead of twice.
2. **A repeated use of the same ingredient keeps the first amount.** `build_items`
   skips an id already seen, and `build` uses `setdefault`; the validator warns
   when an item is bought twice, so authoring catches it, but the list should add
   them, as `basket.py` does.

**Proposed:** fix both, with a test each, before the phone takes catalogue lists.

## 8. The order of work

1. The reference exported to JSON; the Dart model; reading and writing the list.
2. The list engine in Dart, with parity tests against `basket.py`.
3. The list screen: four groups, ticks, source lines, *set amount*, remove a
   recipe.
4. *Add to list* from the pilot recipe.
5. Then step 7's import parts, on this list.

## 9. Decisions this needs from Ibrahim

1. **Approve the shape** — one list of contributions; the list is worked out, the
   cook's edits kept apart; stored on the phone as JSON.
2. **Staples** — on the list, unticked; which entries are staples (the proposed
   set above, or §16.1's, or another).
3. **Aisle order** — add an `aisle` field and the data pass now, or recipe order
   for the first build.
4. **Rounding imports** — the ladder on an import's displayed amounts, or exact as
   published.
5. **The two `matbakh.py` faults** — fix now, before the phone.
6. **Free or premium** — the list itself has no tier yet; cost on it is premium
   (§40). **Proposed:** the list is free.
