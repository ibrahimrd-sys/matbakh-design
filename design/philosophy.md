# Matbakh — App Design Philosophy

**Status:** Living document. Sections marked SETTLED are decided and should not be relitigated without a stated reason. Sections marked OPEN are unresolved.

**Last updated:** 2026-09-24

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

### 16.7 Filters and dietary attributes — VOCABULARY SETTLED (24 September 2026); INTERACTION MODEL OPEN
Dietary requirements, personal preferences, heat, vegan/vegetarian, kids-suitable, weight-watching. The attributes are known; the interaction model is not.

**The vocabulary half is closed — see §26** (PM-07, 24 September 2026): nine authored fields, eight derived tags. **The interaction model — how filters compose in the interface — remains open**, which is the distinction this section has drawn from the start.

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


## 19. The recipe box — SETTLED IN PART (3 September 2026)

A cook may save a recipe to a recipe box. It is an explicit action, in the same
register as the rest of the product: the Profile is stated and never inferred,
the planner remembers and never predicts, and a save is the same shape. Nothing
enters the box by being cooked, viewed or searched for.

### 19.1 Storage rides platform device backup — SETTLED

The box is held on the device and carried between devices by the platform's own
backup — iCloud on iOS, Google Backup on Android. There is no Matbakh account,
no sync server, and no real-time cross-device sync.

Two alternatives were considered and rejected.

- **Pure local-only**, the planner's existing pattern. Rejected because the box
  is a list the cook builds by hand over months, and losing it to a reinstall or
  a new phone is the one failure that makes saving not worth doing. The planner
  survives that failure because it can rebuild from cook history; a box has
  nothing to rebuild from.
- **Account-backed sync.** Rejected because it requires account infrastructure
  the product does not otherwise have. Sign-up, recovery, session handling and a
  server holding user data are a workstream rather than a feature, and founder
  capacity is the binding constraint on everything (R-06). An account may later
  arrive for entitlement reasons; the recipe box is not what should summon it.

**What this buys is restore-on-reinstall, not sync.** Two devices signed into the
same platform account do not converge, and what comes back is whatever the
platform last backed up. That is the honest description of the mechanism, and it
is what the interface must say. Never the word *synced*.

**It assumes a platform-packaged app.** iCloud and Google Backup are native
mechanisms and a web reader has neither, so this decision carries a dependency on
the platform decision (E-01, not started) and must be revisited if that lands on
web.

**It is also the first user data to leave the device.** The planner is local-only
by design, which is part of what makes the privacy position cheap to hold
(L-06). A saved list riding platform backup is a deliberate, narrow departure
from that — a list of recipe ids, held under the cook's own platform account,
never Matbakh's — and it should be described that way rather than quietly folded
into the local-only claim.

### 19.2 Whether the box feeds the planner — OPEN

`suggest_home` splits DUE from UNTRIED on cook history alone. A saved recipe is a
third signal — *wants to cook*, as against *has cooked* — and it is wired
nowhere. Favourite **ingredients** feeding the planner is accepted (KS-02);
favourite **recipes** is not, and the two are not the same claim.

This half is not decided here. It belongs to the planner framing question
(PM-11), and it cannot be tested before the tag vocabulary lands and there are
recipes to plan over (§16.7). Recording it as open rather than letting it
default: *remembers, never predicts* is a stated promise, and a save quietly
becoming a prediction input is the exact drift that promise exists to prevent.


---

## 20. The Cut Library — SETTLED IN PART (5 September 2026)

A cut is a property of a **technique**, not of a recipe. The same butterflied
breast or halved-crosswise tenderloin is visually identical in every dish it
appears in, so a photograph of it is worth making once and referring to N times.
That is the whole of this section.

### 20.1 Cuts are shot once and referenced — SETTLED

Tight "cut identity" photographs are produced **once per distinct cut-state**,
held in a reusable **Cut Library keyed to the activity lexicon**, and referenced
by recipes. They are not re-shot per recipe.

Each cut photograph is tagged to the lexicon entry (§15) it depicts, so the
correct shot resolves wherever that technique appears — in any recipe, and in
any dialect variant, because the key is the activity and not the word.

**Why this and not per-recipe cut shots.** Per-recipe shots pay repeatedly to
photograph the same object. Shooting each cut once moves cut photography off the
column that scales with the **catalogue** and onto the one that scales with the
**vocabulary** — which §5.5 already names as the entire economic question, in
those words. It is the same argument `asset-spec.md` opens with — *an asset that
carries no words is made once* — and the same reason the activity lexicon and the
ingredient reference exist at all. This is not a new idea. It is the idea Matbakh
is already built on, applied to cuts.

**Portability is part of the rationale, not a bonus.** A cut frame is the
tightest, most food-only image in the system: a board and a technique, no plated
dish, no kitchen, no cultural furniture. It therefore crosses every locale with
**zero re-shooting**. That draws a clean line between the *universal* image
assets (cuts) and the *locale-bound* ones (mise en place, plated hero), and it
supports the adaptability position of §10 rather than eroding it.

**Schema fit is the second half of the rationale.** The lexicon is already a
controlled vocabulary of techniques; the Cut Library is its **visual
counterpart** — the same closed set, photographed instead of named. It therefore
lands as a resolved layer of the existing schema rather than as a folder of
images sitting beside it.

**The division of labour from §5.2 holds at this level too: the photograph
carries cut identity, the digit carries quantity and dimension.** No photograph
is relied on to convey proportion or size, and quantities label each ingredient
regardless of any photograph. A library shot answers *what cut*. It does not
answer *what size*, and must not be asked to.

**The per-recipe default is board-as-orientation.** One wide mise en place —
here is everything, prepped — plus at most one tight shot for the single hardest
or least-obvious cut in that recipe, drawn from the Cut Library where the cut
already exists there.

### 20.2 Scope, granularity, scale reference and board sufficiency — OPEN

Four things are deliberately not settled here, and none of them may be defaulted
into by starting the shoot.

- **Scope of the head set, and granularity of the key.** The library is scoped
  from the recipe corpus rather than from intuition: mine the catalogue for
  distinct cut-states, rank by frequency, shoot in frequency order. And the key
  cannot be the word alone — *sliced* onion for a salad is thin rings, *sliced*
  onion for a braise is thick half-moons, and they are not the same photograph.
  The key must be **word + parameter**. How many parameter values are held is
  what decides whether the library is ~30 shots or ~130, so it is settled before
  anything is shot rather than discovered during. Both sit under **PM-12**.
- **The scale reference.** Where dimension matters the recipe-level digit
  carries it, and the mechanism already exists — `cut: brunoise` with
  `cut_mm: 2` replaced the old `qualifier: fine`. What is owed is confirming that
  the labelling convention extends from quantity to dimension. That belongs in
  the cut lexicon's governing note (**C-09**), which is owed regardless.
