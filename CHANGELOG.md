# Changelog

Newest first. One entry per publish. `build.py` warns if a prototype is newer
than the top entry, so this cannot quietly fall behind.

Format: `## YYYY-MM-DD — release`

## 2026-08-29 — pricing and palate adjustment settled

**Philosophy — two new settled sections, two open questions partly closed.**

- **§17 Pricing and the free surface — SETTLED.** The weekly market price list is free perpetually and published without requiring an install; the cost of a specific dish is paid. The commitment is one-way. Consequence: recurring revenue must come from new catalogue content, not from access to prices.
- **§18 Palate adjustment — SETTLED.** Post-cook adjustments stored against the user as multipliers, applied after the scaling class, auto-applied with a deviation marker, flowing through to the shopping list, nutrition and cost. Component adjustments propagate. Deltas layer over the canonical recipe and never fork it. The delta store is shaped for aggregate reading, which makes it a quality signal on the catalogue as well as a personalisation feature.
- **§16.1 Discovery — partly settled.** Ingredient-led entry is a primary route: presence not quantity, staples assumed present, ranked by fewest missing. It resolves against the ingredient graph, so it does not block on §16.7.
- **§16.2 Pre-commit cost and nutrition — partly settled.** The bolognese prototype's answers written back at last, plus the browse-card decision: owners see the figure, a fixed editorial sample set is unblurred for everyone, everyone else sees a server-side blurred figure carrying market and date.
- **§6.7, §9, §11** amended: dual units display as authored with no computed conversion; `why` recorded as required and load-bearing; schema additions for the household-measure field and the palate delta store.
- **Decision log reconciled.** Rows backfilled for the 13 August renumber and the 15 August §11 status change, sub-recipe and lexicon decisions.
- **preflight:** the release-vs-changelog check was an unfinished `pass` and never warned. It now does.
- `discovery-draft.md`: ingredient search is no longer deferred; cost now has three card states, and unpriced-locale must be visually distinct from unpaid.
- **Handover revised** — `02-strategy/handover-2026-08-20.md` updated for the 28–29 August and 1–2 September sessions: provenance note, §0 settled-since-20-August, §7 the `market-study.md` / MON-01 contradiction, §8 items 1 and 11 rewritten plus PM-10, El-Obour and trademark clearance added, §9 four new traps. Header now reads *Revised 15, 19, 20 August and 2 September 2026.*

Source: nine-app competitor study, `02-strategy/ideas-from-cooking-apps.md`.


## 2026-08-26 — a directory you can rely on

- **`DIRECTORY.md` added**, and it is the point of this release. Every file in
  the repository is now marked **CANON · GENERATED · FIXTURE · DRAFT · WORKING ·
  PLACEHOLDER · GUARD**, so the question *can I cite this?* has an answer that
  does not depend on remembering. The vault has its own, beside it and never
  committed.
- **Three overlapping READMEs in `tools/` folded into one.** `README.md`,
  `tools-README.md` and `translator.md` were each a strict superset of the last;
  the merged file is built from the fullest of the three and now covers all
  **four** tools rather than claiming there are two. `translator.md`'s name was
  an accident — it is what `Translator README.md` became when `publish.sh`
  refused a filename containing a space.
- **READMEs now carry something indicative in the name**, a convention set
  today. `tools/README.md` becomes **`ToolsReadme.md`**, the vault's becomes
  **`VaultReadme.md`**, and the archive gets **`ArchiveReadme.md`**; each opens
  with a distinctive H1 and a written date, so the content identifies itself
  even when the filename is stripped by a paste or an export. A bare
  `README.md` does no work in a tab bar when there are fourteen of them. **Two
  permanent exceptions**, recorded in `DIRECTORY.md §11`: the repo root, because
  GitHub renders only `README.md` as the landing page, and
  `content/recipes/README.md`, because it is whitelisted *by name* in all four
  vault guards and a safety net should not be edited to suit a naming
  preference. Pre-existing stub READMEs keep their names until rewritten. The
  cost, taken knowingly: `tools/` no longer gets an auto-rendered description
  when browsed on GitHub.
