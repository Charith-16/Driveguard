"""Slide 10 - When impact happens, response starts immediately."""
from dataclasses import dataclass


@dataclass
class CrashEvent:
    impact_g: float
    airbag_deployed: bool
    occupant_pulse_bpm: int
    lat: float
    lon: float


def respond(ev: CrashEvent) -> dict:
    """Confirm collision and build the payload sent to emergency services."""
    confirmed = ev.impact_g >= 4.0 or ev.airbag_deployed
    if not confirmed:
        return {"confirmed": False, "message": "No collision confirmed"}
    status = "STABLE" if 50 <= ev.occupant_pulse_bpm <= 120 else "CRITICAL"
    return {
        "confirmed": True,
        "dial": "911",
        "data_sent": {
            "location": {"lat": ev.lat, "lon": ev.lon},
            "impact_data": {"g_force": ev.impact_g, "airbag": ev.airbag_deployed},
            "occupant_status": {"pulse_bpm": ev.occupant_pulse_bpm, "status": status},
        },
        "message": "HELP IS ON THE WAY",
    }
