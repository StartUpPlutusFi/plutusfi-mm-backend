from celery import shared_task
from celery.schedules import crontab

from apps.bot.api.views import bigone_autotrade_open, bigone_autotrade_close

# 1m, 5m, 15m, 30m, 1h, 4h, 12h, 1d

# @shared_task
# def data_processing_1m():
#     print(" -------------- Run BigOne autotrade with candle of 1m")
#     return bigone_autotrade_open(1)


@shared_task
def data_processing_5m():
    print(" -------------- Run BigOne autotrade OPEN 5m")
    var = bigone_autotrade_open(5)
    print(var)
    return var

@shared_task
def data_close_5m():
    print(" -------------- Run BigOne autotrade CLOSE 5m")
    var = bigone_autotrade_close(5)
    print(var)
    return var

# @shared_task
# def data_processing_15m():
#     print(" -------------- Run BigOne autotrade with candle of 15m")
#     return bigone_autotrade_open(15)


# @shared_task
# def data_processing_30m():
#     print(" -------------- Run BigOne autotrade with candle of 30m")
#     return bigone_autotrade_open(30)


# @shared_task
# def data_processing_1h():
#     print(" -------------- Run BigOne autotrade with candle of 1h")
#     return bigone_autotrade_open(60)


# @shared_task
# def data_processing_4h():
#     print(" -------------- Run BigOne autotrade with candle of 4h")
#     return bigone_autotrade_open(240)


# @shared_task
# def data_processing_12h():
#     print(" -------------- Run BigOne autotrade with candle of 12h")
#     return bigone_autotrade_open(720)


# @shared_task
# def data_processing_1d():
#     print(" -------------- Run BigOne autotrade with candle of 1d")
#     return bigone_autotrade_open(1440)
