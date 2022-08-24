## Biconomy

# Modules
from email import header
from hashlib import md5
from urllib.parse import urlencode
import requests
import random
import time

from apps.autotrade.db.models import *
from apps.bookfiller.db.models import *


# função de encriptação do header
def encript_string(query_string):
    return md5(query_string.encode()).hexdigest().upper()


def biconomy_default_header():
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-SITE-ID": "127",
    }


def check_ref_price(symbol, size=100):
    # @symbol -> pait_token
    # @size -> response size

    headers = biconomy_default_header()
    BASE_URL = f"https://www.biconomy.com/api/v1/depth?symbol={symbol}"

    params = {
        "symbol": symbol,
        "size": size,
    }

    response = requests.get(BASE_URL, headers=headers, data=params)
    response_json = response.json()

    ask = float(response_json["asks"][0][0])
    bid = float(response_json["bids"][0][0])

    ref_price = (ask + bid) / 2

    return ref_price


def make_request(params, URL):
    headers = biconomy_default_header()

    query_string = urlencode(params)
    # print(query_string)
    md5_params = encript_string(query_string)
    params.pop("secret_key")
    params["sign"] = md5_params
    r = requests.post(URL, headers=headers, data=params)
    response_json = r.json()
    # print(response_json, params["sign"])
    return response_json


def create_order(params):
    BASE_URL = "https://www.biconomy.com/api/v1/private/trade/limit"
    response_json = make_request(params, BASE_URL)
    if response_json["code"] == 10:
        return 0
    return response_json["result"]["id"]


def cancel_order(params):
    BASE_URL = "https://www.biconomy.com/api/v1/private/trade/cancel"
    make_request(params, BASE_URL)
    return {"status": "success"}


## Create and cancel order
def trade_operation(api_key, api_sec, amount, symbol, price, side=2):
    create_order_par = {
        "amount": amount,
        "api_key": api_key,
        "market": symbol,
        "price": price,
        "side": 2,
        "secret_key": api_sec,
    }

    order_id = create_order(create_order_par)
    time.sleep(10)

    cancel_order_par = {
        "api_key": api_key,
        "market": symbol,
        "order_id": order_id,
        "secret_key": api_sec,
    }

    result = (cancel_order(cancel_order_par),)

    return {
        "created_order": order_id,
        "cancel_order": result,
        # "candle_time": candle,
    }


## Take total ASKS and BIDS of an symbol
def take_all_asks_and_bids_by_symbol(symbol, size=100):
    BASE_URL = f"https://www.biconomy.com/api/v1/depth?symbol={symbol}"
    headers = biconomy_default_header()

    params = {
        "symbol": symbol,
        "size": size,
    }

    response = requests.get(BASE_URL, headers=headers, data=params)

    return response.json()


## Biconomy gets the total amount of ASKS and BIDS of x SYMBOL
def get_total_amount_of_asks_and_bids_of_one_symbol(symbol, size=100):
    headers = biconomy_default_header()

    # base URL
    BASE_URL = f"https://www.biconomy.com/api/v1/depth?symbol={symbol}"

    # Configuração de parametros para inclusão de ordem
    params = {
        "symbol": symbol,
        "size": size,
    }

    total_ask = 0.0
    total_bids = 0.0

    response = requests.get(BASE_URL, headers=headers, data=params)
    response_json = response.json()

    for ask in response_json["asks"]:
        total_ask = total_ask + (float(ask[0]) * float(ask[1]))

    for bids in response_json["bids"]:
        total_bids = total_bids + (float(bids[0]) * float(bids[1]))

    return {
        "total_ask": total_ask,
        "total_bids": total_bids,
    }


## Biconomy check all pending orders of x symbol
def check_all_pending_orders_by_symbol(api_key, api_sec, symbol):
    BASE_URL = "https://www.biconomy.com/api/v1/private/order/pending"
    headers = biconomy_default_header()

    params = {"api_key": api_key, "market": symbol, "secret_key": api_sec}

    query_string = urlencode(params)
    md5_params = encript_string(query_string)
    params.pop("secret_key")
    params["sign"] = md5_params

    response = requests.post(BASE_URL, headers=headers, data=params)
    return response.json()


