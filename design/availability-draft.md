# Ingredient availability — DRAFT, not settled

> Drafted for review. Nothing here carries SETTLED. Positions are proposed with
> their reasoning attached. Forks are marked **FORK** rather than resolved.
>
> Prompted by the decision to cover the world's main cuisines. No existing
> section addresses this: philosophy §11 specifies what an ingredient *is*, philosophy §10 establishes
> that pricing is locale-bound, and nothing states what happens when a specified
> ingredient cannot be bought in the locale the cook is standing in.

> **Cross-reference convention.** A bare `§n` refers to a section of *this*
> document. References to another file name it — `philosophy §9`,
> `discovery-draft §2.4`. Adopted 2 August 2026 after an audit found 50 of 108
> references across the three drafts ambiguous: every document numbers from 1,
> so its section numbers collide with `philosophy.md`'s.


---

## 1. The problem

An ingredient can be fully specified in `content/ref/ingredients.yaml` — `cls`,
`unit`, `pack`, `buy`, `nutrition`, `convert`, `diet` all present and correct —
and still be unobtainable in Cairo. Gochujang, dashi, galangal, crème fraîche,
fresh curry leaf. The library says what the thing is; nothing says whether the
cook can get it.

Three things break at once:

1. **`cost_per_serving` cannot compute.** philosophy §11 states prices come from the market
   feed keyed on the id. No feed entry, no price, no per-serving figure — and
   cost is the pillar philosophy §2 assigns to the return visit.
2. **The shopping list contains a line nobody can fill.** philosophy §13's consolidated
   list and its "125 a head" claim both silently degrade.
3. **Discovery would offer a dish the cook cannot cook.** The shelf's promise
   (philosophy §9 — someone chose this, and here is why) is worth nothing if the answer to
   *why this one* is followed by *and you can't make it.*

---

## 2. Two axes, not one

The trap is treating this as a single availability flag. **Obtainable and
priceable are different facts and they come apart in the common case.**

| | Priceable | Not priceable |
|---|---|---|
| **Obtainable** | Staples in the tracked feed | Imported item at a specialty grocer |
| **Not obtainable** | — | Genuinely absent from the market |

The top-right cell is where most world-cuisine ingredients sit in Cairo, and it
is the cell that decides whether this is a small problem or a large one. Conflate
the axes and every specialty ingredient reads as unavailable, which would
truncate the global collection far more aggressively than reality warrants.

---

## 3. `stock` — a per-locale map, not a field on the ingredient

Availability is a fact about an (ingredient, locale) pair, not about an
ingredient. It therefore lives where price lives: alongside the market feed,
keyed on the ingredient id — **not** in `ingredients.yaml`, which stays
locale-neutral.

Proposed states:

| State | Meaning | Cost behaviour |
|---|---|---|
| `staple` | Ordinary retail, in the tracked feed | Priced |
| `specialty` | Obtainable, but not in the tracked feed | Unpriced, cookable |
| `absent` | Not obtainable in this locale | Unpriced, not cookable |
| *unset* | No information | Treated as `absent` for claims, reported as unknown |

**Unset is not `absent`,** on the philosophy §11 `diet` precedent: unknown and known-empty
are different, and collapsing them lets the library lie by omission. The
difference is that `absent` is an editorial statement and *unset* is an
admission — and the two must be distinguishable in a coverage report, or nobody
will ever know how much of the map is actually filled.

`specialty` may optionally carry a `where` string — the bilingual equivalent of
`buy` for a shopper who has to go somewhere unusual. This is the one piece of
per-locale prose in the model and it should stay short and reusable.

---

## 4. Cost when a line cannot be priced

This is the sharpest question, and the answer should **not** simply borrow philosophy §11's
diet rule.

philosophy §11 withholds dietary tags entirely when any ingredient's `diet` is unset,
because a dietary claim is binary and safety-critical — *a vegetarian claim
wrong once costs a guest their dinner*. Cost is neither. It is continuous, and a
stated floor is not a wrong claim.

**Proposed rule, using `cls` to decide:**

- **Unpriced ingredient is `seasoning` or `fixed`** → show a floor:
  `from EGP 84 — excludes 1 item`. A pinch of sumac cannot move a per-serving
  figure enough to mislead, and discarding an otherwise complete cost because of
  it destroys the pillar to protect a rounding error.
- **Unpriced ingredient is `continuous` or `discrete`** → **withhold the cost
  entirely.** These are proteins and main vegetables. An unpriced one can be the
  majority of the dish's cost, and a floor that omits it is not a floor, it is a
  misleading number wearing a qualifier.

This satisfies philosophy §3 — never present a computed estimate as a fact — because the
floor names its own incompleteness, and the withheld case admits it outright. It
uses only `cls`, which already exists and is already authored on every
ingredient.

**Consequence for philosophy §13.** The party plan's "125 a head" is the same rule at menu
scale. One `specialty` spice across twelve covers yields *from 125 a head*. One
unpriced protein withholds the figure — correctly, because the number is the
entire claim and a wrong one is worse than none.

