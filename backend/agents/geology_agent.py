"""Explains current readings in light of general slope-stability / geology reference material (RAG-grounded)."""
from agents.rag_agent import run as rag_run


def run(features: dict) -> str:
    query = (
        f"Given soil moisture of {features['moisture_pct']}%, slope tilt of "
        f"{features['tilt_deg']} degrees, and rainfall of {features['rain_mm_hr']} mm/hr, "
        f"what do geological slope-stability principles say about the risk implications "
        f"of these specific readings?"
    )
    return rag_run(query, category="geology")