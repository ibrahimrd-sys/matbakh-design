# Personal planning — algorithm

Two decisions: **what to cook this week**, and **a menu for N guests under a
budget**. Both run on the cook's own record, held locally.

## The stance: remember, don't predict

`discovery-draft §4` rejected personalisation as *"pretending I know you"* and
chose subtraction — the user supplies the constraint, the app removes what
fails it. This does not overturn that. It adds a second input, the cook's own
history, and applies one rule:

> **If a suggestion cannot be explained in one sentence from the user's own
> record, it is not made.**

The app says *"you have made this six times, last 7 days ago"*. It never says
*"we think you'll like this."* `philosophy §3` forbids presenting a computed
estimate as a fact, and an unexplainable recommendation is exactly that.

## Privacy, and why it is architectural rather than promised

All state is local. Nothing is transmitted, pooled across users, or published
(`philosophy §8`). The algorithm is pure functions over a local store — no
training, no model, no server. It runs on-device, which means it works offline
in a kitchen **and there is no dataset to leak.**

`Profile` is stated, never inferred. A cook declaring a nut allergy is a fact;
an app deducing one from behaviour is a guess that could hurt someone.

## The two signals, and why they are separate

**Affinity** — how much this cook likes this dish, from repeats alone. Repeat
cooking is the only unambiguous signal available. Abandonment counts against,
weakly: a cook may stop because the phone rang.

**Staleness** — whether the dish is due for a return. Exponential in days since
last cooked, 28-day half-life.

**These pull in opposite directions and conflating them is the classic error.**
A dish cooked twelve times but not for six weeks is an excellent suggestion.
The same dish cooked yesterday is a poor one. Scoring is multiplicative, so a
beloved dish cooked three days ago still scores near zero — which is correct,
and which an additive score would get wrong.

## What testing changed

The first version ranked known and unknown dishes in one list. Two failures
appeared immediately:

- A favourite cooked six times **never appeared at all**, buried under dishes
  the cook had never seen.
- Every untried dish scored identically, so with 500 recipes the ranking among
  them was arbitrary while looking authoritative.

Mixing them requires a taste model the app does not have and `philosophy §8`
denies it the data to build. So they are no longer mixed:

| List | Ranked by | Honest because |
|---|---|---|
| **Due for a return** | affinity × staleness | Entirely from the cook's own record |
| **Not tried** | constraint fit, then pantry overlap | A shelf, not a prediction |

## Event planning

Exhaustive within each course — a handful of dishes from a few hundred
candidates, so the result is exact and reproducible rather than heuristic.

Hard constraints filter first: dietary exclusion, dislikes, spice ceiling,
cuisine, budget. **A recipe whose dietary status is unknown is excluded, not
assumed safe** — the `philosophy §11` discipline — and the count of such
exclusions is always reported, so the shelf never lies about its own size.

Two structural rules come from the tag vocabulary and exist because a host
would not think to ask for them but would feel their absence:

- **`max_involved`** — how many demanding dishes one cook can actually run
- **`max_immediate`** — how many dishes need serving the instant they are done

Scoring favours menus the cook has made before, spread across cuisines, using
the budget rather than hoarding it.

## Never return zero silently

When nothing fits, the planner names the **binding constraint** and shows the
nearest menu — per `discovery-draft §9`, so the host relaxes their own
requirement rather than the app guessing which mattered least.

Tested on twelve covers at EGP 1,500:

```
NO MENU FITS — binding constraint: budget
the cheapest 4-dish menu costs 37.20 for 12 — 22.20 over, or 3.10 a head
  main   Koshari               $10.20
  salad  Rocket and lemon      $ 5.40
  side   Rice with vermicelli  $ 4.80
→ raise the budget to $37.20, or drop to 3 dishes
```

That is a real answer to a real constraint, not an empty screen.

## Saved menus — a tested menu beats a computed one

An `Event` records one occasion: date, covers, the dishes, what was spent, and a
**name**. Events are created **explicitly** — when a menu is accepted, or when
the cook says they are planning something. Never inferred by grouping same-day
cooking, because a big-batch Tuesday looks identical to a dinner party and
guessing wrong corrupts the only signal that matters here.

**The name is free text and is never parsed.** *"Amira's birthday"* tells the
cook who was there without the app holding names, matching guests, or storing
personal data about third parties who never agreed to be in it. The app reads it
back and does nothing else with it. That is the entire privacy design for
guests: no structure means nothing to leak and nothing to get wrong.

**A menu's identity is its set of dishes**, so the same four served twice is the
same menu served twice. Saved menus rank on the same two signals as recipes —
times served and time since — with a **120-day half-life** rather than 28,
because a host may entertain a handful of times a year and a short half-life
would mark everything fresh.

**The planner offers saved menus before anything it assembles.** The cook
already knows the combination works at that scale; no computed alternative can
claim as much.

### Recall re-checks everything

Reopening a menu rescales and reprices it — *"10 covers at \$56.50, now 16 at
\$90.40, +\$33.90"* — and **re-checks every dish against the current profile.**

A menu that worked in March may contain something a guest now cannot eat, or a
dish whose dietary data has since been completed and turns out to exclude it.
Tested with a dairy exclusion added, the March menu correctly drops two of its
four dishes and says which and why. **Recalling a saved menu without
re-checking is the one place this design could actually harm someone.**

## Cold start

With no history, `affinity` returns 0.5 for everything and the "due" list is
empty. The app degrades to pure subtraction — which is the day-one behaviour
`discovery-draft §4` specifies anyway. The feature improves with use and is
never broken by its absence.

## Choosing an engine later

Nothing here needs one. Scoring is arithmetic over counts and dates; planning
is a small constrained search. Both run in milliseconds in any language.

If a heavier engine is adopted, it can replace the scoring and the search
without touching the data model — **provided it preserves the explanation
contract.** An engine that cannot say why in one sentence from the cook's own
record cannot be used here, however good its recommendations.

## Files

- `planner.py` — the algorithm
- `test_planner.py` — a plausible year of cooking history, both decisions
