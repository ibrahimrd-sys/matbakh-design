#!/usr/bin/env python3
"""
Matbakh planner — tag-coupled tests.

The assertions test_planner_core.py deferred until the tag vocabulary closed
(PM-07, philosophy §26, 24 Sept 2026; §32 added `lamb`). They lock:

  - the vocabulary itself, so a drift from §26/§32 fails loudly
  - incomplete or out-of-vocabulary tags are shown, marked and counted, never
    guessed (§54): a dish with no course is set aside where the host sees it;
    unknown effort or holds counts against the limits; an unrecorded cuisine or
    protein is outside the preference; unknown spice passes every ceiling (§55)
  - `course: component` never reaches a suggestion
  - suggest_home's effort slots
  - plan_event's course grouping, the cuisine and protein preferences
    (§52, §53: they order, never remove), the two
    structural limits (`effort: involved`, `holds: serve_immediately`), and the
    binding-constraint diagnostics
  - `main_protein` is never read as dietary data

Run standalone (no dependencies):   python test_planner_tags.py
Or under pytest:                     pytest test_planner_tags.py
"""

from datetime import date, timedelta

from planner import (
    CUISINES, COURSES, MAIN_PROTEINS, SPICE_LEVELS, EFFORTS, HOLDS,
    CookEvent, Event, Profile, Store,
    missing_tags, admissible, suggest_home, plan_event,
)

TODAY = date(2026, 10, 30)


def dish(id, course="main", cuisine="egyptian", main_protein="vegetarian",
         spice=0, effort="easy", holds="warm", cost=1.0, contains=(), **extra):
    r = dict(id=id, title=id.title(), course=course, cuisine=cuisine,
             main_protein=main_protein, spice=spice, effort=effort, holds=holds,
             cost=cost, contains=list(contains), ingredients=[])
    r.update(extra)
    return r


