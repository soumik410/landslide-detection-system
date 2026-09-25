from agents.llm_client import call_llm

SYSTEM_PROMPT = (
    "You are a rainfall-pattern assistant for a landslide early-warning system. "
    "Given current rainfall intensity and its short-term trend, explain in 1-2 sentences "
    "whether the current rainfall pattern is a meaningful landslide risk factor, referencing "
    "typical rainfall-intensity risk thresholds. Be concise and specific."
)


def run(features: dict) -> str:
    prompt = (
        f"Current rainfall intensity: {features['rain_mm_hr']} mm/hr\n"
        f"Rate of change: {features['rain_roc']}/s\n"
    )
    try:
        return call_llm(SYSTEM_PROMPT, prompt)
    except Exception as e:
        return f"[rain_agent unavailable: {e}]"