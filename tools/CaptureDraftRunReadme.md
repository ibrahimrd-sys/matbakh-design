# capture-draft — how to do a real run

*Written 1 October 2026, before the first run against the live API.*

**Last updated:** 2026-10-06 — §6: a chef's rewrites of captures go to `09-reviewed-captures/` (release 2026.10.06). Earlier, 2026-10-04: §7: checks F–H (duplicate entries, temperature units, list against method) added to the pre-filter design, with the Boeuf Bourguignon capture as their worked example (release 2026.10.04). Earlier, 2026-10-01: the fallback turned off (release 2026.10.01c); §7, the pre-filter engine's design, added; captures go to `08-unreviewed-captures/`; the consumer-app idea logged as HD-07.

This is the procedure for running `tools/capture-draft.py` against the real
Anthropic API: first once to prove it works, then as a routine. What the tool is,
and what it refuses to do, is in `ToolsReadme.md` § capture-draft.py. This file
says how to run it, and §7 records the agreed design of the next piece, a
pre-filter for its output, which has not been built.

**As of writing, it has been tested offline only** — page extraction, images,
the write guards, the error messages, and the request against a mocked API.
The first real run is the one below.

---

## 1. Once per machine

**Python and the SDK.** From any terminal:

    python3 --version             # 3.10 or newer
    pip install anthropic

On Windows, `python3` may be `python` or `py -3`; use whichever answers.

**An API key.**
1. Sign in to the Anthropic Console (`console.anthropic.com`) and create a key
   under **API keys**. Name it so it can be found and revoked later — for example
   *matbakh-capture-draft*.
2. **Set a monthly spend limit** for it under **Billing** or **Limits**. A few
   dollars covers hundreds of drafts. A limit means a mistake costs that much and
   no more.
3. Copy the key once, into your password manager — the vault's `06-credentials/`
   if that is where credentials live. Not into any file in this repository, not
   into a chat, not into a note.

**Never write the key into a file in this repository.** It is public, and a
published key is a key anyone can bill to you. If one is ever committed, revoke
it in the Console straight away — deleting the commit is not enough.

---

## 2. Each session: put the key in the environment

Set it for the current terminal only. When the terminal closes, it is gone.
The commands below prompt for the key, so it never lands in your shell
history.

**Git Bash:**

    read -s -p "Anthropic key: " ANTHROPIC_API_KEY && export ANTHROPIC_API_KEY && echo

**PowerShell:**

    $env:ANTHROPIC_API_KEY = Read-Host "Anthropic key" -MaskInput

Then run everything below from the `matbakh-design` folder, in the same
terminal.

---

## 3. The first run, step by step

Work through these in order. Each step proves one thing before the next one
spends money.

### Step 1 — a dry run, with no key needed

    python3 tools/capture-draft.py https://www.themealdb.com/meal/52771 --dry-run

**Expect:** the page text, ending in the line
`[schema.org Recipe data found: no]`, which proves fetching works. No API call is
made.

### Step 2 — a URL, for real

Captures go in the vault's **`08-unreviewed-captures/`**. It is a top-level
folder, kept apart from `03-catalogue/` on purpose, and git ignores everything
in it except its README (Ibrahim, 1 Oct 2026; see its `CapturesReadme.md`).
The tool refuses this repository and `03-catalogue/` in any case.

    python3 tools/capture-draft.py https://www.themealdb.com/meal/52771 --format text --out ../matbakh-private/08-unreviewed-captures/arrabiata.txt

**Expect, in about ten to thirty seconds,** a plain-text draft that opens with
`# UNREVIEWED MACHINE TRANSCRIPTION…`, then:

- **TITLE** *Spicy Arrabiata Penne*;
- **INGREDIENTS**, eight lines, quantities as the page gives them — `1 pound
  penne rigate`, `1/4 cup olive oil` …;
