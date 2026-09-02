# Matbakh — App Design Philosophy

**Status:** Living document. Sections marked SETTLED are decided and should not be relitigated without a stated reason. Sections marked OPEN are unresolved.

**Last updated:** 2026-08-29

---

## 1. The stance — SETTLED

**Matbakh is a kitchen instrument that contains recipes, not a recipe app that happens to be used in a kitchen.**

Conventional recipe apps are optimised for browsing and deciding; the cooking moment is an afterthought. Matbakh inverts this. The counter-top posture — tablet or phone propped on the surface, hands busy, attention divided — is the design centre. Everything else is arranged around it.

This is the most defensible thing in the concept. Curation can be copied. Live pricing can be copied. A product built entirely around the ten minutes when the cook's hands are covered in flour is hard to retrofit.

---

## 2. The three pillars are not equal — SETTLED

They operate at different moments, at different frequencies, and do different jobs. Treating them symmetrically would produce a muddled interface.

| Pillar | Owns | Frequency | Job | Surface |
|---|---|---|---|---|
| **Method** | The cooking session | Rarely changes | The reason to open the app today | Full screen (cook mode) |
| **Cost** | The return visit | Weekly | The habit mechanism | Home surface + notification |
| **Nutrition** | Permission to commit | Static | Makes the cook feel authorised, not informed | Findable panel, easy to ignore |

Method gets the screen. Cost gets the notification. Nutrition gets a panel.

---

## 3. Core principles — SETTLED

1. **The page is the unit, not the scroll.** A step is a destination, not a position in a stream. No scrolling anywhere in cook mode. The cook always knows where they are and how far is left.

2. **Show the verb, say the noun.** Icons carry actions. Digits carry quantity. Words carry only the name of the thing and irreducible judgement. This line — not a word count — is the definition of "few words."

3. **One mandatory gesture.** Page turn is the only gesture a cook is *required* to perform. Everything else (tap for detail, tap for video, tap to mark done) is optional and never blocks progress.

4. **Order-independence governs grouping.** Actions that share a station and can be done in any order share a page. Sequence-dependent actions get their own page, because in cooking the sequence *is* the information.

5. **The cook's place is sacred.** State over navigation. Tiles remember themselves. The map never steals your position. Waiting is a property of a step, never a step of its own. The session survives interruption, backgrounding and app kill.

**Two structural commitments underneath:**

- **Two views, one truth.** The visual view and the Arabic/English prose view are two renderings of the same structured recipe object — never authored separately. This turns localisation into a data problem, not an editorial one, and prevents drift across 500 recipes × 2 languages.
- **Every number carries a date and a source.** "EGP 84 — El-Obour, updated Tuesday" is more trustworthy than a bare number. Never present a computed estimate as a fact.

---

## 4. Cook mode (the reader) — SETTLED

### 4.1 Page structure

- **A page may hold multiple actions if they are order-independent and share one station.** All knife prep — onion, garlic, tomato, coriander — is one page with four tiles. "Sear the chicken" and "deglaze" are two pages.
- **Target: 6–10 pages typical, 14 hard ceiling.** Exceeding it is an editorial signal: either the recipe is genuinely a project dish and should be labelled as such, or the steps are over-atomised and need merging.
- **The 14 ceiling is doubly justified** — it is also roughly the most pages that can be shown as legible thumbnails on one phone screen in the map.
- **Waiting is never a page.** "Simmer 20 minutes" is a timer attached to the preceding action, not a step of its own.

### 4.2 The real cost is re-reading, not page count

Turning a page is nearly free. What is expensive is losing your place — returning from the stove and having to reconstruct which half of a page you had already done. Page count is therefore the wrong metric to optimise; **pages you must re-read** is the right one.

### 4.3 Tile state

- Each tile holds its own done/not-done state, persisted.
- **Implicit by default:** turning forward from a page marks its tiles done.
- **Explicit as override:** tapping an individual tile toggles just that one.
- The cook who never taps anything still gets sensible state for free. Nothing is required.
- **Forward turn marks done — not "being past."** Jumping from page 2 to page 7 leaves pages 3–6 bright. A bright page between dimmed ones is a useful warning, not a bug.

### 4.4 The map (thumbnail overview)

- **Primary value is the thirty seconds before starting** — seeing the whole arc, the number of stages, where the long waits are. No recipe app offers this without scrolling the whole thing.
- Doubles as the progress indicator; no separate "step 4 of 8" chrome needed.
- **One screen, no scroll.** The moment it scrolls it becomes the wall of text we removed.
- **Thumbnails are icon clusters, not photos.** Miniaturised step photos are eight indistinguishable brown pans. Icon arrangements stay recognisable at small size — and cost nothing extra to produce.
- **Three states, not two:** untouched (full colour) / partial (dimmed, with finished tiles individually greyed inside the thumbnail) / done (dimmed whole). Partial is the state that earns its keep — it is exactly where binary dimming would lie to the cook.
- Dim to mark *spent*, not to push away. Done pages are still frequently revisited to check a quantity.
- **Returning from the map defaults to where you were, not where you looked.** Opening the map preserves position; tapping a thumbnail moves you; dismissing without tapping returns you. A glance must never cost the cook their place.