---

## 5. Substitution is a note, never a mechanism

The obvious move is per-locale substitution: no crème fraîche in Cairo, so serve
labneh. **Rejected**, for three reasons drawn from settled sections.

- **philosophy §6.1.** The base recipe is the one that was cooked and tested; every
  derivation is stated as such. An auto-substituted recipe is a derivation the
  kitchen never saw, presented as the tested original. That is precisely the
  claim philosophy §6.1 exists to protect.
- **philosophy §9.** One recipe per dish. A substitution creates a second version, and the
  document has no place to put it.
- **Cost.** Substitution is editorial judgement per pair, per locale, per
  recipe. It is the most expensive thing proposed in any draft so far and it
  scales multiplicatively with the world-cuisine decision.

**Proposed instead:** a substitution is authored on the recipe line as a `note`
(philosophy §11 already has `note {kind, text}`), written once by the recipe's author, shown
where the ingredient appears, and **never applied automatically.** The cook
substitutes; the app informs. Cost is computed from what was authored, not from
what the cook might swap in — otherwise the number stops corresponding to
anything tested.

A `note` of kind `substitute` on an ingredient that is `specialty` or `absent` is
also the natural signal for editorial coverage: it is exactly the list of places
the library is straining against a locale.

---

## 6. The real control is publication, not display

The dangerous failure is not a badly rendered card. It is authoring three
thousand world recipes and discovering that a third of them are uncookable in
the only market with a price feed.

**Proposed: availability gates `status` per locale.** A recipe does not reach
published-in-Cairo while any ingredient is `absent` or unset there. It may be
published with `specialty` ingredients — that is the whole point of separating
the axes in §2.

This makes availability an authoring-time report rather than a runtime surprise:
*this recipe is publishable in 3 of 5 locales; blocked in 2 by galangal.* Cheap
to run, and it turns an invisible library problem into a queue.

It also gives the editorial function a concrete instrument: the list of
ingredients blocking the most recipes is the shopping list for whoever is
extending the market feed.

---

## 7. Discovery consequence

Two positions, and this is a **FORK**.

**Hide unavailable dishes.** Clean, but the shelf shrinks silently — which the
discovery draft (discovery-draft §9) already argues against on honesty grounds.

**Show them, marked, and make obtainability a constraint axis.** Consistent with
discovery's subtraction model: *only things I can buy at the supermarket* is a
real constraint a cook holds, and belongs in the same vocabulary as spice level
and effort. `staple`-only becomes a filter; `specialty` dishes remain visible
and honest about what they demand.

I favour the second. Given §6 already prevents `absent` recipes from publishing,
the visible cases are `specialty` — a dish worth cooking that needs a trip to a
particular shop, which is a fair thing to put in front of a cook rather than a
failure to hide. Whether the filter defaults on or off is unresolved.

---

## 8. What it costs to maintain

Better than it looks. The map is *ingredients × locales*, not
*recipes × locales* — a few thousand rows at most, maintained by whoever
maintains the price feed, since `staple` is essentially derivable from feed
presence. Only `specialty` and `absent` need a human judgement, and only once
per ingredient per market.

Compare with the alternatives already accepted: per-locale editors (discovery-draft §2.4) and per-recipe tags (philosophy §16.7). This is the cheapest per-locale
obligation in the system, and it is the one that protects the cost pillar.

---

## 9. Derived, never authored

Following philosophy §11's test — *could a careful person disagree?*

- `cookable_in[locale]` — derived from the stock map. A fact.
- `priceable_in[locale]` — derived from feed presence. A fact.
- `blocking_ingredients[locale]` — derived. The editorial queue in §6.

`stock` itself is authored, because *is this obtainable in Cairo* is a judgement
about a market and a careful person can disagree.

---

## 10. What this does not settle

- **Whether `specialty` needs sub-states** (imported / seasonal / regional).
  Seasonality in particular is a different axis again — obtainable in March, not
  in October — and is deliberately excluded here.
- **The discovery default** in §7.
- **Who fills the map for locale two,** which is the discovery-draft §2.4 hiring problem again.
- **Whether `absent` should ever be overridable by the cook** ("I can get this,
  price it anyway"). Touches philosophy §8's no-publishing rule and needs its own argument.

---

## Proposed decision-log entries, if accepted

| Date | Decision | Section |
|---|---|---|
| — | Obtainable and priceable are separate axes | 2 |
| — | `stock` is a per-locale map beside the price feed; unset ≠ absent | 3 |
| — | Unpriced `seasoning`/`fixed` → cost floor; unpriced `continuous`/`discrete` → withhold | 4 |
| — | Substitution is an authored note, never applied automatically | 5 |
| — | Availability gates publication per locale, not display | 6 |
| — | Obtainability is a discovery constraint axis, not a hidden filter | 7 |
