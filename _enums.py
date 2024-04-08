from enum import Enum, auto


class ReadingStatus(Enum):
    DONE = auto()
    ONGOING = auto()
    INACTIVATE = auto()


class ReaderStatus(Enum):
    OPEN = auto()
    CLOSED = auto()
    ERROR = auto()


class DomainEnum(Enum):
    def to_string(self):
        return self.name.upper()


class AssetDomain(DomainEnum):
    EQUITY = auto()


class EquityDomain(DomainEnum):
    STOCK = auto()
    OPTION = auto()


class PriceDomain(DomainEnum):
    TRADED = auto()
    QUOTE = auto()
    TRADED_QUOTE = auto()