### 4.5 Interaction

- **Tap, not hover.** Deliberate, works on tablet and phone. Hover remains available as a desktop nicety in the prose view only.
- **The tile is the tap target, not the glyph.** Wet hands and a 44px icon do not mix — icon, label and padding form one large zone.
- **Session survives interruption.** Doorbell, child, phone call, lock screen, app kill.

### 4.6 Timers

- **Timers belong to the session, not the page.** Rice and sauce run concurrently; leaving a page must not kill a clock.
- **A persistent band at the screen edge** shows everything currently running with live countdowns, independent of the page in view. The page says what your hands do next; the band says what the stove is doing without you.
- This is how parallelism is expressed without inflating page count — and it is the piece most recipe apps simply do not have.
- Alarms must be audible from another room and survive lock.
- Once the map permits out-of-sequence jumping, **the band is the sole authority on what is actually cooking.**

### 4.7 Resuming

- Progress state persists indefinitely. No auto-expiry (someone may leave dough to prove for six hours).
- Reopening a recipe with existing progress asks once: **resume, or start fresh.** One tap, no guessing.
- Yields useful intelligence: how often cooks abandon partway, and on which page.

---

## 5. Language and notation — SETTLED

### 5.1 Three carriers, not two

| Carrier | Conveys |
|---|---|
| **Icons** | Actions — chop, fold, simmer, rest |
| **Digits + unit symbols** | Quantity — 200 g, 20 min, 180 °C |
| **Words** | Only the name of the thing, and irreducible judgement |

### 5.2 Reducing the residue

The hard cases are doneness cues — *until translucent*, *until the water runs clear*. A wordless app that quietly drops these has removed the cooking knowledge and kept the arithmetic. Two of the three are recoverable:

- **Doneness becomes a photo.** Not hero shots of the finished dish — cropped images of *what it should look like right now*. More precise and more portable than the phrase. The highest-value visual asset in the product, and nobody does it well.
- **Heat becomes an ordinal glyph.** Low/medium/high is a three-segment indicator. Same mechanism serves spice level, which the heat filter needs anyway.
- ***To taste* stays as words.** A short, fixed, reusable phrase set across 500 recipes translates once and costs nothing thereafter.

### 5.3 Numerals

**Western Arabic numerals (200, not ٢٠٠).** Rationale: Egyptian supermarket packaging, price tags and kitchen scales use Western numerals almost universally, and the cook is reading the app beside the bag of flour. Also portable to the Gulf and beyond without a second render path.

A settings toggle for Eastern Arabic numerals may be offered, but Western is the default.

### 5.4 Architectural consequence

**Digits are the only element on the page that changes** — via serving scaling, unit toggles and live pricing. They must therefore be a **live text layer over a static visual grammar**, never baked into an icon or composite step graphic. Easy to violate accidentally once someone starts producing composite artwork.

### 5.5 Four surfaces, and what each one's cost scales with — SETTLED 2 September 2026

A cook in front of the reader asks four questions. Each is answered on a different surface, at a different size, and — the part that decides the economics — each scales with something different.

| The question | Surface | Size | Cost scales with |
|---|---|---|---|
| **Where am I?** | the arc / map | **17 px** | the vocabulary |
| **What do my hands do?** | the tile | **44 px** | **open — see §16.6** |
| **Is it ready?** | the doneness photograph | 361 × 176 | the catalogue |
| **Why, and what did I miss?** | prose, on request | — | free, generated at build |

Three of the four are settled, and they are settled because each has exactly one carrier that survives its size.

- **The arc is glyphs, and cannot be anything else.** A photograph at 17 px is eight indistinguishable brown pans (§4.4), and a video frame at 17 px is a photograph. Whatever the tile becomes, the glyph set is owed — it is not a concession to any option.
- **The doneness photograph is irreducibly recipe-specific**, and it carries the trust claim. That was never the tile's job.
- **Prose is generated at build time**, not authored per recipe.

**The tile is the open question, and it is the only one.** What a 44 px square should carry — a static glyph, an animated glyph, or a short silent loop — is §16.6.

**Why this framing matters more than the answer.** The settled rows do not scale alike. The arc scales with the *vocabulary*: 81 activities, fixed, however large the catalogue grows. The doneness photograph scales with the *catalogue*: 500 recipes and rising. Anything moved from the second column to the first stops being a per-recipe cost and becomes a one-time one. That is the entire economic question in a sentence, and it is why the tile's carrier is worth measuring rather than assuming.

