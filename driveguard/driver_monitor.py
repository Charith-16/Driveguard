"""Slide 9 - The system watches the road and the driver."""
from dataclasses import dataclass
from typing import List
from .models import DriverState


@dataclass
class DriverAssessment:
    level: str            # ok | warning | critical
    alerts: List[str]


def assess_driver(d: DriverState) -> DriverAssessment:
    alerts = []
    score = 0
    if d.eye_closure >= 0.6:
        alerts.append("FATIGUE DETECTED"); score += 2
    elif d.eye_closure >= 0.35:
        alerts.append("Drowsiness building"); score += 1
    if abs(d.head_pose_deg) >= 20:
        alerts.append("Head pose abnormal"); score += 1
    if d.attention < 0.5:
        alerts.append("Driver distracted"); score += 2
    if d.phone_in_use:
        alerts.append("Phone use detected"); score += 2
    level = "critical" if score >= 3 else "warning" if score >= 1 else "ok"
    return DriverAssessment(level, alerts)
