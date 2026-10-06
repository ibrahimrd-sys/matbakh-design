# Changelog

Newest first. One entry per publish. `build.py` warns if a prototype is newer
than the top entry, so this cannot quietly fall behind.

Format: `## YYYY-MM-DD — release`

## 2026-10-06 — capture-draft: where a chef's rewrites live

**A chef's rewrites of captures go to the vault's `09-reviewed-captures/`.**
Ibrahim decided this on 6 Oct 2026. The folder is at the same level as
`08-unreviewed-captures/` and comes one step after it. A rewrite is the chef's
working copy, not a recipe. The recipe is still authored fresh in
`03-catalogue/recipes/` and test-cooked, and nothing is copied across. Git
ignores the folder apart from its README. `CaptureDraftRunReadme.md` §6,
`ToolsReadme.md` and `DIRECTORY.md` now say so.

## 2026-10-04 — pre-filter design: checks F–H

`CaptureDraftRunReadme.md` §7 gains three checks, added at Ibrahim's request on
4 Oct 2026. They are still design only, not built:
- **F**, duplicate ingredient entries, listed with their sum. The chef
  consolidates them; the check never merges anything.
- **G**, temperature units: a temperature with no unit, or one that is not °C.
  It never converts.
- **H**, list against method: quantities used in the steps that do not add up to
  the ingredient list.

They work within the same limits as A–E: flags only, no correction, no score.
The worked example is the Boeuf Bourguignon capture of 4 Oct in the vault's
`08-unreviewed-captures/`. Two new open points: how F and H match an ingredient
named two ways, and whether an ingredient the method uses but the list leaves
out should be flagged.

## 2026-10-01e — the consumer capture-app idea logged as HD-07

`CaptureDraftRunReadme.md` §7 now names the consumer capture-and-author idea by
its register ID, **HD-07** — REOPENS, open, unapproved and not planned toward —
and keeps it distinct from the pre-filter engine. The register entry itself is
in the vault, at Ibrahim's request, 1 Oct 2026.

## 2026-10-01d — capture-draft: where captures live, and the pre-filter design

**Captures go to the vault's `08-unreviewed-captures/`** — Ibrahim, 1 Oct 2026.
It is a top-level folder, kept apart from `03-catalogue/` so that unreviewed
content stays away from authored content. Git ignores it apart from its README.
`CaptureDraftRunReadme.md`, `ToolsReadme.md` and the script's usage line now use
it.

**`CaptureDraftRunReadme.md` §7: the pre-filter engine, designed and not built.**
It is a triage layer for the chef's queue. Five structural checks:
- completeness;
- plausibility, against thresholds a chef sets;
- duplicates against the catalogue;
- ingredients missing from the reference;
- where the draft came from.

It has no score or verdict, filters nothing, and has no write path. The section
says plainly that it is **not** the consumer capture-and-author idea, which stays
open, unapproved and not planned toward. Building it needs a separate brief.

## 2026-10-01c — capture-draft: the fallback turned off

**`tools/capture-draft.py` no longer opts into the API's server-side fallback.**
If the model declines a source on safety grounds, the tool now stops with an
error that says so. Before, the request was re-run on another model without
saying. The call moves from the beta endpoint to the standard
`client.messages.parse`; the model, effort and output schema are unchanged.
Ibrahim's instruction, 1 Oct 2026 — step 5 of the Recime/Honeydew/Pepesto usage
plan. `ToolsReadme.md` and `CaptureDraftRunReadme.md` are updated to match.

## 2026-10-01b — capture-draft: how to do a real run

**`tools/CaptureDraftRunReadme.md`**, written before the tool's first run
against the live API. It covers:
- **the key** — environment only, prompted for so it stays out of shell
  history, with a spend limit;
- **a five-step first run,** dry run first, each step with its expected output;
- **how to check a draft** against its source;
- **every error message** the tool prints, with its fix.

**Two of the tool's error messages are corrected.** They told the user to copy
the recipe into a text file, which the tool cannot read; they now say to pass a
screenshot. Linked from `ToolsReadme.md`, with a row in `DIRECTORY.md` §7.

## 2026-10-01 — capture-draft: a rough recipe draft from a URL or image

**`tools/capture-draft.py`, an internal authoring tool** (competitor study HD-02,
from chapter 11, Honeydew). Give it a recipe URL or a photo of a recipe, and it
asks Claude for a rough draft: ingredients with quantities and units as written,
steps as plain text, and notes for the chef. The draft is printed as JSON or
plain text, for a chef to rewrite and test-cook.

- **It never touches the schema:** no activities, tiles, tags, cuts, nutrition
  or cost.
- **It never writes into this repo or the vault's `03-catalogue/`.** An `--out`
  file pointed at either, or given a `.yaml` name, is refused.
- **The API key comes from the environment,** never from a file.

Documented in `tools/ToolsReadme.md`, with a row in `DIRECTORY.md` §7. Nothing
in the app or the authoring pipeline calls it.

## 2026-09-30d — which activities get a timer: confirmed

**`philosophy.md` §42.** The attendance classification is confirmed, with `boil`
moved to context-dependent — pasta water can be left; milk boils over. That gives
17 unattended, 14 attended, 44 no-time and 6 context-dependent. The file is
renamed `design/activity-attendance.md`, and the authoring standard now points
to it. Not yet in `activities.yaml` (E-14).

