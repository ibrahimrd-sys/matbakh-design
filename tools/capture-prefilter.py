#!/usr/bin/env python3
"""
capture-prefilter — structural flags on a capture-draft, for the chef reviewing it.

    python3 tools/capture-prefilter.py ../matbakh-private/08-unreviewed-captures/Beef_Bourguignon.txt
    python3 tools/capture-prefilter.py draft.json --json

The pre-filter engine of CaptureDraftRunReadme.md §7, built 20 October 2026 on
tools/recipe_core/. It reads a draft capture-draft.py wrote — its JSON, or its
--format text — and prints flags under checks A (completeness), D (unmapped
ingredients), E (source), F (duplicate entries), G (temperature units) and H (list
against method).

**Flags only.** It never corrects, converts, merges, scores or filters anything,
never decides whether a chef sees a draft, and writes nothing — not to the draft,
not to 03-catalogue/. B (plausibility) waits for a chef's thresholds; C (duplicates
against the catalogue) for a larger catalogue. No AI, no network.
"""

import argparse, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # tools/, for recipe_core
import yaml
from recipe_core import checks
from recipe_core.lines import parse
from recipe_core.match import Matcher


def main():
    ap = argparse.ArgumentParser(description="Flags on a capture-draft for the chef. Flags only.")
    ap.add_argument("draft", type=pathlib.Path, help="a capture-draft output: .json or .txt")
    ap.add_argument("--json", action="store_true", help="print the flags as JSON")
    ap.add_argument("--ref", help="path to ingredients.yaml (default: the vault)")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    if not a.draft.is_file():
        sys.exit(f"capture-prefilter: {a.draft} is not a file.")
    draft = checks.load(a.draft)
    m = Matcher(a.ref)
    ref = yaml.safe_load(open(m.path, encoding="utf-8"))
    flags = checks.run(draft, m, ref, parse)
    if a.json:
        print(json.dumps(dict(title=draft["title"], source=draft["source"], flags=flags), ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(checks.as_text(draft, flags))


if __name__ == "__main__":
    main()
