from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("increasing_net_sale")
@register_enrich_operation("increasing_net_sale")
def net_sale_filter_operation(stock, for_years, expected_increment):
    return stock.net_sale_increasing(stock.find_financial_year_of_latest_results(),
                                     for_years,
                                     expected_increment)


@register_filter_operation("increasing_net_sale_compare_to_sector")
@register_enrich_operation("increasing_net_sale_compare_to_sector")
def net_sale_sector_filter_operation(stock, for_years, expected_increment):
    return stock.net_sale_compare_to_sector(for_years, expected_increment)


@register_filter_operation("increased_net_sale")
def net_sale_increased_by_filter_operation(stock, in_years, expected_increment):
    return stock.net_sale_increased_by(stock.find_financial_year_of_latest_results(),
                                       in_years,
                                       expected_increment)


@register_filter_operation("net_sales")
@register_enrich_operation("net_sales")
def net_sale_more_than(stock, minimum_sales):
    return stock.get_net_sales_for_year(stock.find_financial_year_of_latest_results()) >= minimum_sales


@register_enrich_operation("increasing_net_sale_report")
def net_income_enrich_operation(stock):
    stock.update_report_in_metadata({
        "net_sale": [stock.get_net_sales_for_year(year) for year in stock.get_financial_year_of_results()]
    })
