from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("minimum_score")
def minimum_weight(stock, minimum_score):
    return len(stock.get_metadata()["satisfied_criteria"]) >= minimum_score


@register_enrich_operation("add_metadata")
def add_metadata(stock, property_name, value):
    stock.add_metadata(property_name, value)


@register_enrich_operation("remove_property_from_metadata")
def remove_metadata(stock, property_name):
    stock.remove_metadata(property_name)


@register_enrich_operation("cleanup_metadata")
def cleanup_metadata(stock):
    stock.cleanup_metadata()
