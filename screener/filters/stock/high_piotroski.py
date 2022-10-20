from screener.exceptions.not_found import DataNotFound
from screener.filters import constants
from screener.filters.factory import (
    register_filter_operation,
    register_enrich_operation,
    get_enrich_operation
)

piotroski_filters = [
    constants.CASH_FLOW_GREATER_THAN_NET_INCOME,
    constants.ASSET_TURNOVER,
    constants.CURRENT_RATIO,
    constants.GROSS_MARGIN,
    constants.INCREASING_RETURN_ON_ASSET,
    constants.LONG_TERM_DEBT,
    constants.OPERATING_CASH_FLOW,
    constants.POSITIVE_NET_INCOME,
    constants.ISSUED_SHARES
]


@register_filter_operation("high_piotroski_more_than")
def high_piotroski_filter_operation_more_than(stock, required_minimum_score: int) -> bool:
    scored = 0
    for filter_name in piotroski_filters:
        try:
            if get_enrich_operation(filter_name)(stock):
                scored += 1
        except DataNotFound:
            print(f"Data not found for filter={filter_name} isinid={stock.get_isinid()}")
        except Exception as e:
            print(f"Failed to perform operation {filter_name}", e)

    return scored >= required_minimum_score


@register_filter_operation("high_piotroski")
def high_piotroski_filter_operation(stock) -> bool:
    scored = 0
    applicable_filters_count = 0
    for filter_name in piotroski_filters:
        try:
            if get_enrich_operation(filter_name)(stock):
                scored += 1

            applicable_filters_count += 1
        except DataNotFound:
            print(f"Data not found for filter={filter_name}, isinid={stock.get_isinid()}")
        except Exception as e:
            print(f"Failed to perform operation {filter_name}.", e)

    return scored / (applicable_filters_count or len(piotroski_filters)) >= 0.75


@register_enrich_operation("high_piotroski_report")
def high_piotroski_enrich_operation(stock) -> None:
    scored = 0
    for filter_name in piotroski_filters:
        try:
            if get_enrich_operation(filter_name)(stock):
                scored += 1
                stock.update_success_operation_status(filter_name)
            else:
                stock.update_failed_operation_status(filter_name)
        except Exception as e:
            print(f"Failed to perform operation {filter_name}.", e)

    stock.update_score_to(scored)
