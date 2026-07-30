# content

The recipe schema, its validator, and the controlled vocabulary.

## What is here and what is in the vault

| Tracked here | In the vault |
|---|---|
| `matbakh.py` — validator and locale builder | `ref/ingredients.yaml` — all 179, with nutrition |
| `lexicon/` — activities, stations, note kinds, units | `recipes/*.yaml` — the catalogue |
| `ref/ingredients.sample.yaml` — the 12 curated entries | `ref/convert_ingredients.py` |
| `recipes/_template.yaml` and one demo recipe | |

The split is deliberate. Anyone cloning this repository can read the schema,
validate the demo recipe and understand the data model — without the catalogue
or the full reference, which are work product.

## Finding the vault

Resolution order, first hit wins:

1. `--vault PATH` on the command line
2. `MATBAKH_VAULT` in the environment
3. `content/vault.path` — one line holding the path (gitignored; see
   `vault.example.path`)
4. `../../matbakh-private/03-catalogue` — the default sibling layout

With no vault reachable it falls back to the tracked sample and says so, rather
than failing. Every run prints which source it used, so you always know whether
you validated against 179 ingredients or 12.

## Usage

    python3 matbakh.py check                    # validate everything reachable
    python3 matbakh.py check recipes/x.yaml     # one recipe
    python3 matbakh.py build recipes/x.yaml ar  # resolve for a locale
    python3 matbakh.py gaps                     # untranslated strings

## Adding a recipe

Copy `recipes/_template.yaml` into the vault's `recipes/` folder, not here.
The validator picks it up from either place; the guards stop it being committed.
