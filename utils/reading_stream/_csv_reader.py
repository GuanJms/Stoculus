from pathlib import Path
from typing import Type, Optional, List, Any, Iterator
from xmlrpc.client import Boolean


def csv_iter_generator(file_path: Path, encoding, delimiter):
    with file_path.open(mode='r', encoding=encoding) as file:
        for line in file:
            # get rid of the newline character
            line = line.strip()
            yield line.split(delimiter)


class CSVReadingStream:
    def __init__(self, encoding: str = 'utf-8', delimiter: str = ','):
        self._empty: Boolean = False
        self._next: Optional[List[Any]] = None
        self._generator: Optional[Type[Iterator]] = None
        self._encoding = encoding
        self._delimiter = delimiter

    def _open(self, file_path: Path):
        self._generator = csv_iter_generator(file_path, encoding=self._encoding, delimiter=self._delimiter)
        try:
            self._next = next(self._generator)
        except StopIteration:
            self._empty = True

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

    @property
    def empty(self) -> Boolean:
        return self._empty

    @classmethod
    def open(cls, file_path: Path, encoding: str, delimiter: str):
        new_stream = CSVReadingStream(encoding= encoding, delimiter=delimiter)
        new_stream._open(file_path)
        return new_stream
