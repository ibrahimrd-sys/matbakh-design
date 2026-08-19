# Matbakh — recipe authoring standard

**Status:** Operational standard. This is C-03 in the PM log.
**Written:** 15 August 2026. Verified against `content/matbakh.py`, `_template.yaml`,
`lexicon/activities.yaml` (81 activities), `lexicon/chrome.yaml` and
`ref/ingredients.yaml` (177 entries) as they stand today.

This document is written so that **someone with no prior context can produce a
compliant recipe**. If you are the founder authoring the pilot, skip to §2 — but
read §1 once, because it is the thing people get wrong.

Companion: `design/philosophy.md` is authoritative for *why*. This document is
authoritative for *how*. Where they disagree, philosophy wins and this file is
the bug.

---

## 1. The one idea you must hold

**You author IDs and NUMBERS. You do not author names.**

Ingredient names, cooking verbs, station names, note labels, buy hints and unit
symbols all come from the lexicon, already translated into English, Modern
Standard Arabic and three Arabic dialects. You write `do: chop` and
`item: onion`; the reader renders *Chop · Onion* or *فرم · بصل* depending on who
is looking.

The consequence, and the reason the whole schema is shaped this way: **adding a
fifth language costs one pass over the lexicon plus the handful of prose fields
in each recipe — not five hundred recipes' worth of vocabulary.**

Only four things in a recipe are genuinely prose and need a translator:

| Field | What it is |
|---|---|
| `title` | The dish name |
| `why` | The pre-commit pitch |
| `doneness` | What it should look like right now |
| `note.text` | The four typed warnings |

Everything else is a key, a number or a boolean. If you find yourself typing an
English cooking word into a recipe file, stop — you are almost certainly doing
it wrong. The exception is `verb:`, covered in §4.4, and it is rare on purpose.

---

## 2. Before you start

Have these open:

1. **`tools/recipe-editor.html`** — open it in a browser. No install, no server.
   Load three files together (Ctrl-click): `ref/ingredients.yaml` from the vault,
   and `lexicon/activities.yaml` + `lexicon/chrome.yaml` from the repo. Each file
   is recognised by its shape, so order does not matter.
2. **A terminal** in `content/`, for `matbakh.py`.
3. **The dish itself, cooked at least once by you.** This standard assumes you
   are describing something you have made, not transcribing something you read.

The editor drives every activity, station, note-kind and ingredient field from
dropdowns fed by those files, so **a typo cannot enter the catalogue**. It also
carries a live validation rail applying the same rules as `matbakh.py`, and it
refuses to produce a download while any error stands.

Nothing is uploaded. Files are read in the browser and stay on your machine —
which is also why the editor cannot save in place. You download the edited file
and put it back in the vault yourself. **There is no autosave.** Download before
you walk away.

One thing the editor does not do: **comments in the original YAML are not
preserved.** The file is regenerated. If a recipe carries comments worth keeping
— as the molokhia worked example does — edit it by hand rather than round-tripping
it through the editor.

> **Fixed 15 Aug, and worth knowing why.** Until today the editor had three
> defects that between them made it unsafe on an authored file. It did not
> normalise the short tile form, so a tile written `item: onion` loaded with no
> ingredient at all — the "On what" row never appeared, ingredient checks were
> skipped, and saving wrote the tile back with its ingredient deleted. It had no
> concept of `into:` or of sub-recipes (`uses:` / `yield:`), so both were dropped
> on save. And its quoting rule treated a comma as safe, while several fields are
> emitted inside a flow mapping `{ en: …, ar: … }` where a comma separates —
> so any prose containing one was silently cut in half. All three are fixed, and
> a full round-trip of the molokhia recipe now returns byte-equivalent data.

### Where the file goes

Copy `content/recipes/_template.yaml` to **the vault**, at
`03-catalogue/recipes/<id>.yaml`. Never into the repo — the commit guards will
stop you, and correctly. Only the template and one demo recipe are tracked.

