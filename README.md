# Matbakh — application design

*Repository landing page. Refreshed 26 August 2026.*

Hi-fi prototypes and the design system behind them. This folder is the single
place the design lives; everything a reviewer needs is reachable from
`index.html`.

**One rule:** `index.html` is generated. Edit `manifest.yaml`, run `build.py`.
If you hand-edit `index.html` your changes are lost on the next build.

> **`DIRECTORY.md` says what every file here is** — canonical, generated,
> fixture, draft, working sheet or placeholder — and which ones you can trust.
> Read it before citing anything in this folder. This file is the loop;
> that one is the contents.

> **On the name.** READMEs in this project carry something indicative —
> `ToolsReadme.md`, `VaultReadme.md`, `ArchiveReadme.md`. This one and
> `content/recipes/README.md` are the two deliberate exceptions: GitHub renders
> only a file called `README.md` as the landing page, and the recipes one is
> whitelisted by name in all four vault guards. `DIRECTORY.md §11` has the
> reasoning.

---

## Structure

```
matbakh-design/
├── manifest.yaml          ← you edit this when a screen changes
├── build.py               ← preflight checks + generates index.html
├── publish.sh             ← check, build, commit, push in one command
├── index.html             ← GENERATED. entry point for reviewers
├── DIRECTORY.md           ← what every file is, and whether to trust it
│
├── prototypes/            stable kebab-case names → shareable URLs
│   ├── bolognese-iphone.html      the lead. TEMPORARY by agreement
│   ├── app-iphone.html            molokhia, the earlier linked flow
│   ├── recipe-screen-iphone.html
│   ├── cook-mode-tablet.html      cook-mode-tablet-white.html
│   ├── cook-mode-iphone.html      cook-mode-iphone-white.html
│   ├── storyboard-bench-sheet.html   tile-comparison.html   working sheets
│   └── support.js         shared runtime, must sit beside the prototypes
│
├── design/
│   ├── philosophy.md          CANON — settled decisions and open questions
│   ├── authoring-standard.md  CANON — how to enter a recipe
│   ├── asset-spec.md          CANON — photography craft
│   ├── tokens.css             CANON — the palette and type scale
│   ├── step-imagery-*.md      CANON — the research and the decision
│   ├── storyboard-companion.md  (+ .pdf, generated from it)
│   ├── tag-proposal.md · discovery-draft.md · availability-draft.md   DRAFTS
│   ├── icons/  icons/cuts/    PLACEHOLDER glyphs — not the icon set
│   └── source/                Claude Design build artefacts, not shipped
│
├── content/               schema, validator, lexicon (catalogue gitignored)
│   ├── matbakh.py             check · build · lexicon · status · vault
│   ├── lexicon/               activities.yaml · chrome.yaml
│   ├── recipes/               _template.yaml + one schema FIXTURE
│   └── ref/                   the 12-entry fallback sample
│
├── planner/               the planning algorithm + 17 tests
├── tools/                 four single-file browser authoring editors
├── assets/                photos, clips, media.js
│
├── CHANGELOG.md           one entry per publish
├── ATTRIBUTIONS.md        CC credits — a licence condition, and still blank
├── .gitignore  .githooks/  scan.sh  setup-guards.sh    the vault guards
└── .nojekyll              stops GitHub Pages mangling the files
```

### What is deliberately **not** here

The financial model, the strategy documents and the recipe catalogue. This repo
is public so that GitHub Pages can serve it on the free plan, and all three would
be world-readable. They live in `matbakh-private/`, beside this folder and never
inside it — see its `DIRECTORY.md`. Three independent guards keep them out:
`.gitignore`, `.githooks/pre-commit`, and `scan.sh`. Only the schema, the
template, one fixture recipe and a 12-entry ingredient sample are tracked here,
so the data model stays reviewable without publishing the product.

---

## The update loop

Whatever changed, the loop is the same three steps.

**1. Drop the new or revised file in.** A revised screen replaces the file in
`prototypes/`. A new screen gets a kebab-case name — no spaces, ever, or the
shared URL fills with `%20` and `publish.sh` refuses the commit.

**2. Tell the manifest.** For a new screen, add four lines to the relevant
section:

```yaml
      - file: prototypes/discovery-iphone.html
        title: Discovery — iPhone
        blurb: What a cook sees before they have chosen anything.
        tags: [IPHONE, NEW]
```

Then bump `release:` to today's date and add a `CHANGELOG.md` entry. Both are
enforced — `publish.sh` stops if the release stamp is not today, and `build.py`
warns if a prototype is newer than the newest changelog entry.

**3. Publish.**

