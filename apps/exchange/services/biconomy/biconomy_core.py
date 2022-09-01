## Biconomy

# Modules
from email import header
from hashlib import md5
from urllib.parse import urlencode
import requests
import random
import time

from apps.autotrade.models.models import *
from apps.bookfiller.models.models import *


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
            "market": bookbot.pair_token,
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

        CancelOrderBookBot.objects.filter(id=bot['id'], bot_id=bot_id).update(order_status=False)

    return responses



def biconomy_init_bookbot(data):
    limit_generator = data.number_of_orders
    token = data.pair_token
    user_ref_price = data.user_ref_price
    user_max_order_value = data.order_size
    user_side_choice = data.side
    api_key = data.api_key.api_key
    api_sec = data.api_key.api_secret
    bookbot_id = data.id

    # salva id da ordem criada
    if user_side_choice == "ASK":
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


def ref_value(user_ref_price, user_side_choice, user_max_order_value):
    smallest_ask = 0.0
    random_operation = None

    if user_ref_price == 0:
        ref_price, ask, smallest_ask, highest_bid = check_ref_price()
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
    total_order = random.randint(1, user_max_order_value)

    # Gets the price and quantity necessary to make an order from (reference price * 1.02) or * 0.98
    if ask or user_side_choice == 1 or random_operation == smallest_ask:
        price = 0.98 * price
    else:
        price = (1.02 * price)
    print(f"Price {price}")
    quantity = total_order / price
    print(f"Quantity {quantity}")
    return quantity, price


def biconomy_auto_trade_order_open(
        user_ref_price,
        user_side_choice,
        token,
        user_max_order_value,
        api_key,
        api_sec,
        bot_id,
        candle,
        op=3,
):
    order = op
    if op != 1 and op != 2:
        order = random.randint(1, 2)

    quantity, price = ref_value(user_ref_price, user_side_choice, user_max_order_value)

    #ask
    if order == 1:
        exit_code = create_order(price, quantity, token, order, api_key, api_sec)

        log = MarketMakerBotAutoTradeQueue.objects.create(
            bot_id=bot_id,
            price=price,
            quantity=quantity,
            side="ASK",
            status="OPEN",
            candle=candle,
        )

        log.save()

    #bid
    else:
        exit_code = create_order(price, quantity, token, order, api_key, api_sec)

        log = MarketMakerBotAutoTradeQueue.objects.create(
            bot_id=bot_id,
            price=price,
            quantity=quantity,
            side="BID",
            status="OPEN",
            candle=candle,
        )

        log.save()

    return {
        "name": "biconomy_auto_trade_order_open",
        "status": "success",
        "data": exit_code,
    }

def biconomy_auto_trade_order_close(price, quantity, side, apikey, apisec, token):
    try:

        if side == "ASK":
            side = 2 #BID
            exit_code = create_order(price, quantity, token, side, apikey, apisec)

        elif side == "BID":
            side = 1 #ASK
            exit_code = create_order(price, quantity, token, side, apikey, apisec)
        else:
            exit_code = "Invalid side at auto_trade_order_close"

        return {
            "name": "auto_trade_order_close",
            "status": "success",
            "data": exit_code,
        }

    except Exception as e:

        return {
            "name": "biconomy_auto_trade_order_close",
            "status": "error",
            "error": f"ERROR at auto_trade_order_close → {str(e)}",
        }


def biconomy_autotrade_open(candle):
    bots = MarketMakerBot.objects.filter(
        status="START", trade_candle=candle, api_key__exchange__name="biconomy"
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
        ref = check_ref_price(token)

        exit_code = biconomy_auto_trade_order_open(
            user_ref_price,
            user_side_choice,
            token,
            user_max_order_value,
            apikey,
            apisec,
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


def biconomy_autotrade_close(candle):

    open_orders = MarketMakerBotAutoTradeQueue.objects.filter(
        status="OPEN", candle=candle, bot__api_key__exchange__name="biconomy"
    )

    for order in open_orders:

        price = order.price
        quantity = order.quantity
        side = order.side
        apikey = order.bot.api_key.api_key
        apisec = order.bot.api_key.api_secret
        token = order.bot.pair_token

        order_id = order.id

        # print(
        #     f"bigone_autotrade_close :: :: {price}, {quantity}, {side},  {apikey}, {apisec}, {token}"
        # )

        exit_code = biconomy_auto_trade_order_close(price, quantity, side, apikey, apisec, token)

        if exit_code["status"] == "success":

            MarketMakerBotAutoTradeQueue.objects.filter(id=order_id).update(
                status="DONE"
            )

        else:

            MarketMakerBotAutoTradeQueue.objects.filter(id=order_id).update(
                status="CLOSE"
            )

    return {"status": "success"}


#
# def biconomy_geneses(data):
#
#
#     pass