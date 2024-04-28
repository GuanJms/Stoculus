from configuration import ConfigurationManager
from abc import ABC, abstractmethod
import os
import json


class MetaManager(ABC):

    def __init__(self):
        self.root_path = ConfigurationManager.get_root_system()
        self.meta_path = ConfigurationManager.get_meta_config()
        self.meta = None

    def get_meta(self):
        return self.meta

    @staticmethod
    def read_json(path):
        MetaManager.check_path_exists_error(path)
        with open(path, 'r') as file:
            return json.load(file)

    @staticmethod
    def overwrite_json(path, data):
        with open(path, 'w') as file:
            json.dump(data, file)

    # @staticmethod
    # def update_json(path, data):
    #     existing_data = MetaManager.read_json(path)
    #     existing_data.update(data)
    #     MetaManager.overwrite_json(path, existing_data)

    @staticmethod
    def get_directories(path):
        MetaManager.check_path_exists_error(path)
        entries = os.listdir(path)
        return [name for name in entries if os.path.isdir(os.path.join(path, name))]

    @abstractmethod
    def load_meta(self, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @staticmethod
    def check_path_exists_error(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path does not exist: {path}")

