"""Slide 13 - Route for safety, not just speed (Dijkstra on a risk-weighted cost)."""
import heapq
from typing import Dict, List, Tuple

Graph = Dict[str, List[Tuple[str, float, float]]]  # node -> [(to, minutes, risk 0..1)]


def safest_route(graph: Graph, start: str, goal: str, safety_weight: float = 30.0):
    """cost = minutes + safety_weight * risk. Returns (path, minutes, avg_risk)."""
    pq = [(0.0, start, [start], 0.0, 0.0)]
    seen = {}
    while pq:
        cost, node, path, mins, risk_sum = heapq.heappop(pq)
        if node == goal:
            hops = max(len(path) - 1, 1)
            return path, round(mins, 1), round(risk_sum / hops, 2)
        if node in seen and seen[node] <= cost:
            continue
        seen[node] = cost
        for nxt, m, r in graph.get(node, []):
            heapq.heappush(pq, (cost + m + safety_weight * r, nxt, path + [nxt], mins + m, risk_sum + r))
    return None, None, None


DEMO_GRAPH: Graph = {
    "Home": [("Highway", 10, 0.55), ("Ring Rd", 14, 0.10), ("Downtown", 12, 0.35)],
    "Highway": [("Office", 8, 0.60)],      # accident ahead
    "Downtown": [("Office", 10, 0.40)],    # heavy rain
    "Ring Rd": [("Office", 10, 0.08)],     # safety-optimized
}
