from collections import deque
from typing import Optional

from utils.reading_stream import CSVReadingStream, IntradayTimeReader, TimePeekable, BatchReader
from abc import abstractmethod
from pathlib import Path
from _enums import ReadingStatus, ReaderStatus

"""
QuoteReader handle reading quote files. 
"""


class TimeDataStreamReader(IntradayTimeReader, TimePeekable, BatchReader):
    READING_BATCH = 1000

    def __init__(self):
        self._stream: Optional[CSVReadingStream] = None
        self._path: Optional[Path] = None
        self._file_type: Optional[str] = None
        self._data_cache: deque = deque()
        self._date: Optional[int] = None
        self._reading_batch: Optional[int] = None
        self._intraday_time_column: Optional[str] = None
        self._intraday_time_column_IX: Optional[int] = None
        self._intraday_time: Optional[int] = None
        self._header: Optional[list] = None

        self._has_header: Optional[bool] = None
        self._encoding: Optional[str] = None
        self._delimiter: Optional[str] = None

        self.status = ReaderStatus.CLOSED
        self.set_reading_batch(self.READING_BATCH)

    @property
    def empty(self) -> bool:
        self._check_read_batch()
        return self._stream.empty and len(self._data_cache) == 0

    def _next(self):
        return self._data_cache.popleft() if not self.empty else None

    def _open_stream(self, has_header: bool = True, encoding: str = 'utf-8', delimiter: str = ','):
        self._data_cache = deque()
        self._stream = CSVReadingStream.open(self.get_path(), encoding=encoding, delimiter=delimiter)
        if has_header:
            self._header = next(self._stream)
            self._intraday_time_column_IX = self._header.index(self._intraday_time_column)
        self.status = ReaderStatus.OPEN

    def _read_util_time(self, time: int):
        record_to_return = []
        read_status: Optional[ReadingStatus] = None

        while self.peek_time() <= time and self.peek_time() is not None:
            record_to_return.append(self._next())
            if self.peek_time() is None:
                break
            if len(record_to_return) >= self._reading_batch:
                read_status = ReadingStatus.ONGOING
                break
        if read_status != ReadingStatus.ONGOING:
            self._intraday_time = time

        self.status = ReaderStatus.CLOSED if self.empty else ReaderStatus.OPEN
        read_status = ReadingStatus.DONE if read_status is None else read_status
        return record_to_return, read_status

    def set_intraday_time_column(self, time_column: str):
        self._intraday_time_column = time_column

    def get_intraday_time_column(self) -> str:
        return self._intraday_time_column

    def get_intraday_time(self) -> int:
        return self._intraday_time

    def reset_intraday_time(self):
        self._intraday_time = None

    def peek_time(self) -> Optional[int]:
        if self.empty: return None
        return int(self._data_cache[0][self._intraday_time_column_IX])

    def set_date(self, date: int):
        self._date = date

    def get_date(self) -> int:
        return self._date

    def _read_batch(self):
        for i in range(self._reading_batch):
            if self._stream.empty:
                break
            else:
                self._data_cache.append(next(self._stream))

    def set_reading_batch(self, batch_size: int):
        self._reading_batch = batch_size

    def _check_read_batch(self):
        # read more if the data cache is empty
        if len(self._data_cache) == 0:
            self._read_batch()

    def get_path(self):
        return self._path

    def set_path(self, path: Path):
        self._path = path

    def open_stream(self):
        self._open_stream(has_header=self._has_header, encoding=self._encoding,
                          delimiter=self._delimiter)
