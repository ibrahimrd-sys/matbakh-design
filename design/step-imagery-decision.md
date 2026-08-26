# Shooting the vocabulary, not the catalogue

**For:** the step-imagery decision that gates C-05, the icon commission, and the
doneness-photography scope (`philosophy §16.6`).
**Written:** 21 August 2026, in answer to three considerations put by Ibrahim —
(1) shoot a full video per recipe and extract step frames, (2) shoot the 81
activities to replace the icons, (3) offer the recipe in prose on request.
**Status:** Research, options and a recommendation. No decision taken.

**Relationship to `step-imagery-research.md` (18 Aug):** that document asked
whether the *tile* should become a photograph and concluded C — icon for the
action, photograph for the state. Nothing here overturns it. What it did not
consider is that the action layer can be **shot once for the vocabulary instead
of once per recipe**, which changes the arithmetic by roughly a factor of thirty
and is the substance of this document.

---

## 0. The three considerations are not three options

They are three different layers, and only one of them is actually undecided.

A cook in front of the reader asks four questions. Each is answered in a
different place, at a different size, and each has a different natural carrier:

| The question | Where it is answered | Size | Scales with |
|---|---|---|---|
| **Where am I?** | the arc / map | **17 px** | the vocabulary |
| **What do my hands do?** | the tile | **44 px** | ← *the open question* |
| **Is it ready?** | the doneness photograph | 361 × 176 | the catalogue |
| **Why, and what did I miss?** | prose, on request | — | free, if generated |

Two of those four are already closed, and it is worth being blunt about it
because both of the first two considerations are phrased as *replacing* the
icons, and neither can.

**The arc cannot be photographed or filmed.** `asset-spec.md` names the 17 px arc
thumbnail as the binding constraint, and `philosophy §4.4` settled the question in
as many words — *"miniaturised step photos are eight indistinguishable brown
pans."* A video frame at 17 px is a photograph at 17 px. **Whatever else is
decided, the glyph set gets built.** C-05 is not avoidable by any of the three
considerations; it is owed under all of them.

**The doneness photograph cannot be made generic.** It is the one image the cook
holds against their own pan. *"Straw-gold at the edges. One shade past this is
bitter"* is specific to that takliya in that light. This layer is irreducibly
per-recipe, and always was.

So the real question is narrow:

> **What goes in the 44 px tile — and does it scale with the 81-verb vocabulary,
> or with the 500-recipe catalogue?**

That is the whole decision. Everything below serves it.

---

## 1. The finding that decides the economics

**The action is generic. The state is specific.**

Chopping an onion looks the same in molokhia, koshari and bolognese. *Straw-gold
at the edges* does not — it is this pan, this minute. The two layers have
genuinely different natures, and the mistake available here is to pay
per-recipe for something generic.

Consideration 1 shoots the action 500 times. Consideration 2 shoots it once.
They produce a comparable tile; they differ in cost by more than an order of
magnitude. That is the finding, and the rest of this document is the evidence
for it and the honest case against it.

---

## 2. How much of the vocabulary is actually motion? — 47 of 81

If a loop is worth anything, it is worth it exactly where **a single frame cannot
separate one verb from its neighbours**. So the useful question is not "icons or
video" but "how many of the 81 activities are defined by motion?"

I classified the lexicon on disk (`content/lexicon/activities.yaml`, 81 entries,
78 distinct glyphs). Two classes:

- **Class M — motion-defined.** The verb is distinguished from at least one
  neighbour *only* by how something moves. A still cannot separate them.
- **Class S — state-defined.** The verb is a placement, a configuration, or an
  elapsed condition. A single frame captures it entirely; motion adds nothing.

| Station | Total | Class M | Class S |
|---|---|---|---|
| board | 10 | **10** | 0 |
| bench | 34 | 14 | 20 |
| stove | 19 | 15 | 4 |
| serve | 6 | 3 | 3 |
| grill | 4 | 3 | 1 |
| oven | 5 | 1 | 4 |
| any | 3 | 1 | 2 |
| **Total** | **81** | **47 (58%)** | **34 (42%)** |

**Class M (47)** — `blanch` `blend` `boil` `brush` `char` `chop` `crush`
`cut_wedges` `deep_fry` `deglaze` `dice` `drizzle` `dust` `flambe` `flatten`
`fold` `fry` `grate` `grind` `knead` `ladle` `mash` `mince` `mix` `baste`
`peel` `poach` `pour` `reduce` `roll` `sear` `shred` `sift` `simmer` `skewer`
`skim` `slice` `sprinkle` `squeeze` `steam` `stir` `stir_fry` `strip` `sweat`
`toss` `whisk` `zest`

**Class S (34)** — `add` `bain_marie` `bake` `braise` `brine` `broil` `chill`
`coat` `cool` `cure` `do_not_stir` `drain` `dry` `ferment` `freeze` `garnish`
`grill` `infuse` `inject` `layer` `marinate` `pressure_cook` `rest` `roast`
`season` `serve` `set` `shape` `soak` `stuff` `to_taste` `toast` `wash` `wrap`

**This is my judgement, not a measurement** — mark it as contestable and check it
during the pilot. But three things fall straight out of it and they are not
matters of taste.

