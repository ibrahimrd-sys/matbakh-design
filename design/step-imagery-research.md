# Step photography vs the icon lexicon — research and options

**For:** the C-05 / PM-07 decision — whether to freeze an 81-activity icon set or
replace it with step-by-step photography.
**Written:** 18 August 2026, before any icons are commissioned.
**Status:** Research and options. No decision taken.

---

## 0. The question is narrower than it looks

**Matbakh already has step-by-step photographs.** The schema carries `photo` and
`doneness` on every step, and they are specified to travel together. Recipe 1
uses them on **six of its eight pages**:

| Page | Station | Photo | Doneness cue |
|---|---|---|---|
| 1 | Board | ✓ | Onion in even dice — no piece thicker than a matchstick |
| 2 | Stove · stock | ✓ | Meat lets go of the bone when you push it |
| 3 | Bench | — | — |
| 4 | Stove · takliya | ✓ | Straw-gold at the edges. One shade past this is bitter |
| 5 | Stove · pot | ✓ | Thick enough to coat the spoon. No bubbles at the surface |
| 6 | Stove · pot | — | — |
| 7 | Grill | ✓ | Lacquered, blistered in places, dry to the touch |
| 8 | Serve | ✓ | Soup, rice and lemon on the table together |

`asset-spec.md` already specifies their geometry down to the crop — 2.05:1 on the
phone, shoot 4:3 or 3:2 with the subject inside the middle 65% vertically.

So the real question is not *photographs or icons*. It is:

> **Should the 44px tile glyph — the thing that says what your hands do — become
> a photograph, when the page already carries a photograph of the result?**

That is a much sharper question, and the evidence answers it more clearly than
the vague version does.

---

## 1. What the evidence actually supports

Seven findings that bear directly. Strength is marked honestly; two of the things
people commonly assert here turn out to be weaker than their reputation.

### 1.1 Words *and* pictures beat words alone — this says nothing about pictures alone — **strong**

Mayer's multimedia principle (11 experiments, median **d = 1.39**) compares words
+ pictures against **words alone**. The condition "pictures with no words" was
never tested. It is routinely miscited to justify wordless interfaces. It does
not do that work.

### 1.2 Removing irrelevant detail matters *more* than adding pictures — **strong, and this is the crux**

Mayer's **coherence** principle runs at **d = 1.66** across 6+ experiments —
a *larger* effect than the multimedia principle itself. Extraneous material hurts.

This is the central argument against a photograph in the tile. A photograph of a
hand chopping an onion contains the hand, the knife, the board, the counter, the
light, the background — of which one thing is the instruction. A `chop` glyph
drawn to Matbakh's own spec is *three strokes or fewer*. The icon is not a
lower-fidelity photograph; it is the photograph with the coherence violation
removed.

### 1.3 A picture that repeats the adjacent word is fine, but only modestly worth it — **moderate**

The relevant literature is Carney & Levin's picture-function taxonomy, not the
redundancy principle (which is about *two verbal channels*, narration plus
identical on-screen text, and does not apply here — a very common misreading).

Pictures that mirror adjacent text are *representational*, worth about
**g = 0.24** (Schewior & Lindner 2024, 62 studies). Real but small. **Decorative
pictures show no measurable effect at all** — and a photograph that duplicates
the noun printed beside it is drifting toward decorative.

Worth noting: this is precisely the failure the tile had until yesterday. The
builder was drawing the *ingredient* and printing its name beside it, so the icon
carried nothing the words didn't. `asset-spec.md` already forbids it — *"Draw the
action, not the ingredient"* — which is why that fix was a return to spec, not a
new opinion.

### 1.4 Show the ACTION, not the finished state — **strong, and it cuts both ways**

Heiser et al. (2004, Stanford) validated *"action over structure"* on assembly
instructions: diagrams showing the action, with the changing element separated
and a guideline to its destination, beat diagrams showing the part already in
place. Cognitively-designed instructions completed in **10.2 min / 0.5 errors**
against IKEA-style factory sheets at **16.04 min / 0.6 errors**.

Note carefully what that comparison says: the wordless factory diagrams were
**not error-prone** — 0.6 versus 0.5 — they were **slow**. The wordless premise
survives; the execution is what costs time.

The awkward part for the photography proposal: **a still photograph is bad at
depicting an action and good at depicting a state.** A frozen frame of a hand
mid-chop is ambiguous — is it chopping, slicing, mincing, pressing? A frozen
frame of straw-gold garlic is unambiguous. Matbakh's §5.2 already routed doneness
to photographs for exactly this reason. The split the design already makes —
**icon for the action, photograph for the state** — is the one the evidence
supports.

