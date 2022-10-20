import unittest
from unittest import mock

from screener.filters.stock.asset_turnover import asset_turnover_filter_operation, \
    sector_asset_turnover_filter_operation, asset_turnover_enrich_operation


class AssetTurnover(unittest.TestCase):
    def test_asset_turnover_filter_operation_return(self):
        stock = mock.Mock()
        stock.increasing_asset_turnover_ratio = mock.Mock(return_value=True)
        self.assertTrue(asset_turnover_filter_operation(stock))

    def test_asset_turnover_filter_operation_return_false(self):
        stock = mock.Mock()
        stock.increasing_asset_turnover_ratio = mock.Mock(return_value=False)
        self.assertFalse(asset_turnover_filter_operation(stock))

    def test_sector_asset_turnover_filter_operation_return_false(self):
        stock = mock.Mock()
        stock.asset_turnover_is_greater_than_sector = mock.Mock(return_value=False)
        self.assertFalse(sector_asset_turnover_filter_operation(stock))

    def test_sector_asset_turnover_filter_operation_return_true(self):
        stock = mock.Mock()
        stock.asset_turnover_is_greater_than_sector = mock.Mock(return_value=True)
        self.assertTrue(sector_asset_turnover_filter_operation(stock))

    @mock.patch("screener.filters.base.apply_operation_by_years")
    def test_asset_turnover_enrich_operation(self, apply_operation_by_years):
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata)
        exp_asset_turnovers = [1, 2, 3, 4]
        apply_operation_by_years.return_value = exp_asset_turnovers
        stock.get_financial_year_of_results = mock.Mock(return_value=['11', '12', '13', '14'])

        asset_turnover_enrich_operation(stock)

        self.assertListEqual(apply_operation_by_years.call_args[0][1], ['11', '12', '13'])
        update_report_in_metadata.assert_called_with({
            "asset_turnover": exp_asset_turnovers
        })
