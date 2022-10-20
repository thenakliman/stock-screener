import copy


def merge_dict(dict2: dict, dict1: dict):
    for key, value in dict1.items():
        if key in dict2:
            if isinstance(dict2[key], dict):
                merge_dict(dict2[key], dict1[key])
            elif isinstance(dict2[key], list):
                dict2[key].extend(dict1[key])
            # NOTE(thenakliman): If use case comes then we might have to
            # consider list merging if they are being under the
            # same key. Waiting for use case.
        else:
            dict2[key] = copy.deepcopy(value)