---

## 3. The head block

```yaml
id: molokhia                 # snake_case, and it must match the filename
source_locale: en            # the language you are authoring in
status: draft                # draft → tested → published
```

**`status` is a promise, not a label.** `draft` means written. `tested` means
*you cooked it from these steps and they were right*. `published` means it can
ship — and the validator hard-fails a `published` recipe that still has
untranslated strings. Do not promote a recipe you have not cooked.

```yaml
title:
  en: Molokhia bil Farakh
  ar: ملوخية بالفراخ
```

### `why` — the pre-commit pitch

```yaml
why:
  en: The Cairo version — stock from a whole bird, takliya poured at the table.
      No blender, no cornflour, no shortcuts that change the texture.
```

This field exists because of a promise made elsewhere: **one recipe per dish.**
That promise obligates the app to say *why this version* in one line. Without it,
omission reads as absence rather than choice, and someone's grandmother's version
becomes a complaint instead of a conversation.

**Concrete claims, not adjectives.** "Stock from a whole bird, no cornflour" is a
claim a cook can check. "Authentic and delicious" is not. One or two sentences.

### Servings

```yaml
servings:
  base: 4                    # the yield the amounts below are written for
  presets: [2, 4, 8]
  max_scale: 1.5
```

`base` is **the yield you actually cooked and tested.** Every other serving count
is a derivation the kitchen never saw. This is why the reader always shows which
state it is in and why returning to base is one tap.

**`presets` are derived from the recipe's own countable ingredients so they
always come out whole.** A 4-serving recipe containing 3 eggs offers 2 / 4 / 8 —
not 6, which would produce 4.5 eggs. A recipe with no discrete ingredients can
offer 2 / 4 / 6 / 8 freely. Half a divisible item (½ onion) is fine; half a
chicken thigh is not, which is what the ingredient's `divisible` flag records.

Work the presets out at authoring time. The cook must never meet an impossible
number.

**`max_scale` is a physical limit, not an arithmetic one.** Twelve portions in
one wok is a grey stew. Above this the reader shows a two-pan "cook in batches"
glyph rather than refusing. Indicative: stir-fry and sear ×2 · braise and stew
×4 · baking ×2 with a tin-size note.

Omitting `max_scale` is a warning, not an error — but it means the reader cannot
warn on batch size, so fill it in.

### The rest of the head

```yaml
hands_on_minutes: 55
hero: assets/molokhia-dish.jpg
price_source: el_obour
nutrition_per_serving:
  energy_kcal: 410
  protein_g: 38
  fat_g: 12
  carbs_g: 34
```

`hands_on_minutes` is attention, not elapsed time — a 40-minute simmer you walk
away from does not count. Use **"Compute from the ingredients"** in the editor for
nutrition: it adds up what the steps actually use and divides by base yield, and
it reports what it could not include rather than silently under-reporting.

Note the standing gap: an ingredient with no gram conversion (something counted,
or measured in spoons) contributes **nothing** to the computed figures. 21 of the
177 reference entries currently carry no nutrition data at all. Read the editor's
"could not include" list; do not ignore it.

`price_source` is a feed key. **You never author a price or a date** — the feed
supplies both, because every number in Matbakh carries a date and a source.

---

## 4. The steps — where the real work is

### 4.1 Decide the pages before you type

This is the part that separates a good recipe from a compliant one.

**One step = one page = one station. If the cook has to move, that is a new
page — even for a single action.**

**A page may hold several actions only if they are order-independent and share
one station.** All the knife prep — onion, garlic, coriander, jointing the bird —
is one page with four tiles. "Sear the chicken" and "deglaze the pan" are two
pages, because in cooking *the sequence is the information*.

**Waiting is never a page.** "Simmer 20 minutes" is a timer attached to the
preceding action, not a step of its own.

