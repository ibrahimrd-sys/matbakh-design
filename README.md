# Matbakh — application design

Hi-fi prototypes and the design system behind them. This folder is the single
place the design lives; everything a reviewer needs is reachable from
`index.html`.

**One rule:** `index.html` is generated. Edit `manifest.yaml`, run `build.py`.
If you hand-edit `index.html` your changes are lost on the next build.

---

## Structure

```
matbakh-design/
├── manifest.yaml          ← you edit this when a screen changes
├── build.py               ← preflight checks + generates index.html
├── publish.sh             ← check, build, commit, push in one command
├── index.html             ← GENERATED. entry point for reviewers
│
├── prototypes/            stable kebab-case names → shareable URLs
│   ├── app-iphone.html            the linked flow (lead prototype)
│   ├── recipe-screen-iphone.html
│   ├── cook-mode-tablet.html
│   ├── cook-mode-iphone.html
│   ├── cook-mode-tablet-white.html
│   ├── cook-mode-iphone-white.html
│   └── support.js         shared runtime, must sit beside the prototypes
│
├── assets/                photos, clips, media.js
├── design/
│   ├── tokens.css         canonical palette and type scale
│   ├── philosophy.md      settled decisions and open questions
│   └── source/            Claude Design build artefacts, not shipped
├── content/               recipe schema + validator (catalogue gitignored)
│
├── CHANGELOG.md           one entry per publish
├── ATTRIBUTIONS.md        CC credits — a licence condition once public
├── .gitignore             keeps the catalogue and the financials out
└── .nojekyll              stops GitHub Pages mangling the files
```

### What is deliberately **not** here

The financial model, the strategy document and the recipe catalogue. A GitHub
Pages site on the free plan requires a public repository, and all three would
be world-readable. `.gitignore` blocks them and `publish.sh` refuses to push if
one slips through. Keep the catalogue in a separate private repo; only the
schema, the template and one demo recipe are tracked here so the structure
stays reviewable.

---

## The update loop

Whatever changed, the loop is the same three steps.

**1. Drop the new or revised file in.** A revised screen replaces the file in
`prototypes/`. A new screen gets a kebab-case name — no spaces, ever, or the
shared URL fills with `%20`.

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
| `.gitignore` missing its guards | The catalogue or the financials going public |
| Recipe data invalid | Runs `content/matbakh.py check` as part of the same pass |

Errors block the build. Warnings do not — they are the standing backlog.

---

## Publishing to GitHub, first time

Do this once. Steps 4–6 are the only part that needs a decision.

**1. Create the repository.** On github.com: **New repository**, name it
`matbakh-design`. Do not add a README or a `.gitignore` — this folder has both.

**2. Connect this folder.** In a terminal, from inside `matbakh-design/`:

```bash
git init
bash setup-guards.sh          # restores +x, installs the pre-commit hook
./scan.sh                     # confirm nothing sensitive is present
git branch -M main
git add -A
git commit -m "Design repository, first publish"
git remote add origin https://github.com/YOUR-USERNAME/matbakh-design.git
git push -u origin main
```

If you would rather not use the terminal: install **GitHub Desktop**, choose
*Add Local Repository*, point it at this folder, then *Publish repository*. It
runs the same commands. `publish.sh` will still work afterwards.

**3. Sanity-check what landed.** Open the repo on github.com and confirm you do
**not** see any `.xlsx`, `.docx`, or more than two files in `content/recipes/`.
If you do, stop and fix `.gitignore` before enabling Pages — git history keeps
what you push even after you delete it.

**4. Decide public or private.** Pages from a **private** repository requires a
paid GitHub plan; on the free plan the repo must be **public** for Pages to
serve. Worth confirming against GitHub's current pricing page, since plan
features move. Either way the `noindex` tag keeps the site out of search
results while `public: false` in the manifest.

**5. Enable Pages.** Repo **Settings → Pages → Source: Deploy from a branch →
Branch: `main`, folder: `/ (root)` → Save.** First build takes a couple of
minutes.

**6. Your review URL** is `https://YOUR-USERNAME.github.io/matbakh-design/`.
Deep links append directly:

```
https://YOUR-USERNAME.github.io/matbakh-design/prototypes/app-iphone.html#cook/4
```

---

## Before this goes to anyone outside

- [ ] Fill in `ATTRIBUTIONS.md`. Once the repo is public, crediting the CC
      photography is a licence condition, not a courtesy.
- [ ] Replace `design/philosophy.md` with the real document.
- [ ] Drop `assets/` in — preflight currently reports 8 missing files.
- [ ] Confirm the repo contains no financial or strategy documents.
- [ ] Leave `public: false` until launch. It keeps the `noindex` banner and tag
      in place, which is what stops a half-finished design being the first
      Matbakh result on Google.

## Notes for reviewers

Scroll normally; swipe across the tiles to turn pages; tap a tile to mark it
done. Timers ring an audible alarm with a Silence / +2′ banner — keep the screen
awake for it to sound. The shopping list is editable. Servings: presets 2 / 4 / 8
or type any number up to 60.

Opened on a phone or tablet the prototype drops the mockup bezel and fills the
real screen. On a laptop it stays in the frame, with a **PREVIEW AS REAL DEVICE**
toggle underneath. Force either way with `?device=1` or `?device=0`, which
combines with the step links.

Photography and the technique clip are Wikimedia Commons stand-ins, not final
art direction. Icon glyphs are geometric placeholders. Prices are illustrative.
