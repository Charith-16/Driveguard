"""Slide 8 - Protect the space around every door (360 deg perimeter)."""
from dataclasses import dataclass


@dataclass
class DoorWarning:
    door: str
    approaching: bool
    distance_m: float


def door_safety(approach_distance_m: float, approach_speed_ms: float, side: str = "rear-left") -> DoorWarning:
    """Warn occupants not to open a door if something arrives within 3 seconds."""
    approaching = approach_speed_ms > 0.3 and approach_distance_m / approach_speed_ms < 3.0
    return DoorWarning(side, approaching, approach_distance_m)