- **STEPS**, three, worded as on the page;
- **NOTES FOR THE CHEF**, which **should flag kosher salt** — the method uses it
  and the ingredient list does not. If the note is there, the model is reading
  the recipe rather than just copying lines.

### Step 3 — the same URL as JSON

    python3 tools/capture-draft.py https://www.themealdb.com/meal/52771

**Expect** the same content as JSON, with a `_draft` block carrying `warning`,
`source`, `captured`, `model` and `request_id`. Keep the `request_id` if
anything looks wrong; it is what Anthropic support asks for.

### Step 4 — an image

Photograph a page of a printed cookbook, or screenshot a recipe, and save it as
`.jpg` or `.png`:

    python3 tools/capture-draft.py C:/Users/<you>/Pictures/cookbook-page.jpg --format text

**Expect** the page's ingredients and method, with anything the camera blurred
or cut off listed under **NOTES FOR THE CHEF** rather than guessed.

### Step 5 — check the bill

In the Console under **Usage**, the three calls should come to a few cents.
If they cost much more than that, stop and look before running it routinely.

---

## 4. Checking a draft

The draft is a transcription, so check it against the source, not against how
the dish ought to be made.

| Check | Why |
|---|---|
| Every ingredient line in the source is in the draft, and nothing else is | The model is told never to add or complete. An extra line is a fault |
| Quantities and units are **as written** — `1 1/2 cups`, not `360 ml` | Conversion is the chef's job, done against the ingredient reference |
| Steps follow the source's division — not split, not merged | Splitting into pages and tiles is the chef's judgement under the authoring standard |
| Anything unreadable or inconsistent is in the notes, not filled in | A guessed quantity that looks real is worse than a gap |
| `found_recipe` is `false` when the page held no recipe | Redirects and video pages produce exactly this |

**A wrong draft is cheap: correct it by hand, or run it again.** What must never
happen is a draft treated as a recipe. It goes to a chef, who rewrites it to
`design/authoring-standard.md` in `recipe-editor.html`, and the result is
test-cooked before it goes anywhere near the catalogue.

---

## 5. When it fails

Every failure prints one line beginning `capture-draft:`.

| Message | What to do |
|---|---|
| `no credentials. Set ANTHROPIC_API_KEY…` | The key is not set in this terminal. Redo §2 |
| `the API rejected the credentials…` | The key is mistyped, revoked, or from another account. Check it in the Console |
| `rate limited. Try again in a minute.` | Wait a minute. If it keeps happening, the account's limits are low |
| `API error 4xx/5xx: …` | 5xx is Anthropic's side — retry later. 4xx with a spend-limit message: the limit from §1 was reached |
| `the API rejected the request: …` | Usually an image that is too large. Resize it to under about 5 MB and retry |
| `could not reach the API…` | No connection, or a proxy is in the way |
| `the model declined this source…` | The model declined it on safety grounds, and nothing was retried on another model (the tool has no fallback). Try a different source; if an ordinary recipe is being declined, keep the request and report it |
| `the response was cut off or unreadable…` | Rare. Retry once, and if it repeats, keep the `request_id` |
| `… returned HTTP 403` (or 404, 429) | The site blocks scripts. Screenshot the recipe and pass the image |
| warning: `… redirected to …` | The site sent you elsewhere — BBC Good Food sends Egypt to its regional homepage. Expect `found_recipe: false`; screenshot instead |
| warning: `the page has almost no text` | A TikTok, Instagram or YouTube page. Screenshot the caption |
| `the page is … characters, over the … limit` | Screenshot the recipe |
| `refusing to write into …` / `refusing a .yaml --out` | Working as intended. Pick a folder from §3 step 2 and a `.json` or `.txt` name |

---

## 6. After the first run

Record it in the PM log's §13 — the date, that the tool ran against the live
API, the cost of the three calls, and anything that did not match the
*Expect* lines above. Then, if it is to become routine, one open question goes
to Ibrahim:

