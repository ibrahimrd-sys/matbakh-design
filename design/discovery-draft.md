# Discovery — DRAFT, not settled

> Drafted for review. Nothing here carries SETTLED. Positions are proposed with
> their reasoning attached so each can be accepted, rewritten or rejected.
> Genuine forks are marked **FORK** rather than resolved silently.
>
> **Revision 2** — rewritten after the first draft was found to assume a mature
> single-locale (Egyptian) shelf. §2 is new and conditions everything after it.
>
> If accepted, this becomes a numbered section before philosophy §16, and philosophy §16.1 is deleted.

> **Cross-reference convention.** A bare `§n` refers to a section of *this*
> document. References to another file name it — `philosophy §9`,
> `discovery-draft §2.4`. Adopted 2 August 2026 after an audit found 50 of 108
> references across the three drafts ambiguous: every document numbers from 1,
> so its section numbers collide with `philosophy.md`'s.


---

## 1. The stance

**Discovery is a shelf, not a feed.**

The collection is finite, curated, and has one recipe per dish (philosophy §9). A feed
implies inexhaustibility and therefore implies an algorithm deciding what
surfaces. A shelf implies a person who chose what is on it, and can be seen
whole. Matbakh has a curator; presenting that as a feed would be dishonest.

This follows philosophy §1 rather than extending it. The reader is an instrument because
the cook's hands are busy. Discovery is a shelf because the collection is
finite and someone stands behind it. Different rooms, same building.

**The consequence that costs something:** a shelf can be exhausted, and a user
who reaches the end has seen the whole product. That is the risk philosophy §16.1 names —
confidence or thinness. It is accepted deliberately, because the alternative is
padding, and padding is what one-recipe-per-dish exists to refuse.

---

## 2. Locale is a first-class axis

philosophy §10 settles that the wordless principle makes the *interface* portable and does
nothing for the pricing pillar, which is locale-bound by definition. philosophy §15 settles
that dialects are lexicon-only. Discovery is where both of those decisions
become visible to the user, so it must be designed for a locale that has no
price feed and a small shelf — not only for Cairo at 500 recipes.

### 2.1 What degrades, and what does not

| Element | Mature locale | New locale, no price feed |
|---|---|---|
| The shelf itself | Full | Smaller, and must say so |
| `why` on the card | Unchanged | Unchanged — translation only |
| Cook mode | Unchanged | Unchanged — philosophy §15 makes it portable |
| Cost per serving | First-class | **Absent** |
| Cost as sort axis | Default on return | **Unavailable** |
| Cost notification (philosophy §2) | The habit mechanism | **Does not exist** |

The middle column is the product Matbakh is being designed as. The right column
is what actually launches in market two. **philosophy §2 assigns the
return visit to cost — so in a no-price-feed locale, Matbakh ships without a
habit mechanism at all.** That is a strategic fact this section can surface but
cannot solve, and it deserves its own decision rather than being discovered
during a Gulf launch.

### 2.2 The rule

**A locale ships with the price feed or it ships knowing what it lost.**
Discovery must never render a cost affordance that resolves to nothing —
a greyed sort control, an empty field, a "coming soon" — because philosophy §3's honesty
commitment makes a promised-but-absent number worse than an omitted one.

Practically: `price_source` presence is a locale capability flag, and the browse
card and sort controls are composed from capabilities, not hardcoded.

### 2.3 FORK — one shelf or many?

Unresolved, and it is the largest open question in this draft.

**One global collection, filtered by locale.** Cheaper to curate, and a Levantine
dish is genuinely interesting in Cairo. But cuisine tags become locale-relative
in presentation — *Egyptian* is a cuisine in London and the water in Cairo — and
the shelf's coherence dissolves as it grows.

**Per-locale shelves.** Coherent, but multiplies the curation cost that
one-recipe-per-dish already makes expensive, and forces the question of who
curates market two.

A middle position exists — one collection, a locale-declared *core* that leads
discovery, the rest reachable — but it needs arguing, not asserting.

### 2.4 Curation does not translate

philosophy §9's promise is that someone chose. That someone is currently one editorial
voice in Cairo. Editorial ordering (§5 below) is the only ranking mechanism philosophy §8
permits, which means **every new locale needs an editor before it needs
recipes.** This is a hiring constraint disguised as a design decision.

---

## 3. The posture is different, so the physics are different

philosophy §1 fixes the counter-top posture as the reader's design centre. Discovery has a
different one: seated, unhurried, one thumb, hands clean. Every constraint the
reader inherits from wet hands and divided attention is absent.