**Target 6–10 pages. 14 is a hard ceiling.** Exceeding it is an editorial signal,
not a formatting problem: either the dish is genuinely a project and should be
labelled as such, or the steps are over-atomised and need merging. The ceiling is
doubly justified — it is also about the most that can be shown as legible
thumbnails on one phone screen in the map.

**The granularity test:** a step ends when you next need to look at the screen.
Granularity is governed by *hands*, not grammar.

**The metric to optimise is not page count — it is pages you must re-read.**
Turning a page is nearly free. What is expensive is coming back from the stove
and having to reconstruct which half of a page you had already done.

Sketch the pages on paper first. For molokhia the answer was eight: board ·
stove/stock · bench · stove/takliya · stove/pot · stove/pot · grill · serve.

### 4.2 The step fields

```yaml
- station: stove             # board | stove | bench | grill | oven | serve
  qualifier: { en: takliya, ar: التقلية }   # renders as "Stove · takliya"
  ordered: true
  heat: 3                    # 1 low · 2 medium · 3 high
  tiles: [...]
  timer: {...}
  makes: takliya
  photo: assets/garlic-butter-pan.jpg
  doneness: {...}
  note: {...}
```

**`station` is a closed list of six.** An unknown station is a hard error.
Multiple pages at the same station are normal and expected — molokhia has four
`stove` pages, distinguished by `qualifier`.

**`ordered: true` only if doing the tiles out of sequence ruins the dish.**
Default to `false`. Setting `ordered: true` on a single-tile step is meaningless
and the validator warns — it was the one real nit found in recipe 1.

**`photo` and `doneness` travel together.** The photograph shows what the words
say. Do not write one without the other.

### 4.3 Tiles — the lexicon path

```yaml
tiles:
  - do: chop                             # activity key — verb comes free
    item: onion                          # ingredient id
    amt: 2                               # in the ingredient's own unit
    qualifier: { en: fine, ar: ناعم }    # appended: "Chop" + "fine"
```

`do:` takes a key from the 81-activity lexicon. The verb and all five locales come
free. **Prefer this always.**

`qualifier` is how the vocabulary stays small. Rather than a separate `julienne`
activity, you write `slice` plus a qualifier. Seven activities were deliberately
demoted this way — `joint` became `slice` + "into pieces", `simmer_covered`
became `simmer` + "covered", `alongside` became `serve` + "alongside". If you
find yourself wanting a verb that is not in the lexicon, **first ask whether it
is an existing activity plus a qualifier.** The test: *would you draw the same
icon?* If yes, it is one activity plus a qualifier.

**`items:` when one action touches two things:**

```yaml
  - do: simmer
    qualifier: { en: covered, ar: مغطى }
    items:
      - { id: chicken_whole, carried: true }
      - { id: water, amt: 1500 }
```

The displayed amount comes from the first item that has one.

**`carried: true` is the field people forget, and it costs money.** It marks this
as the *same physical ingredient* as an earlier step — the same bird, not a
second purchase. Without it the shopping list double-counts. The validator warns
when an ingredient is bought twice, and that warning is usually a missing
`carried`.

**`amt` is in the ingredient's own unit**, whatever `unit:` says in the reference
— `g`, `ml`, `tsp`, `tbsp`, `count`.

**`into:` and `@intermediate`** — see §4.5.

**`short:`** references a technique clip; see §4.7.

### 4.4 Tiles — the bespoke path, and when it is allowed

```yaml
  - verb: { en: Pour over, listen for the hiss, ar: اسكب واسمع الشهقة }
    glyph: pour
    item: "@takliya"
```

`verb:` overrides the lexicon with bespoke phrasing. **It requires an explicit
`glyph:`** — the validator hard-fails without one, because there is no activity
key to take a picture from.

This is an escape hatch, and it should feel like one. Use it **only when the
lexicon would flatten something genuinely worth keeping.** "Pour over, listen for
the hiss" earns it: the sound is the doneness cue, and no icon carries that.
"Then add" does not earn it — that is just `add`, and writing it as bespoke is a
lint.