### 1.5 Glance cost is set by encoding, not by size or realism — **strong**

Smartwatch study (Blascheck et al. 2018): the exposure needed for ~91% accuracy
was **245 ms for bar charts, 159 ms for donuts, and 1,548 ms for radial bars** —
same data, same tiny screen, a **10× spread** driven purely by how it was
encoded. Size is not the variable. Decodability is.

And place-keeping is the thing to protect: sequence errors — losing your position
in a procedure — rose from **~2% after a 2.76 s interruption to ~12% after
31.91 s** (Altmann, Trafton & Hambrick 2017). Which is §4.2's point,
independently measured: the expensive thing is not turning a page, it is
reconstructing where you were.

### 1.6 "Line drawings beat photographs" is real but much weaker than its reputation — **contested; do not lean on it**

The classic citation (Ryan & Schwartz 1956) is a single 68-year-old
tachistoscopic study of *recognition speed*, never replicated for instructional
tasks. Dwyer's "simple drawings win under time pressure" qualification is
repeated everywhere but hard to verify at source.

The honest modern position is Skulmowski & Rey (2021), who explicitly reject
blanket statements in either direction: **realism helps retention and retrieval
and helps high-spatial-ability learners; realism hurts transfer and hurts
novices**, because perceptual load consumes working memory. And there is a
counter-example — Salmon et al. (2014) found photographs of manipulable objects
were *named faster* than line drawings, by 14 ms.

**Use this as a tilt, not a proof.** Cook mode is time-pressured, glance-based
and read by novices, which is the quadrant where simplification is favoured. That
is an argument, not a finding.

### 1.7 Abstraction, not photography, is what fails cross-culturally — **strong, and there is an Egypt-specific number**

The reliable predictor of comprehension is **concreteness of the referent**, not
whether it is a photo or a drawing. Piamonte et al. (2001): concrete
object-depicting symbols scored **75–87.5%**; abstract ones scored **0–12.5%** —
in Sweden *and* the USA. Zender & Cassedy found 33 of 47 poorly-understood icons
failed from unfamiliar domain or technology, and only 5 of 47 from cultural
difference; the killers were **metaphor** and embedded text-like signs.

The sobering one, and it applies to icons and photographs equally: **sequential
image comprehension is a learned convention, not a perceptual universal.** Cohn
(2019) reports that in **rural Egypt, only 4–8% of 9-year-old village children
produced coherent sequential visual narratives**, against far higher rates among
suburban Cairo children with picture-book exposure.

For an Egypt-first wordless product that is worth knowing plainly. It does not
argue for photographs over icons — it argues that **any** multi-panel visual
grammar carries an assumed literacy, and that the map (§4.4) leans on that
grammar hardest.

### 1.8 What nobody knows

