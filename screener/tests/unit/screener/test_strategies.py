import unittest
from unittest import mock

from screener.engine import Engine
from screener.engine import Filter, Enrich, Strategy, Strategies
from screener.exceptions.not_found import DataNotFound


class EngineTest(unittest.TestCase):
    def test_run_call_generate_report_and_strategies(self):
        filtered_stocks = [1, 2, 3]
        apply = mock.Mock(return_value=filtered_stocks)
        strategies = mock.Mock(apply=apply)
        engine = Engine(strategies)
        stocks = [1, 2, 3, 4]

        engine.run(stocks)

        apply.assert_called_with(stocks)


class FilterTest(unittest.TestCase):
    def test_filter(self):
        f = Filter([lambda x: x.k % 2 == 0, lambda x: x.k % 3 == 0])
        stock_k_2 = mock.Mock(k=2)
        stock_k_6 = mock.Mock(k=6)
        stock_k_3 = mock.Mock(k=3)
        stocks = [stock_k_2, stock_k_3, mock.Mock(k=5), stock_k_6]

        fs = list(f.apply(stocks))
        print(fs)
        self.assertListEqual([stock_k_6], fs)

    def test_filter__fails(self):
        f = Filter([lambda x: x.k % 2 == 0, lambda x: 3 + []])
        stock_k_2 = mock.Mock(k=2)
        stock_k_9 = mock.Mock(k=9)
        stocks = [stock_k_2, mock.Mock(k=3), mock.Mock(k=5), stock_k_9]

        fs = f.apply(stocks)

        self.assertListEqual([], list(fs))

    def test_filter__fails_with_data_not_found(self):
        def k(x):
            if x.k % 3:
                raise DataNotFound()
            return False

        f = Filter([lambda x: x.k % 2 == 0, k])
        stock_k_2 = mock.Mock(k=2)
        stock_k_9 = mock.Mock(k=9)
        stocks = [stock_k_2, mock.Mock(k=3), mock.Mock(k=5), stock_k_9]

        fs = f.apply(stocks)

        self.assertListEqual([], list(fs))


class EnrichTest(unittest.TestCase):
    def test_enrich(self):
        called_1 = []
        called_2 = []
        f = Enrich([
            lambda x: called_1.append(x.k) if x.k % 2 == 0 else 1,
            lambda x: called_2.append(x.k) if x.k % 3 == 0 else 1
        ])
        stocks = [mock.Mock(k=2), mock.Mock(k=3), mock.Mock(k=6)]

        f.apply(stocks)

        self.assertListEqual(called_1, [2, 6])
        self.assertListEqual(called_2, [3, 6])

    def test_enrich_fail(self):
        called_1 = []
        called_2 = []
        f = Enrich([
            lambda x: called_1.append(x.k) if x.k % 2 == 0 else 1,
            lambda x: called_2.append(x.k) if x.k % 3 == 0 else 1 + []
        ])
        stocks = [mock.Mock(k=2), mock.Mock(k=3), mock.Mock(k=6)]

        f.apply(stocks)

        self.assertListEqual(called_1, [2, 6])
        self.assertListEqual(called_2, [3, 6])

    def test_enrich__fails_with_data_not_found(self):
        called_1 = []
        called_2 = []

        def k(x):
            if x.k % 3 == 0:
                raise DataNotFound()
            return called_2.append(x.k)

        f = Enrich([lambda x: called_1.append(x.k) if x.k % 2 == 0 else 1, k])
        stocks = [mock.Mock(k=2), mock.Mock(k=3), mock.Mock(k=6)]

        f.apply(stocks)

        self.assertListEqual(called_2, [2])
        self.assertListEqual(called_1, [2, 6])


class StrategyTest(unittest.TestCase):
    def test_strategy(self):
        s = Strategy("s1", [
            mock.Mock(apply=lambda x: x[:-1]),
            mock.Mock(apply=lambda x: x[1:])
        ])

        ops = []
        s.apply([
            mock.Mock(x=1, update_satisfied_strategy=lambda x: ops.append((x, 1))),
            mock.Mock(x=2, update_satisfied_strategy=lambda x: ops.append((x, 2))),
            mock.Mock(x=3, update_satisfied_strategy=lambda x: ops.append((x, 3))),
            mock.Mock(x=4, update_satisfied_strategy=lambda x: ops.append((x, 4)))
        ])

        self.assertListEqual(ops, [("s1", 2), ("s1", 3)])


class StrateiesTest(unittest.TestCase):
    def test_strategy(self):
        s = Strategies([
            mock.Mock(apply=lambda x: x[1:-1]),
            mock.Mock(apply=lambda x: x[1:])
        ])

        stock_2 = mock.Mock(x=2)
        stock_4 = mock.Mock(x=4)

        self.assertSetEqual({stock_2, stock_4}, s.apply([mock.Mock(x=1), stock_2, stock_4]))
