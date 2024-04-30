from scheduler.jobs.job_frequency_enum import JobFrequency


class MetaScheduler:

    def __init__(self):
        self.jobs = {
            JobFrequency.DAILY: [],
            JobFrequency.WEEKLY: [],
        }

    def add_job(self, job):
        if job.frequency == JobFrequency.DAILY:
            self.jobs[JobFrequency.DAILY].append(job)
        elif job.frequency == JobFrequency.WEEKLY:
            self.jobs[JobFrequency.WEEKLY].append(job)

    def run(self, **kwargs):
        run_frequency = kwargs.get("run_frequency")
        time_messager = kwargs.get("time_messager")
        run_frequency_enum = JobFrequency.from_str(run_frequency)
        jobs = self.jobs.get(run_frequency_enum)
        if jobs is None:
            raise ValueError(f"No jobs for frequency {run_frequency}")
        for job in jobs:
            time_messager(description=job.description)
            job.run(**kwargs)
