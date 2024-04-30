from .job import Job
from .job_frequency_enum import JobFrequency


class UpdateOptionExpsJob(Job):

    def __init__(self):
        super().__init__()
        self._description = "Update option expirations data"
        self._frequency = JobFrequency.WEEKLY

    def run(self, **kwargs):
        from data_meta.option_meta_manager import OptionMetaManager
        manager = OptionMetaManager()
        manager.update(**kwargs)
