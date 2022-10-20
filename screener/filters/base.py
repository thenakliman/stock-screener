from screener.exceptions.not_found import YearNotFound, DataNotFound


def apply_operation_by_years(method, years):
    results = []
    for year in years:
        try:
            results.append(method(year))
        except YearNotFound as e:
            print(e)
        except DataNotFound:
            print("Data not found")
        except Exception as e:
            print(e, apply_operation_by_years.__name__)

    return results
