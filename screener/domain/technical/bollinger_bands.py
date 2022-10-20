class BollingerBand:
    def __init__(self, lower, upper, date):
        self._lower = lower
        self._upper = upper
        self._date = date

    def get_upper_band(self):
        return self._upper

    def get_lower_band(self):
        return self._lower

    def get_date(self):
        return self._date
