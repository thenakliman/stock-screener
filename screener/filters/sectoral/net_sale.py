from screener.filters.factory import register_enrich_operation


@register_enrich_operation("net_sales")
def net_income_enrich_operation(sector):
    sector.update_report_in_metadata({
        "net_sale": [(sector.get_net_sales_for_year(year)) for year in [2018, 2019, 2020, 2021, 2022]]
    })
