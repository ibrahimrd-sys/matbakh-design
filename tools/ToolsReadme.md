# Tools — the authoring editors and the capture-draft script

*Written 26 August 2026. One file per tool question; there is no second copy of
this document.*

**Last updated:** 2026-10-20 — `ingredient-editor.html` keeps the new `makes` field (`philosophy.md` §47). 2026-10-19: `ingredient-match.py` measured again after the reference grew to 436 entries. 2026-10-13: `ingredient-match.py` added, the third import check, and fixed three times the same day (form words, Arabic endings, مسحوق as powder, `=` whole-name aliases, ground spices accept powder); the ingredient editor gains *Other names* (aliases); `ingredient-lines.py` added, the second import check; `structured-data-check.py` fixed after its first real run: Arabic addresses, sitemap order and fallbacks, `--verbose`. 2026-10-12: `structured-data-check.py` added, the first import check (D-19). Earlier, 2026-10-06: the rewrites folder, `09-reviewed-captures/`, noted. 2026-10-01: `capture-draft.py` added; its fallback turned off; its captures folder and pre-filter design noted.

**Five** authoring tools and one research script. Four are single HTML files: open them in a browser, no
install, no server, no Python. The fifth, `capture-draft.py`, is a Python script
that calls the Anthropic API. It produces a starting draft for a chef and never
edits a recipe. `structured-data-check.py` authors nothing: it counts how many
recipe pages publish their own recipe data.

| File | Opens | For |
|---|---|---|
| `ingredient-editor.html` | the vault's `ref/ingredients.yaml` | the ingredient reference — units, conversions, nutrition, diet |
| `lexicon-editor.html` | `content/lexicon/activities.yaml` + `chrome.yaml` | the activity vocabulary and its Arabic |
| `recipe-editor.html` | a recipe + the lexicon + the reference | authoring and editing recipes |
| `translator.html` | recipe files + `chrome.yaml` | handing prose to a collaborator without exposing structure |
| `capture-draft.py` | a URL or an image of a recipe | a rough, unreviewed draft of someone else's recipe, for a chef to rewrite — **never a Matbakh recipe** |
| `ingredient-lines.py` | ingredient lines, or a CSV of them | each line split into quantity, unit and ingredient, in Arabic, English and French |
| `structured-data-check.py` | a list of recipe URLs | counts of which pages carry schema.org Recipe data, and how complete it is — **no recipe text kept** |

**Nothing is uploaded by the four editors.** Files are read in the browser and stay on your machine.
That is also why they cannot save in place — a web page may not write to disk.
You download the edited file and put it back in the vault yourself.

Author against `design/authoring-standard.md`, not against memory — it documents
every error and warning these tools enforce, and what to do about each one.

## ingredient-editor.html

Open `matbakh-private/03-catalogue/ref/ingredients.yaml`.

Search in English or Arabic, edit any field, add or delete ingredients. The
right-hand rail lists every rule `matbakh.py` would enforce, live, and the
download button stays disabled while any error remains — so the file cannot
leave here in a state the validator would reject.

Ingredients missing a scaling class are the ones to fix first; without it,
servings cannot be computed at all.

**Other names** (13 Oct 2026) holds the ingredient's **aliases**, one per line:
the French word, the everyday Arabic, an English variant — *lait*, *حليب*,
*EVOO*. They are written as an `aliases:` list straight after `name`, on every
entry (empty when there are none), and imports are matched against them. A
name may contain a comma. `matbakh.py check` reports an alias claimed by two
ingredients as an error.

### Diet — the prerequisite for recipe tags

Every ingredient carries a `diet` list: `[meat, poultry]` on chicken, `[dairy]`
on ghee, `[]` on onion. From these, `matbakh.py` derives `vegetarian`, `vegan`,
`gluten_free` and the full allergen list for every recipe — so those are never
typed per recipe and cannot drift out of step with an ingredient list that
changed after the tag was written.

**Unset is not the same as empty.** Empty means *contains none of these*, which
is a real answer. Unset means unknown, and any recipe using an unset ingredient
has its dietary tags withheld entirely — a vegetarian claim that is wrong once
costs a guest their dinner and the filter its credibility.

**Propose for all** fills what it can from name rules plus a table of the cases a
name cannot reveal — worcestershire is fish, bechamel is dairy and gluten, pine
nuts are nuts. On the reference as it stood when this was written it resolved all
but two, those two being junk rows that came across from BirdRock and should be
deleted. The button label carries a live count; for the current reference totals
run `matbakh.py status` rather than trusting a number typed into a document.

