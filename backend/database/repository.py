from database.models import SessionLocal, SensorReading, RiskAssessment, Alert


def save_sensor_reading(session, features: dict, raw_frame: dict) -> SensorReading:
    reading = SensorReading(
        moisture_pct=features.get("moisture_pct"),
        rain_mm_hr=features.get("rain_mm_hr"),
        distance_cm=raw_frame.get("distance_cm"),
        displacement_cm=features.get("displacement_cm"),
        tilt_deg=features.get("tilt_deg"),
        vibration=features.get("vibration"),
        raw_frame=raw_frame,
    )
    session.add(reading)
    session.commit()
    session.refresh(reading)
    return reading


def save_risk_assessment(session, assessment: dict, explanation: str = None) -> RiskAssessment:
    row = RiskAssessment(
        risk_score=assessment["risk_score"],
        risk_level=assessment["risk_level"],
        rule_score=assessment["rule_score"],
        model_score=assessment["model_score"],
        triggered_rules=assessment["triggered_rules"],
        features=assessment["features"],
        explanation=explanation,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def create_alert(session, risk_level: str, message: str) -> Alert:
    alert = Alert(risk_level=risk_level, message=message)
    session.add(alert)
    session.commit()
    session.refresh(alert)
    return alert


def get_latest_reading(session):
    return session.query(SensorReading).order_by(SensorReading.timestamp.desc()).first()


def get_latest_risk(session):
    return session.query(RiskAssessment).order_by(RiskAssessment.timestamp.desc()).first()


def get_recent_readings(session, limit: int = 50):
    return session.query(SensorReading).order_by(SensorReading.timestamp.desc()).limit(limit).all()


def get_recent_risk_assessments(session, limit: int = 50):
    return session.query(RiskAssessment).order_by(RiskAssessment.timestamp.desc()).limit(limit).all()


def get_unacknowledged_alerts(session):
    return session.query(Alert).filter(Alert.acknowledged == 0).order_by(Alert.timestamp.desc()).all()


def acknowledge_alert(session, alert_id: int):
    alert = session.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.acknowledged = 1
        session.commit()
    return alert


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()