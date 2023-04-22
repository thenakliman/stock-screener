from unittest import TestCase, mock

from screener.filters.stock.return_on_assets import return_on_asset_filter_operation, \
    sector_return_on_asset_filter_operation, return_on_asset_filter_operation_enrich_operation, \
    increasing_return_on_asset_filter_operation, increasing_return_on_asset_enrich_operation


class ReturnOnEquityTest(TestCase):
    def test_sector_return_on_asset_filter_operation__true__return_on_asset_greater_than_given(self):
        calculate_return_on_asset = mock.Mock(return_value=49)
        stock = mock.Mock(calculate_return_on_asset=calculate_return_on_asset,
                          find_financial_year_of_latest_results=lambda: "34")

        self.assertTrue(return_on_asset_filter_operation(stock, 45))
        calculate_return_on_asset.asset_called_with("34")

    def test_sector_return_on_asset_filter_operation__true__return_on_asset_equals_given(self):
        calculate_return_on_asset = mock.Mock(return_value=49)
        stock = mock.Mock(calculate_return_on_asset=calculate_return_on_asset,
                          find_financial_year_of_latest_results=lambda: "34")

        self.assertTrue(return_on_asset_filter_operation(stock, 49))
        calculate_return_on_asset.asset_called_with("34")

    def test_sector_return_on_asset_filter_operation__false__return_on_asset_less_than_given(self):
        calculate_return_on_asset = mock.Mock(return_value=49)
        stock = mock.Mock(calculate_return_on_asset=calculate_return_on_asset,
                          find_financial_year_of_latest_results=lambda: "34")

        self.assertFalse(return_on_asset_filter_operation(stock, 50))
        calculate_return_on_asset.asset_called_with("34")

    def test_sector_return_on_asset_filter_operation__true__when_roa_greater_than_sector(self):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "89",
                          return_on_asset_is_greater_than_sector=lambda x: x == "89")

        self.assertTrue(sector_return_on_asset_filter_operation(stock))

    def test_sector_return_on_asset_filter_operation__false__when_roa_greater_than_sector(self):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "89",
                          return_on_asset_is_greater_than_sector=lambda x: x != "89")

        self.assertFalse(sector_return_on_asset_filter_operation(stock))

    @staticmethod
    def test_return_on_asset_report():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          calculate_return_on_asset=lambda x: {"20": 34, "19": 98}[x],
                          get_financial_year_of_results=lambda: ["20", "19"])

        return_on_asset_filter_operation_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "return_on_assets": [34]
        })

    def test_increasing_return_on_asset_filter_operation__true__when_increase_roa(self):
        stock = mock.Mock(increasing_return_on_asset=lambda x: x == "19",
                          find_financial_year_of_latest_results=lambda: "19")

        self.assertTrue(increasing_return_on_asset_filter_operation(stock))

    @staticmethod
    def test_increasing_return_on_asset_enrich_operation__true__when_decreasing_roa():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(
            update_report_in_metadata=update_report_in_metadata,
            calculate_return_on_asset=lambda x: {"20": 234, "19": 83, "18": 16}[x],
            get_financial_year_of_results=lambda: ["20", "19", "18"])

        increasing_return_on_asset_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "return_on_asset": [234, 83, 16]
        })
