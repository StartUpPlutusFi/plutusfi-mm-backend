from apps.bot.ex.bigone import *
from apps.dashboard.db.models import *


def auto_trade_order_open(
    user_ref_price,
    user_side_choice,
    user_max_order_value,
    apikey,
    apisec,
    token,
    bot_id,
    candle,
    op=3,
):
    order = op
    if op != 1 and op != 2:
        order = random.randint(1, 2)

    if order == 1:

        quantity, price = ref_value(
            user_ref_price, user_side_choice, user_max_order_value, token
        )

        exit_code = create_order(
            price, quantity, side="BID", token=token, apikey=apikey, apisec=apisec
        )
        log = MarketMakerBotAutoTradeQueue.objects.create(
            bot_id=bot_id,
            price=price,
            quantity=quantity,
            side="BID",
            status="OPEN",
            candle=candle,
        )

        log.save()

    else:

        quantity, price = ref_value(
            user_ref_price, user_side_choice, user_max_order_value, token
        )

        exit_code = create_order(
            price, quantity, side="ASK", token=token, apikey=apikey, apisec=apisec
        )

        log = MarketMakerBotAutoTradeQueue.objects.create(
            bot_id=bot_id,
            price=price,
            quantity=quantity,
            side="ASK",
            status="OPEN",
            candle=candle,
        )

        log.save()

    return {
        "name": "auto_trade_order_open",
        "status": "success",
        "data": exit_code,
    }


def auto_trade_order_close(price, quantity, side, apikey, apisec, token):
    try:

        if side == "ASK":
            side = "BID"
            exit_code = create_order(
                price, quantity, side, token=token, apikey=apikey, apisec=apisec
            )

        elif side == "BID":
            side = "ASK"
            exit_code = create_order(
                price, quantity, side, token=token, apikey=apikey, apisec=apisec
            )

        else:
            exit_code = "Invalid side at auto_trade_order_close"

        return {
            "name": "auto_trade_order_close",
            "status": "success",
            "data": exit_code,
        }
    except Exception as e:

        return {
            "name": "auto_trade_order_close",
            "status": "error",
            "error": f"ERROR at auto_trade_order_close → {str(e)}",
        }


def bigone_autotrade_open(candle):
    bots = MarketMakerBot.objects.filter(status="START", trade_candle=candle)

    result = []

    for data in bots:
        bot_id = data.id
        apikey = data.api_key.api_key
        apisec = data.api_key.api_secret
        user_side_choice = data.side
        user_max_order_value = data.trade_amount
        token = data.pair_token.pair
        user_ref_price = data.user_ref_price
        op = data.side
        ref = check_ref_price(token)

        exit_code = auto_trade_order_open(
            user_ref_price,
            user_side_choice,
            user_max_order_value,
            apikey,
            apisec,
            token,
            bot_id,
            candle,
            op,
        )

        edata = {
            "reference_price": ref,
            "user_ref_price": user_ref_price,
            "user_side_choice": user_side_choice,
            "user_max_order_value": user_max_order_value,
            "token": token,
            "side": data.side,
            "status": data.status,
            "bot_id": bot_id,
            "candle": candle,
            "autotrade": exit_code,
        }

        result.append(edata)
        # print(f"bigone_autotrade_open:: :: {edata}")

    return result


def bigone_autotrade_close(candle):
    open_orders = MarketMakerBotAutoTradeQueue.objects.filter(
        status="OPEN", candle=candle
    )

    for order in open_orders:

        price = order.price
        quantity = order.quantity
        side = order.side
        apikey = order.bot.api_key.api_key
        apisec = order.bot.api_key.api_secret
        token = order.bot.pair_token.pair

        order_id = order.id

        # print(
        #     f"bigone_autotrade_close :: :: {price}, {quantity}, {side},  {apikey}, {apisec}, {token}"
        # )

        exit_code = auto_trade_order_close(price, quantity, side, apikey, apisec, token)

        if exit_code["status"] == "success":

            MarketMakerBotAutoTradeQueue.objects.filter(id=order_id).update(
                status="DONE"
            )

        else:

            MarketMakerBotAutoTradeQueue.objects.filter(id=order_id).update(
                status="CLOSE"
            )

    return {"status": "success"}
