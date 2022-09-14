from apps.autotrade.models.models import MarketMakerBotOrderHistory

def mm_logs(
        bot_id,
        pair_token,
        user_ref_price,
        exec_ref_price,
        side,
        trade_candle,
        trade_amount,
        status,
):
    try:
        logs = MarketMakerBotOrderHistory.objects.create(
            bot_id=bot_id,
            pair_token=pair_token,
            user_ref_price=user_ref_price,
            exec_ref_price=exec_ref_price,
            side=side,
            trade_candle=trade_candle,
            trade_amount=trade_amount,
            status=status,
        )

        logs.save()

        edata = {
            "status": "success",
            "log": {
                    "bot_id": bot_id,
                    "pair_token": pair_token,
                    "user_ref_price": user_ref_price,
                    "exec_ref_price": exec_ref_price,
                    "side": side,
                    "trade_candle": trade_candle,
                    "trade_amount": trade_amount,
                    "status": status,
                },
            }

        logger.warning(edata)

    except Exception as err:

        return {
            "status": "log fail",
            "code": str(err),
        }
