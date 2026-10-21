# Recipe core — one engine under import and capture

*Written 20 October 2026 by Claude, at Ibrahim's request: "both, sharing one
core". Import plan step 5 (vault `02-strategy/import-test-plan-2026-10-12.md`)
and `CaptureDraftRunReadme.md` §7.*

> **Approved by Ibrahim, 20 October 2026, all five decisions below as proposed,
> and built 21 October.** One package, two tools, the existing scripts kept as thin
> command lines (their output checked unchanged); the estimate's gap taken on with
> a data pass — 103 entries given cup or piece weights and 22 given nutrition,
> lifting the share of samples 4–6's lines it can count from 27% to 74%; checks
> A, D, E, F, G, H built, B and C later; `capture-draft.py --from-page-data`
> added as an option, not the default; step 5's cases from the import plan, in
> `tests/run-tests.py` (25 of 25 pass). How each part works is in `ToolsReadme.md`.

## What it is

Steps 1–3 of the import plan built three separate scripts that each solve one
part of reading a recipe page: `structured-data-check.py` finds a page's recipe
data, `ingredient-lines.py` splits a line into quantity, unit and name, and
`ingredient-match.py` finds the line's reference entry. Step 3 passed on
20 October (90% right, 1.8% wrong). **The core puts these three, plus a
shopping list and an estimate, into one importable package,** so that two tools
use the same code:

| | **Import prototype** (step 5) | **Capture pre-filter** (§7) |
|---|---|---|
| Who | A cook's own copy of a recipe | A chef reviewing a draft |
| In | A recipe page URL | A `capture-draft.py` draft (JSON) |
| Out | Shopping list + estimate, labelled تقدير | Flags A, D, E, F, G, H on the draft |
| AI | **None** | None (the draft itself may come from AI) |
| User data | None in the prototype; R-16 when it reaches cooks | None — internal (HD-02) |

They stay **two tools** (import plan §6): the core carries no user data and no
API key, so neither tool brings the other's obligations with it.

## The package

`tools/recipe_core/`, standard library plus PyYAML (already used), no network
except the page fetch:

- **`page.py`** — fetch a page politely (robots.txt, a delay per site, size cap)
  and read its schema.org Recipe: JSON-LD first, then microdata. Returns title,
  author, yield, ingredient lines and steps **exactly as published**, or a plain
  *no recipe data* result — never a guess. Taken from `structured-data-check.py`
  and `capture-draft.py`, which each carry a copy today.
- **`lines.py`** — `ingredient-lines.py`'s parser, unchanged.
- **`match.py`** — `ingredient-match.py`'s `Matcher`, unchanged.
- **`basket.py`** — new: from matched lines to a **shopping list** and an
  **estimate** (below).
- **`checks.py`** — new: the pre-filter's structural checks.

The three existing scripts become thin command lines over the package, **with
the same options and the same output**, so every earlier measurement stays
repeatable.

## The shopping list (`basket.py`)

- One line per reference entry, quantities added when the units agree (2 + 1
  tbsp → 3 tbsp); when they do not, the entry shows both, never a guessed sum.
- **Unmatched lines stay on the list as text, never dropped** (D-19), marked as
  such.
- Purchase rounding is the reference's: `pack`, and `makes` for stock — *stock
  cubes ×2 (for 1 L)* (`philosophy.md` §6, §47).
- Lines that are not purchases (*water*, *for serving*) keep the source's words;
  the list does not decide what the cook already has. *(21 October: staples are
  on the list, set apart and unticked, by the reference's `staple` field —
  `philosophy.md` §48.)*

## The estimate

Calories, protein, carbohydrate and fat for the recipe and per serving,
**labelled تقدير, with every line it could not count listed by name.** A line is
counted only when both are known:

1. **its weight** — from g, kg, oz, lb directly; from ml, l, cups and spoons for
   an entry measured in ml; from cups, spoons or a count through the entry's
   `convert.cup_g` / `convert.piece_g`;
2. **its nutrition** — the entry's per-100 g/ml figures.

**The gap, stated plainly:** today only **5 of 554 entries** carry `convert`, and
402 carry nutrition. So *200 g beef* counts, but *2 cups flour* and *2 onions* do
not — they appear under *not counted*. The estimate is honest from the first
run; how much it covers depends on a data pass adding `cup_g` and `piece_g` to
the common entries (proposed below), not on code.

Servings come from the page's `recipeYield`; when it has none, the estimate is
for the whole recipe and says so.

## The pre-filter checks (`checks.py`)

As designed on 1 and 4 October, **flags only — never a correction, a score or a
filter.** Built now: **A** completeness, **D** unmapped ingredients (the matcher,
so D answers §7's open question: F and H decide *same ingredient* by the
reference entry, not by exact name), **E** source-type carryforward, **F**
duplicate entries with their sum, **G** temperatures without a unit or not in °C,
**H** list against method. **B** waits for a chef's thresholds; **C** (duplicates
against the catalogue) waits until the catalogue has more than its pilot
recipes.

One further use, proposed in the import plan §6 and offered here only as an
option: **on a page with good recipe data, `capture-draft.py` could build its
draft from `page.py` without an API call,** keeping the model for images and
pages without data.

## Tests

`ToolsReadme.md` gains a testing section for each tool, run against saved pages
so a run can be repeated offline. Step 5's proposed cases (import plan §3) are
the import prototype's: an English, an Arabic and a French page with data, a
page with none, a redirect or missing page, a range and a pinch. The
pre-filter's case is the Boeuf Bourguignon capture worked in §7.

## Decisions this needs from Ibrahim

1. **Approve the shape** — one package, two tools, the existing scripts kept as
   thin command lines.
2. **The estimate's gap** — accept *not counted* lines at first, and add `cup_g`
   / `piece_g` to the most-used entries as a data pass (proposed: the 100 entries
   that matched most lines across samples 4–6), the way nutrition was filled.
3. **Which pre-filter checks now** — A, D, E, F, G, H as above, B and C later.
4. **`capture-draft.py` without AI on pages with recipe data** — now, later or
   not at all.
5. **What step 5 must pass** before step 7 (the phone) — the test cases in the
   import plan, or others.
