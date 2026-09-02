# Matbakh — amendment blocks for `philosophy.md` and `discovery-draft.md`

**Drafted 29 August 2026.** Paste-ready text for the six decisions settled in the
competitor-study session, plus the amendments those decisions force on
`discovery-draft.md`.

> **Read this first.** These blocks were written against the project-synced copy
> of both files, not against your working tree. Every section number below is
> stated as a target, not an assertion — **verify against the live file before
> pasting.** Where a block replaces existing text rather than appending, it says
> so explicitly.

> **Cross-reference convention followed throughout:** a bare `§n` means the
> document being edited; anything else names its file.

---

## Numbering — read before pasting

`philosophy.md` currently ends at **§16 Open questions**. Two of the blocks below
are new *settled* sections, which means they land after the open-questions
section — structurally odd, but it honours append-never-insert.

**Do not insert them before §16 and renumber.** That is what happened on 13
August, and the handover still carries the mapping table of broken references.

One complication worth knowing now: `discovery-draft.md`'s own header says that
if accepted it *"becomes a numbered section before philosophy §16, and philosophy
§16.1 is deleted"* — which is an insert-and-renumber by design. So a renumber is
coming anyway when discovery lands. That is fine if it happens **once,
deliberately, with a documented old→new mapping**, the way 13 August was handled.
The failure mode is an undocumented renumber, not a renumber.

So: append as §17 and §18 now; let discovery's landing renumber everything once,
with a table.

---

# Part A — `philosophy.md`

## A1 · §6.7 — dual units (append to the existing subsection)

> **Target:** end of §6.7 "Three numbers, not one". Appends; replaces nothing.

```markdown
**Units display as authored, not as converted.** Where an ingredient record
carries both a mass and a household measure, both are shown together — *200 g ·
1 cup* — rather than behind a toggle. The app performs no unit conversion of its
own: a household measure appears only because someone entered it for that
ingredient. Egyptian cup and spoon sizes vary enough that a computed conversion
would be a fabricated number, which §3 forbids.

The consequence is an authoring requirement, not a rendering one: an ingredient
displays dual units only if both fields are populated. See §11.
```

## A2 · §9 — "why this version" as a required field (append)

> **Target:** end of §9. Appends to the existing settled section.

```markdown
**The obligation is a field, and it is load-bearing.** `why` is required on every
recipe. It is what replaces the contributor identity a UGC platform supplies for
free: on a shelf with no ratings, no review counts and no popularity ordering
(§8), the stated reason for a dish being the chosen version is the only
differentiating element the reader has.

Two consequences that must not be lost:

- It is **the most important string in the recipe**, written once per dish, per
  language.
- It carries an editorial cost that is **not** in the per-recipe production
  model. Add it to what the pilot measures rather than discovering it at recipe
  three hundred.
```

## A3 · §11 — schema additions (append to the settled section)

> **Target:** end of §11 "Schema fields — SETTLED, and now implemented".
> **Note:** §11 is marked settled and implemented, so this must read visibly as
> an addition with a date, not as though it were always there.

```markdown
### 11.x Additions, 29 August 2026

**Ingredient records — household measure.** A second display unit alongside the
mass unit, optional per ingredient. Populated by hand; never computed. Drives
§6.7's dual display.

**Palate deltas — a user-side store, not a recipe field.** Adjustments live
against the user, keyed on `(recipe_id, ingredient_id)` — or on
`(component_id, ingredient_id)` where the line belongs to a sub-recipe (§14).
Stored as **multipliers**, never absolute amounts. See §18.

The delta store is deliberately **aggregatable**: the same records read across
users are the only quality signal available on a catalogue that one author
cannot test at scale. Design the shape for that reading from the first commit,
not after.
```

## A4 · §16.1 — Discovery, partly settled (REPLACES the status line)

> **Target:** §16.1, currently headed *"Discovery — NOT STARTED"*.
> **This block changes the heading and appends below the existing text.** Keep
> the existing two paragraphs about browsing being the product and the governing
> question; they are still right.

```markdown
### 16.1 Discovery — PARTLY SETTLED (29 August 2026)
```

then, after the existing text:

