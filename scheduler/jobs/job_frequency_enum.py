from enum import Enum, auto


class JobFrequency(Enum):
    DAILY = auto()
    WEEKLY = auto()

    @classmethod
    def from_str(cls, frequency):
        frequency = frequency.upper()
        if frequency == "DAILY":
            return cls.DAILY
        elif frequency == "WEEKLY":
            return cls.WEEKLY
        else:
            raise ValueError(f"Invalid frequency: {frequency}")
