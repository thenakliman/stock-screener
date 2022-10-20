import argparse

from screener.screen import screen
from screener.reports.report import reporter


def get_parser():
    parser = argparse.ArgumentParser(description="Stock screener command line interface",
                                     prog="stock-screener")

    parser.add_argument("-p", "--process",
                        type=int,
                        default=8)

    subparsers = parser.add_subparsers(help="Stock screener command help")
    analyse_sub_command_parser = subparsers.add_parser("screen", help="screen based on available type")
    analyse_sub_command_parser.add_argument("-t", "--type",
                                            choices=["stock",
                                                     "sector",
                                                     "index"],
                                            default="stock")
    analyse_sub_command_parser.add_argument("-c", "--config-file",
                                            required=True)
    analyse_sub_command_parser.add_argument("-o", "--output-file",
                                            default="./filtered-companies.yaml")
    analyse_sub_command_parser.set_defaults(func=screen)

    reporter_sub_command_parser = subparsers.add_parser("report", help="Generate report for given companies")
    reporter_sub_command_parser.add_argument("-r", "--type",
                                             choices=["stock",
                                                      "sector",
                                                      "index"],
                                             default="stock")
    reporter_sub_command_parser.add_argument("-c", "--config-file",
                                             required=True)
    reporter_sub_command_parser.add_argument("-o", "--output-file",
                                             default="./filtered-companies.yaml")
    reporter_sub_command_parser.add_argument("-u", "--username", required=True)
    reporter_sub_command_parser.set_defaults(func=reporter)

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
        return

    func(args)
