from processing.calibration import calibrate_moisture


class MoistureSensor:
    name = "moisture"

    def parse(self, raw_frame: dict) -> float:
        """raw_frame comes straight from hardware.serial_reader.SerialReader.read_raw()"""
        raw_value = raw_frame.get("moisture", 0)
        return calibrate_moisture(raw_value)