- **Whether the board shot can also instruct.** If a cook reproduces a hard cut
  from the wide board shot alone, the extra tight shot can be dropped for that
  recipe. This is a measurement rather than a judgement, and the pilot is already
  the shoot — it is a cut-coverage judgement in the pilot tracker (**C-06**),
  recorded the way the tile judgements already are.

**The test that settles them is one afternoon.** Shoot the five or six
highest-frequency cuts, then take the first ten recipes and count how many are
fully cut-covered by that head set alone — library references plus quantity
labels, no bespoke shot. **Eight of ten** and the library carries the catalogue,
with per-recipe cut shots the rare exception already planned for; **around four
of ten** and the tail is fatter than it looks, which sends scope and granularity
back for revision before anything is scheduled. Separately, hand a cook the wide
board shot alone for one recipe with a non-obvious cut and see whether they
reproduce it.

**Recording these as open is itself the decision**, on the same reasoning as
§16.6. Granularity is a four-fold swing on a photography line that is shot once
and then lived with, and choosing it now would fix that line on an argument two
weeks before the afternoon of measurement that would settle it.


---

## 21. The Utensils Library — SETTLED IN PART (5 September 2026)

A utensil is a property of a **kitchen** — not of a technique, and not of a
dish. That single line does most of the work in this section, because the
column a cost lands in is decided by what it varies with, and §5.5 already
names that as the whole economic question.

### 21.1 What is settled

**Utensils are a first-class reference layer**, parallel to the ingredient
reference: what equipment a recipe requires is a fact about the recipe, and the
product needs to hold it. Its first job is the pre-commit surface (§16.2) —
committing to a dish and discovering at the bench that it needs a blender you
do not own is the failure that surface exists to prevent — and its second is as
a filter (§16.7).

**It is three features, not one, and they ship in this order.** The split
matters more than anything else here, on the same reasoning as §13:

1. **The requirement.** What equipment a recipe needs. A reference table and a
   field. Settled here.
2. **The visual carrier.** Whether a utensil is ever *shown*, and by what.
   Open — see §21.2.
3. **Substitution guidance.** *No stand mixer; here is what that costs you.*
   This is cooking knowledge and irreducible judgement, so by §5.1 it is words,
   authored per recipe, and it carries an editorial cost that is not in the
   per-recipe production model — the same trap §9 records for `why`. Open, and
   deliberately last.

**Utensils are locale-bound, and this is the decision that matters.** §20
admits the Cut Library partly on portability: a cut frame is the most food-only
image in the system — a board and a technique, no plated dish, no kitchen, no
cultural furniture — so it crosses every locale with zero re-shooting. **A
utensil is nothing but cultural furniture.** A pot in an Egyptian kitchen is not
a Dutch oven; a tagine, a baladi oven and a mehmas have nothing to travel to.
The argument that makes cuts *universal* therefore **inverts** here, and it
inverts rather than merely weakening: utensils belong in the **locale-bound**
column with mise en place and the plated hero, not in the universal column with
cuts. A utensils layer does not amortise across locales, and §10's caveat
applies to it in full — the interface is portable, the furniture is not.

**The division of labour holds a third time.** The picture carries **tool
identity**; words and digits carry **size, capacity and substitution**. No
photograph conveys *26 cm*, and none should be asked to — the same rule §20.1
states for cuts and §5.2 states for quantity.

**Presence, not inventory.** A cook may mark that they have a blender; never
that they have a 700 W jug blender. This is §16.1's constraint carried over
unchanged, for the same reason — every product that has asked users to maintain
an inventory has died on the maintenance burden. Staples are assumed present
and unset rather than set: a knife, a board, one pot, one pan.

### 21.2 The visual layer, the scope, and authored-vs-derived — OPEN

Four things are deliberately not settled, and the fourth changes what the
question is, so it is resolved first.

- **Whether a visual layer exists at all, and what carries it.** It cannot be
  settled ahead of **PM-09**: the tile is 44 px and already has one open
  carrier competing for it. A utensil shown *as well as* an act is a second
  thing in the same square, and §3's *one mandatory gesture* and §4.4's
  squint test both bear on that. Sequenced behind PM-09, not beside it.
- **Scope and granularity.** Is `pot` one entry or five? This is the same
  four-fold swing **PM-12** carries for cuts, and it takes the same answer:
  mine the corpus for distinct requirements and rank by frequency rather than
  scoping from intuition.
- **Authored or derived.** §11's test is *could a careful person disagree?* —
  and mostly they could not, since a recipe either uses a blender or it does
  not, which argues **derived**. But nothing in the tile currently names a
  tool, so there is nothing to derive *from*: either tiles gain a `tool:`
  field or the recipe carries an authored `equipment:` list. That is a schema
  decision, and it is the expensive kind to retrofit for exactly the reason
  §16.7 gives about tags — every recipe authored before it is settled has to
  be revisited.
- **The measured finding that has to be resolved first.** **24 of the 81
  activities — 23 distinct glyph values — already draw a tool, vessel or
  appliance rather than the act.** `grate` is a grater, `sift` a sieve, `peel`
  a peeler, `blend` a blender, `skim` a spoon, `simmer` a pot, `stir_fry` a
  wok. That is four times the six ingredient-drawing activities **C-05**
  already tracks as a defect against `asset-spec.md`'s *draw the action, not
  the ingredient*. It reads two ways and they lead in opposite directions:
  either it is that same defect at four times the scale, or **utensil-as-
  carrier is already the de facto answer** for the instrument-defined verbs
  and should be made deliberate rather than left accidental. It is currently
  neither, which is the worst of the three. Folded into **C-05**.

  *(The counts are generated from `content/lexicon/activities.yaml`; the
  classification of what a glyph depicts is judgement, on the same footing as
  the Class M / Class S split, and should be contested as the icons are
  reviewed.)*

**How this gets measured, rather than argued.** The pilot is already the
instrument. Record per tile whether the utensil needed to be shown at all, and
whether the activity glyph was already showing it — the same near-zero marginal
cost as the `Tile judgements` tab, on recipes that are being cooked anyway.
Folded into **C-06**.

**Recording these as open is itself the decision**, on the same reasoning as
§16.6 and §20.2. The carrier question in particular would, if answered now,
pre-empt a 44 px square that a measurement two weeks out is about to settle.

### 21.3 Amendment, 5 September 2026 — the list is taken, the repetition is not

Settled the day §21 was written, against the Kitchen Stories instruction-layer
reading (`02-strategy/competitor-study-part-five.md`).

**The per-recipe equipment list is confirmed as the shape**, with an `optional`
flag per entry — the pre-commit check must not warn a cook off a dish over a
grater they could work around.

**There is no separate per-step equipment surface.** Where a tool matters, it is
already showing in that step's own photograph or icon. Kitchen Stories restates
tools at every step because it has four fat steps, no station concept, and a
cook who would otherwise scroll back to the top; Matbakh has **six stations**
naming where the cook stands and a per-recipe list that has already said what to
get out. The repetition earns less here than it does there.

