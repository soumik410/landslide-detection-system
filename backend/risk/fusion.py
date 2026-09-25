from risk.rules import evaluate_rules
from risk.model import risk_model

RISK_LEVELS = ["LOW", "MODERATE", "HIGH", "SEVERE"]


def classify(score: float) -> str:
    if score >= 75:
        return "SEVERE"
    if score >= 50:
        return "HIGH"
    if score >= 25:
        return "MODERATE"
    return "LOW"


def assess(features: dict) -> dict:
    rules_result = evaluate_rules(features)
    model_score = risk_model.score(features)

    fused_score = round(0.5 * rules_result["rule_score"] + 0.5 * model_score, 2)
    if len(rules_result["triggered_rules"]) >= 2:
        fused_score = max(fused_score, 60.0)

    risk_level = classify(fused_score)

    return {
        "risk_score": fused_score,
        "risk_level": risk_level,
        "rule_score": rules_result["rule_score"],
        "model_score": model_score,
        "triggered_rules": rules_result["triggered_rules"],
        "features": features,
    }