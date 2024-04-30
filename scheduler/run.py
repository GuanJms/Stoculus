import os
from scheduler import MetaScheduler
from scheduler.jobs import UpdateTickerJob, UpdateOptionExpsJob

import datetime

def time_messager(**kwargs):
    current_time = datetime.datetime.now()
    message = f"@ {current_time}"
    if kwargs.get("description", None) is not None:
        message = f"Running job: {kwargs['description']} {message}"
    print(message)

def main():
    time_messager()
    scheduler = MetaScheduler()
    scheduler.add_job(UpdateTickerJob())
    scheduler.add_job(UpdateOptionExpsJob())

    run_frequency = os.getenv("run_frequency")
    scheduler.run(run_frequency=run_frequency, time_messager=time_messager)

if __name__ == "__main__":
    main()
