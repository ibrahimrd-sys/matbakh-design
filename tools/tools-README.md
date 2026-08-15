# tools

Two authoring tools. Both are single HTML files: open them in a browser, no
install, no server, no Python.

**Nothing is uploaded.** Files are read in the browser and stay on your machine.
That is also why they cannot save in place — a web page may not write to disk.
You download the edited file and put it back in the vault yourself.

## ingredient-editor.html

Open `matbakh-private/03-catalogue/ref/ingredients.yaml`.

Search in English or Arabic, edit any field, add or delete ingredients. The
right-hand rail lists every rule `matbakh.py` would enforce, live, and the
download button stays disabled while any error remains — so the file cannot
leave here in a state the validator would reject.

Ingredients missing a scaling class are the ones to fix first; without it,
servings cannot be computed at all.

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

**Propose for all 179** fills what it can from name rules plus a table of the
cases a name cannot reveal — worcestershire is fish, bechamel is dairy and
gluten, pine nuts are nuts. Tested against the current reference it resolves 177
of 179; the two it cannot are the junk rows that came across from BirdRock and
should be deleted.

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
no waiting. Keep it in the vault beside `ingredients.yaml`.

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

## What these do not do

Comments in the original file are not preserved; the YAML is regenerated.

Both tools warn before you close the tab, but there is no autosave. Download
before you walk away.
