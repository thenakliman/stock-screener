from screener.common import constants


class CashFlow:
    def __init__(self,
                 financial_year: int,
                 cash_flow_from_operating_activities: float,
                 date_created: str,
                 last_date_updated: str):
        self._financial_year = financial_year
        self._cash_flow_from_operating_activities = cash_flow_from_operating_activities
        self._date_created = date_created
        self._last_date_updated = last_date_updated

    def get_financial_year(self) -> int:
        return self._financial_year

    def get_cash_flow_from_operating_activities(self) -> float:
        return self._cash_flow_from_operating_activities

    def positive_cash_flow(self):
        return self._cash_flow_from_operating_activities > 0