- **`design/philosophy_old.md` retired.** A placeholder header plus the music
  decision, which lives in `philosophy.md §12` in full. Nothing referenced it.
- **`content/ref/ingredients.yaml` retired.** A stale local copy of the vault's
  reference, dated 31 July. Gitignored, so never published — and read by
  nothing: `matbakh.py` resolves either the vault's copy or
  `ingredients.sample.yaml` and never looks at that path. It existed only to be
  mistaken for the real reference.
- **`philosophy.md §16.4` is now explicitly vacant rather than silently
  missing.** Entertaining was promoted out to §13 on 13 August and the number
  was left as a hole. Renumbering 16.5–16.7 would invalidate every
  cross-reference written since, so the gap is annotated instead.
- **The molokhia schema fixture says what it is, in the file.** It is a
  near-copy of the vault's authored pilot recipe — same dish, differing only in
  `id` and one `ordered:` flag — which is why a raw `check` reads *3 authored*
  where the catalogue holds two. Retiring it needs a pilot stub to stand in and
  four guard files edited, so it is documented rather than moved.
- **`storyboard-bench-sheet.html` and `tile-comparison.html` listed in the
  manifest** under a new *Working sheets* section. They were orphans — on disk,
  in no manifest, so preflight warned on every run and no reviewer could reach
  the argument behind option C. Tagged `WORKING, TEMPORARY`; they come out when
  the question closes.
- **`README.md` refreshed.** The structure tree had no `planner/`, no `tools/`,
  and called `app-iphone.html` the lead; the pre-launch checklist still asked for
  a real `philosophy.md` and an empty `assets/`, both of which landed weeks ago.
  The first-time-publish walkthrough is now a fresh-clone section, since the repo
  is published.
- `planner/__pycache__/` removed from disk. Already gitignored; it was never
  committed.

*Nothing moved folders. `manifest.yaml`, `build.py`, `publish.sh` and the three
vault guards all still see the layout they expect.*

## 2026-08-20 — the log now says when it has gone stale

- **`content/matbakh.py status`** emits the measurable half of the PM log as a
  fenced markdown block — catalogue counts, lexicon reach, shared glyphs, the
  state of the ingredient reference. `status --write <file>` splices it into the
  log in place and leaves every other line alone; re-running replaces the block
  rather than adding a second one.
- The reason it exists: the ingredient count has been quoted as 177, 178 and 179
  inside one week, and `tag-proposal.md` sized a backfill on the wrong one. A
  number that is generated cannot drift. Statuses, decisions and risks are
  deliberately **not** generated — a script that guessed at those would make a
  stale log look maintained, which is worse than one that is obviously old.
- **The vault catalogue and the repo fixture are now counted separately.** They
  were not, so `check` reported *3 authored* where the catalogue holds two — the
  third is `content/recipes/molokhia_bil_farakh.yaml`, a schema demo that exists
  so a bare clone has something to validate.
- **`content/matbakh.py vault`** prints the resolved vault path, so `build.py` can
  ask where the vault is rather than keep a second copy of the four-step
  resolution order.
- **Preflight now warns when the PM log falls behind the repo** — comparing both
  the log's own `Last updated:` date and the generated block's measured date
  against the newest changelog entry and prototype. Warnings, not errors: it
  should nag, not block. Silent when no vault is reachable, because a fresh clone
  or CI has none by design. This is the check that did not exist between 30 July
  and 13 August, when the tracker fell three weeks behind and nothing said a word.

## 2026-08-19 — bolognese, and the tile question made visible

- `prototypes/bolognese-iphone.html` added and promoted to lead. **Temporary** —
  it exists to settle how a step should be shown, and comes out once that is
  decided. The molokhia linked flow drops one level into *Screens on their own*.