Check what it proposed. These are name rules, not knowledge of your shelf.

### Measuring another way

`convert` records **one** number per ingredient and derives the rest:

- `cup_g` — what one cup weighs. A tablespoon is that over 16, a teaspoon over
  48. Those are never stored, so there is one figure to keep right instead of
  three that can drift apart.
- `piece_g` — what one of them weighs, for things a cook counts.

This is what turns "2 tbsp ghee" and "2 onions" into grams, and grams are what
nutrition is computed from. Without it those ingredients contribute nothing to
a recipe's per-serving figures, and `matbakh.py` warns when that is the case.

**Fill common conversions** applies well-established weights to whatever it
recognises by name and reports what it set, leaving anything already filled
alone. They are a starting point: how finely something is ground, and whether
it is packed or spooned, moves flour by 20% and brown sugar by more.

### Nutrition lookup

Two sources, tried in order.

**Offline first.** Open `nutrition-db.json` through the same button as the
YAML — a USDA export of 6,389 foods, each carrying kcal, protein, carbohydrate,
fat, saturated fat, cholesterol, sodium and fibre per 100 g. No key, no network,
no waiting. **It lives in the vault at `03-catalogue/ref/nutrition-db.json`,
beside `ingredients.yaml`** — the same folder `matbakh.py` resolves for the
ingredient reference. It is loaded through the file picker, not by path, so
moving it breaks nothing; the reason to keep it there is that it is the only
copy and the vault is what gets backed up.

**USDA online second**, for anything the export does not hold. That needs a key
and a connection; see below.

Search plainly either way. USDA indexes *Onions, raw* rather than *red onion*,
and *Jute, potherb* rather than *molokhia*. A more general term finds more.

### USDA nutrition lookup, online

**Look up in USDA** searches FoodData Central for the ingredient in front of
you and fills the five figures from whichever result you pick. **Fill every gap**
walks the ingredients that have no nutrition at all, one after another.

Read the badge on each result before choosing it:

- **Foundation** and **SR Legacy** report per 100 g, which is the basis this
  reference uses. Prefer these.
- **Branded** reports per serving. Taking those figures at face value would be
  wrong, so they are flagged in red.

Two things it cannot know for you. USDA reports per 100 **g**; ingredients
measured in **ml** — oil, honey, cream — need adjusting for density, and the
tool says so rather than pretending otherwise. And USDA indexes plain names:
*Onions, raw* rather than *red onion*. A more general search term finds more.

### The API key

It works immediately on USDA's shared `DEMO_KEY`, which allows only a handful
of requests an hour — enough to try, not enough to fill many gaps in a sitting.
A free key from **api.data.gov** lifts that.

**The key is never written into this file.** It is kept in your browser's local
storage on this machine only. That is deliberate: USDA deactivates any key it
finds published in a code repository, and `tools/` is in a public one.

## lexicon-editor.html

Open `activities.yaml` and `chrome.yaml` together from `content/lexicon/` — Ctrl
to select both. chrome.yaml supplies the stations and the locale list, so the
editor needs it. Add a recipe file too and the list marks which activities that
recipe actually uses.

The check that earns its keep is **collision detection per dialect**. Two
activities sharing a word put identical text on two different tiles, and a cook
reading Arabic cannot tell the steps apart however different the English keys
look. Eight of these were found during the CSV merge — toss/stir in Egyptian,
zest/peel and grill/roast in Levantine and Gulf. The field turns red as you type,
and the file cannot be saved while one stands.

Each activity shows a **tile preview at 44px and an arc strip at 17px**, the two
sizes an icon has to survive.

Dialect fields left blank fall back — ar_gulf → ar_eg → ar — so partial coverage
is fine, and the rail reports what is missing.

## recipe-editor.html

Open three files at once — hold Ctrl while clicking:

- `ingredients.yaml` from the vault
- `activities.yaml` and `chrome.yaml` from `content/lexicon/`

Add a recipe file too if you are editing one, or press **New recipe**. Each
file is recognised by its shape, so the order does not matter.

Activities, stations, note kinds and ingredients are all dropdowns fed from
those files, so a typo cannot enter the catalogue. Bespoke wording is still
available per action when the lexicon would flatten something worth keeping.

**Compute from the ingredients** fills in per-serving nutrition by adding up
what the steps actually use and dividing by the base yield. It reports what it
could not include — an ingredient with no nutrition figures, or one measured in
whole units where grams are unknown.