```markdown
**Settled 29 August 2026: ingredient-led entry is a primary discovery route.**
The user names what they already have; the shelf subtracts everything they
cannot cook. Three independent signals support it — it is given away free by one
market leader, charged for as a premium feature by another, and is the entire
product of the most-downloaded Egyptian recipe app.

Two constraints settled with it:

- **Presence, not quantity.** No pantry inventory. The user marks that they have
  chicken, not that they have 340 g of it. Every product that has asked users to
  maintain quantities has died on the maintenance burden. Quantity resolution
  happens against the recipe, never against the pantry.
- **Staples assumed present** — salt, oil, onion, garlic, flour, sugar — and
  unset rather than set. A session that opens with twenty taps before returning
  anything is not completed.

**This route runs on the ingredient graph, not on tags.** It therefore does not
block on §16.7. Recording that explicitly, because bundling the two made an
accepted feature look blocked by the project's most overdue decision.

The rest of §16.1 remains open, and `discovery-draft.md` remains its input.
```

## A5 · §16.2 — pre-commit cost and nutrition (REPLACES the subsection)

> **Target:** §16.2, currently *"Pre-commit presentation of cost and nutrition —
> NOT STARTED"*. **Replace the whole subsection.** Two things land at once: the
> bolognese prototype's answers, which the handover records as never written
> back, and the browse-card decision.

```markdown
### 16.2 Pre-commit presentation of cost and nutrition — PARTLY SETTLED

**Answered in practice 19 August 2026 by the bolognese prototype.** Nutrition
sits on the Overview pane beneath the cost — same class of fact, same glance.
The cost row shows its own absence: `—` with *no price feed connected*, never an
invented number. That puts §3's honesty commitment on screen rather than in
prose.

**Settled 29 August 2026 — cost on the browse card.**

Indicative cost is visible to owners on every browse card. Non-owners see it on
a **fixed sample set** of dishes only, chosen editorially and precomputed —
never a live query, which would be a free API over the catalogue.

The split follows the pricing commitment in §17. The market price list is free;
the cost of a *specific dish* is paid, because it requires the recipe.

**What the card carries.** Not a bare figure: the named market, the date, and
which serving preset the number refers to. Presets are discrete, so a cost
without its preset is ambiguous. Where the owner holds a palate delta on that
recipe (§18), the card shows the adjusted figure.

**What a non-owner sees: a blurred figure**, in the same position and
typography as an owner's, with the market and date still legible. Not a padlock.
The blur must be produced server-side; a client-side effect over the true value
leaves the number in the payload and makes the boundary decorative.

**The distinction this rests on, stated because it is easy to get wrong.**
`discovery-draft §2.2` forbids a cost affordance that resolves to nothing.
Absence because *no data exists* is dishonest — it implies a number that is not
there. Absence because *unpaid* is honest — the number exists, is real, and is
dated. These are different facts and **they must be visually distinct.** A
reader in a locale with no price feed and a non-owner in a priced locale must
never see the same treatment.

Still open: the recipe page before commit, which is larger than the card.
```

## A6 · §17 — pricing and the free surface (NEW SETTLED SECTION)

> **Target:** new top-level section appended after §16.

```markdown
## 17. Pricing and the free surface — SETTLED (29 August 2026)

### 17.1 What is free, permanently

**The weekly market price list.** What staples cost, at a named market, on a
named date. Published in the app and — with no install required — on the
channels where the audience already is.

This is free **perpetually**. The commitment is one-way and cannot be withdrawn.

### 17.2 What is paid

**The catalogue, and the cost of a specific dish.** A dish cost requires the
recipe, its quantities, its scaling classes and its purchase-unit rounding. It
is therefore a property of the catalogue, not of the price list.

The line is: **free is the raw data; paid is the data applied to a dish.**
Knowing what tomatoes cost this week does not tell a cook what koshari costs,
how much to buy, or how to make it.

### 17.3 Why the free thing is never the paid thing

A free tier carved out of the catalogue would give away fixed assets — each
recipe authored, test-cooked and photographed once, at real cost — to someone
who may never pay. The price list is the opposite: one dataset, produced weekly,
served to everyone at no marginal cost. It also has to exist for the paid
product regardless.

The structural benefit is that **nothing ever has to be taken away.** Products
that build a free audience and later paywall it pay for the retrofit in
goodwill. A product where the free surface was never the paid surface cannot
incur that.

### 17.4 The consequence to hold

Because the price list is permanently free, it cannot carry a renewal charge.
Any recurring revenue must come from new catalogue content, not from access to
prices. That constraint is now fixed.
```

