import json
import logging
import random
import time
from typing import Optional

from config.settings import settings

logger = logging.getLogger(__name__)

try:
    import serial  # pyserial
except ImportError:
    serial = None


class SerialReader:
    def __init__(self):
        self._ser = None
        self._simulate = settings.SIMULATE_HARDWARE or serial is None
        if not self._simulate:
            try:
                self._ser = serial.Serial(
                    settings.SERIAL_PORT,
                    settings.SERIAL_BAUDRATE,
                    timeout=settings.SERIAL_TIMEOUT,
                )
                logger.info(f"Opened serial port {settings.SERIAL_PORT}")
            except Exception as e:
                logger.warning(f"Could not open serial port ({e}); falling back to simulation mode")
                self._simulate = True

    def read_raw(self) -> Optional[dict]:
        """Return one raw sensor reading as a dict, or None if unavailable/unparseable."""
        if self._simulate:
            return self._simulate_reading()

        try:
            line = self._ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                return None
            return json.loads(line)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.debug(f"Bad serial frame skipped: {e}")
            return None
        except Exception as e:
            logger.error(f"Serial read error: {e}")
            return None

    def _simulate_reading(self) -> dict:
        """Synthetic but plausible sensor frame, with slow drift so risk logic has something to react to."""
        t = time.time()
        drift = (t % 600) / 600.0  # 0 -> 1 over a 10 min cycle, then resets
        return {
            "moisture": int(300 + drift * 500 + random.uniform(-15, 15)),   # raw ADC-ish 0-1023
            "rain": int(random.uniform(0, 200) * (1 + drift)),               # raw ADC-ish
            "dist_cm": round(50 - drift * 8 + random.uniform(-0.5, 0.5), 2), # ultrasonic distance to slope face
            "ax": round(random.uniform(-0.05, 0.05), 4),
            "ay": round(random.uniform(-0.05, 0.05), 4),
            "az": round(9.8 + random.uniform(-0.05, 0.05), 4),
            "gx": round(drift * random.uniform(0, 2), 4),
            "gy": round(drift * random.uniform(0, 2), 4),
            "gz": round(random.uniform(-0.1, 0.1), 4),
        }

    def close(self):
        if self._ser is not None:
            self._ser.close()