**First: the board is 10 for 10.** Every knife verb is motion. This is not a
coincidence — it is *why* `chop` and `mince` share a glyph. Two three-stroke
drawings of a blade over a board are the same drawing. Two two-second loops of a
blade over a board are obviously different things. The collision is an artefact
of the carrier, not of the vocabulary.

**Second: the stove is 15 of 19, and this is the surprise.** `boil`, `simmer`
and `poach` are *defined by bubble behaviour*. As stills they are three pans of
water. As loops they are unmistakable. The stove looked like the station where
photography had least to offer; on this reading it is the second-strongest case
after the board.

**Third, and this is the one worth keeping: two of the three real glyph
collisions dissolve, and the third does not.**

| Collision (verified on disk) | Class | Does a loop fix it? |
|---|---|---|
| `chop` / `mince` — both draw `chop` | M / M | **Yes.** Different motions. |
| `brush` / `baste` — both draw `brush` | M / M | **Yes.** Different motions. |
| `season` / `to_taste` — both draw `salt` | S / S | **No.** |

`season` and `to_taste` are the *same physical act*. What separates them is
intent — *add salt now, measured* versus *adjust at the end, by taste*. **No
photograph, frame or loop can show intent.** That collision is a lexicon problem
or a layout problem, and imagery of any kind is the wrong tool for it. Worth
knowing before spending anything, because it is the one collision that survives
every option in this document.

*(A correction to earlier notes: the handover lists `cut_wedges`/`zest` as a
collision pair. On disk they carry distinct glyphs. Three pairs share a glyph,
not four.)*

---

## 3. What the evidence says about motion — strong, and unusually well-aimed

The 18 Aug research found that the literature could not settle *photograph versus
drawing*. It settles **animation versus still** much more cleanly, and it happens
to be aimed directly at this case.

**Höffler & Leutner (2007), *Learning and Instruction* 17(6) — 26 studies, 76
pairwise comparisons.** Verified against the ERIC record:

| Condition | Effect size |
|---|---|
| Animation over static pictures, overall | **d = 0.37** (95% CI 0.25–0.49) |
| When the animation is *representational*, not decorative | d = 0.40 (0.26–0.53) |
| When the animation is **highly realistic, e.g. video-based** | **d = 0.76** (0.39–1.13) |
| When **procedural-motor knowledge** is to be acquired | **d = 1.06** (0.72–1.40) |

Procedural-motor is the largest moderator in the analysis, at nearly **three times
the overall effect**. Cooking hand-actions are procedural-motor knowledge acquired
from realistic depiction — the two conditions under which the advantage is
strongest, stacked.

This is a materially better-aimed piece of evidence than anything in the 18 Aug
document. The multimedia principle (d = 1.39) was miscited there by everyone who
cites it, because it compares pictures+words to words alone. This one compares
*moving pictures to still pictures* for *motor procedures*, which is exactly the
comparison at hand.

**But length reverses it — and this is the constraint that kills consideration 1's
premise.** Wong, Leahy, Marcus & Sweller (2012) on the transient information
effect: short animations beat static graphics, and **long animations lose the
advantage entirely**, because working memory drowns in transient information. The
same reversal appears for audio-visual versus visual-only material — an advantage
for short segments that "disappears or reverses" with longer ones.

So the evidence does not say *film the recipe*. It says **a few seconds of the
action, repeating**, and it says the advantage decays as that grows. Two
commercial libraries built independently for other domains both converged on
**~6-second clips**, which is a market confirming the same curve.

**The honest limits.** Höffler & Leutner is a 2007 meta-analysis of instructional
settings, not kitchens. Nobody has measured any of this under kitchen conditions —
that gap, noted in the 18 Aug document, is still open and will stay open. And the
d = 1.06 cell is a moderator with 26 studies behind the whole analysis, not 26
behind that cell. Treat it as a **strong tilt with an unusually good aim**, not as
proof.

---

## 4. Every adjacent domain solved this by shooting the vocabulary. Cooking has not.

This is the most useful thing the research turned up, and it is worth stating
plainly: **the "shoot the action library once" model is not novel, experimental or
risky. It is the settled industry standard everywhere except cooking.**

| Domain | Product | Library | Model |
|---|---|---|---|
| Fitness | **Fitbod** | **1,600+ exercises**, professionally filmed | An algorithm generates unlimited workouts by *selecting from* a fixed media library |
| Fitness | Hevy | 400+ exercises, one looping animation each | Same |
| Fitness | ExRx.net | 2,100+ exercises, licensed by API | Same |
| Rehab | Physiotec / Wibbi | **20,000+ exercise videos**, 18+ specialties | Clinicians compose programmes from a fixed library |
| Rehab | Medbridge | 8,000–9,000 video exercises | Same |
| Sign language | **Spreadthesign** | **610,000+ videos, 35 sign languages** | One clip per lexical item, reused in every context |

Fitbod is the exact structural precedent: **the content is generated, the imagery
is drawn from a closed set.** Nobody films a new squat for each workout. That is
Matbakh's situation with the lexicon already in place.

**The libraries are cheap enough to be commodities.** Gym Animations sells **7,000
exercise animations for $599** (1920×1080, 6-second MP4, produced by a team of ten
3D animators). ExerciseDB sells 1,500 with metadata for **$300**. That is roughly
**$0.09–$0.20 per finished clip** at market. It is not a category where costs run
away.

