from screener.domain.technical.historical_prices import HistoricalValues
from screener.domain.fundamental.index import Index
from screener.factories.domain.stock import get_historical_prices


def get_index(index_details: dict) -> Index:
    return _get_index_with_isinid_given(index_details, index_details.get("stocks"))


def _get_index_with_isinid_given(index_details, stocks_isinid):
    historical_prices_as_dict = index_details.get("historical_values", [])
    historical_prices = get_historical_prices(
        historical_prices_as_dict,
        date_extractor=lambda value: value.get("date"),
        value_extractor=lambda value: value.get("value"),
        low_extractor=lambda value: None,
        high_extractor=lambda value: None,
        open_value_extractor=lambda value: None,
        volume_extractor=lambda value: None
    )

    return Index(
        index_details.get("name"),
        stocks_isinid,
        HistoricalValues(historical_prices),
        index_details.get("current_value"),
        index_details.get("pe"),
        index_details.get("pb"),
        index_details.get("free_float"),
        index_details.get("full"),
        index_details.get("code"),
        index_details.get("category")
    )
