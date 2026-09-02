# DIRECTORY — matbakh-design

**What every file in this repository is, and which of them you can trust.**
Written 26 August 2026. Companion to `README.md`, which explains the *loop*;
this explains the *contents*.

The vault, `matbakh-private/`, has its own `DIRECTORY.md` beside this one. It is
not described here — this file is in a public repository.

---

## 0. The four-line version

| Question | Answer |
|---|---|
| What do I edit when a screen changes? | `manifest.yaml`, then run `build.py`. Never `index.html`. |
| Where are the settled design decisions? | `design/philosophy.md`. |
| How do I author a recipe? | `design/authoring-standard.md`, using `tools/recipe-editor.html`. |
| Where is the project tracker? | Not here. `matbakh-private/02-strategy/matbakh_pm_log.md`. |

---

## 1. Status vocabulary

Every row below carries one of these. It is the whole point of this document.

| Mark | Means |
|---|---|
| **CANON** | The authority on its subject. Cite it, edit it, trust it. |
| **GENERATED** | Written by a tool. Hand edits are lost. Never edit directly. |
| **FIXTURE** | Exists so the tooling has something to chew on. Not real content. |
| **DRAFT** | Real work, not yet decided. Do not cite as settled. |
| **WORKING** | A sheet made to answer one question. Disposable once answered. |
| **PLACEHOLDER** | Stands in for something not yet made. Reads finished; is not. |
| **GUARD** | Part of the safety net that keeps the vault out of git. Change with care. |

---

## 2. Repository root

