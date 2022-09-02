
from celery import shared_task
from apps.exchange.services.bigone.bigone_core import bigone_autotrade_open, bigone_autotrade_close
from apps.exchange.services.biconomy.biconomy_core import biconomy_autotrade_open, biconomy_autotrade_close



@shared_task
def run_autotrade_periodically_every_1min(time=1):

    print("TASKS::RUN → run every 1min")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }


@shared_task
def run_autotrade_periodically_every_5min(time=5):

    print("TASKS::RUN → run every 5min")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

@shared_task
def run_autotrade_periodically_every_7min(time=7):

    print("TASKS::RUN → run every 7min")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

@shared_task
def run_autotrade_periodically_every_15min(time=15):

    print("TASKS::RUN → run every 15min")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

@shared_task
def run_autotrade_periodically_every_30min(time=30):

    print("TASKS::RUN → run every 30min")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

@shared_task
def run_autotrade_periodically_every_1hour(time=60):

    print("TASKS::RUN → run every 1hour")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

@shared_task
def run_autotrade_periodically_every_2hours(time=120):

    print("TASKS::RUN → run every 2hours")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

@shared_task
def run_autotrade_periodically_every_4hours(time=240):

    print("TASKS::RUN → run every 4hours")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

@shared_task
def run_autotrade_periodically_every_6hours(time=360):

    print("TASKS::RUN → run every 6hours")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

@shared_task
def run_autotrade_periodically_every_12hours(time=720):

    print("TASKS::RUN → run every 12hours")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

@shared_task
def run_autotrade_periodically_every_1day(time=1440):

    print("TASKS::RUN → run every 1day")

    close_bigone = bigone_autotrade_close(time)
    open_bigone = bigone_autotrade_open(time)

    close_biconomy = biconomy_autotrade_close(time)
    open_biconomy = biconomy_autotrade_open(time)

    return {
        "close_bigone": close_bigone,
        "open_bigone": open_bigone,

        "close_biconomy": close_biconomy,
        "open_biconomy": open_biconomy,
    }

