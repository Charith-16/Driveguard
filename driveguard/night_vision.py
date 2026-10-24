"""Slide 6 - Night vision: detect what headlights can't."""
from .models import VehicleState

HEADLIGHT_RANGE_M = 60.0


def night_detections(state: VehicleState):
    """Objects beyond headlight reach that the IR/thermal sensor still sees."""
    if not state.is_night:
        return []
    return [o for o in state.objects if o.distance_m > HEADLIGHT_RANGE_M and o.kind in ("pedestrian", "cyclist")]