## translator.html

For a collaborator translating into their own language. Open the recipe files
together with `chrome.yaml` from `content/lexicon/`, then **Add photos** if the
`assets` folder is available.

**A translator cannot break a recipe.** The tool walks each file for per-locale
string maps and edits nothing else — ingredient ids, amounts, scaling classes,
activity keys and every other structural field are unreachable from it. Verified
against the demo recipe: 31 prose units found, zero structural fields exposed,
and a round-trip that leaves every tile byte-identical.

**Doneness cues show their photograph.** A cue describes a picture — *straw-gold
at the edges, one shade past this is bitter* is about `garlic-butter-pan.jpg`.
Translating it without seeing the image is guesswork, so the tool pairs them and
says so when the photos have not been loaded.

**Repeated phrases are translated once.** Qualifiers are where this pays: one
recipe already contains *fine*, *covered*, *into pieces*, *skin-side*. Across
500 recipes the same few dozen recur constantly, so the tool remembers each
translation and offers it wherever the phrase appears again.

**Each field says what it is for.** A `label` is read at a glance on a timer; a
`why` is the most important sentence on the browse card; a `qualifier` sits
beside a verb on a small tile and must stay short. The translator sees the job,
not the field name.

Ctrl+Enter saves and advances. **Next untranslated** skips to the first gap.

## capture-draft.py

*Added 1 October 2026. Competitor study HD-02 (chapter 11, Honeydew).*
**How to do a real run — key, first run, checking a draft, every error message:
`CaptureDraftRunReadme.md`.** Captures go in the vault's `08-unreviewed-captures/`; a chef's rewrites of them go in `09-reviewed-captures/`.
Its §7 holds the design of a planned **pre-filter engine** — triage flags for the
chef's queue, with no score and no filtering. It is not built, and it is not a
step toward automating authoring.

Paste a recipe URL or give it a photo of a recipe — a screenshot, a cookbook
page — and it returns a **rough draft for a chef**. The draft has the ingredients,
with quantity and unit exactly as the source wrote them, and the steps as plain
text, divided the way the source divides them. It also has notes on anything it
could not read or that does not add up, such as an ingredient used in the method
but missing from the list.

    python3 tools/capture-draft.py https://example.com/recipe          # JSON
    python3 tools/capture-draft.py cookbook-page.jpg --format text     # plain text
    python3 tools/capture-draft.py URL --out ../matbakh-private/08-unreviewed-captures/x.json
    python3 tools/capture-draft.py URL --dry-run                       # no API call

**It is a starting draft and nothing more.** It does not choose activities,
stations, tiles, pages, tags or cuts, and it computes no nutrition or cost —
that decomposition is the chef's judgement, not something to automate. A
captured recipe becomes a Matbakh recipe only when a person rewrites it to
`design/authoring-standard.md` and it is test-cooked.

**What it can and cannot write.** It writes nothing except what it prints and an
optional `--out` file. `--out` refuses:
- any path inside this repository — it is public, and a draft is someone else's
  recipe;
- anything in the vault's `03-catalogue/`;
- a `.yaml` name, so a draft can never pass for a recipe file.

Each draft opens with an *UNREVIEWED MACHINE TRANSCRIPTION* warning, and gives
its source and the time it was captured.

**How it reads a source.**
- **A URL:** it fetches the page and sends its visible text. If the page also
  publishes schema.org recipe data, it sends that too.
- **An image** (`.jpg`, `.png`, `.gif`, `.webp`): it goes straight to Claude's
  vision.
- **One API call** to Claude Opus 5.5 returns a fixed JSON shape. The prompt
  says to transcribe and never invent, convert or scale.

**Where it falls short.**
- **Social-video links** (TikTok, Instagram, YouTube) render in the browser, and
  a plain fetch gets almost nothing. The tool warns you; screenshot the caption
  and pass the image.
- **Some sites redirect visitors from Egypt** to a regional homepage — BBC Good
  Food does. The tool warns when a page redirects, and the draft will say there
  was no recipe.
- **A page over 400,000 characters is refused, not cut down.** Screenshot the
  recipe and pass the image.

**Setup and cost.**
- **Install:** `pip install anthropic`.
- **Credentials:** `ANTHROPIC_API_KEY` in the environment, or an
  `ant auth login` profile. As with the USDA key above, **never write the key
  into a file in this folder.** `--dry-run` shows what would be sent, with no
  call and no key.
- **Cost:** each run is one API call, billed to the key — a few cents for a
  screenshot or a short page.