**And now the negative finding, which was searched for properly and is clean:**

> **No cooking product composes a reusable, action-keyed clip library into the
> step-by-step flow of its recipes.** Checked product by product (Kitchen Stories,
> SideChef, Yummly Pro, Tasty, Serious Eats, ChefSteps, Rouxbe, America's Test
> Kitchen), by capability, by patent search, and through the academic literature.
> Nothing.

What exists everywhere is the *browsable technique library* the user visits
separately — Kitchen Stories has 23 such items, and tellingly files them under the
**recipe** content type (`/recipes/how-to-prepare-artichokes`). Techniques are
modelled as recipes, not as a reusable primitive. America's Test Kitchen sells
techniques as courses and books. Nobody has a composable action layer.

**Why nobody has done it, and why Matbakh can.** A keyed library needs a *closed
verb vocabulary* to key against. Every one of those products accepts free-text
steps, so there is no key to hang a clip on. Matbakh has spent three weeks
building exactly that key and has already settled it (`philosophy §15`). **The
lexicon is the asset that makes this possible, and it is the asset nobody else
has.**

**One independent corroboration that the vocabulary genuinely closes:**
**EPIC-KITCHENS-100**, the largest egocentric-vision dataset, annotates
unconstrained real-world kitchen footage with a closed vocabulary of exactly **97
verb classes**. Researchers with no knowledge of Matbakh, annotating real kitchens
from scratch, landed within 20% of 81. That is meaningful external validation that
kitchen actions close at this cardinality — and therefore that a library keyed to
them is finite and stays finite.

---

## 5. Consideration 1 — a full video per recipe, frames extracted

The intuition is strong: you are cooking the dish anyway, film it, take what you
need. It is also the direction the 19 August session was heading. Three separate
problems, in ascending order of severity.

### 5.1 The shutter conflict — you cannot get both from one pass

This is the technical objection and it is unavoidable.

Video looks right at a **180° shutter** — 1/48 s at 24 fps, 1/60 s at 30 fps —
because that motion blur is what the eye expects. A clean *still* of moving hands
needs roughly **1/250–1/500 s**, and a chart for actively moving subjects puts the
minimum at 1/250 s (rising as the subject fills more of the frame — which an
overhead rig on hands does).

Working the angle back:

| | 1/60 s | 1/250 s | 1/500 s |
|---|---|---|---|
| at 24 fps | 144° | 34.6° | 17.3° |
| at 30 fps | **180°** | **43.2°** | 21.6° |

At 30 fps, the shutter speed that merely *starts* to freeze a moving hand puts you
at **43°** — narrower than the 45° Kaminski used for explosions in *Saving Private
Ryan*. That is a documented, deliberate, violent stylistic effect. Your footage
would not be "slightly crisp"; it would stutter.

So: **shoot for video and your frames are smeared; shoot for frames and your video
is broken.** A practitioner who tested Panasonic's 6K PHOTO put it exactly:
shooting fast enough to freeze motion means "your video will simply look like a
bunch of hi-res still images stuck together." It also costs three stops of light.

If the video is *only ever* a frame source and never shown to anyone, this
dissolves — shoot at 1/500 s and let it stutter. But then you have built a
500-session video archive whose sole purpose is to yield stills, which invites the
obvious question in §5.4.

### 5.2 The frames are JPEGs, and asset-spec needs RAW discipline

Frame grabs come out as **JPEG only** — on Canon's R5 II, not available at all for
RAW movies or movies with a Custom Picture set; Panasonic's 6K PHOTO likewise
extracts JPEGs. Canon states it in their own documentation: *"saving a still image
from a single movie frame does not result in the same image quality as a normal
still image."*

A 4K frame carries roughly **1/20th the data per pixel** of a compressed RAW still
(~0.05 vs ~1.1 bytes/pixel). Every white-balance and exposure decision is baked in
at shoot time.

Set against `asset-spec.md`'s own requirement — *"consistent light and angle across
the catalogue… a lighting change reads to a cook as a doneness change"* — that is
the wrong way round. Consistency across 500 sessions shot over two years is a
**post-production** problem, and baked JPEGs are the format that gives you least
room to solve it.

There is a compounding problem: **Long-GOP compression spends the fewest bits on
the frames with the most motion.** The most indicative frame — the blade crossing
the steel, the pour mid-air — is precisely the frame the codec degraded most.
All-Intra fixes it and roughly doubles the bitrate.

### 5.3 Selection does not automate, and Matbakh already proved it

Each 30–45 minute session is **54,000–81,000 frames**. Picking 8–14 is a selection
ratio of roughly **1 in 4,000 to 1 in 10,000**. For scale: a full-day wedding is
2,000–3,000 exposures. One cook session holds twenty times more frames than an
entire wedding.

Automation does not rescue this:

- Keyframe selection by sharpness and scene-change scoring reports **42.5% error
  on static surveillance footage** — its worst category. A locked-off overhead
  cooking rig *is*, formally, static surveillance. There are no cuts to detect.
- Video summarisation is worse than it sounds: at CVPR 2019, **randomly generated
  summaries scored comparably to or better than published state of the art**, and
  on one benchmark human annotations scored *below* random.
