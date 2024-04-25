from typing import Optional, List

from _enums import DomainEnum
from path import PathManager


class LocalValidator:

    def __init__(self):
        self._domain: Optional[List[DomainEnum]] = None

    def get_domain_path(self):
        _path = PathManager.get_director_path(self._domain)