- **No fallback.** If the model declines a request on safety grounds, the tool
  stops with an error saying so; nothing is retried on another model. *(Until
  release 2026.10.01c it opted into the API's server-side fallback, which did
  retry. Turned off 1 Oct 2026 at Ibrahim's instruction, so that a decline is
  never a silent switch of model.)*

## structured-data-check.py

*Added 12 October 2026.* The first of the import checks in the PM log's §11 item 9
(D-19): before an import engine is built, how many Arabic recipe pages publish
schema.org Recipe data — JSON-LD or microdata — that an importer could read
without AI?

    python3 tools/structured-data-check.py urls.txt
    python3 tools/structured-data-check.py urls.txt --csv ../matbakh-private/04-research/sd-check-2026-10-12.csv

`urls.txt` holds one URL per line; `#` starts a comment. **Or let it pick the pages
from each site's own sitemap:**

    python3 tools/structured-data-check.py --site example.com --site example.org --per-site 10 --save-urls ../matbakh-private/04-research/sd-check-urls.txt

`--site` reads the sitemaps named in the site's `robots.txt`, or the usual
`/sitemap.xml` locations, keeps the URLs that look like single recipes, and picks
`--per-site` of them at random. The pick is repeatable: `--seed` fixes it, and
`--save-urls` keeps the list so the same sample can be checked again later.
Recipe-named sitemaps are read first. If the sitemap `robots.txt` names is gone,
it tries the standard locations; if a site has **no sitemap at all**, it takes
the recipe links on the home page instead — which favours featured recipes, and
the per-site line says so (*no usable sitemap; N home-page links*). A slow
sitemap gets one retry with a longer wait. `--verbose` shows every sitemap read.
Addresses with spaces or Arabic letters are encoded before fetching.
**Check the line it prints per site** — *N URLs, M look like recipes*. The
built-in guess only keeps URLs containing *recipe*, *recette*, `/r/` or *وصفة*,
so on a site whose recipe pages are named by dish alone the pool is small and
skewed; give that site its own pattern with `--match`. A listing page that slips
through reads as *none*, which counts against the site — glance at the saved
URLs before reading the totals.

For each page it reports
whether it was fetched, whether it carries a Recipe, and which fields it fills:
ingredient and step counts, the share of ingredient lines with a quantity
(Western or Arabic-Indic digits, or a fraction) and in Arabic, yield, times,
nutrition, image and video, and the page's **language** — as the page declares
it, else as the recipe declares it, else guessed from the ingredient lines
(Arabic script, French cooking words, otherwise English). It then totals per site
and **per language**, so Arabic, English and French sources can be compared
(decided 12 Oct: imports come from all three).

- **It keeps no recipe text.** The output is counts and yes/no flags only, so it
  can be filed anywhere and is not a copy of anyone's recipe.
- **It calls no AI service** and needs no key. Standard library only.
- **It is polite:** it skips anything a site's `robots.txt` disallows and waits
  between requests to the same site (`--delay`, 2 seconds by default).
- **A page with no Recipe is a result, not an error.** Social-video pages
  (TikTok, Instagram, YouTube) render in the browser and will read as *none*;
  they are not what this check measures.

## ingredient-lines.py

*Added 13 October 2026.* The parser for import step 2 (D-19): it splits an
ingredient line into **quantity** (and range), **unit** and **ingredient**, with
no AI.

    python3 tools/ingredient-lines.py "2 c. à soupe d'huile d'olive" "كوبين ونصف حليب"
    python3 tools/ingredient-lines.py --csv lines.csv --out parsed.csv

`--csv` reads a column named `line`; `--out` writes every input column plus
`qty`, `qty_max`, `unit`, `name`, `note` and `kind`. **Units** come out as one
key each — `g`, `kg`, `ml`, `cl`, `l`, `tsp`, `tbsp`, `cup`, `oz`, `lb`, `pinch`,
`clove`, `can`, `packet`, `piece`, `slice`, `bunch`, … — whatever the language
or abbreviation. **Kinds:** `measured` (a quantity and a unit), `count` (2 eggs),
`to_taste`, `no_quantity`, `heading` (*Pour la pâte :*), `unparsed`.

What it reads: digits, decimal commas, mixed and `½`-style fractions,
Arabic-Indic digits, ranges; number words in all three languages, the Arabic
dual (*كوبان*, *ليتران*) and *ونصف*; abbreviations and spelling variants
(*Tbsp*, *cuil. à s.*, *م ك*, *ملعقه صغيره*); size words before a unit (*heaping*,
*belles*); Arabic's *ingredient - quantity* order and preparation words written
before the quantity. **Capital `T` is a tablespoon, small `t` a teaspoon.**

