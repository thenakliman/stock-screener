import functools
from typing import Dict

from screener.engine import Engine
from screener.engine import Filter, Enrich, Strategy, Strategies
from screener.filters.factory import get_filter_operation, get_enrich_operation


def get_flows(flow_name, flow_description):
    operations = []
    for flow_operations in flow_description:
        for operations_name, operation_description in flow_operations.items():
            if operations_name == "filters":
                operations.append(get_filter_operations(operation_description))
            elif operations_name == "operations":
                operations.append(get_enrich_operations(operation_description))
            else:
                raise ValueError("Value error")

    return Strategy(flow_name, operations)


def get_filter_operations(filters):
    operations = []
    for operation in filters:
        operation_parameters = operation["parameters"] if "parameters" in operation else {}
        filter_operation = functools.partial(get_filter_operation(operation["name"]), **operation_parameters)
        operations.append(filter_operation)

    return Filter(operations)


def get_enrich_operations(enrich_operations):
    operations = []
    for operation in enrich_operations:
        operation_parameters = operation["parameters"] if "parameters" in operation else {}
        enrich_operation = functools.partial(get_enrich_operation(operation["name"]), **operation_parameters)
        operations.append(enrich_operation)

    return Enrich(operations)


def get_engine(config):
    strategies = get_strategies(config["strategies"])
    return Engine(strategies)


def get_operations(config: Dict) -> Enrich:
    output_config = config.get("output", {})
    return get_enrich_operations(output_config.get("operations", {}))


def get_strategies(config):
    flows = [get_flows(flow_name, description) for flow_name, description in config.items()]
    return Strategies(flows)
