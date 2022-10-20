class DayValue:
    def __init__(self, date: str, value: float, open: float, low: float, high: float, volume: int):
        self._date = date
        self._open = open
        self._value = value
        self._low = low
        self._high = high
        self._volume = volume

    def get_value(self) -> float:
        return self._value

    def get_date(self) -> str:
        return self._date

    def get_low(self) -> float:
        return self._low

    def get_high(self) -> float:
        return self._high

    def get_volume(self) -> int:
        return self._volume

    def get_typical_value(self) -> float:
        return (self._low + self._high + self._value) / 3

    def get_raw_money_flow(self) -> float:
        return self.get_typical_value() * self._volume

    def __gt__(self, other) -> bool:
        return self._value > other.get_value()

    def __lt__(self, other) -> bool:
        return self._value < other.get_value()

    def to_dict(self):
        return {
            "date": self._date,
            "open": self._open,
            "value": self._value,
            "low": self._low,
            "high": self._high,
            "volume": self._volume
        }
