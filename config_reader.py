import json


class ConfigReader:
    __instance = None

    def __init__(self, config_file="config.json"):
        if ConfigReader.__instance is not None:
            raise Exception("Singleton cannot be instantiated more than once!")
        else:
            ConfigReader.__instance = self
            self.config_file = config_file
            self.__read_from_config()

    @staticmethod
    def get_instance():
        if ConfigReader.__instance is None:
            ConfigReader.__instance = ConfigReader()

        return ConfigReader.__instance

    def __read_from_config(self):
        with open(self.config_file) as file:
            data = json.load(file)

        try:
            self.interest_percentage = data['interest_percentage']
            self.m = data['m']
            self.quantiles = data['quantiles']
            self.k = data['k']
            self.elbow_iter = data['elbow_iter']
            self.silhouette_iter = data['silhouette_iter']
            self.input_file = data['input_file']
            self.rrfm_file = data['rrfm_file']
            self.date = data['date']
        except KeyError:
            raise KeyError("No such key in config file!")
