#!/usr/bin/env python3
"""
Matbakh design — build and preflight.

    python3 build.py            check everything, regenerate index.html
    python3 build.py --check    check only, write nothing

Preflight exists because a design review site fails silently. A moved asset or
a renamed prototype gives the reviewer a blank screen and gives you a polite
email three days later. Everything below is a failure mode that has already
happened to someone.
"""

import re, sys, subprocess, datetime, pathlib
import yaml

ROOT = pathlib.Path(__file__).parent
MAN = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
ERR, WARN = [], []


def err(m):
    ERR.append(m)


def warn(m):
    WARN.append(m)


def manifest_files():
    out = [MAN["lead"]["file"], MAN["deep_links"]["target"]]
    for s in MAN.get("sections", []):
        out += [i["file"] for i in s["items"]]
    out += [r["file"] for r in MAN.get("reference", [])]
    return out


# ─────────────────────────────────────────────────────────────── preflight

def check_files_exist():
    for f in set(manifest_files()):
        if not (ROOT / f).exists():
            err(f"manifest points at a file that is not there: {f}")


def check_no_orphans():
    listed = {pathlib.Path(f).name for f in manifest_files()}
    for p in sorted((ROOT / "prototypes").glob("*.html")):
        if p.name not in listed:
            warn(f"prototype not listed in the manifest, so no reviewer will "
                 f"ever find it: prototypes/{p.name}")


def check_filenames():
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or "node_modules" in p.parts:
            continue
        if p.is_file() and " " in p.name:
            err(f"space in filename breaks shared URLs: {p.relative_to(ROOT)}")


def check_asset_refs():
    """Every asset a prototype asks for must exist, or the screen renders empty."""
    missing = {}
    for p in sorted((ROOT / "prototypes").glob("*.html")):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        refs = set(re.findall(r'"\.\./(assets/[A-Za-z0-9._/-]+)"', txt))
        # MEDIA() keys are single-quoted and stay relative to the repo root
        refs |= set(re.findall(r"'(assets/[A-Za-z0-9._/-]+)'", txt))
        for ref in sorted(refs):
            if not (ROOT / ref).exists():
                missing.setdefault(ref, []).append(p.name)
        for ref in sorted(set(re.findall(r'src="\.?/?(support\.js)"', txt))):
            if not (p.parent / ref).exists():
                err(f"{p.name} loads {ref} and it is not beside it")
    for ref, users in missing.items():
        warn(f"missing asset {ref} — referenced by {len(users)} prototype(s). "
             f"Drop the file in and rerun; nothing else needs changing.")


def check_noindex():
    if MAN["project"].get("public"):
        return
    for p in sorted((ROOT / "prototypes").glob("*.html")):
        if 'name="robots"' not in p.read_text(encoding="utf-8", errors="ignore"):
            err(f"{p.name} has no noindex tag while project.public is false")


def check_colour_drift():
    tokens = (ROOT / "design" / "tokens.css").read_text(encoding="utf-8")
    declared = {c.upper() for c in re.findall(r"#[0-9A-Fa-f]{6}", tokens)}
    seen = {}
    for p in sorted((ROOT / "prototypes").glob("*.html")):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        for c in re.findall(r"#[0-9A-Fa-f]{6}", txt):
            seen[c.upper()] = seen.get(c.upper(), 0) + 1
    undeclared = {c: n for c, n in seen.items() if c not in declared}
    deprecated = [c for c in ("#C0562F", "#FAF6EE") if c in seen]
    if undeclared:
        top = ", ".join(f"{c}×{n}" for c, n in
                        sorted(undeclared.items(), key=lambda x: -x[1])[:6])
        warn(f"{len(undeclared)} colour(s) used but not declared in tokens.css: {top}")
    for c in deprecated:
        warn(f"{c} is marked deprecated in tokens.css but still used {seen[c]}× "
             f"— consolidate when you next touch those files")


def check_changelog():
    cl = ROOT / "CHANGELOG.md"
    if not cl.exists():
        err("no CHANGELOG.md — reviewers cannot tell what changed since they last looked")
        return
    dates = re.findall(r"##\s*(\d{4}-\d{2}-\d{2})", cl.read_text(encoding="utf-8"))
    if not dates:
        warn("CHANGELOG.md has no dated '## YYYY-MM-DD' entry")
        return
    newest_entry = max(dates)
    protos = list((ROOT / "prototypes").glob("*.html"))
    if protos:
        newest_file = max(p.stat().st_mtime for p in protos)
        fdate = datetime.date.fromtimestamp(newest_file).isoformat()
        if fdate > newest_entry:
            warn(f"a prototype changed on {fdate} but the newest changelog entry "
                 f"is {newest_entry} — add a line before publishing")
    if MAN["project"]["release"].replace(".", "-") < newest_entry.replace("-", "-")[:10]:
        pass



