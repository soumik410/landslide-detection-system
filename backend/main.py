import asyncio
import logging
import contextlib

from fastapi import FastAPI

from config.settings import settings
from database.models import init_db, SessionLocal
from database import repository
from hardware.serial_reader import SerialReader
from sensors.moisture import MoistureSensor
from sensors.rain import RainSensor
from sensors.ultrasonic import UltrasonicSensor
from sensors.mpu6050 import MPU6050Sensor
from processing.filter import MovingAverageFilter
from processing.features import build_feature_vector
from processing.validator import validate_frame
from risk.fusion import assess
from api import sensor_routes, risk_routes, alert_routes, ai_routes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("landslide_backend")

app = FastAPI(title=settings.APP_NAME)
app.include_router(sensor_routes.router)
app.include_router(risk_routes.router)
app.include_router(alert_routes.router)
app.include_router(ai_routes.router)

# Shared pipeline components
_serial = SerialReader()
_moisture, _rain, _ultrasonic, _imu = MoistureSensor(), RainSensor(), UltrasonicSensor(), MPU6050Sensor()
_filter = MovingAverageFilter(window_size=5)

_poll_task = None


async def monitoring_loop():
    """Continuously: read -> calibrate -> filter -> build features -> assess risk -> persist -> alert if needed."""
    while True:
        try:
            raw = _serial.read_raw()
            if raw:
                moisture_pct = _filter.apply("moisture", _moisture.parse(raw))
                rain_mm_hr = _filter.apply("rain", _rain.parse(raw))
                ultra = _ultrasonic.parse(raw)
                imu = _imu.parse(raw)
                displacement_cm = _filter.apply("displacement", ultra["displacement_cm"])
                tilt_deg = _filter.apply("tilt", imu["tilt_deg"])
                vibration = _filter.apply("vibration", imu["vibration"])

                features = build_feature_vector(
                    _filter.history("moisture"),
                    _filter.history("rain"),
                    _filter.history("displacement"),
                    _filter.history("tilt"),
                    _filter.history("vibration"),
                    settings.POLL_INTERVAL_SECONDS,
                )
                features.update({
                    "distance_cm": ultra["distance_cm"],
                    "displacement_cm": displacement_cm,
                    "tilt_deg": tilt_deg,
                    "vibration": vibration,
                })

                bad_fields = validate_frame(features)
                if bad_fields:
                    logger.warning(f"Rejected frame -- invalid fields: {bad_fields}")
                else:
                    session = SessionLocal()
                    try:
                        repository.save_sensor_reading(session, features, {**raw, "distance_cm": ultra["distance_cm"]})
                        assessment = assess(features)
                        repository.save_risk_assessment(session, assessment)

                        if assessment["risk_level"] in ("HIGH", "SEVERE"):
                            repository.create_alert(
                                session,
                                assessment["risk_level"],
                                f"{assessment['risk_level']} risk detected (score {assessment['risk_score']}/100). "
                                f"Triggered: {', '.join(assessment['triggered_rules']) or 'model threshold'}.",
                            )
                        logger.info(f"Risk: {assessment['risk_level']} ({assessment['risk_score']}/100)")
                    finally:
                        session.close()
        except Exception as e:
            logger.error(f"Monitoring loop error: {e}")

        await asyncio.sleep(settings.POLL_INTERVAL_SECONDS)


@app.on_event("startup")
async def on_startup():
    init_db()
    global _poll_task
    _poll_task = asyncio.create_task(monitoring_loop())
    logger.info(f"{settings.APP_NAME} started (simulate_hardware={settings.SIMULATE_HARDWARE})")


@app.on_event("shutdown")
async def on_shutdown():
    if _poll_task:
        _poll_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await _poll_task
    _serial.close()


@app.get("/")
def root():
    return {"status": "ok", "app": settings.APP_NAME}