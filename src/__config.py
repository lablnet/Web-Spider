import json


def get_config(config):
    file = open("config.json", "r")
    data = file.read()
    configuration = json.loads(data)
    if config in configuration:
        return configuration[config]
    else:
        return None