- Cooking-specific step localisation — the closest academic analogue — reaches
  **37.0% mIoU** on YouCook2 and **12.9 mAP at IoU 0.7** on HT-Step. Nowhere near
  publishable without review. *(A useful aside from that dataset: YouCook2 videos
  average **7.7 segments**, independent confirmation that 6–10 pages is the right
  granularity.)*
- The two commercial "best frame" tools publish **no accuracy benchmarks at all**,
  and one caps input at 10 minutes.

**And Matbakh has already run this experiment.** The 19 August session found that
Laplacian-variance blur scoring rated a frame of a hand at **126** and the frame of
the blade crossing the steel at **56** — and the second was the one a cook needs.
The handover's own conclusion, *"blur scoring can only reject; selection is
human,"* is exactly what the published literature says. That was a finding on one
recipe. It generalises to 500.

There is also a practitioner account that is almost eerily on point. A food
photographer whose specific problem was *capturing both hands while making
something* tried an intervalometer and **abandoned it**, because "I would have to
sort through 100s of images making sure I got the action." She switched to a
**foot-pedal shutter release** — about $50–75 in parts — which autofocuses and
fires on a press, freeing both hands and eliminating culling entirely.

Her unmanageable pile was *hundreds*. The frame-extraction proposal is
**fifty-four thousand**, five hundred times over.

### 5.4 Cost, honestly

Take the most favourable possible reading: you are cooking anyway, the rig is
locked off, nothing is edited for publication, the footage exists only to yield
frames.

| Line | Per recipe |
|---|---|
| Marginal shoot time (setup, light check, retakes when a hand blocks the frame) | 45–90 min |
| Frame review, scrubbing a 30–45 min single-angle clip | 8–22 min |
| Export, crop, colour-correct 8–14 baked JPEGs | 16–28 min |
| **Marginal total** | **~1.5–2.5 h** |

Across 500 recipes: **750–1,250 hours ≈ 6–10 months of full-time work**, and that
is the floor. The one fully itemised solo-blogger breakdown available puts
photography and videography at **3.5 h plus 1.5 h photo editing plus 4.0 h video
editing = 9 h per recipe** — but that includes producing a publishable video, so
treat it as the ceiling. The honest range is **1.5–4 h per recipe, 750–2,000
hours, six months to eighteen months of full-time founder work.**

Against the ~7 h/recipe authoring estimate that already puts 500 recipes at **2–5
years**, this adds **20–55%** to the critical path — and R-06, founder capacity, is
already the binding constraint on everything.

Storage: 250–375 hours of footage is **11–17 TB** at 4K H.265, **27–40 TB**
All-Intra, and **99–149 TB** at ProRes 422 HQ. Archive cost is modest at the H.265
end (a few hundred dollars a year on Glacier Deep Archive, ~$90 of LTO-9 media)
and is not modest at the other. Offload and verify at benchmarked rates is another
**20–30 hours** of pipeline time for the H.265 case.

One operational trap worth naming: **Canon's R5 caps continuous 8K at 20 minutes**
without the $459 cooling grip. Cook sessions are 30–45.

**For scale on what per-recipe video production actually costs:** BuzzFeed Tasty
runs two studios with four filming stations each and **75 people** for roughly
**60 videos a month**, with the simplest recipes at a two-hour minimum and complex
ones taking up to a month. Pinch of Yum — the closest small-team analogue, two
people — produces **~16 videos a month** on two shoot days and three edit days a
week: about **1.25 person-days per finished recipe video**. At that rate, 500
recipes is **625 person-days**, or **two and a half years** of one person doing
nothing else.

---

## 6. Consideration 2 — shoot the activities once

Same tile. Different bill.

### 6.1 It is 47 clips, not 81

Only Class M needs motion (§2). The 34 Class S activities keep glyphs, and a
glyph is not a compromise for them — it is the *right* carrier, because
`philosophy §3` principle 2 is "show the verb," and for `rest`, `chill` and
`marinate` there is no verb to show. A four-second loop of resting dough is four
seconds of nothing happening, at a cost.

The eight cut glyphs stay glyphs too. A cut is a **result**, not a motion —
brunoise and dice differ by `cut_mm`, which is a number, not a movement.

### 6.2 Cost

