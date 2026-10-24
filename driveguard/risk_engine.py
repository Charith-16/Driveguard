"""Slides 3, 4, 12 - fuse signals into a risk score and a decision."""
from dataclasses import dataclass, field
from typing import List, Optional
from .models import VehicleState
from . import weather as wx
from .driver_monitor import assess_driver


@dataclass
class RiskReport:
    risk_pct: int
    level: str                       # LOW | MEDIUM | HIGH
    time_to_impact_s: Optional[float]
    action: str
    alerts: List[str] = field(default_factory=list)
    grip: float = 1.0
    stopping_distance_m: float = 0.0
    object_counts: dict = field(default_factory=dict)


def time_to_impact(state: VehicleState) -> Optional[float]:
    times = [o.distance_m / o.closing_speed_ms
             for o in state.objects if o.in_path and o.closing_speed_ms > 0.1]
    return round(min(times), 1) if times else None


def evaluate(state: VehicleState) -> RiskReport:
    alerts: List[str] = []
    grip = wx.road_grip(state.weather, state.speed_kmh)
    stop = wx.stopping_distance_m(state.speed_kmh, grip)
    tti = time_to_impact(state)

    risk = 5.0
    if tti is not None:
        risk += max(0, (4.0 - tti)) * 18
    for o in state.objects:
        if o.in_path and o.distance_m < stop:
            risk += 15
            alerts.append(f"{o.kind.title()} inside stopping distance ({o.distance_m:.0f} m)")
    risk += (1 - grip) * 25
    risk += (1 - state.weather.visibility) * 15
    if state.is_night:
        risk += 8
    if wx.hydroplaning_risk(state.weather, state.speed_kmh):
        risk += 10; alerts.append("HYDROPLANING RISK")
    da = assess_driver(state.driver)
    risk += {"ok": 0, "warning": 10, "critical": 22}[da.level]
    alerts += da.alerts
    if state.lane_confidence < 0.6:
        risk += 6; alerts.append("Low lane confidence")

    risk = int(max(0, min(100, round(risk))))
    level = "HIGH" if risk >= 60 else "MEDIUM" if risk >= 30 else "LOW"

    if tti is not None and tti <= 2.5:
        action = "AUTOMATIC BRAKING PRE-CHARGED" if tti > 1.2 else "EMERGENCY BRAKE"
    elif level == "HIGH":
        action = "REDUCE SPEED"
    elif level == "MEDIUM":
        action = "CAUTION - INCREASE FOLLOWING DISTANCE"
    else:
        action = "ALL SYSTEMS NORMAL"

    counts: dict = {}
    for o in state.objects:
        counts[o.kind] = counts.get(o.kind, 0) + 1
    return RiskReport(risk, level, tti, action, alerts, grip, round(stop, 1), counts)
