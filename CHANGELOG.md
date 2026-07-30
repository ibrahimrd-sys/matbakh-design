# Changelog

Newest first. One entry per publish. `build.py` warns if a prototype is newer
than the top entry, so this cannot quietly fall behind.

Format: `## YYYY-MM-DD — release`

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
