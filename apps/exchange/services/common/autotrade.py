from celery import shared_task
from apps.exchange.services.bigone.bigone_core import (
    bigone_autotrade_open,
    bigone_autotrade_close,
)
from apps.exchange.services.biconomy.biconomy_core import (
    biconomy_autotrade_open,
    biconomy_autotrade_close,
)
import logging

logger = logging.getLogger(__name__)

@shared_task
def run_autotrade_periodically_every_10sec(time=10):

    # close_bigone = bigone_autotrade_close(time)
    # open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    data = {
        # "close_bigone": close_bigone,
        # "open_bigone": open_bigone,
        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

    logging.debug(data)

    print(data)
