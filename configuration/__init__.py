import json


class Configuration:
    def __init__(self):
        with open('configuration.json', 'r') as configuration_file:
            configuration_file_content = configuration_file.read()
            json.loads(configuration_file_content)
