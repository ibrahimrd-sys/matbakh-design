# Asset specification

Icons, photographs and technique clips for Matbakh. Every figure below is
measured from the prototypes rather than chosen in the abstract — where a size
looks odd, it is because that is what the screen actually renders.

This is the document to hand a photographer or an illustrator.

---

## The principle that governs all three

**An asset that carries no words is made once. An asset that carries words is
made again for every language.**

That is the same argument as the lexicon, applied to pictures. A clip with
"medium heat" burned into the corner is not one clip, it is one clip per
language you ever ship — and unlike a line of YAML, re-rendering it means
going back to the edit.

So: no text in photographs, no captions in clips, no lettering in icons.
Anything that must be said is said in the lexicon, over the top, in the reader.

The second principle follows from the interface being near-wordless. **Visual
consistency is structural, not decorative.** A cook reading a doneness photo is
comparing it to the pan in front of them. If the light, angle and distance shift
between recipes, the comparison stops working and they fall back to reading —
which is the thing the design is built to avoid. This is why a permanent studio
setup matters more than a good camera.

---

## 1. Icons

### Where they appear, and at what size

| Context | Rendered size | Notes |
|---|---|---|
| Cook mode tile | **44 × 44 px** | The primary size. Also the minimum touch target. |
| Tablet tile | 62 × 62 px | Largest use. |
| Recipe screen inline | 32 / 24 / 22 px | Chrome and list rows. |
| Arc thumbnail | **~17 px** | 40 × 38 box at `scale(.42)`. The hardest case. |

An icon has to survive a 3.6× range, from 17px to 62px. **The 17px arc thumbnail
is the binding constraint** — an icon that is legible there is legible
everywhere, and the reverse is not true.

### Format

- **SVG**, one file per glyph key, filename exactly the key: `chop.svg`,
  `simmer_covered.svg`. The lexicon's `glyph:` field is the filename.
- **24 × 24 viewBox**, stroke-based, **2px stroke**, round caps and joins.
  This is the Tabler geometry, and the production set is Tabler Icons (MIT).
- **`stroke="currentColor"`, no `fill`.** The reader colours icons by state —
  ink for normal, terracotta for accent, green for a running timer, red for
  danger. A hardcoded colour breaks all four.
- **No `width` or `height` attributes** on the root `<svg>`; the reader sizes
  it. Leave `viewBox` alone.
- Strip metadata, comments and `<title>`. These ship 500 times over.

### Drawing rules

- **Three strokes or fewer** where possible. At 17px, a fourth becomes noise.
- **No detail below 2px** at the 24 grid. It disappears in the arc.
- **Silhouette must differ** from every neighbouring icon. Test by squinting at
  the arc strip: if two steps look alike at a glance, the cook loses their place.
- **No lettering, no numerals.** Both need translating; numerals also need
  Eastern Arabic forms.
- Draw the **action**, not the ingredient. `crush` is a pressed blade, not a
  garlic clove — the ingredient supplies its own glyph separately.

### The association with the lexicon

Resolution order when the reader draws a tile:

```
tile.glyph          explicit override on that tile
  ↓ else
activity.glyph      from lexicon/activities.yaml
  ↓ else
ingredient.glyph    from ref/ingredients.yaml
```

So an activity's glyph is a default, not a mandate. `add` carries a generic
plus; when a recipe adds bay leaves, the leaf comes from the ingredient. This is
why `drop_in` was merged away — it was `add` wearing an ingredient's icon.

Two rules follow:

- **Every activity key needs a glyph.** `matbakh.py lexicon` errors without one,
  because a tile that cannot be drawn is a blank square.
- **Every ingredient wants one**, but generic is fine. `jar` for pantry staples
  is honest; inventing 179 distinct icons is not worth it.

### Delivery

```
design/icons/
  chop.svg  crush.svg  fry.svg  sear.svg  …
  LICENSE            ← Tabler's MIT text, retained as the licence requires
```

Around 60 activity icons and perhaps 25 ingredient-category icons. Not 179 —
ingredients share by category.

---

## 2. Photographs

### Where they appear, and at what size

| Use | Rendered | Fit | Aspect |
|---|---|---|---|
| **Hero** (recipe screen) | 393 × 318 | `contain` | **5:4 landscape** |
| **Step / doneness** (phone) | 361 × 176 | `cover` | wide crop, 2.05:1 |
| **Step / doneness** (tablet) | fills the tile | `cover` | — |
| **Shorts poster** | 84 × 64 | `cover` | 1.31:1 |
| **Arc thumbnail** | ~54 × 42 | `cover` | 1.29:1 |
| **Resume card** | 460 wide | `cover` | — |

### Shoot the hero at 5:4 landscape

The hero band is 393 × 318, a ratio of **1.236**. Five-by-four is 1.25. Shot at
5:4, the photograph fills the band almost exactly — under two pixels of margin —
while `contain` still guarantees nothing is cropped. The mismatch is
4.5 px, split top and bottom.

