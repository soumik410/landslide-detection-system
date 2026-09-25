import os
import pickle

MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_model.pkl")

# Hand-set feature weights (0-1 normalized contributions), used until a trained model exists
DEFAULT_WEIGHTS = {
    "moisture_pct": 0.20,
    "rain_mm_hr": 0.20,
    "displacement_cm": 0.25,
    "tilt_deg": 0.20,
    "vibration": 0.15,
}

# Rough normalization ceilings for each feature, so the weighted sum lands in 0-100
NORMALIZATION = {
    "moisture_pct": 100.0,
    "rain_mm_hr": 40.0,
    "displacement_cm": 10.0,
    "tilt_deg": 15.0,
    "vibration": 5.0,
}


class RiskModel:
    def __init__(self):
        self._sklearn_model = self._try_load_trained_model()

    def _try_load_trained_model(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                return pickle.load(f)
        return None  # falls back to the weighted-sum heuristic below

    def score(self, features: dict) -> float:
        if self._sklearn_model is not None:
            x = [[features[k] for k in DEFAULT_WEIGHTS]]
            return round(float(self._sklearn_model.predict_proba(x)[0][1]) * 100, 2)

        total = 0.0
        for feat, weight in DEFAULT_WEIGHTS.items():
            normalized = min(1.0, max(0.0, features.get(feat, 0.0) / NORMALIZATION[feat]))
            total += normalized * weight
        return round(total * 100, 2)


risk_model = RiskModel()