## A7 · §18 — palate adjustment (NEW SETTLED SECTION)

> **Target:** new top-level section appended after §17.

```markdown
## 18. Palate adjustment — SETTLED (29 August 2026)

After cooking a recipe as authored, a cook may adjust ingredient quantities to
taste. The adjustment belongs to the cook, never to the catalogue.

This does not weaken the test-cooked promise: they cooked the authored version
first, and adjusting on a second attempt is the ordinary behaviour of a cook, not
a deviation the product has to defend.

### 18.1 Multipliers, never absolute amounts

An adjustment is a factor — ×1.5 salt — applied **after** the ingredient's
scaling class has been resolved (§6.2). Three reasons compound:

- Serving presets are discrete, so an absolute delta captured at four servings is
  wrong at eight.
- Seasoning has its own scaling class precisely because it does not scale
  linearly; an absolute delta would bypass that rule rather than compose with it.
- When a later edition revises a recipe's quantities, a multiplier survives the
  revision. An absolute silently corrupts.

### 18.2 Deltas, never forks

The adjustment is a layer over the canonical recipe. It never produces a copy.
A fork would make the catalogue hold many recipes per dish through the user's own
hands, which is exactly what §9 exists to prevent.

### 18.3 Applied automatically, and marked

Subsequent cooks show the adjusted quantities by default, with a visible marker
that the recipe deviates from the authored version and a one-tap return to it.
Never silent: the cook must always be able to see which state they are in, in the
same way §6.1 requires for scaling.

### 18.4 It flows through

Adjusted quantities propagate to the consolidated shopping list, the computed
nutrition panel and the cost figure. All three are computed rather than typed, so
this is wiring — but it must be wired deliberately, or the nutrition panel
describes a dish the cook is not making.

### 18.5 Components propagate

A sub-recipe is a first-class recipe (§14), never duplicated into its parent. An
adjustment to a component therefore belongs to the component and follows it into
every dish that uses it.

### 18.6 What the deltas are also for

Read across users, the deltas are a continuous quality signal: if most cooks
reduce the salt in a recipe, that recipe is over-salted. This is telemetry, not
publication, and §8 is untouched.

Given that the catalogue is authored by one person who cannot test at scale, this
may be the more valuable half of the feature. It only exists if the store is
shaped for aggregate reading from the outset.
```

## A8 · Decision-log entries

> **Target:** `philosophy.md`'s dated decision log. Match the existing column
> format — check whether the log sits inside `<!-- GENERATED -->` markers before
> typing into it; if it does, hand-edits will be overwritten.

| Date | Decision | Section |
|---|---|---|
| 29 Aug 2026 | Units display as authored; no computed conversion | 6.7, 11 |
| 29 Aug 2026 | `why` is a required, load-bearing field with an editorial cost | 9 |
| 29 Aug 2026 | Ingredient-led entry settled as a discovery route; presence not quantity; does not block on tags | 16.1 |
| 29 Aug 2026 | Bolognese prototype's cost and nutrition placement written back | 16.2 |
| 29 Aug 2026 | Cost on browse card: owners see it, sample set for everyone, blurred server-side otherwise | 16.2 |
| 29 Aug 2026 | Weekly market price list free perpetually; dish cost paid; commitment is one-way | 17 |
| 29 Aug 2026 | Palate adjustment as multipliers, auto-applied and marked, flowing through, components propagating | 18 |

---

# Part B — `discovery-draft.md`

Two amendments. The first is mandatory: the draft currently defers a feature that
has since been accepted, and a session reading it would build around a deferral
that no longer holds.

## B1 · §8 — ingredient search is no longer deferred (REPLACES the bullet)

> **Target:** §8 "Search", the third bullet, currently reading *"Ingredient search
> is deferred. 'What can I make with what's in the fridge' is a pantry feature
> with no schema behind it. Different surface, argued separately if at all."*
> **Replace it.**

