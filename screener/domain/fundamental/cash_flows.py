from typing import List, Optional, Tuple

from screener.domain.fundamental.cash_flow import CashFlow
from screener.exceptions.not_found import CashFlowNotFound


class CashFlows:
    def __init__(self, cash_flows: List[CashFlow]):
        self._cash_flows = cash_flows

    def _find_cash_flow_for_year(self, year: int) -> Optional[CashFlow]:
        for cash_flow in self._cash_flows:
            if cash_flow.get_financial_year() == year:
                return cash_flow

        raise CashFlowNotFound(year=year)

    def positive_cash_flow(self, year: int) -> bool:
        return self._find_cash_flow_for_year(year).positive_cash_flow()

    def get_latest_financial_year_of_result(self) -> int:
        return max(self.get_financial_year_of_results(), default=1985)

    def get_cash_flow(self, year: int) -> float:
        return self._find_cash_flow_for_year(year).get_cash_flow_from_operating_activities()

    def get_financial_year_of_results(self) -> Tuple[int]:
        return tuple(cash_flow.get_financial_year() for cash_flow in self._cash_flows)
