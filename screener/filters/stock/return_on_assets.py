from screener.common.constants import RETURN_ON_ASSETS
from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("return_on_asset")
def return_on_asset_filter_operation(stock, return_on_asset):
    return stock.calculate_return_on_asset(stock.find_financial_year_of_latest_results()) >= return_on_asset


@register_filter_operation("return_on_asset_is_greater_than_sector")
@register_enrich_operation("return_on_asset_is_greater_than_sector")
def sector_return_on_asset_filter_operation(stock):
    return stock.return_on_asset_is_greater_than_sector(stock.find_financial_year_of_latest_results())


@register_enrich_operation("return_on_asset_report")
def return_on_asset_filter_operation_enrich_operation(stock):
    stock.update_report_in_metadata({
        RETURN_ON_ASSETS: [stock.calculate_return_on_asset(year) for year in
                           stock.get_financial_year_of_results()[:-1]]
    })


@register_filter_operation("increasing_return_on_asset")
@register_enrich_operation("increasing_return_on_asset")
def increasing_return_on_asset_filter_operation(stock):
    return stock.increasing_return_on_asset(stock.find_financial_year_of_latest_results())


@register_enrich_operation("increasing_return_on_asset_report")
def increasing_return_on_asset_enrich_operation(stock):
    stock.update_report_in_metadata({
        "return_on_asset": [stock.calculate_return_on_asset(year) for year in stock.get_financial_year_of_results()]
    })