## 2026-09-30c — the snapshot cadence confirmed

**`philosophy.md` §41.1**, an amendment appended after §41: §41's proposed
snapshot cadence is decided. A vault snapshot is taken before pilot recipe 2's
first shot, then after every test cook that adds a library photograph. It uses
the existing encrypted-OneDrive and plain-D: procedure, and it is tied to the
cook because only a cook changes the libraries.

## 2026-09-30b — where the libraries live

**`philosophy.md` §41.** The Cut Library and the state library live in the vault,
at `03-catalogue/cut-library/` and `state-library/`. Git ignores the photographs.
Every vault backup carries them, to the same encrypted OneDrive and plain `D:`
locations as the rest of the vault. §41 records why: the tools already find the
folder; it stays private, where this repo is public; and git history would grow
by gigabytes.

- **PROPOSED:** a snapshot before pilot recipe 2's first shot, then after every
  test cook that adds shots.
- **Carried into** the authoring standard (§4.3a, doneness) and `asset-spec.md`
  (where the JPEG masters are).

## 2026-09-30 — the retail layer's boundaries

**`philosophy.md` §40: three decisions for when retailer partnerships go live.**

- **A recipe's cost is never retailer-specific.** `cost_per_serving` stays on the
  indicative engine's Class A rate permanently. Only the shopping list shows a
  live retailer's real prices.
- **With more than one retailer, the shopper picks** from a row of logos, a
  stored preference. IP may suggest a first default but never decides.
- **Retailer and manufacturer promotions run outside the app.** Matbakh builds
  and displays nothing for them.

**Open:** Matbakh-brokered promotions, a future design task; and what IP-based
suggestion does with the address (L-06). The reasoning is in the vault's
referral-fee memo. §27–§29 stand as written.

## 2026-09-29 — ingredient states join the libraries

**`philosophy.md` §39.** An ingredient's doneness state — caramelized onion,
golden garlic, parboiled rice — looks the same in every recipe. So its
photograph is a library asset, keyed (ingredient, state) and shot once at the
first test cook that needs it. **Dish-state doneness stays recipe-specific** and
keeps the trust claim. §5.5 and §16.6 stand as written, superseded for
ingredient states only. Fat states stay §35's illustrated layers.

- **PROPOSED:** §33's *would a photo mislead?* test for state variants.
- **OPEN:** failure states; an authored field for a state key; where the library
  lives.
- **Carried into** the authoring standard (doneness guidance, and a pilot duty),
  `asset-spec.md` (two kinds of doneness photograph) and
  `step-imagery-decision.md` §6.3 (a dated note — the trust argument stands).

## 2026-09-28d — the page rule, heat and timers, everywhere they are quoted

**§34 and §35 carried into the documents that quote the old wording.** In place,
with the superseded wording quoted:

- `design/storyboard-companion.md` and `prototypes/storyboard-bench-sheet.html`:
  the grouping rule is now *in sequence, briefly, one utensil, one station, ordered
  or not*; the board is one arrangement and the last page is `serve`; `heat` notes
  the five decided levels and the 1, 3, 5 mapping; timers only on activities the
  cook can leave.
- `design/step-imagery-research.md`, dated 18 August: a dated note that §34
  widened the rule. Compressing to Kitchen Stories' four steps still fights it.

No decision changes.

## 2026-09-28c — the authoring standard catches up with §33–§38

**`design/authoring-standard.md` brought level with the decisions of 27–28
September.** It is the operational spec, so it is edited in place, with the
superseded wording quoted where it changed.

- **Who you write for:** a cook with basic cooking literacy; one language on
  screen at a time.
- **Pages (§4.1):** the new grouping rule — in sequence, briefly, one utensil,
  one station, ordered or not — replacing *order-independent*; the board as one
  arrangement, still one tile per cut in data; preparations upfront (gremolata);
  every recipe closing on a `serve` page with the finished photo.
- **Step fields:** `heat` stays 1–3 until the five-level scale ships; fat states
  decided but not yet authorable.
- **Tiles:** keep writing `amt` everywhere — display is the reader's job; `flip`
  decided but not in the lexicon.
- **New §4.3a — cuts and the Cut Library:** `cut:` / `cut_mm:`, one shot per
  (ingredient, cut) pair at the first test cook, the *would a photo mislead?*
  test, purchased cuts, and `matbakh.py cuts` as not yet built.
- **Timers:** only on activities the cook could leave; ≈ derived, not authored;
  the classification referenced as DRAFT. Cooked-through for poultry, pork and
  mince is OPEN.
- **Pilot and definition of done:** cut variants settled at the stove, the
  layered step page judged in Tile judgements, `flip` as the one lexicon-freeze
  exception; three new done-checks. No cut-coverage check until the command
  exists, per §33.

PROPOSED, DRAFT and OPEN items are marked as such and are not rules.

## 2026-09-28b — the Osso Buco walkthrough: pages, heat, utensils, purchased cuts, feedback

**`philosophy.md` §34–§38**, from walking a braised Osso Buco through the page
grammar as a design exemplar. It is not a catalogue recipe: no recipe file, and
the source card images are not in the repository. Labels are kept as decided:
DECIDED, PROPOSED, OPEN, DRAFT.

