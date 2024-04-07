from abc import ABC, abstractmethod


class IntradayTimeReader(ABC):

    @abstractmethod
    def set_intraday_time_column(self, time_column: str):
        pass

    @abstractmethod
    def get_intraday_time_column(self) -> str:
        pass

    @abstractmethod
    def get_intraday_time(self) -> int:
        pass

    @abstractmethod
    def reset_intraday_time(self):
        pass

    @abstractmethod
    def set_date(self, date: int):
        pass

    @abstractmethod
    def get_date(self) -> int:
        pass


class TimePeekable(ABC):
    @abstractmethod
    def peek_time(self) -> int:
        pass


class BatchReader(ABC):

    @abstractmethod
    def _read_batch(self):
        pass

    @abstractmethod
    def set_reading_batch(self, batch_size: int):
        pass

    @abstractmethod
    def _check_read_batch(self):
        pass




