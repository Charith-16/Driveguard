"""Slide 7 - Natural interaction via gestures."""
GESTURES = {
    "swipe": "Change view",
    "push": "Confirm",
    "wave": "Answer call",
    "open_palm": "Pause / Mute",
    "point_home": "Navigate home",
}


def interpret(gesture: str) -> str:
    return GESTURES.get(gesture, "Gesture not recognised")