```markdown
- **Ingredient search is a primary route, settled 29 August 2026**
  (philosophy §16.1). The earlier position in this draft deferred it as "a pantry
  feature with no schema behind it"; that is now overtaken. The schema does exist
  — `content/ref/ingredients.yaml` is a closed, controlled vocabulary with
  scaling classes, which is precisely what the route resolves against. It is a
  **subtraction** in §4's sense, not a recommendation: the user supplies what
  they hold, the shelf removes what they cannot cook.
  - **Presence, not quantity.** No inventory to maintain.
  - **Staples assumed present**, unset rather than set.
  - **Rank by fewest missing**, not by exact match only. A dish missing one
    ingredient is the useful result, and naming the missing item with its price
    is where this route meets the pricing pillar.
  - It runs on the ingredient graph, so unlike §4's declared filters it does
    **not** block on philosophy §16.7.
```

## B2 · §5 and §2.2 — the paid state on the card (APPEND to §5)

> **Target:** end of §5 "The card is the unit", after the `why` paragraph.

```markdown
### 5.1 Cost has three states on the card, not two

Settled 29 August 2026 (philosophy §16.2). §2.2 establishes that a cost affordance
must never resolve to nothing. Ownership introduces a third state, and it must
not be confused with the second:

| State | When | What the card shows |
|---|---|---|
| **Priced** | Locale has a feed; the reader owns the catalogue | The figure, with market and date |
| **Unpriced locale** | No `price_source` for this locale | The cost element is **composed out entirely** — no row, no grey, no placeholder (§2.2) |
| **Unpaid** | Locale has a feed; the reader does not own the catalogue | A **blurred figure** in the same position and typography, market and date still legible |

The second and third states must be **visually distinct**. They mean different
things: one says *this data does not exist here*, the other says *this data
exists and is not yours yet*. Collapsing them into a single grey treatment makes
an honest signal and a commercial one indistinguishable, which is the failure
§2.2 is written to prevent.

The blurred state is not an exception to §2.2. That rule protects against a
number being *implied but absent*. Here the number exists, is real and is dated
— the reader simply has not bought access to it. Absence-because-no-data and
absence-because-unpaid are different facts.

**A fixed editorial sample set of dishes shows its cost unblurred to everyone**,
precomputed and refreshed with the feed. This is the same set used off-app; it
is chosen, not scraped, which is the point.
```

## B3 · §12 — update what remains unsettled

> **Target:** §12 "What this section does not settle". Amend two bullets rather
> than adding.

- The philosophy §16.2 bullet: narrow it. §5.1 and philosophy §16.2 now settle the
  card; the recipe page before commit remains open.
- Add: **the tag vocabulary blocks §4's declared filters only.** Computed
  constraints — cost, hands-on time, ingredients held — resolve against data that
  already exists and are buildable now.

## B4 · Proposed decision-log entries — add two rows

| Date | Decision | Section |
|---|---|---|
| 29 Aug 2026 | Ingredient search is a primary route, not deferred; presence not quantity; rank by fewest missing | 8 |
| 29 Aug 2026 | Cost has three card states; unpriced-locale and unpaid must be visually distinct | 5.1 |

---

# What to check before pasting

1. **Section numbers.** Every target above is stated from the synced copy. Verify
   against your working tree.
2. **Whether the decision log is generated.** If it sits inside
   `<!-- GENERATED -->` markers, hand-edits are overwritten on the next build.
3. **§16.2's existing wording.** A5 replaces the subsection. Confirm nothing else
   in the file depends on its current text.
4. **§11's structure.** A3 assumes §11 has numbered subsections it can extend.
   If it does not, fold the additions into the existing prose with the date.
5. **`manifest.yaml`'s `next_up`.** It currently lists Discovery (§16.1) and the
   tag vocabulary (PM-07, §16.7). After these edits, §16.1 is partly settled and
   the two are no longer one item — PM-11 now owns discovery.

Then: CHANGELOG.md, `matbakh_pm_log.md` §13, and **push**. None of this reaches a
Claude Code session until it is on GitHub.
