# Storyboard companion

**Everything in the project that bears on the step-imagery decision, in one
place.** Compiled 21 August 2026 from `philosophy.md`, `asset-spec.md`,
`authoring-standard.md`, `activities.yaml`, `step-imagery-research.md`,
`step-imagery-decision.md`, `recipe-pilot-scheme.md`, and the two authored
recipes in the vault.

**For:** storyboarding a number of recipes by hand, on paper, to settle what
goes in the 44 px tile.

> **Every count here is read from the file, not remembered.** Where this
> document and any older note disagree, re-run `matbakh.py status` and
> `matbakh.py lexicon` — they are the authority. The one thing here that is
> *judgement* rather than measurement is the Class M / Class S split in §5, and
> it is marked as such.

---

## 1. What the storyboard is actually deciding

Three of the four layers are closed. Do not spend storyboard time on them.

| The cook asks | Answered at | Carrier | Status |
|---|---|---|---|
| Where am I? | the arc, **17 px** | glyph | **closed** — `philosophy §4.4`, nothing else survives 17 px |
| **What do my hands do?** | the tile, **44 px** | **open** | ← this is the decision |
| Is it ready? | doneness band | photograph of the state | **closed** — `§5.2` |
| Why? What did I miss? | prose, on request | generated from the object | **closed** — `§3`, two views one truth |

The three candidates for the tile:

| | Cost at 500 recipes | Survives 17 px | Recolours by state | Separates `chop`/`mince` |
|---|---|---|---|---|
| **Static glyph** | 0 | yes | yes | **no** |
| **Animated glyph** | ~60–100 h once | yes | yes | probably |
| **Reusable action loop** (81-verb library) | ~50–60 h once | no | no | yes |
| **Recipe-specific frame** (video per recipe) | 750–2,000 h | no | no | yes |

### The four things a storyboard can settle that nothing else can

1. **Does the page grammar survive real recipes at volume?** `philosophy §16.5`
   says step granularity *"has not yet been tested against real recipes at
   volume."* A storyboard is that test, minus the cooking.
2. **How many tiles actually land on a page**, and therefore how many glyphs
   compete for attention in one glance.
3. **Which actions you could not draw** — the honest signal for where a glyph is
   not carrying its weight.
4. **Whether the ingredient changes the gesture.** This is the one finding that
   could kill the reusable-library recommendation. See §9.

**What a storyboard cannot settle:** whether motion helps. You cannot draw
motion on paper. That needs the prototype
(`prototypes/tile-comparison.html`) or the published page, held next to the
paper.

---

## 2. The rules a page must obey

From `philosophy §3`, `§4.1–4.7` and `authoring-standard §4.1`. These are
settled — a storyboard page that breaks one is a storyboard of a different
product.

**Structural**

- **One step = one page = one station.** If the cook has to move, that is a new
  page — even for a single action.
- **A page may hold several actions only if they are order-independent and share
  one station.** All the knife prep is one page with four tiles. *Sear* and
  *deglaze* are two pages, because in cooking **the sequence is the
  information**.
- **Waiting is never a page.** *Simmer 20 minutes* is a timer attached to the
  preceding action.
- **Target 6–10 pages. 14 is a hard ceiling.** Exceeding it is an editorial
  signal, not a formatting problem — either the dish is genuinely a project, or
  the steps are over-atomised. The ceiling is doubly justified: it is about the
  most that shows as legible thumbnails on one phone screen in the map.
- **Nothing scrolls, anywhere in cook mode.**

**The two tests to apply while drawing**

- **Granularity:** *a step ends when you next need to look at the screen.*
  Governed by hands, not grammar.
- **The metric is not page count — it is pages you must re-read.** Turning a page
  is nearly free; coming back from the stove and reconstructing which half of a
  page you had already done is expensive.

**Carriers** — `philosophy §5.1`

| Carrier | Conveys |
|---|---|
| **Icons** | Actions — chop, fold, simmer, rest |
| **Digits + unit symbols** | Quantity — 200 g, 20 min, 180 °C |
| **Words** | Only the name of the thing, and irreducible judgement |