**This narrows §21.2's first open item without closing C-05.** The measured
finding — 24 of 81 activities draw a tool rather than the act — was recorded as
reading two ways. This decision leans on the second: for the instrument-defined
verbs the utensil is *already on the tile*, and a second surface would draw it
twice. C-05 stays open, because the glyph must still draw the **action** wherever
the action is what distinguishes it from a neighbour. What is now closed is the
narrower question of whether equipment gets a surface of its own per step. It
does not.

**One case the pilot should watch, recorded rather than argued:** a step where
**two vessels are in play at one station** — a pan and a pot on the stove
together — and neither the act glyph nor the station header says which the tile
means. If it shows up in the fifteen it is a layout question, not grounds to
reopen this. **C-06.**


---

## 22. Ingredient substitutes for costing — SETTLED IN PART (16 September 2026)

Recipes carry an **explicit substitute list per ingredient**, and every
substitute is tagged either **cost-only** or **changes-the-cook**. Only cost-only
substitutes are swappable in the app, with the recipe cost recomputing live.
Changes-the-cook substitutes are shown as information, with a prose note on the
steps they affect — not swappable in this version.

**Why this version.** Meat cuts and fish species cannot be priced by averaging.
*Beef* spans a two- to four-fold range across cuts, and fish species are not
interchangeable in cost or in cook behaviour. The recipe already names the
best-fit cut or species for its method; substitutes exist so that cost can vary
without the primary ingredient's identity being blurred into a range. Splitting
cost-only from changes-the-cook keeps that honest: a cut swap in a braise is
usually just a price change, a fish-species swap usually is not — thickness and
timing shift, and the doneness photograph (§16.6) was authored for the primary
species specifically. It also keeps cook mode's wordless default intact: prose
appears only once a cook actively selects a changes-the-cook substitute, never
on the baseline path.

### 22.1 What is DECIDED

- **The primary ingredient is the cut or species the steps, timer and doneness
  photograph were authored against.**
- **Substitutes are an explicit authored list** — never inferred, and never
  averaged from price data.
- **Each substitute is tagged cost-only or changes-the-cook.**
- **Cost-only substitutes are swappable in-app**, and the recipe cost
  recomputes live.
- **Changes-the-cook substitutes are informational only** — *with X instead:
  from Y EGP* — plus a prose note on which steps are affected. Not swappable in
  this version.
- **The prose note is scoped to the substitute-selection moment.** It does not
  appear anywhere in baseline cook mode.

### 22.2 What is OPEN — PM-15

- **Whether changes-the-cook substitutes become swappable later** — each with
  its own timer and doneness cue, and possibly its own photograph. Costed
  against the doneness-photograph economics once they are known per recipe, the
  same line `step-imagery-decision.md` and §16.6 carry.
- **Whether the pilot's fifteen recipes need to exercise changes-the-cook
  substitutes**, or whether that waits until doneness-photograph cost per recipe
  is known. Instrument: the pilot cook-through — flag any recipe that naturally
  needs one (**C-06**).
- **The reference-species convention for fish costing** — which species the
  recipe's method and timing were written for, stated explicitly. There is no
  governing document for it yet: the same shape of gap as the Cut Library's
  (§20, D-13), and cut-level substitutes cannot be authored at volume until
  that one exists.

**The validation test, stated in advance.** If any substitute logged during the
pilot as cost-only turns out to shift a step's timing or doneness cue, the
cost-only / changes-the-cook split has failed and is reworked before authoring
scales past the pilot.


---

## 23. The cooking log — SETTLED (18 September 2026)

A cook gets a plain, chronological record of the dishes they have finished —
recipe and date, nothing else — surfaced in Profile. It describes what happened.
It asks for nothing.

The data already exists and is already trusted: the planner computes
`times_cooked()` and `last_cooked()` per recipe, and `suggest_home` splits DUE
from UNTRIED on that history alone (§19.2). The log is that same record shown to
the cook directly, rather than read only as a ranking signal.

### 23.1 Completions only

An entry is written when the cook finishes — the last page turn in cook mode,
which the prototypes already label **Finish** / *خلصنا*. Reaching the final page
without taking it, or walking away partway, writes nothing.

### 23.2 Abandonment is tracked, but not shown here

§4.7 and §8 both record that the app has good reason to know how often cooks
abandon and on which page — §8 calls it the most valuable signal available. That
is telemetry for the editor. **It is deliberately not surfaced to the cook in
this version**, and the line is drawn here so that a later reader finds a scope
decision rather than an omission.

### 23.3 Not a streak

A streak — a consecutive-day counter that resets on a miss — is a pressure
mechanic even when it is displayed honestly, because the number's whole job is to
make you not want it to drop. That is the aggregate-behaviour optimisation §8
declines. A plain log has nothing to protect and nothing that resets.

### 23.4 It lives in Profile, not in the recipe box

The recipe box (§19) is an **explicit** save: nothing enters it by being cooked,
viewed or searched for. The cooking log is the opposite mechanism — implicit, and
written by the act of cooking. Folding one into the other would blur a
distinction §19 was drawn to make, so the log sits in Profile rather than as a
tab inside the box.

### 23.5 `recall_menu` is the entertaining-specific view of this

The planner's `recall_menu()` re-opens a saved menu at a new headcount, and the
saved-menu list already tells a host *you served this 3 times, last 47 days ago*.
That is this same mechanism scoped to menus rather than to single recipes.
Recording it as one mechanism with two views, rather than two parallel ones,
costs nothing today and prevents them drifting apart later. **No behaviour in
§13 changes.**

### 23.6 Deferred: if abandonment is ever surfaced, it records *why*

Should a later version show abandonment to the cook, a bare count — *you did not
finish this 3 times* — is judgemental without being useful. The reason is what
would make a cook's own record worth reading: the phone rang, an ingredient ran
out, it took too long, they did not like it. Recorded now as a constraint on that
future decision, not as something being built.


---

## 24. Course-weighted serving for the party plan — SETTLED IN PART (18 September 2026)

The party plan (§13) computes each dish's quantity from an **effective covers**
figure rather than from the guest count directly. Effective covers is a share of
a per-course consumption target, divided across the dishes sharing that course,
weighted per dish by the cook for that event. The result is fed into §6's
existing scaling mechanism unchanged.

**Why this version.** The planner currently scales every dish to the full guest
count, as though each dish were the only thing on the table — `cost = sum(r["cost"]
* covers for r in m)` appears twice in `plan_event()`, and the same per-dish
`r["cost"] * covers` at three more sites, one of them in `recall_menu()`. Six
dishes for ten guests therefore price six full ten-person portions, and the
consolidated shopping list inherits the same arithmetic. Nobody eats six full
servings in one sitting, and catering practice runs the other way: the more
dishes share a course, the less of each a guest takes. **This is a capability
being added, not a defect being repaired** — nothing in this document or in
`planner/README.md` ever promised multi-dish discounting, so the code is not
departing from a stated rule.

**It is built on what exists.** §6 already has a tested scaling mechanism — the
four classes, `max_scale_factor`, the rounding ladder, the presets — and this
changes only the number fed *into* it. The grouping key is the `course` tag,
which is where the real dependency lies: see the open half.

