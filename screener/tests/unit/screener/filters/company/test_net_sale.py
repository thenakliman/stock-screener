from unittest import TestCase, mock

from screener.filters.stock.net_sale import (
    net_sale_filter_operation,
    net_income_enrich_operation,
    net_sale_more_than,
    net_sale_increased_by_filter_operation, net_sale_sector_filter_operation)


class NetSaleTest(TestCase):
    def test_net_sale_filter_operation__true__when_net_sales_increasing(self):
        net_sale_increasing = mock.Mock(return_value=True)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: ["19", "18"],
                          net_sale_increasing=net_sale_increasing)

        self.assertTrue(net_sale_filter_operation(stock, 2, 6))
        net_sale_increasing.assert_called_with(["19", "18"], 2, 6)

    def test_net_sale_filter_operation__false__when_net_sales_increasing(self):
        net_sale_increasing = mock.Mock(return_value=False)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: ["19", "18"],
                          net_sale_increasing=net_sale_increasing)

        self.assertFalse(net_sale_filter_operation(stock, 2, 6))
        net_sale_increasing.assert_called_with(["19", "18"], 2, 6)

    def test_net_sale_sector_filter_operation__false(self):
        stock = mock.Mock(net_sale_compare_to_sector=lambda x, y: False)

        self.assertFalse(net_sale_sector_filter_operation(stock, 2, 6))

    def test_net_sale_sector_filter_operation__true(self):
        stock = mock.Mock(net_sale_compare_to_sector=lambda x, y: True)

        self.assertTrue(net_sale_sector_filter_operation(stock, 2, 6))

    def test_net_sale_more_than_filter_operation__true__when_net_sales_more_than_given(self):
        get_net_sales_for_year = mock.Mock(return_value=200)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "21",
                          get_net_sales_for_year=get_net_sales_for_year)

        self.assertTrue(net_sale_more_than(stock, 100))
        get_net_sales_for_year.assert_called_with("21")

    def test_net_sale_more_than_filter_operation__true__when_net_sales_more_equal_given(self):
        get_net_sales_for_year = mock.Mock(return_value=200)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "21",
                          get_net_sales_for_year=get_net_sales_for_year)

        self.assertTrue(net_sale_more_than(stock, 200))
        get_net_sales_for_year.assert_called_with("21")

    def test_net_sale_more_than_filter_operation__false__when_net_sales_less_than_given(self):
        get_net_sales_for_year = mock.Mock(return_value=200)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "21",
                          get_net_sales_for_year=get_net_sales_for_year)

        self.assertFalse(net_sale_more_than(stock, 201))
        get_net_sales_for_year.assert_called_with("21")

    def test_net_sale_increased_by_filter_operation__true__when_net_sales_greater_than_given(self):
        get_net_sales_for_year = mock.Mock(return_value=True)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "21",
                          net_sale_increased_by=get_net_sales_for_year)

        self.assertTrue(net_sale_increased_by_filter_operation(stock, 5, 201))
        get_net_sales_for_year.assert_called_with('21', 5, 201)

    def test_net_sale_increased_by_filter_operation__false__when_net_sales_less_than_given(self):
        get_net_sales_for_year = mock.Mock(return_value=False)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "21",
                          net_sale_increased_by=get_net_sales_for_year)

        self.assertFalse(net_sale_increased_by_filter_operation(stock, 5, 201))
        get_net_sales_for_year.assert_called_with('21', 5, 201)

    @staticmethod
    def test_net_income_enrich_operation():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          get_financial_year_of_results=lambda: ["20", "19"],
                          get_net_sales_for_year=lambda x: {"20": 32, "19": 432}[x])

        net_income_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "net_sale": [32, 432]
        })
