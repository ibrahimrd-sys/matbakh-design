# Recipe tags — proposal

> **CLOSED 24 Sept 2026 — see `philosophy.md` for the decision-log entry.
> This document is now historical/reference, not a live proposal.**
>
> The field list below is the final one, as settled. What changed between the
> 1 August draft and closure is listed at the foot, under *Changed at closure*.

Draft for review, 1 August 2026. Written to unblock §13.4 (the party plan) and
§13.7 (filters), and to be settled **before authoring reaches volume** — tags
are the one thing genuinely expensive to retrofit.

---

## The governing rule: derive what can be derived

Every hand-entered tag is five hundred chances to be inconsistent. A
`vegetarian` flag that is wrong once is worse than no flag at all, because a
guest goes hungry and the filter loses its credibility permanently.

So the scheme is split in two:

- **Authored** — genuine editorial judgement. Nine fields, all short.
- **Derived** — computed from the steps and the ingredient reference at build
  time. Never typed, never able to drift.

The test for which side a tag belongs on: *could a careful person disagree?*
Cuisine is a judgement. "Contains dairy" is a fact about the ingredient list.

---

## Authored, per recipe

```yaml
tags:
  cuisine: egyptian          # one, the primary claim
  course: main               # one
  main_protein: beef         # one
  occasion: [everyday, ramadan]   # zero or more
  spice: 1                   # 0–3
  effort: moderate           # easy | moderate | involved
  holds: warm                # serve_immediately | warm | room | cold | better_next_day
  season: [summer]           # zero or more, omit for year-round
  contains_override: []      # rare; see below
```

### cuisine — closed list

`egyptian · levantine · gulf · north_african · turkish · persian · italian ·
french · chinese · indian · american · mexican · japanese · greek · spanish ·
thai · latin_american · eastern_european`

**`thai`, `latin_american` and `eastern_european` added at closure.**
`eastern_european` bundles Russia, on the same pattern as `gulf` and
`north_african` — a region that earns one filter value, not five with two
recipes each.

One value. A dish is *from* somewhere. If a recipe genuinely needs two, that is
usually a sign it needs a better name.

Kept short deliberately — a filter is a promise, and a list of forty cuisines
with two recipes each reads as thinness, which is precisely the risk §13.1
raises about discovery.

### course — closed list

`main · side · salad · soup · bread · sauce · dip · pickle · dessert ·
breakfast · drink · component`

`component` is the one doing real work: it marks a recipe that exists to be
consumed by another recipe — a spice mix, a dough, a stock. Already a settled
concept (components are first-class recipes, never duplicated); this is how the
planner knows not to suggest tahini sauce as a dish in its own right.

### main_protein — closed list

`beef · poultry · seafood · pork · vegetarian · mixed · none`

One value. **A new authored field, formalised at closure** — §16.7 has asked for
protein since 1 August and the draft never gave it a field. It is authored
rather than derived because it is the dish's *claim*, not its ingredient list: a
soup with a spoonful of stock is not a poultry dish, and `contains: poultry`
cannot tell the difference. `mixed` is for a dish built on two proteins at once;
`none` is for bread, pickles and drinks, where the question does not apply.

### occasion — closed list

`everyday · guests · ramadan · eid · siami_seafood · siami_no_seafood ·
celebration · picnic · make_ahead_meal`

`ramadan` and `eid` matter commercially. Ramadan is the single largest cooking
event in the Egyptian year and the obvious moment for a sponsored collection.

**`siami` is split in two, at closure.** `siami_seafood` is the Nativity Fast,
which permits seafood; `siami_no_seafood` is Great Lent, which does not.

The split is doing work no derived tag can do. A `siami_no_seafood` dish will
generally also carry the derived `vegan` tag. A `siami_seafood` dish will not —
it contains fish — but it still excludes meat, poultry and dairy, and **no
single derived tag captures that combination.** The occasion tag is the only
thing that can answer the question a cook actually asks during the fast.

### spice — 0 to 3

`0` none · `1` warm, not hot · `2` noticeably hot · `3` hot

A number rather than a word because the party brief says *not too spicy*, which
is a threshold, not a category. Filtering wants `spice <= 1`.

### effort — three values

`easy` under 30 minutes hands-on, nothing that can go wrong ·
`moderate` ·
`involved` long, or has a step where timing genuinely matters

Not difficulty. A cook planning twelve covers needs to know how many involved
dishes they are signing up for, and the answer is one.

### holds — how long it survives after cooking

`serve_immediately · warm · room · cold · better_next_day`

**This field only exists because of entertaining, and it is the one the party
plan cannot work without.** It is what decides the order in §13.4's task list:
anything `better_next_day` moves to the day before, and only one or two
`serve_immediately` dishes can sensibly be in a menu at all.

### season

`summer · winter · spring · autumn`. Omit for year-round. Ties to the price
feed — a tomato salad in February is a different recipe economically.

