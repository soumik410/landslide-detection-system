from collections import deque


class MovingAverageFilter:
    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self._buffers: dict[str, deque] = {}

    def apply(self, key: str, value: float) -> float:
        """Push a new value for `key` and return the smoothed (windowed mean) value."""
        buf = self._buffers.setdefault(key, deque(maxlen=self.window_size))
        buf.append(value)
        return round(sum(buf) / len(buf), 3)

    def history(self, key: str) -> list:
        return list(self._buffers.get(key, []))