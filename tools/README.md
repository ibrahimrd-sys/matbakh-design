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

### USDA nutrition lookup

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
