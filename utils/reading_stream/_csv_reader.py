from pathlib import Path
from typing import Type, Optional, List, Any, Iterator

from ._reading_stream import ReadingStream


def csv_iter_generator(file_path: Path, encoding, delimiter):
    with file_path.open(mode='r', encoding=encoding) as file:
        for line in file:
            # get rid of the newline character
            line = line.strip()
            yield line.split(delimiter)


class CSVReadingStream(ReadingStream):
    def __init__(self, encoding: str = 'utf-8', delimiter: str = ','):
        super().__init__(encoding)
        self._delimiter = delimiter

    def _open(self, file_path: Path):
        self._generator = csv_iter_generator(file_path, encoding=self._encoding, delimiter=self._delimiter)
        try:
            self._next = next(self._generator)
        except StopIteration:
            self._empty = True

    @classmethod
    def open(cls, file_path: Path, encoding: str, **kwargs):
        delimiter = kwargs.get('delimiter', ',')
        new_stream = CSVReadingStream(encoding=encoding, delimiter=delimiter)
        new_stream._open(file_path)
        return new_stream
