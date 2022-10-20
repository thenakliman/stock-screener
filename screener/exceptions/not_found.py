from screener.exceptions.stock_analysis_exception import StockAnalysisException


class NotFound(StockAnalysisException):
    message = "Not found"


class CurrentPriceNotFound(NotFound):
    message = "Current price not found for security isinid: {isinid}"


class HistoricalPricesIsNotAvailable(NotFound):
    message = "Historical prices are not available"


class YearNotFound(NotFound):
    message = "year: {year} not found"


class DataNotFound(NotFound):
    message = "Data not found in {data} for year: {year}"


class CashFlowNotFound(NotFound):
    message = "Cash flow not found for {year}"


class BalanceSheetNotFound(NotFound):
    message = "Balance sheet not found for {year}"


class FinancialRatioNotFound(NotFound):
    message = "Financial ratio not found for {year}"


class IncomeStatementNotFound(NotFound):
    message = "Income statement not found for {year}"


class ReportDataNotFound(NotFound):
    message = "Data not found in stock details: {data}"