- It is the first prototype driven end to end by real recipe data:
  `03-catalogue/recipes/bolognese.yaml` through `matbakh.py build`, at 2 / 4 / 8
  servings. Nothing on screen is hand-typed. The Accademia Italiana della Cucina
  recipe as registered in Bologna, 2023 revision.
- **One act per card.** A photograph of the doing — a frame lifted from the cook
  video — then the ingredients that act takes, each with its weight and the cut
  it wants. Three "Mince" tiles became one act with three items.
- **The cut is a picture, per ingredient.** `cut: brunoise` with `cut_mm: 2`
  replaces `qualifier: fine`. Eight glyphs in `design/icons/cuts/`, a closed set
  on the same terms as the activity lexicon. `cut_mm` carries the one thing a
  glyph cannot: brunoise and dice are the same shape at different sizes.
- `into:` is carried in the data but never printed. The frame is chosen to show
  where the food goes, so a caption would only repeat the picture.
- `matbakh.py build` now emits per-item detail — name, glyph, own scaled amount,
  carried flag, cut — because a tile with four ingredients could previously show
  only one quantity.
- The page is real HTML; JavaScript only upgrades it to cook mode. It renders
  with scripts disabled, which the earlier build did not.
- **Pre-commit screen added**, so the prototype is the whole flow rather than
  cook mode alone: hero, why-this-version, hands-on against unattended time, the
  cost row, the arc as tappable thumbnails with their timers, the shopping list
  with buy hints and tick-off, technique shorts, per-serving nutrition, and the
  derived dietary line. Every figure comes from `matbakh.py build`; the basket
  rescales with the serving presets alongside the step quantities.
- The cost row shows its own absence — `—` with *no price feed connected* — rather
  than an invented number. §3 says every number carries a date and a source; there
  is no source yet, so there is no number. It also makes P-01 visible on screen.
- **Nothing scrolls.** Core principle 1 says the page is the unit, not the scroll,
  and the earlier build broke it — cook pages ran past the viewport. Every screen
  now sizes itself to the phone: cook pages give the acts five parts and the
  doneness band three, and both shrink together. Verified at 375×667, 393×852 and
  430×932 — zero overflow on all nine cook pages and all three pre-commit panes.
- The pre-commit screen is three panes behind a segmented control — Overview, The
  arc, Basket — because it carries more than one screenful. Note this departs
  from `recipe-screen-iphone.html`, which the manifest tags HAND SCROLL.
- **Nutrition moved onto Overview, under the cost.** The Health pane is retired.
  Energy, protein, fat and carbs are four digits on one strip, and the dietary
  line sits with them — the same class of fact as cost, read in the same glance,
  before committing. A pane of its own made a findable panel out of four numbers.
- **The arc and the basket stay two panes, not one.** Nine thumbnails and fifteen
  basket rows do not fit one phone screen together at any size tested, and *the
  page is the unit, not the scroll* now outranks *fewer taps*. The molokhia
  pre-commit screen fits them together only because it scrolls.
- **Prose is on request.** The doneness paragraph moved behind an ⓘ on the
  doneness photograph — the picture is the primary carrier of state (§5.2), and
  the words are the fallback for a cook who wants them. What stays on the page
  unasked is the NEVER note, which is the one place scarce prose earns its room.
- **The tile qualifier is separated from its act.** `matbakh.py build` joined them
  with a bare space, so page 8 read *"Drain keep a cup of the water"* — one clause
  where there are two. It now emits `act` and `qual` as their own fields (and
  `verb` still joined, with the same ` · ` the station qualifier already used), and
  the renderer sets the qualifier lighter and smaller behind the act.
- **Arabic fixes found by reading the RTL build rather than trusting it.** The page
  counter was bidi-mirrored — *8 / 9* rendered as *9 / 8*, which tells the cook the
  wrong thing — now isolated LTR. Back / Next / Map / Settings, the nutrition
  labels, the dietary flags, the doneness cue, the NEVER note and the running
  timer's label were all still English in the `ar` build; all now switch with the
  language. The `contains` line stays English — those are tag keys, and PM-07.
