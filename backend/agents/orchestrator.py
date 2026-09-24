"""
Coordinates all sub-agents. Policy: always run the cheap, fast sensor/rain/movement
agents; only invoke the more expensive RAG-grounded geology/historical agents (extra
retrieval + LLM calls) once risk is at least MODERATE, since they add the most value
when something is already worth explaining in depth. This keeps LOW-risk polling
cycles cheap while still giving a rich explanation when it matters.

NOTE: this invocation policy is a reasonable default, not a fixed requirement --
tune AGENT_TRIGGER_LEVEL below to change when the RAG agents kick in.
"""
from agents import sensor_agent, rain_agent, movement_agent, geology_agent, historical_agent, explanation_agent

RISK_ORDER = {"LOW": 0, "MODERATE": 1, "HIGH": 2, "SEVERE": 3}
AGENT_TRIGGER_LEVEL = "MODERATE"  # geology/historical agents run at this level and above


def run(assessment: dict) -> dict:
    features = assessment["features"]

    sub_agent_notes = {
        "sensor_agent": sensor_agent.run(features),
        "rain_agent": rain_agent.run(features),
        "movement_agent": movement_agent.run(features),
    }

    if RISK_ORDER.get(assessment["risk_level"], 0) >= RISK_ORDER[AGENT_TRIGGER_LEVEL]:
        sub_agent_notes["geology_agent"] = geology_agent.run(features)
        sub_agent_notes["historical_agent"] = historical_agent.run(features)

    explanation = explanation_agent.run(assessment, sub_agent_notes)

    return {
        "explanation": explanation,
        "sub_agent_notes": sub_agent_notes,
    }