- ~~**where drafts live**~~ — **decided 1 Oct 2026:** `08-unreviewed-captures/`
  in the vault, top-level, ignored by git apart from its README;
- ~~**where a chef's rewrites live**~~ — **decided 6 Oct 2026:**
  `09-reviewed-captures/` in the vault, beside `08-unreviewed-captures/`,
  ignored by git apart from its README. A rewrite is the chef's working copy,
  not a recipe: the recipe is authored fresh in `03-catalogue/recipes/`, and
  nothing is copied across;
- **whether a draft is kept**, and now its rewrite too, after the recipe is authored. It is a third-party
  transcription, so the case for deleting it is its copyright, and the case for
  keeping it is provenance.

Until that is settled the tool stays outside every workflow, as it is now.

---

## 7. Pre-filter engine for capture-draft.py (design, not yet built)

*Design agreed by Ibrahim, 1 October 2026; checks F–H added at Ibrahim's
request, 4 October 2026. **Not built.** The next step is a separate build brief, which is
not part of this document.*

### What this is, and what it is not

**It is a triage layer for the chef's queue, not authoring.** It reads a draft
that `capture-draft.py` has already produced, and attaches structural flags so
a chef can review the draft faster. The chef still reviews every draft, rewrites
it to `design/authoring-standard.md`, and the dish is still test-cooked. None of
that changes.

**It is not the consumer capture-and-author app** — an app in which cooks capture
recipes that are then authored to Matbakh's specs. That idea was discussed on
1 October 2026 and **logged the same day as HD-07** in the competitor study's
register (vault, `02-strategy/competitor-study-combined.md`, Appendix A). It is a
separate matter entirely:

- **Open, unapproved, and explicitly not being planned toward.**
- **It would reopen settled positions:** import-your-own-recipes, which is
  recorded as structurally unavailable (competitor study, Appendix A §3); the
  test-cooked promise; and one recipe per dish (§9).

The pre-filter is a smaller, approved-to-design extension of an internal tool.
**It does not move toward automating authoring,** and building it is not a step
toward that app. A future reader should not treat one as progress on the other.

### Purpose

It speeds up the chef's review of captured drafts. It:

- **never decides** which drafts a chef sees;
- **never writes** to `03-catalogue/`;
- **never assigns tags,** and never breaks a recipe into tiles, pages or
  activities.

Tags and the breakdown stay the chef's judgement calls, consistent with
`philosophy.md` §11's test — *could a careful person disagree?* — and with the
capture tool's original boundary: its job ends at a rough draft.

### The checks

All eight are structural. None is a judgement call.

**A. Completeness.**
- Every ingredient has a name, a quantity and a unit, or is flagged as missing
  one — never silently guessed.
- Every step has real instructional text.
- There is at least one ingredient and one step.

*Example output: "3 of 8 ingredients have no quantity in the source."*

**B. Plausibility.** Flags quantities wildly outside a sane range for their unit,
using **thresholds set by a chef**, not invented by the engine. It only flags:
it never corrects or discards anything.

**C. Duplicates against the catalogue.** It fuzzy-matches the captured title and
key ingredients against what is already authored in `03-catalogue/`, reading
only. This is the one check with a direct economic payoff: it catches *"this
looks like a dish we already have"* before a chef spends time on it.

**D. Unmapped ingredients.** It fuzzy-matches every captured ingredient against
`ref/ingredients.yaml` and flags anything not found. That shows how much new
reference work a capture would need.

**E. Source-type carryforward.** It passes on what `capture-draft.py` already
knows about where a draft came from, instead of losing that context:
- the site's own schema.org recipe data;
- a screenshot or photograph;
- a page that behaved oddly — a geo-redirect, or almost no text.

*Checks F–H added 4 October 2026, at Ibrahim's request. They work within the
same limits as A–E: they only flag, they never correct anything, they give no
score, and they hide nothing from the chef.*

