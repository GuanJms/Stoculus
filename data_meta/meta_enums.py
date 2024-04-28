from enum import Enum, auto


class MetaEnum(Enum):
    TICKER = auto()
    OPTION = auto()

    def to_string(self):
        return self.name.upper()
