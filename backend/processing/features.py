import statistics
from typing import List


def rate_of_change(history: List[float], interval_seconds: float) -> float:
    """Change per second between the oldest and newest value in the window."""
    if len(history) < 2 or interval_seconds <= 0:
        return 0.0
    total_time = interval_seconds * (len(history) - 1)
    return round((history[-1] - history[0]) / total_time, 4) if total_time > 0 else 0.0


def rolling_stats(history: List[float]) -> dict:
    if not history:
        return {"mean": 0.0, "stdev": 0.0, "min": 0.0, "max": 0.0}
    return {
        "mean": round(statistics.mean(history), 3),
        "stdev": round(statistics.pstdev(history), 3) if len(history) > 1 else 0.0,
        "min": round(min(history), 3),
        "max": round(max(history), 3),
    }


def build_feature_vector(moisture_hist, rain_hist, displacement_hist, tilt_hist, vibration_hist, poll_interval_s):
    """Assembles the flat feature dict consumed by risk/model.py and risk/rules.py."""
    return {
        "moisture_pct": moisture_hist[-1] if moisture_hist else 0.0,
        "moisture_roc": rate_of_change(moisture_hist, poll_interval_s),
        "rain_mm_hr": rain_hist[-1] if rain_hist else 0.0,
        "rain_roc": rate_of_change(rain_hist, poll_interval_s),
        "displacement_cm": displacement_hist[-1] if displacement_hist else 0.0,
        "displacement_roc": rate_of_change(displacement_hist, poll_interval_s),
        "tilt_deg": tilt_hist[-1] if tilt_hist else 0.0,
        "vibration": vibration_hist[-1] if vibration_hist else 0.0,
        "vibration_stats": rolling_stats(vibration_hist),
    }