Every bespoke verb is logged during the pilot. The rule that will be applied
afterwards: a verb reached for in **≥3 recipes** earns a place in the closed set;
once or twice, it stays bespoke. **Do not grow a closed vocabulary for a long
tail** — every entry is a word translated into every language ever shipped.

### 4.5 Intermediates — things the recipe makes and then uses

```yaml
intermediates:
  stock:
    glyph: pot
    unit: ml
    name: { en: Stock, ar: المرق }
```

Declared in the head block, produced by a step via `makes:`, and referenced
downstream as `@stock`. **They never reach the shopping list** — you do not buy
your own stock.

```yaml
  - station: stove
    tiles: [...]
    makes: stock          # this step produces it
  ...
  - station: bench
    tiles:
      - do: drain
        item: "@stock"    # consumed later
        amt: 1200
```

Two hard errors guard this: using an intermediate **before any step makes it**,
and declaring one that **no step makes**.

**An intermediate is not a sub-recipe.** An intermediate is made inside this
recipe and used inside it. A sub-recipe — a tahini sauce, a dough, a spice mix —
is a *first-class recipe in its own file*, authored and test-cooked once, never
duplicated into the parent, referenced with `uses: [{id, amt}]` against its own
`yield`. Its ingredients roll into the parent's shopping list and its allergens
roll up too, recursively. If the thing you are making is used by more than one
dish, it is a sub-recipe, not an intermediate.

### 4.6 Timers, doneness and notes

```yaml
  timer:
    minutes: 40
    label: { en: Stock, ar: المرق }
    mass_sensitive: true
```

Timers belong to the **session**, not the page — a timer keeps running when the
cook turns the page, and the persistent band is what expresses parallelism.

**`mass_sensitive: true` when the time scales with the batch.** Simmering six
portions takes about as long as four; browning six takes noticeably longer. A
rest, a proof or a marinade does **not** scale — leave the flag off. When a
mass-sensitive timer is scaled, the reader presents it alongside the doneness
photo rather than as the authority: the clock becomes advisory, the target state
becomes the truth.

**`doneness` is the highest-value writing in the whole file.**

```yaml
  doneness:
    en: Straw-gold at the edges. One shade past this is bitter.
```

This is where cooking knowledge lives. The wordless principle removes vocabulary,
not judgement — a recipe that drops the doneness cue has kept the arithmetic and
thrown away the craft. Write what the cook should *see, hear or feel right now*,
and where possible name the failure on the other side of it. "Meat lets go of the
bone when you push it." "Thick enough to coat the spoon. No bubbles at the
surface."

Note that the doneness text and the doneness photograph must agree. If the words
say straw-gold at the edges, the photograph has to show straw-gold at the edges —
not one shade past.

**Notes are a closed, typed set of four.** Free-text headers would destroy the
convention a cook learns to read.

| Kind | Severity | Reads as | Use for |
|---|---|---|---|
| `coming_up` | info | COMING UP | Something to prepare for two pages ahead |
| `stay_here` | warn | STAY HERE | Do not walk away from the pan |
| `never` | danger | NEVER | An absolute — "never let it boil, a boil splits it" |
| `make_ahead` | info | MAKE AHEAD | Can be done the day before |

Spend `never` carefully. Its power comes from being rare.

### 4.7 Technique shorts

```yaml
shorts:
  takliya_colour:
    secs: 31
    poster: assets/garlic-butter-pan.jpg
    clip: assets/clip-knife.webm      # omit if not shot yet
    title: { en: Takliya — the colour to stop at, ar: التقلية — لون التوقّف }
```

Referenced from a tile by `short: takliya_colour`. Defined but unreferenced is a
warning; referenced but undefined is a hard error.

