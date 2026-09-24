"""IMU (MPU6050): accelerometer + gyroscope readings used to infer tilt and vibration/movement."""
import math
from processing.calibration import calibrate_imu


class MPU6050Sensor:
    name = "mpu6050"

    def parse(self, raw_frame: dict) -> dict:
        accel, gyro = calibrate_imu(raw_frame)
        ax, ay, az = accel
        # Tilt angle from vertical, derived from accelerometer components (small-angle static approximation)
        tilt_deg = math.degrees(math.atan2(math.sqrt(ax ** 2 + ay ** 2), az)) if az != 0 else 0.0
        vibration = math.sqrt(gyro[0] ** 2 + gyro[1] ** 2 + gyro[2] ** 2)
        return {
            "accel": {"x": ax, "y": ay, "z": az},
            "gyro": {"x": gyro[0], "y": gyro[1], "z": gyro[2]},
            "tilt_deg": round(tilt_deg, 3),
            "vibration": round(vibration, 3),
        }