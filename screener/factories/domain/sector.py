from typing import List, Callable

from screener.common import date
from screener.domain.fundamental.sector import Sector
from screener.filters.index.near_max_filter import WORKING_DAYS_IN_YEAR

_SECTORS = {}


def update_sector_in_stocks(stocks):
    valid_stocks = [stock for stock in stocks if stock is not None]
    sector_wise_stocks = {}
    for stock in valid_stocks:
        if stock.get_sector_name() in sector_wise_stocks:
            sector_wise_stocks[stock.get_sector_name()].append(stock)
        else:
            sector_wise_stocks[stock.get_sector_name()] = [stock]

    for sector_name, stocks_in_sector in sector_wise_stocks.items():
        _SECTORS[sector_name] = create_sector(sector_name, stocks_in_sector)


def _average(value_callable: Callable, objects: List) -> float:
    sum_ = 0
    count = 0
    for object_ in objects:
        try:
            sum_ += value_callable(object_)
        except Exception:
            pass
        else:
            count += 1

    return sum_ / count if count != 0 else 0


def _sum(value_callable: Callable, objects: List) -> float:
    sum_ = 0
    for object_ in objects:
        try:
            sum_ += value_callable(object_)
        except Exception:
            pass

    return sum_


def _eliminate_incomplete_data(stocks, in_years: float):
    return [stock for stock in stocks
            if len(stock.get_historical_prices()) >= int(in_years * WORKING_DAYS_IN_YEAR)]


def get_historical_prices(stocks, in_years: float = 0.05):
    days = int(in_years * WORKING_DAYS_IN_YEAR)
    prices = []
    stocks = _eliminate_incomplete_data(stocks, in_years)
    weights = []
    total_market_capital = sum((stock.get_market_capital() for stock in stocks))
    for stock in stocks:
        weights.append(stock.get_market_capital() / total_market_capital)
        number_of_days_stock_available_in_market = len(stock.get_historical_prices())
        start_index = number_of_days_stock_available_in_market - days
        prices.append(stock.get_historical_prices()[start_index:])

    if len(prices) == 0:
        return []

    historical_prices = []
    days = min(days, len(prices[0]))
    for i in range(days - 1, -1, -1):
        value = 0
        for index, price in enumerate(prices):
            value += ((float(price[i]["value"]) * weights[index]) / float(price[0]["value"]))

        historical_prices.append({
            "value": value,
            "date": prices[0][i]["date"]
        })
    return historical_prices


def _average_net_sales(stocks, latest_year, for_year):
    stocks_with_data = []
    for stock in stocks:
        try:
            stock.get_net_sales_for_year(latest_year - for_year + 1)
        except Exception:
            pass
        else:
            stocks_with_data.append(stock)
    # pylint: disable=cell-var-from-loop
    return [{
        "year": year,
        "sale": _sum(lambda stock: stock.get_net_sales_for_year(year), stocks_with_data)} for year in
        range(latest_year - for_year + 1, latest_year + 1, 1)
    ]


def create_sector(name, stocks):
    market_leader = max(stocks, key=lambda stock: stock.get_market_capital())
    market_leader.mark_market_leader()
    latest_year = date.current_year()
    for_year = 3
    sector = Sector(
        name=name,
        market_leader=market_leader,
        pe=_average(lambda stock: stock.get_pe(), stocks),
        price_to_book=_average(lambda stock: stock.get_price_to_book_value(), stocks),
        asset_turn_over=_average(lambda stock: stock.calculate_asset_turnover(latest_year), stocks),
        current_ratio=_average(lambda stock: stock.get_current_ratio(latest_year), stocks),
        gross_margin=_average(lambda stock: stock.get_gross_margin(latest_year), stocks),
        net_sales=_average_net_sales(stocks, latest_year, for_year),
        return_on_asset=_average(lambda stock: stock.calculate_return_on_asset(latest_year), stocks),
        debt_to_equity=_average(lambda stock: stock.get_debt_to_equity_ratio(latest_year), stocks),
        market_capital=sum((stock.get_market_capital() for stock in stocks)),
        historical_values=get_historical_prices(stocks),
        stocks=stocks,
        return_on_equity=0,  # todo: to be implemented
    )
    list(map(lambda stock: stock.update_sector(sector), stocks))
    return sector


def get_sectors(stocks):
    sector_wise_stocks = {}
    for stock in stocks:
        if stock.get_sector_name() in sector_wise_stocks:
            sector_wise_stocks[stock.get_sector_name()].append(stock)
        else:
            sector_wise_stocks[stock.get_sector_name()] = [stock]

    return [create_sector(sector_name, stocks_in_sector)
            for sector_name, stocks_in_sector in sector_wise_stocks.items()]