---

---

## 6. Serving scaling — SETTLED

### 6.1 Frame

The base recipe is the one that was cooked and tested. Every other serving count is a derivation the kitchen never saw. The app always shows which state it is in, and **returning to the tested base is one tap.** A scaled recipe is a calculation; the ×1 is the promise.

### 6.2 Scaling is a property of the recipe line, not the ingredient

Salt in bread dough is 2% of flour weight and scales linearly. Salt in a stew is a judgement and does not. Same ingredient, opposite behaviour. The class defaults from the ingredient library and is **overridable per recipe line** — the author accepts the default most of the time and corrects the rest.

| Class | Behaviour | Typical |
|---|---|---|
| **Continuous** | Linear, rounded to a legible increment | Flour, rice, stock, meat by weight |
| **Discrete** | Linear, then rounded to whole (or ½ if divisible) | Eggs, lemons, chicken thighs, onions |
| **Seasoning** | Sub-linear — factor^0.75 | Salt, chilli, spices added to taste |
| **Fixed** | Does not scale | Frying oil, blanching water, pan-coating butter |

**Why sub-linear seasoning:** tripling a stew and tripling its cumin produces an inedible stew — flavour compounds concentrate faster than volume. factor^0.75 turns ×3 into ≈×2.3, close to where an experienced cook lands; the residual is caught by *to taste*.

**Why Fixed matters:** it is the class people forget, and the one that produces absurd output. Nobody wants 750 ml of frying oil because they doubled the koftas — oil depth is set by the pan, not the batch.

### 6.3 Rounding ladder

Precision exceeding what the kitchen can measure is fake precision.

| Magnitude | Round to |
|---|---|
| under 10 g | 1 g |
| 10–100 g | 5 g |
| 100–500 g | 10 g |
| over 500 g | 25 g |
| spoons | ¼ tsp / ½ tbsp |

Where rounding moves the value more than ~5% off exact, prefix with **≈**. It is a symbol, not a word, so it costs nothing against the wordless principle.

### 6.4 Serving presets, not a free slider

Each recipe **declares its serving presets, derived from its own countable ingredients** so they always come out whole.

- A 4-serving recipe with 3 eggs offers **2 / 4 / 8** — not 6, which would produce 4.5 eggs.
- A recipe with no discrete ingredients offers **2 / 4 / 6 / 8** freely.
- Half of a divisible item (½ onion) is acceptable and shown as ½. Half a chicken thigh is not — hence the `divisible` flag.

The constraint is computed at authoring time, not guessed at runtime. The cook never encounters an impossible number.

### 6.5 Physical ceiling

Scaling has a limit unrelated to arithmetic — twelve portions in one wok is a grey stew. Each recipe carries `max_scale_factor`. Beyond it the app does not refuse; it shows a **two-pan glyph meaning "cook in batches."** Cooking knowledge delivered as a symbol.

Indicative: stir-fry and sear ×2 · braise and stew ×4 · baking ×2 with a tin-size note.

### 6.6 Time under scaling

Simmering 6 portions takes about as long as 4; browning 6 takes noticeably longer. Rather than model this, **mark mass-sensitive timed steps** — when scaled, the timer is presented alongside the doneness photo rather than as the authority. The clock becomes advisory; the target state becomes the truth. Scaling error is routed into a mechanism already being built.

### 6.7 Three numbers, not one

**Exact** (internal, unrounded) → **Displayed** (rounded, what the cook reads) → **Purchase** (rounded up to pack size, shopping list only).

**Cost per dish computes from exact quantity consumed, never from pack size** — otherwise a pinch of saffron costs a whole jar and the headline cost figure becomes nonsense. Pack-size rounding belongs only to the shopping list.

**Units display as authored, not as converted.** Where an ingredient record
carries both a mass and a household measure, both are shown together — *200 g ·
1 cup* — rather than behind a toggle. The app performs no unit conversion of its
own: a household measure appears only because someone entered it for that
ingredient. Egyptian cup and spoon sizes vary enough that a computed conversion
would be a fabricated number, which §3 forbids.

The consequence is an authoring requirement, not a rendering one: an ingredient
displays dual units only if both fields are populated. See §11.

---

## 7. Technique video — SETTLED (revised from original concept)

Original concept: hover-to-play clip on every activity icon, in cook mode.

**Revised:** technique video lives in a separate **Techniques library** browsed *before* cooking, and in the prose view. Not in the critical path of cook mode.

Rationale:
- The governing principle is **if a step needs a video to be understood, the step is wrong.** Icons in cook mode must be self-sufficient.
- Precise taps on small icons with wet hands is the hardest interaction in the app.
- 65 clips is a production line, a storage cost and a recurring localisation burden.
- Separating it lets clips be produced gradually for the ~20 activities that genuinely need them, rather than all 65 up front.

