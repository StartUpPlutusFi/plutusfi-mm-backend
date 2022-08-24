# from celery import shared_task
# from apps.autotrade.bigone.autotrade_bigone import bigone_autotrade_close, bigone_autotrade_open
#
#
# # ------------------------------------------------------------------------- #
# @shared_task
# def bigone_auto_trade_open_1m():
#     print(" -------------- Run BigOne autotrade OPEN 5m")
#     var = bigone_autotrade_open(1)
#     print(var)
#     return var
#
#
# @shared_task
# def bigone_auto_trade_close_1m():
#     print(" -------------- Run BigOne autotrade CLOSE 5m")
#     var = bigone_autotrade_close(1)
#     print(var)
#     return var
#
#
# # ------------------------------------------------------------------------- #
# @shared_task
# def bigone_auto_trade_open_5m():
#     print(" -------------- Run BigOne autotrade OPEN 5m")
#     var = bigone_autotrade_open(5)
#     print(var)
#     return var
#
#
# @shared_task
# def bigone_auto_trade_close_5m():
#     print(" -------------- Run BigOne autotrade CLOSE 5m")
#     var = bigone_autotrade_close(5)
#     print(var)
#     return var
#
#
# # ------------------------------------------------------------------------- #
# @shared_task
# def bigone_auto_trade_open_15m():
#     print(" -------------- Run BigOne autotrade OPEN 15m")
#     var = bigone_autotrade_open(15)
#     print(var)
#     return var
#
#
# @shared_task
# def bigone_auto_trade_close_15m():
#     print(" -------------- Run BigOne autotrade CLOSE 15m")
#     var = bigone_autotrade_close(15)
#     print(var)
#     return var
#
#
# # ------------------------------------------------------------------------- #
# @shared_task
# def bigone_auto_trade_open_30m():
#     print(" -------------- Run BigOne autotrade OPEN 30m")
#     var = bigone_autotrade_open(30)
#     print(var)
#     return var
#
#
# @shared_task
# def bigone_auto_trade_close_30m():
#     print(" -------------- Run BigOne autotrade CLOSE 30m")
#     var = bigone_autotrade_close(30)
#     print(var)
#     return var
#
#
# # ------------------------------------------------------------------------- #
# @shared_task
# def bigone_auto_trade_open_1h():
#     print(" -------------- Run BigOne autotrade OPEN 1h")
#     var = bigone_autotrade_open(60)
#     print(var)
#     return var
#
#
# @shared_task
# def bigone_auto_trade_close_1h():
#     print(" -------------- Run BigOne autotrade CLOSE 1h")
#     var = bigone_autotrade_close(60)
#     print(var)
#     return var
#
#
# # ------------------------------------------------------------------------- #
# @shared_task
# def bigone_auto_trade_open_4h():
#     print(" -------------- Run BigOne autotrade OPEN 4h")
#     var = bigone_autotrade_open(240)
#     print(var)
#     return var
#
#
# @shared_task
# def bigone_auto_trade_close_4h():
#     print(" -------------- Run BigOne autotrade CLOSE 4h")
#     var = bigone_autotrade_close(240)
#     print(var)
#     return var
#
#
# # ------------------------------------------------------------------------- #
# @shared_task
# def bigone_auto_trade_open_12h():
#     print(" -------------- Run BigOne autotrade OPEN 12h")
#     var = bigone_autotrade_open(720)
#     print(var)
#     return var
#
#
# @shared_task
# def bigone_auto_trade_close_12h():
#     print(" -------------- Run BigOne autotrade CLOSE 12h")
#     var = bigone_autotrade_close(720)
#     print(var)
#     return var
#
#
# # ------------------------------------------------------------------------- #
# @shared_task
# def bigone_auto_trade_open_1d():
#     print(" -------------- Run BigOne autotrade OPEN 1D")
#     var = bigone_autotrade_open(1440)
#     print(var)
#     return var
#
#
# @shared_task
# def bigone_auto_trade_close_1d():
#     print(" -------------- Run BigOne autotrade CLOSE 1D")
#     var = bigone_autotrade_close(1440)
#     print(var)
#     return var
