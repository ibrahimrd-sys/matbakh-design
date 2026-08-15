#!/usr/bin/env python3
"""
Matbakh planner — core logic tests (vocabulary-independent).

These assertions lock the behaviour that does NOT depend on the recipe tag
vocabulary (course / cuisine / effort / holds / spice level), which is still
unsettled (PM-07). They cover the parts that are safe to freeze now:

  - the two signals: affinity and staleness
  - the multiplicative combination that is the algorithm's central claim
  - menu identity (a menu is its set of dishes)
  - saved-menu ranking and recall re-checking
  - the hard-filter safety rule (unknown dietary data is excluded, not assumed)

Dietary classes (meat, dairy, ...) are treated as stable: they are derived from
the ingredient reference, not from the recipe-tag vocabulary PM-07 will settle.

Deliberately NOT tested here (would couple to PM-07 and cause rework):
  - suggest_home effort-slot filtering
  - plan_event course/cuisine/effort/holds scoring and the binding-constraint
    diagnostics

Run standalone (no dependencies):   python test_planner_core.py
Or under pytest:                     pytest test_planner_core.py
"""

from datetime import date
from math import exp, isclose

from planner import (
    CookEvent, Event, Profile, Store,
    times_cooked, times_abandoned, last_cooked,
    affinity, staleness, staleness_days,
    menu_key, saved_menus, recall_menu, admissible,
)

TODAY = date(2026, 8, 14)


# ───────────────────────────────────────────────────────── counting signals

def test_counts_only_completed_cooks():
    s = Store(cooks=[
        CookEvent("a", date(2026, 8, 1), 4, True),
        CookEvent("a", date(2026, 7, 1), 4, True),
        CookEvent("a", date(2026, 6, 1), 4, False, abandoned_at=3),
    ])
    assert times_cooked(s, "a") == 2
    assert times_abandoned(s, "a") == 1
    assert last_cooked(s, "a") == date(2026, 8, 1)   # newest completed
    assert last_cooked(s, "never") is None


# ─────────────────────────────────────────────────────────────── affinity

def test_affinity_unknown_is_neutral():
    # Never cooked, never abandoned -> 0.5 (unknown, not disliked).
    assert affinity(Store(), "x") == 0.5

def test_affinity_rises_with_repeats_and_saturates():
    def a(made):
        return affinity(Store(cooks=[CookEvent("x", TODAY, 4, True)] * made), "x")
    assert a(1) < a(4) < a(20)          # monotonic in repeats
    assert a(500) <= 1.0                # saturates, never exceeds 1

def test_affinity_never_collapses_to_zero_on_abandonment():
    # Abandonment counts against, but weakly and never below the 0.05 floor.
    s = Store(cooks=[CookEvent("x", TODAY, 4, False, abandoned_at=2)] * 5)
    assert affinity(s, "x") >= 0.05
    # And a repeatedly-made dish outranks a repeatedly-abandoned one.
    made = Store(cooks=[CookEvent("x", TODAY, 4, True)] * 3)
    quit = Store(cooks=[CookEvent("x", TODAY, 4, False, abandoned_at=2)] * 3)
    assert affinity(made, "x") > affinity(quit, "x")


# ─────────────────────────────────────────────────────────────── staleness

def test_staleness_never_cooked_is_one():
    assert staleness(Store(), "x", TODAY) == 1.0

def test_staleness_zero_just_cooked_and_rises():
    s = Store(cooks=[CookEvent("x", TODAY, 4, True)])
    assert staleness(s, "x", TODAY) == 0.0
    earlier = Store(cooks=[CookEvent("x", date(2026, 7, 1), 4, True)])
    later = Store(cooks=[CookEvent("x", date(2026, 8, 1), 4, True)])
    assert staleness(earlier, "x", TODAY) > staleness(later, "x", TODAY)

def test_staleness_half_life_shape():
    # At one 28-day half-life, staleness ~ 1 - e^-1 ~ 0.632.
    s = Store(cooks=[CookEvent("x", TODAY, 4, True)])
    # 28 days before today
    from datetime import timedelta
    s.cooks[0].on = TODAY - timedelta(days=28)
    assert isclose(staleness(s, "x", TODAY), 1 - exp(-1), abs_tol=1e-9)


# ───────────────────────── the central claim: multiplicative, not additive

def test_beloved_but_recent_scores_near_zero():
    """A dish cooked many times but only days ago must score low; the same dish
    left alone for months must score high. This is the whole reason the two
    signals are multiplied rather than added."""
    from datetime import timedelta
    beloved_recent = Store(cooks=[CookEvent("x", TODAY - timedelta(days=2), 4, True)] * 6)
    beloved_stale = Store(cooks=[CookEvent("x", TODAY - timedelta(days=90), 4, True)] * 6)

    recent = affinity(beloved_recent, "x") * staleness(beloved_recent, "x", TODAY)
    stale = affinity(beloved_stale, "x") * staleness(beloved_stale, "x", TODAY)

    assert recent < 0.15          # near zero despite high affinity
    assert stale > 0.5            # a strong suggestion
    assert recent < stale