- **§34 — page composition, time and timers.** DECIDED: a page groups
  activities done in sequence, in a short time, with one utensil at one station,
  ordered or not — superseding the grouping wording of §3 principle 4 and §4.1,
  including the sear/deglaze example, without editing them. The board is one
  arrangement of cut results, like the ingredients wheel. Preparations are made
  upfront unless they depend on another step or degrade. Time sits next to its
  ingredients as live text: one ≈ number for attended activities, an exact timer
  only for activities the cook could leave. Quantities show only where an
  ingredient is used partly. One language on screen; every recipe ends on a
  finished-product photo. PROPOSED: a page-level `utensil` field; derived
  partial quantities.
- **§35 — heat, fat, `flip`.** DECIDED: five heat levels, L to H, in colour;
  existing `heat` 1–3 map to 1, 3, 5 when it ships, with no data changed now;
  fat states as variants of the fat layer; `flip` as a class-N verb, taking the
  lexicon to 82 — computed, never typed. OPEN: `cover`.
- **§36 — utensils.** DECIDED: an illustrated utensil library, drawn once. The
  layered step page — utensil base, ingredient layers — is PM-09's **leading
  candidate**, a working design for the pilot to judge. PM-09 is not closed.
- **§37 — purchased cuts.** DECIDED: the Cut Library holds butcher's cuts where
  the form matters (`veal_shank__osso_buco_slice`), and prepared cuts are never
  AI-generated.
- **§38 — feedback.** DECIDED: T-06 — a private report card on the finished
  page, opening a report page with the page map. A community was raised, not
  decided; §8 stands.
- **New DRAFT file:** `design/activity-attendance-draft.md`, the 81 activities
  sorted by attendance, checked against `activities.yaml`. Not applied to it.
- `activities.yaml`, recipes and the schema are unchanged.

## 2026-09-28 — no head-set cuts in the worked maps

**`design/worked-page-maps.md` brought level with §33.** It called `dice`,
`mince`, `chop` and the wedge *head-set cuts*, but §33 retired the head set. The
phrase is struck through, with a dated note: each (ingredient, cut) pair is shot
at the first test cook that needs it and referenced after. The point it made
still holds: a cut reference is a library reference, not a per-recipe shot. No
decision changes.

## 2026-09-27c — the cut glyphs stop waiting on PM-12

**Three pointers brought level with §33.** `asset-spec.md`, `ATTRIBUTIONS.md`
and the README checklist said the cut glyphs wait on the Cut Library's keying
(PM-12). PM-12 closed today: photo keys are (ingredient, cut), each pair's
granularity is settled at its test cook, and a separate glyph does not
pre-decide a separate key. The glyphs' source is PM-13, like the activity set.
Whether a pair that splits ever needs its own glyph is not decided. No decision
changes.

## 2026-09-27b — ingredient art: either source, one base per family, the label disambiguates

**Corrects part of `philosophy.md` §33, point 6, filed earlier this session.**
Its source was given only as "hand-drawn or AI-generated", which read as one
pipeline — a hand-drawn base, retouched by computer. What was decided:

- **Source is hand-drawn *or* AI-generated, chosen per asset,** PNG either way.
  The difference is methodology, not format or acceptability, and there is no
  commitment to one pipeline for the whole layer.
- **Retouch-group logic applies to the wheel, sauces included:** one base
  illustration per shape or visual family, retouched for colour and variants,
  with the ingredient's name label doing the disambiguation colour cannot — a
  generic onion retouched and labelled *red onion* is honest here.
- **Scoped to the wheel only.** The Cut Library keeps point 3's *would a photo
  mislead* test, with no retouch-and-label fallback: the cook-mode layer is
  near-wordless by design (§5.5), the wheel carries a name label as standard.
  A filing note records that *inside step tiles* does not settle PM-09.

## 2026-09-27 — the Cut Library is shot at the stove

**`philosophy.md` §33 resolves PM-12, both halves.** Cuts are photographed only
at test cooks, never at a scheduled shoot (KS-03), so the library's size is
discovered through authoring rather than forecast — the ~30 vs ~130 question
is retired, and §20.2's head-set afternoon with it. Each (ingredient, cut) pair
is shot once, ever, and referenced by every recipe that needs it. §20 stays as
written.

- **Granularity is decided per pair, at the stove:** prep both variants side by
  side and ask whether a cook aiming for one would be misled by a photo of the
  other. Yes, two keys; no, one entry and `cut_mm` carries the difference.
  Mince fine/coarse stays as C-09 ruled it. Every other pair — dice/brunoise and
  julienne/baton included, whose separate glyphs do not pre-decide separate
  keys — is tested when a real recipe first needs it.
- **The library indexes itself by filename,**
  `cut-library/<ingredient_id>__<cut_key>.jpg`, with no manifest to drift.
- **New tooling, not built yet:** `matbakh.py cuts <recipe>.yaml` lists which
  of a recipe's cuts are covered and which to shoot this session, and warns on
  near-miss names (`onion__dice` beside `onion_yellow__dice`).
- **Ingredient identity art is illustrated, never photographed,** from a
  library separate from cut photography — a new tracked item (PM-17), kept
  apart from the glyph-sourcing question (PM-13).
- **Still open from §20.2:** the scale-reference convention (C-09's governing
  note, now unblocked) and whether the board shot can instruct (C-06).

## 2026-09-24l — the first-500 workbook's new path

**`philosophy.md` §31 and §32 re-pointed.** The vault filed its narrative and
reference documents, the first-500 workbook among them, in a new
`PDF Files/Documentation/` subfolder; both sections named the workbook's old
place in `03-catalogue/`. No decision changes.

