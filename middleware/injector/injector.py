import os
from typing import List, Optional


class Injector:

    BASE_PATH = "D:\\TempDataHouse"

    def __init__(self):
        self._logger_path: Optional[str] = None

    def get_logger_path(self):
        if self._logger_path is None:
            raise ValueError("Logger path is not set")
        return os.path.join(self.BASE_PATH, self._logger_path)

    def check_existence(self, sub_path_list: List[str]):
        path = self.get_path(sub_path_list)
        return os.path.exists(path)

    def get_path(self, sub_path_list: List[str]):
        return os.path.join(self.BASE_PATH, *sub_path_list)

    def create_directory(self, sub_path_list: List[str]):
        if self.check_existence(sub_path_list):
            return
        path = self.get_path(sub_path_list)
        os.makedirs(path)