# The PM log is the canonical tracker and it lives in the vault, outside this
# repository — so nothing here has ever been able to tell you it had gone
# stale. Between 30 July and 13 August it fell three weeks behind and no tool
# said a word. This is the same trick check_changelog() already plays on the
# prototypes, pointed at the log.
#
# It is silent when the vault is not reachable. A fresh clone, or CI, has no
# vault by design, and a warning nobody can act on is noise.

MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"])}


def _newest_change_date():
    """The latest date this repo admits to having changed on."""
    dates = []
    cl = ROOT / "CHANGELOG.md"
    if cl.exists():
        dates += re.findall(r"##\s*(\d{4}-\d{2}-\d{2})", cl.read_text(encoding="utf-8"))
    protos = list((ROOT / "prototypes").glob("*.html"))
    if protos:
        dates.append(datetime.date.fromtimestamp(
            max(p.stat().st_mtime for p in protos)).isoformat())
    return max(dates) if dates else None


def _vault_path():
    """Ask matbakh.py rather than re-implement its four-step resolution order.
    One copy of that logic is the whole point."""
    v = ROOT / "content" / "matbakh.py"
    if not v.exists():
        return None
    try:
        r = subprocess.run([sys.executable, "matbakh.py", "vault"],
                           cwd=ROOT / "content", capture_output=True, text=True,
                           timeout=60)
    except Exception:
        return None
    out = r.stdout.strip().splitlines()
    out = [l for l in out if l.strip()]
    if not out or out[-1].strip() == "MISSING":
        return None
    return pathlib.Path(out[-1].strip())


def check_pm_log():
    newest = _newest_change_date()
    if not newest:
        return
    vault = _vault_path()
    if not vault:
        return                      # no vault reachable — nothing to check
    log = vault.parent / "02-strategy" / "matbakh_pm_log.md"
    if not log.exists():
        hits = list(vault.parent.glob("*/matbakh_pm_log.md"))
        if not hits:
            return
        log = hits[0]
    txt = log.read_text(encoding="utf-8", errors="replace")

    # 1. the hand-maintained half: is the log's own date behind the repo?
    iso = re.search(r"Last updated:\**\s*(\d{4}-\d{2}-\d{2})", txt)
    if iso:
        stamped = iso.group(1)
    else:
        long = re.search(r"Last updated:\**\s*(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", txt)
        if not long:
            warn("the PM log has no readable 'Last updated:' date — add one as "
                 "YYYY-MM-DD so this check can do its job")
            return
        d, mon, y = long.groups()
        m = MONTHS.get(mon.lower())
        if not m:
            warn(f"the PM log's 'Last updated: {long.group(0)}' is not a date "
                 "this can read — use YYYY-MM-DD")
            return
        stamped = f"{y}-{m:02d}-{int(d):02d}"
        warn("the PM log's 'Last updated' is in long form — switch it to "
             "YYYY-MM-DD, which is what this check reads")
    if stamped < newest:
        warn(f"the PM log was last updated {stamped} but this repo changed on "
             f"{newest} — the canonical tracker is behind. It is in the vault: "
             f"{log}")

    # 2. the generated half: is the measured block behind the repo?
    gen = re.search(r"GENERATED: matbakh\.py status.*?Measured\s+(\d{4}-\d{2}-\d{2})",
                    txt, re.S)
    if not gen:
        warn("the PM log has no generated status block — run: "
             "cd content && python3 matbakh.py status --write <log>")
    elif gen.group(1) < newest:
        warn(f"the PM log's measured figures are from {gen.group(1)} and the "
             f"repo changed on {newest} — re-run: cd content && "
             f"python3 matbakh.py status --write <log>")



def check_content_guard():
    gi = ROOT / ".gitignore"
    if not gi.exists():
        err("no .gitignore — the recipe catalogue and business model would be "
            "committed to a public repository")
        return
    txt = gi.read_text(encoding="utf-8")
    for needed in ("content/recipes/", "*.xlsx", "*.docx"):
        if needed not in txt:
            err(f".gitignore does not exclude {needed} — publishing would expose it")


