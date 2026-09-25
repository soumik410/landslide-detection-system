"""Endpoints for the current and historical deterministic risk assessments."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.repository import get_session, get_latest_risk, get_recent_risk_assessments

router = APIRouter(prefix="/api/risk", tags=["risk"])


def _serialize_risk(r):
    return {
        "id": r.id,
        "timestamp": r.timestamp.isoformat(),
        "risk_score": r.risk_score,
        "risk_level": r.risk_level,
        "rule_score": r.rule_score,
        "model_score": r.model_score,
        "triggered_rules": r.triggered_rules,
        "has_explanation": bool(r.explanation),
    }


@router.get("/current")
def current_risk(session: Session = Depends(get_session)):
    risk = get_latest_risk(session)
    return _serialize_risk(risk) if risk else {"message": "No risk assessments yet"}


@router.get("/history")
def risk_history(limit: int = 50, session: Session = Depends(get_session)):
    rows = get_recent_risk_assessments(session, limit=limit)
    return [_serialize_risk(r) for r in rows]