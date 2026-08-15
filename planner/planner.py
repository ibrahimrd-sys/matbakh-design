#!/usr/bin/env python3
"""
Matbakh — personal planning algorithm.

Two decisions supported:
  suggest_home()  — what to cook this week
  plan_event()    — a menu for N guests under a budget and a set of constraints

DESIGN STANCE
-------------
The app REMEMBERS. It does not PREDICT.

discovery-draft §4 rejected personalisation as "pretending I know you" and chose
subtraction: the user supplies the constraint, the app removes what fails it.
This module does not overturn that. It supplies a second input — what the cook
has actually done — and every output carries a one-sentence reason drawn from
that record.

The test applied throughout: **if a suggestion cannot be explained from the
user's own history in one sentence, it is not made.** No inferred taste vectors,
no collaborative filtering, no "customers like you". philosophy §3 forbids
presenting a computed estimate as a fact; an unexplainable recommendation is
exactly that.

PRIVACY
-------
All state is local. Nothing is transmitted, nothing is pooled across users,
nothing is published (philosophy §8). The algorithm is pure functions over a
local store, so it runs on-device with no server and no model. That is a
deliberate architectural choice, not a limitation: it means the feature works
offline in a kitchen, and it means there is no dataset to leak.

ENGINE-AGNOSTIC
---------------
Nothing here requires training. Scoring is arithmetic over counts and dates;
event planning is a small constrained search — a menu of five from a few hundred
candidates. Both run in milliseconds in any language. If a heavier engine is
chosen later it can replace `score_candidates` and `plan_event` without touching
the data model or the explanation contract.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
from itertools import combinations
from math import exp
from typing import Iterable


# ─────────────────────────────────────────────────────────── the local record

@dataclass
class CookEvent:
    """One cooking session. Written when the cook opens cook mode."""
    recipe_id: str
    on: date
    servings: int
    completed: bool                 # reached the serve station
    abandoned_at: int | None = None # step number, if they stopped
    event_id: str | None = None     # set when cooked as part of a recorded occasion


@dataclass
class ListEvent:
    """One shopping list. `had_already` is the cook unticking an item —
    the only honest signal about what is in their kitchen."""
    on: date
    had_already: list[str] = field(default_factory=list)
    bought: list[str] = field(default_factory=list)


@dataclass
class Profile:
    """Stated, never inferred. A cook declaring a nut allergy is a fact;
    the app deducing one from behaviour is a guess that could hurt someone."""
    household: int = 4
    excludes: set[str] = field(default_factory=set)   # diet classes
    dislikes: set[str] = field(default_factory=set)   # ingredient ids
    spice_max: int = 3


@dataclass
class Event:
    """One occasion the cook chose to record.

    Created EXPLICITLY — when a menu is accepted in the planner, or when the
    cook says they are planning something. Never inferred by grouping same-day
    cooking, because a big-batch Tuesday looks identical to a dinner party and
    guessing wrong corrupts the only signal that matters here.

    `name` is free text and is NEVER PARSED. "Amira's birthday" tells the cook
    who was there without the app holding names, matching guests, or storing
    personal data about third parties who never agreed to be in it. The app
    reads it back and does nothing else with it. This is the whole privacy
    design for guests, and it is deliberate: no structure means nothing to leak
    and nothing to get wrong.
    """
    id: str
    name: str
    on: date
    covers: int
    dishes: list[str]
    budget: float | None = None
    spent: float | None = None
    note: str = ""                  # private, like the name — never published


@dataclass
class Store:
    cooks: list[CookEvent] = field(default_factory=list)
    lists: list[ListEvent] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
    profile: Profile = field(default_factory=Profile)


# ────────────────────────────────────────────────────────────────── signals

def times_cooked(store: Store, rid: str) -> int:
    return sum(1 for c in store.cooks if c.recipe_id == rid and c.completed)


def times_abandoned(store: Store, rid: str) -> int:
    return sum(1 for c in store.cooks if c.recipe_id == rid and not c.completed)


def last_cooked(store: Store, rid: str) -> date | None:
    ds = [c.on for c in store.cooks if c.recipe_id == rid and c.completed]
    return max(ds) if ds else None


def affinity(store: Store, rid: str) -> float:
    """How much this cook likes this dish, from repeats alone.

    Repeat cooking is the strongest signal available and the only one that is
    unambiguous — a cook who makes something four times likes it. Abandonment
    is treated as evidence against, but weakly: a cook may abandon because the
    phone rang, and philosophy §8 already collects abandonment for editorial
    use rather than as a verdict.

    Range 0..1, saturating. Never negative: a dish is never suppressed
    permanently by one bad night.
    """
    made, quit = times_cooked(store, rid), times_abandoned(store, rid)
    if made == 0 and quit == 0:
        return 0.5                       # unknown, not disliked
    return max(0.05, min(1.0, (made - 0.35 * quit) / (made + quit + 1.5)))


def staleness(store: Store, rid: str, today: date, half_life_days: int = 28) -> float:
    """Whether the dish is due for a return.

    Frequency and recency pull in OPPOSITE directions and conflating them is
    the classic error. A dish cooked twelve times but not for six weeks is an
    excellent suggestion. The same dish cooked yesterday is a poor one.

    Returns 0 immediately after cooking, rising to 1 as the gap grows.
    A dish never cooked returns 1 — nothing to be tired of.
    """
    last = last_cooked(store, rid)
    if last is None:
        return 1.0
    days = max(0, (today - last).days)
    return 1.0 - exp(-days / half_life_days)


def pantry(store: Store, within_days: int = 21, today: date | None = None) -> set[str]:
    """Ingredients the cook unticked from recent lists — they had them.

    A weak signal used only as a tie-breaker. It is wrong often enough (things
    run out) that it must never gate a suggestion, only nudge one.
    """
    today = today or date.today()
    out: set[str] = set()
    for l in store.lists:
        if (today - l.on).days <= within_days:
            out.update(l.had_already)
    return out


# ──────────────────────────────────────────────────────────── hard filtering

def admissible(recipe: dict, store: Store) -> tuple[bool, str]:
    """Constraints that are never traded off. Returns (ok, reason_if_not).

    Dietary exclusion uses the DERIVED `contains` list, and a recipe whose
    dietary status is unknown is EXCLUDED, not assumed safe — the same
    discipline as philosophy §11. discovery-draft §9 requires the count of
    such exclusions be reported rather than hidden.
    """
    p = store.profile
    contains = recipe.get("contains")
    if contains is None:
        return False, "dietary data incomplete"
    if p.excludes & set(contains):
        return False, f"contains {', '.join(sorted(p.excludes & set(contains)))}"
    if p.dislikes & set(recipe.get("ingredients", [])):
        return False, "contains something you have excluded"
    if recipe.get("spice", 0) > p.spice_max:
        return False, "spicier than you asked for"
    return True, ""




# ───────────────────────────────────────────────────────────── saved menus

def menu_key(dishes: Iterable[str]) -> frozenset:
    """A menu's identity is its set of dishes. Order and date are incidental —
    the same four dishes served twice is the same menu served twice."""
    return frozenset(dishes)


def saved_menus(store: Store, today: date) -> list[dict]:
    """Menus the cook has actually served, most useful first.

    Ranked on the same two signals as recipes — how often it was served, and
    how long ago — because the argument is identical. A menu served three times
    and not for a year is a strong suggestion; the same menu served last month
    to the same crowd is a weak one.

    A TESTED MENU BEATS A COMPUTED ONE. The planner should offer these before
    it offers anything it assembled, because the cook already knows this
    combination works at this scale.
    """
    groups: dict[frozenset, list[Event]] = {}
    for e in store.events:
        groups.setdefault(menu_key(e.dishes), []).append(e)

    out = []
    for key, evs in groups.items():
        evs.sort(key=lambda e: e.on)
        last = evs[-1]
        days = (today - last.on).days
        out.append({
            "key": key,
            "dishes": last.dishes,
            "times_served": len(evs),
            "last_served": last.on,
            "days_ago": days,
            "occasions": [e.name for e in evs],      # shown back, never parsed
            "covers": last.covers,
            "spent": last.spent,
            "score": round(min(1.0, len(evs) / 3) * staleness_days(days), 3),
        })
    return sorted(out, key=lambda m: -m["score"])


def staleness_days(days: int, half_life_days: int = 120) -> float:
    """Menus go stale far more slowly than weeknight dishes — a host may
    entertain a handful of times a year, so a 28-day half-life would mark
    everything fresh. 120 days is roughly a season."""
    return 1.0 - exp(-days / half_life_days)


def recall_menu(store: Store, catalogue: list[dict], key: frozenset,
                covers: int) -> dict:
    """Re-open a saved menu at a new headcount.

    Rescales and reprices, and — importantly — RE-CHECKS every dish against the
    current profile. A menu that worked in March may contain something a guest
    now cannot eat, or a dish whose dietary data has since been completed and
    turns out to exclude it. Recalling a menu without re-checking would be the
    one place this design could actually harm someone.
    """
    by_id = {r["id"]: r for r in catalogue}
    evs = [e for e in store.events if menu_key(e.dishes) == key]
    if not evs:
        return {"ok": False, "reason": "no such menu"}
    evs.sort(key=lambda e: e.on)
    last = evs[-1]

    dishes, problems, missing = [], [], []
    for did in last.dishes:
        r = by_id.get(did)
        if r is None:
            missing.append(did)
            continue
        ok, why = admissible(r, store)
        if not ok:
            problems.append({"title": r["title"], "why": why})
            continue
        dishes.append({"id": did, "title": r["title"], "course": r.get("course"),
                       "cost": round(r["cost"] * covers, 2)})

    cost = sum(d["cost"] for d in dishes)
    return {
        "ok": not problems and not missing,
        "name": last.name,
        "served": len(evs),
        "last_served": last.on,
        "previously": {"covers": last.covers, "spent": last.spent},
        "now": {"covers": covers, "cost": round(cost, 2)},
        "change": (round(cost - last.spent, 2) if last.spent is not None else None),
        "dishes": dishes,
        "no_longer_suitable": problems,
        "no_longer_in_catalogue": missing,
    }

# ──────────────────────────────────────────────────── home / weekly planning

SLOT_EFFORT = {"weeknight": {"easy", "moderate"}, "weekend": {"easy", "moderate", "involved"}}


def suggest_home(catalogue: list[dict], store: Store, today: date,
                 slot: str = "weeknight", n: int = 5) -> dict:
    """What to cook, as TWO separate lists — and the separation is the point.

    Testing the first version showed the flaw plainly: with a large catalogue,
    every untried dish scores identically, so ranking them is arbitrary while
    looking authoritative. Worse, a favourite cooked last week was buried
    beneath a hundred dishes the cook has never seen.

    Mixing them requires a taste model the app does not have and philosophy §8
    denies it the data to build. So they are not mixed:

      DUE       dishes with a record, ranked affinity x staleness.
                Genuinely personal, fully explainable.
      UNTRIED   dishes with no record, filtered by constraint and pantry only,
                presented as a shelf rather than a ranking — which is exactly
                discovery-draft §4's subtraction model.

    The app says "you have made this six times, not since June" and "these
    twelve fit tonight and you have not tried them". It never says "we think
    you will like this."
    """
    have = pantry(store, today=today)
    allowed = SLOT_EFFORT.get(slot, SLOT_EFFORT["weeknight"])
    due, untried, withheld = [], [], 0

    for r in catalogue:
        ok, why_not = admissible(r, store)
        if not ok:
            if why_not == "dietary data incomplete":
                withheld += 1
            continue
        if r.get("effort") not in allowed:
            continue

        ings = set(r.get("ingredients", []))
        overlap = len(ings & have) / max(1, len(ings))
        made = times_cooked(store, r["id"])
        quit_ = times_abandoned(store, r["id"])
        last = last_cooked(store, r["id"])

        if made or quit_:
            a = affinity(store, r["id"])
            st = staleness(store, r["id"], today)
            gap = (today - last).days if last else None
            if made >= 3 and gap is not None:
                reason = f"you have made this {made} times, last {gap} days ago"
            elif made and gap is not None:
                reason = f"you made this {gap} days ago"
            else:
                step = next(c.abandoned_at for c in store.cooks
                            if c.recipe_id == r['id'] and not c.completed)
                reason = f"you stopped partway through last time, on step {step}"
            due.append({"id": r["id"], "title": r["title"],
                        "score": round(a * st * (1 + 0.25 * overlap), 3),
                        "reason": reason, "cost": r.get("cost", 0)})
        else:
            untried.append({"id": r["id"], "title": r["title"],
                            "pantry": round(overlap, 2), "cost": r.get("cost", 0),
                            "reason": (f"you already have {int(overlap*100)}% of the ingredients"
                                       if overlap >= 0.5 else "fits tonight")})

    due.sort(key=lambda x: -x["score"])
    untried.sort(key=lambda x: (-x["pantry"], x["cost"]))
    return {"due": due[:n], "untried": untried[:n],
            "untried_total": len(untried),
            "withheld_for_incomplete_data": withheld}


# ───────────────────────────────────────────────────────── event / hosting

def plan_event(catalogue: list[dict], store: Store, today: date,
               covers: int, budget: float, cuisine: str | None = None,
               offer_saved: bool = True,
               need_courses: tuple[str, ...] = ("main", "main", "side", "salad"),
               max_involved: int = 1, max_immediate: int = 2,
               top: int = 3) -> dict:
    """A menu under hard constraints, scored by the cook's own record.

    A small constrained selection, not an optimisation problem: a handful of
    dishes chosen from a few hundred. Exhaustive within each course, so the
    result is exact and reproducible — no heuristics to explain away.

    Two structural rules come from the tag vocabulary and exist because a host
    would not think to ask for them but would feel their absence:

      max_involved  — how many demanding dishes one cook can actually run
      max_immediate — how many dishes need serving the instant they are done

    Returns the menu, its cost, its reasons, and — per discovery-draft §9 —
    the count of dishes excluded for incomplete dietary data, so the shelf
    never lies about its own size.
    """
    # A TESTED MENU BEATS A COMPUTED ONE. Offer what the cook has actually
    # served before anything assembled — they already know it works at scale.
    recalled = []
    if offer_saved:
        for m in saved_menus(store, today):
            rec = recall_menu(store, catalogue, m["key"], covers)
            if not rec["ok"]:
                continue
            if rec["now"]["cost"] > budget:
                continue
            if cuisine:
                cs = {r.get("cuisine") for r in catalogue if r["id"] in m["dishes"]}
                if cuisine not in cs:
                    continue
            recalled.append({
                "kind": "served before",
                "name": rec["name"],
                "times_served": m["times_served"],
                "last_served": m["last_served"],
                "occasions": m["occasions"],
                "menu": rec["dishes"],
                "cost": rec["now"]["cost"],
                "headroom": round(budget - rec["now"]["cost"], 2),
                "reason": (f"you served this {m['times_served']} time"
                           f"{'s' if m['times_served'] > 1 else ''}, last "
                           f"{m['days_ago']} days ago" +
                           (f" for {m['covers']}" if m["covers"] != covers else "")),
            })

    pool, withheld = [], 0
    for r in catalogue:
        ok, why = admissible(r, store)
        if not ok:
            if why == "dietary data incomplete":
                withheld += 1
            continue
        if cuisine and r.get("cuisine") != cuisine:
            continue
        pool.append(r)

    by_course: dict[str, list[dict]] = {}
    for r in pool:
        by_course.setdefault(r.get("course", "main"), []).append(r)

    # candidates per course, best-first, capped so the search stays small
    ranked: dict[str, list[dict]] = {}
    for course, rs in by_course.items():
        ranked[course] = sorted(
            rs, key=lambda r: -(affinity(store, r["id"]) * staleness(store, r["id"], today))
        )[:8]

    need = list(need_courses)
    for c in set(need):
        if len(ranked.get(c, [])) < need.count(c):
            return {"ok": False,
                    "reason": f"not enough {c} dishes match — {len(ranked.get(c, []))} available, {need.count(c)} needed",
                    "withheld_for_incomplete_data": withheld}

    # build every admissible combination, then score
    def course_options(c: str, k: int):
        return combinations(ranked[c], k)

    counts: dict[str, int] = {}
    for c in need:
        counts[c] = counts.get(c, 0) + 1

    menus = []
    def recurse(courses: list[str], chosen: list[dict]):
        if not courses:
            menus.append(list(chosen))
            return
        c = courses[0]
        for combo in course_options(c, counts[c]):
            recurse(courses[1:], chosen + list(combo))
    recurse(sorted(counts), [])

    results = []
    for m in menus:
        cost = sum(r["cost"] * covers for r in m)
        if cost > budget:
            continue
        if sum(1 for r in m if r.get("effort") == "involved") > max_involved:
            continue
        if sum(1 for r in m if r.get("holds") == "serve_immediately") > max_immediate:
            continue

        known = [r for r in m if times_cooked(store, r["id"]) > 0]
        confidence = len(known) / len(m)
        variety = len({r.get("cuisine") for r in m}) / len(m)
        spend = cost / budget
        score = (0.5 * confidence + 0.3 * variety + 0.2 * spend
                 + 0.2 * sum(affinity(store, r["id"]) for r in m) / len(m))

        results.append({
            "menu": [{"id": r["id"], "title": r["title"], "course": r.get("course"),
                      "cost": round(r["cost"] * covers, 2),
                      "note": (f"you have made this {times_cooked(store, r['id'])} times"
                               if times_cooked(store, r["id"]) else "new to you")}
                     for r in m],
            "cost": round(cost, 2),
            "headroom": round(budget - cost, 2),
            "you_have_cooked": f"{len(known)} of {len(m)}",
            "score": round(score, 3),
        })

    results.sort(key=lambda x: -x["score"])
    if results or recalled:
        return {"ok": True,
                "served_before": recalled[:top],
                "options": results[:top],
                "withheld_for_incomplete_data": withheld, "reason": None}

    # NEVER RETURN ZERO SILENTLY (discovery-draft §9).
    # Name the binding constraint and show what would work, so the host relaxes
    # their own requirement rather than the app guessing which mattered least.
    diag = []
    for m in menus:
        cost = sum(r["cost"] * covers for r in m)
        inv = sum(1 for r in m if r.get("effort") == "involved")
        imm = sum(1 for r in m if r.get("holds") == "serve_immediately")
        diag.append((cost, inv, imm, m))
    if not diag:
        return {"ok": False, "binding": "structure",
                "reason": "no combination of courses is possible from what matches",
                "withheld_for_incomplete_data": withheld}

    diag.sort(key=lambda x: x[0])
    cheapest_cost, inv, imm, cheapest = diag[0]
    within_budget = [d for d in diag if d[0] <= budget]

    if not within_budget:
        over = cheapest_cost - budget
        per_head = cheapest_cost / covers
        return {
            "ok": False,
            "binding": "budget",
            "reason": (f"the cheapest {len(need)}-dish menu costs {cheapest_cost:.2f} "
                       f"for {covers} — {over:.2f} over, or {per_head:.2f} a head"),
            "nearest": [{"title": r["title"], "course": r.get("course"),
                         "cost": round(r["cost"] * covers, 2)} for r in cheapest],
            "budget_needed": round(cheapest_cost, 2),
            "or_drop_to": max(1, len(need) - 1),
            "withheld_for_incomplete_data": withheld,
        }

    blocked_effort = sum(1 for d in within_budget if d[1] > max_involved)
    blocked_holds = sum(1 for d in within_budget if d[2] > max_immediate)
    return {
        "ok": False,
        "binding": "effort" if blocked_effort >= blocked_holds else "timing",
        "reason": (f"{len(within_budget)} menus fit the budget but "
                   + (f"need more than {max_involved} demanding dish(es)"
                      if blocked_effort >= blocked_holds else
                      f"need more than {max_immediate} served the moment they are done")),
        "withheld_for_incomplete_data": withheld,
    }
