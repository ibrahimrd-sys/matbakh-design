#!/usr/bin/env python3
"""
structured-data-check — do recipe pages publish their own recipe data?

    python3 structured-data-check.py urls.txt
    python3 structured-data-check.py urls.txt --csv ../../matbakh-private/04-research/sd-check.csv
    python3 structured-data-check.py https://example.com/a-recipe https://example.org/another
    python3 structured-data-check.py --site example.com --site example.org --per-site 10

The first of the import checks (PM log §11 item 9, D-19): before any import
engine is built, find out how many Arabic recipe pages carry schema.org Recipe
data — JSON-LD or microdata — that an importer could read without AI.

For each URL it reports whether the page could be fetched, whether it carries
a Recipe, and which fields that Recipe fills: ingredient and step counts, how
many ingredient lines carry a quantity, how many are in Arabic, yield, times,
nutrition, image and video. Then it rolls the results up per site.

What it does NOT do:
  - it keeps no recipe text — only counts and yes/no flags — so its output is
    not a copy of anyone's recipe and can be filed anywhere;
  - it calls no AI service and sends nothing anywhere except the page requests;
  - it fetches nothing a site's robots.txt disallows, and waits between
    requests to the same site (--delay).

Standard library only. The URL file takes one URL per line; blank lines and
lines starting with # are skipped.

--site samples recipe pages from a site's own sitemap instead of a hand-made
list: it reads the sitemaps named in robots.txt (or the usual /sitemap.xml
locations), keeps URLs that look like single recipes, and picks --per-site of
them at random, with a fixed --seed so a run can be repeated. --match narrows
which URLs count as recipes when the default guess is wrong for a site.
"""

import argparse, collections, csv, gzip, html.parser, http.client, json, random, re, sys, time
import xml.etree.ElementTree as ET
import urllib.error, urllib.parse, urllib.request, urllib.robotparser


import pathlib as _pathlib, sys as _sys
_sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))   # tools/, for recipe_core
from recipe_core.page import (UA, ARABIC, QUANTITY, MAX_BYTES, FRENCH, _Page, _is_recipe, _recipes_in, _flatten_steps, _as_list, _yes, _language, _robots, _last, allowed, _encode, fetch)

FIELDS = ["url", "site", "status", "final_url", "language", "lang", "jsonld_blocks", "recipe_source",
          "name", "ingredients", "ingredients_with_quantity", "ingredients_arabic",
          "steps", "yield", "total_time", "nutrition", "image", "video"]


def analyse(raw, charset):
    page = _Page()
    page.feed(raw.decode(charset or "utf-8", errors="replace"))
    recipes, bad = [], 0
    for blob in page.jsonld:
        try:
            recipes += _recipes_in(json.loads(blob.strip()))
        except json.JSONDecodeError:
            bad += 1
    row = {"lang": page.lang, "jsonld_blocks": f"{len(page.jsonld)}" + (f" ({bad} unparseable)" if bad else "")}
    if recipes:
        r = recipes[0]
        ings = [str(x) for x in _as_list(r.get("recipeIngredient") or r.get("ingredients"))]
        row.update(recipe_source="json-ld", name=_yes(r.get("name")),
                   steps=len(_flatten_steps(r.get("recipeInstructions"))),
                   **{"yield": _yes(r.get("recipeYield"))},
                   total_time=_yes(r.get("totalTime") or r.get("cookTime")),
                   nutrition=_yes(r.get("nutrition")), image=_yes(r.get("image")),
                   video=_yes(r.get("video")))
    elif page.micro:
        ings = [x for x in page.micro_ingredients if x]
        mp = page.micro_props
        row.update(recipe_source="microdata", name=_yes(mp.get("name")),
                   steps=mp.get("recipeInstructions", 0) or mp.get("step", 0),
                   **{"yield": _yes(mp.get("recipeYield"))},
                   total_time=_yes(mp.get("totalTime") or mp.get("cookTime")),
                   nutrition=_yes(mp.get("nutrition")), image=_yes(mp.get("image")),
                   video=_yes(mp.get("video")))
    else:
        return {**row, "recipe_source": "none", "language": _language(page.lang, None, [])}
    row["language"] = _language(page.lang, r.get("inLanguage") if recipes else None, ings)
    row.update(ingredients=len(ings),
               ingredients_with_quantity=sum(1 for i in ings if QUANTITY.search(i)),
               ingredients_arabic=sum(1 for i in ings if ARABIC.search(i)))
    return row


