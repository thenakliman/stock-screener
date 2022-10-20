class StochasticOscillator:
    def __init__(self, date, slow_oscillator, fast_oscillator):
        self._date = date
        self._slow_oscillator = slow_oscillator
        self._fast_oscillator = fast_oscillator

    def get_date(self):
        return self._date

    def get_slow_oscillator(self):
        return self._slow_oscillator

    def get_fast_oscillator(self):
        return self._fast_oscillator
