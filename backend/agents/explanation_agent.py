"""
Final synthesis step: combines the deterministic risk assessment plus every sub-agent's
output into one coherent, human-readable explanation for the end user / alert message.
This agent explains the risk score -- it never changes it.
"""
from agents.llm_client import call_llm

SYSTEM_PROMPT = (
    "You are the final explanation-writer for a landslide early-warning system. "
    "You will be given a fixed, already-decided risk level/score plus notes from several "
    "specialist sub-agents. Write one clear paragraph (4-6 sentences) explaining WHY the "
    "system reached this risk level, in plain language suitable for a non-expert resident. "
    "Never contradict or second-guess the given risk level or score -- your job is only to "
    "explain it clearly using the supporting notes provided."
)


def run(assessment: dict, sub_agent_notes: dict) -> str:
    notes_block = "\n".join(f"- {name}: {note}" for name, note in sub_agent_notes.items() if note)
    prompt = (
        f"Risk level: {assessment['risk_level']} (score: {assessment['risk_score']}/100)\n"
        f"Triggered rules: {', '.join(assessment['triggered_rules']) or 'none'}\n\n"
        f"Specialist notes:\n{notes_block}\n\n"
        f"Write the final explanation."
    )
    try:
        return call_llm(SYSTEM_PROMPT, prompt)
    except Exception as e:
        return f"Risk level {assessment['risk_level']} ({assessment['risk_score']}/100) based on triggered factors: {', '.join(assessment['triggered_rules']) or 'baseline monitoring'}. [explanation_agent unavailable: {e}]"