- **Basket quantities are editable.** Type over one and it stops following the
  serving presets, marked in terracotta, because a cook who already has 300 g of
  beef does not want the app overwriting them.
- **Settings added** — language, numerals, keep-screen-awake — and the language
  switch is real: EN/AR flips every string and sets RTL, driven by the `ar` build
  of the same recipe. Nothing is translated in the page; both locales come out of
  `matbakh.py build`.
- Deep links retargeted, `#recipe` and `#cook/1`–`#cook/9`, and the hash follows
  the cook.

## 2026-08-15 — planner and discovery drafts, philosophy renumber

- Planner and tests; `design/discovery-draft.md` and `design/availability-draft.md` added, both explicitly DRAFT.
- **`philosophy.md` renumbered.** Open questions §13 → §16; entertaining and hosting promoted from §13.4 to its own top-level §13; §16.4 left deliberately vacant. Anything written before this date cites the old numbers.
- **§14 Sub-recipes — SETTLED.** First-class recipes, referenced with a quantity, scaling by `amt ÷ yield`, allergens rolling up recursively.
- **§15 The activity lexicon — SETTLED.** 81 activities, ceiling ~95, dialects lexicon-only.
- **§11 advanced** from *schema fields to lock before authoring begins* to *SETTLED, and now implemented.*

*Recorded retrospectively 29 Aug 2026 from git (`873a964`).*

2026-08-12 — translator tool
`tools/translator.html` added, the fourth authoring tool. Locale-scoped queue
over any number of recipe files, with progress per recipe and a jump to the
next gap.
Structurally safe by construction: it walks for per-locale string maps and can
reach nothing else. Tested on the demo recipe — 31 prose units, zero
structural fields exposed, tiles byte-identical after a round-trip.
Doneness cues are shown beside the photograph they describe.
Translation memory for repeated phrases. Qualifiers are the case that matters:
one recipe already repeats pot, and fine / covered / skin-side recur
across any catalogue.
Measured correction: a recipe carries ~31 translatable prose units, not the
~10 previously estimated — qualifiers are per tile. The lexicon, by contrast,
is 98 strings translated once per language, not the ~600 previously stated.

2026-08-01e — sub-recipes
A recipe can now consume another: `uses: \[{id, amt}]` on the parent,
`yield: {amount, unit}` on the sub-recipe. Everything scales by amt ÷ yield.
Sub-recipe ingredients roll into the parent's shopping list, summed by
ingredient id; allergens roll up too, with cycle protection, so a sauce cannot
hide its sesame.
Testing found a real distinction: `fixed` ingredients do not scale with
servings but DO scale on a roll-up share. Water for boiling is constant for
two or eight, yet 37.5% of a sauce holds 37.5% of its water. The builder now
separates the two cases.
§13.8 records the decision; the recipe template documents it where an author
will see it.
2026-08-01d — diet field, and derived dietary tags
Ingredients gained `diet`. The editor has a chip selector and a bulk-propose
button that resolves 177 of the 179 from name rules plus a table of cases a
name cannot reveal — worcestershire is fish, bechamel is dairy and gluten.
`matbakh.py` derives `vegetarian`, `vegan`, `gluten\_free` and `contains` from
it. If any ingredient in a recipe lacks the field, the flags are withheld
entirely and the validator names what to fix: a wrong vegetarian claim costs a
guest their dinner, so silence is the correct failure.
§13.4 (the party plan) and §13.7 (filters) are unblocked by this.
2026-08-01c — audit output, and the last dialect gaps
The lexicon audit printed 70 warnings for one predictable fact — that most
activities are unused when a single recipe is loaded. It now summarises, and
only names them past 40 recipes, when "unused" starts to mean "probably does
not need an icon".
Retracted the ">60 activities, look for a merge" warning. 81 is the reviewed
outcome of sorting 294 candidate verbs; it is a decision, not drift. The check
that matters is collisions, and there are none.
Station names and note labels now carry all three dialects — 30 strings that
appear on every screen of every recipe, so a gap there cost more than any
single verb. All five locales report complete.
An Egyptian cook now reads الطبلية and متبعدش where a Gulf cook reads
لوح التقطيع and لا تبعد.


