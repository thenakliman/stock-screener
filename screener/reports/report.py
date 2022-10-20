from screener.reports.yaml import (
    index,
    sector,
    stock
)

_REPORTER_MAPPING = {
    "stock": stock.reporter,
    "sector": sector.reporter,
    "index": index.reporter
}


def reporter(args):
    _REPORTER_MAPPING[args.type](args)