# ── sampling recipe pages from a site's sitemap ────────────────────────────

# a path that names a recipe, in English or Arabic (وصفة / وصفات, also URL-encoded)
RECIPE_PATH = re.compile(r"recipe|recette|/r/|وصف|%D9%88%D8%B5%D9%81", re.I)
NOT_A_RECIPE = re.compile(r"/(tag|tags|category|categories|author|page|search|collection|"
                          r"collections|video|videos|wp-content|feed|amp)(/|$)|\.(jpe?g|png|webp|pdf)$", re.I)
RECIPE_SITEMAP = re.compile(r"recipe|recette|وصف|%D9%88%D8%B5%D9%81", re.I)
MAX_SITEMAPS = 12         # sitemaps read per site
MAX_SITEMAP_URLS = 50000  # URLs collected per site before sampling
ENOUGH = 400              # stop reading sitemaps once this many candidate pages are found
VERBOSE = False


def _get(url, delay):
    """Fetch a sitemap or robots-allowed resource; returns bytes, gunzipped if needed."""
    if not allowed(url):
        raise PermissionError("robots.txt disallows " + url)
    try:
        raw, _, _ = fetch(url, delay)
    except (TimeoutError, urllib.error.URLError) as e:
        if "timed out" not in str(getattr(e, "reason", e)):
            raise
        raw, _, _ = fetch(url, delay, timeout=90)     # big sitemaps can be slow; one retry
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw


def _locs(xml):
    """(kind, [loc]) for a sitemap index or a urlset, ignoring namespaces."""
    root = ET.fromstring(xml)
    kind = root.tag.rsplit("}", 1)[-1]
    return kind, [e.text.strip() for e in root.iter() if e.tag.rsplit("}", 1)[-1] == "loc" and e.text]


def _say(msg):
    if VERBOSE:
        print("  " + msg, file=sys.stderr)


def _priority(u):
    """recipe-named sitemaps first, then post-named, then the rest; news and images last"""
    return (not RECIPE_SITEMAP.search(u), not re.search(r"post", u, re.I),
            bool(re.search(r"news|image|video|tag|author|categor", u, re.I)))


class _Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def _home_links(base, delay):
    """Fallback for a site with no sitemap: the links on its home page."""
    try:
        if not allowed(base + "/"):
            return []
        raw, charset, final = fetch(base + "/", delay)
    except (urllib.error.URLError, OSError, ValueError, http.client.HTTPException):
        return []
    p = _Links()
    p.feed(raw.decode(charset or "utf-8", errors="replace"))
    return [urllib.parse.urljoin(final, h).split("#")[0] for h in p.hrefs]


