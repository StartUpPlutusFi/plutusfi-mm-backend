import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketmaker.settings.dev")

app = Celery("marketmaker")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     "run-test-every-1-min": {
#         "task": "apps.bot.tasks.data_processing_1m",
#         "schedule": 60.0,
#     },
# }

app.conf.beat_schedule = {
    "run-every-5-min": {
        "task": "apps.bot.tasks.data_processing_5m",
        "schedule": 5.0,
    },
}

# app.conf.beat_schedule = {
#     "run-every-15-min": {
#         "task": "apps.bot.tasks.data_processing_15m",
#         "schedule": 15*60.0,
#     },
# }


# app.conf.beat_schedule = {
#     "run-every-30-min": {
#         "task": "apps.bot.tasks.data_processing_30m",
#         "schedule": 60.0,
#     },
# }

# app.conf.beat_schedule = {
#     "run-every-1-h": {
#         "task": "apps.bot.tasks.data_processing_1h",
#         "schedule": 60.0,
#     },
# }

# app.conf.beat_schedule = {
#     "run-every-4-h": {
#         "task": "apps.bot.tasks.data_processing_4h",
#         "schedule": 60.0,
#     },
# }

# app.conf.beat_schedule = {
#     "run-every-12-h": {
#         "task": "apps.bot.tasks.data_processing_12h",
#         "schedule": 60.0,
#     },
# }

# app.conf.beat_schedule = {
#     "run-every-24-h": {
#         "task": "apps.bot.tasks.data_processing_1d",
#         "schedule": 60.0,
#     },
# }