def check_content():
    v = ROOT / "content" / "matbakh.py"
    if not v.exists():
        warn("content/ has no validator; recipe data is unchecked")
        return
    r = subprocess.run([sys.executable, "matbakh.py", "check"],
                       cwd=ROOT / "content", capture_output=True, text=True)
    if r.returncode != 0:
        err("recipe validation failed — run: cd content && python3 matbakh.py check")
    else:
        tail = [l for l in r.stdout.strip().splitlines() if "recipe(s)" in l]
        if tail:
            print("  content: " + tail[-1].strip())


# ──────────────────────────────────────────────────────────────── generate

CSS = """
  :root { --paper:#F4EFE6; --ink:#221E1A; --card:#FBF8F2; --accent:#A2542F; }
  * { box-sizing:border-box }
  body { margin:0; background:var(--paper); color:var(--ink);
         font-family:'IBM Plex Sans',system-ui,sans-serif; -webkit-font-smoothing:antialiased }
  a { color:var(--accent); text-decoration:none } a:hover { color:#8A4526 }
  .wrap { max-width:940px; margin:0 auto; padding:56px 28px 80px }
  .head { display:flex; align-items:flex-end; gap:18px; padding-bottom:18px;
          border-bottom:1px solid rgba(34,30,26,.14) }
  h1 { margin:0; font-size:30px; font-weight:600; letter-spacing:-.02em }
  .ar { font-family:'Noto Naskh Arabic',serif; font-size:19px; color:rgba(34,30,26,.6) }
  .mono { font-family:'IBM Plex Mono',monospace; letter-spacing:.06em }
  .head .mono { white-space:nowrap; font-size:10.5px; color:rgba(34,30,26,.55) }
  .lede { margin:20px 0 0; max-width:60ch; font-size:15px; line-height:1.6;
          color:rgba(34,30,26,.75); text-wrap:pretty }
  .draft { margin:22px 0 0; padding:10px 14px; border-radius:9px;
           border:1.5px solid rgba(34,30,26,.2); background:#FBF8F2;
           font-family:'IBM Plex Mono',monospace; font-size:10.5px;
           letter-spacing:.1em; color:rgba(34,30,26,.66) }
  h2 { margin:44px 0 4px; font-size:11px; letter-spacing:.16em; text-transform:uppercase;
       color:rgba(34,30,26,.55) }
  .sub { margin:0 0 16px; font-size:13px; color:rgba(34,30,26,.55); max-width:66ch; line-height:1.5 }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:14px }
  .card { display:flex; flex-direction:column; gap:8px; padding:18px; border-radius:14px;
          background:var(--card); border:1.5px solid rgba(34,30,26,.14) }
  .card:hover { border-color:var(--accent) }
  .card .t { font-size:16px; font-weight:600; letter-spacing:-.01em; color:var(--ink) }
  .card .d { font-size:13px; line-height:1.5; color:rgba(34,30,26,.65) }
  .tags { display:flex; flex-wrap:wrap; gap:6px; margin-top:2px }
  .tag { font-family:'IBM Plex Mono',monospace; font-size:10.5px; letter-spacing:.1em;
         white-space:nowrap; padding:3px 7px; border-radius:5px;
         background:rgba(34,30,26,.07); color:rgba(34,30,26,.62) }
  .lead { background:#2A2620; border-color:#2A2620 }
  .lead .t { color:#F7F3EB } .lead .d { color:rgba(247,243,235,.72) }
  .lead .tag { background:rgba(247,243,235,.12); color:rgba(247,243,235,.75) }
  .rows { display:flex; flex-direction:column; border-radius:14px; overflow:hidden;
          border:1.5px solid rgba(34,30,26,.14) }
  .row { display:flex; align-items:center; gap:14px; padding:14px 16px; background:var(--card) }
  .row:nth-child(even) { background:#F8F4EC }
  .row .t { flex:1; font-size:14.5px; color:var(--ink) }
  .row .m { font-family:'IBM Plex Mono',monospace; font-size:10.5px; color:rgba(34,30,26,.6) }
  footer { margin-top:52px; padding-top:18px; border-top:1px solid rgba(34,30,26,.14);
           font-family:'IBM Plex Mono',monospace; font-size:10.5px; line-height:1.8;
           color:rgba(34,30,26,.55) }
"""


def esc(s):
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def flat(s):
    return " ".join(str(s or "").split())


def card(it, lead=False):
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in it.get("tags", []))
    return (f'<a class="card{" lead" if lead else ""}" href="{esc(it["file"])}">'
            f'<div class="t">{esc(it["title"])}</div>'
            f'<div class="d">{esc(flat(it["blurb"]))}</div>'
            f'<div class="tags">{tags}</div></a>')


