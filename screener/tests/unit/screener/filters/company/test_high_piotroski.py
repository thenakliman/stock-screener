from unittest import TestCase, mock
from unittest.mock import call

from screener.exceptions.not_found import DataNotFound
from screener.filters.stock.high_piotroski import high_piotroski_filter_operation_more_than, \
    high_piotroski_filter_operation, high_piotroski_enrich_operation


class HighPiotroskiTest(TestCase):
    @mock.patch("screener.filters.stock.high_piotroski.get_enrich_operation")
    def test_high_piotroski_filter_operation_more_than__true__score_is_greater_than_required(self, mocked_get_enrich):
        def _side_effect(filter_name):
            def okay(x):
                if filter_name in ["cash_flow_greater_than_net_income", "asset_turnover"]:
                    return False
                return True

            return okay

        mocked_get_enrich.side_effect = _side_effect
        stock = mock.Mock()

        self.assertTrue(high_piotroski_filter_operation_more_than(stock, 6))

        mocked_get_enrich.assert_has_calls([
            call('cash_flow_greater_than_net_income'),
            call('asset_turnover'),
            call('current_ratio'),
            call('gross_margin'),
            call('increasing_return_on_asset'),
            call('long_term_debt'),
            call('operating_cash_flow'),
            call('positive_net_income'),
            call('issued_shares')
        ])

    @mock.patch("screener.filters.stock.high_piotroski.get_enrich_operation")
    def test_high_piotroski_filter_operation_more_than__false__score_is_less_than_required(self, mocked_get_enrich):
        def _side_effect(filter_name):
            def okay(x):
                if filter_name in ["cash_flow_greater_than_net_income", "asset_turnover"]:
                    return False
                return True

            return okay

        mocked_get_enrich.side_effect = _side_effect
        stock = mock.Mock()

        self.assertFalse(high_piotroski_filter_operation_more_than(stock, 8))

        mocked_get_enrich.assert_has_calls([
            call('cash_flow_greater_than_net_income'),
            call('asset_turnover'),
            call('current_ratio'),
            call('gross_margin'),
            call('increasing_return_on_asset'),
            call('long_term_debt'),
            call('operating_cash_flow'),
            call('positive_net_income'),
            call('issued_shares')
        ])

    @mock.patch("screener.filters.stock.high_piotroski.get_enrich_operation")
    def test_high_piotroski_filter_operation_more_than__true__handle_data_not_failure(self, mocked_get_enrich):
        def _side_effect(filter_name):
            def okay(x):
                if filter_name in ["cash_flow_greater_than_net_income", "asset_turnover"]:
                    raise DataNotFound()
                return True

            return okay

        mocked_get_enrich.side_effect = _side_effect
        stock = mock.Mock()

        self.assertTrue(high_piotroski_filter_operation_more_than(stock, 7))

        mocked_get_enrich.assert_has_calls([
            call('cash_flow_greater_than_net_income'),
            call('asset_turnover'),
            call('current_ratio'),
            call('gross_margin'),
            call('increasing_return_on_asset'),
            call('long_term_debt'),
            call('operating_cash_flow'),
            call('positive_net_income'),
            call('issued_shares')
        ])

    @mock.patch("screener.filters.stock.high_piotroski.get_enrich_operation")
    def test_high_piotroski_filter_operation_more_than__true__any_error(self, mocked_get_enrich):
        def _side_effect(filter_name):
            def okay(x):
                if filter_name in ["cash_flow_greater_than_net_income", "asset_turnover"]:
                    raise Exception()
                return True

            return okay

        mocked_get_enrich.side_effect = _side_effect
        stock = mock.Mock()

        self.assertTrue(high_piotroski_filter_operation_more_than(stock, 7))

        mocked_get_enrich.assert_has_calls([
            call('cash_flow_greater_than_net_income'),
            call('asset_turnover'),
            call('current_ratio'),
            call('gross_margin'),
            call('increasing_return_on_asset'),
            call('long_term_debt'),
            call('operating_cash_flow'),
            call('positive_net_income'),
            call('issued_shares')
        ])

    @mock.patch("screener.filters.stock.high_piotroski.get_enrich_operation")
    def test_high_piotroski_filter_operation__true(self, mocked_get_enrich):
        def _side_effect(filter_name):
            def okay(x):
                if filter_name in ["cash_flow_greater_than_net_income", "asset_turnover"]:
                    raise False
                return True

            return okay

        mocked_get_enrich.side_effect = _side_effect
        stock = mock.Mock()

        self.assertTrue(high_piotroski_filter_operation(stock))

        mocked_get_enrich.assert_has_calls([
            call('cash_flow_greater_than_net_income'),
            call('asset_turnover'),
            call('current_ratio'),
            call('gross_margin'),
            call('increasing_return_on_asset'),
            call('long_term_debt'),
            call('operating_cash_flow'),
            call('positive_net_income'),
            call('issued_shares')
        ])

    @mock.patch("screener.filters.stock.high_piotroski.get_enrich_operation")
    def test_high_piotroski_filter_operation__false(self, mocked_get_enrich):
        def _side_effect(filter_name):
            def okay(x):
                if filter_name in ["cash_flow_greater_than_net_income", "asset_turnover", "issued_shares"]:
                    return False
                return True

            return okay

        mocked_get_enrich.side_effect = _side_effect
        stock = mock.Mock()

        self.assertFalse(high_piotroski_filter_operation(stock))

        mocked_get_enrich.assert_has_calls([
            call('cash_flow_greater_than_net_income'),
            call('asset_turnover'),
            call('current_ratio'),
            call('gross_margin'),
            call('increasing_return_on_asset'),
            call('long_term_debt'),
            call('operating_cash_flow'),
            call('positive_net_income'),
            call('issued_shares')
        ])

    @mock.patch("screener.filters.stock.high_piotroski.get_enrich_operation")
    def test_high_piotroski_filter_operation__true__does_not_consider_failed_exception(self, mocked_get_enrich):
        def _side_effect(filter_name):
            def okay(x):
                if filter_name in ["cash_flow_greater_than_net_income", "asset_turnover"]:
                    return False
                if filter_name == "issued_shares":
                    raise Exception()
                return True

            return okay

        mocked_get_enrich.side_effect = _side_effect
        stock = mock.Mock()

        self.assertTrue(high_piotroski_filter_operation(stock))

        mocked_get_enrich.assert_has_calls([
            call('cash_flow_greater_than_net_income'),
            call('asset_turnover'),
            call('current_ratio'),
            call('gross_margin'),
            call('increasing_return_on_asset'),
            call('long_term_debt'),
            call('operating_cash_flow'),
            call('positive_net_income'),
            call('issued_shares')
        ])

    @mock.patch("screener.filters.stock.high_piotroski.get_enrich_operation")
    def test_high_piotroski_filter_operation__false__does_not_consider_failed_exception(self, mocked_get_enrich):
        def _side_effect(filter_name):
            def okay(x):
                if filter_name in ["cash_flow_greater_than_net_income", "asset_turnover", "positive_net_income"]:
                    return False
                if filter_name == "issued_shares":
                    raise DataNotFound()
                return True

            return okay

        mocked_get_enrich.side_effect = _side_effect
        stock = mock.Mock()

        self.assertFalse(high_piotroski_filter_operation(stock))

        mocked_get_enrich.assert_has_calls([
            call('cash_flow_greater_than_net_income'),
            call('asset_turnover'),
            call('current_ratio'),
            call('gross_margin'),
            call('increasing_return_on_asset'),
            call('long_term_debt'),
            call('operating_cash_flow'),
            call('positive_net_income'),
            call('issued_shares')
        ])

    @mock.patch("screener.filters.stock.high_piotroski.get_enrich_operation")
    def test_high_piotroski_enrich_operation(self, mocked_get_enrich):
        def _side_effect(filter_name):
            def okay(x):
                if filter_name in ["cash_flow_greater_than_net_income", "asset_turnover"]:
                    return False
                elif filter_name == "positive_net_income":
                    raise Exception()

                return True

            return okay

        mocked_get_enrich.side_effect = _side_effect
        failed = []
        succeed = []
        score = []
        stock = mock.Mock(
            update_success_operation_status=lambda x: succeed.append(x),
            update_failed_operation_status=lambda x: failed.append(x),
            update_score_to=lambda s: (score.append(s))
        )

        high_piotroski_enrich_operation(stock)

        self.assertListEqual(failed, [
            "cash_flow_greater_than_net_income",
            "asset_turnover"
        ])
        self.assertListEqual(succeed, [
            "current_ratio",
            "gross_margin",
            "increasing_return_on_asset",
            "long_term_debt",
            "operating_cash_flow",
            "issued_shares"
        ])
        self.assertEquals(score[0], 6)
        mocked_get_enrich.assert_has_calls([
            call('cash_flow_greater_than_net_income'),
            call('asset_turnover'),
            call('current_ratio'),
            call('gross_margin'),
            call('increasing_return_on_asset'),
            call('long_term_debt'),
            call('operating_cash_flow'),
            call('positive_net_income'),
            call('issued_shares')
        ])
