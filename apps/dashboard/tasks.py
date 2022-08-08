from celery import shared_task
from celery.schedules import crontab


@shared_task
def data_processing():
    print("10 -- -- -- -- secs")
