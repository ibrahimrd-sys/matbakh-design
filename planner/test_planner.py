from datetime import date, timedelta
from planner import *

TODAY = date(2026, 8, 13)

CAT = [
 dict(id="molokhia", title="Molokhia bil farakh", course="main", cuisine="egyptian",
      effort="moderate", holds="warm", spice=1, cost=2.10,
      contains=["meat","poultry","dairy"], ingredients=["chicken_whole","molokhia_frozen","ghee","garlic"]),
 dict(id="koshari", title="Koshari", course="main", cuisine="egyptian",
      effort="involved", holds="warm", spice=1, cost=0.85,
      contains=["gluten"], ingredients=["rice","lentils_raw","pasta","onion"]),
 dict(id="mahshi", title="Mahshi", course="main", cuisine="egyptian",
      effort="involved", holds="better_next_day", spice=0, cost=1.40,
      contains=[], ingredients=["rice","onion","tomato_paste"]),
 dict(id="fattah", title="Fattah", course="main", cuisine="egyptian",
      effort="moderate", holds="serve_immediately", spice=0, cost=2.60,
      contains=["meat","gluten","dairy"], ingredients=["beef","rice","ghee","garlic"]),
 dict(id="samak", title="Sayyadeya", course="main", cuisine="egyptian",
      effort="moderate", holds="warm", spice=1, cost=3.10,
      contains=["fish"], ingredients=["fish_filet","rice","onion"]),
 dict(id="tagine", title="Vegetable tagine", course="main", cuisine="north_african",
      effort="easy", holds="warm", spice=2, cost=1.20,
      contains=[], ingredients=["onion","carrot","chickpea","tomato_paste"]),
 dict(id="salata", title="Baladi salad", course="salad", cuisine="egyptian",
      effort="easy", holds="cold", spice=0, cost=0.55,
      contains=[], ingredients=["tomato","cucumber","onion","lemon"]),
 dict(id="tabbouleh", title="Tabbouleh", course="salad", cuisine="levantine",
      effort="easy", holds="cold", spice=0, cost=0.70,
      contains=["gluten"], ingredients=["bulgur","tomato","lemon"]),
 dict(id="rocket", title="Rocket and lemon", course="salad", cuisine="egyptian",
      effort="easy", holds="cold", spice=0, cost=0.45,
      contains=[], ingredients=["lemon","olive_oil"]),
 dict(id="rice_verm", title="Rice with vermicelli", course="side", cuisine="egyptian",
      effort="easy", holds="warm", spice=0, cost=0.40,
      contains=["gluten"], ingredients=["rice","vermicelli","ghee"]),
 dict(id="bamia", title="Bamia", course="side", cuisine="egyptian",
      effort="easy", holds="warm", spice=1, cost=0.95,
      contains=["meat"], ingredients=["okra","tomato_paste","onion"]),
 dict(id="baba", title="Baba ghanoush", course="dip", cuisine="levantine",
      effort="easy", holds="room", spice=0, cost=0.60,
      contains=["sesame"], ingredients=["eggplant","sesame_paste","lemon"]),
 dict(id="mystery", title="Unlabelled dish", course="main", cuisine="egyptian",
      effort="easy", holds="warm", spice=0, cost=1.00,
      contains=None, ingredients=["onion"]),   # diet unknown — must be excluded
]

def d(n): return TODAY - timedelta(days=n)

store = Store(profile=Profile(household=4, excludes=set(), spice_max=3))
# a plausible year of cooking: molokhia is a staple, koshari tried once and abandoned
for n in (7, 34, 61, 96, 130, 165):  store.cooks.append(CookEvent("molokhia", d(n), 4, True))
for n in (12, 40, 75):               store.cooks.append(CookEvent("rice_verm", d(n), 4, True))
for n in (21, 55):                   store.cooks.append(CookEvent("salata", d(n), 4, True))
store.cooks.append(CookEvent("koshari", d(48), 4, False, abandoned_at=5))
store.cooks.append(CookEvent("samak", d(88), 4, True))
store.cooks.append(CookEvent("bamia", d(3), 4, True))          # cooked three days ago
store.lists.append(ListEvent(d(5), had_already=["rice","onion","ghee","lemon","garlic"]))

print("═══ SIGNALS ═══")
for rid in ("molokhia","bamia","koshari","tagine","samak"):
    print(f"  {rid:<10} affinity {affinity(store,rid):.2f}  staleness {staleness(store,rid,TODAY):.2f}"
          f"  made {times_cooked(store,rid)}  quit {times_abandoned(store,rid)}")

for slot in ("weeknight","weekend"):
    r = suggest_home(CAT, store, TODAY, slot, 5)
    print(f"\n═══ HOME — {slot} ═══")
    print("  DUE FOR A RETURN")
    for s in r["due"]: print(f"    {s['score']:.3f}  {s['title']:<24} — {s['reason']}")
    print(f"  NOT TRIED ({r['untried_total']} fit tonight)")
    for s in r["untried"]: print(f"           {s['title']:<24} — {s['reason']}")
    if r["withheld_for_incomplete_data"]:
        print(f"  {r['withheld_for_incomplete_data']} excluded: dietary data incomplete")

