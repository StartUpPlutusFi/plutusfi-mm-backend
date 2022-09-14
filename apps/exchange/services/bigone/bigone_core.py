import logging

from apps.autotrade.models.models import *

import requests
import time
import random
import jwt
import json

from apps.bookfiller.models.models import CancelOrderBookBot
from apps.geneses.models.models import *


def cancel_one_order(apikey, apisec, code):
    base_url = 'https://big.one/api/v3/viewer/order/cancel'
    params = {
        "order_id": int(code),
    }
    json_params = json.dumps(params, indent=4)
    r = requests.post(base_url, headers=get_order_header_encoded(apikey, apisec), data=json_params)
    return r.json()


def ping():
    ping_url = "https://big.one/api/v3/ping"
    ping = requests.get(ping_url)
    ping_json = ping.json()
    timestamp = ping_json["data"]["Timestamp"]
    return timestamp


def get_order_header_encoded(apikey, apisec):
    payload = {
        "type": "OpenAPIV2",
        "sub": apikey,
        "nonce": str(ping()),
        "recv_window": "50",
    }
    token = jwt.encode(
        headers=get_headers(),
        payload=payload,
        key=apisec,
    )
    header_encoded = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }
    return header_encoded


def get_order_url():
    BASE_URL = "https://big.one/api/v3/viewer/orders"
    return BASE_URL


def check_ref_price(token):
    smallest_ask = 0.0
    highest_bid = 0.0
    ask = False

    BASE_URL = f"https://big.one/api/v3/asset_pairs/{token}/depth"
    r = requests.get(BASE_URL)
    response_json = r.json()

    if not response_json["data"]["bids"]:
        ref_price = float(response_json["data"]["asks"][0]["price"])
        ask = True
        # print(f"There is no bids so the ref price value is the lowest ask: {ref_price}")
        return ref_price, ask, smallest_ask, highest_bid
    if not response_json["data"]["asks"]:
        ref_price = float(response_json["data"]["bids"][0]["price"])
        # print(
        #     f"There is no asks so the ref price value is the highest bid: {ref_price}"
        # )
        return ref_price, ask, smallest_ask, highest_bid
    ref_price = (
                        float(response_json["data"]["bids"][0]["price"])
                        + float(response_json["data"]["asks"][0]["price"])
                ) / 2
    smallest_ask = float(response_json["data"]["asks"][0]["price"])
    highest_bid = float(response_json["data"]["bids"][0]["price"])

    return ref_price, ask, smallest_ask, highest_bid


def get_headers():
    headers = {
        "alg": "HS256",
        "typ": "JWT",
    }
    return headers


def create_order(price, quantity, side, token, apikey, apisec):
    try:
        params = {
            "asset_pair_name": token,
            "side": side,
            "price": str(price),
            "amount": str(quantity),
            "type": "LIMIT",
        }

        json_params = json.dumps(params, indent=4)
        r = requests.post(
            get_order_url(),
            headers=get_order_header_encoded(apikey, apisec),
            data=json_params,
        )

        return r.json()

    except Exception as e:

        return {
            "status": "error",
            "code": str(e),
        }


def ref_value(user_ref_price, user_side_choice, user_max_order_value, token):
    ask = False
    smallest_ask = 0.0
    price = 0.0
    random_operation = 0

    if user_ref_price == 0:
        ref_price, ask, smallest_ask, highest_bid = check_ref_price(token)

        if user_side_choice == 1:
            price = random.uniform(ref_price, smallest_ask)
        elif user_side_choice == 2:
            price = random.uniform(ref_price, highest_bid)
        else:
            random_list = [smallest_ask, highest_bid]
            random_operation = random.choice(random_list)
            price = random.uniform(ref_price, random_operation)
    else:
        ref_price = user_ref_price
        ask = False
        price = ref_price
    total_order = 0

    total_order = random.randint(12, user_max_order_value)
    # print(f"Total order value in USDT: {total_order}")
    # Gets the price and quantity necessary to make an order from (reference price * 1.02) or * 0.98
    if ask or user_side_choice == 1 or random_operation == smallest_ask:
        price = 0.98 * price
    else:
        price = (1.02) * price
    # print(f"Price {price}")
    quantity = total_order / price
    # print(f"Quantity {quantity}")
    return quantity, price


