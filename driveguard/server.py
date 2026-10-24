"""Tiny stdlib HTTP server: dashboard + JSON API.  Run: python -m driveguard.server"""
import json, os
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from . import simulator, risk_engine, routing, night_vision

ROOT = os.path.join(os.path.dirname(__file__), "..", "dashboard")


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/api/scenarios":
            return self._send(200, simulator.SCENARIOS)
        if u.path == "/api/evaluate":
            name = q.get("scenario", ["highway_hazard"])[0]
            st = simulator.make(name)
            rep = risk_engine.evaluate(st)
            return self._send(200, {
                "scenario": name, "state": asdict(st), "report": asdict(rep),
                "night_detections": [asdict(o) for o in night_vision.night_detections(st)],
            })
        if u.path == "/api/route":
            path, mins, risk = routing.safest_route(routing.DEMO_GRAPH, "Home", "Office")
            return self._send(200, {"path": path, "minutes": mins, "avg_risk": risk})
        if u.path in ("/", "/index.html"):
            with open(os.path.join(ROOT, "index.html"), "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")
        self._send(404, {"error": "not found"})

    def log_message(self, *a):
        pass


def main(port=8000):
    print(f"DriveGuard AI dashboard -> http://localhost:{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main(int(os.environ.get("PORT", 8000)))