---

## 8. User feedback — SETTLED

Cooks may **report** — timing was off, cost looks wrong, this did not work. They may never **publish**. Feedback is telemetry for the editor, not content.

The most valuable signal available: **which step people abandon on.** That is a map of where recipes are failing, and no UGC competitor can read it that cleanly.

---

## 9. "One recipe per dish" — SETTLED

A promise, not scarcity. But it obligates the app to state **why this version** in one line. Without that, omission reads as absence rather than choice, and someone's grandmother's version becomes a complaint instead of a conversation.

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

---

## 10. On "globally adaptable" — SETTLED (with caveat)

Visual design makes the *interface* portable — likely a two-thirds reduction in translated word count. It does **nothing** for the pricing pillar, which is locale-bound by definition and is the actual expansion bottleneck.

Egypt → Gulf is not a translation problem. It is a wholesale-data-sourcing problem. The wordless principle must not create false confidence about the cost of market entry.

---

## 11. Schema fields — SETTLED, and now implemented

Cheap to decide now, very expensive to retrofit across 500 recipes.

**Reconciled against the built schema, 1 August 2026.** The names below are the
implemented ones. The July draft of this section used names that were all
changed during implementation — `scale_class` became `cls`, `base_servings`
became `servings.base`, `order_dependent` became `ordered` — so it described a
schema that never existed. `content/recipes/_template.yaml` is the working
reference; this section is the argument for why each field is there.

**On the ingredient** — `content/ref/ingredients.yaml`

| Field | Why |
|---|---|
| `cls` | continuous · discrete · seasoning · fixed. Without it nothing can scale. |
| `divisible` | Only meaningful on `discrete`. Half an onion is sensible, half a bay leaf is not. |
| `unit` | g · ml · count · tsp · tbsp |
| `pack` | Pack size, for the shopping list |
| `buy` | What a shopper looks for on the shelf. Bilingual. |
| `nutrition` | Per 100 g/ml. Lets per-serving figures be computed rather than typed 500 times. |
| `convert` | `cup_g` and `piece_g`. Spoons derive at cup/16 and cup/48 — one recorded number, not three that can disagree. Without it, counted and spoon-measured ingredients contribute nothing to computed nutrition. |
| `diet` | The allergen and dietary classes. **Unset ≠ empty:** empty means *contains none*, unset means unknown, and any recipe using an unset ingredient has its dietary tags withheld entirely. A vegetarian claim wrong once costs a guest their dinner. |

No cost field. Prices come from the market feed, keyed on the id.

**On the tile** — one action

`do` (lexicon activity) or `verb` (bespoke, needs `glyph`) · `qualifier` ·
`item` or `items[]` · `amt` · `carried` · `short`

`carried: true` marks the same physical ingredient reappearing at a later
station, so the shopping list counts one bird rather than three.

**On the step** — one page, one station

`station` · `qualifier` · `ordered` · `heat` · `photo` · `doneness` ·
`note {kind, text}` · `timer {minutes, label, mass_sensitive}` · `makes`

`photo` and `doneness` travel together: the photograph shows what the words say.

**On the recipe**

`id` · `source_locale` · `status` · `title` · `why` ·
`servings {base, presets, max_scale}` · `hands_on_minutes` · `hero` ·
`price_source` · `nutrition_per_serving` · `intermediates` · `shorts` · `steps`

**Added since the July draft**

| Field | Section |
|---|---|
| `uses [{id, amt}]` and `yield {amount, unit}` | §14 |
| `diet` on the ingredient | §16.7 |
| `convert` on the ingredient | above |
| `@intermediate` references | §14 |
| `tags` — proposed in `design/tag-proposal.md`, **not yet settled** | §16.7 |

**Derived, never authored:** `contains` · `vegetarian` · `vegan` ·
`gluten_free` · `total_minutes` · `cost_per_serving` · `kcal_per_serving`. The
test for which side a field belongs on: *could a careful person disagree?*
Cuisine is judgement. "Contains dairy" is a fact about the ingredient list.

### Additions, 29 August 2026

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

---

## 12. Music while cooking — SETTLED

**Decided 30 July 2026.** Matbakh does not integrate with Spotify or any other
music service. A cook who wants music opens their own app; the home button is
four seconds away.

- **Streaming playback would exclude much of the audience.** Spotify's Web
  Playback SDK and every playback endpoint require full Premium. Mobile-only
  tiers — Lite, Premium Mini — are excluded, and those are what a large share of
  Egyptian subscribers hold. The API reports them as `"product": "premium"`
  regardless, so the failure cannot be detected cleanly before it happens.
- **It fights the counter-top posture (§1).** Mobile browsers block transferred
  playback as autoplay; recovery needs a deliberate tap. Every failure mode
  lands on a cook with wet hands.
