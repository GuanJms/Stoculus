from collections import deque
from typing import Optional, List

from _enums import ReadingStatus


class DataCache:

    def __init__(self, token: str):
        self._token = token
        self._status: Optional[ReadingStatus] = ReadingStatus.INACTIVATE
        self._cache: deque = deque()

    def __str__(self):
        return f"DataCache {self._token} with status {self._status}"

    @property
    def token(self) -> str:
        return self._token

    @property
    def status(self) -> ReadingStatus:
        return self._status

    def add(self, data):
        self._cache.append(data)

    def pop(self):
        return self._cache.popleft()

    def is_empty(self):
        return len(self._cache) == 0

    def set_status(self, status: ReadingStatus):
        self._status = status

    def write(self, data: dict, **kwargs):
        self._cache.append(data)

    def read(self) -> List[dict]:
        result = []
        while not self.is_empty():
            result.append(self._cache.popleft())
        # print(f"DataCache {self._token} read {result} records")
        return result









