from dataclasses import dataclass, field
from typing import List


@dataclass
class DetectedObject:
    kind: str          # "vehicle" | "pedestrian" | "cyclist" | "hazard"
    distance_m: float
    closing_speed_ms: float  # positive = getting closer
    in_path: bool = True


@dataclass
class Weather:
    condition: str = "dry"      # dry | wet | heavy_rain | flooded | fog
    visibility: float = 1.0     # 0..1
    water_depth_cm: float = 0.0
    temperature_c: float = 22.0


@dataclass
class DriverState:
    eye_closure: float = 0.1       # 0..1 (PERCLOS)
    head_pose_deg: float = 0.0
    attention: float = 0.95        # 0..1
    phone_in_use: bool = False


@dataclass
class VehicleState:
    speed_kmh: float = 72.0
    lane_confidence: float = 0.98
    is_night: bool = False
    objects: List[DetectedObject] = field(default_factory=list)
    weather: Weather = field(default_factory=Weather)
    driver: DriverState = field(default_factory=DriverState)
