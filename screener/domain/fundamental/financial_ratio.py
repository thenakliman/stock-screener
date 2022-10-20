from screener.common import constants


class FinancialRatio:
    def __init__(self,
                 current_ratio: float,
                 gross_margin: float,
                 asset_turnover_ratio: float,
                 return_on_asset: float,
                 financial_year: int,
                 date_created: str,
                 last_date_updated: str):
        self._current_ratio = current_ratio
        self._gross_margin = gross_margin
        self._asset_turnover_ratio = asset_turnover_ratio
        self._return_on_asset = return_on_asset
        self._financial_year = financial_year
        self._date_created = date_created
        self._last_date_updated = last_date_updated

    def get_current_ratio(self) -> float:
        return self._current_ratio

    def get_asset_turnover(self) -> float:
        return self._asset_turnover_ratio

    def get_return_on_asset(self) -> float:
        return self._return_on_asset

    def get_gross_margin(self) -> float:
        return self._gross_margin

    def get_financial_year(self) -> int:
        return self._financial_year

    def to_dict(self) -> dict:
        return {
            constants.CURRENT_RATIO: self._current_ratio,
            constants.GROSS_MARGIN: self._gross_margin,
            constants.ASSET_TURNOVER_RATIO: self._asset_turnover_ratio,
            constants.RETURN_ON_ASSET: self._return_on_asset,
            constants.FINANCIAL_YEAR: self._financial_year,
            constants.DATE_CREATED: self._date_created,
            constants.LAST_DATE_UPDATED: self._last_date_updated
        }
