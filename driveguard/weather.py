"""Slide 5 - Weather changes the rules: road grip + hydroplaning risk."""
from .models import Weather

_BASE_GRIP = {"dry": 1.0, "wet": 0.75, "heavy_rain": 0.6, "flooded": 0.45, "fog": 0.85}


def road_grip(w: Weather, speed_kmh: float) -> float:
    """Return grip coefficient 0..1 (1 = dry road)."""
    grip = _BASE_GRIP.get(w.condition, 0.8)
    grip -= min(w.water_depth_cm, 15) * 0.01
    if w.temperature_c <= 2:
        grip -= 0.2  # ice risk
    if speed_kmh > 80 and w.condition in ("wet", "heavy_rain", "flooded"):
        grip -= (speed_kmh - 80) * 0.004
    return max(0.05, round(grip, 2))


def hydroplaning_risk(w: Weather, speed_kmh: float) -> bool:
    return w.condition in ("heavy_rain", "flooded") and (
        speed_kmh > 70 or w.water_depth_cm >= 8
    )


def stopping_distance_m(speed_kmh: float, grip: float, reaction_s: float = 1.0) -> float:
    v = speed_kmh / 3.6
    return v * reaction_s + v * v / (2 * 9.81 * max(grip, 0.05))
