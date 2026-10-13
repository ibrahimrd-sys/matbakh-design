#!/usr/bin/env python3
"""
ingredient-match — find which reference ingredient an imported ingredient name means.

    python3 ingredient-match.py "huile d'olive" "حليب سائل" "2 large eggs"
    python3 ingredient-match.py --csv parsed.csv --out matched.csv     # a column named `name`

Import step 3 (PM log §11 item 9, D-19): after `ingredient-lines.py` has split
a line into quantity, unit and ingredient, this matches the ingredient against
the vault's `ref/ingredients.yaml` — every entry's English and Arabic `name`
and its `aliases` (philosophy §45). A match is the reference id, or empty.

How it matches: both sides are lower-cased and normalised (Arabic diacritics
and letter variants — أ إ آ → ا, ة → ه, ى → ي — the Arabic article ال, Arabic
dual and plural endings, English plurals), then a reference name matches when
**all its words appear in the ingredient's words**. The longest such name wins,
so *garlic powder* finds `garlic_powder`, not `garlic`. **A match is refused**
when the ingredient has a word that makes it a different food — *broth*,
*powder*, *extract*, *syrup*, *sauce*, *paste*, *flakes*, *vinegar* … (FORM) —
and the matched name does not, so *chicken broth* never becomes a chicken. An
alias written with a leading = (*=pepper*) matches only the whole name. It
never guesses beyond that: no fuzzy spelling, no translation, no AI. An
ingredient it cannot match comes back empty, and an importer keeps it on the
shopping list as plain text.

The reference is found the way `content/matbakh.py` finds it: --ref PATH,
then MATBAKH_VAULT, then content/vault.path, then ../../matbakh-private/03-catalogue.
"""

import argparse, csv, os, pathlib, re, sys, unicodedata

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent


def _reference(path=None):
    if path:
        return pathlib.Path(path)
    if os.environ.get("MATBAKH_VAULT"):
        return pathlib.Path(os.environ["MATBAKH_VAULT"]).expanduser() / "ref" / "ingredients.yaml"
    cfg = REPO / "content" / "vault.path"
    if cfg.exists():
        line = cfg.read_text(encoding="utf-8").strip().splitlines()
        if line and line[0].strip() and not line[0].startswith("#"):
            return pathlib.Path(line[0].strip()).expanduser() / "ref" / "ingredients.yaml"
    return REPO / ".." / "matbakh-private" / "03-catalogue" / "ref" / "ingredients.yaml"


def words(s):
    s = unicodedata.normalize("NFKC", str(s)).lower()
    s = re.sub(r"[ً-ْـ]", "", s)              # Arabic diacritics, tatweel
    s = s.translate(str.maketrans("أإآىة", "ااايه"))
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))  # é → e, but keep Arabic letters
    s = re.sub(r"[^\w\s]", " ", s)
    out = []
    for t in s.split():
        t = re.sub(r"^ال(?=\w{2})", "", t)
        if re.fullmatch(r"[a-z]+", t) and len(t) > 3:
            t = re.sub(r"ies$", "y", t)
            t = re.sub(r"(oes|ches|shes)$", lambda m: m.group(1)[:-2], t)
            t = re.sub(r"s$", "", t)
        elif re.fullmatch(r"[ء-ي]+", t):
            # dual and plural endings (بصلتان, بيضتين, بيضات), then the ة that was
            # turned into ه (جزرة → جزر, بودرة → بودر) — on both sides alike
            if len(t) >= 5 and t.endswith(("تان", "تين")):
                t = t[:-3]
            elif len(t) >= 5 and t.endswith("ات"):
                t = t[:-2]
            if len(t) >= 4 and t.endswith("ه"):
                t = t[:-1]
            if t == "مسحوق":                     # مسحوق is powder, as بودرة is
                t = "بودر"
        out.append(t)
    return out


# A word that makes an ingredient a different food from the plain thing named
# inside it: chicken *broth* is not a chicken, *powdered* sugar is not granulated.
# A match that lacks one of these words the ingredient has is refused, and the
# ingredient stays on the list as text. LAST counts only as the last word:
# *garlic salt* is not salt, but *salt and pepper* and *a sprinkle of salt* are.
FORM = set(words("powder powdered poudre بودرة broth stock bouillon مرقة extract extrait "
                 "خلاصة syrup sirop sauce صوص صلصة paste معجون flakes vinegar vinaigre خل "
                 "condensed evaporated cereal root pâtissière flour farine دقيق starch "
                 "amidon wine vin نبيذ beans haricots fritters beignets purée creamed زهر ورد"))
LAST = set(words("salt sprinkles"))


class Matcher:
    def __init__(self, ref_path=None):
        self.path = _reference(ref_path)
        ref = yaml.safe_load(open(self.path, encoding="utf-8"))
        self.size = len(ref)
        self.names = []                                   # (words, id, label, whole)
        for iid, v in ref.items():
            labels = [str(n) for n in (v.get("name") or {}).values() if n]
            labels += [str(a) for a in (v.get("aliases") or [])]
            labels.append(iid.replace("_", " "))
            for lab in labels:
                # an alias written =pepper matches only an ingredient that is that
                # name and nothing more: *pepper*, but not *cayenne pepper*
                whole = lab.startswith("=")
                w = words(lab[1:] if whole else lab)
                if w:
                    self.names.append((w, iid, lab, whole))

    def match(self, name):
        """(id, matched label) for the longest reference name contained in `name`, or ("", "").

        Refused, and so empty, when the ingredient has a FORM word the name lacks,
        or when it has one and two different names tie for longest (*garlic salt*:
        garlic, or salt?). Two entries sharing one name is the reference's to fix;
        the first in the file wins, as before."""
        ws = words(name)
        have = set(ws)
        form = (have & FORM) | ({ws[-1]} & LAST if ws else set())
        best = []
        for w, iid, lab, whole in self.names:
            if whole and set(w) != have:
                continue
            if all(t in have for t in w):
                if not best or len(w) > len(best[0][0]):
                    best = [(w, iid, lab)]
                elif len(w) == len(best[0][0]):
                    best.append((w, iid, lab))
        if not best:
            return ("", "")
        w, iid, lab = best[0][:3]
        if form and (form - set(w) or len({tuple(sorted(b[0])) for b in best}) > 1):
            return ("", "")
        return (iid, lab)


def main():
    ap = argparse.ArgumentParser(description="Match imported ingredient names to the reference.")
    ap.add_argument("names", nargs="*")
    ap.add_argument("--csv", help="read names from this CSV's `name` column")
    ap.add_argument("--out", help="write the input rows plus `match` and `matched_on`")
    ap.add_argument("--ref", help="path to ingredients.yaml (default: the vault)")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    m = Matcher(a.ref)
    print(f"reference: {m.size} ingredients from {m.path}", file=sys.stderr)
    rows = [{"name": n} for n in a.names]
    if a.csv:
        with open(a.csv, encoding="utf-8-sig") as fh:
            rows += list(csv.DictReader(fh))
    if not rows:
        ap.error("give names, or --csv")
    for r in rows:
        r["match"], r["matched_on"] = m.match(r.get("name", ""))
    if a.out:
        with open(a.out, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"written {len(rows)} rows to {a.out}")
    else:
        for r in rows:
            print(f"{r['match'] or '—':<22} {r['name']}" + (f"   (on: {r['matched_on']})" if r["match"] else ""))


if __name__ == "__main__":
    main()