# ────────────────────────────────────────────────────────── menu identity

def test_menu_key_is_the_set_of_dishes():
    assert menu_key(["a", "b", "c"]) == menu_key(["c", "b", "a"])   # order-free
    assert menu_key(["a", "b", "a"]) == menu_key(["a", "b"])        # dedup
    assert menu_key(["a", "b"]) != menu_key(["a", "b", "c"])


def test_staleness_days_120_day_half_life():
    assert staleness_days(0) == 0.0
    assert isclose(staleness_days(120), 1 - exp(-1), abs_tol=1e-9)
    assert staleness_days(300) > staleness_days(120)


# ────────────────────────────────────────────────────────── saved menus

def _store_with_events():
    return Store(events=[
        Event("e1", "Party A", date(2026, 3, 1), 12, ["x", "y", "z"], spent=50.0),
        Event("e2", "Party B", date(2026, 4, 1), 10, ["x", "y", "z"], spent=45.0),
        Event("e3", "Small",   date(2026, 7, 1),  6, ["p", "q"],      spent=20.0),
    ])

def test_saved_menus_group_by_dish_set():
    menus = saved_menus(_store_with_events(), TODAY)
    assert len(menus) == 2                                   # two distinct dish-sets
    top = menus[0]
    assert top["times_served"] == 2                          # x/y/z served twice
    assert top["dishes"] == ["x", "y", "z"]                  # most recent instance
    assert top["occasions"] == ["Party A", "Party B"]        # names shown back, in order
    # Served-more / longer-ago ranks above served-once / recent.
    assert menus[0]["times_served"] >= menus[1]["times_served"]


# ─────────────────────────────────────────────── recall re-checks profile

CAT = [
    {"id": "x", "title": "X", "course": "main",  "cost": 2.0, "contains": ["dairy"]},
    {"id": "y", "title": "Y", "course": "salad", "cost": 1.0, "contains": []},
    {"id": "z", "title": "Z", "course": "side",  "cost": 0.5, "contains": []},
]

def test_recall_rescales_and_reprices():
    store = _store_with_events()
    key = menu_key(["x", "y", "z"])
    r = recall_menu(store, CAT, key, covers=16)
    assert r["ok"] is True
    assert isclose(r["now"]["cost"], (2.0 + 1.0 + 0.5) * 16)     # 56.0
    assert r["now"]["covers"] == 16
    # change vs the last recorded spend (45.0)
    assert isclose(r["change"], 56.0 - 45.0)

def test_recall_drops_now_excluded_dishes():
    """The safety-critical path: a profile that now excludes a diet class must
    drop the offending dish on recall and say why."""
    store = _store_with_events()
    store.profile = Profile(excludes={"dairy"})
    key = menu_key(["x", "y", "z"])
    r = recall_menu(store, CAT, key, covers=12)
    assert r["ok"] is False
    dropped = {p["title"] for p in r["no_longer_suitable"]}
    assert dropped == {"X"}                                       # only the dairy dish
    assert len(r["dishes"]) == 2                                  # y and z survive
    assert isclose(r["now"]["cost"], (1.0 + 0.5) * 12)            # 18.0

def test_recall_flags_dish_missing_from_catalogue():
    store = Store(events=[
        Event("e", "Old", date(2026, 3, 1), 8, ["x", "gone"], spent=30.0),
    ])
    r = recall_menu(store, CAT, menu_key(["x", "gone"]), covers=8)
    assert r["ok"] is False
    assert "gone" in r["no_longer_in_catalogue"]


# ─────────────────────────────────────────── hard filter (safety rule)

def test_admissible_excludes_unknown_dietary_data():
    ok, why = admissible({"contains": None}, Store())
    assert ok is False and why == "dietary data incomplete"

def test_admissible_excludes_declared_diet_class():
    store = Store(profile=Profile(excludes={"dairy"}))
    ok, why = admissible({"contains": ["dairy"]}, store)
    assert ok is False and "dairy" in why

def test_admissible_passes_clean_recipe():
    ok, why = admissible({"contains": []}, Store())
    assert ok is True and why == ""


# ─────────────────────────────────────────────────── standalone runner

def _run_all():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {t.__name__}  — {e or 'assertion failed'}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  ERROR {t.__name__}  — {type(e).__name__}: {e}")
    print(f"\n{passed} passed, {failed} failed, {len(tests)} total")
    return failed == 0


if __name__ == "__main__":
    import sys
    print("═══ planner core tests (vocabulary-independent) ═══")
    sys.exit(0 if _run_all() else 1)
