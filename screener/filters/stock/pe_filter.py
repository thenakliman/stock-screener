from screener.common import constants
from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("pe_filter")
@register_enrich_operation("pe_filter")
def pe_filter_operation(stock, percentage_of_industry):
    pe = stock.get_pe()
    if pe < 0:
        return False  # stock in loss

    return pe * 100 <= stock.get_industry_pe() * percentage_of_industry


@register_filter_operation("max_pe")
def max_pe_filter(stock, maximum_pe):
    return maximum_pe >= stock.get_pe()


@register_filter_operation("pe_is_less_than_sector_pe")
@register_enrich_operation("pe_is_less_than_sector_pe")
def sector_pe_filter_operation(stock):
    return stock.pe_is_less_than_sector_pe()


@register_enrich_operation("pe_filter_report")
def pe_enrich_operation(stock):
    stock.update_report_in_metadata({
        constants.PE: stock.get_pe(),
        constants.INDUSTRY_PE: stock.get_industry_pe()
    })
