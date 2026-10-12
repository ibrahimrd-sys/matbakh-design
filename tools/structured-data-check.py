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

import argparse, collections, csv, gzip, html.parser, json, random, re, sys, time
import xml.etree.ElementTree as ET
import urllib.error, urllib.parse, urllib.request, urllib.robotparser

UA = "Mozilla/5.0 (Matbakh structured-data-check; internal research tool)"
ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
# a quantity: Western or Arabic-Indic digits, or a vulgar fraction
QUANTITY = re.compile(r"[0-9٠-٩۰-۹¼-¾⅐-⅞]")
MAX_BYTES = 5_000_000

FIELDS = ["url", "site", "status", "final_url", "lang", "jsonld_blocks", "recipe_source",
          "name", "ingredients", "ingredients_with_quantity", "ingredients_arabic",
          "steps", "yield", "total_time", "nutrition", "image", "video"]


# ── parsing ────────────────────────────────────────────────────────────────

class _Page(html.parser.HTMLParser):
    """Collects JSON-LD blocks, the <html lang>, and microdata Recipe properties."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang, self.jsonld, self._ld = "", [], None
        self.micro = False                       # an itemtype=…/Recipe was seen
        self.micro_props = collections.Counter() # itemprop counts inside the page
        self._prop, self._buf = None, []
        self.micro_ingredients = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html" and a.get("lang"):
            self.lang = a["lang"]
        if tag == "script" and a.get("type", "").lower().split(";")[0].strip() == "application/ld+json":
            self._ld = []
        if re.search(r"schema\.org/Recipe\b", a.get("itemtype", ""), re.I):
            self.micro = True
        prop = a.get("itemprop")
        if prop:
            for p in prop.split():
                self.micro_props[p] += 1
            if "recipeIngredient" in prop.split() or "ingredients" in prop.split():
                self._prop, self._buf = "ingredient", []

    def handle_endtag(self, tag):
        if tag == "script" and self._ld is not None:
            self.jsonld.append("".join(self._ld))
            self._ld = None
        if self._prop == "ingredient" and tag in ("li", "span", "p", "div", "td"):
            self.micro_ingredients.append("".join(self._buf).strip())
            self._prop = None

    def handle_data(self, data):
        if self._ld is not None:
            self._ld.append(data)
        elif self._prop:
            self._buf.append(data)


def _is_recipe(node):
    t = node.get("@type")
    types = t if isinstance(t, list) else [t]
    return any(isinstance(x, str) and x.split("/")[-1].lower() == "recipe" for x in types)


def _recipes_in(node):
    """Every Recipe object in a JSON-LD value, through arrays and @graph."""
    out = []
    if isinstance(node, list):
        for n in node:
            out += _recipes_in(n)
    elif isinstance(node, dict):
        if _is_recipe(node):
            out.append(node)
        for key in ("@graph", "mainEntity", "mainEntityOfPage", "itemListElement", "item"):
            if key in node:
                out += _recipes_in(node[key])
    return out


def _flatten_steps(v):
    """recipeInstructions may be a string, a list of strings, HowToStep or HowToSection."""
    if isinstance(v, str):
        return [s for s in re.split(r"\n+", v) if s.strip()]
    if isinstance(v, dict):
        if "itemListElement" in v:
            return _flatten_steps(v["itemListElement"])
        return [v.get("text") or v.get("name") or ""]
    if isinstance(v, list):
        out = []
        for x in v:
            out += _flatten_steps(x)
        return [s for s in out if str(s).strip()]
    return []


def _as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def _yes(v):
    return "yes" if v not in (None, "", [], {}) else "no"


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
        return {**row, "recipe_source": "none"}
    row.update(ingredients=len(ings),
               ingredients_with_quantity=sum(1 for i in ings if QUANTITY.search(i)),
               ingredients_arabic=sum(1 for i in ings if ARABIC.search(i)))
    return row


# ── fetching, politely ─────────────────────────────────────────────────────

_robots, _last = {}, {}


def allowed(url):
    parts = urllib.parse.urlsplit(url)
    base = f"{parts.scheme}://{parts.netloc}"
    if base not in _robots:
        rp = urllib.robotparser.RobotFileParser(base + "/robots.txt")
        try:
            req = urllib.request.Request(base + "/robots.txt", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                rp.parse(r.read().decode("utf-8", errors="replace").splitlines())
        except urllib.error.HTTPError as e:
            # 4xx: no robots file, everything allowed; 5xx: be cautious, allow nothing
            rp.parse([] if e.code < 500 else ["User-agent: *", "Disallow: /"])
        except (urllib.error.URLError, TimeoutError, OSError):
            rp.parse([])
        _robots[base] = rp
    return _robots[base].can_fetch(UA, url)


def fetch(url, delay):
    site = urllib.parse.urlsplit(url).netloc
    wait = _last.get(site, 0) + delay - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    _last[site] = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html,application/xhtml+xml",
                                               "Accept-Language": "ar,en;q=0.5"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("page over 5 MB")
        return raw, r.headers.get_content_charset(), r.geturl()


# ── sampling recipe pages from a site's sitemap ────────────────────────────

# a path that names a recipe, in English or Arabic (وصفة / وصفات, also URL-encoded)
RECIPE_PATH = re.compile(r"recipe|recette|/r/|وصف|%D9%88%D8%B5%D9%81", re.I)
NOT_A_RECIPE = re.compile(r"/(tag|tags|category|categories|author|page|search|collection|"
                          r"collections|video|videos|wp-content|feed|amp)(/|$)|\.(jpe?g|png|webp|pdf)$", re.I)
MAX_SITEMAPS = 8          # child sitemaps read per site
MAX_SITEMAP_URLS = 20000  # URLs collected per site before sampling


def _get(url, delay):
    """Fetch a sitemap or robots-allowed resource; returns bytes, gunzipped if needed."""
    if not allowed(url):
        raise PermissionError("robots.txt disallows " + url)
    raw, _, _ = fetch(url, delay)
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw


def _locs(xml):
    """(kind, [loc]) for a sitemap index or a urlset, ignoring namespaces."""
    root = ET.fromstring(xml)
    kind = root.tag.rsplit("}", 1)[-1]
    return kind, [e.text.strip() for e in root.iter() if e.tag.rsplit("}", 1)[-1] == "loc" and e.text]


def sample_site(site, n, match, delay, rng):
    base = site if re.match(r"https?://", site) else "https://" + site
    base = base.rstrip("/")
    allowed(base + "/")                                   # loads robots.txt
    rp = _robots[f"{urllib.parse.urlsplit(base).scheme}://{urllib.parse.urlsplit(base).netloc}"]
    queue = list(rp.site_maps() or []) or [base + p for p in
                                           ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml")]
    seen, urls, read = set(), [], 0
    while queue and read < MAX_SITEMAPS and len(urls) < MAX_SITEMAP_URLS:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            kind, locs = _locs(_get(sm, delay))
        except (urllib.error.URLError, PermissionError, ET.ParseError, OSError, ValueError):
            continue
        read += 1
        if kind == "sitemapindex":
            # recipe- or post-named child sitemaps first; they are where the pages are
            locs.sort(key=lambda u: (not re.search(r"recipe|وصف|%D9%88%D8%B5%D9%81", u, re.I),
                                     not re.search(r"post", u, re.I)))
            queue = locs + queue
        else:
            urls += locs
    pattern = re.compile(match, re.I) if match else RECIPE_PATH
    host = urllib.parse.urlsplit(base).netloc.removeprefix("www.")
    pool = [u for u in dict.fromkeys(urls)
            if urllib.parse.urlsplit(u).netloc.removeprefix("www.") == host
            and pattern.search(u) and not NOT_A_RECIPE.search(urllib.parse.urlsplit(u).path)]
    picked = rng.sample(pool, min(n, len(pool)))
    print(f"{site}: {read} sitemap(s) read, {len(urls)} URLs, {len(pool)} look like recipes, "
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
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
        return {**row, "status": "error: " + str(getattr(e, "reason", e))[:80]}
    row["status"] = "ok"
    if final.rstrip("/") != url.rstrip("/"):
        row["final_url"] = final
        if urllib.parse.urlsplit(final).netloc.removeprefix("www.") != site:
            row["status"] = "ok, redirected off-site"
    return {**row, **analyse(raw, charset)}


# ── report ─────────────────────────────────────────────────────────────────

def report(rows):
    print(f"\n{'site':<28} {'pages':>5} {'fetched':>7} {'recipe':>6} {'json-ld':>7} "
          f"{'ingr.':>5} {'w/ qty':>6} {'arabic':>6} {'steps':>5} {'nutr.':>5}")
    by_site = collections.defaultdict(list)
    for r in rows:
        by_site[r["site"]].append(r)
    for site in sorted(by_site) + ["ALL"]:
        rs = rows if site == "ALL" else by_site[site]
        got = [r for r in rs if r.get("status", "").startswith("ok")]
        rec = [r for r in got if r.get("recipe_source") not in (None, "none")]
        ing = sum(int(r.get("ingredients") or 0) for r in rec)
        qty = sum(int(r.get("ingredients_with_quantity") or 0) for r in rec)
        ara = sum(int(r.get("ingredients_arabic") or 0) for r in rec)
        pct = lambda n, d: f"{100 * n // d}%" if d else "—"
        if site == "ALL":
            print("-" * 84)
        print(f"{site[:28]:<28} {len(rs):>5} {len(got):>7} {pct(len(rec), len(got)):>6} "
              f"{pct(sum(r['recipe_source'] == 'json-ld' for r in rec), len(got)):>7} "
              f"{ing:>5} {pct(qty, ing):>6} {pct(ara, ing):>6} "
              f"{sum(int(r.get('steps') or 0) for r in rec):>5} "
              f"{pct(sum(r.get('nutrition') == 'yes' for r in rec), len(rec)):>5}")
    failed = [r for r in rows if not r.get("status", "").startswith("ok")]
    if failed:
        print(f"\nNot read ({len(failed)}):")
        for r in failed:
            print(f"  {r['status']:<20} {r['url']}")
    print("\nrecipe and json-ld: share of fetched pages. w/ qty and arabic: share of "
          "ingredient lines. nutr.: share of recipes carrying nutrition.")


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
    ap.add_argument("--delay", type=float, default=2.0,
                    help="seconds between requests to the same site (default 2)")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):      # Windows consoles default to cp1252
        stream.reconfigure(encoding="utf-8", errors="replace")
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
