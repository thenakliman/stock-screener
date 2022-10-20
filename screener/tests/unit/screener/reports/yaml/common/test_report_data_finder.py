import unittest

from screener.exceptions.not_found import ReportDataNotFound
from screener.reports.yaml.common.report_data_finder import find


class TestFind(unittest.TestCase):
    def test_find__map_name(self):
        self.assertEqual("weird", find("name", {"report_data": {"name": "weird"}}))

    def test_find__map_satisfied_strategies(self):
        self.assertListEqual(["a"], find("satisfied_strategies", {"satisfied_strategies": ["a"]}))

    def test_find__map_score(self):
        self.assertEqual(3, find("score", {"score": 3}))

    def test_find__map_sector(self):
        self.assertEqual("abc", find("sector", {"report_data": {"sector": "abc"}}))

    def test_find__map_not_met_criteria(self):
        self.assertListEqual(["abc"], find("not_met_criterias", {"missed_criteria": ["abc"]}))

    def test_find__met_criteria(self):
        self.assertListEqual(["abc"], find("met_criteria", {"satisfied_criteria": ["abc"]}))

    def test_find__map_isinid(self):
        self.assertEqual("INC424324", find("isinid", {"report_data": {"isinid": "INC424324"}}))

    def test_find__map_asset_turnover(self):
        self.assertEqual(["INC424324"], find("asset_turnover", {"report_data": {"asset_turnover": ["INC424324"]}}))

    def test_find__map_cash_flows(self):
        self.assertEqual(["INC424324"], find("cash_flows", {"report_data": {"cash_flows": ["INC424324"]}}))

    def test_find__map_current_price(self):
        self.assertEqual(123, find("current_price", {"report_data": {"current_price": 123}}))

    def test_find__map_current_ratio(self):
        self.assertEqual(["INC424324"], find("current_ratio", {"report_data": {"current_ratio": ["INC424324"]}}))

    def test_find__map_debt(self):
        self.assertEqual(["INC424324"], find("debt", {"report_data": {"debt": ["INC424324"]}}))

    def test_find__map_financial_year(self):
        self.assertEqual("123", find("financial_year", {"report_data": {"financial_year": "123"}}))

    def test_find__map_graham_number(self):
        self.assertEqual(123, find("graham_number", {"report_data": {"graham_number": 123}}))

    def test_find__map_gross_margin(self):
        self.assertEqual(["INC424324"], find("gross_margin", {"report_data": {"gross_margin": ["INC424324"]}}))

    def test_find__map_incomes(self):
        self.assertEqual(["INC424324"], find("incomes", {"report_data": {"incomes": ["INC424324"]}}))

    def test_find__map_industry_pe(self):
        self.assertEqual(123, find("industry_pe", {"report_data": {"industry_pe": 123}}))

    def test_find__map_less_than_maximum_price(self):
        self.assertEqual(123, find("less_than_maximum_price", {"report_data": {"less_than_maximum_price": 123}}))

    def test_find__map_market_capital(self):
        self.assertEqual(123, find("market_capital", {"report_data": {"market_capital": 123}}))

    def test_find__map_long_term_debts(self):
        self.assertEqual(["INC424324"], find("long_term_debts", {"report_data": {"long_term_debts": ["INC424324"]}}))

    def test_find__map_maximum_price(self):
        self.assertEqual(123, find("maximum_price", {"report_data": {"maximum_price": 123}}))

    def test_find__map_minimum_price(self):
        self.assertEqual(123, find("minimum_price", {"report_data": {"minimum_price": 123}}))

    def test_find__map_more_than_minimum_price(self):
        self.assertEqual(123, find("more_than_minimum_price", {"report_data": {"more_than_minimum_price": 123}}))

    def test_find__map_new_issued_shares(self):
        self.assertEqual(123, find("new_issued_shares", {"report_data": {"new_issued_shares": 123}}))

    def test_find__map_net_sale(self):
        self.assertEqual(["INC424324"], find("net_sale", {"report_data": {"net_sale": ["INC424324"]}}))

    def test_find__map_operating_cash_flow(self):
        self.assertEqual(["INC424324"],
                         find("operating_cash_flow", {"report_data": {"operating_cash_flow": ["INC424324"]}}))

    def test_find__map_return_on_assets(self):
        self.assertEqual(["INC424324"],
                         find("return_on_assets", {"report_data": {"return_on_assets": ["INC424324"]}}))

    def test_find__map_tags(self):
        self.assertEqual(["INC424324"],
                         find("tags", {"report_data": {"tags": ["INC424324"]}}))

    def test_find__map_pe(self):
        self.assertEqual(123, find("pe", {"report_data": {"pe": 123}}))

    def test_find__map_price_to_book(self):
        self.assertEqual(123, find("price_to_book", {"report_data": {"price_to_book": 123}}))

    def test_find__map_latest_debt_to_equity(self):
        self.assertEqual(123, find("latest_debt_to_equity", {"report_data": {"latest_debt_to_equity": 123}}))

    def test_find__minus_one_when_data_is_not_available(self):
        self.assertEqual(-1, find("latest_debt_to_equity", {"report_data": {"ok": 123}}))

    def test_find__map_debt_to_equity(self):
        self.assertListEqual([123], find("debt_to_equity", {"report_data": {"debt_to_equity": [123]}}))

    def test_find__map_latest_debt_to_equity_when_debt_to_equity_is_none(self):
        self.assertEqual(-1, find("latest_debt_to_equity", {"report_data": {"equity": None}}))

    def test_find__map_latest_debt_to_equity_when_debt_to_equity_length_is_zero(self):
        self.assertEqual(-1, find("latest_debt_to_equity", {"report_data": {"equity": []}}))

    def test_find__map_market_leader(self):
        self.assertEqual(True, find("market_leader", {"report_data": {"market_leader": True}}))

    def test_find__map_total_issued_shares(self):
        self.assertEqual(123, find("total_issued_shares", {"report_data": {"total_issued_shares": 123}}))

    def test_find__raise_exception__key_not_found(self):
        with self.assertRaises(ReportDataNotFound):
            find("total_issued_shardsfes", {"report_data": {"total_issued_shares": 123}})
