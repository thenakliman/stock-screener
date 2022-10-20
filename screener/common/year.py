from screener.common import date


def is_latest_financial_year(year):
    if date.current_month() <= 3:
        return date.current_year() - 1 == year

    if 4 <= date.current_month() <= 6:
        return date.current_year() == year or date.current_year() - 1 == year

    return date.current_year() == year