```bash
./publish.sh "discovery screen, first pass"
```

That runs preflight, regenerates `index.html`, blocks anything that should not
be public, commits and pushes. Pages rebuilds in about a minute.

To look before you leap: `python3 build.py --check` checks and writes nothing.

**And after every publish**, refresh the tracker's measured half:

```bash
cd content && python3 matbakh.py status --write ../../matbakh-private/02-strategy/matbakh_pm_log.md
```

Preflight will remind you if you forget, which is the whole point of it.

### What preflight catches

| Check | Why it exists |
|---|---|
| Manifest points at a missing file | A dead link in the index is the most common review-day failure |
| Prototype on disk not in the manifest | An orphan screen nobody can find |
| Space in a filename | `%20` in every URL you share |
| Referenced asset missing | The screen renders blank with no visible error |
| `support.js` not beside the prototypes | Same, and harder to diagnose |
| `noindex` missing while `public: false` | Stops Google indexing the design before launch |
| Colour not declared in `tokens.css` | Makes palette drift visible instead of silent |
| Prototype newer than the changelog | Stops the changelog quietly falling behind |
| PM log older than the repo | Stops the tracker quietly falling behind |
| `.gitignore` missing its guards | The catalogue or the financials going public |
| Recipe data invalid | Runs `content/matbakh.py check` as part of the same pass |

Errors block the build. Warnings do not — they are the standing backlog.

---

## After a fresh clone

```bash
git fetch                     # before diagnosing that anything is missing
bash setup-guards.sh          # restores +x, installs the pre-commit hook
./scan.sh                     # confirm nothing sensitive is present
python3 build.py --check
```

`setup-guards.sh` is not optional: git does not carry the executable bit or the
hooks path, so a fresh clone has no pre-commit guard until you run it. The hook
uses `#!/bin/bash` rather than `#!/usr/bin/env bash` because the latter cannot
resolve under GitHub Desktop's restricted PATH.

Without the vault beside this folder, `matbakh.py` validates against the
12-entry sample instead of the real reference — **and says so on every run.**
Read that line before drawing a conclusion from the output.

### Pages

The site is served from `main`, folder `/ (root)`. Review URL:
`https://ibrahimrd-sys.github.io/matbakh-design/`. Deep links append directly:

```
https://ibrahimrd-sys.github.io/matbakh-design/prototypes/bolognese-iphone.html#cook/4
```

`public: false` in the manifest keeps the `noindex` tag on every prototype, which
is what stops a half-finished design becoming the first Matbakh result on Google.
**Leave it false until launch.**

---

## Before this goes to anyone outside

- [ ] **Fill in `ATTRIBUTIONS.md`.** Seven blank rows, and the repo is *already*
      public — crediting the CC photography is a licence condition being missed
      now, not a pre-launch chore.
- [ ] **Replace the placeholder icons.** `design/icons/` is 28 geometric
      stand-ins that render at full fidelity, so a reviewer reads them as the
      icon set. Keep the Tabler MIT licence text at `design/icons/LICENSE` when
      the real set lands.
- [ ] **Decide the bolognese prototype.** It is tagged `TEMPORARY` and exists to
      settle one question. Say yes or no, write it into `philosophy.md`, take it
      out.
- [ ] Consolidate the undeclared colours and retire the two deprecated tokens
      (`#C0562F`, `#FAF6EE`) that preflight still reports.
- [ ] Leave `public: false` until launch.

Done, and no longer on this list: the real `philosophy.md` is in place, `assets/`
is populated, the repo is published, and the vault guards are installed and
audited.

## Notes for reviewers

Tap a tile to mark it done; Back / Next to turn pages; ⓘ for the doneness cue;
the gear for language and numerals; MAP for the whole arc. Servings 2 / 4 / 8
rescale the steps and the basket together, and an edited basket quantity stops
following the presets. Timers ring an audible alarm with a Silence / +2′ banner —
keep the screen awake for it to sound.

**Nothing should scroll** in cook mode. If something does, that is a bug worth
reporting.

Opened on a phone or tablet the prototype drops the mockup bezel and fills the
real screen. On a laptop it stays in the frame, with a **PREVIEW AS REAL DEVICE**
toggle underneath. Force either way with `?device=1` or `?device=0`, which
combines with the step links.

The standing caveats, because reviewers calibrate on them: photography and the
technique clips are Wikimedia Commons stand-ins, **no cook video has been shot**,
so the `FRAME TO PULL` and `TO BE SHOT` placeholders are the honest state; icon
glyphs are geometric placeholders; prices are illustrative and the cost row
deliberately shows a dash rather than an invented number.
