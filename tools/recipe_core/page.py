"""Read a recipe page: fetch it politely and find its schema.org Recipe (JSON-LD, then
microdata). Moved from structured-data-check.py (import step 1); read_recipe() is new.

It keeps nothing and sends nothing anywhere except the page request. It respects
robots.txt and waits between requests to the same site."""

import collections, html.parser, http.client, json, re, time
import urllib.error, urllib.parse, urllib.request, urllib.robotparser

UA = "Mozilla/5.0 (Matbakh structured-data-check; internal research tool)"
ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
# a quantity: Western or Arabic-Indic digits, or a vulgar fraction
QUANTITY = re.compile(r"[0-9٠-٩۰-۹¼-¾⅐-⅞]")
MAX_BYTES = 5_000_000
# French cooking words, for pages that do not declare their language
FRENCH = re.compile(r"\b(c\.? ?à ?(soupe|café|s|c)|cuill[eè]res?|pinc[ée]es?|gousses?|beurre|farine|"
                    r"sucre|sel|poivre|huile|oignons?|œufs?|crème|lait|eau)\b", re.I)


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


def _language(html_lang, in_language, ings):
    """ar / en / fr / another code, or ? — the page's declaration first, then the
    recipe's inLanguage, then a guess from the ingredient lines."""
    for declared in (html_lang, in_language if isinstance(in_language, str) else ""):
        code = declared.strip().lower()[:2]
        if code.isalpha() and len(code) == 2:
            return code
    if not ings:
        return "?"
    if sum(1 for i in ings if ARABIC.search(i)) * 2 > len(ings):
        return "ar"
    if sum(1 for i in ings if FRENCH.search(i)) * 10 > len(ings) * 3:
        return "fr"
    return "en"


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


def _encode(url):
    """Percent-encode spaces and non-ASCII letters (Arabic slugs), keeping existing %XX escapes."""
    p = urllib.parse.urlsplit(url.strip())
    safe = "/%:@!$&'()*+,;=-._~"
    return urllib.parse.urlunsplit((p.scheme, p.netloc.encode("idna").decode("ascii"),
                                    urllib.parse.quote(p.path, safe=safe),
                                    urllib.parse.quote(p.query, safe=safe + "?"), ""))


def fetch(url, delay, timeout=30):
    url = _encode(url)
    site = urllib.parse.urlsplit(url).netloc
    wait = _last.get(site, 0) + delay - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    _last[site] = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html,application/xhtml+xml",
                                               "Accept-Language": "ar,en;q=0.5"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("page over 5 MB")
        return raw, r.headers.get_content_charset(), r.geturl()


# ── reading one recipe: what the import prototype and capture-draft use ────
# Added 20 October 2026 (RecipeCoreDesign.md). Everything above is the step 1
# check's code, unchanged.

import html as _html


class PageError(Exception):
    """The page could not be read as a recipe. The message says why, in plain words."""


def _clean(s):
    """Text as a cook would read it. Some sites encode their recipe data twice, so
    an ingredient arrives as `8&quot; pita` or `za&#39;atar`: decode it, drop any
    tags, and collapse the spaces. Nothing else is changed."""
    s = _html.unescape(_html.unescape(str(s)))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\[([^\]]+)\]\((?:https?://|/)[^)]*\)", r"\1", s)   # a markdown link: keep its words
    return re.sub(r"\s+", " ", s).strip()


def _author(v):
    for a in _as_list(v):
        if isinstance(a, dict) and a.get("name"):
            return _clean(a["name"])
        if isinstance(a, str) and a.strip():
            return _clean(a)
    return ""


def _image(v):
    """The recipe's image address, as published — never downloaded here."""
    for a in _as_list(v):
        if isinstance(a, dict):
            a = a.get("url") or a.get("contentUrl") or ""
        if isinstance(a, str) and a.startswith(("http://", "https://")):
            return a
    return ""


def _servings(v):
    """recipeYield as written, and the first whole number in it (or None)."""
    texts = [_clean(x) for x in _as_list(v) if str(x).strip()]
    for t in texts:
        m = re.search(r"\d+", t.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")))
        if m and int(m.group()) > 0:
            return (texts[0] if texts else ""), int(m.group())
    return (texts[0] if texts else ""), None


def parse_html(raw, charset=None):
    """The page's own recipe, or None when it publishes none. Never a guess."""
    page = _Page()
    page.feed(raw.decode(charset or "utf-8", errors="replace"))
    recipes = []
    for blob in page.jsonld:
        try:
            recipes += _recipes_in(json.loads(blob.strip()))
        except json.JSONDecodeError:
            pass
    if recipes:
        r = recipes[0]
        ings = [_clean(x) for x in _as_list(r.get("recipeIngredient") or r.get("ingredients"))]
        steps = [_clean(s) for s in _flatten_steps(r.get("recipeInstructions"))]
        yield_text, servings = _servings(r.get("recipeYield"))
        rec = dict(source="json-ld", title=_clean(r.get("name") or ""), author=_author(r.get("author")),
                   yield_text=yield_text, servings=servings, image=_image(r.get("image")),
                   language=_language(page.lang, r.get("inLanguage"), ings))
    elif page.micro:
        ings, steps = [_clean(x) for x in page.micro_ingredients], []
        rec = dict(source="microdata", title="", author="", yield_text="", servings=None, image="",
                   language=_language(page.lang, None, ings))
    else:
        return None
    rec.update(ingredients=[i for i in ings if i], steps=[s for s in steps if s])
    return rec


def read_recipe(url, delay=2.0):
    """Fetch a page and read its recipe. Raises PageError with a plain reason when
    it cannot: robots.txt refuses, the page is missing or unreachable, or the page
    publishes no recipe data."""
    try:
        if not allowed(url):
            raise PageError("the site's robots.txt asks tools not to read this page")
        raw, charset, final = fetch(url, delay)
    except urllib.error.HTTPError as e:
        raise PageError("the page does not exist (HTTP 404)" if e.code == 404
                        else f"the site refused the page (HTTP {e.code})") from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException) as e:
        raise PageError(f"the page could not be reached: {getattr(e, 'reason', e)}") from None
    rec = parse_html(raw, charset)
    if rec is None:
        raise PageError("this page has no recipe Matbakh can read")
    rec.update(url=url, final_url=final,
               redirected=urllib.parse.unquote(final).rstrip("/") != urllib.parse.unquote(url).rstrip("/"))
    return rec
