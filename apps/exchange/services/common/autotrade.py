from celery import shared_task
from apps.exchange.services.biconomy.biconomy_core import (
    biconomy_autotrade_open,
    biconomy_autotrade_close,
    biconomy_new_autotrade,
)
import logging
logger = logging.getLogger(__name__)


@shared_task
def run_autotrade_periodically_every_10sec(time=10):
    open_biconomy = biconomy_autotrade_open(time)
    close_biconomy = biconomy_autotrade_close(time)

    data = {
        "open_biconomy": open_biconomy,
        "close_biconomy": close_biconomy,
    }

    logging.debug(data)
    print(data)


@shared_task
def run_new_autotrade_periodically_every_10sec(time=10):
    autotrade = biconomy_new_autotrade(time)

    data = {
        "autotrade": autotrade,
    }

    logging.debug(data)
    print(data)

