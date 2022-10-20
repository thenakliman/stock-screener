from screener.common.constants import SECTOR
from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("sector")
@register_enrich_operation("sector")
def sector_filter_operation(stock, sectors):
    return str(stock.get_sector_name()).lower() in [sector.lower() for sector in sectors]


@register_enrich_operation("sector_report")
def sector_enrich_operation(stock):
    stock.update_report_in_metadata({
        SECTOR: str(stock.get_sector_name())
    })
