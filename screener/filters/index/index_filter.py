from screener.filters.factory import register_enrich_operation, register_filter_operation
from screener.filters.index.constants import INDEX_NAME_KEY


@register_filter_operation("index_name_filter")
def index_filter_operation(index, indexes) -> True:
    return str(index.get_name()).lower() in [index.lower() for index in indexes]


@register_enrich_operation("index_name_report")
def index_enrich_operation(index) -> None:
    index.update_report_in_metadata({
        INDEX_NAME_KEY: str(index.get_name())
    })
