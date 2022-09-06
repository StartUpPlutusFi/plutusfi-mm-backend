from apps.autotrade.models.models import MarketMakerBotOrderHistory


def autotrade_operation_log(
    bot_id,
    type,
    exchange,
    pair_token,
    reference_price,
    user_ref_price,
    side,
    trade_candle,
    trade_amount,
):
    # try:
    if True:
        edata = MarketMakerBotOrderHistory.objects.create(
            bot_id,
            type,
            exchange,
            pair_token,
            reference_price,
            user_ref_price,
            side,
            trade_candle,
            trade_amount,
        )

        edata.save()

        return {
            "status": "success",
            "result": {
                "bot_id": bot_id,
                "type": type,
                "exchange": exchange,
                "pair_token": pair_token,
                "reference_price": reference_price,
                "user_ref_price": user_ref_price,
                "side": side,
                "trade_candle": trade_candle,
                "trade_amount": trade_amount,
            }
        }

    # except Exception as err:
    #
    #     return {
    #         "status": "error",
    #         "code": str(err),
    #     }

