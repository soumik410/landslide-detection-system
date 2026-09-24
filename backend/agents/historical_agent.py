"""Checks current readings against historical/regional landslide-incident patterns (RAG-grounded)."""
from agents.rag_agent import run as rag_run


def run(features: dict) -> str:
    query = (
        f"Given current moisture of {features['moisture_pct']}%, rainfall of "
        f"{features['rain_mm_hr']} mm/hr, and displacement of {features['displacement_cm']} cm, "
        f"how does this compare to historical landslide precursor patterns for this region?"
    )
    return rag_run(query, category="historical")