from screener.common import u_yaml
from screener.factories.repositories.mongodb_client import get_sector_repository
from screener.reports.yaml.factory.report import get_report


def reporter(args):
    config = u_yaml.read(args.config_file)
    report = get_report(report_type="sector", config=config, output_file=args.output_file)
    sectors = get_sector_repository().get_all_sectors()
    return report.generate(sectors)