## 2026-09-24k — `main_protein` gains `lamb`

**`philosophy.md` §32: eight values, not seven.** `beef · lamb · poultry ·
seafood · pork · vegetarian · mixed · none`. The candidate 500 builds 27 dishes
on lamb across eight cuisines, and neither `beef` nor `mixed` could hold them
truthfully. §26 stays as written; `tag-proposal.md` carries a pointer.

- Game is not decided: the one game dish, rabbit, sits under `poultry` in the
  workbook as a noted judgement.
- The vault's first-500 workbook is re-mapped to the eight values (Revision 5).

## 2026-09-24j — wine, and what "halal" can claim

**`philosophy.md` §31 files a 2 September decision that never reached canon.**
No halal second version of a recipe — a fork, which §9 and §18.2 forbid. Where
wine is structural, the ingredient line carries an authored substitute note,
never auto-applied. *Contains alcohol* derives from the existing `diet` class
with no new schema. **The claim is alcohol-free, never halal**, unless a real
sourcing record stands behind it: halal turns on slaughter and additives the
schema does not track.

- Decided in chat on 2 September and held until now only in that session's
  handoff note, outside both repositories; the note is archived in the vault.
- **Open:** whether an alcohol-free badge or filter ships, and what a halal
  sourcing record would need.

## 2026-09-24i — three units authored, the cook shows two

**`philosophy.md` §30 files the three-unit display.** Every ingredient record
authors imperial, metric and kitchen-measure values; the cook chooses in
settings which two display side by side. No computed conversion and no
mid-recipe toggle — both unchanged from §6.7.

- Decided 20 September as the correction to T-04 in the competitor register,
  filed here 24 September. It supersedes the dual-unit paragraphs of §6.7 and
  §11's 29 August household-measure addition without editing them.
- **Not in the schema yet**, and neither is the 29 August household measure.
  Field names, the default pair, blanks for counted items and authoring cost
  are open; `manifest.yaml`'s `next_up` carries the schema step.

## 2026-09-24h — publish.sh prints the right Pages address

**`publish.sh`'s closing line printed `…github.io/matbakh-design.git/`.** Its
pattern, `(.+)(\.git)?$`, let the greedy group swallow the `.git` suffix, so the
optional group matched nothing. The suffix is now stripped in its own step; the
line prints `https://ibrahimrd-sys.github.io/matbakh-design/`, and gives the same
for an SSH remote or one without `.git`.

## 2026-09-24g — §26–§29 carry the day they were decided

**`philosophy.md` §26–§29 re-dated from 20 to 24 September.** PM-07 (the tag
vocabulary), the monetisation fork, substitution scope and price sourcing were
decided on 24 September, the day they were filed; the filing text carried
20 September and the headings, addendum titles and decision-log rows took it.

- **§25 keeps 20 September.** The D-1 reversal was decided that day, and every
  "the 20 Sept D-1 reversal" reference to it stands.
- The same correction runs through §16.7's pointer to §26, the closure note in
  `tag-proposal.md`, the PM-07 line in `manifest.yaml`, and the four entries
  below, which said "Decided 20 September, filed 24 September".
- **`philosophy.md`'s *Last updated* moved to 2026-09-24.** §26–§29 landed on
  the 24th while the header still said the 23rd.
- The vault carries the matching correction in the PM log, the competitor
  register and the 22–24 September session report.

## 2026-09-24f — referral-fee options, as prep rather than terms

**`philosophy.md` §27's deal-mechanic line now names a file.** The vault gains
`02-strategy/referral-fee-variances.md`: the ~3% benchmark and five structures —
flat, points-back to the shopper, per-unit-sold, volume-tiered, and a
retail-media add-on — with a suggested sequencing for a first retailer
conversation.

- **It decides nothing.** M-03's shape stays settled and its terms stay open;
  the pointer says so in §27, in the PM log's M-03 row, and in `DIRECTORY.md`,
  where it is registered as reference rather than a decision.
- KU-03 and KU-04, which the memo's sequencing leans on, remain SLOT in the
  idea register — not accepted.

## 2026-09-24e — publish.sh accepts the release it is given

**`publish.sh` step 2 rewritten.** It demanded `release:` be today's bare date,
so it refused every second publish of a day — while the CHANGELOG has used a
`b`/`c`/`d` suffix since 18 September and `build.py` compares against it. The
script was rejecting the repo's own convention, and four filings today were
committed by hand to get around it.

- The release is now **read from the manifest**, not assumed, so the commit
  message's `Release …` line carries the suffix.
- Accepted: today's date, optionally plus **one lowercase letter**. Rejected: a
  wrong date, a two-letter or uppercase suffix, a missing `release:` key — each
  with its own message.
- Step 2 now prints the release it accepted instead of passing in silence.

## 2026-09-24d — the price source is a government portal

**`philosophy.md` §29 added — its own addendum, merged into nothing.**

- **`agriprice.gov.eg/local-prices` is the primary price source**: live, and
  needing no negotiated access, unlike the El-Obour relationship. **P-01 is
  de-risked, not closed** — coverage, currency and weekly cadence unverified.
- **P-03's mechanism described:** compile from the portal for staples plus
  direct collection from a few large chains for packaged goods, review, adjust.
  Still needs an owner, a cadence and tooling.
