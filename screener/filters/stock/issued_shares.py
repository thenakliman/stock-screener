from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("issued_shares")
@register_enrich_operation("issued_shares")
def issued_shares_filter_operation(stock):
    return not stock.new_shares_issued(stock.find_financial_year_of_latest_results())


@register_enrich_operation("issued_shares_report")
def issued_shares_enrich_operation(stock):
    total_issued_shares = [stock.get_issued_shares(year) for year in stock.get_financial_year_of_results()]
    new_issued_shares = [stock.get_new_issued_shares(year) for year in stock.get_financial_year_of_results()[:-1]]

    stock.update_report_in_metadata({
        "total_issued_shares": total_issued_shares,
        "new_issued_shares": new_issued_shares
    })