| File | Status | What it is |
|---|---|---|
| `manifest.yaml` | **CANON** | The only file you edit when a screen is added, renamed or retired. Also holds `release:` (must be today's date to publish) and `public:` (false keeps `noindex` on every prototype). |
| `index.html` | **GENERATED** | The reviewer entry point. `build.py` overwrites it from `manifest.yaml`. Hand edits vanish. |
| `build.py` | **CANON** | Preflight + generates `index.html`. `python3 build.py --check` checks and writes nothing. Errors block; warnings are the standing backlog. |
| `publish.sh` | **CANON** | check → build → commit → push. Refuses to run unless `release:` is today. |
| `scan.sh` | **GUARD** | Audits all three vault defences at once. Run it if you ever doubt them. |
| `setup-guards.sh` | **GUARD** | Restores `+x` and installs the pre-commit hook. **Run after every fresh clone.** |
| `.githooks/pre-commit` | **GUARD** | Blocks any commit staging a path containing `matbakh-private` or `DO-NOT-COMMIT`, whatever tool made it. Uses `#!/bin/bash`, not `env bash` — GitHub Desktop's PATH cannot resolve the latter. |
| `.gitignore` | **GUARD** | Second line of defence. Names four whitelisted content files by hand; see §5. |
| `import-screen.sh` | — | Imports a Claude Design export into `prototypes/` with a safe name. |
| `README.md` | **CANON** | The loop, the preflight table, the reviewer notes. Kept under this name by deliberate exception — GitHub renders only `README.md` as the landing page. See §11. |
| `DIRECTORY.md` | **CANON** | This file. |
| `CHANGELOG.md` | **CANON** | One entry per publish, newest first. Preflight warns when a prototype is newer than the top entry. |
| `ATTRIBUTIONS.md` | **PLACEHOLDER** | **Seven blank rows on a repository that is already public.** CC-BY and CC-BY-SA both require credit; this is a licence condition being missed now, not a pre-launch chore. `build.py` cannot check it — only you know each file's provenance. |
| `.gitattributes` | — | Line endings and diff behaviour. |
| `.nojekyll` | — | Stops GitHub Pages mangling underscore-prefixed paths. |

---

## 3. `prototypes/` — the screens

Kebab-case names only; a space becomes `%20` in every shared link and
`publish.sh` refuses the commit. `support.js` **must** sit beside them or the
screens render blank with no visible error.

| File | Status | In the manifest? | What it is |
|---|---|---|---|
| `bolognese-iphone.html` | **CANON**, tagged TEMPORARY | lead | The current lead. First prototype driven end to end by real recipe data, both locales, nothing scrolling. Exists to settle option C (icons + a frame from the cook video); **comes out once that is decided**. |
| `app-iphone.html` | — | yes | The earlier molokhia linked flow, hand-built. Dropped one level when bolognese landed. Still the only prototype with the Resume button. |
| `recipe-screen-iphone.html` | — | yes | Pre-commit screen, single surface. Tagged `HAND SCROLL` — it fits the arc and basket together only because it is allowed to scroll. |
| `cook-mode-tablet.html` | — | yes | The primary posture. |
| `cook-mode-iphone.html` | — | yes | Same session logic, one-handed. |
| `cook-mode-tablet-white.html` | — | yes | Colour experiment. |
| `cook-mode-iphone-white.html` | — | yes | Colour experiment. |
| `storyboard-bench-sheet.html` | **WORKING** | added 26 Aug | Bench sheet for the storyboard companion. Was an orphan — on disk, in no manifest, so preflight warned and no reviewer could find it. |
| `tile-comparison.html` | **WORKING** | added 26 Aug | *What Goes In The Tile* — the sheet that argued option C. Same orphan story. |
| `support.js` | **CANON** | n/a | Shared runtime. Must stay in this folder. |

> The two working sheets pull fonts from the Google Fonts CDN; the rest use
> system fonts. Not a defect, but it means those two look different offline.

---

## 4. `design/` — decisions, specification, glyphs

| File | Status | What it is |
|---|---|---|
| `philosophy.md` | **CANON** | The settled decisions and the open questions, with a dated decision log. Renumbered around 13 August: anything written before then cites the old sections. `§16.4` is deliberately vacant — see the note in place. |
| `authoring-standard.md` | **CANON** | How to enter a recipe, with all 21 enforced errors and 11 warnings documented. Author against this, not memory. Closes C-03. |
| `asset-spec.md` | **CANON** | Photography craft, derived from real render geometry. WebP q82, 1600×1280 hero, 1400×1050 step, subject in the middle 65%. A lighting change reads to a cook as a doneness change. |
| `tokens.css` | **CANON** | The palette and type scale. Not a suggestion — an invented terracotta once pushed the undeclared-colour warning from 30 to 48. |
| `step-imagery-research.md` | **CANON** | The four options studied. Records *why* photographs cannot replace icons: at 17px they are eight indistinguishable brown pans. |
| `step-imagery-decision.md` | **CANON** | The options as finally analysed, and the recommendation — **option E**, shoot the vocabulary once rather than the catalogue. It **supersedes** `step-imagery-research.md`'s option C, which it improves on rather than restates. CANON here means the analysis is canonical; **the decision is PM-09 and has not been taken.** Reading this row as "C is settled" is how PM-09 spent eleven days pointed at the superseded option. |
| `storyboard-companion.md` | **CANON** | The storyboard companion. |
| `Matbakh-storyboard-companion.pdf` | **GENERATED** | A render of the file above. Regenerate rather than edit; if the two disagree, the `.md` is right. |
| `tag-proposal.md` | **DRAFT** | The tag vocabulary awaiting decision (PM-07). Carries a stale ingredient count — its backfill sizing was built on the wrong number. |
| `discovery-draft.md` | **DRAFT** | §16.1. Not settled. |
| `availability-draft.md` | **DRAFT** | Ingredient availability. Not settled. |
| `icons/` (20 SVG) | **PLACEHOLDER** | Geometric stand-ins. The production set is Tabler Icons (MIT), which will need its licence text at `design/icons/LICENSE`. **The prototypes render these at full fidelity, so a reviewer reads them as the icon set. They are not.** C-05 is open. |
| `icons/cuts/` (8 SVG) | **PLACEHOLDER** | The cut glyphs — a closed set on the same terms as the activity lexicon, but with no governing document yet. |
| `icons/README.md` | **CANON** | Says plainly that the glyphs are placeholders. Read it before commissioning anything. |
| `source/ios-frame.jsx` | — | Claude Design build artefact. Not shipped, not loaded by anything. |
| ~~`philosophy_old.md`~~ | **REMOVED 26 Aug** | A placeholder header plus the music decision, which now lives in `philosophy.md §12` in full. Nothing referenced it. |

---

## 5. `content/` — schema, validator, vocabulary

**The catalogue is not here.** It lives in the vault. What is here is the data
*model*, so a reviewer can understand the shape without being handed the product.

| File | Status | What it is |
|---|---|---|
| `matbakh.py` | **CANON** | Schema, validator, builder, and the `status` generator. `check` · `build` · `lexicon` · `status` · `vault`. **Every run prints which ingredient source it used — read that line first.** |
| `lexicon/activities.yaml` | **CANON** | The 81-activity lexicon across four Arabic variants. A recipe refers to `chop` by key; the word lives only here. Six activities still draw the ingredient rather than the act. |
| `lexicon/chrome.yaml` | **CANON** | Stations, locale list, and the interface strings. The editors need this alongside `activities.yaml`. |
| `recipes/_template.yaml` | **CANON** | Copy this into the **vault** to start a recipe. Never into the repo. |
| `recipes/molokhia_bil_farakh.yaml` | **FIXTURE** | So a bare clone has something to validate. It is a near-copy of the vault's authored `molokhia.yaml` — same dish, differing only in `id` and one `ordered:` flag. A raw `check` therefore reads *3 authored* where the catalogue holds two; `status` splits the two sources. Retiring it means editing four files that name it by hand: `.gitignore`, `publish.sh`, `scan.sh`, `.githooks/pre-commit`. |
| `ref/ingredients.sample.yaml` | **FIXTURE** | The 12-entry fallback used when no vault is reachable. **This is how a wrong conclusion about the ingredient reference was once reached** — the sample lacked `diet` on all 12 while the vault's full reference had it on every entry. |
| `vault.example.path` | **CANON** | Copy to `content/vault.path` (gitignored) if the vault is not at the default location. |
| `README.md` | **CANON** | What this folder is. |
| `recipes/README.md` | **CANON** | Points at the template. Kept under this name by deliberate exception — it is whitelisted **by name** in `.gitignore`, `publish.sh`, `scan.sh` and `.githooks/pre-commit`. See §11. |
| ~~`ref/ingredients.yaml`~~ | **REMOVED 26 Aug** | A stale local copy of the vault's reference, dated 31 July. Gitignored, so never committed — and **read by nothing**: `matbakh.py` resolves either the vault's copy or `ingredients.sample.yaml` and never looks at this path. It existed only to be mistaken for the real reference. |

---

## 6. `planner/` — the personal planning algorithm

| File | Status | What it is |
|---|---|---|
| `planner.py` | **CANON** | Remembers, never predicts. Local-only, which also helps on the privacy side. |
| `test_planner.py`, `test_planner_core.py` | **CANON** | 17 tests, Python 3.10–3.13. |
| `README.md` | **CANON** | How it works and what it deliberately does not do. |
| ~~`__pycache__/`~~ | **REMOVED 26 Aug** | Build junk. Already gitignored; it was only ever on disk. |

> Standing caveat: the planner can only plan over *tagged* recipes, so it has
> nothing real to work on until PM-07 lands and recipes exist.

---

## 7. `tools/` — the four browser authoring editors

Single HTML files. No server, no install, nothing uploaded. Each has a live
validation rail applying the same rules as `matbakh.py`, and refuses to produce a
download while an error stands.

| File | Status | What it is |
|---|---|---|
| `ingredient-editor.html` | **CANON** | The ingredient reference. USDA lookup plus a 6,389-food offline export. The API key lives in browser local storage, **never in a file** — USDA deactivates keys found in public repos, and this folder is in one. |
| `lexicon-editor.html` | **CANON** | Per-dialect collision detection is the check that earns its keep. 44px and 17px previews. |
| `recipe-editor.html` | **CANON** | Every field a dropdown fed from the lexicon and reference. **Repaired 15 August** — before that it silently deleted short-form ingredients on save, and `q()` truncated any prose containing a comma. Anything saved from it before 15 Aug should be re-read for lost clauses. |
| `translator.html` | **CANON** | Prose only. A translator cannot reach a structural field. |
| `ToolsReadme.md` | **CANON** | Covers all four. Named per §11; there is no `tools/README.md` any more. |
| ~~`tools-README.md`~~ | **REMOVED 26 Aug** | Was `README.md` plus a Diet section. |
| ~~`translator.md`~~ | **REMOVED 26 Aug** | Was `tools-README.md` plus a translator section — the fullest of the three, so it is the one the merged `README.md` is built from. Its name was an accident: it is what `Translator README.md` became when `publish.sh` refused a filename containing a space. |

---

## 8. `assets/`

Placeholder photography and one clip, all Wikimedia Commons, standing in for
shot art direction. `media.js` (7 MB) defines `window.MB_MEDIA`, a map of these
paths to embedded data URIs; when it is present the images load from the map,
when it is absent the prototypes fall back to the files. Both work, which is why
a reviewer on a slow connection and a reviewer opening one saved file see the
same screens.

**Every file here needs a row in `ATTRIBUTIONS.md`.** Seven are still blank.

The claude.ai project sync excludes `/assets/`, so these are the one part of the
repo not visible there.

---

## 9. Known duplicates and traps, after this cleanup

Resolved on 26 August: the three overlapping `tools/` READMEs (now one
`ToolsReadme.md`), the dead
`philosophy_old.md`, the dead `content/ref/ingredients.yaml`, `planner/__pycache__/`,
the two orphan prototypes, and the vacant `§16.4`.

Still standing, deliberately:

1. **The molokhia fixture is still a second molokhia.** Documented in place and
   in §5 above; retiring it needs a real pilot stub to stand in, plus four guard
   files edited. A decision, not a chore.
2. **`ATTRIBUTIONS.md` is seven blank rows on a public repo.** Only you know the
   provenance.
3. **The icons look finished and are not.**
4. **`design/` mixes CANON, DRAFT and WORKING in one flat folder.** Left flat on
   purpose — moving files would break `manifest.yaml` and every cross-reference
   written since 13 August. §1's status marks are the substitute for folders.
5. **The claude.ai project holds manual copies** of `authoring-standard.md`,
   `step-imagery-research.md`, `step-imagery-decision.md` and
   `storyboard-companion.md` under `claude/`, alongside the automatic GitHub
   sync of the same files. Two homes for one file is the drift the vault's
   `data-sources-and-updates.md` rule exists to prevent.

And the standing traps, which no cleanup removes:

- **`index.html` is generated.** Hand edits vanish.
- **Before diagnosing that something is missing from git, `git fetch`.** A stale
  clone will describe the world as it was, confidently.
- **Never hand-type a measurable number.** Run `matbakh.py status`.
- **A fresh clone with no vault validates against a 12-entry sample**, and says
  so on every run. Read that line first.
- **`publish.sh` refuses unless `release:` is today's date.** Deliberate.
- **iOS Safari caches hard.** Cache-bust with `?v=n` or use a Private tab.
- **Right-to-left mirrors things that are not sentences.** Isolate sequence
  indicators as LTR.
- **A prototype that renders every pixel from JavaScript is a white page** the
  moment a script fails. Test with scripts disabled.
- **Git history keeps what you push even after you delete it.**

---

## 10. Where things live that are not here

| | |
|---|---|
| Recipe catalogue, ingredient reference | `matbakh-private/03-catalogue/` |
| Project tracker (canonical) | `matbakh-private/02-strategy/matbakh_pm_log.md` |
| Handover | `matbakh-private/02-strategy/handover-2026-08-20.md` |
| Financials, strategy, research, partners, legal | `matbakh-private/01-` … `07-` |
| Refresh the log's measured half | `cd content && python3 matbakh.py status --write ../../matbakh-private/02-strategy/matbakh_pm_log.md` |

A bare `§n` in any Matbakh document means the current document. Anything else
names its file — `philosophy §9`.

---

## 11. The README naming convention

**Set 26 August 2026.** A README this project produces carries something
indicative in its name — a description attached to the word, or a date.

A bare `README.md` says only *read me*. Across these two trees there are
fourteen of them, and in a tab bar, a search result or a `git log` the filename
does no work at all: you cannot tell the one about authoring tools from the one
about the archive without opening both.

| Instead of | Write |
|---|---|
| `tools/README.md` | `tools/ToolsReadme.md` |
| `matbakh-private/README.md` | `matbakh-private/VaultReadme.md` |
| `_ARCHIVE/README.md` | `_ARCHIVE/ArchiveReadme.md` |

Each also opens with a distinctive H1 and a written date, so the content
identifies itself even when the filename has been stripped by a paste, an export
or a project sync.

**Scope.** Applies to READMEs authored from 26 August onward. The pre-existing
stubs — `assets/`, `planner/`, `design/icons/`, `content/`, and the vault's seven
numbered folders — keep their names until a session next rewrites one.

### The two permanent exceptions

| File | Why it stays `README.md` |
|---|---|
| `README.md` (repo root) | GitHub renders **only** a file called `README.md` as the repository landing page. Renaming it leaves the repo with no front door. |
| `content/recipes/README.md` | Whitelisted **by name** in four places: `.gitignore`, `publish.sh`, `scan.sh` and `.githooks/pre-commit`. Those four are what keep the recipe catalogue out of a public repository. Editing a safety net to accommodate a naming preference is the wrong way round. |

### The cost, accepted deliberately

A folder whose README has been renamed no longer gets an auto-rendered
description when browsed on GitHub. `tools/` is the first to lose it. That is the
trade: this file is the entry point for *what is in here*, and it covers every
folder at once rather than one folder at a time.
