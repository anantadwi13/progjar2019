import json


class Config:
    def __init__(self, config_file=None):
        with open('../server_data/config.json' if config_file is None else config_file, 'r') as config:
            self.config = json.loads(config.read())

    @property
    def get_config(self):
        return self.config