---

## Derived at build time — never authored

Computed by `matbakh.py` from the steps and the ingredient reference:

| Tag | Derived from |
|---|---|
| `contains` | union of `diet` classes on every ingredient used |
| `vegetarian` | no `meat`, `poultry`, `fish`, `shellfish` in `contains` |
| `vegan` | the above, plus no `dairy`, `egg`, `honey` |
| `gluten_free` | no `gluten` |
| `total_minutes` | `hands_on_minutes` + the sum of timers |
| `stations` | the distinct stations across the steps |
| `cost_per_serving` | shopping list × market feed ÷ servings |
| `kcal_per_serving` | already computed from step amounts |

`contains_override` exists for the cases derivation cannot see — a recipe that
calls for stock made from a bird, where the stock is an intermediate rather than
a listed ingredient. Rare, and the validator should warn when it is used, since
its normal use is to paper over a missing `diet` field.

**Confirmed at closure:** every use of `contains_override` is **auto-flagged for
validator review**, per this document's own caution above. It is the one
authored field that can silently contradict the ingredient reference.

**`contains: pork` is meaningful again**, now that pork is back in the catalogue
(Revision 2, 14 September). Checked at closure: nothing treats it as permanently
false — `matbakh.py` excludes `pork` in both the `vegetarian` and `vegan`
derivations, the ingredient editor carries it in the `diet` vocabulary and
proposes it for bacon, pancetta and ham, and the reference and the bolognese
recipe both use it.

---

## What this needs on the ingredient side

One new field on every ingredient, and it is the prerequisite for everything
above:

```yaml
chicken_whole:
  diet: [meat, poultry]
eggs:
  diet: [egg]
cheese_feta:
  diet: [dairy]
flour:
  diet: [gluten]
anchovy:
  diet: [fish]
onion:
  diet: []
```

Vocabulary: `meat · poultry · fish · shellfish · dairy · egg · gluten · nuts ·
peanut · sesame · soy · honey · alcohol · pork`

**Glyph cannot substitute for this.** Checked against the current 179:
`fish_filet` carries a `meat` glyph, `eggs` sits under `dairy`, `anchovy` is a
`jar`. Glyph is a drawing hint; this is a taxonomy, and conflating them would
produce exactly the wrong-once failure the whole scheme is designed to avoid.

The ingredient editor should make this a required field with a multi-select, and
`matbakh.py` should refuse to derive dietary tags for any recipe using an
ingredient that lacks one — silence is worse than refusal here.

**How much work this is.** Tested against the current 179: roughly 109 can be
proposed automatically from the name — anything containing *chicken*, *cheese*,
*flour*, *tahini*, plus every vegetable and spice which is plainly `[]`. The
remaining 70 need an eye, and most are obvious once seen (`mozzarella` and
`pecorino_romano` are dairy, `fusili` gluten, `chocolate_chips` usually dairy).
With a bulk-propose button in the ingredient editor this is an hour, not a week
— and it is an hour that has to happen before recipe two, not after recipe two
hundred.

---

## The worked example

Twelve covers, Mexican, beef and chicken over seafood, two vegetarians, not too
spicy, a salad, 1,500 LE. That resolves to:

```
cuisine = mexican
course covers {main, main, side, salad, dip}
spice <= 1
at least 2 recipes with vegetarian = true
excludes fish, shellfish in contains
sum(cost_per_serving × 12) <= 1500
at most 1 with effort = involved
at most 2 with holds = serve_immediately
```

Every line is a filter over the fields above, and the last two are the ones a
host would never think to ask for but would feel the absence of — which is the
argument for `effort` and `holds` earning their place.

---

## Changed at closure — 24 September 2026

The three questions this document left open are resolved, and the *Open* section
is removed with them.

| | Draft, 1 August | Closed, 24 September |
|---|---|---|
| **One cuisine per recipe?** | Open — Ottoman and Levantine inheritance might need two | **One value, kept.** Three values added to the list instead: `thai`, `latin_american`, `eastern_european` |
| **Is `occasion` a tag or a collection?** | Open | **A tag, kept** — and extended, with `siami` split into `siami_seafood` and `siami_no_seafood` |
| **Is `hidden` worth having?** | Open — `course: component` may cover it | **Removed.** `course: component` already keeps sub-recipes out of suggestion, and a work-in-progress recipe should not be in the authored catalogue at all until it is finished. A third mechanism is redundant |

**Added:** `main_protein`, as a closed-list authored field. **Removed:**
`hidden`. Still **nine authored fields**, and the derived set is unchanged.

**Not closed here, and not part of this decision:** how filters compose in the
interface — `philosophy §16.7` distinguishes the vocabulary from the interaction
model, and only the vocabulary is settled. **S-07**, the translation layer for
derived tag keys, also stays open.