## Biconomy GET ALL USDT PAIRS
def take_all_usdt_pairs():
    headers = biconomy_default_header()
    BASE_URL = "https://www.biconomy.com/api/v1/tickers"
    response = requests.get(BASE_URL, headers=headers)
    return response.json()


## Biconomy BOOK REF_PRICE AND MINIMAL QUANTITY
def take_bool_ref_price_and_minimal_quantity(symbol, size=100):
    total_order = 10
    ref_price = check_ref_price(symbol, size=100)
    quantity = total_order / ref_price

    return quantity


## Biconomy BOOK ORDER CREATOR BASED ON REF_PRICE AND MINIMAL QUANTITY
def bid_order_creator(limit, price, symbol):
    # @limit -> Order quantity
    # @symbol -> Pair token
    # @size -> Response size

    total_order = 11

    if price != 0:
        bid_price = price
    else:
        bid_price = check_ref_price(symbol)

    bid_prices = []
    bid_quantitys = []

    order_pair = []

    for number in range(limit):
        bid_price = (1.02) * bid_price
        bid_prices.append(bid_price)

        bid_quantity = total_order / bid_price
        bid_quantitys.append(bid_quantity)

        order_pair.append({"price": bid_price, "quantity": bid_quantity})

    return {"order_pair": order_pair}


## Biconomy RANDOM ORDER LOOP
def auto_trade_mm_bot(user_max_order_value, symbol):
    ref_price = check_ref_price(symbol, size=100)

    total_order = random.randint(10, user_max_order_value)

    bid_price = ref_price
    bid_price = 1.02 * bid_price
    bid_quantity = total_order / bid_price

    # create_order_par = {
    #     "amount": bid_quantity,
    #     "api_key": api_key,
    #     "market": symbol,
    #     "price": bid_price,
    #     "side": 2,
    #     "secret_key": api_sec,
    # }

    # order_id = create_order(create_order_par)

    return {
        "ref_price": ref_price,
        "bid_price": bid_price,
        "bid_quantity": bid_quantity,
    }



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
        cancel_codes.append(code["result"]["id"])

        CancelOrderBookBot.objects.create(
            bot_id=bookbot_id, cancel_order_id=code["result"]["id"], order_status=True
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


def biconomy_cancel_all_orders(bookbot):
    responses = []

    bot_id = bookbot.id
    cancel_list = CancelOrderBookBot.objects.filter(
        order_status=True, bot_id=bot_id
    ).values("id", "bot", "cancel_order_id")

    for bot in cancel_list:
        params = {
            "api_key": bookbot.api_key.api_key,
            "market": bookbot.pair_token.pair,
            "order_id": bot["cancel_order_id"],
            "secret_key": bookbot.api_key.api_secret,
        }

        query_string = urlencode(params)
        md5_params = encript_string(query_string)
        params.pop("secret_key")
        params["sign"] = md5_params

        r = requests.post(get_order_cancel_url(), headers=get_headers(), data=params)
        response_json = r.json()
        responses.append(response_json)

        CancelOrderBookBot.objects.filter(bot_id=bot_id).update(order_status=False)

    return responses


def biconomy_init_bookbot(data):
    limit_generator = data.number_of_orders
    token = data.pair_token.pair
    user_ref_price = data.user_ref_price
    user_max_order_value = data.order_size
    user_side_choice = data.side
    api_key = data.api_key.api_key
    api_sec = data.api_key.api_secret
    bookbot_id = data.id

    # salva id da ordem criada
    if data.side == "ASK":
        user_side_choice = 1
    else:
        user_side_choice = 2

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
        bookbot_id,
    )

    return {
        "number_of_orders": len(cancel_codes),
        "cancel_codes": cancel_codes,
    }