**There is no published engagement, retention or completion data comparing
recipes with step photographs against recipes without.** Not from Cookpad, not
Kitchen Stories, not Tasty, not DELISH KITCHEN. And there is **no controlled study
of pictorial versus photographic instruction under kitchen conditions at all** —
the only cooking-specific source found is qualitative (ASSETS '24).

This decision cannot be settled by citing anyone. It can only be argued from
craft, or measured in-house. Which is what §7 proposes.

---

## 2. What the market actually does

Six findings, several of which contradict the common assumption.

**Step photos are optional even at Cookpad, even in Japan.** Cookpad's own
contributor guidance in Japan, South Africa and the Arabic edition asks only for
a **finished-dish** photo. Japanese contributors add step photos anyway — a norm
sustained by community culture, not product enforcement. In an Arabic sample the
pattern was bimodal: three recipes had a photo on every step (5/5, 8/8, 13/13),
two had almost none (1/4, 0/6). **A UGC norm is not available to Matbakh** —
one-recipe-per-dish, founder-authored, means every image is a cost line.

**Kitchen Stories — the reference implementation — controls the budget by
compressing the recipe, not by dropping photos.** Recipes inspected had exactly
**3 steps and 3 step photos**, roughly 5 images per recipe including hero and
plated shot. Shot in four in-house Berlin show kitchens, never shooting an
untested recipe.

That is the most important product finding here, because **Matbakh targets 6–10
pages with a 14 ceiling**. Photo-per-page at Matbakh's granularity is two to
three times Kitchen Stories' asset count per recipe. Either the image budget
triples, or page count compresses — and compressing pages fights §4.1's
order-independence rule, which is settled.

**Kitchen Stories went from 12 languages to 2.** Reported as available in 12
languages in 2015; today the App Store lists English and German only. No published
explanation, so causation is unproven — but it is exactly what a per-recipe
fixed-asset cost model predicts.

**The video-first apps replaced step stills entirely.** Kurashiru: one ~60s video,
zero step images. DELISH KITCHEN: a looping micro-clip per step — and their
operation is ~1,000 videos/month with **~30 food stylists**, fixed cameras at
each booth, and **271 documented production rules** covering hand direction, tool
centring and seasoning speed. That is roughly **1.5 finished assets per stylist
per day** in a purpose-built studio. It is the throughput ceiling for a
systematised operation, and it is the strongest evidence that per-step imagery is
an industrial commitment, not a content decision.

**Google does not force this.** In the Recipe structured-data spec,
`HowToStep.image` is a **Recommended**, not Required, property. There is no SEO
gun to the head.

**No Arabic or MENA recipe product publishes an editorial policy on step
imagery**, and Atyab Tabkha — whose recipe URLs literally say *بالصور* — carries
no per-step images at all; the phrase refers to the hero shot.

---

## 3. The three constraints from Matbakh's own documents

These are not new opinions. They are already settled, and two of them bind hard.

### 3.1 The 17px map thumbnail — this is decisive

`asset-spec.md`: *"An icon has to survive a 3.6× range, from 17px to 62px. **The
17px arc thumbnail is the binding constraint.**"*

And §4.4 already answered the photography question for the map, in as many words:

> *"Thumbnails are icon clusters, not photos. Miniaturised step photos are eight
> indistinguishable brown pans."*

**A photograph cannot serve the map, and the map is not optional** — it is the
progress indicator, the thirty-seconds-before-starting view, and the thing §4.4
identifies as something no other recipe app offers.

The consequence is unavoidable: **even a full photo-per-step design still needs
the icon set.** Photographs cannot replace icons. They can only be added to them.
That single fact reframes the whole trade — this is not *icons or photos*, it is
*icons, or icons plus a great deal more work*.

### 3.2 Wordless assets are made once

`asset-spec.md`: *"An asset that carries no words is made once. An asset that
carries words is made again for every language."*

Photographs satisfy this — they are language-neutral. But the market evidence
says they are **not market-neutral**: Tasty produces roughly half its localised
output as net-new shooting per market; Cookpad reaches 16 languages only by
pushing photography onto users. Ingredients, packaging, utensils and hands are
all visible market signals.

For Egypt-first this barely binds. It binds hard at Gulf expansion — and §10
already warns against false confidence about the cost of market entry.

### 3.3 Consistency is structural, not decorative

`asset-spec.md`: *"A cook reading a doneness photo is comparing it to the pan in
front of them. If the light, angle and distance shift between recipes, the
comparison stops working... This is why a permanent studio setup matters more
than a good camera."*

This is already the strongest argument **for** investing in photography — and it
applies to the doneness photographs that already exist, whether or not tiles ever
become photographic.

---

## 4. Cost

The surprising result: **cost does not decide this.** Both options are affordable;
they consume different resources.

### Icons

~60 activity glyphs plus ~25 ingredient-category glyphs, built on Tabler (MIT).
Effectively a **one-time cost with zero marginal cost per recipe**. Recipe 500
costs exactly what recipe 1 did: nothing. The outstanding work is C-05 — verify
glyph names against tabler.io, since several are invented, and resolve the
collisions the pilot has surfaced.

### Photography, at Egyptian rates

This is where the numbers are genuinely favourable, and they support the
conclusion `asset-spec.md` already reached — a permanent setup, not a day rate.

| Line | Figure |
|---|---|
| Cairo studio package | **7,000 EGP (~$139)** for a 2-hour food shoot, all images edited |
| Cairo photographer salary | **8,400–22,300 EGP/month gross (~$168–445)** |
| Camera body, in Egypt | Canon R50 kit **~40,000 EGP (~$800)** — imported gear runs 20–50% above US street |
| Entry rig, Egypt | **~$1,000–1,500** — used body, 50mm, one COB + softbox, C-stand + boom |
| Mid-tier two-station rig | **~$4,000–6,000** |
| Step-image throughput, one person | **~30–50 finished images/day** sustained, cooking dishes they are cooking anyway |

**A mid-tier rig plus a Cairo in-house shooter for a year costs less than a single
US commercial shoot day.** For contrast, published US/UK cookbook photography runs
**$400–900 per photographed recipe** — and that is hero images only. Step images
are essentially never in a trade cookbook budget, because print cookbooks don't
carry them.

At Matbakh's scale — 500 recipes × ~8 pages ≈ **4,000 step images** — the shooting
alone is **80–130 working days**. That is the real cost, and it is not money.

**It is founder time, and founder capacity is R-06, already the binding constraint
everywhere.** Four to six months of one person's shooting days, spent before the
catalogue exists.

### AI generation is not a way out

As of August 2026 there is **no published example of a recipe product credibly
shipping generated step imagery for real dishes**, and the documented failures are
precisely the failure that matters here — *the dish is recognisable but the stage
is wrong*:

- AI-generated tamale images showing husks **lying flat and sauced** instead of
  standing upright during steaming (Fortune, Nov 2025)
- Instacart's generated recipe imagery: a roast chicken with **two pairs of
  wings**, green onion slices floating in mid-air, a mug made of chocolate cake —
  deleted after press coverage
- Cross-image consistency, which a step sequence needs absolutely: reported
  **~90% failure placing 6+ objects** accurately in one scene, and visible drift
  between frames in a session. A mise-en-place shot routinely has 6+ objects.

And there is a positioning argument beyond quality. AI imagery is now an active
**trust liability** in food content — visible consumer backlash, and food blogs
reporting heavy traffic collapse amid the slop wave. Matbakh's entire claim is
curation and trust. Generated step imagery would spend exactly the asset the
product is built on.

**The credible AI play is enhancement of real capture** — colour, cleanup,
background — not synthesis.

---

## 5. Where photographs genuinely win

Stating the case for the proposal at its strongest, because it has real merit:

- **A state is unambiguous in a photograph and nearly impossible in an icon.**
  *"Straw-gold at the edges. One shade past this is bitter"* cannot be drawn in
  three strokes. §5.2 already concedes this and routes doneness to photography.
- **The failure photograph is the highest-value image in the product and nobody
  has it.** `asset-spec.md` already suggests shooting *one shade past* — the
  bitter takliya. That single image is worth more than any icon, and no
  competitor has it.
- **Photographs need no lexicon.** They sidestep the four collision pairs, the
  seven demotions and the 15 slash-glosses in the MSA verbs entirely — none of
  those problems exist in a photograph.
- **Photographs are language-neutral by construction**, which is the same
  argument the lexicon makes, applied to pictures.
- **Trust.** A photograph of *this* dish at *this* stage is evidence the recipe
  was actually cooked. Given the one-recipe-per-dish promise, that is
  brand-consistent in a way an icon set is not.

---

## 6. The options

### A — Icons only, as designed
81 activity glyphs; photographs stay where they are, on the page paired with
doneness. **Cost:** effectively zero marginal. **Risk:** the pilot is already
finding the icon layer is the weak part — four activity pairs share a glyph, six
activities draw ingredients rather than actions, and several glyph names are
invented. Those are fixable, but they are real.

### B — Photographs replace icons
**Not viable.** It breaks the map at 17px, which §4.4 has already settled and
`asset-spec.md` names as the binding constraint. You would still need the icon
set for the arc, so this option does not remove any work — it only adds.

### C — Icons for the action, photograph for the state *(the current design, fully executed)*
Exactly what the schema already encodes. The gap is not missing photographs — it
is that the icons are unfinished and the photographs are placeholders. **Cost:**
finish C-05, then shoot to `asset-spec.md`. **This is the lowest-risk path and
the one the evidence supports**: icon carries the action (coherence, glance cost,
survives 17px), photograph carries the state (unambiguous, high-value, already
specified).

### D — C, plus a process photograph on the pages that earn it
Add a *second, optional* photographic slot for steps where the action itself is
genuinely hard — a windowpane dough, a stuffing technique, a fold. Escalation
rather than uniformity, exactly as technique shorts already work (§7: *if a step
needs a video to be understood, the step is wrong* — the same logic scales down
to process stills). **Cost:** bounded, because it applies to perhaps 10–20% of
steps. **Risk:** a new schema field and an editorial judgement per step.

---

## 7. Recommendation

**Take C now, and test D inside the pilot rather than deciding it in the
abstract.**

The reasoning in one line: **photographs cannot replace icons because of the 17px
map, so the only real question is whether to add photographic work on top — and
that question has no published evidence behind it, which means it should be
measured on the fifteen recipes you are already cooking.**

Concretely, and at near-zero extra cost:

1. **Do not commission 81 icons yet.** The pilot exists precisely to test the
   vocabulary, and it is already returning findings. Finish C-05's glyph-name
   verification first — several are invented — and resolve the four collision
   pairs.
2. **While cooking pilot recipes 2–15, shoot the step photographs anyway.** You
   are standing at the pan with the dish in front of you; this is the cheapest
   these images will ever be. A phone on a locked-off overhead mount is adequate
   for step frames — the published objections to phones (shallow depth of field,
   lens choice, low-light headroom) are all *hero-shot* concerns, and step images
   want deep focus and a wide overhead frame. Shoot to `asset-spec.md`: 4:3 or
   3:2, subject in the middle 65% vertically.
3. **Add one column to the pilot tracker: "would a photo have said this better
   than the icon?"** per tile. Fifteen recipes gives roughly 150 judgements —
   the only dataset on this question that will ever exist, since nobody has
   published one.
4. **Shoot one failure photograph.** One shade past on the takliya. If it lands
   the way `asset-spec.md` expects, that is the strongest evidence for scaling
   photographic investment, and it costs one extra pan of garlic.
5. **Decide D after the batch**, using the same discipline the pilot already
   applies to the lexicon: measure first, decide once.

**What would change this recommendation:** if the pilot finds that a large
fraction of actions are unclear as icons — the same ≥3-recipe threshold used for
adding a verb — then the icon layer is not carrying its weight and D becomes
mandatory rather than optional. That is a finding the pilot can produce and
nothing else can.

---

## 8. Two things to fix regardless

- **`season` and `to_taste` both draw `salt`,** and both appear in molokhia. A
  fourth collision pair, not on the flagged list.
- **Six activities draw ingredients rather than actions** — `cut_wedges` (fixed),
  `zest`, `garnish`, `season`, `to_taste`, `simmer`. This violates
  `asset-spec.md`'s own rule: *"Draw the action, not the ingredient."*

---

## Sources

**Cognitive and instructional evidence**
Mayer, *Multimedia Instruction* (2014) · Carney & Levin, *Educational Psychology
Review* 14(1) (2002) · Schewior & Lindner, *Educational Psychology Review* 36(2)
(2024) · Heiser, Phan, Agrawala, Tversky & Hanrahan, AVI'04 (2004) · Agrawala et
al., SIGGRAPH (2003) · Skulmowski & Rey, *Educational Psychology Review* (2021) ·
Ryan & Schwartz, *Am. J. Psychology* 69(1) (1956) · Salmon, Matheson & McMullen,
*Frontiers in Psychology* 5 (2014) · Kools et al., *Patient Education and
Counseling* 64 (2006) · Booher, *Human Factors* 17(3) (1975) · Blascheck et al.,
IEEE TVCG (2018) · Matthews et al., UCB/EECS-2006-173 (2006) · Altmann, Trafton &
Hambrick, *JEP: Applied* 23(2) (2017) · Cohn, *Psychonomic Bulletin & Review*
27(2) (2019) · Piamonte, Abeysekera & Ohlsson, *IJIE* 27(6) (2001) · Zender &
Cassedy, *Visible Language* · Hancock et al., *Human Factors* 46(2) (2004) ·
FAA/DOT briefing-card pictorial comprehension study · Li et al., ASSETS '24

**Market and production**
Cookpad contributor guidance (JP/ZA/Arabic) · Kitchen Stories app listings, team
and studio pages · TechCrunch on Kitchen Stories (2015) · Kurashiru recipe pages
and Forbes (2019) · DELISH KITCHEN help docs and amana Insights production
interview · BuzzFeed Tasty press, CNBC and TODAY production accounts · Google
Search Central Recipe structured-data spec · Atyab Tabkha · Wonderful Machine
pricing case studies · Kristin Donnelly and Carla Lalli Music on cookbook
photography budgets · Alex Gell and Clean Plate rate cards · Paylab Egypt · Mkan,
Mediaphic and Sharp Lens Cairo pricing · Fortune (Nov 2025) and Futurism on AI
food imagery failures · V-Flat World iPhone vs mirrorless test

**Matbakh's own**
`design/philosophy.md` §3, §4.1, §4.2, §4.4, §5.1, §5.2, §7, §10, §15, §16.5,
§16.6 · `design/asset-spec.md` · `03-catalogue/recipe-pilot-scheme.md` ·
`02-strategy/matbakh_pm_log.md` (C-05, R-06, PM-07) ·
`03-catalogue/recipes/molokhia.yaml`