def get_budget(coin, side, apikey, apisec):
    BASE_URL = "https://big.one/api/v3/viewer/accounts"
    r = requests.get(BASE_URL, headers=get_order_header_encoded(apikey, apisec))
    response_json = r.json()
    for x in response_json["data"]:
        if x["asset_symbol"] == "USDT" and side == "BID":
            return x["balance"]
        if x["asset_symbol"] == coin and side == "ASK":
            return x["balance"]


def auto_trade_order_open(
        exec_ref_price,
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
            exec_ref_price, user_side_choice, user_max_order_value, token
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
            exec_ref_price=exec_ref_price,
        )

        log.save()

    else:

        quantity, price = ref_value(
            exec_ref_price, user_side_choice, user_max_order_value, token
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
            exec_ref_price=exec_ref_price,
        )

        log.save()

    return {
        "name": "bigone_auto_trade_order_open",
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
    bots = MarketMakerBot.objects.filter(
        status="START", trade_candle=candle, api_key__exchange__name="bigone"
    )

    result = []

    for data in bots:
        bot_id = data.id
        apikey = data.api_key.api_key
        apisec = data.api_key.api_secret
        user_side_choice = data.side
        user_max_order_value = data.trade_amount
        token = data.pair_token
        user_ref_price = data.user_ref_price
        op = data.side
        ref = check_ref_price(token)[0]

        if user_ref_price == 0:
            exec_ref_price = ref
        else:
            exec_ref_price = user_ref_price

        exit_code = auto_trade_order_open(
            exec_ref_price,
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
            "exec_ref_price": exec_ref_price,
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
        status="OPEN", candle=candle, bot__api_key__exchange__name="bigone"
    )

    for order in open_orders:

        price = order.price
        quantity = order.quantity
        side = order.side
        apikey = order.bot.api_key.api_key
        apisec = order.bot.api_key.api_secret
        token = order.bot.pair_token

        order_id = order.id

        print(
            f"bigone_autotrade_close :: :: {price}, {quantity}, {side},  {apikey}, {apisec}, {token}"
        )

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


def bigone_cancel_all_orders(bookbot):
    responses = []

    apikey = bookbot.api_key.api_key
    apisec = bookbot.api_key.api_secret
    bot_id = bookbot.id

    cancel_list = CancelOrderBookBot.objects.filter(
        order_status=True, bot_id=bot_id
    ).values("id", "bot", "cancel_order_id")

    for bot in cancel_list:

        response_json = cancel_one_order(apikey, apisec, bot["cancel_order_id"])

        try:
            if response_json['data']['state'] == "CANCELLED":
                CancelOrderBookBot.objects.filter(id=bot['id'], bot_id=bot_id).update(order_status=False)
            else:
                CancelOrderBookBot.objects.filter(id=bot['id'], bot_id=bot_id).update(order_status=True)

        except Exception as err:

            return {
                "status": f"fail to cancel order {bot['cancel_order_id']}"
            }

        responses.append({
            "status": response_json['data']['state'],
            "code": bot['cancel_order_id'],
        })

    return responses


def bookfiller_check_ref_price(token):
    ask = False
    base_url = f"https://big.one/api/v3/asset_pairs/{token}/depth"
    r = requests.get(base_url)
    response_json = r.json()
    if not response_json["data"]["bids"]:
        ref_price = float(response_json["data"]["asks"][0]["price"])
        ask = True
        return ref_price, ask
    if not response_json["data"]["asks"]:
        ref_price = float(response_json["data"]["bids"][0]["price"])
        return ref_price, ask
    ref_price = (
                        float(response_json["data"]["bids"][0]["price"])
                        + float(response_json["data"]["asks"][0]["price"])
                ) / 2
    return ref_price, ask


# Gets the price and quantity necessary to make an order from (reference price * 1.02)
def bigone_book_generator(
        limit_generator, token, user_ref_price, user_max_order_value, side, api_key, api_sec, bookbot_id
):
    if user_ref_price == 0:
        price = bookfiller_check_ref_price(token)

    else:
        price = user_ref_price

    multiplier = 1.02
    if side == 2:  # 2 == BID
        multiplier = 0.98

    prices = []
    quantitys = []
    exit_codes = []

    if side == 1:
        side = "ASK"
    else:
        side = "BID"

    try:
        for x in range(limit_generator):
            price = multiplier * price
            prices.append(price)
            quantity = user_max_order_value / price
            quantitys.append(quantity)
            code = create_order(price, quantity, side, token, api_key, api_sec)
            exit_codes.append(code['data']['id'])

            CancelOrderBookBot.objects.create(
                bot_id=bookbot_id, cancel_order_id=code['data']['id'], order_status=True
            )

        return {
            "prices": prices,
            "quantitys": quantitys,
            "exit_codes": exit_codes,
        }

    except Exception as e:

        return {
            "status": "error",
            "code": str(e),
            "exit_code": exit_codes,
        }


def bigone_init_bookbot(data):
    limit_generator = data.number_of_orders
    token = data.pair_token
    user_ref_price = data.user_ref_price
    user_max_order_value = data.order_size
    user_side_choice = data.side
    api_key = data.api_key.api_key
    api_sec = data.api_key.api_secret
    bookbot_id = data.id

    if user_side_choice == "ASK":
        side = 1
    else:
        side = 2

    if user_ref_price == 0:
        user_ref_price = check_ref_price(token)

    cancel_codes = bigone_book_generator(
        limit_generator,
        token,
        user_ref_price,
        user_max_order_value,
        side,
        api_key,
        api_sec,
        bookbot_id,
    )

    return {
        "number_of_orders": len(cancel_codes),
        "cancel_codes": cancel_codes,
    }


def bigone_market_creator_open(geneses_bot):
    user_order_size_bid = geneses_bot.user_order_size_bid
    user_order_size_ask = geneses_bot.user_order_size_ask
    token = geneses_bot.token
    apikey = geneses_bot.api_key.api_key
    apisec = geneses_bot.api_key.api_secret
    market_value = geneses_bot.market_value
    spread_distance = geneses_bot.spread_distance
    gid = geneses_bot.id

    try:
        price_bid = market_value * (1 - (spread_distance / 100.0))
        quantity_bid = user_order_size_bid / price_bid
        exit_code1 = f"The bid price will be {price_bid} and the bid quantity price will be {quantity_bid}"
        exit_code_bid = create_order(price_bid, quantity_bid, "BID", token, apikey, apisec)

        GenesesQueue.objects.create(
            geneses_id=gid, cancel_code=exit_code_bid['data']['id'], status="OPEN"
        )

        price_ask = market_value * ((spread_distance / 100.0) + 1.0)
        quantity_ask = user_order_size_ask / price_ask
        exit_code2 = f"The ask price will be {price_ask} and the ask quantity price will be {quantity_ask}"
        exit_code_ask = create_order(price_ask, quantity_ask, "ASK", token, apikey, apisec)

        GenesesQueue.objects.create(
            geneses_id=gid, cancel_code=exit_code_ask['data']['id'], status="OPEN"
        )

        return {
            "status": "success",
            "bid": {
                "order": exit_code1,
                "bid": exit_code_bid,
            },
            "ask": {
                "order": exit_code2,
                "ask": exit_code_ask,
            },
        }

    except Exception as e:
        # response_json_bid = cancel_one_order(apikey, apisec, exit_code_bid['data']['id'])
        # response_json_ask = cancel_one_order(apikey, apisec, exit_code_ask['data']['id'])

        return {
            "status": "error",
            "code": str(e),
        }


def bigone_market_creator_close(geneses_bot):
    responses = []

    apikey = geneses_bot.api_key.api_key
    apisec = geneses_bot.api_key.api_secret
    gid_id = geneses_bot.id

    cancel_list = GenesesQueue.objects.filter(
        status="OPEN", geneses_id=gid_id
    ).values("id", "geneses", "cancel_code")

    for reg in cancel_list:

        response_json = cancel_one_order(apikey, apisec, reg["cancel_code"])

        try:
            if response_json['data']['state'] == "CANCELLED":
                GenesesQueue.objects.filter(id=reg['id'], geneses_id=gid_id).update(status="DONE")
            else:
                GenesesQueue.objects.filter(id=reg['id'], geneses_id=gid_id).update(status="FAIL")

        except Exception as err:

            return {
                "status": f"fail to cancel order {reg['cancel_code']}",
                "code": str(err),
            }

        responses.append({
            "status": response_json['data']['state'],
            "code": reg['cancel_code'],
        })

    return {
        "status": "done",
        "result": responses,
    }
