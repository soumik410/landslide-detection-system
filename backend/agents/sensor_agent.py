"""Interprets the raw, filtered sensor readings into a short plain-language status summary."""
from agents.llm_client import call_llm

SYSTEM_PROMPT = (
    "You are a sensor-interpretation assistant for a landslide early-warning system. "
    "Given raw sensor feature values, summarize the current physical state of the slope "
    "in 2-3 plain sentences. Be factual and specific with numbers. Do not invent a risk "
    "classification -- that is decided elsewhere; just describe what the sensors show."
)


def run(features: dict) -> str:
    prompt = (
        f"Soil moisture: {features['moisture_pct']}% (rate of change: {features['moisture_roc']}/s)\n"
        f"Rainfall intensity: {features['rain_mm_hr']} mm/hr (rate of change: {features['rain_roc']}/s)\n"
        f"Ground displacement: {features['displacement_cm']} cm (rate of change: {features['displacement_roc']}/s)\n"
        f"Slope tilt: {features['tilt_deg']} degrees\n"
        f"Vibration index: {features['vibration']}\n"
    )
    try:
        return call_llm(SYSTEM_PROMPT, prompt)
    except Exception as e:
        return f"[sensor_agent unavailable: {e}]"