- **Collection is not uniform** — Carrefour Egypt blocks automated clients.
- **L-05 is now concretely actionable:** portal data and retailer-posted prices
  likely differ in reuse standing.
- **New item P-06:** an indicative-pricing engine normalising brand, weight and
  origin variance to a standard unit. It feeds §28's tiers, so it decides what
  `cost_per_serving` means. Formula open.
- Decided and filed 24 September. Release bumped to 2026.09.24d.

## 2026-09-24c — substitutes stay on the shopping list

**`philosophy.md` §28 added — a further addendum; §22 is not edited.** PM-15's
swappability question is resolved.

- **Substitutes are shopping-list-only and never enter the instruction set.**
  Steps, technique and authored timers stay as test-cooked.
- **A rules table** of (original, substitute) pairs replaces D-15's prose note.
- **Packaged goods** show quality tiers side by side; the displayed
  `cost_per_serving` is **pinned to Class A**, not averaged or cheapest.
- **Protein swaps** surface a **suggested timer adjustment — auto-applied,
  visibly flagged, overridable in one tap.**
- **New UI scope under E-06:** editing a timer's duration mid-session, which no
  prototype has and §4.6 does not describe.
- **Still open:** one rules table or two, whether the packaged-goods tiers earn
  their own governing document, and how the protein table relates to D-13.
- Decided and filed 24 September. Release bumped to 2026.09.24c.

## 2026-09-24b — the monetisation fork resolved

**`philosophy.md` §27 added — a further addendum, §25 left as written.** M-01,
M-02 and M-03 are decided as one set.

- **Build-to-own, Kurashiru-shaped** — retail media, audience first and the
  retail relationship second, non-exclusive by construction, not single-retailer
  exclusivity. Resolves PM-02.
- **The free/paid boundary made concrete:** raw weekly market prices stay free
  forever (NY-01 untouched); the computed cost of a dish and the planner's
  costed, consolidated week are premium. Free is the raw data, premium is the
  data applied to a dish or a week.
- **Layer 3 confirmed as retail media**, with a referral fee once a partnership
  is agreed. **The deal mechanic is deliberately not decided** — flat,
  points-back or tiered awaits a real retailer — so T-05 stays DEFER.
- **Model referral at ~3%, not 5%** (Instacart 3%, Kroger 1.6–4.8%, Ocado 3%).
- **Not closed: F-01.** The numeric base case has not been run against this
  shape.
- Decided and filed 24 September. Release bumped to 2026.09.24b.

## 2026-09-24 — the tag vocabulary is closed

**`philosophy.md` §26 added, §16.7 re-titled (PM-07).** Nine authored fields and
eight derived tags, final. `main_protein` is new and authored — the dish's claim,
not its ingredient list. `occasion` splits `siami` into `siami_seafood` and
`siami_no_seafood`: a seafood-fast dish still excludes meat, poultry and dairy
but is not `vegan`, and no derived tag says that. `cuisine` gains `thai`,
`latin_american` and `eastern_european`. `hidden` is removed, redundant against
`course: component`.

- **`design/tag-proposal.md` closed to reference** — final field list in place,
  its three open questions resolved and recorded in a *Changed at closure*
  table, the *Open* section removed.
- **§16.7 is now VOCABULARY SETTLED; INTERACTION MODEL OPEN.** How filters
  compose in the interface is not settled and was not part of this decision.
- **S-07 untouched** — derived tag keys still render in English in the Arabic
  build.
- **`main_protein` is not in the schema yet.** The recipe schema,
  `matbakh.py check` and `authoring-standard.md` do not know the field.
- Decided and filed 24 September. Release bumped to 2026.09.24.

## 2026-09-22 — competitor citations point at one file

**`philosophy.md` decision log: one row, no design change.** The vault's
competitor research is now a single file, `competitor-study-combined.md`.
Older citations are left as written: `competitor-study-part-five.md` is its
chapter 3R and `ideas-from-cooking-apps.md` its Appendix A, with the KS- IDs
unchanged — including the ones cited in `design/worked-page-maps.md`.

## 2026-09-18b — the party plan stops pricing six full portions

**`philosophy.md` §24 added (D-17).** Party-plan quantities come from an
effective-covers figure — a per-course target split across the dishes sharing
that course, weighted per event — fed into §6's existing scaling. Blocked on
PM-07 until `course` is authored on recipes; the numbers and the default split
are open as PM-16.

## 2026-09-18 — the cooking log, and what it deliberately is not

**`philosophy.md` §23 added (D-16).** A plain chronological record of finished
cooks in Profile — completions only, no streak, and separate from the recipe
box's explicit save. `recall_menu()` is reframed as the entertaining-specific
view of the same mechanism rather than a parallel one.

## 2026-09-16 — substitutes for costing: swap the price, not the cook

**`philosophy.md` §22 added (D-15).** Recipes carry an explicit substitute list
per ingredient, tagged cost-only (swappable, live cost recompute) or
changes-the-cook (informational only, with a prose note); the open half is PM-15.

## 2026-09-06 — two hand-drawn maps translated into pages

**`design/worked-page-maps.md` added.** Beef Enchilada Skillet and Chicken
Skewers with Thai Curry, drawn by hand on 5–6 September and mapped into the page
grammar with the carrier named for every element. The third and fourth worked
storyboards after molokhia and bolognese, and the first two that were **drawn
before they were mapped** — so they test the grammar against a hand that was not
following it.