And the architectural consequence, `§5.4`: **digits are a live text layer over a
static visual grammar, never baked into artwork.** Easy to violate the moment
anyone produces composite step graphics — worth holding in mind while drawing,
because a hand-drawn storyboard naturally merges them.

---

## 3. The anatomy of one page

What each storyboard frame has to account for. Field names are the implemented
ones (`philosophy §11`, reconciled 1 August).

### The step — one page

```yaml
- station: stove              # board | stove | bench | grill | oven | serve
  qualifier: { en: takliya, ar: التقلية }    # renders "Stove · takliya"
  ordered: true               # only if out-of-sequence ruins the dish
  heat: 3                     # 1 low · 2 medium · 3 high
  tiles: [...]
  timer: { minutes: 40, label: {...}, mass_sensitive: true }
  makes: takliya              # names an intermediate
  photo: assets/....jpg
  doneness: { en: ..., ar: ... }
  note: { kind: never, text: {...} }
```

- **`station` is a closed list of six.** Multiple pages at one station are normal
  — molokhia has four `stove` pages, separated by `qualifier`.
- **`ordered: true` only if doing the tiles out of sequence ruins the dish.**
  Default `false`. On a single-tile step it is meaningless and warns.
- **`photo` and `doneness` travel together.** The photograph shows what the words
  say. Never one without the other.

### The tile — one action

```yaml
- do: mince                   # lexicon key — the verb comes free, in 5 locales
  qualifier: { en: no colour, ar: بدون تلوين }
  into: "@soffritto"          # destination — carried in data, NEVER printed
  items:
    - { id: onion,   amt: 1,  cut: brunoise, cut_mm: 2 }
    - { id: carrots, amt: 60, cut: brunoise, cut_mm: 2 }
  short: hand_mince           # attaches a technique clip
```

or the bespoke path, which is the deliberate escape hatch:

```yaml
- verb: { en: "Pour over, listen for the hiss", ar: اسكب واسمع الشهقة }
  glyph: pour                 # bespoke verb REQUIRES an explicit glyph
  item: "@takliya"
```

**Fields:** `do` **or** `verb` · `qualifier` · `item` or `items[]` · `amt` ·
`carried` · `cut` · `cut_mm` · `into` · `short` · `glyph` (override).

Two that matter for the storyboard specifically:

- **`carried: true`** marks the same physical ingredient reappearing at a later
  station, so the shopping list counts one bird rather than three. On paper,
  mark carried items differently — it is the single most common validator
  warning.
- **`into:` is never captioned.** Settled 19 August: the frame is chosen to show
  where the food goes, so a caption only repeats the picture. It briefs the
  imagery; it does not print.

### Glyph resolution order — `asset-spec.md`

```
tile.glyph          explicit override on that tile
  ↓ else
activity.glyph      from lexicon/activities.yaml
  ↓ else
ingredient.glyph    from ref/ingredients.yaml
```

**The activity glyph wins over the ingredient glyph.** This was a real bug fixed
on 19 August — the builder was drawing the *ingredient*, which inverts
`philosophy §5.1` and the asset-spec rule *"draw the action, not the
ingredient."* It matters on paper too: ingredient glyphs are coarse categories
(45 ingredients share `jar`, 38 share `vegetable`), so a page of four spices drew
four identical jars and the 17 px arc degraded with it.

---

## 4. True geometry — draw your frames at these proportions

From `asset-spec.md`, measured from the prototypes rather than chosen.

