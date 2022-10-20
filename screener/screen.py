from screener.common import u_yaml
from screener.factories import engine as engine_factory
from screener.factories.repositories.mongodb_client import get_stock_repository, get_index_repository
from screener.reports.yaml.factory import report as report_factory
from screener.reports.yaml.sector import reporter as sector_reporter


def screen_stock(args):
    stocks = get_stock_repository().get_active_stocks()
    config = u_yaml.read(args.config_file)
    stocks = engine_factory.get_engine(config).run(stocks)
    report = report_factory.get_stock_report(config, output_file=args.output_file)
    report.generate(stocks)


def screen_index(args):
    indexes = get_index_repository().get_all()
    config = u_yaml.read(args.config_file)
    indexes = engine_factory.get_engine(config).run(indexes)
    report = report_factory.get_index_report(config, args.output_file)
    report.generate(indexes)


_TYPE_TO_SCREENER_MAPPING = {
    "stock": screen_stock,
    "sector": sector_reporter,
    "index": screen_index
}


def screen(args):
    _TYPE_TO_SCREENER_MAPPING[args.type](args)