**F. Duplicate ingredient entries.** It lists every entry for the same
ingredient across the list's sections, and shows their sum. A Matbakh recipe
lists each ingredient once. **The chef consolidates; the check never merges
anything.** If an entry has no quantity, or the units cannot be added, the check
shows the entries without a total. It never guesses a total.

*Example output: "butter — 1 tbsp (onions) + 2 tbsp (mushrooms) = 3 tbsp."*

**G. Temperature units.** It flags a temperature that has no unit, or a unit
other than Matbakh's convention, which is °C (`philosophy.md` §5.1). **It never
converts.**

*Example output: "Step 1: 450° has no unit. Step 14: 325°F is not °C."*

**H. List against method.** For each ingredient, it adds up the quantities the
steps use and flags any ingredient whose total does not match the list. If a
quantity in a step cannot be read, it is flagged as unreadable, not guessed.

*Example output: "butter — list 3 tbsp; steps use 1 + 2 + 1 = 4 tbsp."*

**Worked example for F, G and H: the Boeuf Bourguignon capture.**
`08-unreviewed-captures/Beef_Bourguignon.txt` in the vault is a capture of Julia
Child's Boeuf Bourguignon from garlicandzest.com, made 4 October 2026. All three
new checks would flag it:

- **F:**
  - butter: 1 tbsp + 2 tbsp = 3 tbsp;
  - olive oil: 1 + 1 + 1 tbsp = 3 tbsp;
  - thyme: 5–6 sprigs + 3–4 sprigs = 8–10 sprigs;
  - bay leaf: 2 + ½ = 2½;
  - parsley: 4 sprigs, plus a chopped garnish with no quantity, so there is no
    total;
  - beef stock 2–3 cups and beef broth ½ cup are named differently. They would
    total 2½–3½ cups if they count as one ingredient (see *Open* below).
- **G:**
  - steps 1 and 6 give 450° and 325° with no unit;
  - step 14 gives 325°F, which is not °C.
- **H:**
  - butter: the list has 3 tbsp, but the steps use 1 (step 9) + 2 (step 10) +
    1 (step 11) = 4 tbsp;
  - olive oil: step 10's "½1 tablespoon" cannot be read, so it is flagged
    unreadable and no total is given;
  - mushrooms: step 10's "half 1 pound" cannot be read either.

The capture's own *Notes for the chef* already point out the butter conflict,
the missing units and the garbled mushroom step, but only because the model
happened to notice them. F–H would catch them on every capture.

### Non-goals, stated plainly

- **No breakdown into tiles, pages or activities.**
- **No tag assignment.**
- **No pass/fail verdict, and no composite score of any kind.** A single score
  would, over time, risk becoming an approval signal. That defeats the purpose,
  which is that a person reviews every draft.
- **No filtering of which drafts reach a chef.**
- **No write path to `03-catalogue/`.** The output stays attached to the raw
  capture in `08-unreviewed-captures/`.

### Open, and not settled by this design

- ~~**Where the drafts folder is.**~~ **Decided 1 Oct 2026:**
  `08-unreviewed-captures/`. The design as first written named `04-drafts/`,
  which would have collided with the vault's `04-research/`. Ibrahim chose a
  top-level folder, not one nested under `03-catalogue/`, with a name that says
  the contents are unreviewed captures, not recipes in progress.
- **The chef-set thresholds for check B** do not exist yet. A chef has to set
  them; the engine must not invent them.
- **Whether a draft is kept** after authoring, from §6 above. It also decides how
  long a draft's flags are kept.
- **How F and H decide that two entries are the same ingredient** — for example
  *beef stock* and *beef broth, or stock*. Whether they use check D's mapping to
  `ref/ingredients.yaml` or exact names is not settled.
- **An ingredient used in the method but missing from the list** — for example
  the fresh thyme garnish in the Bourguignon example. H as specified compares
  quantities only. Whether to flag this is not settled.
