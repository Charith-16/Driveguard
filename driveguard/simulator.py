"""Scenario generator that mirrors the slides' demo situations."""
import random
from .models import VehicleState, DetectedObject, Weather, DriverState

SCENARIOS = ["highway_hazard", "heavy_rain", "hidden_pedestrian", "distracted_driver", "fatigue", "intersection"]


def make(name: str, seed: int = None) -> VehicleState:
    r = random.Random(seed)
    s = VehicleState()
    if name == "highway_hazard":
        s.objects = [DetectedObject("hazard", 48, 20), DetectedObject("vehicle", 90, 2)]
    elif name == "heavy_rain":
        s.speed_kmh = 85
        s.weather = Weather("flooded", 0.5, 12, 14)
    elif name == "hidden_pedestrian":
        s.is_night, s.speed_kmh = True, 50
        s.weather = Weather("wet", 0.55, 1, 16)
        s.objects = [DetectedObject("pedestrian", 35, 13.9)]
    elif name == "distracted_driver":
        s.driver = DriverState(0.2, 8, 0.25, True)
        s.objects = [DetectedObject("vehicle", 30, 8)]
    elif name == "fatigue":
        s.driver = DriverState(0.68, -12, 0.55, False)
    elif name == "intersection":
        s.speed_kmh = 32
        s.objects = [DetectedObject("vehicle", 22, 6), DetectedObject("pedestrian", 18, 2),
                     DetectedObject("cyclist", 25, 1), DetectedObject("vehicle", 40, 0)]
    else:
        s.objects = [DetectedObject("vehicle", r.uniform(40, 120), r.uniform(0, 10))]
    return s