## 2026-08-01b — lexicon editor

- `tools/lexicon-editor.html` added, same pattern as the ingredient editor:
  open, edit, save straight back. Live per-dialect collision checking, with the
  offending field marked and saving blocked while one stands.
- Shows a 44px tile preview and a 17px arc strip per activity — the two sizes an
  icon has to survive.
- Verified against the real 81-activity lexicon: zero collisions, zero errors,
  and a round-trip preserving every verb across all five locales.

## 2026-08-01 — lexicon merged, three Arabic dialects

- 294-row activity list reviewed and merged. Tier 1 is 81 activities, each with
  its own icon; 124 verbs render as an activity plus a qualifier; 84 rows are
  out of scope. Review moved 10 out of Tier 1 and 8 in.
- Three dialect locales added — ar_eg, ar_lv, ar_gulf — with a fallback chain
  in chrome.yaml. ar_gulf → ar_eg → ar, so partial coverage degrades to a
  comprehensible word rather than a blank. Dialects are lexicon-only; per-recipe
  prose stays in `ar`, since dialectising 5,000 prose strings is a second
  content project the size of the first.
- Eight verbs were reworded to clear within-dialect collisions found by the
  audit: toss/stir in Egyptian, zest/peel and grill/roast in Levantine and Gulf,
  cool/chill in Gulf and MSA, season/marinate in MSA. Zero collisions remain in
  any of the four.
- Three review decisions were overridden after checking against the recipe.
  do_not_stir and to_taste have no underlying activity to qualify — do_not_stir
  rendered as `stir` plus a qualifier would read as "stir" at 44px, on the one
  step where stirring splits the dish. `serve` was kept because `alongside`
  demotes to it.
- The demo recipe was migrated: joint → slice+qualifier, simmer_covered →
  simmer+qualifier, add_to → add+qualifier, alongside → serve+qualifier,
  strain → drain. The validator caught all five.
- `matbakh.py build` now writes status to stderr, so its JSON can be piped.

## 2026-07-30g — music integration ruled out

- No integration with Spotify or any music service. Full Premium requirement
  excludes the mobile-only tiers most of the Egyptian audience holds, mobile
  autoplay restrictions fight the counter-top posture, downloaded playlists are
  encrypted DRM, and the platform terms bar commercial streaming integrations.
  Recorded in design/philosophy.md so the question does not return.
- Left open: the timer alarm must be audible over music already playing on the
  same speaker. A sound-design problem, not an integration one.

## 2026-07-30f — lexicon template and audit

- `content/lexicon/_template.yaml` added, carrying the decision rule for when a
  verb earns an entry: if you would draw the same icon, it is one activity plus
  a qualifier. Three routes ranked — lexicon, lexicon plus qualifier, bespoke.
- `matbakh.py lexicon` audits the closed vocabulary for keys that read alike,
  entries nothing uses, and per-locale translation gaps.
- It found two defects on its first run. `sear` and `fry` both read حمّر in
  Arabic, which would have shown a cook the same word for browning garlic in
  ghee and searing chicken on the grill; `sear` is now اشوِ. And `drop_in` failed
  the icon test — it was `add` with a leaf glyph, and glyphs resolve from the
  ingredient anyway — so it was merged away. 17 activities, now 16.


- Offline nutrition search added: `nutrition-db.json`, a 6,389-food USDA export,
  loads through the same picker and is searched before the online API. Field
  order decoded and verified against known values — kcal, protein, carb, fat,
  satfat, cholesterol, sodium, fibre per 100 g.

- Ingredients gained `convert`: `cup_g` and `piece_g`. Tablespoons and teaspoons
  are derived at cup/16 and cup/48 rather than stored, so one number per
  ingredient can be kept right instead of three that can disagree.
