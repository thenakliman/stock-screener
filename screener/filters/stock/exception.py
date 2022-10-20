def log_exception(func):
    def new_func(stock, *args, **kwargs):
        try:
            return func(stock, *args, **kwargs)
        except Exception as e:
            print("failed isinid: ", stock.get_isinid(), e)
            raise e

    return new_func