- **8 pages and 6 pages**, both inside the 6–10 target. Four in a row now
  (8, 9, 8, 6).
- **Four doneness photographs across two complete recipes** — three and one,
  against §16.6's open estimate of 4–6 per recipe. Two maps is not a
  measurement, but both sit at or below the bottom of the range, and that figure
  multiplies the largest content line after the build.
- **Nine authored strings across both recipes**, plus a `why` each: four
  doneness cues, three notes, six qualifiers, one bespoke verb. Everything else
  — verbs in five locales, unit symbols, station headers, page counter, the
  whole prose view — is generated. The wordless claim, stated as a number.
- **Logged for the ≥3 rule, no thresholds met:** `toast` resolves to a slice of
  bread on a page toasting ground spices and `garnish` to a leaf on a page
  garnishing three things (both already on C-05's ingredient-drawing list, now
  seen in a drawn recipe); `season`/`to_taste` co-occur for the second recipe
  running and survive by luck rather than design; `brush`/`baste` is genuinely
  **ambiguous** rather than colliding when brushing marinade onto grilling
  skewers; `char` appears as a doneness state rather than an act; two cuts the
  vocabulary does not name (*into squares*, *into strips*).
- **Two gaps recorded, both cheaper to close now than at recipe 400.** The
  schema cannot **partition an in-recipe intermediate by fraction** — *set aside
  a third* needs a yield a cook never measures, and a ratio is scale-invariant
  where a millilitre figure is not, which argues for `fraction_of` rather than a
  workaround. And the reader has no model for an **obligation during a wait** —
  turning and brushing throughout a five-minute timer, the positive inverse of
  `do_not_stir`, currently carried by a `stay_here` note.
- **One rendering proposal:** render a `carried` item **without its amount**,
  since the quantity was established on the page where it was prepped. Drops the
  skewers' fattest tile from eight amounts to five.
- Every activity key used was verified present in `content/lexicon/activities.yaml`.

## 2026-09-05 — the equipment list is taken, the per-step repetition is not

**`philosophy.md` §21.3 added — second utensils decision, same day as §21.**

- **The per-recipe equipment list is confirmed as the shape**, with an
  `optional` flag per entry: §16.2's pre-commit check must not warn a cook off a
  dish over a grater they could work around.
- **No separate per-step equipment surface.** Where a tool matters it is already
  showing in that step's own photograph or icon. Kitchen Stories repeats tools
  at every step because it has four fat steps, no station concept and a cook who
  would otherwise scroll back to the top; Matbakh has six stations naming where
  the cook stands and a per-recipe list that has already said what to get out.
- **This narrows §21.2's first open item without closing C-05.** The measured
  finding — 24 of 81 activities draw a tool rather than the act — was recorded as
  reading two ways; this leans on the second, that for instrument-defined verbs
  the utensil is already on the tile. C-05 stays open: the glyph must still draw
  the **action** wherever the action is what distinguishes it.
- **One case for the pilot to watch (C-06):** two vessels in play at one station,
  where neither the act glyph nor the station header says which the tile means.
- Source: the Kitchen Stories instruction-layer reading,
  `matbakh-private/02-strategy/competitor-study-part-five.md`.

## 2026-09-05 — utensils open as a reference layer, in the locale-bound column

**`philosophy.md` §21 added — the utensils layer settled in part.**

- **What equipment a recipe requires is a fact about the recipe**, and it gets a
  first-class reference parallel to the ingredient one. Its first job is the
  pre-commit surface (§16.2) — committing to a dish and finding at the bench
  that it needs a blender you do not own is the failure that surface exists to
  prevent — and its second is as a filter (§16.7).
- **It is three features, not one, and they ship in that order:** the
  requirement (settled), the visual carrier (open), and substitution guidance
  (open, and deliberately last — it is irreducible judgement, so by §5.1 it is
  words, and it carries an editorial cost not in the production model, the same
  trap §9 records for `why`).
- **The decision that matters is which column it lands in, and it is not the
  Cut Library's.** §20 admits cuts partly on portability: a cut frame is the
  most food-only image in the system — a board and a technique, no plated dish,
  no kitchen, no cultural furniture — so it crosses every locale with zero
  re-shooting. **A utensil is nothing but cultural furniture.** A pot in an
  Egyptian kitchen is not a Dutch oven; a tagine, a baladi oven and a mehmas
  have nothing to travel to. The argument therefore **inverts** rather than
  merely weakening, and utensils sit in the **locale-bound** column with mise
  en place and the plated hero. A utensils layer does not amortise across
  locales, and §10's caveat applies in full.
- **Division of labour holds a third time: the picture carries tool identity,
  words and digits carry size, capacity and substitution.** No photograph
  conveys *26 cm* and none should be asked to.
- **Presence, not inventory** — §16.1's constraint carried over unchanged, for
  the same reason it was set there. Staples assumed present and unset: knife,
  board, one pot, one pan.
- **Left open, and not defaulted into:** whether a visual layer exists at all
  and what carries it — **sequenced behind PM-09**, because the 44 px tile
  already has one open carrier competing for it; scope and granularity, mined
  from the corpus by frequency rather than scoped from intuition (**PM-14**);
  and whether the requirement is **authored or derived** — §11's *could a
  careful person disagree?* argues derived, but nothing in the tile names a
  tool, so there is nothing to derive from, which makes it a schema retrofit on
  the same logic §16.7 gives for tags.
