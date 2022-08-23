# modulos
import time
from hashlib import md5
from urllib.parse import urlencode
from apps.dashboard.db.models import *

import requests


def encript_string(query_string):
    return md5(query_string.encode()).hexdigest().upper()


def get_order_url():
    BASE_URL = "https://www.biconomy.com/api/v1/private/trade/limit"
    return BASE_URL


def get_order_cancel_url():
    BASE_URL = "https://www.biconomy.com/api/v1/private/trade/cancel"
    return BASE_URL


def check_ref_price(token):
    smallest_ask = 0.0
    highest_bid = 0.0
    ask = False
    BASE_URL = f"https://www.biconomy.com/api/v1/depth?symbol={token}"
    r = requests.get(BASE_URL)
    response_json = r.json()
    if not response_json["bids"]:
        ref_price = float(float(response_json["asks"][0][0]))
        ask = True
        # print(f"There is no bids so the ref price value is the lowest ask: {ref_price}")
        return ref_price, ask, smallest_ask, highest_bid
    if not response_json["asks"]:
        ref_price = float(response_json["bids"][0][0])
        # print(
        #     f"There is no asks so the ref price value is the highest bid: {ref_price}"
        # )
        return ref_price, ask, smallest_ask, highest_bid
    ref_price = (
        float(response_json["bids"][0][0]) + float(float(response_json["asks"][0][0]))
    ) / 2
    smallest_ask = float(float(response_json["asks"][0][0]))
    highest_bid = float(response_json["bids"][0][0])
    # print(f"The ref price value is: {ref_price}")
    # print(f"The smallest ASK is {smallest_ask} and the highest BID is {highest_bid}")
    return ref_price, ask, smallest_ask, highest_bid


def get_headers():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-SITE-ID": "127",
    }
    return headers


def create_order(price, quantity, token, side, api_key, api_sec):
    params = {
        "amount": str(quantity),
        "api_key": api_key,
        "market": token,
        "price": str(price),
        "side": side,
        "secret_key": api_sec,
    }
    query_string = urlencode(params)
    md5_params = encript_string(query_string)
    params.pop("secret_key")
    params["sign"] = md5_params
    r = requests.post(get_order_url(), headers=get_headers(), data=params)
    response_json = r.json()
    return response_json


# Gets the price and quantity necessary to make an order from (reference price * 1.02)


def book_generator(
    limit_generator,
    token,
    user_ref_price,
    user_max_order_value,
    user_side_choice,
    api_key,
    api_sec,
    bookbot_id,
):
    price = 0.0
    if user_ref_price == 0:
        price, ask = check_ref_price(token)
    else:
        price = user_ref_price
    multiplier = 1.02
    if user_side_choice == 2:
        multiplier = 0.98
    prices = []
    quantitys = []
    cancel_codes = []

    for x in range(limit_generator):
        price = multiplier * price
        prices.append(price)
        quantity = user_max_order_value / price
        quantitys.append(quantity)
        time.sleep(0.2)
        code = create_order(price, quantity, token, user_side_choice, api_key, api_sec)
        code.append(code["result"]["id"])

        CancelOrderBookBot.objects.create(
            bot_id=bookbot_id, cancel_order_id=code, order_status=True
        )

    return cancel_codes


def get_budget(token, side):
    BASE_URL = "https://www.biconomy.com/api/v1/private/user"
    r = requests.get(BASE_URL, headers=get_headers())
    response_json = r.json()
    for x in response_json["result"]:
        if (x) == "USDT" and side == 2:
            return x["available"]
        if (x) == token and side == 1:
            return x["available"]


def biconomy_cancel_all_orders(bot_id):

    responses = []

    cancel_list = CancelOrderBookBot.objects.filter(
        order_status=True, bot_id=bot_id
    ).values()

    for bot in cancel_list:

        params = {
            "api_key": bot.api_key.api_key,
            "market": bot.pair_token.name,
            "order_id": bot.cancel_order_id,
            "secret_key": bot.api_key.api_secret,
        }

        query_string = urlencode(params)
        md5_params = encript_string(query_string)
        params.pop("secret_key")
        params["sign"] = md5_params

        r = requests.post(get_order_cancel_url(), headers=get_headers(), data=params)
        response_json = r.json()
        responses.append(response_json)

        CancelOrderBookBot.objects.filter(id=bot.id).update(cancel_order_id=False)

    return responses


def biconomy_init_bookbot(data):

    limit_generator = data.number_of_orders
    token = data.pair_token.pair
    user_ref_price = data.user_ref_price
    user_max_order_value = data.order_size
    user_side_choice = data.side
    api_key = data.api_key.api_key
    api_sec = data.api_key.api_secret

    # salva id da ordem criada
    if data.side == "ASK":
        user_side_choice = 1
    else:
        user_side_choice = 21

    if user_ref_price == 0:
        user_ref_price = check_ref_price(token)

    cancel_codes = book_generator(
        limit_generator,
        token,
        user_ref_price,
        user_max_order_value,
        user_side_choice,
        api_key,
        api_sec,
    )

    return {
        "cancel_codes": cancel_codes,
    }
