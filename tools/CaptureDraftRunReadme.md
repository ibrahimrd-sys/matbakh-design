# capture-draft — how to do a real run

*Written 1 October 2026, before the first run against the live API.*

**Last updated:** 2026-10-01 — the fallback turned off (release 2026.10.01c).

This is the procedure for running `tools/capture-draft.py` against the real
Anthropic API: first once to prove it works, then as a routine. What the tool is,
and what it refuses to do, is in `ToolsReadme.md` § capture-draft.py. This file
says only how to run it.

**As of writing, it has been tested offline only** — page extraction, images,
the write guards, the error messages, and the request against a mocked API.
The first real run is the one below.

---

## 1. Once per machine

**Python and the SDK.** From any terminal:

    python3 --version             # 3.10 or newer
    pip install anthropic

On Windows, `python3` may be `python` or `py -3`; use whichever answers.

**An API key.**
1. Sign in to the Anthropic Console (`console.anthropic.com`) and create a key
   under **API keys**. Name it so it can be found and revoked later — for example
   *matbakh-capture-draft*.
2. **Set a monthly spend limit** for it under **Billing** or **Limits**. A few
   dollars covers hundreds of drafts. A limit means a mistake costs that much and
   no more.
3. Copy the key once, into your password manager — the vault's `06-credentials/`
   if that is where credentials live. Not into any file in this repository, not
   into a chat, not into a note.

**Never write the key into a file in this repository.** It is public, and a
published key is a key anyone can bill to you. If one is ever committed, revoke
it in the Console straight away — deleting the commit is not enough.

---

## 2. Each session: put the key in the environment

Set it for the current terminal only. When the terminal closes, it is gone.
The commands below prompt for the key, so it never lands in your shell
history.

**Git Bash:**

    read -s -p "Anthropic key: " ANTHROPIC_API_KEY && export ANTHROPIC_API_KEY && echo

**PowerShell:**

    $env:ANTHROPIC_API_KEY = Read-Host "Anthropic key" -MaskInput

Then run everything below from the `matbakh-design` folder, in the same
terminal.

---

## 3. The first run, step by step

Work through these in order. Each step proves one thing before the next one
spends money.

### Step 1 — a dry run, with no key needed

    python3 tools/capture-draft.py https://www.themealdb.com/meal/52771 --dry-run

**Expect:** the page text, ending in the line
`[schema.org Recipe data found: no]`, which proves fetching works. No API call is
made.

### Step 2 — a URL, for real

Make a folder for drafts **outside this repository and outside the vault's
`03-catalogue/`** — the tool refuses both. Where drafts live is not yet decided
(PM log, 1 Oct); until it is, something like `C:\Users\<you>\matbakh-drafts\`
will do.

    python3 tools/capture-draft.py https://www.themealdb.com/meal/52771 --format text --out C:/Users/<you>/matbakh-drafts/arrabiata.txt

**Expect, in about ten to thirty seconds,** a plain-text draft that opens with
`# UNREVIEWED MACHINE TRANSCRIPTION…`, then:

- **TITLE** *Spicy Arrabiata Penne*;
- **INGREDIENTS**, eight lines, quantities as the page gives them — `1 pound
  penne rigate`, `1/4 cup olive oil` …;
- **STEPS**, three, worded as on the page;
- **NOTES FOR THE CHEF**, which **should flag kosher salt** — the method uses it
  and the ingredient list does not. If the note is there, the model is reading
  the recipe rather than just copying lines.

### Step 3 — the same URL as JSON

    python3 tools/capture-draft.py https://www.themealdb.com/meal/52771

**Expect** the same content as JSON, with a `_draft` block carrying `warning`,
`source`, `captured`, `model` and `request_id`. Keep the `request_id` if
anything looks wrong; it is what Anthropic support asks for.

### Step 4 — an image

Photograph a page of a printed cookbook, or screenshot a recipe, and save it as
`.jpg` or `.png`:

    python3 tools/capture-draft.py C:/Users/<you>/Pictures/cookbook-page.jpg --format text

**Expect** the page's ingredients and method, with anything the camera blurred
or cut off listed under **NOTES FOR THE CHEF** rather than guessed.

### Step 5 — check the bill

In the Console under **Usage**, the three calls should come to a few cents.
If they cost much more than that, stop and look before running it routinely.

---

## 4. Checking a draft

The draft is a transcription, so check it against the source, not against how
the dish ought to be made.

| Check | Why |
|---|---|
| Every ingredient line in the source is in the draft, and nothing else is | The model is told never to add or complete. An extra line is a fault |
| Quantities and units are **as written** — `1 1/2 cups`, not `360 ml` | Conversion is the chef's job, done against the ingredient reference |
| Steps follow the source's division — not split, not merged | Splitting into pages and tiles is the chef's judgement under the authoring standard |
| Anything unreadable or inconsistent is in the notes, not filled in | A guessed quantity that looks real is worse than a gap |
| `found_recipe` is `false` when the page held no recipe | Redirects and video pages produce exactly this |

**A wrong draft is cheap: correct it by hand, or run it again.** What must never
happen is a draft treated as a recipe. It goes to a chef, who rewrites it to
`design/authoring-standard.md` in `recipe-editor.html`, and the result is
test-cooked before it goes anywhere near the catalogue.

---

## 5. When it fails

Every failure prints one line beginning `capture-draft:`.

| Message | What to do |
|---|---|
| `no credentials. Set ANTHROPIC_API_KEY…` | The key is not set in this terminal. Redo §2 |
| `the API rejected the credentials…` | The key is mistyped, revoked, or from another account. Check it in the Console |
| `rate limited. Try again in a minute.` | Wait a minute. If it keeps happening, the account's limits are low |
| `API error 4xx/5xx: …` | 5xx is Anthropic's side — retry later. 4xx with a spend-limit message: the limit from §1 was reached |
| `the API rejected the request: …` | Usually an image that is too large. Resize it to under about 5 MB and retry |
| `could not reach the API…` | No connection, or a proxy is in the way |
| `the model declined this source…` | The model declined it on safety grounds, and nothing was retried on another model (the tool has no fallback). Try a different source; if an ordinary recipe is being declined, keep the request and report it |
| `the response was cut off or unreadable…` | Rare. Retry once, and if it repeats, keep the `request_id` |
| `… returned HTTP 403` (or 404, 429) | The site blocks scripts. Screenshot the recipe and pass the image |
| warning: `… redirected to …` | The site sent you elsewhere — BBC Good Food sends Egypt to its regional homepage. Expect `found_recipe: false`; screenshot instead |
| warning: `the page has almost no text` | A TikTok, Instagram or YouTube page. Screenshot the caption |
| `the page is … characters, over the … limit` | Screenshot the recipe |
| `refusing to write into …` / `refusing a .yaml --out` | Working as intended. Pick a folder from §3 step 2 and a `.json` or `.txt` name |

---

## 6. After the first run

Record it in the PM log's §13 — the date, that the tool ran against the live
API, the cost of the three calls, and anything that did not match the
*Expect* lines above. Then, if it is to become routine, two open questions go to
Ibrahim:

- **where drafts live** — a standard folder outside `03-catalogue/`;
- **whether a draft is kept** after the recipe is authored. It is a third-party
  transcription, so the case for deleting it is its copyright, and the case for
  keeping it is provenance.

Until those are settled the tool stays outside every workflow, as it is now.