| Element | Rendered | Notes |
|---|---|---|
| **Cook-mode tile glyph** | **44 × 44 px** | the primary size, and the minimum touch target |
| Tablet tile glyph | 62 × 62 px | largest use |
| **Arc thumbnail glyph** | **~17 px** | 40 × 38 box at `scale(.42)`. **The binding constraint** |
| Inline chrome | 32 / 24 / 22 px | |
| Minimum touch target | **48 px** | nothing tappable smaller — wet hands |
| **Hero photo** | 393 × 318, `contain` | shoot **5:4 landscape** (1.25 vs the band's 1.236) |
| **Step / doneness photo** | 361 × 176, `cover` | **2.05:1** — shoot 4:3 or 3:2, subject in the middle **65% vertically** |
| Arc thumbnail photo | ~54 × 42 | 1.29:1 |
| Shorts poster | 84 × 64 | 1.31:1 |

**Type scale** — `tokens.css`: quantity digits 44 px · the action 22 px · the
noun 17 px · body 15 px · mono labels 11 px. Nothing functional below 15 px;
cook mode is read at arm's length.

**An icon must survive a 3.6× range, 17 px to 62 px.** An icon legible at 17 px
is legible everywhere; the reverse is not true. Drawing rules: **three strokes or
fewer**, no detail below 2 px on the 24 grid, **silhouette must differ from every
neighbour** — test by squinting at the arc strip.

---

## 5. The vocabulary — all 81, by station

Read from `content/lexicon/activities.yaml`. **81 activities, 78 distinct
glyphs, 3 shared-glyph pairs.**

**Class M / Class S is my judgement, not a measurement** — M means a single frame
cannot separate it from at least one neighbour; S means a placement, a
configuration, or an elapsed condition that a still captures entirely. Correct it
as you draw. Totals: **47 M / 34 S.**

### board — 10 (10 M / 0 S)

| Key | Class | Glyph |
|---|---|---|
| `chop` | M | `chop` **⚠ shares with `mince`** |
| `crush` | M | `crush` |
| `cut_wedges` | M | `wedges` |
| `dice` | M | `grid-dots` |
| `grate` | M | `grater` |
| `mince` | M | `chop` **⚠ shares with `chop`** |
| `peel` | M | `peeler` |
| `shred` | M | `line-dashed` |
| `slice` | M | `slice` |
| `zest` | M | `lemon` |

*The board is 10 for 10 motion. This is not a coincidence — it is why `chop` and
`mince` share a file.*

### stove — 19 (15 M / 4 S)

| Key | Class | Glyph |
|---|---|---|
| `bain_marie` | S | `bowl-over-pot` |
| `blanch` | M | `bubbles-fast` |
| `boil` | M | `bubbles` |
| `braise` | S | `pot-deep` |
| `deep_fry` | M | `deep-fry` |
| `deglaze` | M | `deglaze` |
| `do_not_stir` | S | `nostir` |
| `flambe` | M | `flame-pan` |
| `fry` | M | `fry` |
| `ladle` | M | `ladle` |
| `poach` | M | `egg` |
| `pressure_cook` | S | `pressure-cooker` |
| `reduce` | M | `arrow-down-right` |
| `simmer` | M | `pot` |
| `skim` | M | `spoon` |
| `steam` | M | `steam` |
| `stir` | M | `rotate` |
| `stir_fry` | M | `wok` |
| `sweat` | M | `steam-low` |

*`boil`, `simmer` and `poach` are defined by bubble behaviour. As stills they are
three pans of water.*

### bench — 34 (14 M / 20 S)

| Key | Class | Glyph |
|---|---|---|
| `blend` | M | `blender` |
| `brine` | S | `bowl-salt` |
| `brush` | M | `brush` **⚠ shares with `baste`** |
| `chill` | S | `snowflake` |
| `coat` | S | `coat` |
| `cool` | S | `temp-down` |
| `cure` | S | `salt-cure` |
| `drain` | S | `strain` |
| `dry` | S | `sun` |
| `ferment` | S | `ferment` |
| `flatten` | M | `flatten` |
| `fold` | M | `fold` |
| `freeze` | S | `ice` |
| `grind` | M | `mill` |
| `infuse` | S | `infuse` |
| `inject` | S | `syringe` |
| `knead` | M | `hand-grab` |
| `layer` | S | `layers` |
| `marinate` | S | `bowl-spoon` |
| `mash` | M | `mash` |
| `mix` | M | `mix` |
| `rest` | S | `clock-pause` |
| `roll` | M | `roll` |
| `set` | S | `set` |
| `shape` | S | `shape` |
| `sift` | M | `sieve` |
| `soak` | S | `bowl` |
| `squeeze` | M | `squeeze` |
| `strip` | M | `strip` |
| `stuff` | S | `stuff` |
| `toss` | M | `toss` |
| `wash` | S | `droplet` |
| `whisk` | M | `whisk` |
| `wrap` | S | `wrap` |

*The bench is where Class S concentrates — 20 of 34. A loop of `rest` is four
seconds of nothing happening.*

### grill — 4 (3 M / 1 S) · oven — 5 (1 M / 4 S) · serve — 6 (3 M / 3 S) · any — 3 (1 M / 2 S)

| Key | Station | Class | Glyph |
|---|---|---|---|
| `char` | grill | M | `flame` |
| `grill` | grill | S | `grill` |
| `sear` | grill | M | `sear` |
| `skewer` | grill | M | `skewer` |
| `bake` | oven | S | `bread` |
| `baste` | oven | M | `brush` **⚠ shares with `brush`** |
| `broil` | oven | S | `flame-top` |
| `roast` | oven | S | `oven` |
| `toast` | oven | S | `toast` |
| `drizzle` | serve | M | `drizzle` |
| `dust` | serve | M | `dust` |
| `garnish` | serve | S | `leaf` |
| `serve` | serve | S | `plate` |
| `sprinkle` | serve | M | `sprinkle` |
| `to_taste` | serve | S | `salt` **⚠ shares with `season`** |
| `add` | any | S | `add` |
| `pour` | any | M | `pour` |
| `season` | any | S | `salt` **⚠ shares with `to_taste`** |

### The three glyph collisions, and which imagery fixes them

| Pair | Class | Does motion fix it? |
|---|---|---|
| `chop` / `mince` | M / M | **Yes** — different motions |
| `brush` / `baste` | M / M | **Yes** — different motions |
| `season` / `to_taste` | S / S | **No.** Same physical act; what differs is *intent* |

`season` and `to_taste` both appear in molokhia. No photograph, frame or loop can
show intent — that one is a lexicon or layout problem and survives every imagery
option. **Storyboard it deliberately and see whether the page can separate them.**

*(A correction worth carrying: earlier notes list `cut_wedges`/`zest` as a
collision pair. On disk they carry distinct glyphs — `wedges` and `lemon`. Three
pairs share a glyph, not four. Sole meunière and sayadeya were chosen partly to
test that pair, so it is still worth watching in practice, but it is not a
shared-file collision.)*

### The seven demotions — activity + qualifier, no icon, no new word

Recipes referring to the old keys must use the form on the right.

| Old key | Becomes |
|---|---|
| `joint` | `slice` + *into pieces* / لقطع |
| `simmer_covered` | `simmer` + *covered* / مغطى |
| `add_to` | `add` + *into* / في |
| `pour_over` | `pour` + *over it* / فوقها |
| `arrange` | `serve` + *arranged* / مرصوص |
| `alongside` | `serve` + *alongside* / بجانبها |
| `pickle` | `ferment` + *pickled* / مخلل |

`do_not_stir`, `to_taste` and `serve` were demoted in review but **kept** — they
have no underlying activity to qualify. `do_not_stir` in particular *inverts* its
verb: rendered as `stir` with a qualifier it would read as **"stir"** on a 44 px
tile, on the one step where stirring splits the dish.

### The escape hatch

A bespoke `verb:` is allowed and is **working as designed** — recipe 1 used it
twice. It requires an explicit `glyph:`. Log every use: a verb reached for in
**≥3** recipes earns a place in the closed set; reached once or twice, it stays
bespoke. *Do not grow the vocabulary for a long tail.*

---

## 6. The four other closed vocabularies

**Stations (6):** `board` · `stove` · `bench` · `grill` · `oven` · `serve`

**Note kinds (4)** — free-text headers would destroy the convention a cook learns
to read:

| Kind | Severity | Reads as | Use for |
|---|---|---|---|
| `coming_up` | info | COMING UP | something to prepare for two pages ahead |
| `stay_here` | warn | STAY HERE | do not walk away from the pan |
| `never` | danger | NEVER | an absolute — *never let it boil, a boil splits it* |
| `make_ahead` | info | MAKE AHEAD | can be done the day before |

**Spend `never` carefully. Its power comes from being rare.** It is also the one
piece of prose that speaks unasked — everything else sits behind an ⓘ.

**Units (7):** `g` · `kg` · `ml` · `L` · `tsp` (rounds to ¼) · `tbsp` (rounds to
½) · `count`

**Scaling classes (4):**

| Class | Behaviour | Typical |
|---|---|---|
| `continuous` | linear, rounded to a legible increment | flour, rice, stock, meat by weight |
| `discrete` | linear, then whole or ½ if `divisible` | eggs, lemons, onions |
| `seasoning` | **sub-linear — factor^0.75** | salt, chilli, spices |
| `fixed` | does not scale | frying oil, blanching water |

*Tripling a stew and tripling its cumin produces an inedible stew. And nobody
wants 750 ml of frying oil because they doubled the koftas — oil depth is set by
the pan, not the batch.*

**Locales (5):** `en` · `ar` · `ar_eg` · `ar_lv` · `ar_gulf`, falling back
`ar_gulf → ar_eg → ar`. **Dialects are lexicon-only**; per-recipe prose stays in
`ar`.

---

## 7. Two worked storyboards, as authored

The only two recipes that exist. Draw against these — they are the calibration.

### Molokhia bil farakh — 8 pages, 14 activities, 4 demotions

| # | Station · qualifier | Heat | Tiles | Timer | Photo + doneness |
|---|---|---|---|---|---|
| 1 | **board** | — | `chop` onion ×2 *fine* · `crush` garlic ×8 · `chop` coriander · `slice` chicken *into pieces* ⟵ demotion | — | ✓ *Onion in even dice — no piece thicker than a matchstick* |
| 2 | **stove · stock** | 2 | `simmer` *covered* ⟵ demotion (chicken **carried**, water 1500) · `add` bay leaf | 40 min | ✓ *Meat lets go of the bone when you push it* |
| 3 | **bench** | — | `strip` chicken **carried** · `drain` `@stock` 1200 | — | — · note `coming_up` |
| 4 | **stove · takliya** | 3 | `fry` (garlic **carried**, ghee) · **bespoke** *"Then add"* glyph `spice` | — | ✓ *Straw-gold at the edges. One shade past this is bitter* · note `stay_here` |
| 5 | **stove · pot** | 1 | `add` *into the stock* molokhia 400 → `@stock` | 8 min ⟵ mass-sensitive | ✓ *Thick enough to coat the spoon. No bubbles at the surface* · note `never` |
| 6 | **stove · pot** | 1 | **bespoke** *"Pour over, listen for the hiss"* glyph `pour` · `do_not_stir` *after* | — | — |
| 7 | **grill** | 3 | `sear` chicken **carried** *skin-side* · `season` salt | 6 min ⟵ mass-sensitive | ✓ *Lacquered, blistered in places, dry to the touch* |
| 8 | **serve** | — | `serve` *alongside* rice ⟵ demotion · `cut_wedges` lemon · `to_taste` salt | — | ✓ *Soup, rice and lemon on the table together* |

**What recipe 1 already told us.** 14 activities and 4 demotions, 18 coverage
cells. Every demotion read naturally as activity + qualifier. Only two bespoke
verbs — *"Pour over, listen for the hiss"* (the escape hatch working as designed,
**keep**) and *"Then add"* (which should simply be `add` — **lint, no lexicon
change**). Nothing missing; no collision hit in practice.

**Note page 8:** `season` (page 7) and `to_taste` (page 8) both occur. They share
`salt.svg`. Different pages, so it did not bite — but that is luck, not design.

### Tagliatelle al ragù — 9 pages, the stove arc

| # | Station · qualifier | Heat | Tiles | Timer | Photo + doneness |
|---|---|---|---|---|---|
| 1 | **board** | — | `mince` → `@soffritto` — onion 1, carrots 60 g, celery 60 g, all `cut: brunoise`, `cut_mm: 2` | — | ✓ *Grains the size of a match head, cut not crushed* |
| 2 | **stove · soffritto** | 1 | `sweat` *no colour* (3 carried + olive oil) · `makes: soffritto` | 12 min ⟵ mass-sensitive | ✓ *Slumped and glassy, no gold at the edges* |
| 3 | **stove · meat** `ordered` | 3 | `fry` pancetta *until the fat runs* → `sear` beef | — | ✓ *Browned in patches and still sizzling* · note `never` |
| 4 | **stove · pot** `ordered` | 2 | `add` `@soffritto` *to the meat* · `deglaze` wine | 6 min | ✓ *The pan quiet and the base dry again* |
| 5 | **stove · pot** | 1 | `add` (tomatoes, paste) · `season` salt · `makes: ragu` | — | ✓ *Barely more than a slick of red through the meat* |
| 6 | **stove · covered** | 1 | `simmer` *covered* `@ragu` · `add` stock *a ladle when it tightens* | 90 min | ✓ *One lazy bubble every few seconds at the edge* · note `stay_here` |
| 7 | **stove · uncovered** | 1 | `add` milk → `@ragu` | 90 min | ✓ *Dark orange, glossy, thick enough to leave a channel* |
| 8 | **stove · pasta** `ordered` | 3 | `boil` (water, salt **carried**) · `add` tagliatelle · `drain` *keep a cup of the water* | 3 min ⟵ mass-sensitive | ✓ *Floats and the edge has lost its chalk* |
| 9 | **serve** `ordered` | — | `toss` *in the pan, off the heat* (pasta **carried** + `@ragu`) · `grate` parmesan *over* | — | ✓ *Every ribbon coated and nothing pooling on the plate* |

**What this one demonstrates:** one tile carrying **three ingredients with
individual amounts and cuts** (page 1), the `into:` destination, two
intermediates (`@soffritto`, `@ragu`), six of nine pages at the **same station**
separated only by `qualifier`, and 180 minutes of passive time that produce **no
pages at all** — waiting is a timer, never a step.

**Both recipes are 8–9 pages, inside the 6–10 target.** That is a sample of two.
Whether it holds is exactly what the storyboard tests.

---

## 8. Which recipes to storyboard

The pilot's fifteen were chosen for *coverage*, not convenience
(`recipe-pilot-scheme.md §1`). Storyboarding is far cheaper than cooking, so you
can do more of them — but if you want the smallest set that stresses the imagery
question specifically, the coverage matrix points at six:

| # | Dish | Why, for **imagery** |
|---|---|---|
| 1 | **Molokhia** | Already authored — the control. Carries `season`/`to_taste`, the collision no imagery fixes |
| 2 | **Bolognese** | Already authored — the stove arc, `boil`/`simmer` as motion, multi-item tiles |
| 4 | **Sole meunière** | `baste`↔`brush` collision **and** the lemon pair in one dish |
| 6 | **Lamb kofta** | `mince`↔`chop` collision, plus the **only carrier of the grill station** (`grill`, `char`, `skewer`) |
| 13 | **Baladi bread** | The Class S extreme — `ferment`, `rest`, `set`, `prove`. Where motion shows nothing |
| 2b | **Koshari** | Assembly and layering, the `arrange`→`serve`+qualifier demotion, an unusually flat page shape |

Two are already authored, so that is four new. If you want a seventh, **mahshi**
adds a sub-recipe (`uses` / `yield`), which changes page shape in a way nothing
else in the list does.

**A discipline worth borrowing from the pilot:** two waves, not one. Storyboard a
first batch, log everything, **change nothing**, then do the rest and re-audit.
Deciding after the first batch over-fits to it.

---

## 9. What to record while drawing

A storyboard that produces an impression settles nothing. A storyboard that
produces a dataset settles it. Per tile:

| Column | Values | Why |
|---|---|---|
| **Carrier verdict** | glyph sufficient / needed motion / needed *this specific dish* | The three-way version of the question. ~150 judgements across 15 recipes — the only dataset on this that will ever exist |
| **Ingredient changed the gesture?** | y / n | **The falsifiable one.** ≥3 recipes = the action is not generic and the reusable library fails |
| **Could you draw it in ≤3 strokes?** | y / n | The asset-spec rule, tested by hand |
| **Silhouette clash on this page** | which pair | `asset-spec.md`: squint at the arc — if two steps look alike, the cook loses their place |
| **Reached outside the lexicon** | the bespoke wording | Feeds the ≥3 rule |
| **Demotion felt forced** | y / n | ≥2 recipes promotes it back |
| **Arabic felt wrong** | the word | One real context is enough to fix a cell |

Per page: station · tile count · `ordered` y/n · timer y/n · has doneness y/n ·
would you re-read this page.

Per recipe: page count against 6–10/14 · activities used · bespoke count ·
demotions used · sub-recipes · **minutes to storyboard it**.

The tracker already has the shape of this —
`03-catalogue/recipe-pilot-tracker.xlsx`, Recipes / Coverage / Lexicon-decisions
tabs. *Clear the stale Excel lock file `~$matbakh-lexicon-review-annotated.xlsx`
in `03-catalogue/ref/` before the verdicts land.*

### The thresholds, applied only after the batch

- **Add a verb** to the closed set only if reached for in **≥3** recipes.
- **Promote a demotion back** if its activity+qualifier read awkwardly in **≥2**.
- **Split or redesign an icon** if a glyph failed at 17 px anywhere, or two
  actions collided on one picture in practice.
- **Fix an Arabic cell** if a drafted verb felt wrong in even **one** real
  context.
- **An unexercised activity means *examine*, not *delete*.**

### Exit criteria — all four must hold before freezing the lexicon

1. **≥90%** of actions mapped to an existing activity or a clean
   activity + qualifier.
2. No new verb recurred **≥3×** without being addressed.
3. Every icon used read at **both 44 px and 17 px**, no unresolved in-practice
   collision.
4. Every drafted-Arabic verb that appeared was confirmed or corrected.

---

## 10. Traps

Things that will bite while you draw, each learned the hard way.

- **`ordered: true` on a single-tile page is meaningless** — the one real nit
  found in recipe 1.
- **A missing `carried: true` is the most common warning** — *"X already bought
  in step N"*. On paper, mark carried items distinctly or the basket triples the
  chicken.
- **Six of the 81 activities currently draw the ingredient, not the action** —
  `cut_wedges`, `zest`, `garnish`, `season`, `to_taste`, `simmer`. This violates
  asset-spec's own rule. If your storyboard reproduces it, that is the placeholder
  glyph misleading you, not the design.
- **Ingredient glyphs are coarse.** 45 ingredients share `jar`, 38 share
  `vegetable`. A page of four spices is four identical pictures.
- **The activity glyph must win over the ingredient glyph.** Fixed in the builder
  19 August; easy to invert again by hand.
- **`into:` is data, not a caption.** Never write it on the frame.
- **Digits are a live layer.** Do not draw a quantity into the picture — scaling,
  unit toggles and live pricing all change it.
- **Waiting is never a page.** Bolognese has 180 passive minutes and zero pages
  for them.
- **The 81 glyph names are not all verified against tabler.io — several are
  invented** (C-05, still open). The 20 SVGs in `design/icons/` plus 8 cut glyphs
  are **geometric placeholders**, and the prototype renders them at full fidelity,
  so a reviewer reads them as the icon set. They are not.
- **Never hand-type a measurable number.** The ingredient count has been quoted as
  177, 178 and 179 inside one week. `matbakh.py status` generates them.
- **`check` counts the repo fixture as a recipe** — `content/recipes/` holds a
  second molokhia so a bare clone validates. A raw `check` reads *3 authored*
  where two are real; `status` splits them.

---

## 11. The evidence, in one place

For weighing what you see on paper against what is known.

**Settled by Matbakh's own documents**

- Photographs cannot serve the 17 px arc — `philosophy §4.4`, `asset-spec.md`.
  **The icon set gets built under every option.**
- Doneness belongs to photography — `§5.2`. Irreducibly per-recipe.
- Prose is two renderings of one object, never authored separately — `§3`.
- An asset that carries no words is made once — `asset-spec.md`, the founding
  principle, and the argument the reusable library extends.

**Strong external evidence**

- **Animation over static pictures for procedural-motor knowledge: d = 1.06**
  (95% CI 0.72–1.40), the largest moderator in Höffler & Leutner's 26-study
  meta-analysis. Realistic/video-based: d = 0.76. Overall: d = 0.37.
- **But length reverses it** — Wong et al. on the transient information effect:
  short animations win, long ones lose the advantage entirely.
- **Coherence beats multimedia** — Mayer's coherence principle runs at d = 1.66,
  *larger* than the multimedia principle. Extraneous detail hurts. A `chop` glyph
  is the photograph with the coherence violation removed.
- **A still is bad at action, good at state** — Heiser et al. A frozen frame
  mid-chop cannot distinguish chop from slice from mince.
- **Glance cost is set by encoding, not size** — a 10× spread on the same tiny
  screen from encoding alone.
- **Abstraction, not photography, is what fails cross-culturally** — concrete
  symbols 75–87.5%, abstract 0–12.5%. And the sobering Egypt-specific one:
  sequential image comprehension is a **learned convention**, not a perceptual
  universal.

**Precedent**

- Every adjacent domain shoots the vocabulary once: Fitbod 1,600 exercises,
  Physiotec 20,000+, Spreadthesign 610,000 clips across 35 sign languages.
  Libraries trade as commodities at $0.09–$0.20 per clip.
- **No cooking product composes an action-keyed library into recipe steps.**
  Clean negative, searched by product, capability, patent and academic
  literature. Nobody has done it because it needs a closed verb vocabulary to key
  against — which is exactly what Matbakh has and nobody else does.
- **EPIC-KITCHENS-100** annotates unconstrained real kitchen footage with **97
  verb classes**. Independent corroboration that the vocabulary closes near 81.

**What nobody knows**

There is **no published data comparing recipes with step photographs against
recipes without**, and **no controlled study of pictorial versus photographic
instruction under kitchen conditions at all.** This decision cannot be settled by
citation. It can be argued from craft, or measured in-house — which is what the
storyboard is.

---

## 12. Where everything lives

| | |
|---|---|
| Design decisions | `matbakh-design/design/philosophy.md` |
| Asset geometry and craft | `matbakh-design/design/asset-spec.md` |
| How to author a recipe | `matbakh-design/design/authoring-standard.md` |
| The imagery research | `design/step-imagery-research.md` (18 Aug) |
| The imagery decision | `design/step-imagery-decision.md` (21 Aug) |
| The live comparison | `prototypes/tile-comparison.html` |
| The vocabulary | `content/lexicon/activities.yaml` |
| The pilot scheme | `matbakh-private/03-catalogue/recipe-pilot-scheme.md` |
| The tracker | `matbakh-private/03-catalogue/recipe-pilot-tracker.xlsx` |
| The two authored recipes | `matbakh-private/03-catalogue/recipes/{molokhia,bolognese}.yaml` |
| Refresh the measured numbers | `cd content && python3 matbakh.py status --write ../../matbakh-private/02-strategy/matbakh_pm_log.md` |

**Reading order, if you only read three things before starting:**
`authoring-standard.md §4.1` (decide the pages before you type) ·
`philosophy §4.1–4.4` (page structure, re-reading, tile state, the map) ·
§5 and §7 of this document (the vocabulary, and the two worked storyboards).
