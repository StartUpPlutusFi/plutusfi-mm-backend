from celery import shared_task
from apps.exchange.services.biconomy.biconomy_core import (
    biconomy_new_autotrade,
)
import logging
logger = logging.getLogger(__name__)


@shared_task
def run_new_autotrade_periodically_every_10sec(time=5):
    autotrade = biconomy_new_autotrade(time)

    data = {
        "autotrade": autotrade,
    }

    logging.debug(data)
    print(data)