**Omit `clip` for one you have not shot.** The reader shows TO BE SHOT and the
validator reminds you. This is the normal state during the pilot.

Remember where video sits in the design: **if a step needs a video to be
understood, the step is wrong.** Shorts are a library browsed *before* cooking,
never a dependency in the critical path.

---

## 5. Validate

```bash
cd content
python3 matbakh.py check                       # everything reachable
python3 matbakh.py check recipes/molokhia.yaml # one recipe
python3 matbakh.py lexicon                     # audit the vocabulary
python3 matbakh.py gaps                        # untranslated strings
```

**The vault must resolve, or you are validating against 12 sample ingredients
instead of 177.** Resolution order, first hit wins: `--vault PATH` →
`MATBAKH_VAULT` → `content/vault.path` → `../../matbakh-private/03-catalogue`.
Every run prints which source it used. **Read that line.**

> **Known trap.** With the vault set, a *relative* `recipes/...` path resolves
> against the repo folder, not the vault, producing a spurious `FAIL`. Pass the
> full path, or let the bare `check` find it.

> **Fixed 15 Aug.** A scaffolded recipe with `steps: []` used to report
> `PASS · clean`. It now reports its own state, **`STUB`**, and the summary line
> separates authored work from scaffolding:
>
> `15 recipe(s) · 1 authored · 14 stub(s) · 0 failing · 17 warning(s)`
>
> A stub is deliberately **not** an error — it must not block `publish.sh` while
> the pilot runs — but it is no longer a pass. A stub that also has real errors
> still reports `FAIL`, and the exit code is unchanged, so the publish gate
> behaves exactly as before.

> **A comma inside a flow mapping needs quotes.** Fields written on one line —
> `verb: { en: …, ar: … }`, `qualifier`, `title`, `label`, intermediate `name` —
> use a comma as the separator. `en: Pour over, listen for the hiss` therefore
> parses as `en: "Pour over"` plus a junk key, and the recipe still validates
> because the YAML is legal. Write `en: "Pour over, listen for the hiss"`. Both
> occurrences of this in the demo recipe were found and fixed on 15 August.

### Reading the result line

`PASS` · authored and valid. `STUB` · scaffolded, `steps` still empty.
`FAIL` · has errors. **Never read "0 failing" as "authored"** — read the
`authored` count.

### Every hard error, and what it means

Errors block. The recipe is not authored until these are clear.

| Error | What it means |
|---|---|
| `will not parse` | Broken YAML — usually indentation |
| `missing required field: X` | One of `id`, `source_locale`, `title`, `servings`, `steps` |
| `expected per-locale text, got a bare string` | You wrote `title: Molokhia` instead of `title: {en: ...}` |
| `missing source locale 'en'` | A prose field has no text in the language you are authoring in |
| `servings.base is required` | Nothing can scale without it |
| `unknown station 'X'` | Not one of the six |
| `no tiles` | A page with nothing on it |
| `unknown note kind 'X'` | Not one of the four |
| `activity 'X' is not in the lexicon` | Typo, or a verb that needs the bespoke path |
| `verb override needs an explicit glyph` | Bespoke `verb:` without `glyph:` |
| `needs either 'do' or 'verb'` | A tile with no action at all |
| `short 'X' is not defined` | Referenced a clip key that has no entry |
| `intermediate 'X' is not declared` | `@X` with no entry in `intermediates` |
| `uses 'X' before any step makes it` | Order violation |
| `intermediate 'X' is declared but no step makes it` | The reverse |
| `ingredient 'X' is not in ref/ingredients.yaml` | Add it in the ingredient editor first |
| `'X' has no scaling class` | **Servings would break.** The single most important ingredient field |
| `'X' has unknown scaling class` | Not one of the four |
| `makes 'X' which is not declared` | `makes:` naming an undeclared intermediate |
| `timer without minutes` | — |
| `status:published with N untranslated strings` | Promote to `published` only when complete |

