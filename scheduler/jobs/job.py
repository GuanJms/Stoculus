from typing import Optional

from scheduler.jobs.job_frequency_enum import JobFrequency
from abc import ABC, abstractmethod


class Job(ABC):

    def __init__(self):
        self._description: Optional[str] = None
        self._frequency: Optional[JobFrequency] = None

    @property
    def description(self):
        return self._description

    @property
    def frequency(self):
        return self._frequency

    @abstractmethod
    def run(self, **kwargs):
        pass