- **Downloaded playlists are not a way round it.** The offline cache is
  encrypted DRM — defeated technically, and prohibited by the terms.
- **Terms risk.** Spotify's platform terms bar commercial streaming
  integrations. Matbakh is a commercial product.
- **It moves no number that matters.** The launch gate is commerce attach rate.

**What this leaves open.** The timer alarm has to be audible over music already
playing on the same speaker. A web page cannot duck another app's volume, so the
alarm must carry on its own — a sound-design problem, not an integration one.
This is true today with no integration at all, and a missed 40-minute stock is a
ruined dish.

If music returns, the only shape worth considering is licensed instrumental
audio Matbakh owns outright: offline, duckable, no third party. That is a
Ramadan sponsorship asset, not a launch feature.

## 13. Entertaining — WORKED THROUGH, NOT BUILT
Proposed menus, budget, shopping list. A genuinely different mode with different physics.

Argued through 1 August 2026. The conclusion is that it is **two features, not one**, and the split matters more than anything else here: one is a document, the other is a change to the reader. They ship separately and in that order.

**Worked example** (the brief this was argued against): twelve covers, Mexican, beef and chicken preferred over seafood, two vegetarians, not too spicy, a salad included, 1,500 LE — about 125 a head.

#### A. The party plan — a pre-commit document

Everything the host reads *before* they start cooking. It cannot drift, because nothing in it is live.

1. **Menu suggestion, modifiable.** A constrained selection over tagged recipes — cuisine, protein, spice, course, dietary, cost. Small enough to solve exactly. Blocked on §16.7; see below.
2. **One consolidated shopping list, editable.** Merge the `items` arrays across every chosen recipe, sum by ingredient key, apply scaling classes. `carried` already prevents double-counting within a recipe and does the same across them. Priced live from the market feed — which is what makes "125 a head" a claim no recipe app can make, and is arguably the acquisition hook rather than the schedule.
3. **What can be made ahead.** `make_ahead` and the `makes` / `@intermediate` edges already express this. A sequence with no clock: what to do Thursday, what to do Saturday morning.
4. **Batched preparation.** Group every tile across the whole menu by `(activity, ingredient, qualifier)` — *chop 14 onions once*, not four times across four recipes. This is the thing no recipe app does and every cook does by hand.

   The August 2026 lexicon merge is what makes this work. With 294 separate verbs, `julienne` and `slice` would have grouped apart; consolidated into one activity with a qualifier, they group together. The grouping key is the qualifier precisely because that is what distinguishes *diced* from *sliced* onion when three recipes want one and the fourth wants the other.
5. **An ordered task list, no clock times.** Sorted by passive duration descending — the four-hour marinade first, the ninety-minute proof next, the twenty-five-minute rice late. Relative to serve time, never absolute.

**Why no clock, and no scheduler.** A schedule that says *7:12 — take the beef out* is a promise. The moment the cook is nine minutes behind, every line after it is wrong, and the instrument that is supposed to be trustworthy with wet hands is lying at exactly the moment the stakes are highest. Falling behind is not the exception in home cooking; it is the normal case.

Constraint scheduling is technically straightforward here — forty tasks, six resources, solvable in milliseconds. That is not what makes it hard. What makes it hard is that durations are unreliable (a timer is honest; *chop two onions* is ninety seconds for one cook and five minutes for another), the cook is the scarce resource and is unmodellable, and the engine's real job would be re-planning silently every time reality diverges. The value is in the ordering, not the timing, and the ordering needs no engine.

#### B. Multi-recipe sessions — an extension to the reader

The requirement that cannot be dropped: **several recipes open at once, with free movement between them.** This is not orchestration. It is *presence* — each recipe holds its own place and its own running timers, and the cook chooses which one is on screen.

This preserves §1 rather than breaking it. The cook's place stays sacred; there are simply several places now, and the cook decides which they are standing in. Nothing competes for the screen, because nothing pushes them anywhere they did not choose to go.

**Settled 1 August 2026:**

- **Switching.** Tablet gets a tab strip — it is the primary posture and has the room. Phone gets a single button opening the list of recipes in the session. The phone does not pretend to have space it lacks.
- **Alarms.** When a timer fires in a recipe the cook is not looking at, the app takes them to it — the alarm exists to prevent a missed step, and making them navigate defeats it. **Return is one tap:** the banner that replaces the alarm names where they came from, and going back costs a single gesture. This keeps the one-mandatory-gesture principle intact and handles the case where the cook is mid-cut in another dish when the stock finishes.

Session-owned timers already exist in the prototype and already survive the recipe-to-cook transition. What changes is that a session holds several recipes rather than one.

#### Why this order

