from screener.filters import base
from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("asset_turnover")
@register_enrich_operation("asset_turnover")
def asset_turnover_filter_operation(stock):
    return stock.increasing_asset_turnover_ratio(stock.find_financial_year_of_latest_results())


@register_filter_operation("asset_turnover_is_greater_than_sector")
@register_enrich_operation("asset_turnover_is_greater_than_sector")
def sector_asset_turnover_filter_operation(stock):
    return stock.asset_turnover_is_greater_than_sector(stock.find_financial_year_of_latest_results())


@register_enrich_operation("asset_turnover_report")
def asset_turnover_enrich_operation(stock):
    asset_turnovers = base.apply_operation_by_years(
        stock.calculate_asset_turnover,
        stock.get_financial_year_of_results()[:-1])

    stock.update_report_in_metadata({
        "asset_turnover": asset_turnovers
    })
