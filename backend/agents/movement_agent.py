"""Interprets IMU (tilt + vibration) and displacement data for signs of ground movement."""
from agents.llm_client import call_llm

SYSTEM_PROMPT = (
    "You are a ground-movement assistant for a landslide early-warning system. "
    "Given slope tilt, vibration, and displacement readings, explain in 1-2 sentences "
    "whether these readings suggest meaningful ground movement or are within normal noise. "
    "Be concise and specific with the numbers given."
)


def run(features: dict) -> str:
    prompt = (
        f"Slope tilt: {features['tilt_deg']} degrees\n"
        f"Vibration index: {features['vibration']}\n"
        f"Displacement: {features['displacement_cm']} cm (rate of change: {features['displacement_roc']}/s)\n"
    )
    try:
        return call_llm(SYSTEM_PROMPT, prompt)
    except Exception as e:
        return f"[movement_agent unavailable: {e}]"