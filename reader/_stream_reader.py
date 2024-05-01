from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from collections import deque
from pathlib import Path
from typing import Optional

from _enums import ReaderStatus, ReadingStatus, DomainEnum

if TYPE_CHECKING:
    from request.cache.cache_basics import DataCache
from utils.reading_stream import ReadingStream


class StreamReader(ABC):
    READING_BATCH = 1000

    def __init__(self):
        self._stream: Optional[ReadingStream] = None
        self._path: Optional[Path] = None
        self._file_type: Optional[str] = None
        self._reader_data_queue: deque = deque()
        self._reading_batch: Optional[int] = None
        self._header: Optional[list] = None
        self._has_header: Optional[bool] = None
        self._encoding: Optional[str] = None
        self._delimiter: Optional[str] = None
        self.status = ReaderStatus.CLOSED
        self._data_cache: Optional['DataCache'] = None
        self._reading_status: Optional[ReadingStatus] = None
        self._domains: List[DomainEnum] = []

    def __str__(self):
        return f"{self.__class__.__name__} @{self._path if self._path else ''} with status {self.status}"

    @property
    def empty(self) -> bool:
        self._check_read_batch()
        return self._stream.empty and len(self._reader_data_queue) == 0

    @property
    def reading_status(self) -> ReadingStatus:
        return self._reading_status

    @property
    def domains(self) -> List[DomainEnum]:
        return self._domains

    def _next(self):
        return self._reader_data_queue.popleft() if not self.empty else None

    def _read_batch(self):
        for i in range(self._reading_batch):
            if self._stream.empty:
                break
            else:
                self._reader_data_queue.append(next(self._stream))

    def _check_read_batch(self):
        # read more if the data cache is empty
        if len(self._reader_data_queue) == 0:
            self._read_batch()

    def set_reading_batch(self, batch_size: int):
        self._reading_batch = batch_size

    def get_path(self):
        return self._path

    def set_path(self, path: Path):
        self._path = path

    def set_data_cache(self, data_cache: 'DataCache'):
        self._data_cache = data_cache

    def set_reading_status(self, reading_status: ReadingStatus):
        self._reading_status = reading_status

    def get_param(self, param: str):
        if hasattr(self, param):
            return getattr(self, param)
        if hasattr(self, f'_{param}'):
            return getattr(self, f'_{param}')
        return None


    @abstractmethod
    def read(self, return_type: str = 'json', push_to_cash:bool = True, **kwargs):
        pass

    @abstractmethod
    def open_stream(self, has_header: bool = True, encoding: str = 'utf-8', delimiter: str = ',', **kwargs):
        pass

    @abstractmethod
    def tag(self, data: List[List], **kwargs):
        raise NotImplementedError("Tagging is implemented in subclass")


