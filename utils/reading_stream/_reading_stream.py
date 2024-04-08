from pathlib import Path
from typing import Type, Optional, List, Any, Iterator

from abc import ABC, abstractmethod


class ReadingStream(ABC):

    def __init__(self, encoding: str = 'utf-8'):
        self._empty: bool = False
        self._next: Optional[List[Any]] = None
        self._generator: Optional[Type[Iterator]] = None
        self._encoding = encoding

    @property
    def empty(self) -> bool:
        return self._empty

    @abstractmethod
    def _open(self, file_path: Path):
        pass

    def __iter__(self):
        return self

    def __next__(self) -> List[Any]:
        """
        Return the self.peek element, or raise StopIteration
        if empty
        """
        if self._empty:
            raise StopIteration()
        to_return = self._next
        try:
            self._next = next(self._generator)
        except StopIteration:
            self._next = None
            self._empty = True
        return to_return

    @classmethod
    @abstractmethod
    def open(cls, file_path: Path, encoding: str, **kwargs) -> 'ReadingStream':
        pass