Three reader rules therefore do **not** carry into discovery, each with a stated
reason as the Status line requires:

| Reader rule | Status in discovery | Why |
|---|---|---|
| No scrolling (philosophy §3, principle 1) | **Lifted** | It exists so a cook never loses their place mid-task. A browser has no place to lose. |
| One mandatory gesture (philosophy §3, principle 3) | **Lifted** | It protects a cook who cannot tap precisely. Not the situation here. |
| Show the verb, say the noun (philosophy §3, principle 2) | **Partially lifted** | Icons carry actions. Discovery is about *which dish* — only a name and a picture carry that. Words do more work here. |

What carries across unchanged:

- **Every number carries a date and a source** (philosophy §3).
- **Never present a computed estimate as a fact** (philosophy §3).
- **Feedback is telemetry, never published** (philosophy §8). The most consequential
  inherited constraint — see §6.

---

## 4. The governing question

philosophy §16.1 states it: *how do I help you decide fast without pretending I know you.*

**Proposed answer: the user supplies the constraint, the app subtracts.**

Not "here is what you'll like." The app has no basis for that on day one, and philosophy §8
denies it the behavioural data that would ever furnish one. What it can honestly
do is take a constraint the cook already holds — *it's Tuesday, forty minutes,
two of us* — and remove everything that fails it.

Subtraction is honest in a way ranking is not. It explains itself in one
sentence, it cannot be wrong, and the user stays the author of the decision.

This is philosophy §13's menu-suggestion machinery at single-dish scale. They should share
a vocabulary and an implementation — a second reason philosophy §16.7 is on the critical
path.

**Locale note.** Constraint *axes* must be universal; their *calibration* is
not. Spice level, effort, and course all mean different things by market, and
cuisine is the tag whose presentation is most locale-relative. The vocabulary
should be closed and global per philosophy §16.7; only the display is localised.

---

## 5. The card is the unit

A shelf entry must answer *why this one* before anything else, because philosophy §9
removed the alternative versions a user would otherwise compare against.

| Element | Field | Why it earns the space |
|---|---|---|
| Name | `title` | — |
| Image | `hero` | The only element that works pre-attention |
| Why this version | `why` | philosophy §9's obligation, discharged here or nowhere |
| Cost per serving | `cost_per_serving` + `price_source` | **Locale-conditional** (§2.1) |
| Hands-on time | `hands_on_minutes` | The real question behind "is this a weeknight dish" |

Deliberately **not** on the card: nutrition. philosophy §2 assigns it a findable panel and
the job of authorising, not informing. Putting kcal on a browse card converts
Matbakh into a diet app by accident.

**`why` becomes load-bearing** — and doubly so in locales without cost, where it
is the *only* differentiating element left on the card. It is currently a schema
field with no surface depending on it. This section makes it the most important
string in the recipe, written once per dish, per language. That is an editorial
cost not in the ~$40 per-recipe model (philosophy §16.6), and it recurs on every locale.

---

## 6. What philosophy §8 forbids, and what that buys

philosophy §8 settles that cooks may report but never publish. Discovery inherits this,
removing the standard toolkit entirely: no ratings, no star averages, no review
counts, no "most cooked this week," no popularity ordering, no social proof.

**This should be marketed, not apologised for.** Every competitor's discovery
surface is ranked by aggregate behaviour, which is why they converge on the same
twelve dishes. Matbakh cannot do that. What it has instead is a stated reason
for every item being present — `why`, again.

**What ordering remains:**

1. **Editorial** — the curator's order. Locale-specific (§2.4).
2. **User-constrained** — the result of §4's subtraction.
3. **Objective sorts** — hands-on time ascending everywhere; cost ascending only
   where the feed exists.

Telemetry still runs. philosophy §8 and philosophy §4.7 already collect abandonment-by-step, the
strongest editorial signal in the product. It informs what the curator promotes.
It never becomes a number on a card.

---

## 7. Two surfaces, not one

**FORK.**

**First run — the case for the collection.** No constraint yet; the user is
deciding whether this app is serious. Demonstrate range and standards fast.
Editorial, wide, not personalised, honest about size.

**Return visit — the case for tonight.** The user has a constraint. Subtract, in
as few taps as possible. In a priced locale, philosophy §2 makes cost the
natural default axis and the notification's landing surface. **In an unpriced
locale this surface has no defined return trigger** — which is §2.1's problem
resurfacing, and the strongest argument for treating the price feed as a launch
gate per market rather than an enhancement.