| Line | Figure |
|---|---|
| Clips needed | **47** |
| Shooting, locked rig, ingredients prepped, no dish to finish — 12–20 usable loops/day *[derived]* | **3–4 days** |
| Post: trim, match first and last frame, two encodes, poster frame — 15–25 min each | **2–3 days** |
| **One-time total** | **~6–7 working days** |
| Marginal cost per recipe | **zero** |
| Marginal cost per language | **zero** — no words in a clip (`asset-spec.md`'s founding principle) |
| Payload | ~47 × 250 KB × 2 encodes ≈ **25 MB**, bundled, downloaded once, works offline |

Against consideration 1's **125–330 working days** and rising. The ratio is
roughly **20–50×**, and it is the wrong comparison anyway, because the two numbers
behave differently over time:

> **At recipe 500, consideration 1 still costs 1.5–4 hours. Consideration 2 costs
> nothing, and has cost nothing since recipe 1.**

One taxes every recipe you will ever write. The other is paid once. That, and not
the headline figure, is the argument.

The offline point is not incidental either. `asset-spec.md` budgets hero images
under 180 KB and step images under 140 KB explicitly because "a recipe opens over
an Egyptian mobile connection." A fixed 25 MB library downloads once and never
again. Per-recipe step video streams every time, forever.

### 6.3 The honest case against — three objections, one of which is real

**Objection 1: "A generic clip is not evidence this recipe was cooked."** True,
and the 18 Aug document was right to list trust as a genuine win for
recipe-specific imagery. But the trust claim is carried by the **hero and the
doneness photographs**, which stay recipe-specific under every option in this
document. It was never the tile's job. The trust argument survives; it just does
not live in the 44 px square.

**Objection 2: "It will read as stock footage."** It reads as stock if it *is*
stock — and the research found ~950,000 cooking clips on iStock alone, unkeyed and
unusable for this. It reads as *yours* if it is your hands, your knife, your board,
your light, shot to `asset-spec.md`. And there is an argument the other way that
is stronger than it first appears: **`asset-spec.md` §3.3 demands visual
consistency across the catalogue** — same height, same distance, same colour
temperature — *"measured, not remembered."* Forty-seven clips shot in one week
satisfy that by construction. **Five hundred cook sessions spread over two years
will drift, and no amount of discipline fully prevents it.** The fixed library is
not a consistency compromise; it is the only version that reliably meets the
spec's own standard.

**Objection 3, and this is the real one: the action is not always as generic as
the argument needs.** Folding a stiff batter and folding a loose one are different
gestures. Kneading bread dough is not kneading pasta dough. Where the ingredient
changes the motion, a generic loop is not merely unhelpful — it is **wrong**, and a
confidently wrong instruction is worse than a neutral glyph.

This is the objection that could sink the whole approach, so it is the one the
pilot must test, and §11 makes it the falsifiable criterion. My expectation is
that it bites on a small minority of verbs — `fold`, `knead`, `whisk`, `mix`,
`reduce` are the candidates — and that the answer for those is two or three
variants rather than 500, which is still the vocabulary scaling, just with a
slightly larger constant.

### 6.4 So: loops or stills? — loops, for Class M; glyphs for Class S; no stills

You asked me to argue this rather than assume it.

**Against stills, decisively.** A still of the action is the worst of both: it
carries the photograph's coherence penalty (the hand, the knife, the board, the
counter, the light — of which one thing is the instruction) *without* the motion
that justifies paying it. The 18 Aug document already made this point from Heiser
et al. — a frozen frame mid-chop cannot distinguish chop from slice from mince —
and §2 above shows that ambiguity is not an edge case: **58% of the vocabulary is
defined by motion.** A still-image library would spend most of the cost and buy
back the collisions it was meant to fix.

There is one place a still genuinely wins, and it is not the action: **the cut.**
`brunoise` versus `dice` is a static, geometric, purely visual distinction, and
eight cut stills at 44 px would carry it better than eight glyphs. That is worth
testing separately and cheaply.

**For loops, with a caveat about calm.** `philosophy §3` principle 5 is "the cook's
place is sacred," and four simultaneously looping tiles on one page is four
competing motions in the periphery of someone holding a knife. Motion is not free.

The design that resolves it, and my proposal: **loop once on page turn, then hold
the final frame; tap to replay.** The cook gets the motion at exactly the moment
they arrive at the page — which is when they need to know what their hands do —
and then the page goes still. The held final frame is a legible photograph. It
honours principle 3, "one mandatory gesture": the replay is optional and never
blocks. And it sits at the favourable end of the transient-information curve
rather than running a distracting perpetual loop.

---

## 7. A fourth carrier nobody has costed: the animated glyph

Between "static SVG" and "video clip" there is a third thing, and it is nearly
free.

Matbakh's icons are **stroke-based SVG on a 24×24 grid with
`stroke="currentColor"`** — a format that animates natively in the browser at
essentially no cost. `chop.svg` on disk is three paths: a board, a blade, and a
hilt. Animating the blade's descent is a few lines of CSS on an asset that already
exists.

| | Static glyph | **Animated glyph** | Video loop | Recipe frame |
|---|---|---|---|---|
| Production cost | done | **~1–2 h per glyph, no shoot** | 6–7 days once | 750–2,000 h |
| File size | ~250 B | **~400 B** | ~250 KB | ~140 KB |
| Works at **17 px** | **yes** | **yes** | no | no |
| Recolours by state (`currentColor`) | **yes** | **yes** | no | no |
| Language-neutral | yes | yes | yes | yes |
| Separates `chop` from `mince` | **no** | **probably** | yes | yes |
| Shows a real kitchen | no | no | yes | yes |

Two things make this more than a curiosity.

**It is the only candidate that can move at 17 px.** A video cannot serve the arc.
An animated glyph can — which raises a question worth asking: could a *moving* arc
thumbnail carry position better than a static one? `philosophy §4.4` calls the map
the thing no other recipe app offers. Untested, cheap to test.

**It preserves the state-colour system.** `asset-spec.md` requires
`stroke="currentColor"` precisely so the reader can tint an icon ink, terracotta,
green for a running timer, or red for danger. **A video cannot be recoloured by
state.** That is a real functional loss in the tile, and it is the strongest
argument for keeping glyphs in the tile even after a clip library exists —
possibly as a layered treatment rather than a replacement.

The accompanying prototype implements this for real on the actual `chop.svg`, so
it can be judged rather than imagined.

---

## 8. Consideration 3 — prose on request is already decided; it needs building, not deciding