- This closes both holes in computed nutrition: counted ingredients and
  spoon-measured ones previously contributed nothing, silently. The recipe
  editor now converts to grams first, and names anything it still cannot.
- `matbakh.py` warns when an ingredient has nutrition but no conversion, since
  that is exactly the case where the figures come out low without saying so.

- Ingredient editor gained USDA FoodData Central lookup: search per ingredient,
  or walk every ingredient with no nutrition. Results are labelled by data type
  — Foundation and SR Legacy are per 100 g and preferred; Branded is per serving
  and flagged, since taking it at face value would be wrong.
- ml-measured ingredients are called out on apply, because USDA reports per 100 g
  and density makes the two differ for oil, honey and cream.
- The API key is held in browser local storage, never in the file. USDA
  deactivates keys found in code repositories, and tools/ is in a public one.

- `tools/ingredient-editor.html` and `tools/recipe-editor.html`. Single files,
  opened in a browser: no server, no Python, no install. Files are read client
  side and never uploaded; editing produces a download you put back yourself.
- Both carry a live validation rail applying the same rules as `matbakh.py`,
  and refuse to produce a download while any error stands — so a file cannot
  leave the editor in a state the validator would reject.
- The recipe editor drives activities, stations, note kinds and ingredients
  from the lexicon and reference files, so a typo cannot enter the catalogue.
  Bespoke verb wording stays available per action.
- Per-serving nutrition can be computed from step amounts against the 156
  ingredients carrying per-100g figures, and reports what it could not include
  rather than silently under-reporting.

2026-07-30e — authoring tools
Offline nutrition search added: `nutrition-db.json`, a 6,389-food USDA export,
loads through the same picker and is searched before the online API. Field
order decoded and verified against known values — kcal, protein, carb, fat,
satfat, cholesterol, sodium, fibre per 100 g.
Ingredients gained `convert`: `cup\_g` and `piece\_g`. Tablespoons and teaspoons
are derived at cup/16 and cup/48 rather than stored, so one number per
ingredient can be kept right instead of three that can disagree.
This closes both holes in computed nutrition: counted ingredients and
spoon-measured ones previously contributed nothing, silently. The recipe
editor now converts to grams first, and names anything it still cannot.
`matbakh.py` warns when an ingredient has nutrition but no conversion, since
that is exactly the case where the figures come out low without saying so.
Ingredient editor gained USDA FoodData Central lookup: search per ingredient,
or walk every ingredient with no nutrition. Results are labelled by data type
— Foundation and SR Legacy are per 100 g and preferred; Branded is per serving
and flagged, since taking it at face value would be wrong.
ml-measured ingredients are called out on apply, because USDA reports per 100 g
and density makes the two differ for oil, honey and cream.
The API key is held in browser local storage, never in the file. USDA
deactivates keys found in code repositories, and tools/ is in a public one.
`tools/ingredient-editor.html` and `tools/recipe-editor.html`. Single files,
opened in a browser: no server, no Python, no install. Files are read client
side and never uploaded; editing produces a download you put back yourself.
Both carry a live validation rail applying the same rules as `matbakh.py`,
and refuse to produce a download while any error stands — so a file cannot
leave the editor in a state the validator would reject.
The recipe editor drives activities, stations, note kinds and ingredients
from the lexicon and reference files, so a typo cannot enter the catalogue.
Bespoke verb wording stays available per action.
Per-serving nutrition can be computed from step amounts against the 156
ingredients carrying per-100g figures, and reports what it could not include
rather than silently under-reporting.
2026-07-30d — hero shows the whole photo
The pre-commit hero used `object-fit: cover`, which crops the photo to fill
the band — on a phone this cut the top or bottom off the dish. Changed to
`object-fit: contain`, so the whole photo is visible, letterboxed against the
warm background. One property; the 318px band is unchanged.
An earlier attempt also made the band height follow the photo. That broke
scrolling on the recipe screen and was reverted. If the fixed band is
revisited, test scrolling on a real device before shipping — the failure was
not visible in preflight.
app-iphone.html and recipe-screen-iphone.html. Step photos, shorts posters and
the resume thumbnail still use `cover`; cropping is right for a thumbnail.