- **One finding is resolved first, because it changes what the question is:**
  **24 of the 81 activities — 23 distinct glyph values — already draw a tool,
  vessel or appliance rather than the act.** `grate` is a grater, `sift` a
  sieve, `peel` a peeler, `blend` a blender, `skim` a spoon, `simmer` a pot,
  `stir_fry` a wok. That is four times the six ingredient-drawing activities
  **C-05** already tracks as a defect against `asset-spec.md`'s *draw the
  action, not the ingredient*. Either it is that same defect at four times the
  scale, or **utensil-as-carrier is already the de facto answer** for the
  instrument-defined verbs and should be made deliberate. It is currently
  neither. Counts generated from `content/lexicon/activities.yaml`; the
  classification of what a glyph depicts is judgement, on the same footing as
  the Class M / Class S split. Folded into **C-05**, measured in **C-06**.

## 2026-09-05 — cuts become a library, not a per-recipe line item

**`philosophy.md` §20 added — cut photography settled in part.**

- **The Cut Library exists as a first-class, reusable image asset**, referenced
  by recipes rather than embedded per recipe. Tight "cut identity" photographs
  are produced once per distinct cut-state and re-used. A cut is a property of a
  **technique**, not of a dish — the same butterflied breast or halved
  tenderloin is visually identical across every recipe it appears in, so
  per-recipe cut shots pay repeatedly to photograph the same object.
- **Why this version.** Shooting each cut once and referencing it N times moves
  cut photography off the column that scales with the catalogue and onto the one
  that scales with the vocabulary — the move §5.5 already names as the entire
  economic question — and it is the same "an asset that carries no words is made
  once" logic that already justifies the lexicon and the ingredient vault.
- **It is keyed to the activity lexicon.** Each cut photo is tagged to the
  lexicon entry (technique) it depicts, so the correct shot resolves wherever
  that technique appears, in any recipe and any dialect variant. The library is
  the visual counterpart of a vocabulary that already exists, so it lands as a
  resolved layer of the schema rather than a loose folder of images.
- **Portability falls out for free.** A cut frame is the tightest, most
  food-only image in the system — a board and a technique, no plated dish, no
  kitchen, no cultural furniture — so it travels across every locale with **zero
  re-shooting**. That separates the universal image asset from the locale-bound
  ones (mise en place, plated hero), supporting the locale-portability premise
  rather than eroding it.
- **Division of labour confirmed at this level too: photo carries cut identity,
  the digit carries quantity and dimension.** No photograph is relied on to
  convey proportion or size, and quantities label each ingredient regardless of
  any photograph.
- **Board-as-orientation is the per-recipe default** — one wide mise en place,
  "here's everything, prepped" — **plus at most one tight shot for the single
  hardest or least-obvious cut** in that recipe, drawn from the Cut Library
  where the cut already exists there.
- **§20.2 — four things deliberately left OPEN, not decided.** The scope of the
  head set; the granularity of the library key (*word + parameter*, since
  "sliced" for a salad is not "sliced" for a braise, and the answer is a
  four-fold swing — ~30 shots or ~130 — on a line that is shot once and then
  lived with); the scale-reference convention; and whether the wide board shot
  can instruct well enough to drop the tight shot. A one-afternoon validation
  test is specified to settle all four before the library is shot at scale.
- **Header date corrected.** `philosophy.md` read *Last updated: 2026-09-03*.

Tracked in the vault as **D-13** (WS1). The open half is split rather than
parked in one place: **scope and granularity open as PM-12** — deliberately not
folded into PM-09, which was narrowed on 2 September to the single question of
what the 44 px tile carries; the **scale reference folds into C-09**'s owed
governing note, where `cut_mm` is already the mechanism; and **board sufficiency
folds into C-06** as a cut-coverage judgement column in the pilot tracker,
alongside the tile judgements.

Cross-refs **PM-01** — it removes repeated cut shots from the catalogue
photography line PM-01's options are priced against — and the step-imagery
decision (**PM-09** / **D-11**), whose *shoot the vocabulary, not the catalogue*
recommendation this is the same argument applied one level further out.

## 2026-09-03 — the recipe box gets a storage decision

**`philosophy.md` §19 added — the recipe box, settled in part.**

- **§19.1 Storage — SETTLED.** The box is held on the device and carried between
  devices by the platform's own backup: iCloud on iOS, Google Backup on Android.
  No Matbakh account, no sync server, no real-time cross-device sync. Pure
  local-only was rejected because a hand-built list has nothing to rebuild from
  when a phone is replaced — the planner survives that failure only because it
  can rebuild from cook history. Account-backed sync was rejected because
  sign-up, recovery, session handling and a server holding user data are a
  workstream rather than a feature, against R-06.
- **What it buys is restore-on-reinstall, not sync**, and the interface must say
  so. Two devices do not converge; what returns is the platform's last backup.
  The word *synced* is not available to describe this.
- **Two dependencies recorded rather than assumed away.** iCloud and Google
  Backup are native mechanisms, so the decision assumes a platform-packaged app
  and must be revisited if E-01 lands on web. And it is the first user data to
  leave the device — a narrow, deliberate departure from the local-only position
  the planner holds for free (L-06), and described as such rather than folded
  into that claim.
