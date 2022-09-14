import os
import logging
import logging.config
from celery import Celery
from celery.signals import after_setup_logger
from celery.app import trace

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketmaker.settings.dev")

app = Celery("marketmaker")
app.config_from_object("django.conf:settings", namespace="CELERY")

logger = logging.getLogger(__name__)
# trace.LOG_SUCCESS = None

for f in ['./broker/out', './broker/processed']:
    if not os.path.exists(f):
        os.makedirs(f)

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logging.config.fileConfig('./marketmaker/log_auto_trade.ini', disable_existing_loggers=False)


app.autodiscover_tasks()
