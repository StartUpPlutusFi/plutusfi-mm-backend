import os
import logging
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
    formatter = logging.Formatter("{\"time\": \"%(asctime)s\", \"func name\": \"[%(funcName)s]\", \"levelname\": \"%("
                                  "levelname)s\", \"message\": \"%(message)s\"}")

    # add filehandler
    fh = logging.FileHandler('logs/autotrade.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


app.autodiscover_tasks()
