import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from driveguard import simulator, risk_engine, routing, collision, weather, gestures
from driveguard.models import Weather


class Tests(unittest.TestCase):
    def test_hazard_triggers_braking(self):
        r = risk_engine.evaluate(simulator.make("highway_hazard"))
        self.assertIsNotNone(r.time_to_impact_s)
        self.assertIn("BRAK", r.action)

    def test_fatigue_alert(self):
        r = risk_engine.evaluate(simulator.make("fatigue"))
        self.assertIn("FATIGUE DETECTED", r.alerts)

    def test_hydroplaning(self):
        self.assertTrue(weather.hydroplaning_risk(Weather("flooded", 0.5, 12), 85))
        self.assertLess(weather.road_grip(Weather("flooded", 0.5, 12), 85), 0.5)

    def test_safe_route_avoids_accident(self):
        path, _, _ = routing.safest_route(routing.DEMO_GRAPH, "Home", "Office")
        self.assertEqual(path, ["Home", "Ring Rd", "Office"])

    def test_collision_response(self):
        out = collision.respond(collision.CrashEvent(8.0, True, 80, 17.4, 78.5))
        self.assertTrue(out["confirmed"])
        self.assertEqual(out["data_sent"]["occupant_status"]["status"], "STABLE")

    def test_gesture(self):
        self.assertEqual(gestures.interpret("wave"), "Answer call")


if __name__ == "__main__":
    unittest.main()
