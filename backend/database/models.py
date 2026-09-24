"""SQLAlchemy ORM models for sensor readings, risk assessments, and alerts."""
import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import settings

Base = declarative_base()


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    moisture_pct = Column(Float)
    rain_mm_hr = Column(Float)
    distance_cm = Column(Float)
    displacement_cm = Column(Float)
    tilt_deg = Column(Float)
    vibration = Column(Float)
    raw_frame = Column(JSON)


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    risk_score = Column(Float)
    risk_level = Column(String(20))
    rule_score = Column(Float)
    model_score = Column(Float)
    triggered_rules = Column(JSON)
    features = Column(JSON)
    explanation = Column(Text, nullable=True)  # filled in later by the agent/explanation layer


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    risk_level = Column(String(20))
    message = Column(Text)
    acknowledged = Column(Integer, default=0)  # 0/1 boolean flag (SQLite-friendly)


engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    Base.metadata.create_all(bind=engine)