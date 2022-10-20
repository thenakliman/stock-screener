class RateOfChange:
    def __init__(self, date, value):
        self._date = date
        self._value = value

    def get_date(self):
        return self._date

    def get_value(self):
        return self._value


def _get_rate_of_change(current_value, old_value):
    return ((current_value - old_value) / old_value) * 100


def get_rate_of_change(time_series, day):
    assert day > 0, "day must be greater than 0"
    rate_of_changes = []
    for index, day_value in enumerate(time_series):
        old_value_index = max(0, index - day)
        rate_of_change = _get_rate_of_change(
            day_value.get_value(),
            time_series[old_value_index].get_value())

        rate_of_changes.append(RateOfChange(day_value.get_date(), rate_of_change))

    return rate_of_changes