### Warnings — the standing backlog

Warnings do not block, but each one means something.

| Warning | Usually means |
|---|---|
| `no servings.max_scale` | The reader cannot warn on batch size |
| `base N is not one of the presets` | Your preset list forgot the tested yield |
| `short 'X' has no clip yet` | Normal during the pilot — renders TO BE SHOT |
| `ordered:true with 1 tile` | Ordering is meaningless; set it `false` |
| `has one but not the other — no photo/doneness` | They travel together |
| `'X' is divisible but not discrete` | The flag has no effect |
| `'X' is counted with no weight per item` | It contributes nothing to nutrition |
| `'X' is measured in tsp with no cup weight` | Same |
| `'X' already bought in <step>` | **Almost always a missing `carried: true`** |
| `timer is mass_sensitive but nothing here scales` | Flag is wrong, or the tile is |
| `short 'X' defined but no tile references it` | Dead entry |

---

## 6. During the pilot (PM-04), also do this

While the fifteen pilot recipes are being authored, the recipe is only half the
output. The other half is the measurement, and it is the reason the pilot exists.

1. **Start a timer when you begin authoring.** Authoring minutes are a pilot
   output — and the input PM-01 and F-01 have been waiting on.
2. **Log every reach outside the lexicon** — each action where no activity fit,
   or where you wanted a verb that is not there. *This is the single most
   important thing the pilot captures.*
3. **Eyeball each icon at 44px and 17px** in **`tools/lexicon-editor.html`** —
   the tile and arc previews live there, not in the recipe editor. Mark whether
   the glyph reads at both sizes, and whether two different actions in this one
   recipe landed on the same picture.
4. **Check each demotion in context** — does `slice` + "into pieces" actually say
   *joint the chicken* to a cook, or does it feel forced?
5. **Cook it.** Note where reality diverged from the written steps, what doneness
   cues you needed, and whether the granularity felt right on a phone with wet
   hands. Record **test-cook minutes** and **ingredient cost**.
6. **Flag any Arabic that felt wrong in context**, especially the 14 drafted
   verbs.
7. **Log the row** in `recipe-pilot-tracker.xlsx` and tick the Coverage tab.

**The governing discipline: nothing about the lexicon changes during the pilot.**
Author against the vocabulary as it stands. Measure first, decide once — after
the whole batch, so the vocabulary is not over-fitted to the first wave.

---

## 7. Definition of done

A recipe is authored when all of these hold:

- [ ] `matbakh.py check` passes with **zero errors**, and every warning is either
      understood or fixed
- [ ] `steps` is not empty *(the validator will not catch this — see §5)*
- [ ] Page count is 6–10, or the dish is deliberately labelled a project
- [ ] Every page has `photo` **and** `doneness`
- [ ] Every doneness cue describes what to see, hear or feel — and the photograph
      agrees with it
- [ ] Every repeated ingredient carries `carried: true`
- [ ] `presets` come out whole against the countable ingredients
- [ ] `max_scale` is set and reflects a physical limit
- [ ] Bespoke verbs are justified, not lazy
- [ ] Arabic is present for all four prose fields
- [ ] You have cooked it from these steps → `status: tested`

---

## Appendix A — the 81 activities, by station hint

The hint is guidance for the editor's dropdown ordering, not a constraint. An
activity may be used at any station.

**any (3)** — `add` · `pour` · `season`

**board (10)** — `chop` · `crush` · `cut_wedges` · `dice` · `grate` · `mince` ·
`peel` · `shred` · `slice` · `zest`

**bench (34)** — `blend` · `brine` · `brush` · `chill` · `coat` · `cool` ·
`cure` · `drain` · `dry` · `ferment` · `flatten` · `fold` · `freeze` · `grind` ·
`infuse` · `inject` · `knead` · `layer` · `marinate` · `mash` · `mix` · `rest` ·
`roll` · `set` · `shape` · `sift` · `soak` · `squeeze` · `strip` · `stuff` ·
`toss` · `wash` · `whisk` · `wrap`