def _raises(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except ValueError:
        return True
    return False


# ─────────────────────────────────────────────── the vocabulary, as filed

def test_vocabulary_matches_section_26_and_32():
    assert CUISINES == {
        "egyptian", "levantine", "gulf", "north_african", "turkish", "persian",
        "italian", "french", "chinese", "indian", "american", "mexican",
        "japanese", "greek", "spanish", "thai", "latin_american", "eastern_european"}
    assert COURSES == {"main", "side", "salad", "soup", "bread", "sauce", "dip",
                       "pickle", "dessert", "breakfast", "drink", "component"}
    assert MAIN_PROTEINS == {"beef", "lamb", "poultry", "seafood", "pork",
                             "vegetarian", "mixed", "none"}          # §32: eight
    assert SPICE_LEVELS == {0, 1, 2, 3}
    assert EFFORTS == {"easy", "moderate", "involved"}
    assert HOLDS == {"serve_immediately", "warm", "room", "cold", "better_next_day"}


# ─────────────────────────────────── incomplete tags: shown, marked, counted

def test_missing_tags_is_empty_for_a_fully_tagged_dish():
    assert missing_tags(dish("a")) == []

def test_missing_tags_names_every_missing_or_unknown_field():
    r = dish("a", effort="hard")             # not in the vocabulary
    del r["main_protein"]                    # missing
    assert set(missing_tags(r)) == {"main_protein", "effort"}

def test_untagged_dish_is_shown_marked_and_counted():
    r = dish("plain")
    del r["cuisine"], r["holds"]
    out = suggest_home([r, dish("ok")], Store(), TODAY)
    assert out["shown_with_incomplete_tags"] == 1
    shown = {s["id"]: s["tags_missing"] for s in out["untried"]}
    assert shown == {"plain": ["cuisine", "holds"], "ok": []}

def test_unknown_effort_is_shown_in_every_slot():
    r = dish("unsure")
    del r["effort"]
    for slot in ("weeknight", "weekend"):
        out = suggest_home([r], Store(), TODAY, slot=slot)
        assert [s["id"] for s in out["untried"]] == ["unsure"]

def test_dish_without_a_course_is_set_aside_not_filed_as_a_main():
    r = dish("drinkish")
    del r["course"]                          # the August code filed this as a main
    ev = plan_event([r, dish("m1"), dish("m2")], Store(), TODAY, covers=4,
                    budget=100, need_courses=("main", "main"))
    assert all(d["id"] != "drinkish" for o in ev["options"] for d in o["menu"])
    assert ev["no_course_to_place"] == [
        {"id": "drinkish", "title": "Drinkish", "tags_missing": ["course"]}]
    assert ev["shown_with_incomplete_tags"] == 1

def test_dish_with_other_tags_missing_still_joins_a_menu_and_is_marked():
    r = dish("m2")
    del r["main_protein"]
    ev = plan_event([dish("m1"), r], Store(), TODAY, covers=4, budget=100,
                    need_courses=("main", "main"))
    marks = {d["id"]: d["tags_missing"] for d in ev["options"][0]["menu"]}
    assert marks == {"m1": [], "m2": ["main_protein"]}

def test_unknown_effort_and_holds_count_against_the_limits():
    a, b = dish("a", effort="involved"), dish("b")
    del b["effort"]
    ev = plan_event([a, b], Store(), TODAY, covers=4, budget=100,
                    need_courses=("main", "main"), max_involved=1)
    assert ev["ok"] is False and ev["binding"] == "effort"
    c, d = dish("c", holds="serve_immediately"), dish("d")
    del d["holds"]
    ev = plan_event([c, d], Store(), TODAY, covers=4, budget=100,
                    need_courses=("main", "main"), max_immediate=1)
    assert ev["ok"] is False and ev["binding"] == "timing"

def test_unrecorded_cuisine_or_protein_is_outside_the_preference():
    r = dish("r")
    del r["cuisine"], r["main_protein"]
    ev = plan_event([r, dish("e")], Store(), TODAY, covers=4, budget=100, top=10,
                    prefer_cuisines={"egyptian"}, prefer_proteins={"vegetarian"},
                    need_courses=("main",))
    assert [o["menu"][0]["id"] for o in ev["options"]] == ["e", "r"]
    assert ev["options"][1]["outside_preference"] == [
        "R (cuisine not recorded, protein not recorded)"]

def test_unknown_spice_is_shown_to_every_cook_and_marked():
    r = dish("a")
    del r["spice"]
    for ceiling in SPICE_LEVELS:
        store = Store(profile=Profile(spice_max=ceiling))
        assert admissible(r, store)[0] is True
        out = suggest_home([r], store, TODAY)
        assert [(s["id"], s["tags_missing"]) for s in out["untried"]] == [("a", ["spice"])]
    # A recorded level above the ceiling is still excluded.
    assert admissible(dish("hot", spice=3), Store(profile=Profile(spice_max=1)))[0] is False


# ─────────────────────────────────────────────── components never suggested

def test_component_is_never_suggested_and_not_counted_as_withheld():
    cat = [dish("stock", course="component"), dish("soup", course="soup")]
    out = suggest_home(cat, Store(), TODAY)
    assert [s["id"] for s in out["untried"]] == ["soup"]
    assert out["shown_with_incomplete_tags"] == 0        # by design, not a gap

def test_component_cannot_be_requested_as_a_course():
    assert _raises(plan_event, [], Store(), TODAY, covers=4, budget=10,
                       need_courses=("main", "component"))


# ──────────────────────────────────────────────────── suggest_home slots

def test_weeknight_excludes_involved_weekend_includes_it():
    cat = [dish("quick", effort="easy"), dish("project", effort="involved")]
    week = suggest_home(cat, Store(), TODAY, slot="weeknight")
    end = suggest_home(cat, Store(), TODAY, slot="weekend")
    assert {s["id"] for s in week["untried"]} == {"quick"}
    assert {s["id"] for s in end["untried"]} == {"quick", "project"}


# ─────────────────────────────────────────────────────────── plan_event

def test_menu_takes_dishes_from_the_courses_asked_for():
    cat = [dish("m1"), dish("m2"), dish("s1", course="side"),
           dish("sal", course="salad"), dish("d1", course="dessert")]
    ev = plan_event(cat, Store(), TODAY, covers=4, budget=100,
                    need_courses=("main", "side", "salad"))
    assert ev["ok"]
    for o in ev["options"]:
        assert sorted(d["course"] for d in o["menu"]) == ["main", "salad", "side"]

def test_cuisine_preference_orders_and_never_removes():
    cat = [dish("e1"), dish("e2"), dish("l1", cuisine="levantine")]
    ev = plan_event(cat, Store(), TODAY, covers=4, budget=100, top=10,
                    prefer_cuisines={"levantine"}, need_courses=("main",))
    assert [d["id"] for d in ev["options"][0]["menu"]] == ["l1"]
    assert ev["options"][0]["outside_preference"] == []
    # The Egyptian dishes are still offered, below, and named as outside it.
    assert {d["id"] for o in ev["options"] for d in o["menu"]} == {"e1", "e2", "l1"}
    assert ev["options"][1]["outside_preference"] in (["E1 (egyptian)"], ["E2 (egyptian)"])
    assert _raises(plan_event, cat, Store(), TODAY, covers=4, budget=100,
                   prefer_cuisines={"lebanese"}, need_courses=("main",))

def test_cuisine_and_protein_misses_count_once_per_dish():
    # §13's brief: Mexican, beef and chicken preferred over seafood.
    cat = [dish("tacos", cuisine="mexican", main_protein="beef"),
           dish("ceviche", cuisine="mexican", main_protein="seafood"),
           dish("sayyadeya", cuisine="egyptian", main_protein="seafood")]
    ev = plan_event(cat, Store(), TODAY, covers=4, budget=100, top=10,
                    prefer_cuisines={"mexican"}, prefer_proteins={"beef", "poultry"},
                    need_courses=("main",))
    by_dish = {o["menu"][0]["id"]: o["outside_preference"] for o in ev["options"]}
    assert by_dish == {"tacos": [], "ceviche": ["Ceviche (seafood)"],
                       "sayyadeya": ["Sayyadeya (egyptian, seafood)"]}
    assert ev["options"][0]["menu"][0]["id"] == "tacos"

def test_protein_preference_orders_and_never_removes():
    # §13's brief: beef and chicken preferred over seafood.
    cat = [dish("kofta", main_protein="beef"), dish("farakh", main_protein="poultry"),
           dish("samak", main_protein="seafood"), dish("mansaf", main_protein="lamb")]
    ev = plan_event(cat, Store(), TODAY, covers=4, budget=100, top=10,
                    prefer_proteins={"beef", "poultry"}, need_courses=("main", "main"))
    assert ev["ok"]
    first = ev["options"][0]
    assert {d["id"] for d in first["menu"]} == {"kofta", "farakh"}
    assert first["outside_preference"] == []
    # Seafood and lamb are still offered, below, and named as outside it.
    offered = {d["id"] for o in ev["options"] for d in o["menu"]}
    assert {"samak", "mansaf"} <= offered
    misses = [len(o["outside_preference"]) for o in ev["options"]]
    assert misses == sorted(misses)
    assert any("Samak (seafood)" in o["outside_preference"] for o in ev["options"])
    assert _raises(plan_event, cat, Store(), TODAY, covers=4, budget=100,
                   prefer_proteins={"chicken"}, need_courses=("main",))

def test_protein_preference_still_returns_a_menu_when_nothing_matches_it():
    cat = [dish("samak", main_protein="seafood")]
    ev = plan_event(cat, Store(), TODAY, covers=4, budget=100,
                    prefer_proteins={"beef"}, need_courses=("main",))
    assert ev["ok"]
    assert ev["options"][0]["outside_preference"] == ["Samak (seafood)"]

def test_protein_preference_keeps_preferred_dishes_through_the_candidate_cap():
    # Nine well-loved seafood mains and one untried beef main: the per-course
    # cap of eight must not cut the beef dish the host asked for.
    fish = [dish(f"f{i}", main_protein="seafood") for i in range(9)]
    store = Store(cooks=[CookEvent(f"f{i}", TODAY - timedelta(days=90), 4, True)
                         for i in range(9)] * 3)
    cat = fish + [dish("kofta", main_protein="beef")]
    ev = plan_event(cat, store, TODAY, covers=4, budget=100,
                    prefer_proteins={"beef"}, need_courses=("main",))
    assert [d["id"] for d in ev["options"][0]["menu"]] == ["kofta"]

def test_protein_preference_orders_saved_menus_without_dropping_them():
    cat = [dish("samak", main_protein="seafood"), dish("kofta", main_protein="beef")]
    store = Store(events=[
        Event("e1", "Fish night", date(2026, 3, 1), 4, ["samak"], spent=4.0),
        Event("e2", "Fish night", date(2026, 4, 1), 4, ["samak"], spent=4.0),
        Event("e3", "Kofta night", date(2026, 10, 1), 4, ["kofta"], spent=4.0),
    ])
    plain = plan_event(cat, store, TODAY, covers=4, budget=100, need_courses=("main",))
    assert [m["name"] for m in plain["served_before"]] == ["Fish night", "Kofta night"]
    pref = plan_event(cat, store, TODAY, covers=4, budget=100,
                      prefer_proteins={"beef"}, need_courses=("main",))
    assert [m["name"] for m in pref["served_before"]] == ["Kofta night", "Fish night"]
    assert pref["served_before"][1]["outside_preference"] == ["Samak (seafood)"]

def test_main_protein_is_never_read_as_diet():
    # A soup whose claim is `vegetarian` but whose derived `contains` says
    # poultry (chicken stock) must still be excluded for a no-poultry guest.
    soup = dish("shorba", course="soup", main_protein="vegetarian", contains=["poultry"])
    store = Store(profile=Profile(excludes={"poultry"}))
    assert admissible(soup, store)[0] is False
    # And a seafood claim does not exclude a dish for a no-fish guest by itself;
    # `contains` is what decides.
    odd = dish("odd", main_protein="seafood", contains=[])
    assert admissible(odd, Store(profile=Profile(excludes={"fish"})))[0] is True

def test_at_most_max_involved_demanding_dishes():
    cat = [dish("a", effort="involved"), dish("b", effort="involved"), dish("c")]
    ev = plan_event(cat, Store(), TODAY, covers=4, budget=100,
                    need_courses=("main", "main"), max_involved=1)
    for o in ev["options"]:
        assert {d["id"] for d in o["menu"]} != {"a", "b"}

def test_at_most_max_immediate_serve_at_once_dishes():
    cat = [dish("a", holds="serve_immediately"), dish("b", holds="serve_immediately"),
           dish("c", holds="better_next_day")]
    ev = plan_event(cat, Store(), TODAY, covers=4, budget=100,
                    need_courses=("main", "main"), max_immediate=1)
    for o in ev["options"]:
        assert sum(1 for d in o["menu"] if d["id"] in {"a", "b"}) <= 1


# ─────────────────────────────────────── never return zero silently

def test_binding_budget_names_the_cheapest_menu():
    cat = [dish("m1", cost=2.0), dish("m2", cost=3.0)]
    ev = plan_event(cat, Store(), TODAY, covers=10, budget=10,
                    need_courses=("main",), offer_saved=False)
    assert ev["ok"] is False and ev["binding"] == "budget"
    assert ev["budget_needed"] == 20.0
    assert [d["title"] for d in ev["nearest"]] == ["M1"]

def test_binding_effort():
    cat = [dish("a", effort="involved"), dish("b", effort="involved")]
    ev = plan_event(cat, Store(), TODAY, covers=4, budget=100,
                    need_courses=("main", "main"), max_involved=1)
    assert ev["ok"] is False and ev["binding"] == "effort"

def test_binding_timing():
    cat = [dish("a", holds="serve_immediately"), dish("b", holds="serve_immediately")]
    ev = plan_event(cat, Store(), TODAY, covers=4, budget=100,
                    need_courses=("main", "main"), max_immediate=1)
    assert ev["ok"] is False and ev["binding"] == "timing"

def test_not_enough_dishes_in_a_course_says_which():
    ev = plan_event([dish("m1")], Store(), TODAY, covers=4, budget=100,
                    need_courses=("main", "salad"))
    assert ev["ok"] is False and "salad" in ev["reason"]
    assert ev["shown_with_incomplete_tags"] == 0


# ─────────────────────────────────────────── the record still ranks first

def test_cooked_dish_ranks_in_due_and_untried_stays_a_shelf():
    store = Store(cooks=[CookEvent("fav", TODAY - timedelta(days=60), 4, True)] * 4)
    out = suggest_home([dish("fav"), dish("new")], store, TODAY)
    assert [s["id"] for s in out["due"]] == ["fav"]
    assert [s["id"] for s in out["untried"]] == ["new"]


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
    print("═══ planner tag-coupled tests ═══")
    sys.exit(0 if _run_all() else 1)