This matters because `contain` was chosen deliberately: cropping was cutting the
top off the dish. Shooting to the band's ratio is what makes "show the whole
photo" and "fill the screen" stop fighting each other. **Any other ratio
letterboxes against `#E4DACA`**, which is not wrong, just weaker.

### Step photos are cropped, so frame for it

Step photos use `cover` into a **2.05:1** letterbox on the phone. Whatever you
shoot, the top and bottom go.

- Shoot **4:3 or 3:2 landscape**, and keep the subject inside the **middle 65%
  vertically**. Anything above or below that is padding.
- Never place the doneness cue near a frame edge. The colour of a takliya's
  edge, the surface of a stock — put it dead centre.

### Doneness photographs specifically

These carry more weight than the hero. A cook is holding the tablet next to the
pan, deciding whether to stop.

- **Match the schema's claim.** `doneness.en` for the takliya says *"Straw-gold
  at the edges. One shade past this is bitter."* The photograph has to show
  straw-gold at the edges — not one shade past.
- **Shoot the moment, not the ideal.** The most useful frames are the ones
  taken at the exact instant the words describe, which usually means shooting a
  sequence and choosing, not staging afterwards.
- **Consider shooting the failure too.** One shade past bitter is the single
  most useful image in the whole recipe, and no cookbook has it.
- **Consistent light and angle across the catalogue.** Same height, same
  distance, same temperature. This is the structural-consistency point: a cook
  compares your photo to their pan, and a lighting change reads as a doneness
  change.

### Files

- **Format: WebP**, quality 82. AVIF is smaller but the encode is slower and
  the gain does not repay it at these sizes. Keep JPEG only as an archive
  master.
- **Export at 3×** the rendered size, for a phone at DPR 3:

  | Use | Export |
  |---|---|
  | Hero | **1600 × 1280** (5:4, covers tablet too) |
  | Step / doneness | **1400 × 1050** (4:3, cropped by the reader) |
  | Shorts poster | 640 × 488 |

- **sRGB**, embedded profile. Strip EXIF except copyright.
- **Filenames** match what the recipe refers to, lowercase kebab-case:
  `molokhia-takliya-done.webp`. No spaces — `build.py` treats a space in a
  filename as a hard error, for the URL reasons discovered the hard way.
- **Budget:** hero under 180 KB, step under 140 KB. A recipe carries eight to
  ten images and opens over an Egyptian mobile connection.

### Volume

Roughly ten images per recipe — one hero, one per step, a few posters. Across
500 recipes that is **about 5,000 photographs**, which is the arithmetic that
makes a day-rate studio the wrong model and a permanent setup the right one.

---

## 3. Technique clips

### How the reader plays them

```html
<video autoplay loop muted playsinline object-fit:cover>
```

Four constraints fall straight out of that line:

- **`muted`** — there is no audio, ever. If the clip only works with narration,
  it does not work.
- **`loop`** — it repeats with no gap. First and last frame must match, or the
  loop jumps.
- **`autoplay`** — it starts with no press, so it must make sense from frame one.
  No title cards, no slow build.
- **`cover`** — it gets cropped like a step photo. Same rule: subject in the
  middle 65%.

### Length and content

The four shorts in the prototype run 18 to 31 seconds. That is the right range.

- **One technique per clip.** *Knife work, keeping the edge.* Not "prep".
- **Hands and the pan only.** No face, no kitchen, no brand. A face dates the
  clip and ties it to one presenter; a plain frame lasts.
- **No text, no captions, no arrows.** Same reason as everything else — the
  moment lettering appears, the clip belongs to one language. What needs saying
  is in `shorts[].title`, which the lexicon system already translates.
- **Shoot at the same angle as the step photograph** it accompanies. The cook
  moves between a still and a moving version of the same thing; a change of
  viewpoint costs them a second of re-orientation.

### Files

- **Two encodes**, same basename:
  - `clip-knife.webm` — VP9, CRF 32
  - `clip-knife.mp4` — H.264 High, CRF 23, `+faststart`
  WebM is smaller; MP4 is the one that reliably plays on older iOS. Ship both.
- **1080 × 810** (4:3) or **1280 × 720**, **30 fps**, no audio track at all —
  strip it rather than muting it, it is wasted bytes.
- **Under 3 MB.** These autoplay; a cook on mobile data should not notice.
- **A poster frame per clip**, same basename, `.webp`. A clip with no `clip:`
  field renders as TO BE SHOT and the validator says so, so the poster can land
  first and the clip follow.

---

## Checklist before a shoot

- [ ] Hero framed 5:4, subject centred
- [ ] Step shots 4:3, doneness cue in the middle 65%
- [ ] The failure state photographed as well as the success, where it teaches
- [ ] Light, height and distance identical to the last session — measured,
      not remembered
- [ ] No text in any frame, no hands wearing anything identifying
- [ ] Clips silent, looping cleanly, one technique each
- [ ] Filenames lowercase, hyphenated, matching the recipe YAML
- [ ] `python3 build.py` run afterwards — it names every asset a prototype
      expects and cannot find
