from .job import Job
from .job_frequency_enum import JobFrequency


class UpdateTickerJob(Job):

    def __init__(self):
        super().__init__()
        self._description = "Update ticker data"
        self._frequency = JobFrequency.DAILY

    def run(self, **kwargs):
        from data_meta.ticker_meta_manager import TickerMetaManager
        ticker_meta_manager = TickerMetaManager()
        ticker_meta_manager.update()