print("\n═══ ENTERTAINING — your worked example, adapted ═══")
print("  12 covers · Egyptian · budget 1,500 EGP (~$31) · no seafood · two vegetarians\n")

guest_store = Store(cooks=store.cooks, lists=store.lists,
                    profile=Profile(household=12, excludes={"fish","shellfish"}, spice_max=1))
r = plan_event(CAT, guest_store, TODAY, covers=12, budget=31.25, cuisine=None,
               need_courses=("main","main","side","salad"))
if not r["ok"]:
    print(f"   NO MENU FITS — binding constraint: {r['binding']}")
    print(f"   {r['reason']}")
    if r.get("nearest"):
        print("   nearest:")
        for d in r["nearest"]: print(f"     {d['course']:<7} {d['title']:<24} ${d['cost']:>6.2f}")
        print(f"   → raise the budget to ${r['budget_needed']:.2f}, or drop to {r['or_drop_to']} dishes")
else:
    for i, opt in enumerate(r["options"], 1):
        print(f"  OPTION {i} — ${opt['cost']:.2f} of $31.25, ${opt['headroom']:.2f} spare"
              f" · you have cooked {opt['you_have_cooked']}")
        for d in opt["menu"]:
            print(f"     {d['course']:<7} {d['title']:<24} ${d['cost']:>5.2f}  ({d['note']})")
        print()
print(f"  {r['withheld_for_incomplete_data']} dish(es) excluded: dietary data incomplete")

print("\n═══ THE SAME EVENT ON HALF THE BUDGET ═══")
r2 = plan_event(CAT, guest_store, TODAY, covers=12, budget=15.0)
if r2["ok"]:
    print(f"   {len(r2['options'])} options, best ${r2['options'][0]['cost']:.2f}")
else:
    print(f"   binding: {r2['binding']} — {r2['reason']}")


print("\n═══ A REALISTIC BUDGET — 3,500 EGP (~$73) for 12 ═══")
guest_store.events = store.events        # same cook, same record
r3 = plan_event(CAT, guest_store, TODAY, covers=12, budget=73.0)
if r3["ok"]:
    for i,opt in enumerate(r3["options"][:2],1):
        print(f"  OPTION {i} — ${opt['cost']:.2f}, ${opt['headroom']:.2f} spare · cooked before: {opt['you_have_cooked']}")
        for d in opt["menu"]: print(f"     {d['course']:<7} {d['title']:<24} ${d['cost']:>6.2f}  ({d['note']})")
        print()
else:
    print("   ", r3["reason"])

print("\n═══ SAVED MENUS ═══")
# three recorded occasions; the same menu twice
store.events += [
 Event("e1","Amira's birthday", date(2026,3,14), 12,
       ["molokhia","salata","rice_verm","fattah"], budget=73.0, spent=67.80),
 Event("e2","Eid lunch", date(2026,4,2), 10,
       ["molokhia","salata","rice_verm","fattah"], budget=70.0, spent=56.50),
 Event("e3","Neighbours, Friday", date(2026,6,20), 6,
       ["tagine","tabbouleh","rice_verm"], budget=30.0, spent=13.50),
]
for m in saved_menus(store, TODAY):
    print(f"  {m['score']:.3f}  served {m['times_served']}x · last {m['days_ago']}d ago · "
          f"{m['covers']} covers")
    print(f"          occasions: {', '.join(m['occasions'])}")
    print(f"          {', '.join(m['dishes'])}")

print("\n═══ RECALL AT A NEW HEADCOUNT ═══")
key = saved_menus(store, TODAY)[0]["key"]
r = recall_menu(store, CAT, key, covers=16)
print(f"  \"{r['name']}\" — served {r['served']}x, last {r['last_served']}")
print(f"  previously {r['previously']['covers']} covers at ${r['previously']['spent']:.2f}")
print(f"  now {r['now']['covers']} covers at ${r['now']['cost']:.2f}  (change ${r['change']:+.2f})")
for d in r["dishes"]: print(f"     {d['course']:<7} {d['title']:<24} ${d['cost']:>6.2f}")

print("\n═══ RECALL WHEN A GUEST'S CONSTRAINT NOW EXCLUDES A DISH ═══")
strict = Store(cooks=store.cooks, lists=store.lists, events=store.events,
               profile=Profile(household=12, excludes={"dairy"}, spice_max=3))
r2 = recall_menu(strict, CAT, key, covers=12)
print(f"  ok={r2['ok']}")
for p in r2["no_longer_suitable"]:
    print(f"     DROPPED  {p['title']} — {p['why']}")
print(f"     remaining {len(r2['dishes'])} dishes, ${r2['now']['cost']:.2f}")

print("\n═══ PLANNER OFFERS A TESTED MENU FIRST ═══")
guest_store.events = store.events        # same cook, same record
r3 = plan_event(CAT, guest_store, TODAY, covers=12, budget=73.0)
for opt in r3.get("served_before", []):
    print(f"  SERVED BEFORE — \"{opt['name']}\" · ${opt['cost']:.2f} · {opt['reason']}")
    for d in opt["menu"]: print(f"     {d['course']:<7} {d['title']:<24} ${d['cost']:>6.2f}")
print(f"  ...then {len(r3['options'])} assembled option(s)")