The document ships first because it is a report over data that already exists, it cannot be wrong, and it produces the large basket the pre-build validation sprint exists to measure. Multi-recipe sessions ship second because they change the reader, and the reader is the test instrument.

Full orchestration — a live plan tracking the cook's position across three dishes — stays out until someone has been watched using the document version. The working hypothesis is that a paper plan plus timers that refuse to let you forget covers most of it, and that the remainder is where the design becomes genuinely dangerous.

#### What blocks it

§16.7. Menu suggestion cannot be built without the tag vocabulary, and **tags are the expensive retrofit** — adding them at recipe 400 means revisiting 400 files. This is the same closed-vocabulary problem the lexicon solved in August 2026, and it should be settled before authoring reaches volume, not after.

---

## 14. Sub-recipes — SETTLED

A recipe may consume another: a tahini sauce, a dressing, a spice mix, a dough.

**The sub-recipe is a first-class recipe.** Its own file, its own steps, its own
yield, authored and test-cooked once. Never duplicated into the parent, so
fixing it fixes every dish that uses it.

**Referenced, with a quantity.** The parent declares `uses: [{id, amt}]` and the
sub-recipe declares `yield: {amount, unit}`. Everything scales by
`amt ÷ yield` — 150 ml taken from a 400 ml sauce buys 150 ml worth of its
ingredients, not a whole batch.

**Its ingredients roll into the parent's shopping list**, summed with the
parent's own by ingredient id. One consequence found in testing: `fixed`
ingredients scale on a roll-up share even though they do not scale with
servings. Water for boiling stays constant whether you cook for two or eight —
but 37.5% of a sauce genuinely contains 37.5% of its water. These are different
kinds of scaling and the builder now distinguishes them.

**Its allergens roll up too.** A tahini sauce cannot hide its sesame from a
parent's dietary tags. Derivation recurses, with cycle protection.

**In the reader it is a link.** A tile that opens the sub-recipe as a second
recipe in the session, with one-tap return — the same mechanism as §13's
multi-recipe sessions. Its steps are never spliced into the parent's flow: that
would defeat authoring it once, and would drop the cook somewhere they did not
choose to go, against §1.

The mid-flow case is rarer than it looks. A sub-recipe is usually made *before*
the parent is started, which means the cook meets it in the prep-ahead list
rather than mid-page.

---

## 15. The activity lexicon — SETTLED

The closed vocabulary of cooking verbs. A recipe refers to `chop` by key; the
word "chop" and its Arabic exist only in `content/lexicon/activities.yaml`.

**Why this shape.** It is the same argument as §5. Adding a language costs one
pass over the lexicon plus the handful of prose fields in each recipe — not five
hundred recipes' worth of vocabulary. It only holds if the vocabulary stays
small, because every entry is a word translated into every language ever shipped.

**When a verb earns an entry: the icon decides.** If you would draw the same
picture, it is one activity plus a qualifier, not two.

- *Chop fine* and *chop roughly* — one activity, `chop`, plus a qualifier.
- *Fry* and *sear* — two. Different pan, different heat, different picture, and
  a cook who confuses them ruins the dish.
- *"Pour over, listen for the hiss"* — neither. The phrasing is the teaching and
  it belongs to one recipe. A bespoke `verb:` on that tile.

Three routes, in order of preference: `do:` from the lexicon · `do:` plus
`qualifier:` · bespoke `verb:`. The validator counts bespoke verbs so drift stays
visible.

**The merge, 1 August 2026.** A 294-verb candidate list was reviewed and sorted:

- **81 activities** get an icon and a lexicon entry
- **124 verbs** render as an activity plus a qualifier — *julienne* is `slice`
  plus *matchsticks*
- **84 rows** were out of scope: beverages (no station in a reader with six),
  cleaning (a cook never sees it), testing (already handled as per-step doneness
  cues), and duplicate rows

The evidence for consolidating: 70 of the 185 distinct Egyptian entries were
multi-word phrases rather than verbs — `نزع القشرة` for *hull*, `شيل القلب` for
*core*. Dictionary glosses, not what a cook says at a stove, and they do not fit
a 44px tile. That is the clearest signal of which rows were reference material
rather than lexicon material.

**Dialects.** `ar` (Modern Standard), `ar_eg`, `ar_lv`, `ar_gulf`, resolved
`ar_gulf → ar_eg → ar`, so partial coverage degrades to a comprehensible word
rather than a blank. **Dialects are lexicon-only** — per-recipe prose stays in
`ar`, because dialectising ~5,000 prose strings is a second content project the
size of the first. Mixed register (dialect imperatives over standard descriptive
prose) is how Arabic cooking media already reads.

**Every verb must be distinct within each dialect.** Two activities sharing a
word put identical text on two different tiles, and a cook reading Arabic cannot
tell the steps apart however different the English keys look. This is an error,
not a warning. Eight were found and fixed during the merge — `toss`/`stir` in
Egyptian, `zest`/`peel` and `grill`/`roast` in Levantine and Gulf, `cool`/`chill`
in Gulf and MSA, `season`/`marinate` in MSA.