def generate():
    p = MAN["project"]
    h = ['<!DOCTYPE html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">']
    if not p.get("public"):
        h.append('<meta name="robots" content="noindex,nofollow">')
    h += [f'<title>{esc(p["name"])} — design files</title>',
          '<link rel="preconnect" href="https://fonts.googleapis.com">',
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
          '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600'
          '&family=IBM+Plex+Mono:wght@400;500&family=Noto+Naskh+Arabic:wght@400&display=swap" '
          'rel="stylesheet">',
          f'<style>{CSS}</style>', '</head>', '<body>',
          '<!-- GENERATED BY build.py FROM manifest.yaml — DO NOT EDIT BY HAND -->',
          '<div class="wrap">',
          '<div class="head">', f'<h1>{esc(p["name"])}</h1>',
          f'<div class="ar">{esc(p["name_ar"])}</div>', '<div style="flex:1"></div>',
          f'<div class="mono">DESIGN FILES · REL {esc(p["release"])}</div>', '</div>',
          f'<p class="lede">{esc(flat(p["tagline"]))}</p>']

    if not p.get("public"):
        h.append('<p class="draft">INTERNAL REVIEW BUILD · NOT INDEXED · '
                 'PLACEHOLDER ART AND ILLUSTRATIVE PRICING</p>')

    h += ['<h2>Start here</h2>',
          '<p class="sub">The linked flow — decide, then cook, with state carried '
          'between the two.</p>',
          f'<div class="grid">{card(MAN["lead"], lead=True)}</div>']

    dl = MAN["deep_links"]
    h += ['<h2>Send a reviewer to one step</h2>',
          f'<p class="sub">{esc(flat(dl["note"]))}</p>', '<div class="rows">']
    for l in dl["links"]:
        h.append(f'<div class="row"><div class="t"><a href="{esc(dl["target"])}'
                 f'{esc(l["hash"])}">{esc(l["label"])}</a></div>'
                 f'<div class="m">{esc(l["hash"])}</div></div>')
    h.append('</div>')

    for s in MAN.get("sections", []):
        h += [f'<h2>{esc(s["heading"])}</h2>', f'<p class="sub">{esc(flat(s["sub"]))}</p>',
              '<div class="grid">' + "".join(card(i) for i in s["items"]) + '</div>']

    h += ['<h2>Reference</h2>', '<div class="rows">']
    for r in MAN.get("reference", []):
        h.append(f'<div class="row"><div class="t"><a href="{esc(r["file"])}">'
                 f'{esc(r["title"])}</a></div><div class="m">{esc(r["kind"])}</div></div>')
    h.append('</div>')

    h.append('<footer>')
    for c in MAN.get("caveats", []):
        h.append(esc(flat(c)).upper() + '<br>')
    if MAN.get("next_up"):
        h.append('NEXT UP · ' + " · ".join(esc(x).upper() for x in MAN["next_up"]) + '<br>')
    h.append(f'RELEASE {esc(p["release"])} · GENERATED FROM MANIFEST.YAML BY BUILD.PY')
    h += ['</footer>', '</div>', '</body>', '</html>']
    return "\n".join(h) + "\n"


# ───────────────────────────────────────────────────────────────────── main

def main():
    check_only = "--check" in sys.argv
    print("preflight")
    for fn in (check_files_exist, check_no_orphans, check_filenames, check_asset_refs,
               check_noindex, check_colour_drift, check_changelog,
               check_pm_log, check_content_guard, check_content):
        fn()

    for e in ERR:
        print(f"  error    {e}")
    for w in WARN:
        print(f"  warning  {w}")
    if not ERR and not WARN:
        print("  clean")

    if ERR:
        print(f"\n{len(ERR)} error(s) — index.html not written. Nothing published.")
        sys.exit(1)

    if check_only:
        print(f"\ncheck only · {len(WARN)} warning(s)")
        return

    # newline="\n" is required: Python's default text mode writes CRLF on
    # Windows, which contradicts the eol=lf rule in .gitattributes and makes
    # git warn on every add.
    with open(ROOT / "index.html", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(generate())
    n = sum(len(s["items"]) for s in MAN.get("sections", [])) + 1
    print(f"\nindex.html written · {n} screens · "
          f"{len(MAN['deep_links']['links'])} deep links · "
          f"release {MAN['project']['release']} · {len(WARN)} warning(s)")


if __name__ == "__main__":
    main()
