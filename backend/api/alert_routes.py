"""Endpoints for reading and acknowledging alerts raised by the monitoring loop."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.repository import get_session, get_unacknowledged_alerts, acknowledge_alert

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("/")
def list_alerts(session: Session = Depends(get_session)):
    alerts = get_unacknowledged_alerts(session)
    return [
        {"id": a.id, "timestamp": a.timestamp.isoformat(), "risk_level": a.risk_level, "message": a.message}
        for a in alerts
    ]


@router.post("/{alert_id}/acknowledge")
def ack_alert(alert_id: int, session: Session = Depends(get_session)):
    alert = acknowledge_alert(session, alert_id)
    if not alert:
        return {"error": "Alert not found"}
    return {"id": alert.id, "acknowledged": bool(alert.acknowledged)}