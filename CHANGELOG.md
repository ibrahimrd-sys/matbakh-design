# Changelog

Newest first. One entry per publish. `build.py` warns if a prototype is newer
than the top entry, so this cannot quietly fall behind.

Format: `## YYYY-MM-DD — release`

## 2026-07-30b — guards simplified, import path added

- Pre-commit hook cut from 118 lines to 59. Content scanning removed: it caused
  three false positives (tokens.css, media.js twice) and caught nothing real.
  The hook now checks filenames and counts only — business documents, credential
  files, the vault marker, and recipe files beyond the template and demo.
- Hook shebang changed to `#!/bin/bash`. `#!/usr/bin/env bash` cannot resolve
  under GitHub Desktop's restricted PATH.
- The deeper content scan remains in `scan.sh`, which is advisory and run on
  demand, where a false positive costs nothing.
- `import-screen.sh` added. The repository is now the system of record for
  prototypes; Claude Design is a drafting tool with a one-way import. The script
  applies all four required transformations — kebab-case name, asset path
  rewrite, MEDIA() fallback patch, noindex stamp — and prints the manifest
  snippet to add.

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