**It never guesses.** A line it cannot split comes back with the whole line as
the ingredient, so it can still go on a shopping list as text.

**Measured 13 October 2026** on real lines from Arabic, English and French
recipe sites: **147 of 150 fresh lines right (98%)** with the parser frozen —
English 48/50, Arabic 49/50, French 49/50. The lines and the per-line verdicts
are in the vault (`04-research/step2-summary-2026-10-13.md`), not here: they
are other people's recipe text.

## ingredient-match.py

*Added 13 October 2026.* The matcher for import step 3 (D-19): it finds which
reference ingredient an imported ingredient name means, with no AI.

    python3 tools/ingredient-match.py "huile d'olive" "حليب سائل" "2 large eggs"
    python3 tools/ingredient-match.py --csv parsed.csv --out matched.csv

`--csv` reads a column named `name` — `ingredient-lines.py`'s output; `--out`
writes every input column plus `match` (the reference id, or empty) and
`matched_on` (the name or alias that matched). It reads the vault's
`ref/ingredients.yaml` the way `content/matbakh.py` finds it, or `--ref PATH`.

**How it matches.** Both sides are lower-cased and normalised — Arabic
diacritics and letter variants (أ إ آ → ا, ة → ه, ى → ي), the article ال,
English plurals, French accents. A reference name — English, Arabic, any
`aliases` entry, or the id — matches when **all its words are in the
ingredient's words**; the longest wins, so *garlic powder* finds `garlic_powder`,
not `garlic`. **A match is refused** when the ingredient has a *form* word the
matched name lacks — *powder*, *broth*, *stock*, *extract*, *syrup*, *sauce*,
*paste*, *flakes*, *vinegar* and the like, in all three languages (`FORM` in the
script) — so *chicken broth* never becomes a chicken; *salt* counts only as the
last word (*garlic salt*). Arabic dual, plural and final ة are normalised
(*بصلتان*, *بيضات*, *جزرة*), and *مسحوق* is read as powder, like *بودرة*. A ground
spice (an entry with `cls: seasoning`) accepts *powder*: *cumin powder* is cumin. **An
alias written `=pepper` matches only the whole name** — *pepper*, not *cayenne
pepper* (`authoring-standard.md` Appendix C). **It never guesses beyond that:** an ingredient it
cannot match comes back empty and stays on the shopping list as text.

**Measured 13 October 2026.** First run, on 961 real lines from 90 pages step 2
never used: 75% right, **6% matched to the wrong entry** — compounds falling back
to a word inside them. After the form-word rule and 74 new aliases, on 1,087
lines from 104 fresh pages with the matcher frozen: **79% right, 2% wrong**
(English 79%, Arabic 82%, French 75%). **A second round** (more form words, `=`
aliases, مسحوق) measured on 94 more fresh pages: **75% right, 2.7% wrong** — no
better on unseen pages; the errors left are mostly products named after an
ingredient (*egg noodles*, *cake mix*). After small fixes (ground spices accept
powder, 45 aliases), on 95 more: **81% right, 3.4% wrong** — misses fell, wrong
matches did not. After Ibrahim's review went into the reference (19 October,
436 entries), on 69 more English and Arabic pages, the matcher unchanged:
**88% right, 2.6% wrong** (English 92%, Arabic 83%). After that sample's review
(482 entries), on 68 more pages, mostly English: **90% right, 2.4% wrong**; after
the next (517), on 70 more: **90% right, 1.8% wrong**. The lines, the per-line verdicts and a review workbook are in
the vault
(`04-research/step3-summary-2026-10-13.md`), not here.

## What these do not do

*This section is about the four editors.* Comments in the original file are not preserved; the YAML is regenerated. Keep
that in mind for `_template.yaml` and the schema fixture, which are mostly
comment.

Each tool warns before you close the tab, but **there is no autosave**. Download
before you walk away.

---

*One README covers all the tools — four editors until 1 October 2026, then `capture-draft.py`. Until 26 August 2026 there were three
overlapping copies of this file in this folder — `README.md`, `tools-README.md`
and `translator.md`, each a superset of the last. This is the merge of all three;
the other two are gone.*

*The name is the project convention: a README carries something indicative, so
it can be told apart from the other thirteen in these two trees. See
`DIRECTORY.md §11`.*
