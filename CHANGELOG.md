# Changelog

Newest first. One entry per publish. `build.py` warns if a prototype is newer
than the top entry, so this cannot quietly fall behind.

Format: `## YYYY-MM-DD — release`

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
- Deep links retargeted, `#cook/1`–`#cook/9`, and the hash follows the cook.

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
