from collections import deque
from typing import Optional, List
from abc import abstractmethod

import colorama

from _enums import ReadingStatus, ReaderStatus
from ._stream_reader import StreamReader
from request.cache.cache_basics import DataCache
from utils.reading_stream import CSVReadingStream, IntradayTimeReader, TimePeekable, BatchReader

"""
QuoteReader handle reading quote files. 
"""


class TimeDataStreamReader(StreamReader, IntradayTimeReader, TimePeekable, BatchReader):

    def __init__(self):
        super().__init__()
        self._date: Optional[int] = None
        self._intraday_time_column: Optional[str] = None
        self._intraday_time_column_IX: Optional[int] = None
        self._intraday_time: Optional[int] = None
        self.set_reading_batch(self.READING_BATCH)

    def open_stream(self, **kwargs):
        self._reader_data_queue = deque()
        if self._encoding is None:
            self._encoding = 'utf-8'
        if self._delimiter is None:
            self._delimiter = ','
        self._stream = CSVReadingStream.open(self.get_path(), encoding=self._encoding, delimiter=self._delimiter)
        if self._has_header is not None and self._has_header:
            self._header = next(self._stream)
            self._intraday_time_column_IX = self._header.index(self._intraday_time_column)
        self.status = ReaderStatus.OPEN

    def _read_upto_time(self, time: int):
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
        if self.empty:
            return None
        return int(self._reader_data_queue[0][self._intraday_time_column_IX])

    def set_date(self, date: int):
        self._date = date

    def get_date(self) -> int:
        return self._date

    @abstractmethod
    def jsonfy(self, data: List[List], time: int):
        pass

    @abstractmethod
    def tag(self, data: List[List], **kwargs):
        raise NotImplementedError("Tagging is implemented in subclass")

    def write_data_to_cache(self, data: List[List] | dict):
        if self._data_cache is None:
            raise ValueError("Timeline Cache is not set")
        tagged_data = self.tag(data)
        self._data_cache.write(tagged_data)

    def read(self, return_type: str = 'json', push_to_cache: bool = True, **kwargs):
        time = kwargs['time']
        read_until_time_data, reading_status = self._read_upto_time(time)
        self.set_reading_status(reading_status)
        match return_type:
            case 'json':
                if push_to_cache:
                    self.write_data_to_cache(read_until_time_data)
                else:
                    return self.jsonfy(read_until_time_data, time)
            case 'list':
                if push_to_cache:
                    self.write_data_to_cache(read_until_time_data)
                else:
                    return [read_until_time_data]
