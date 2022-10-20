from screener.common.constants import TAGS
from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("tag")
@register_enrich_operation("tag")
def tag_filter_operation(stock, tags):
    return stock.has_tags(tags)


@register_enrich_operation("tag_report")
def tag_enrich_operation(stock):
    stock.update_report_in_metadata({
        TAGS: [str(tag) for tag in stock.get_tags()]
    })
