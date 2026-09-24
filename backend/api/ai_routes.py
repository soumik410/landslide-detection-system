"""On-demand endpoint to run the full multi-agent RAG explanation pipeline for the latest risk assessment."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.repository import get_session, get_latest_risk
from database.models import RiskAssessment
from agents.orchestrator import run as run_orchestrator

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/explain")
def explain_latest_risk(session: Session = Depends(get_session)):
    latest: RiskAssessment = get_latest_risk(session)
    if not latest:
        return {"error": "No risk assessment available yet"}

    assessment = {
        "risk_score": latest.risk_score,
        "risk_level": latest.risk_level,
        "triggered_rules": latest.triggered_rules,
        "features": latest.features,
    }
    result = run_orchestrator(assessment)

    latest.explanation = result["explanation"]
    session.commit()

    return {
        "risk_level": latest.risk_level,
        "risk_score": latest.risk_score,
        "explanation": result["explanation"],
        "sub_agent_notes": result["sub_agent_notes"],
    }