The alternative — one adaptive surface that changes with familiarity — is
rejected as personalisation theatre, which philosophy §16.1 warns against by name. But it
is a real fork.

---

## 8. Search

With a finite collection and no duplicates, search-by-name works whenever the
user arrives knowing the dish. Cheap, and it should exist.

- **Normalisation is a per-script concern, resolved like philosophy §15's dialects.** For
  Arabic: ة/ه, ي/ى, hamza forms, and diacritics normalised rather than
  corrected. Each new script adds a normalisation pass, not a redesign.
- **Dish names cross scripts; they do not translate.** *koshari*, *kushari*,
  *كشري* and *كشرى* must all land on the same dish. A user in London searching
  Latin characters for an Egyptian dish is the normal case, not an edge one.
- **Ingredient search is deferred.** "What can I make with what's in the fridge"
  is a pantry feature with no schema behind it. Different surface, argued
  separately if at all.

---

## 9. The empty shelf

Subtraction over a finite collection with several constraints will return three
results, or none. This is the failure mode of the whole approach.

**Never return zero silently.** When the constraint set empties the shelf, show
the nearest results with the failing constraint named — *four dishes match, none
under 30 minutes; these are 35–40*. The user relaxes their own constraint rather
than the app guessing which mattered least.

**This is a launch problem, not an edge case.** A locale opening with 80 recipes
empties far faster than Cairo at 500. The minimum viable shelf size per locale
is an unanswered question that belongs with §2.3.

**A consequence of philosophy §11's diet discipline.** Dietary tags are withheld entirely
when any ingredient's `diet` is unset, so a *vegetarian* filter excludes recipes
of unknown status — an incomplete ingredient library shrinks results invisibly,
and each new locale starts with an incomplete one. Discovery must be able to say
*31 dishes match; 4 more are excluded because their dietary data is incomplete*,
or the shelf silently lies about its own size at exactly the point a guest's
dinner depends on it.

---

## 10. Where `shorts` lives

philosophy §7 evicted technique video from cook mode on the principle that a step needing a
video is authored wrong, and gave technique clips a Techniques library. `shorts`
(philosophy §11) has had no home since.

**Proposed: discovery.** Pre-commit, seated, thumb already scrolling, deciding
rather than doing. Every objection in philosophy §7 — precise taps with wet hands, breaking
the critical path — is specific to cook mode.

**Locale caveat.** Video is the least portable asset in the product: unlike the
lexicon, it cannot be re-rendered per language. Following philosophy §15's logic, shorts
should be **wordless or captioned, never voiced** — otherwise every locale is a
reshoot, and the one genuinely portable acquisition asset becomes the least.

---

## 11. What discovery must not do

- **No infinite feed.** Contradicts philosophy §1.
- **No personalisation before there is anything to personalise on.** philosophy §16.1 warns
  against it by name.
- **No algorithmic ranking presented as authority.** philosophy §8 forbids the input.
- **No nutrition on browse cards.** philosophy §2.
- **No bare numbers, and no cost affordance that resolves to nothing.** philosophy §3, §2.2.
- **No hiding the collection's size.** Finiteness is the promise.

---

## 12. What this section does not settle

- **philosophy §16.2** — pre-commit presentation of cost and nutrition. §5 takes a position
  on the *card*; the recipe page before commit is larger and remains open.
- **philosophy §16.7** — the tag vocabulary. §4 is unbuildable without it.
- **philosophy §16.3** — the meal planner. Adjacent, deliberately untouched.
- **§2.3** — one shelf or many. The largest open question here.
- **Minimum viable shelf size per locale.** Raised in §9, unanswered.
- **Collections.** Whether editorial groupings (Ramadan, weeknight, one-pan) are
  a first-class object with their own schema, or saved filter states.

---

## Proposed decision-log entries, if accepted

| Date | Decision | Section |
|---|---|---|
| — | Discovery is a shelf, not a feed | 1 |
| — | Locale capability flags compose the card; no affordance resolving to nothing | 2 |
| — | Every locale needs an editor before it needs recipes | 2.4 |
| — | Reader constraints on scroll and gesture lifted for discovery, with reasons | 3 |
| — | User supplies the constraint; the app subtracts. No inferred preference | 4 |
| — | Browse card: title, hero, `why`, cost (locale-conditional), hands-on | 5 |
| — | No ratings, counts or popularity ordering; editorial + objective sorts only | 6 |
| — | Never return zero; name the failing constraint and the withheld-data count | 9 |
| — | `shorts` lives in discovery; wordless or captioned, never voiced | 10 |
