class RSI:
    def __init__(self, date, value):
        self._date = date
        self._value = value

    def get_date(self):
        return self._date

    def get_value(self):
        return self._value