- **§19.2 Whether the box feeds the planner — left OPEN.** `suggest_home` splits
  DUE from UNTRIED on cook history alone; a saved recipe is a third signal,
  *wants to cook*, wired nowhere. Favourite *ingredients* feeding the planner is
  accepted (KS-02); favourite *recipes* is not, and the two are not the same
  claim. It belongs to PM-11 and cannot be tested before tags land.
- **Header date corrected.** `philosophy.md` read *Last updated: 2026-08-29*
  while already carrying §5.5, a rewritten §16.6 and two decision-log rows dated
  2 September.

Tracked in the vault as **D-12** (WS1), with the planner half folded into
**PM-11**.

## 2026-09-02 — the project consolidated into one folder

- **`matbakh-design` and `matbakh-private` moved to sit as siblings under
  `Matbakh_Project_Dir`**, previously nested three levels deep under
  `~/matbakh/Matbakh/matbakh/`. Done with a plain `mv` of each folder — `.git`
  history and the GitHub remote (`ibrahimrd-sys/matbakh-design`) came through
  untouched, confirmed via `git status` and `git remote -v`.
- **Vault resolution verified working end to end.** `matbakh.py status --write`
  run against the moved repo found the vault, read 178 ingredients, and spliced
  the generated block into the PM log with no error — the sibling-relative
  path logic (`../../matbakh-private` from `content/`) needed no changes.
- **`DIRECTORY.md` and `data-sources-and-updates.md` checked, not edited.**
  Neither file hardcodes an absolute path to the old location — both resolve
  relatively or refer to the vault/repo by name — so nothing needed updating.
- **`scan.sh` re-run post-move: clean.** All three vault defences (working
  folder, git tracking, commit history) reported clear. The vault has its own
  local-only `.git` with no remote — confirmed fine, not a leak risk.
- The Cowork project's connected local folder was re-pointed to the vault's
  new path.

## 2026-09-02 — the vault gets history, and the guards learn the difference

**`matbakh-private/` is under version control — local only, with no remote.** The vault had no history, and that cost real work: a stale `CHANGELOG.md` sitting three directories above this repo swallowed two days of edits, and only the half that had been committed came back. The vault is now its own git repository. No remote is configured, `.git/hooks/pre-push` refuses every push, and `scan.sh` fails if a remote ever appears.

- **`scan.sh` and `setup-guards.sh` now check for a remote, not for `.git`.** Both previously failed on the vault being a repository at all, so both would have fired on every run from here on — and a guard that cries wolf is a guard you learn to bypass, as `.githooks/pre-commit` says in its own comments. A repository cannot leak; a push can, and git history keeps what you push even after you delete it. Absence of history is now a warning rather than the desired state.
- **`scan.sh` also warns when the vault's `pre-push` hook is missing.** Nothing tracks that hook, so it could vanish without a sound.
- **Both guards were tested by firing them.** A remote was added to the vault and a real push attempted against a throwaway bare repository: `scan.sh` reported FOUND and exited 1, the hook refused, and nothing was transferred. A check that has never been seen to fire is not a check.
- **What this trades.** The vault's protection was structural — git was never pointed at it, so a leak needed someone to move files. It is now configurational: git is pointed at it, and what keeps it private is that no remote exists. That is a real downgrade, recorded in `matbakh-private/VaultReadme.md` rather than left to be rediscovered.
- **The vault's `.gitignore` un-ignores `*.xlsx` and `*.docx`**, which `~/.gitignore_global` excludes machine-wide. Without that, `git add -A` there silently skips the financial model, the business plan and the pilot tracker — and reports success.
- `.gitignore`: `.claude/` added.

- **PM-09 reframed, and half of it closed.** It had read "sign off option C, or reject it" since 19 August, pointing at the recommendation `step-imagery-decision.md` superseded on 21 August with option E. `DIRECTORY.md` called that file "Option C as finally specified" while the file itself recommends E and says "no decision taken" — two documents disagreeing, which is how the decision stayed aimed at the wrong option for eleven days. Both corrected. **`philosophy.md` §5.5 added:** four surfaces, each answering a different question at a different size and each scaling with something different — the arc with the vocabulary, the doneness photograph with the catalogue. **§16.6 rewritten** from *SCOPE UNDECIDED* to open and pinned to the pilot; no per-recipe photograph count is recorded until one is measured. A contradiction inside §9 of the decision document was resolved on the way and its hours column flagged as not following from its own counts.

**Still open:** git is history on the same disk, not a backup. An encrypted off-machine backup remains unaddressed.


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

## 2026-08-12 — translator tool
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

## 2026-08-01e — sub-recipes
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
## 2026-08-01d — diet field, and derived dietary tags
Ingredients gained `diet`. The editor has a chip selector and a bulk-propose
button that resolves 177 of the 179 from name rules plus a table of cases a
name cannot reveal — worcestershire is fish, bechamel is dairy and gluten.
`matbakh.py` derives `vegetarian`, `vegan`, `gluten\_free` and `contains` from
it. If any ingredient in a recipe lacks the field, the flags are withheld
entirely and the validator names what to fix: a wrong vegetarian claim costs a
guest their dinner, so silence is the correct failure.
§13.4 (the party plan) and §13.7 (filters) are unblocked by this.
## 2026-08-01c — audit output, and the last dialect gaps
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

## 2026-07-30e — authoring tools
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
## 2026-07-30d — hero shows the whole photo
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