**What it unlocks.** Batched preparation across a menu (§13) groups tiles by
`(activity, ingredient, qualifier)`. With 294 separate verbs, *julienne* and
*slice* would group apart and produce fragmented prep instructions. Consolidated,
they group together — and the qualifier is exactly what distinguishes diced from
sliced onion when three recipes want one and the fourth wants the other.

**Ceiling.** 81 was settled deliberately. Past roughly 95, two entries probably
share an icon and should be merged.

---

## 16. Open questions

### 16.1 Discovery — PARTLY SETTLED (29 August 2026)
No philosophy established. 500 curated recipes with no duplicates means **browsing is the product** for the first ten minutes of anyone's relationship with Matbakh. This is where the curation promise reads either as confidence or as thinness.

The governing question differs from the reader's. The reader asks *how do I not break your concentration.* Discovery asks *how do I help you decide fast without pretending I know you.* These do not share a design logic and should not be forced to.

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

### 16.3 The meal planner — NOT STARTED
How it stays advisory without becoming nagging. Established constraint from prior work: non-rigid, non-mandatory, treats deviation as normal; hard rules apply only to dietary exclusions.

### 16.4 — retired, not missing
Entertaining and hosting was §13.4 here until 13 August 2026, when it was promoted to its own top-level **§13**. The number is left vacant deliberately: renumbering 16.5–16.7 would silently invalidate every cross-reference written since. If you arrived here looking for 16.4, you want **§13**.

### 16.5 Step granularity — PARTIALLY SETTLED
Working answer: granularity governed by **hands**, not grammar — a step ends when you next need to look at the screen. Section 4.1's order-independence rule operationalises this, but it has not yet been tested against real recipes at volume.

### 16.6 Doneness photography and the tile carrier — SCOPE OPEN, PINNED TO THE PILOT

*Revised 2 September 2026; previously “Doneness photography — SCOPE UNDECIDED”.*

The mechanism is settled (§5.2), and so is which surface owns what (§5.5). Two things are not, and both are now questions the pilot answers rather than arguments to be won on paper.

**Settled.** Doneness photographs are recipe-specific under every option, they carry the trust claim, and they are captured by the author while cooking — which is the only moment the state exists.

**Open, and deliberately not guessed at here.**

- **How many per recipe.** Not one per page: one per genuine decision point. `step-imagery-decision.md` §10 estimates **4–6**, against **8–14** for photo-per-page. That is an estimate, not a measurement — molokhia used doneness on 6 of 8 pages, and several of those were carrying the tile's job rather than their own. This figure is the multiplier on the largest content-cost line after the build, so **no number is recorded here until the pilot measures one.**
- **What the 44 px tile carries** — a static glyph (A), an animated glyph (A+), a glyph plus a per-recipe photograph (C), or a short silent loop from a shot-once library (E). `step-imagery-decision.md` recommends E and argues it well. It is a recommendation, not a finding, and it says so.

**How the pilot decides it, which is the point.** The pilot is already the shoot. The fifteen recipes are coverage-driven and will exercise most of the vocabulary whether or not a camera is running. Record for each tile whether the glyph was *sufficient*, whether it *needed motion*, or whether it *needed this specific dish* — roughly 150 judgements, and the only dataset on this question that will ever exist. The decision rules are already written and falsifiable: if **≥3 recipes** show a generic loop misleading because the ingredient changed the gesture, the action layer is not generic and the per-recipe options return; if **≥90%** of tiles read as glyph-sufficient, do not shoot at all.

**Recording this as open is itself the decision.** Choosing an option now would fix the largest content-cost line in the model on an argument, two weeks before the measurement that settles it exists.

### 16.7 Filters and dietary attributes — NOT STARTED, NOW ON THE CRITICAL PATH
Dietary requirements, personal preferences, heat, vegan/vegetarian, kids-suitable, weight-watching. The attributes are known; the interaction model is not.

**Raised in priority 1 August 2026.** §13 established that menu suggestion is blocked on this, and that tags are the one thing genuinely expensive to retrofit — every recipe authored before the vocabulary is settled has to be revisited. The vocabulary should be closed and small for the same reason the activity lexicon is: it is translated once, and it is what a filter can promise.

At minimum it needs cuisine, course, protein, spice level, dietary exclusion (*vegetarian as written*, not *could be made vegetarian*), effort, and whether a dish holds well — that last one only matters for entertaining, which is why it surfaced now.

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


---

## Decision log