`philosophy §3` carries this as one of two structural commitments:

> **Two views, one truth.** The visual view and the Arabic/English prose view are
> two renderings of the same structured recipe object — never authored separately.
> This turns localisation into a data problem, not an editorial one, and prevents
> drift across 500 recipes × 2 languages.

So the answer to "should the recipe be available in prose?" is **yes, and it was
settled on 1 August.** The open question is narrower and more consequential:
**generated, or authored?**

**Generated, at build time, from the structured object.** Reasons, in order:

1. **Authoring it is a second content project.** `philosophy §15` already refuses
   the equivalent for dialects, on the grounds that "dialectising ~5,000 prose
   strings is a second content project." A prose view authored per recipe per
   locale is that same project, twice over. At even one hour per recipe it is
   **500 hours**, on top of everything in §5.4.
2. **Authored prose drifts.** Two hand-written descriptions of the same step will
   diverge the first time a quantity changes and only one is updated. Generation
   makes drift structurally impossible — which is the commitment's own stated
   purpose.
3. **It is checkable.** Generated at build time, prose falls under
   `matbakh.py check` like everything else, and joins the generated-numbers
   discipline established on 20 August. Hand-typed prose does not.
4. **The marginal cost is zero**, in both locales and in every dialect the lexicon
   already covers.

**And one thing to rule out explicitly: do not generate the prose at runtime with
a language model.** In a product whose entire promise is *500 individually
test-cooked, founder-authored recipes*, shipping non-deterministic text that no
one wrote and no one cooked would spend precisely the asset the product is built
on — the same argument the 18 Aug document made against generated imagery, and it
applies with more force to words, because words make claims. Build-time templating
over the lexicon is deterministic, inspectable, diffable and free.

**What stays authored** is what the schema already treats as authored: the
irreducible judgement. Doneness cues, the NEVER note, *why this version*. Those
are the ~5,000 strings §15 refers to, and they are the ones worth a founder's
hands.

**The one real risk is register**, and it is testable today at zero cost:
generated Arabic assembled from lexicon verbs and quantities may read
mechanically in a way generated English does not — Arabic verb forms, agreement
and the construct state are less forgiving of templating. **You have two authored
recipes right now.** Generate both prose views, read the Arabic aloud, and you
will know. That is an afternoon, not a project, and it should happen before any
camera is bought.

---

## 9. The options, costed

| | What the 44px tile shows | One-time | Per recipe | At 500 recipes |
|---|---|---|---|---|
| **A** Icons only *(as designed)* | static glyph | C-05 only | 0 | **0** |
| **A+** Icons, animated | animated glyph | C-05 + ~1–2 h × 47 | 0 | **~60–100 h once** |
| **B** Photographs replace icons | — | — | — | **Not viable** — breaks the 17 px arc |
| **C** Icon + doneness photo *(18 Aug recommendation)* | static glyph | C-05 | ~4–6 photos | **~250–400 h** |
| **D** C + process photo where it earns it | glyph + occasional photo | C-05 | +10–20% | ~300–500 h |
| **1** Video per recipe, frames pulled | recipe-specific frame | rig | **1.5–4 h** | **750–2,000 h** |
| **2** Activity clip library | reusable action loop | **~6–7 days** | 0 | **~50–60 h once** |
| **E** ← **the recommendation** | loop (M) / glyph (S) | ~6–7 days + C-05 | ~4–6 doneness photos | **~300–450 h** |

Option E's per-recipe number is *lower* than option C's, because the tile stops
needing a photograph at all and the doneness count drops from "one per page" to
"one per genuine decision point" — molokhia used doneness on 6 of 8 pages, and
several of those were carrying the tile's job rather than their own.

---

## 10. Recommendation

**Shoot the vocabulary, not the catalogue.**

Concretely — option **E**:

1. **Keep the glyphs, and finish C-05.** They own the 17 px arc, which nothing
   else can serve, and they remain the correct carrier for the 34 state-defined
   activities. This work is owed under every option; it is not a concession.
2. **Shoot ~47 short silent loops**, one per motion-defined activity, keyed to
   `activities.yaml`. Once. Loop on page turn, hold the final frame, tap to
   replay. No text, no captions, no face — `asset-spec.md` §3 already specifies
   the format down to the encode.
3. **Per recipe, capture only the doneness states** — 4–6, not 8–14. These are
   irreducibly specific and they carry the trust claim.
4. **Capture them with a foot pedal, not by extracting frames.** ~$50–75 in
   parts. RAW instead of baked JPEG, correct shutter without breaking the video,
   both hands free, and no culling — the failure mode that killed it for the one
   practitioner documented trying the automated route.
5. **Generate the prose at build time.** Test the Arabic register this week on the
   two recipes you already have.
6. **Test the animated glyph** — it is nearly free, it is the only moving carrier
   that survives 17 px, and it is the only one that keeps the state-colour system.

**What this buys.** The action layer stops scaling with the catalogue. Recipe 500
costs what recipe 1 costs. Two of the three glyph collisions dissolve without a
lexicon change. Adding a language stays a data problem. The library ships offline
in 25 MB. And the consistency requirement in `asset-spec.md` §3.3 is met by
construction rather than by two years of remembered discipline.