def sample_site(site, n, match, delay, rng):
    base = site if re.match(r"https?://", site) else "https://" + site
    base = base.rstrip("/")
    allowed(base + "/")                                   # loads robots.txt
    rp = _robots[f"{urllib.parse.urlsplit(base).scheme}://{urllib.parse.urlsplit(base).netloc}"]
    standard = [base + p for p in ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml")]
    # robots.txt's sitemaps first, recipe-named ones at the front; the standard
    # locations after them, in case robots.txt names a sitemap that is gone
    queue = sorted(rp.site_maps() or [], key=_priority) + standard
    pattern = re.compile(match, re.I) if match else RECIPE_PATH
    host = urllib.parse.urlsplit(base).netloc.removeprefix("www.")

    def candidate(u):
        s = urllib.parse.urlsplit(u)
        return (s.netloc.removeprefix("www.") == host and pattern.search(u)
                and not NOT_A_RECIPE.search(s.path))

    seen, urls, read, pool = set(), [], 0, []
    while queue and read < MAX_SITEMAPS and len(urls) < MAX_SITEMAP_URLS and len(pool) < ENOUGH:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            kind, locs = _locs(_get(sm, delay))
        except (urllib.error.URLError, PermissionError, ET.ParseError, OSError, ValueError,
                http.client.HTTPException) as e:
            _say(f"{sm}: skipped ({str(getattr(e, 'code', '') or e)[:60]})")
            continue
        read += 1
        if kind == "sitemapindex":
            _say(f"{sm}: index of {len(locs)}")
            queue = sorted(locs, key=_priority) + queue
        else:
            urls += locs
            pool = [u for u in dict.fromkeys(urls) if candidate(u)]
            _say(f"{sm}: {len(locs)} URLs, {len(pool)} candidates so far")
    source = f"{read} sitemap(s) read"
    if not pool:
        links = _home_links(base, delay)
        pool = [u for u in dict.fromkeys(links) if candidate(u)]
        if pool:
            source = f"no usable sitemap; {len(links)} home-page links"
    picked = rng.sample(pool, min(n, len(pool)))
    print(f"{site}: {source}, {len(urls)} sitemap URLs, {len(pool)} look like recipes, "
          f"{len(picked)} sampled", file=sys.stderr)
    return picked


def check(url, delay):
    site = urllib.parse.urlsplit(url).netloc.removeprefix("www.")
    row = {"url": url, "site": site}
    try:
        if not allowed(url):
            return {**row, "status": "robots-disallowed"}
        raw, charset, final = fetch(url, delay)
    except urllib.error.HTTPError as e:
        return {**row, "status": f"http-{e.code}"}
    except (urllib.error.URLError, TimeoutError, OSError, ValueError,
            http.client.HTTPException) as e:
        return {**row, "status": "error: " + str(getattr(e, "reason", e))[:80]}
    row["status"] = "ok"
    if urllib.parse.unquote(final).rstrip("/") != urllib.parse.unquote(url).rstrip("/"):
        row["final_url"] = final
        if urllib.parse.urlsplit(final).netloc.removeprefix("www.") != site:
            row["status"] = "ok, redirected off-site"
    return {**row, **analyse(raw, charset)}


# ── report ─────────────────────────────────────────────────────────────────

def report(rows):
    pct = lambda n, d: f"{100 * n // d}%" if d else "—"

    def line(label, rs, lang=""):
        got = [r for r in rs if r.get("status", "").startswith("ok")]
        rec = [r for r in got if r.get("recipe_source") not in (None, "none")]
        ing = sum(int(r.get("ingredients") or 0) for r in rec)
        qty = sum(int(r.get("ingredients_with_quantity") or 0) for r in rec)
        ara = sum(int(r.get("ingredients_arabic") or 0) for r in rec)
        print(f"{label[:26]:<26} {lang:>4} {len(rs):>5} {len(got):>7} {pct(len(rec), len(got)):>6} "
              f"{pct(sum(r['recipe_source'] == 'json-ld' for r in rec), len(got)):>7} "
              f"{ing:>5} {pct(qty, ing):>6} {pct(ara, ing):>6} "
              f"{sum(int(r.get('steps') or 0) for r in rec):>5} "
              f"{pct(sum(r.get('nutrition') == 'yes' for r in rec), len(rec)):>5}")

    def main_language(rs):
        langs = collections.Counter(r.get("language") or "?" for r in rs
                                    if r.get("status", "").startswith("ok"))
        if not langs:
            return "?"
        top = langs.most_common()
        return top[0][0] if len(top) == 1 else top[0][0] + "+"

    print(f"\n{'site':<26} {'lang':>4} {'pages':>5} {'fetched':>7} {'recipe':>6} {'json-ld':>7} "
          f"{'ingr.':>5} {'w/ qty':>6} {'arabic':>6} {'steps':>5} {'nutr.':>5}")
    by_site = collections.defaultdict(list)
    for r in rows:
        by_site[r["site"]].append(r)
    for site in sorted(by_site):
        line(site, by_site[site], main_language(by_site[site]))
    print("-" * 92)
    by_lang = collections.defaultdict(list)
    for r in rows:
        if r.get("status", "").startswith("ok"):
            by_lang[r.get("language") or "?"].append(r)
    for lang in sorted(by_lang, key=lambda l: ({"ar": 0, "en": 1, "fr": 2}.get(l, 3), l)):
        line(f"all {lang} pages", by_lang[lang], lang)
    line("ALL", rows)
    failed = [r for r in rows if not r.get("status", "").startswith("ok")]
    if failed:
        print(f"\nNot read ({len(failed)}):")
        for r in failed:
            print(f"  {r['status']:<20} {r['url']}")
    print("\nlang: the page's declared language, else the recipe's, else a guess from the "
          "ingredient lines; + means a site's pages are mixed. recipe and json-ld: share of "
          "fetched pages. w/ qty and arabic: share of ingredient lines. nutr.: share of "
          "recipes carrying nutrition.")


def main():
    ap = argparse.ArgumentParser(description="How many recipe pages publish schema.org "
                                 "Recipe data? Counts only; keeps no recipe text.")
    ap.add_argument("sources", nargs="*", help="URLs, or a file with one URL per line")
    ap.add_argument("--site", action="append", default=[],
                    help="sample recipe pages from this site's sitemap (repeatable)")
    ap.add_argument("--per-site", type=int, default=10,
                    help="pages to sample per --site (default 10)")
    ap.add_argument("--match", help="regex a sampled URL must match, instead of the "
                    "built-in guess at what a recipe URL looks like")
    ap.add_argument("--seed", type=int, default=12,
                    help="random seed for sampling, so a run can be repeated (default 12)")
    ap.add_argument("--save-urls", help="write the URLs actually checked to this file, "
                    "so the same sample can be re-run later")
    ap.add_argument("--csv", help="also write one row per URL to this CSV file")
    ap.add_argument("--verbose", action="store_true",
                    help="show each sitemap read while sampling")
    ap.add_argument("--delay", type=float, default=2.0,
                    help="seconds between requests to the same site (default 2)")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):      # Windows consoles default to cp1252
        stream.reconfigure(encoding="utf-8", errors="replace")
    global VERBOSE
    VERBOSE = a.verbose
    if not a.sources and not a.site:
        ap.error("give URLs, a URL file, or at least one --site")

    urls = []
    rng = random.Random(a.seed)
    for site in a.site:
        urls += sample_site(site, a.per_site, a.match, a.delay, rng)
    for s in a.sources:
        if re.match(r"https?://", s):
            urls.append(s)
        else:
            with open(s, encoding="utf-8") as fh:
                urls += [l.strip() for l in fh if l.strip() and not l.lstrip().startswith("#")]
    urls = list(dict.fromkeys(urls))             # drop duplicates, keep order
    if not urls:
        sys.exit("structured-data-check: no URLs to check.")
    if a.save_urls:
        with open(a.save_urls, "w", encoding="utf-8") as fh:
            fh.write(f"# structured-data-check sample, seed {a.seed}\n" + "\n".join(urls) + "\n")

    rows = []
    for n, url in enumerate(urls, 1):
        r = check(url, a.delay)
        rows.append(r)
        print(f"[{n}/{len(urls)}] {r['status']:<20} {r.get('recipe_source', ''):<9} "
              f"{r.get('ingredients', '')!s:>3} ingr. {url}", file=sys.stderr)

    report(rows)
    if a.csv:
        with open(a.csv, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, FIELDS, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        print(f"\nwritten to {a.csv}")


if __name__ == "__main__":
    main()
