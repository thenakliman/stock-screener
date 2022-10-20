from screener.filters.factory import register_enrich_operation, register_filter_operation


@register_filter_operation("category_filter")
def category_filter_operation(index, category) -> bool:
    return index.get_category() == category


@register_enrich_operation("category_report")
def category_enrich_operation(index) -> None:
    index.update_report_in_metadata({
        "category": index.get_category()
    })