| Date | Decision | Section |
|---|---|---|
| 24 Jul 2026 | Kitchen instrument, not recipe app — the stance | 1 |
| 24 Jul 2026 | Three pillars are asymmetric; method/cost/nutrition get different surfaces | 2 |
| 24 Jul 2026 | Five core principles + two structural commitments | 3 |
| 24 Jul 2026 | Order-independence governs page grouping; 6–10 typical, 14 ceiling | 4.1 |
| 24 Jul 2026 | Implicit tile state with explicit override | 4.3 |
| 24 Jul 2026 | Map: one screen, icon-cluster thumbnails, three dim states, preserves position | 4.4 |
| 24 Jul 2026 | Tap replaces hover; tile is the tap target | 4.5 |
| 24 Jul 2026 | Timers belong to session; persistent running band expresses parallelism | 4.6 |
| 24 Jul 2026 | Resume-or-restart prompt; no auto-expiry | 4.7 |
| 24 Jul 2026 | Three carriers: icons / digits / words | 5.1 |
| 24 Jul 2026 | Doneness → photo; heat → ordinal glyph; *to taste* stays words | 5.2 |
| 24 Jul 2026 | Western Arabic numerals as default | 5.3 |
| 24 Jul 2026 | Digits are a live text layer, never baked into artwork | 5.4 |
| 24 Jul 2026 | Four scale classes, line-level override | 6.2 |
| 24 Jul 2026 | Rounding ladder + ≈ marker | 6.3 |
| 24 Jul 2026 | Serving presets derived at authoring time; no free slider | 6.4 |
| 24 Jul 2026 | `max_scale_factor` + batch-cooking glyph | 6.5 |
| 24 Jul 2026 | Exact / Displayed / Purchase — cost from exact only | 6.7 |
| 24 Jul 2026 | Technique video removed from cook mode into a Techniques library | 7 |
| 24 Jul 2026 | Feedback is telemetry, never published | 8 |
| 30 Jul 2026 | No music-app integration; alarm must carry unaided | 12 |
| 1 Aug 2026 | Party plan is a document; multi-recipe sessions are a reader change; no scheduler | 13 |
| 1 Aug 2026 | Alarm jumps to the recipe, return costs one tap | 13 |
| 1 Aug 2026 | Tab strip on tablet, single button on phone | 13 |
| 1 Aug 2026 | Sub-recipes: referenced not embedded, scaled by yield, shown as a link | 14 |
| 1 Aug 2026 | Lexicon: 294 verbs → 81 activities, 124 qualifiers, 84 out of scope | 15 |
| 1 Aug 2026 | Three Arabic dialects, lexicon-only, prose stays in ar | 15 |
| 1 Aug 2026 | §11 reconciled against the built schema; July field names never existed | 11 |
| 13 Aug 2026 | **Renumbered.** Open questions §13 → §16. Entertaining and hosting promoted from §13.4 to its own top-level §13. §16.4 left deliberately vacant rather than reused — renumbering 16.5–16.7 would silently invalidate every cross-reference written since. Anything written before this date cites the old numbers. | 13, 16 |
| 15 Aug 2026 | **§11 status advanced** — schema fields moved from *to lock before authoring begins* to *SETTLED, and now implemented*. The validator enforces them; they are no longer a specification awaiting code. | 11 |
| 15 Aug 2026 | **Activity lexicon — SETTLED.** A recipe refers to an activity by key; the word and its Arabic live only in `activities.yaml`. 81 activities, ceiling ~95. Dialects are lexicon-only, resolving `ar_gulf → ar_eg → ar`; per-recipe prose stays in `ar`. Two activities sharing a word within one dialect is an error, not a warning. | 15 |
| 29 Aug 2026 | Units display as authored; no computed conversion | 6.7, 11 |
| 29 Aug 2026 | `why` is a required, load-bearing field with an editorial cost | 9 |
| 29 Aug 2026 | Ingredient-led entry settled as a discovery route; presence not quantity; does not block on tags | 16.1 |
| 29 Aug 2026 | Bolognese prototype's cost and nutrition placement written back | 16.2 |
| 29 Aug 2026 | Cost on browse card: owners see it, sample set for everyone, blurred server-side otherwise | 16.2 |
| 29 Aug 2026 | Weekly market price list free perpetually; dish cost paid; commitment is one-way | 17 |
| 29 Aug 2026 | Palate adjustment as multipliers, auto-applied and marked, flowing through, components propagating | 18 |
| 2 Sep 2026 | **Four surfaces settled, and what each one's cost scales with.** The arc is glyphs and can be nothing else; the doneness photograph is recipe-specific and carries the trust claim; prose is generated at build. The 44 px tile is the only open carrier | 5.5, 16.6 |
| 2 Sep 2026 | Doneness count and tile carrier **left open and pinned to the pilot** rather than settled on paper. No per-recipe figure recorded until one is measured — it is the multiplier on the largest cost line after the build | 16.6 |