# Soil moisture: raw ADC 0 (dry) - 1023 (wet) on a typical 10-bit ADC
def calibrate_moisture(raw: int) -> float:
    raw = max(0, min(1023, raw))
    return round((raw / 1023.0) * 100.0, 2)  # -> 0-100%


# Rain sensor: raw ADC 1023 (dry) - 0 (fully wet) typically; invert and scale to a rough mm/hr proxy
def calibrate_rain(raw: int) -> float:
    raw = max(0, min(1023, raw))
    wetness = (1023 - raw) / 1023.0
    return round(wetness * 40.0, 2)  # -> 0-40 mm/hr proxy scale


# Ultrasonic (HC-SR04-style): already arrives as cm from the board's own pulse-timing math
def calibrate_distance(raw_cm: float) -> float:
    return round(max(0.0, raw_cm), 2)


def calibrate_imu(raw_frame: dict):
    accel = (
        float(raw_frame.get("ax", 0.0)),
        float(raw_frame.get("ay", 0.0)),
        float(raw_frame.get("az", 1.0)),
    )
    gyro = (
        float(raw_frame.get("gx", 0.0)),
        float(raw_frame.get("gy", 0.0)),
        float(raw_frame.get("gz", 0.0)),
    )
    return accel, gyro