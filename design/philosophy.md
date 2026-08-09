# Matbakh — App Design Philosophy

**Status:** Living document. Sections marked SETTLED are decided and should not be relitigated without a stated reason. Sections marked OPEN are unresolved.

**Last updated:** 24 July 2026

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

---

## 10. On "globally adaptable" — SETTLED (with caveat)

Visual design makes the *interface* portable — likely a two-thirds reduction in translated word count. It does **nothing** for the pricing pillar, which is locale-bound by definition and is the actual expansion bottleneck.

Egypt → Gulf is not a translation problem. It is a wholesale-data-sourcing problem. The wordless principle must not create false confidence about the cost of market entry.

---

## 11. Schema fields to lock before authoring begins — SETTLED

Cheap now, very expensive to retrofit across 500 recipes.

**On the ingredient:**
- `scale_class` (continuous | discrete | seasoning | fixed)
- `divisible` (bool)
- `default_unit`
- `pack_size`

**On the recipe line:**
- `scale_class_override`

**On the recipe:**
- `base_servings`
- `serving_presets[]`
- `max_scale_factor`

**Implied additionally by decisions above (to confirm):**
- step-level: `mass_sensitive_timing` (bool), `doneness_photo`, `heat_level` (ordinal)
- page-level: `station`, `order_dependent` (bool)

---


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

## 13. Open questions

### 13.1 Discovery — NOT STARTED
No philosophy established. 500 curated recipes with no duplicates means **browsing is the product** for the first ten minutes of anyone's relationship with Matbakh. This is where the curation promise reads either as confidence or as thinness.

The governing question differs from the reader's. The reader asks *how do I not break your concentration.* Discovery asks *how do I help you decide fast without pretending I know you.* These do not share a design logic and should not be forced to.

### 13.2 Pre-commit presentation of cost and nutrition — NOT STARTED
How cost and nutrition present themselves on a recipe *before* the cook commits.

### 13.3 The meal planner — NOT STARTED
How it stays advisory without becoming nagging. Established constraint from prior work: non-rigid, non-mandatory, treats deviation as normal; hard rules apply only to dietary exclusions.

### 13.4 The entertaining / hosting mode — WORKED THROUGH, NOT BUILT
Proposed menus, budget, shopping list. A genuinely different mode with different physics.

Argued through 1 August 2026. The conclusion is that it is **two features, not one**, and the split matters more than anything else here: one is a document, the other is a change to the reader. They ship separately and in that order.

**Worked example** (the brief this was argued against): twelve covers, Mexican, beef and chicken preferred over seafood, two vegetarians, not too spicy, a salad included, 1,500 LE — about 125 a head.

#### A. The party plan — a pre-commit document

Everything the host reads *before* they start cooking. It cannot drift, because nothing in it is live.

1. **Menu suggestion, modifiable.** A constrained selection over tagged recipes — cuisine, protein, spice, course, dietary, cost. Small enough to solve exactly. Blocked on §13.7; see below.
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

§13.7. Menu suggestion cannot be built without the tag vocabulary, and **tags are the expensive retrofit** — adding them at recipe 400 means revisiting 400 files. This is the same closed-vocabulary problem the lexicon solved in August 2026, and it should be settled before authoring reaches volume, not after.

### 13.5 Step granularity — PARTIALLY SETTLED
Working answer: granularity governed by **hands**, not grammar — a step ends when you next need to look at the screen. Section 4.1's order-independence rule operationalises this, but it has not yet been tested against real recipes at volume.

### 13.6 Doneness photography — SCOPE UNDECIDED
Agreed as the right mechanism (§5.2). Not yet decided: how many recipes get them, how many per recipe, who shoots them, and what that adds to the per-recipe production cost currently modelled at ~$40.

### 13.7 Filters and dietary attributes — NOT STARTED, NOW ON THE CRITICAL PATH
Dietary requirements, personal preferences, heat, vegan/vegetarian, kids-suitable, weight-watching. The attributes are known; the interaction model is not.

**Raised in priority 1 August 2026.** §13.4 established that menu suggestion is blocked on this, and that tags are the one thing genuinely expensive to retrofit — every recipe authored before the vocabulary is settled has to be revisited. The vocabulary should be closed and small for the same reason the activity lexicon is: it is translated once, and it is what a filter can promise.

At minimum it needs cuisine, course, protein, spice level, dietary exclusion (*vegetarian as written*, not *could be made vegetarian*), effort, and whether a dish holds well — that last one only matters for entertaining, which is why it surfaced now.

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
| 1 Aug 2026 | Party plan is a document; multi-recipe sessions are a reader change; no scheduler | 13.4 |
| 1 Aug 2026 | Alarm jumps to the recipe, return costs one tap | 13.4 |
| 1 Aug 2026 | Tab strip on tablet, single button on phone | 13.4 |
