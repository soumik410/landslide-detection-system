"""Ultrasonic distance sensor: tracks distance to the slope face to detect ground displacement over time."""
from processing.calibration import calibrate_distance


class UltrasonicSensor:
    name = "ultrasonic"

    def __init__(self):
        self._baseline_cm = None  # distance recorded at install time / first reading

    def parse(self, raw_frame: dict) -> dict:
        dist_cm = calibrate_distance(raw_frame.get("dist_cm", 0.0))
        if self._baseline_cm is None:
            self._baseline_cm = dist_cm
        displacement_cm = round(self._baseline_cm - dist_cm, 2)  # positive = slope moved toward sensor
        return {"distance_cm": dist_cm, "displacement_cm": displacement_cm}