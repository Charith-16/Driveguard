# DriveGuard AI – Predictive Vehicle Safety

Prototype based on the *DriveGuard AI* presentation: an AI safety layer that fuses sensor,
weather, driver and route signals into a single risk score and an action.
> Simulation only – uses synthetic data; not for use in a real vehicle.

## Features
- Risk engine: time-to-impact, stopping distance, auto-brake pre-charge
- Weather: road grip & hydroplaning risk
- Night vision, driver fatigue/distraction monitoring, 360° door perimeter
- Collision detection & emergency payload, gesture control
- Safety-optimized routing (Dijkstra with risk-weighted cost)
- Live web dashboard + JSON API

## Run (Python 3.9+, no dependencies)
```bash
python main.py                 # CLI demo of all scenarios
python -m driveguard.server    # dashboard at http://localhost:8000
python -m unittest discover tests
```
API: `/api/scenarios`, `/api/evaluate?scenario=heavy_rain`, `/api/route`

## Next steps
Replace `simulator.py` with real camera/radar/CAN feeds, train ML models (YOLO for detection,
LSTM for trajectory prediction), and plug in live weather/traffic APIs. See `docs/SLIDE_MAPPING.md`.
