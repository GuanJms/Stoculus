from pathlib import Path
from typing import Optional, List

from _enums import DomainEnum
from path import PathManager


class LocalValidator:

    def __init__(self):
        self._domain: Optional[List[DomainEnum]] = None

    def get_director_path(self):
        path = PathManager.get_director_path(self._domain)
        return path

    def _check_existence(self, sub_path: List[str]):
        path = self.get_director_path()
        try:
            for sub in sub_path:
                path = path / sub
        except Exception as e:
            raise ValueError(f"Invalid sub path: {sub_path}")
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")






