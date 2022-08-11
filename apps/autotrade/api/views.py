import random

from apps.dashboard.ex.bigone import *
from apps.dashboard.db.models import *


def auto_trade_order_open(user_ref_price, user_side_choice, user_max_order_value, apikey, apisec, token, bot_id, candle, op=3):
    
    order = op
    if op == 3:
        order = random.randint(1, 2)

    if order == 1:

        quantity, price = ref_value(
            user_ref_price, user_side_choice, user_max_order_value, token)

        exit  = create_order(price, quantity, side="BID",
                    token=token, apikey=apikey,  apisec=apisec)
        log = MarketMakerBotAutoTradeQueue.objects.create(
            bot_id = bot_id,
            price = price,
            quantity = quantity,
            side = "BID",
            status = "OPEN",
            candle = candle
        )

        log.save()

    else:

        quantity, price = ref_value(
            user_ref_price, user_side_choice, user_max_order_value, token)

        exit  = create_order(price, quantity, side="ASK",
                    token=token, apikey=apikey,  apisec=apisec)

        log = MarketMakerBotAutoTradeQueue.objects.create(
            bot_id = bot_id,
            price = price,
            quantity = quantity,
            side = "ASK",
            status = "OPEN",
            candle = candle
        )

        log.save()


    return {
            "name": "auto_trade_order_open",
            'status': "success", 
            "data": exit,
        }


def auto_trade_order_close(price, quantity, side,  apikey, apisec, token):

    try:

        if side == "ASK":
            side = "BID"
            exit = create_order(price, quantity, side,
                        token=token, apikey=apikey,  apisec=apisec)
            
        elif side == "BID":
            side = "ASK"
            exit = create_order(price, quantity, side,
                        token=token, apikey=apikey,  apisec=apisec)
            
        else: 
            exit = "Invalid side at auto_trade_order_close"



        return {
            "name": "auto_trade_order_close",
            'status': "success", 
            "data": exit,
        }
    except Exception as e :

        return {
            "name": "auto_trade_order_close",
            'status': "error", 
            "error": f"ERROR at auto_trade_order_close → {str(e)}",
        }
        