**What it costs.** About six or seven working days, once, plus the C-05 work you
already owe — against six to eighteen months for consideration 1.

**The line to hold on to:** the lexicon exists so that adding a language costs one
pass over `activities.yaml` instead of 500 recipes' worth of vocabulary. An
activity clip library is the identical argument applied one level further out —
`asset-spec.md` already states the principle in its first sentence: *"An asset
that carries no words is made once."* **Consideration 2 is not a new idea. It is
the idea Matbakh is already built on, extended to pictures.**

---

## 11. What the pilot should measure — and the elegant part

**The pilot is already the library shoot.** Recipe 1 exercised 14 activities. The
fifteen pilot recipes are designed for coverage and will exercise most of the
vocabulary between them. You are going to perform those actions anyway, on camera
or not.

So: **shoot the loop for each Class M activity the first time a pilot recipe calls
for it.** Not all 47 — only the ones the pilot reaches, which is the whole point
of a coverage-driven pilot. By recipe 15 you will have most of the library, at a
marginal cost of the seconds it takes to do the action once more cleanly.

This preserves the pilot's own discipline exactly: *measure first, decide once.*
It tests the model at a fraction of its cost, and if the model fails you have lost
days, not months.

Five things to record while cooking:

1. **A three-way column on the tracker, per tile** — replacing the 18 Aug
   document's two-way version: *glyph sufficient* / *needed motion* / *needed this
   specific dish*. Fifteen recipes ≈ 150 judgements, which remains the only
   dataset on this question that will ever exist.
2. **Flag every tile where the ingredient changed the gesture.** This is §6.3's
   real objection and the criterion that decides the whole approach.
3. **Test `season` / `to_taste` deliberately.** Both appear in molokhia. Neither
   imagery nor motion can separate them; confirm that in practice and fix it in
   the lexicon or the layout.
4. **Shoot one failure frame** — one shade past on the takliya. Still the single
   highest-value image in the product, still nobody has it, still costs one extra
   pan of garlic.
5. **Check my Class M / Class S split against reality** and correct it. It is
   judgement, and §2 says so.

**Decision rules, applied only after the batch** — the same shape the lexicon
review already uses:

- **The falsifiable one:** if **≥3 recipes** show a generic loop misleading
  because the ingredient changed the gesture, the action layer is not generic and
  consideration 1 comes back onto the table. This is the test that can kill the
  recommendation, and it should be allowed to.
- If **≥90%** of tiles read as *glyph sufficient*, do not shoot at all — take
  option A+, animate the glyphs, and spend the money on doneness photography.
- If a Class S activity repeatedly wanted motion, move it to Class M. One recipe
  is an anecdote; three is a finding.

---

## 12. What would change this, and what is genuinely uncertain

**Marked honestly, because three of the last document's confident statements
turned out to be wrong.**

- **The 47/34 split is my judgement, not a measurement.** Every number in §2 is
  generated from the file on disk; the *classification* is argued. Contest it.
- **The 12–20 loops/day shooting rate is derived, not observed.** No one publishes
  a rate for shooting short action loops. The industrial worst case — DELISH
  KITCHEN at 1.5 finished assets per stylist per day — is for full recipe
  micro-clips with a dish to cook, which is a much heavier unit. If my rate is off
  by 3×, consideration 2 costs three weeks instead of one, and the conclusion does
  not move.
- **d = 1.06 is verified but is not a kitchen finding.** Höffler & Leutner is
  instructional-settings research from 2007. Nobody has measured any of this under
  kitchen conditions, and the 18 Aug document's §1.8 gap is still open.
- **Nobody in cooking has done this**, which cuts both ways. It is a real
  opportunity and it is also unproven in this domain. The mitigation is that the
  pilot tests it for days rather than months.
- **The register risk on generated Arabic is untested** and could be material. It
  is also testable this week for nothing.
- **Motion in cook mode may simply annoy people.** The loop-once-then-hold
  proposal in §6.4 is a design argument, not a finding. The prototype exists so it
  can be judged on a real phone rather than accepted on paper.

---

## Sources