**Per-dish weight belongs to the event, not the recipe.** The same dish is the
anchor at one party and an accent at another, depending on what else is served.
`course` is a fact about the dish and belongs on the recipe; weight is a fact
about the evening and does not.

**The cook's coefficient is free-form judgement, and deliberately unstructured.**
The app does not ask *why* a number is being adjusted — a light gathering, drinks
involved, a hungry family. Named event profiles and a drinks toggle were both
considered and rejected: either would have the app modelling a judgement that is
the cook's to make. This follows §19's rule that the Profile is **stated and
never inferred**.

### 24.1 What is DECIDED

- **Per-guest consumption targets exist per course**, as one global reference
  table, grouped by the `course` tag.
- **Within a course holding more than one dish, the target is divided by a
  weighted split**, not an even one. The weight is set by the cook **per event**
  and is never written back to the recipe.
- **The targets are adjustable as a standing Profile preference** — per course
  individually, or by one coefficient across the whole table.
- **That coefficient may be overridden for a single event**, as free judgement
  with no structured inputs.
- **The output is an effective-covers figure per dish**, fed into §6's existing
  scaling class and `max_scale_factor`. No second scaling system.

### 24.2 What is OPEN — PM-16, and one blocker that is not PM-16

**The blocker first: `course` is not an authored tag yet.** It is proposed in
`design/tag-proposal.md` (a draft of 1 August, closed list) and §11 still records
`tags` as *not yet settled*. No recipe carries a `tags:` block — none of the
sixteen in the catalogue — and the only live use is the validator's check that a
*sub-recipe* is tagged `component`, `sauce` or `dip`. So the grouping key this
mechanism needs does not exist on any recipe today. **This is blocked on PM-07**,
and on the retrofit R-10 tracks, in exactly the way §13's menu suggestion already
is. Nothing here can compute before that lands.

Three questions are open in their own right, under **PM-16**:

- **The course-target numbers themselves** — grams or millilitres per guest, per
  course. Pending Ibrahim's own catering research and **deliberately not invented
  as placeholders**, on the same reasoning §16.6 gives for the doneness count: a
  number recorded before it is measured gets quoted back as though it were.
- **The default split when a course holds several dishes and the cook has set no
  weight.** An even split is the obvious fallback, but it is not yet decided, and
  without a stated default the mechanism cannot compute unattended.
- **Whether `drink`, `soup` and the other rarely-multiplied courses take part in
  this at all.** Best settled alongside the reference numbers rather than now.

**What to watch once the party plan is used in anger.** If dishes routinely go
unweighted and the even-split default produces implausible quantities, that is
evidence against the **default**, not against the mechanism — and it is the
default that should be revisited.


---

## 25. Monetisation model reversed — SETTLED (20 September 2026)

*Recorded as an addendum, per append-never-insert: it supersedes §17 without
editing it, and §17 still reads SETTLED. **D-1** is the competitor study's ID
for the decision §17 records — this file has no D-1 entry of its own.*

## Addendum — 20 Sept 2026: Monetisation model reversed

D-1 (settled 29 Aug) read: catalogue paid, prices free. This is reversed.

**New decision, settled 20 Sept 2026:** free catalogue, paid premium
features. The original D-1 entry above stays in place per this file's
append-never-insert convention — this addendum supersedes it rather than
editing it out.

This is a structural reversal, not an addition, and it has not yet been
checked against everything that assumed D-1's original shape. Flagged here,
not resolved:

- The marketing recommendation's "instrument you buy, not a service you
  rent" positioning (competitor-study.md, Recommendation section) was built
  on catalogue ownership as the headline claim. Needs review.
- T-02's settled wording — "visible to owners" — presumed a purchase event
  gating the feature. Needs reconciling with a free catalogue.
- Axis 7 monetisation-response arguments across the competitor study
  (particularly the Kitchen Stories and NYT Cooking entries) were framed
  as contrasts against a one-time-purchase model. Those comparisons now
  need re-reading in light of the reversal — Kitchen Stories in particular
  is no longer a contrast case but the closer analogue.
- M-02 ("Monetisation model — final base case") was already logged NS
  (not settled) before this reversal. This addendum fixes the shape
  of the model; the numeric base case is still open and unaffected by
  this entry.

---

## 26. Recipe tag vocabulary — SETTLED (24 September 2026)

**PM-07 is closed.** The vocabulary that §16.7 has waited on since 1 August is
final. `design/tag-proposal.md` carries the full reasoning and is now
historical; this section is the decision.

**Nine authored fields, all editorial judgement:**

| Field | Values |
|---|---|
| `cuisine` | one, closed: `egyptian · levantine · gulf · north_african · turkish · persian · italian · french · chinese · indian · american · mexican · japanese · greek · spanish · thai · latin_american · eastern_european` |
| `course` | one, closed: `main · side · salad · soup · bread · sauce · dip · pickle · dessert · breakfast · drink · component` |
| `main_protein` | one, closed: `beef · poultry · seafood · pork · vegetarian · mixed · none` — **new at closure** |
| `spice` | `0` none · `1` warm · `2` noticeably hot · `3` hot |
| `effort` | `easy · moderate · involved` |
| `holds` | `serve_immediately · warm · room · cold · better_next_day` |
| `season` | zero or more: `summer · winter · spring · autumn`; omit for year-round |
| `occasion` | zero or more, closed: `everyday · guests · ramadan · eid · siami_seafood · siami_no_seafood · celebration · picnic · make_ahead_meal` |
| `contains_override` | rare, free text; **every use auto-flagged for validator review** |

**Eight derived tags, never authored**, unchanged from the draft: `contains`,
`vegetarian`, `vegan`, `gluten_free`, `total_minutes`, `stations`,
`cost_per_serving`, `kcal_per_serving`.

**Three things the closure decided, beyond confirming the draft.**

1. **`main_protein` is authored, not derived.** It is the dish's claim, not its
   ingredient list: a soup carrying a spoonful of stock is not a poultry dish,
   and `contains: poultry` cannot tell the difference.
2. **`siami` splits in two** — `siami_seafood` for the Nativity Fast, which
   permits seafood, and `siami_no_seafood` for Great Lent, which does not. A
   `siami_no_seafood` dish will generally also be derived `vegan`; a
   `siami_seafood` dish will not, because it contains fish, yet it still
   excludes meat, poultry and dairy. **No single derived tag captures that
   combination**, which is why the occasion tag earns its place here.
3. **`hidden` is removed.** `course: component` already keeps sub-recipes out of
   suggestion, and an unfinished recipe does not belong in the authored
   catalogue at all. A third mechanism was redundant.

**What this does not settle.** §16.7 separates the vocabulary from **how filters
compose in the interface**, and only the vocabulary is closed here — the
interaction model stays open. **S-07**, the translation layer for derived tag
keys (`contains` renders its English keys even in the Arabic build), is a
separate open item and is untouched. `main_protein` is a new field in the
authored schema: the recipe schema, `matbakh.py check` and
`authoring-standard.md` do not know about it yet.

