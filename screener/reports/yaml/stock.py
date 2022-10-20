# todo: fix reporting part
from screener.common import u_yaml
from screener.factories.repositories.mongodb_client import get_stock_repository
from screener.reports.yaml.factory.report import get_report


def reporter(args):
    stock_client = get_stock_repository()
    config = u_yaml.read(args.config_file)
    stocks = [stock_client.get_by_id(company) for company in config["companies"]]
    get_report(report_type="stock", config=config, output_file=args.output_file).generate(stocks)
