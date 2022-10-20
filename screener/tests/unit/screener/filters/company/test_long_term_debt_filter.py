from unittest import TestCase, mock

from screener.filters.stock.long_term_debt_filter import long_term_debt_filter_operation, \
    long_term_debt_enrich_operation


class LongTermDebtTest(TestCase):
    def test_long_term_debt_enrich_operation__true__when_long_term_debts_are_decreasing(self):
        decreasing_long_term_debt_ratio_by_year = mock.Mock(return_value=True)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "20",
                          decreasing_long_term_debt_ratio_by_year=decreasing_long_term_debt_ratio_by_year)

        self.assertTrue(long_term_debt_filter_operation(stock))
        decreasing_long_term_debt_ratio_by_year.assert_called_with("20")

    def test_long_term_debt_enrich_operation__false__when_long_term_debts_are_increasing(self):
        decreasing_long_term_debt_ratio_by_year = mock.Mock(return_value=False)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "20",
                          decreasing_long_term_debt_ratio_by_year=decreasing_long_term_debt_ratio_by_year)

        self.assertFalse(long_term_debt_filter_operation(stock))
        decreasing_long_term_debt_ratio_by_year.assert_called_with("20")

    @staticmethod
    def test_long_term_debt_enrich_operation():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          get_financial_year_of_results=lambda: ["20", "19"],
                          get_long_term_debts=lambda x: {"20": 45, "19": 65}[x])

        long_term_debt_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "long_term_debts": [45, 65]
        })
