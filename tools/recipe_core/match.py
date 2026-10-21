"""Match an ingredient name to the reference — moved unchanged from ingredient-match.py
(import step 3). See that script's docstring for how it matches."""

import os, pathlib, re, unicodedata

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent.parent   # the design repo


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
# A ground spice is a powder already: *cumin powder* and *مسحوق الكمون* are
# cumin_ground, though its name lacks the word. So these do not refuse a match
# to an entry whose scaling class is `seasoning`.
POWDER = set(words("powder powdered poudre بودرة"))
# Filler words a whole-name alias ignores: *a little oil* (قليل زيت) is oil.
FILLER = set(words("a little some few of قليل شوية بعض un peu de du"))


class Matcher:
    def __init__(self, ref_path=None):
        self.path = _reference(ref_path)
        ref = yaml.safe_load(open(self.path, encoding="utf-8"))
        self.size = len(ref)
        self.names = []                                   # (words, id, label, whole)
        self.seasoning = {iid for iid, v in ref.items() if v.get("cls") == "seasoning"}
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
            if whole and set(w) != have - FILLER:
                continue
            if all(t in have for t in w):
                if not best or len(w) > len(best[0][0]):
                    best = [(w, iid, lab)]
                elif len(w) == len(best[0][0]):
                    best.append((w, iid, lab))
        if not best:
            return ("", "")
        w, iid, lab = best[0][:3]
        if iid in self.seasoning:
            form -= POWDER
        if form and (form - set(w) or len({tuple(sorted(b[0])) for b in best}) > 1):
            return ("", "")
        return (iid, lab)
