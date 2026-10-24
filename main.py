"""CLI demo: python main.py [scenario ...]"""
import sys
from driveguard import simulator, risk_engine, routing

for n in sys.argv[1:] or simulator.SCENARIOS:
    st = simulator.make(n)
    r = risk_engine.evaluate(st)
    print(f"\n=== {n} ===")
    print(f"Risk {r.risk_pct}% ({r.level}) | TTI: {r.time_to_impact_s} s | Grip {r.grip} | Stop {r.stopping_distance_m} m")
    print("Action:", r.action)
    for a in r.alerts:
        print("  !", a)
path, mins, risk = routing.safest_route(routing.DEMO_GRAPH, "Home", "Office")
print(f"\nSafest route: {' -> '.join(path)} ({mins} min, avg risk {risk})")
