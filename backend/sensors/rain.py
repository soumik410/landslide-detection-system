from processing.calibration import calibrate_rain


class RainSensor:
    name = "rain"

    def parse(self, raw_frame: dict) -> float:
        raw_value = raw_frame.get("rain", 0)
        return calibrate_rain(raw_value)