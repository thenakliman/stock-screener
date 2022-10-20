_INDEX_FILTERS = {}

FILTER_OPERATION_KEY = "filters"
ENRICH_OPERATION_KEY = "enrich"

_OPERATIONS = {
    FILTER_OPERATION_KEY: {},
    ENRICH_OPERATION_KEY: {}
}


def register(operation_type, filter_name, filter_operation):
    _OPERATIONS[operation_type][filter_name] = filter_operation


def register_filter_operation(filter_name):
    def decorator_func(decorated_func):
        def actual_assigned_func(stock, *args, **kwargs):
            return decorated_func(stock, *args, **kwargs)

        register(FILTER_OPERATION_KEY, filter_name, actual_assigned_func)
        return actual_assigned_func

    return decorator_func


def register_enrich_operation(operation_name):
    def decorator_func(decorated_func):
        def actual_assigned_func(stock, *args, **kwargs):
            value = decorated_func(stock, *args, **kwargs)
            if value is not None:  # todo: find clean solution. Not a enrich operator
                if value:
                    stock.update_success_operation_status(operation_name)
                else:
                    stock.update_failed_operation_status(operation_name)

            return value

        register(ENRICH_OPERATION_KEY, operation_name, actual_assigned_func)
        return decorated_func

    return decorator_func


def get_filter_operation(filter_operation_name):
    return _OPERATIONS[FILTER_OPERATION_KEY][filter_operation_name]


def get_enrich_operation(enrich_operation_name):
    return _OPERATIONS[ENRICH_OPERATION_KEY][enrich_operation_name]