**stove (19)** — `bain_marie` · `blanch` · `boil` · `braise` · `deep_fry` ·
`deglaze` · `do_not_stir` · `flambe` · `fry` · `ladle` · `poach` ·
`pressure_cook` · `reduce` · `simmer` · `skim` · `steam` · `stir` · `stir_fry` ·
`sweat`

**oven (5)** — `bake` · `baste` · `broil` · `roast` · `toast`

**grill (4)** — `char` · `grill` · `sear` · `skewer`

**serve (6)** — `drizzle` · `dust` · `garnish` · `serve` · `sprinkle` ·
`to_taste`

> Three pairs are flagged as possible icon collisions and are under test in the
> pilot: **chop/mince**, **cut_wedges/zest**, **baste/brush**. If both members of
> a pair appear in one recipe, note whether the shared picture confused you.

## Appendix B — closed vocabularies

**Stations (6):** `board` · `stove` · `bench` · `grill` · `oven` · `serve`

**Note kinds (4):** `coming_up` · `stay_here` · `never` · `make_ahead`

**Units (7):** `g` · `kg` · `ml` · `L` · `tsp` (rounds to ¼) · `tbsp` (rounds to
½) · `count`

**Scaling classes (4):**

| Class | Behaviour | Typical |
|---|---|---|
| `continuous` | Linear, rounded to a legible increment | Flour, rice, stock, meat by weight |
| `discrete` | Linear, then rounded to whole or ½ if divisible | Eggs, lemons, onions |
| `seasoning` | Sub-linear — factor^0.75 | Salt, chilli, spices |
| `fixed` | Does not scale | Frying oil, blanching water |

*Why sub-linear seasoning:* tripling a stew and tripling its cumin produces an
inedible stew. *Why `fixed` matters:* it is the class people forget, and the one
that produces absurd output — nobody wants 750 ml of frying oil because they
doubled the koftas. Oil depth is set by the pan, not the batch.

**Locales (5):** `en` · `ar` · `ar_eg` · `ar_lv` · `ar_gulf`. Dialects fall back
— `ar_gulf` → `ar_eg` → `ar` — so partial coverage degrades to a comprehensible
word, never a blank. **Dialects are lexicon-only.** Per-recipe prose stays in
`ar`; dialectising 5,000 prose strings is a second content project the size of
the first.

## Appendix C — the ingredient record

You do not author these; you select them. But you need to read them.

```yaml
chicken_whole:
  glyph: chicken
  name: { en: Chicken, ar: فرخة كاملة }
  diet: [meat, poultry]        # closed 14-value taxonomy — drives dietary tags
  unit: g                      # the unit your `amt` is in
  cls: continuous              # scaling class — required, or servings break
  buy: { en: 1 bird, ar: فرخة } # shopping-list hint
```

Plus, where relevant: `divisible` (can it be halved), `pack` (pack size, shopping
list only), `convert.cup_g` / `convert.piece_g` (what a cup or one item weighs —
tbsp and tsp are *derived* at cup/16 and cup/48, never stored), and `nutrition`
per 100 g.

If an ingredient is missing, add it in **`tools/ingredient-editor.html`** before
authoring the recipe. Fill `cls` first — without it, servings cannot be computed
at all.

**Note on cost:** cost per dish computes from the *exact quantity consumed*,
never from pack size — otherwise a pinch of saffron costs a whole jar. Pack-size
rounding belongs only to the shopping list.

---

## Appendix D — worked example

`03-catalogue/recipes/molokhia.yaml` is the reference implementation: 8 pages,
five stations, two intermediates, three timers, four technique shorts, one
justified bespoke verb and one that was not. Read it alongside §4.

Its eight pages: board · stove/stock · bench · stove/takliya · stove/pot ·
stove/pot · grill · serve.