---

## 27. The monetisation fork resolved — SETTLED (24 September 2026)

*A further addendum, per append-never-insert. It does not edit §25, the 20 Sept
D-1 reversal, which stays as written; this settles what "premium" contains and
what the retail layer is. **M-01**, **M-02** and **M-03** are the PM log's
commercial IDs (§6's **PM-02** and **PM-03**); **D-1** and **D-4** are the
competitor study's.*

## Addendum — 24 Sept 2026: M-01/M-02/M-03 resolved

Following the 20 Sept D-1 reversal (free catalogue, paid premium features),
the shape of "premium" and the retail-layer strategy are now decided
together, as one coherent set rather than three separate forks.

**M-01 (PM-02) — build-to-own vs build-to-be-bought: DECIDED — build-to-own,
Kurashiru-shaped.** Not exclusivity with a single retailer (the Walmart/Tasty
pattern the study calls a trap), but the retail-media pattern: audience first,
retail relationship second, non-exclusive by construction. This resolves
PM-02.

**D-1, refined — the exact free/paid boundary:**
- Raw weekly market prices — staples, named market, named date — **free,
  forever.** This is the acquisition engine (NY-01, ACCEPTED 29 Aug, marked
  irreversible) and stays exactly as settled — nothing about this addendum
  reopens it.
- The computed cost of a specific dish, and the planner's costed,
  consolidated week — **premium.** This is what "paid premium features"
  in the 20 Sept D-1 reversal concretely means. Free is the raw data;
  premium is the data applied to a dish or a week.

**M-03 (D-4) — Layer 3: CONFIRMED as re-specified retail media**, per the
existing REOPENS recommendation — non-exclusive, multiple retailers, a
referral fee once a retail partnership is agreed. The exact deal
mechanic (flat referral vs. Kurashiru's points-back-to-shopper vs. a
volume-tiered structure) is deliberately NOT decided here — it depends on
actual negotiation with a real retailer and is tracked separately as
negotiation-prep material, not a settled decision, in
`matbakh-private/02-strategy/referral-fee-variances.md` *(pointer added
24 September 2026, when that file was written; the decision is unchanged)*.

**Benchmark on record for any referral-fee modelling:** grocery affiliate
commissions run ~3% (Instacart 3%, Kroger 1.6–4.8%, Ocado 3%) — corrected
from an earlier, overstated 5% figure already flagged once in this project's
own documents. Model against 3%, not 5%.

**T-05 (substitution at the grocery handoff)** stays DEFER — this addendum
does not change that. It remains blocked on the actual mechanics of M-03,
which now have a shape (referral-fee-based, non-exclusive) but not yet
concrete terms.

---

## 28. Substitution scope and mechanism — SETTLED IN PART (24 September 2026)

*A further addendum, per append-never-insert. It stacks after §26 and §27 and
edits neither, and it does not edit §22: **§22.2's open list is superseded on
the swappability question only**, and PM-15's other items stay open there.*

## Addendum — 24 Sept 2026: PM-15 resolved — substitution scope and mechanism

PM-15 (opened 16 Sept) is now resolved on the swappability question.

**Substitutes are shopping-list-only. They never enter the instruction
set.** Recipe steps, technique, and authored timers remain exactly as
test-cooked — consistent with §6.1 and §5 (availability-draft.md's
existing rejection of auto-substitution).

**Mechanism: a rules table**, keyed by (original, substitute) pairs —
e.g. beef cut sirloin → cutlet — each carrying a consistent effect (a
suggested timer adjustment). Upgrades D-15's "informational prose note"
into a structured, reusable table.

**Two tiers, both shopping-list-only:**
- **Packaged goods** (e.g. spaghetti): brand/quality tiers — Class C
  local, Class A local, imported — shown side by side on the shopping
  list. No cooking impact. The recipe's displayed cost_per_serving is
  pinned to ONE canonical tier (Class A), not an average or the cheapest.
- **Protein** (fish fillet type, beef cut): substitute options with an
  attached rule. Selecting one on the shopping list surfaces a suggested
  timer adjustment in cook mode.

**The suggested timer adjustment is auto-applied but visibly flagged —
never silently identical to the tested original.** Cook mode shows the
adjusted duration distinctly (e.g. "25 min — adjusted for cutlet, tap
to confirm or edit"). Preserves "the derivation is stated as such"
(§6.1); keeps the cook's judgement in the loop on a food-safety-relevant
adjustment. The cook can manually override the suggested value — it's a
one-tap default, not a forced change.

**New UI scope:** editing a timer's duration mid-session. Log under
E-06 as new scope.

**Left explicitly open:**
- Whether one rules table covers both cuts and species, or two systems
- Whether the packaged-goods tier layer becomes its own governing
  document (parallel to D-13/D-14) or stays an informal add-on
- Whether the protein substitution table relates to or extends D-13's
  Cut Library, given PM-12's own open scope question

---

## 29. Pricing data sourcing — SETTLED IN PART (24 September 2026)

*A further addendum, per append-never-insert. Its own topic, stacked after §28
and merged into nothing. The facts about the portal are recorded as stated by
Ibrahim; this file has not independently verified them.*

## Addendum — 24 Sept 2026: Pricing data sourcing — P-01 updated, new indicative-pricing scope opened

P-01 status changes from "NS — HIGH RISK, no contact made" to "primary
source identified and confirmed live; coverage and reliability
verification still pending." agriprice.gov.eg/local-prices — an
official Egyptian government portal — is confirmed live and requires
no negotiated access, unlike the originally-referenced El-Obour
relationship. Not a full close: coverage, data currency, and
weekly-cadence support are unverified.

Sourcing method: a compiled, multi-source pipeline. agriprice.gov.eg
for wholesale/local commodity staples, supplemented by direct price
collection (manual and/or electronic, chain-dependent) from a small
number of large supermarket chains for packaged/branded goods.
Compiled into spreadsheets, reviewed, then adjusted. First real
description of the P-03 mechanism; still needs an owner, cadence, and
tooling before P-03 can close.

Known obstacle, already on record: Carrefour Egypt blocks automated
clients. Electronic collection won't work uniformly — account for
which chains are scrapable versus need manual collection.

L-05 (data licensing rights) — still NS, now concretely actionable. A
government portal's data and a retailer's posted prices likely carry
different legal standing for reuse. Worth real legal review now that a
specific method exists to evaluate.

New scope: an indicative-pricing engine for packaged goods. Normalizes
brand/weight/origin variance (e.g. spaghetti across brands and pack
sizes) into one indicative price per item, compared on a standard-unit
basis (e.g. per 100g/kg) before applying back to a recipe's actual
quantity. Exact normalization formula not yet decided. Directly feeds
the Class A/C/imported tier system from §28 — the canonical Class A
rate is what cost_per_serving uses.

Left explicitly open:
- The exact normalization formula (median / average / defined Class A
  rate)
- Which supermarket chains, and which support electronic vs. manual
  collection
- P-03's owner, cadence, and tooling for the weekly cycle

---

## 30. Units — three authored, the cook shows two — SETTLED (20 September 2026)

*An addendum, per append-never-insert. It supersedes the dual-unit paragraphs of
§6.7 and §11's 29 August household-measure addition without editing them; both
still describe two units. Recorded on 20 September as the T-04 correction in the
competitor register (`competitor-study-combined.md`, Appendix A) and filed here
on 24 September — until then this file did not carry it.*

## Addendum — 20 Sept 2026: three authored units, two displayed

T-04 (accepted 29 Aug) displayed whatever two units were already entered for an
ingredient — a mass and, where someone had entered one, a household measure.
This is corrected.

**New decision, settled 20 Sept 2026:**

- **Every ingredient record authors three unit values** — imperial (oz, lb,
  fl oz), metric (g, ml) and kitchen measure (cup, spoon).
- **The cook chooses, in settings, which two of the three display**, and those
  two show side by side on every quantity.
- **Still no computed conversion.** All three are authored per ingredient and
  none is derived; §6.7's reason — Egyptian cup and spoon sizes vary too much
  for a conversion to be anything but a fabricated number — stands.
- **Still no toggling mid-recipe.** The choice is a setting, not a control on
  the cook page; §6.7's "rather than behind a toggle" is unchanged.

**What it adds:** a third unit field on the ingredient record (§11) and a
display-preference setting.

**Not settled here, flagged:**

- **Field names and storage** in `content/ref/ingredients.yaml`. None of the
  three is in the schema yet — §11's household measure of 29 August was never
  implemented either.
- **The default pair**, before the cook has chosen.
- **Ingredients with no sensible value in a unit** — counted items such as eggs,
  or a pinch. The decision requires all three; whether a field may be blank, and
  what displays when it is, is open.
- **Authoring cost.** A third hand-entered value on every entry in the ingredient
  reference; the register still rates T-04 **XS**.

---

## 31. Wine, and what "halal" can claim — SETTLED IN PART (2 September 2026)

*Decided in a chat session on 2 September and carried until now only by that
session's handoff note, which sat outside both repositories; filed here on 24
September, and the note archived. Written in this file's terms rather than
copied, as the note itself asked.*

**No "halal" second version of a recipe.** The proposal was a second recipe
file, labelled halal, for dishes cooked with wine. Rejected: it is a fork, and a
fork is what §9 exists to prevent — §18.2's "many recipes per dish", made by the
author's hand instead of the user's. It would also present a version the kitchen
never tested as a tested recipe (§6.1).

**Where wine is structural — deglazing, a braising liquid, a reduction — the
line carries an authored substitute.** This is `availability-draft.md` §5's
`note {kind: substitute}`: written once by the recipe's author, shown on the
ingredient line, never applied automatically. Cost and nutrition compute from
the wine as authored. Beef bourguignon, pilot recipe 5, is the first case.
*The first-500 workbook (`PDF Files/Documentation/` in the vault, Revision 4, 14 September) goes further
on Ibrahim's instruction — "always suggest substitutes for the alcohol" — so
every alcohol line carries one, not only the structural ones.*

**"Contains alcohol" needs no new schema.** `alcohol` is already a `diet` class
on the ingredient (§11) and `contains` derives from it (§26), so a recipe's
alcohol content is computed from its ingredient list the way vegetarian and
gluten-free are — and withheld, as they are, when any ingredient's `diet` is
unset.

**The claim is "alcohol-free", not "halal".** Alcohol content is provable from
the ingredient reference. Halal is not: it also turns on how the meat was
sourced and slaughtered, and on additives — gelatin, rennet — that nothing in
the schema tracks. A wrong halal claim is §11's warning about `diet` ("a
vegetarian claim wrong once costs a guest their dinner") made heavier, because
it is a claim about religious observance. **Any badge or filter says
alcohol-free; halal is not claimed** unless a real sourcing record stands
behind it.

**Open:**

- Whether an alcohol-free badge or filter ships at all, and where it sits in
  §16.7's still-open filter interaction model.
- What a sourcing record behind a halal claim would have to be — schema,
  supplier evidence, certification — if one is ever wanted.

---

## 32. `main_protein` gains `lamb` — SETTLED (24 September 2026)

*An addendum to §26, per append-never-insert. §26's list still reads seven
values; this supersedes it without editing it.*

**`main_protein` is a closed list of eight:** `beef · lamb · poultry · seafood ·
pork · vegetarian · mixed · none`.

Lamb was missing, and nothing in the seven could hold it truthfully. The first
candidate catalogue (`PDF Files/Documentation/matbakh_first_500_recipes.xlsx`, in the vault) builds 27 of
its 500 dishes on lamb — fattah, mansaf, tarb, kuzu tandır, rogan josh, lamb
tagine — across the Egyptian, Levantine, Turkish, Gulf, Persian, Indian, Greek
and North African cuisines. Filed under `beef`, a cook filtering for beef gets
mansaf; filed under `mixed`, the value stops meaning *two proteins at once*. The
field is the dish's claim (§26), so the claim has to be one the cook would make.

**Unchanged:** one value per dish; authored, not derived; `mixed` for two
proteins at once, `none` for bread, pickles and drinks.

**Not decided here:** game. The catalogue has one game dish, rabbit with
freekeh, placed under `poultry` in the workbook as a judgement recorded on its
row — rabbit is sold at the poultry shop in Egypt and cooked like it — not as a
rule. A second game dish would be the moment to decide.

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
| 3 Sep 2026 | **Recipe box storage settled.** The box rides platform device backup — iCloud on iOS, Google Backup on Android — with no account, no sync server and no cross-device sync. Restore-on-reinstall, not sync, and the interface must not say *synced*. Rejected: pure local-only (a hand-built list has nothing to rebuild from) and account-backed sync (account infrastructure the product does not otherwise have, against R-06). Assumes a platform-packaged app (E-01). Whether the box feeds the planner is left open under PM-11 | 19 |
| 2 Sep 2026 | Doneness count and tile carrier **left open and pinned to the pilot** rather than settled on paper. No per-recipe figure recorded until one is measured — it is the multiplier on the largest cost line after the build | 16.6 |
| 5 Sep 2026 | **Cut photography settled as a reusable library, not a per-recipe cost.** Tight cut-identity photographs are produced **once per distinct cut-state**, held in a Cut Library **keyed to the activity lexicon**, and referenced by recipes rather than re-shot per recipe — a cut is a property of a *technique*, not of a dish, so the same butterflied breast is visually identical in every recipe it appears in and per-recipe cut shots pay repeatedly to photograph the same object. This moves cut photography off the column that scales with the catalogue and onto the one that scales with the vocabulary, which §5.5 already names as the whole economic question, on the same logic that justifies the lexicon and the ingredient vault. Two properties are part of the rationale rather than bonuses: a cut frame is the most food-only image in the system — a board and a technique, no plated dish, no kitchen, no cultural furniture — so it crosses every locale with zero re-shooting, separating the universal image asset from the locale-bound ones (mise en place, plated hero); and the lexicon is already a controlled vocabulary, so its visual counterpart resolves into the existing schema rather than sitting beside it as a folder of images. **The division of labour holds at this level too — the photograph carries cut identity, the digit carries quantity and dimension**; no photograph is relied on for proportion or size, and quantities label each ingredient regardless of any picture. **Per-recipe default:** one wide board-as-orientation mise en place, plus at most one tight shot for the single hardest cut, drawn from the library where the cut already exists. Scope, granularity, the scale-reference convention and whether the board shot can instruct unaided are deliberately **not** settled here | 20 |
| 5 Sep 2026 | **Utensils opened as a reference layer, and placed in the locale-bound column.** What equipment a recipe requires is a fact about the recipe and gets a first-class reference parallel to the ingredient one, serving the pre-commit surface (§16.2) first and filters (§16.7) second. **It is three features, not one, shipping in that order** — the requirement, the visual carrier, and substitution guidance — and only the first is settled. **The decision that matters is the column:** §20 admits the Cut Library partly because a cut frame is food-only and crosses every locale with zero re-shooting, and a utensil is *nothing but* cultural furniture — a tagine, a baladi oven and a mehmas have nothing to travel to — so the portability argument **inverts** and utensils sit with mise en place and the plated hero, not with cuts. A utensils layer does not amortise across locales. **Division of labour holds a third time** — the picture carries tool identity, words and digits carry size, capacity and substitution; no photograph conveys *26 cm*. **Presence, not inventory** (§16.1 carried over), staples assumed present and unset. **Left open:** whether a visual layer exists and what carries it (sequenced behind PM-09 — the 44 px tile already has one open carrier); scope and granularity, corpus-mined not intuited (PM-14); and whether the requirement is authored or derived, which is a schema retrofit on the same logic as §16.7. **Resolved first, because it changes the question:** **24 of 81 activities — 23 distinct glyphs — already draw a tool, vessel or appliance rather than the act** (`grate` a grater, `sift` a sieve, `simmer` a pot), four times the six ingredient-drawing activities C-05 tracks as a defect; either the same defect at four times the scale, or utensil-as-carrier is already de facto and should be made deliberate — currently neither. Folded into **C-05**, measured in **C-06** | 21 |
| 5 Sep 2026 | **Utensils, second decision: the per-recipe list is taken, the per-step repetition is rejected.** The equipment list is confirmed as the shape, with an `optional` flag per entry so the pre-commit check does not warn a cook off a dish over a grater. **No separate per-step equipment surface** — where a tool matters it is already showing in that step's own photograph or icon. Kitchen Stories restates tools every step because it has four fat steps, no station concept and a cook who would otherwise scroll back; Matbakh has six stations naming where the cook stands and a per-recipe list that has already said what to get out, so the repetition earns less. **Narrows §21.2's first open item without closing C-05:** the measured finding that 24 of 81 activities draw a tool rather than the act was recorded as reading two ways, and this leans on the second — for instrument-defined verbs the utensil is already on the tile and a second surface would draw it twice — while C-05 stays open, because the glyph must still draw the **action** wherever the action is what distinguishes it. **Watch in the pilot (C-06):** two vessels in play at one station, where neither glyph nor station header says which the tile means. Source: the Kitchen Stories instruction-layer reading, `competitor-study-part-five.md` | 21.3 |
| 16 Sep 2026 | **Ingredient substitutes for costing settled in part.** Recipes carry an explicit authored substitute list per ingredient — never inferred or averaged from price data — each tagged **cost-only** or **changes-the-cook**. The primary ingredient is the cut or species the steps, timer and doneness photograph were authored against. Cost-only substitutes swap in-app with a live cost recompute; changes-the-cook substitutes are informational (*with X instead: from Y EGP*) with a prose note on the affected steps, shown only at the moment of selection so baseline cook mode stays wordless. **Why:** cuts and fish species cannot be priced by averaging — *beef* spans a two- to four-fold range — and a species swap shifts thickness, timing and the doneness photograph where a cut swap in a braise usually does not. **Left open (PM-15):** whether changes-the-cook substitutes become swappable; whether the pilot must exercise them; the reference-species convention for fish, which lacks a governing document as the Cut Library does. **Validation test:** a pilot substitute logged cost-only that shifts a step's timing or doneness cue fails the split | 22 |
| 18 Sep 2026 | **The cooking log settled.** A cook gets a plain, chronological record of finished dishes — recipe and date, nothing more — in Profile. **Completions only:** an entry is written on the last page turn in cook mode, the one the prototypes label **Finish**; reaching the last page without taking it writes nothing. **Abandonment stays telemetry** (§4.7, §8) and is deliberately not shown to the cook in this version — a scope line, recorded so it reads as one later. **Not a streak:** a consecutive-day counter that resets on a miss is a pressure mechanic however honestly it is drawn, which is the aggregate-behaviour optimisation §8 declines; a plain log has nothing to protect. **In Profile, not in the recipe box** — §19 is an explicit save and this is its opposite, implicit and written by cooking, so folding them together would blur the distinction §19 exists to draw. **`recall_menu()` is reframed as the entertaining-specific view of the same mechanism**, not a parallel one, with no behaviour change in §13. Reuses `times_cooked()` / `last_cooked()`, already computed for `suggest_home`'s DUE list — no new tracked fields, no new authoring. **Deferred:** if abandonment is ever surfaced to the cook it must carry *why*, not merely *that* | 23 |
| 18 Sep 2026 | **Course-weighted serving settled as the party plan's quantity mechanism.** Each dish's quantity comes from an **effective covers** figure — a share of a per-course consumption target, divided across the dishes sharing that course, weighted per dish by the cook **for that event** and never written back to the recipe — fed into §6's existing scaling class and `max_scale_factor` rather than into a second scaling system. Targets are adjustable as a standing Profile preference, per course or by one coefficient, with a free-judgement per-event override; named event profiles and a drinks toggle were rejected because either would have the app modelling the cook's judgement, against §19's *stated and never inferred*. **Why:** the planner scales every dish to the full guest count — `cost = sum(r["cost"] * covers for r in m)` twice in `plan_event()`, plus three more per-dish sites including one in `recall_menu()` — so six dishes for ten guests price six full ten-person portions, and the consolidated shopping list inherits it. **This is a capability being added, not a defect repaired:** multi-dish discounting was never promised. **Blocked on PM-07:** `course` is proposed in `tag-proposal.md` but authored on no recipe, so the grouping key does not yet exist. **Open under PM-16:** the target numbers (pending catering research, not invented as placeholders), the default split when no weight is set, and whether `drink`/`soup` participate | 24 |
| 22 Sep 2026 | **Competitor citations now resolve to one file.** The competitor research was consolidated into a single vault file, `competitor-study-combined.md`, and its separate parts, the `ideas-from-cooking-apps.md` register and the study PDFs were retired. Rows above that cite `competitor-study-part-five.md` or `ideas-from-cooking-apps.md` are left as written, per append-never-insert: read `competitor-study-part-five.md` as chapter 3R of the combined file and `ideas-from-cooking-apps.md` as its Appendix A, where the KS- IDs are unchanged. No design decision changes | — |
| 20 Sep 2026 | **Monetisation model reversed — free catalogue, paid premium features.** Recorded as an addendum superseding **§17** (catalogue paid, prices free, settled 29 August) without editing it, per append-never-insert; §17 still reads SETTLED and the two now disagree. **Ripples flagged and deliberately left open:** the ownership positioning in the competitor study's recommendation, T-02's *visible to owners* wording, the Axis 7 monetisation arguments — Kitchen Stories becomes the closer analogue rather than the contrast case — and **M-02**, whose numeric base case was already NS and is unaffected. Decided outside the session that recorded it | 25 |
| 24 Sep 2026 | **PM-07 (tag vocabulary) CLOSED.** Nine authored fields — `cuisine`, `course`, **`main_protein`** (new), `spice`, `effort`, `holds`, `season`, `occasion`, `contains_override` — and eight derived tags unchanged from the draft. `main_protein` is authored because it is the dish's claim rather than its ingredient list; `occasion` gains **`siami_seafood`** and **`siami_no_seafood`**, since a seafood-fast dish excludes meat, poultry and dairy yet is not `vegan`, a combination no derived tag expresses; `cuisine` gains `thai`, `latin_american` and `eastern_european`; **`hidden` is removed** as redundant against `course: component`. `tag-proposal.md` is closed to reference. **Not settled:** §16.7's interaction model, **S-07**'s derived-key translation, and the schema work `main_protein` implies | 26, 16.7 |
| 24 Sep 2026 | **The monetisation fork resolved — M-01, M-02 and M-03 decided as one set.** **Build-to-own, Kurashiru-shaped** (retail media: audience first, retail relationship second, non-exclusive by construction — not the single-retailer exclusivity the study calls a trap), which resolves **PM-02**. **The free/paid boundary made concrete under §25's reversal:** raw weekly market prices stay **free forever** — NY-01 untouched and still irreversible — while the computed cost of a dish and the planner's costed week are **premium**; free is the raw data, premium is the data applied to a dish or a week. **Layer 3 confirmed as re-specified retail media** with a referral fee once a partnership is agreed. **Deliberately not decided:** the deal mechanic — flat referral, Kurashiru's points-back, or volume-tiered — which awaits a real retailer and is negotiation-prep material, not canon; **T-05** stays DEFER on the same grounds. **Benchmark of record: model referral at ~3%** (Instacart 3%, Kroger 1.6–4.8%, Ocado 3%), not the overstated 5% already corrected once in this project's documents. The numeric base case (**F-01**) still has to be run against this shape | 27, 25 |
| 24 Sep 2026 | **Substitution scope and mechanism settled in part — PM-15's swappability question resolved.** **Substitutes are shopping-list-only and never enter the instruction set:** steps, technique and authored timers stay exactly as test-cooked (§6.1, and `availability-draft.md` §5's existing rejection of auto-substitution). **Mechanism is a rules table** keyed by (original, substitute) pairs, each carrying a consistent effect — a structured, reusable upgrade of D-15's informational prose note. **Two tiers:** packaged goods as brand/quality tiers side by side on the shopping list with no cooking impact, and the displayed `cost_per_serving` **pinned to one canonical tier (Class A)**, never an average or the cheapest; proteins carrying an attached rule that surfaces a **suggested timer adjustment, auto-applied but visibly flagged** and overridable in one tap, so the derivation is stated as such and the cook's judgement stays in a food-safety-relevant loop. **New UI scope: editing a timer's duration mid-session, logged under E-06.** **Left open:** one rules table or two for cuts and species; whether the packaged-goods tier layer earns its own governing document; and how the protein table relates to D-13's Cut Library while PM-12's scope is open. §22.2's remaining PM-15 items — the fish reference-species convention and whether the pilot must exercise substitutes — are untouched | 28, 22 |
| 24 Sep 2026 | **Pricing data sourcing settled in part — P-01 de-risked, and an indicative-pricing engine opened.** **`agriprice.gov.eg/local-prices`, an official Egyptian government portal, is the primary source** — live and needing no negotiated access, which replaces the El-Obour relationship R-02 was written around. **Not a close:** coverage, data currency and weekly-cadence support are unverified. **The method is a compiled, multi-source pipeline** — the portal for wholesale and local commodity staples, plus direct collection from a small number of large chains for packaged goods, compiled into spreadsheets, reviewed, then adjusted; the first real description of the **P-03** mechanism, which still needs an owner, a cadence and tooling. **Collection cannot be uniform:** Carrefour Egypt blocks automated clients, so chains split into scrapable and manual. **L-05 is now concretely actionable** — a government portal's data and a retailer's posted prices likely carry different standing for reuse, and that is a real legal question rather than a hypothetical one. **New scope: an indicative-pricing engine** that normalises brand, weight and origin variance into one price per item on a standard-unit basis before applying a recipe's actual quantity; it feeds §28's tier system directly, because the canonical Class A rate is what `cost_per_serving` uses. **Open:** the normalisation formula, which chains and by which method, and P-03's owner, cadence and tooling | 29, 28 |
| 20 Sep 2026 | **Units: three authored, the cook shows two — T-04 corrected.** Every ingredient record authors **imperial, metric and kitchen-measure** values; the cook picks in settings which two display side by side. No computed conversion and no mid-recipe toggle, both unchanged. Supersedes the dual-unit paragraphs of §6.7 and §11's 29 Aug household-measure addition without editing them. **Open:** field names and storage, the default pair, blanks for counted items, and authoring cost. Recorded in the competitor register on 20 Sept; filed here 24 Sept | 30 |
| 2 Sep 2026 | **Wine, and what "halal" can claim.** No halal second version of a recipe — a fork, which §9 and §18.2 forbid. Where wine is structural, the line carries an authored `substitute` note, never auto-applied (and per the first-500 workbook, 14 Sept, every alcohol line carries one). "Contains alcohol" derives from the existing `diet` class with no new schema. **The claim is *alcohol-free*, never *halal*,** unless a real sourcing record stands behind it — halal turns on slaughter and additives the schema does not track. **Open:** whether a badge or filter ships, and what a halal sourcing record would need. Decided in chat 2 Sept; filed 24 Sept | 31 |
| 24 Sep 2026 | **`main_protein` gains `lamb` — eight values.** `beef · lamb · poultry · seafood · pork · vegetarian · mixed · none`. Lamb carries 27 of the candidate 500 across eight cuisines, and neither `beef` nor `mixed` could hold it truthfully. Supersedes §26's seven without editing it. **Not decided:** game — one dish, rabbit, placed under `poultry` in the workbook as a noted judgement | 32 |

