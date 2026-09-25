VALID_RANGES = {
    "moisture_pct": (0.0, 100.0),
    "rain_mm_hr": (0.0, 200.0),
    "distance_cm": (0.0, 500.0),
    "tilt_deg": (0.0, 90.0),
}


def validate(name: str, value: float) -> bool:
    lo, hi = VALID_RANGES.get(name, (float("-inf"), float("inf")))
    return lo <= value <= hi


def validate_frame(features: dict) -> list:
    """Returns a list of field names that failed validation (empty list = all good)."""
    failures = []
    checks = {
        "moisture_pct": features.get("moisture_pct"),
        "rain_mm_hr": features.get("rain_mm_hr"),
        "tilt_deg": features.get("tilt_deg"),
    }
    for name, value in checks.items():
        if value is not None and not validate(name, value):
            failures.append(name)
    return failures