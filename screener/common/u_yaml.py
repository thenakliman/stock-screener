import yaml


def read(name):
    with open(name, "r", encoding='utf-8') as stream:
        return yaml.safe_load(stream)


def write(name, data):
    with open(name, "a", encoding='utf-8') as stream:
        yaml.dump(data, stream, default_flow_style=False, sort_keys=False)
