from apps.bot.ex.bigone import *


def market_creator(user_order_size_bid, user_order_size_ask, token,  apikey, apisec, market_value, spread_distance):

    try:
        price_bid = (market_value * (1 - (spread_distance / 100.0)))
        quantity_bid = user_order_size_bid / price_bid
        exit_code1 = f"The bid price will be {price_bid} and the bid quantity price will be {quantity_bid}"
        create_order(price_bid, quantity_bid, "BID", token, apikey, apisec)

        price_ask = (market_value * ((spread_distance / 100.0) + 1.0))
        quantity_ask = user_order_size_ask / price_ask
        exit_code2 = f"The ask price will be {price_ask} and the ask quantity price will be {quantity_ask}"
        create_order(price_bid, quantity_bid, "ASK", token, apikey, apisec)

        return {
            "status": "success",
            "bid": exit_code1,
            "ask": exit_code2,
        }

    except Exception as e:
        return {
            "status": "error",
            "code": str(e),
        }
