from config.settings import settings


def evaluate_rules(features: dict) -> dict:
    triggered = []

    if features["moisture_pct"] >= settings.MOISTURE_HIGH_PCT:
        triggered.append("high_soil_moisture")
    if features["rain_mm_hr"] >= settings.RAIN_HIGH_MM_PER_HR:
        triggered.append("heavy_rainfall")
    if features["tilt_deg"] >= settings.TILT_HIGH_DEGREES:
        triggered.append("excessive_slope_tilt")
    if features["displacement_cm"] >= settings.DISPLACEMENT_HIGH_CM:
        triggered.append("ground_displacement")
    if features["moisture_roc"] > 5.0:
        triggered.append("rapid_moisture_increase")
    if features["displacement_roc"] > 0.5:
        triggered.append("rapid_displacement")

    # Each triggered rule contributes weight toward the rule_score (0-100)
    weights = {
        "high_soil_moisture": 20,
        "heavy_rainfall": 20,
        "excessive_slope_tilt": 25,
        "ground_displacement": 25,
        "rapid_moisture_increase": 10,
        "rapid_displacement": 15,
    }
    rule_score = min(100, sum(weights[r] for r in triggered))

    return {"triggered_rules": triggered, "rule_score": rule_score}