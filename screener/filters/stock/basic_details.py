from screener.filters.factory import register_enrich_operation


@register_enrich_operation("basic_details_report")
def basic_details(stock):
    stock.update_report_in_metadata({
        "isinid": str(stock.get_isinid()),
        "financial_year": str(stock.find_financial_year_of_latest_results()),
        "name": str(stock.get_company_name())
    })
