from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.repository import get_session, get_latest_reading, get_recent_readings

router = APIRouter(prefix="/api/sensors", tags=["sensors"])


def _serialize_reading(r):
    return {
        "id": r.id,
        "timestamp": r.timestamp.isoformat(),
        "moisture_pct": r.moisture_pct,
        "rain_mm_hr": r.rain_mm_hr,
        "distance_cm": r.distance_cm,
        "displacement_cm": r.displacement_cm,
        "tilt_deg": r.tilt_deg,
        "vibration": r.vibration,
    }


@router.get("/latest")
def latest_reading(session: Session = Depends(get_session)):
    reading = get_latest_reading(session)
    return _serialize_reading(reading) if reading else {"message": "No readings yet"}


@router.get("/recent")
def recent_readings(limit: int = 50, session: Session = Depends(get_session)):
    readings = get_recent_readings(session, limit=limit)
    return [_serialize_reading(r) for r in readings]