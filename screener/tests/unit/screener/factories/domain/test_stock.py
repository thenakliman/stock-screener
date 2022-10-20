from unittest import TestCase, mock

from screener.factories.domain.stock import get_stock


class StockTest(TestCase):
    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="hp")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock(self, mocked_stock, mocked_historical_prices, mocked_balance_sheets,
                       mocked_balance_sheet, mocked_income_statement, mocked_income_statements,
                       mocked_cash_flow, mocked_cash_flows, mocked_financial_ratio,
                       mocked_financial_ratios):
        stock = get_stock(dict())

        self.assertEqual("s-t-o-c-k", stock)
        mocked_stock.assert_called_with({'historical_prices': 'hp'}, "bss", "iss", "cfs", "frs")

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__map_date(self, mocked_stock, mocked_historical_prices, mocked_day, mocked_balance_sheets,
                                 mocked_balance_sheet, mocked_income_statement, mocked_income_statements,
                                 mocked_cash_flow, mocked_cash_flows, mocked_financial_ratio, mocked_financial_ratios):
        get_stock({"historical_prices": [{"date": "d"}]})

        mocked_day.assert_called_with("d", None, None, None, None, None)

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__map_value(self, mocked_stock, mocked_historical_prices, mocked_day, mocked_balance_sheets,
                                  mocked_balance_sheet, mocked_income_statement, mocked_income_statements,
                                  mocked_cash_flow, mocked_cash_flows, mocked_financial_ratio, mocked_financial_ratios):
        get_stock({"historical_prices": [{"date": "d", "value": "v"}]})

        mocked_day.assert_called_with("d", "v", None, None, None, None)

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__map_open(self, mocked_stock, mocked_historical_prices, mocked_day, mocked_balance_sheets,
                                 mocked_balance_sheet, mocked_income_statement, mocked_income_statements,
                                 mocked_cash_flow, mocked_cash_flows, mocked_financial_ratio, mocked_financial_ratios):
        get_stock({"historical_prices": [{"date": "d", "value": "v", "open": "o"}]})

        mocked_day.assert_called_with("d", "v", "o", None, None, None)

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__map_low(self, mocked_stock, mocked_historical_prices, mocked_day, mocked_balance_sheets,
                                mocked_balance_sheet, mocked_income_statement, mocked_income_statements,
                                mocked_cash_flow, mocked_cash_flows, mocked_financial_ratio, mocked_financial_ratios):
        get_stock({"historical_prices": [{"date": "d", "value": "v", "open": "o", "low": "l"}]})

        mocked_day.assert_called_with("d", "v", "o", "l", None, None)

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__map_high(self, mocked_stock, mocked_historical_prices, mocked_day, mocked_balance_sheets,
                                 mocked_balance_sheet, mocked_income_statement, mocked_income_statements,
                                 mocked_cash_flow, mocked_cash_flows, mocked_financial_ratio, mocked_financial_ratios):
        get_stock({"historical_prices": [{"date": "d", "value": "v", "open": "o", "low": "l", "high": "h"}]})

        mocked_day.assert_called_with("d", "v", "o", "l", "h", None)

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__map_volume(self, mocked_stock, mocked_historical_prices, mocked_day, mocked_balance_sheets,
                                   mocked_balance_sheet, mocked_income_statement, mocked_income_statements,
                                   mocked_cash_flow, mocked_cash_flows, mocked_financial_ratio,
                                   mocked_financial_ratios):
        get_stock({"historical_prices": [
            {"date": "d", "value": "v", "open": "o", "low": "l", "high": "h", "volume": "v"}
        ]})

        mocked_day.assert_called_with("d", "v", "o", "l", "h", "v")

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__map_historical_prices(self, mocked_stock, mocked_historical_prices, mocked_day,
                                              mocked_balance_sheets, mocked_balance_sheet, mocked_income_statement,
                                              mocked_income_statements, mocked_cash_flow, mocked_cash_flows,
                                              mocked_financial_ratio, mocked_financial_ratios):
        stocks = get_stock({"historical_prices": [
            {"date": "d", "value": "v", "open": "o", "low": "l", "high": "h", "volume": "v"},
            {}
        ]})

        self.assertEqual("s-t-o-c-k", stocks)
        self.assertEqual(2, mocked_day.call_count)

    @staticmethod
    def _get_financial_statements():
        return {
            "balance_sheet": [{
                "financial_year": 2021,
                "total_current_liability": 26251.55,
                "total_current_asset": 15854.59,
                "total_non_current_asset": 49205.07,
                "total_shareholders_fund": 19055.97,
                "total_asset": 65059.66,
                "long_term_borrowing": 16326.77,
                "short_term_borrowings": 2542.5,
                "last_date_updated": "03-02-2022",
                "date_created": "03-02-2022"
            }],
            "income_statements": [{
                "income": -2395.44,
                "net_sale": 49325.45,
                "total_expense": 45607.95,
                "issued_shares": 38288.11,
                "date_created": "03-02-2022",
                "last_date_updated": "03-02-2022",
                "financial_year": 2021
            }],
            "cash_flows": [{
                "cash_flow_from_operating_activities": 6680.32,
                "date_created": "03-02-2022",
                "last_date_updated": "03-02-2022",
                "financial_year": 2021
            }],
            "financial_ratios": [{
                "current_ratio": 0.56,
                "gross_margin": -4.65,
                "asset_turnover_ratio": 1.22,
                "return_on_asset": 49.77,
                "financial_year": 2021,
                "date_created": "03-02-2022",
                "last_date_updated": "03-02-2022"
            }],
            "date_created": "03-02-2022",
            "last_date_updated": "03-02-2022"
        }

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__create_balance_sheets(self, mocked_stock, mocked_historical_prices, mocked_day,
                                              mocked_balance_sheets, mocked_balance_sheet, mocked_income_statement,
                                              mocked_income_statements, mocked_cash_flow, mocked_cash_flows,
                                              mocked_financial_ratio, mocked_financial_ratios):
        stocks = get_stock(self._get_financial_statements())

        self.assertEqual("s-t-o-c-k", stocks)
        mocked_balance_sheets.assert_called_with(['bs'])
        mocked_balance_sheet.assert_called_with(
            financial_year=2021,
            total_current_liability=26251.55,
            total_current_asset=15854.59,
            total_non_current_asset=49205.07,
            total_shareholders_funds=19055.97,
            total_asset=65059.66,
            long_term_borrowings=16326.77,
            short_term_borrowings=2542.5,
            date_created='03-02-2022',
            last_date_updated='03-02-2022'
        )

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__income_statement(self, mocked_stock, mocked_historical_prices, mocked_day,
                                         mocked_balance_sheets, mocked_balance_sheet, mocked_income_statement,
                                         mocked_income_statements, mocked_cash_flow, mocked_cash_flows,
                                         mocked_financial_ratio, mocked_financial_ratios):
        stocks = get_stock(self._get_financial_statements())

        self.assertEqual("s-t-o-c-k", stocks)
        mocked_income_statements.assert_called_with(['is'])
        mocked_income_statement.assert_called_with(
            financial_year=2021,
            incomes=-2395.44,
            net_sale=49325.45,
            expenses=45607.95,
            issued_shares=38288.11,
            date_created="03-02-2022",
            last_date_updated="03-02-2022"
        )

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__cash_flow(self, mocked_stock, mocked_historical_prices, mocked_day,
                                  mocked_balance_sheets, mocked_balance_sheet, mocked_income_statement,
                                  mocked_income_statements, mocked_cash_flow, mocked_cash_flows,
                                  mocked_financial_ratio, mocked_financial_ratios):
        stocks = get_stock(self._get_financial_statements())

        self.assertEqual("s-t-o-c-k", stocks)
        mocked_cash_flows.assert_called_with(['cf'])
        mocked_cash_flow.assert_called_with(
            cash_flow_from_operating_activities=6680.32,
            date_created="03-02-2022",
            last_date_updated="03-02-2022",
            financial_year=2021
        )

    @mock.patch("screener.factories.domain.stock.FinancialRatioV2", return_value="frs")
    @mock.patch("screener.factories.domain.stock.FinancialRatio", return_value="fr")
    @mock.patch("screener.factories.domain.stock.CashFlows", return_value="cfs")
    @mock.patch("screener.factories.domain.stock.CashFlow", return_value="cf")
    @mock.patch("screener.factories.domain.stock.IncomeStatements", return_value="iss")
    @mock.patch("screener.factories.domain.stock.IncomeStatement", return_value="is")
    @mock.patch("screener.factories.domain.stock.BalanceSheet", return_value="bs")
    @mock.patch("screener.factories.domain.stock.BalanceSheets", return_value="bss")
    @mock.patch("screener.factories.domain.stock.DayValue", return_value="dv")
    @mock.patch("screener.factories.domain.stock.HistoricalValues", return_value="h")
    @mock.patch("screener.factories.domain.stock.Stock", return_value="s-t-o-c-k")
    def test_get_stock__financial_statement(self, mocked_stock, mocked_historical_prices, mocked_day,
                                            mocked_balance_sheets, mocked_balance_sheet, mocked_income_statement,
                                            mocked_income_statements, mocked_cash_flow, mocked_cash_flows,
                                            mocked_financial_ratio, mocked_financial_ratios):
        stocks = get_stock(self._get_financial_statements())

        self.assertEqual("s-t-o-c-k", stocks)
        mocked_financial_ratios.assert_called_with(['fr'])
        mocked_financial_ratio.assert_called_with(
            current_ratio=0.56,
            gross_margin=-4.65,
            asset_turnover_ratio=1.22,
            return_on_asset=49.77,
            financial_year=2021,
            date_created="03-02-2022",
            last_date_updated="03-02-2022"
        )