**Cognitive evidence**
Höffler & Leutner, *Learning and Instruction* 17(6), 722–738 (2007) — effect
sizes verified against the [ERIC record EJ780451](https://eric.ed.gov/?id=EJ780451) ·
Wong, Leahy, Marcus & Sweller, *Learning and Instruction* (2012), transient
information effect, [ERIC EJ978021](https://eric.ed.gov/?id=EJ978021) · Heiser,
Phan, Agrawala, Tversky & Hanrahan, AVI'04 · Mayer, *Multimedia Instruction*
(2014) · Skulmowski & Rey (2021) · Castro-Alonso et al. and Ayres et al. on the
human-movement effect (abstracts only; paywalled)

**Reusable-library precedent**
[Fitbod exercise library](https://fitbod.me/about-fitbod-exercises/) and
[algorithm](https://fitbod.me/blog/fitbod-algorithm/) ·
[Hevy](https://help.hevyapp.com/hc/en-us/articles/35688251991575-Hevy-Exercise-Library-400-Exercises-and-Custom-Exercises) ·
[ExRx.net licensing](https://exrx.net/Store/Other/Licensing) ·
[Physiotec / Wibbi](https://wibbi.com/) ·
[Medbridge](https://www.medbridge.com/care/exercises) ·
[Physitrack](https://www.physitrack.com/exercise-library) ·
[Spreadthesign](https://en.wikipedia.org/wiki/Spreadthesign) ·
[Gym Animations](https://gym-animations.com/) ·
[ExerciseDB](https://exercisedb.gumroad.com/l/exercisedb) ·
[EPIC-KITCHENS-100 annotations](https://github.com/epic-kitchens/epic-kitchens-100-annotations/blob/master/README.md) ·
[Kitchen Stories how-tos](https://www.kitchenstories.com/en/how-tos/basics) ·
[SideChef](https://www.sidechef.com/recipes/) ·
[America's Test Kitchen 100 Techniques](https://www.amazon.com/100-Techniques-Master-Lifetime-Cooking/dp/1945256931)

**Frame extraction, shutter and selection**
[Canon on 4K Frame Grab quality](https://snapshot.asia.canon/article/first-hand-review-frame-grab-and-4k-movie-on-the-eos-1d-x-mark-ii) ·
[Canon R5 II frame-grab constraints](https://cam.start.canon/en/C017/manual/html/UG-05_Playback_0080.html) ·
[Canon EOS R5 specifications](https://www.canon.co.uk/cameras/eos-r5/specifications/) ·
[Panasonic 6K/4K PHOTO](https://www.panasonic.com/sg/consumer/lumix/brand/technologies/lumix-6k-4k-photo.html) ·
[Matthew Starling 6K Photo test](https://www.matthewstarling.co.uk/panasonic-6kphoto/) ·
[Cinema Shock on the 45° shutter](https://cinemashock.org/2012/07/30/45-degree-shutter-in-saving-private-ryan/) ·
[Giggster freeze-motion shutter chart](https://giggster.com/guide/photography/shutter-speed-freeze-motion/) ·
[Canon on IPB / Long-GOP](https://snapshot.asia.canon/en/article/videography-faq-what-is-ipblong-gop-and-all-iintra-frame) ·
[Digital Camera World, Long GOP vs All-Intra](https://www.digitalcameraworld.com/features/long-gop-vs-all-intra-what-are-they-and-whats-the-difference) ·
[Adobe Stock on frame grabs as photos](https://community.adobe.com/t5/stock-contributors-discussions/can-i-upload-stills-from-videos-as-photos-to-the-adobe-stock-for-sale/m-p/14664015) ·
[Otani et al., CVPR 2019, "Rethinking the Evaluation of Video Summaries"](https://openaccess.thecvf.com/content_CVPR_2019/papers/Otani_Rethinking_the_Evaluation_of_Video_Summaries_CVPR_2019_paper.pdf) ·
[keyframe-policy error rates, arXiv 2506.00667](https://arxiv.org/html/2506.00667v1) ·
[YouCook2 / ProcNets](https://cdn.aaai.org/ojs/12342/12342-13-15870-1-2-20201228.pdf) ·
[HT-Step, NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/file/9d58d85bfc041b4f901c62ba37a3f322-Paper-Datasets_and_Benchmarks.pdf) ·
[Y.M.Cinema on R5 8K recording limits](https://ymcinema.com/2020/07/15/canon-updates-eos-r5-recording-times-specifications-8k-for-20-minutes-maximum/)

**Production cost and throughput**
[TODAY, inside BuzzFeed Tasty's kitchen](https://www.today.com/food/how-do-they-make-tasty-videos-check-out-buzzfeed-s-t159042) ·
[Digiday on Tasty](https://digiday.com/media/just-15-months-old-tasty-driving-buzzfeed-video-facebook/) and
[on publishers' test kitchens](https://digiday.com/media/a-new-way-of-working-publishers-test-kitchens-return-to-studio-with-new-safety-procedures-in-the-mix/) ·
[Food Blogger Pro ep. 139, Pinch of Yum](https://www.foodbloggerpro.com/podcast/recipe-video-questions/) ·
[Imagelicious, itemised solo recipe cost](https://www.imagelicious.com/blog/truth-about-food-bloggers) ·
[Kristin Donnelly on cookbook shoot costs](https://www.kristindonnelly.com/journal/2020/12/30/how-much-do-cookbook-photo-shoots-cost/) ·
[The Post Flow storage calculator](https://thepostflow.com/filmmaker-resources/video-storage-calculator/) ·
[Agave IS on LTO archive cost](https://agaveis.com/blog/lto-tape-storage-cheapest-data-retention) ·
[Newsshooter offload benchmark](https://www.newsshooter.com/2019/10/28/what-is-the-fastest-offload-software/) ·
[echo echo studio, foot-pedal shutter release](https://echoechostudio.com/blogs/tutorials/learn-how-to-control-your-camera-with-a-foot-pedal) ·
[Photography Life on pre-release capture](https://photographylife.com/pre-release-capture-explained)

**Matbakh's own**
`design/philosophy.md` §3, §4.4, §5.1, §5.2, §15, §16.5, §16.6 ·
`design/asset-spec.md` · `design/step-imagery-research.md` (18 Aug) ·
`content/lexicon/activities.yaml` — 81 activities, 78 distinct glyphs, three
shared-glyph pairs, all counted from the file rather than quoted ·
`design/icons/` — 20 placeholder SVGs plus 8 cut glyphs ·
`claude/HANDOVER.md` (20 Aug) for the blur-scoring finding
