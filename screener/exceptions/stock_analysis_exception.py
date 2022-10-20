class StockAnalysisException(Exception):
    message = "Internal Error"

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return self.message.format(**self.kwargs)


class InvalidException(StockAnalysisException):
    message = "Invalid"
