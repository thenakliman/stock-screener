import datetime

STOCK_ANALYSIS_DATE_FORMAT = '%d-%m-%Y'


def today() -> str:
    return datetime.date.today().strftime(STOCK_ANALYSIS_DATE_FORMAT)


def current_year() -> int:
    return datetime.date.today().year


def current_month() -> int:
    return datetime.date.today().month


def seconds_since_epoch() -> str:
    return datetime.date.today().strftime('%s')