## 2026-07-30d — hero shows the whole photo

- The pre-commit hero used `object-fit: cover`, which crops the photo to fill
  the band — on a phone this cut the top or bottom off the dish. Changed to
  `object-fit: contain`, so the whole photo is visible, letterboxed against the
  warm background. One property; the 318px band is unchanged.
- An earlier attempt also made the band height follow the photo. That broke
  scrolling on the recipe screen and was reverted. If the fixed band is
  revisited, test scrolling on a real device before shipping — the failure was
  not visible in preflight.
- app-iphone.html and recipe-screen-iphone.html. Step photos, shorts posters and
  the resume thumbnail still use `cover`; cropping is right for a thumbnail.

## 2026-07-30c — content data moved to the vault

- 179 ingredients imported from BirdRock: bilingual names, per-100g nutrition
  on 156, pack sizes on 52. Scaling class derived from `type`, never from names
  — "Bell pepper" and "Green pepper" would have been mis-classed as seasoning
  by any name rule. Cost, supplier and pack price dropped; prices come from the
  market feed.
- The full reference now lives in the vault at `03-catalogue/ref/`. Only
  `content/ref/ingredients.sample.yaml` (the 12 curated entries) is tracked, so
  the schema stays reviewable and the demo recipe still validates on a fresh
  clone with no vault present.
- `matbakh.py` resolves the vault via `--vault`, `MATBAKH_VAULT`,
  `content/vault.path`, then the default sibling path — and prints which source
  it used on every run. Recipes are read from the vault and the repo together.
- Guards extended: the hook and `scan.sh` both block the full reference, and
  `.gitignore` covers it plus `vault.path`.
- `content/README.md` added, documenting the split.

## 2026-07-30b — guards simplified, import path added

- Pre-commit hook cut from 118 lines to 59. Content scanning removed: it caused
  three false positives (tokens.css, media.js twice) and caught nothing real.
  The hook now checks filenames and counts only — business documents, credential
  files, the vault marker, and recipe files beyond the template and demo.
- Hook shebang changed to `#!/bin/bash`. `#!/usr/bin/env bash` cannot resolve
  under GitHub Desktop's restricted PATH.
- The deeper content scan remains in `scan.sh`, which is advisory and run on
  demand, where a false positive costs nothing.
- `import-screen.sh` added. The repository is now the system of record for
  prototypes; Claude Design is a drafting tool with a one-way import. The script
  applies all four required transformations — kebab-case name, asset path
  rewrite, MEDIA() fallback patch, noindex stamp — and prints the manifest
  snippet to add.

## 2026-07-30 — 2026.07.30

- Repository restructured: prototypes moved to `prototypes/` with kebab-case
  filenames, so shared links no longer contain `%20`.
- `index.html` is now generated from `manifest.yaml` by `build.py`. Adding a
  screen is a manifest edit, not an HTML edit.
- Preflight checks added: missing assets, orphaned prototypes, filename spaces,
  colour drift against `design/tokens.css`, changelog freshness, gitignore
  guards.
- `design/tokens.css` added as the canonical palette. Audit currently reports
  two terracottas and five off-whites in use; consolidation pending.
- `noindex` stamped on every prototype while `project.public` is false.
- Recipe content schema added under `content/` — lexicon-based, locale-neutral,
  validated. Shopping list and technique shorts now derive from step data.
- `ios-frame.jsx` moved to `design/source/` — it is a Claude Design build
  artefact, referenced by no prototype at runtime.

## 2026-07-29 — pre-restructure

- Cook mode and pre-commit recipe screen, native scrolling, audible timer
  alarm, editable shopping list, device mode.
