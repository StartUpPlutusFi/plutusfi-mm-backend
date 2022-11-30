from hashlib import md5
from urllib.parse import urlencode
import requests
import random
import time

from apps.autotrade.models.models import *
from apps.exchange.services.common.MMlogs import mm_logs
from apps.geneses.models.models import *
from apps.bookfiller.models.models import *
from apps.exchange.helper.crypto_utils import EncryptationTool
from apps.orderLimit.models.models import CancelOrderOrderLimit


def encript_string(query_string):
    return md5(query_string.encode()).hexdigest().upper()


def get_headers() -> dict:
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-SITE-ID": "127",
    }


def get_order_url() -> str:
    return "https://www.biconomy.com/api/v1/private/trade/limit"


def get_order_cancel_url() -> str:
    return "https://www.biconomy.com/api/v1/private/trade/cancel"


def check_ref_price(token) -> tuple[float, bool, float, float]:
    smallest_ask = 0.0
    highest_bid = 0.0
    ask = False

    url = f"https://www.biconomy.com/api/v1/depth?symbol={token}"
    response = requests.get(url)
    response_json = response.json()

    if not response_json["bids"]:
        ref_price = float(float(response_json["asks"][0][0]))
        ask = True
        return ref_price, ask, smallest_ask, highest_bid

    if not response_json["asks"]:
        ref_price = float(response_json["bids"][0][0])
        return ref_price, ask, smallest_ask, highest_bid

    ref_price = (
                        float(response_json["bids"][0][0]) + float(float(response_json["asks"][0][0]))
                ) / 2
    smallest_ask = float(float(response_json["asks"][0][0]))
    highest_bid = float(response_json["bids"][0][0])

    return ref_price, ask, smallest_ask, highest_bid


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

    response = requests.post(get_order_url(), headers=get_headers(), data=params)
    response_json = response.json()
    return response_json


def book_generator(
        limit_generator,
        token,
        user_ref_price,
        user_max_order_value,
        user_side_choice,
        api_key,
        api_sec,
        bookbot_id,
) -> dict:
    try:
        if user_ref_price == 0:
            price, ask, smallest_ask, highest_bid = check_ref_price(token)
        else:
            price = user_ref_price
        multiplier = 1.02
        if user_side_choice == 2:
            multiplier = 0.98
        prices = []
        quantitys = []
        response = []

        for x in range(limit_generator):
            price = multiplier * price
            prices.append(price)
            quantity = user_max_order_value / price
            quantitys.append(quantity)
            time.sleep(0.2)
            code = create_order(price, quantity, token, user_side_choice, api_key, api_sec)
            response.append(code)

            if code['code'] == 10:
                raise ValueError(code, price, quantity, token, user_side_choice)

            CancelOrderBookBot.objects.create(
                bot_id=bookbot_id, cancel_order_id=code["result"]["id"], order_status=True
            )

        return {"response": response}

    except Exception as err:

        return {
            "response": str(err)
        }


def get_budget(token, side):
    url = "https://www.biconomy.com/api/v1/private/user"
    response = requests.get(url, headers=get_headers())
    response_json = response.json()

    for x in response_json["result"]:
        if (x) == "USDT" and side == 2:
            return x["available"]
        if (x) == token and side == 1:
            return x["available"]


def biconomy_cancel_all_orders(bookbot) -> list:
    responses = []
    bot_id = bookbot.id

    cancel_list = CancelOrderBookBot.objects.filter(
        order_status=True, bot_id=bot_id
    ).values("id", "bot", "cancel_order_id")

    for bot in cancel_list:
        params = {
            "api_key": EncryptationTool.read(bookbot.api_key.api_key),
            "market": bookbot.pair_token,
            "order_id": bot["cancel_order_id"],
            "secret_key": EncryptationTool.read(bookbot.api_key.api_secret),
        }

        query_string = urlencode(params)
        md5_params = encript_string(query_string)
        params.pop("secret_key")
        params["sign"] = md5_params

        response = requests.post(
            get_order_cancel_url(), headers=get_headers(), data=params
        )
        response_json = response.json()
        responses.append(response_json)

        CancelOrderBookBot.objects.filter(id=bot["id"], bot_id=bot_id).update(
            order_status=False
        )

    return responses


def biconomy_init_bookbot(data) -> dict:
    try:
        limit_generator = data.number_of_orders
        token = data.pair_token
        user_ref_price = data.user_ref_price
        user_max_order_value = data.order_size
        user_side_choice = data.side
        api_key = EncryptationTool.read(data.api_key.api_key)
        api_sec = EncryptationTool.read(data.api_key.api_secret)
        bookbot_id = data.id

        if user_side_choice == "ASK":
            user_side_choice = 1
        elif user_side_choice == "BID":
            user_side_choice = 2
        else:
            raise ValueError("Invalid side, side must be ASK or BID strings")

        if user_ref_price == 0:
            user_ref_price, ask, smallest_ask, highest_bid = check_ref_price(token)

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
            "status": "success",
            "number_of_orders": len(cancel_codes),
            "cancel_codes": cancel_codes,
        }

    except Exception as err:

        return {
            "status": "error",
            "code": str(err),
            "number_of_orders": 0,
            "cancel_codes": 0,
        }


def biconomy_cancel_one_order(api_key, api_sec, order_id, token):
    params = {
        "api_key": api_key,
        "market": token,
        "order_id": order_id,
        "secret_key": api_sec,
    }

    query_string = urlencode(params)
    md5_params = encript_string(query_string)
    params.pop("secret_key")
    params["sign"] = md5_params

    response = requests.post(get_order_cancel_url(), headers=get_headers(), data=params)
    return response.json()


def biconomy_reference_value(
        user_ref_price: float, user_side_choice: int, user_max_order_value: int, token: str
) -> tuple[float, float]:
    random_operation = 0.0
    smallest_ask = 0.0
    price = 0.0

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
        price = user_ref_price

    total_order = random.randint(1, user_max_order_value)

    if isinstance(price, (int, float)):
        if user_side_choice == 1 or random_operation == smallest_ask:
            price = 0.98 * price
        else:
            price = 1.02 * price
    else:
        raise ValueError(
            {"status": "price is not numeric", "data": [price, total_order]}
        )

    quantity = total_order / price
    return quantity, price


def biconomy_auto_trade_order_open(
        exec_ref_price: float,
        user_side_choice: int,
        token: str,
        user_max_order_value: int,
        api_key: str,
        api_sec: str,
        bot_id: int,
        candle: int,
        operation_type: int = 3,
        status: str = "OPEN",
        quantity: float = None,
        price: float = None,
):
    order = operation_type
    if operation_type != 1 and operation_type != 2:
        order = random.randint(1, 2)

    if quantity is None or price is None:
        quantity, price = biconomy_reference_value(
            exec_ref_price, user_side_choice, user_max_order_value, token
        )

    # ask
    if order == 1:
        exit_code = create_order(price, quantity, token, order, api_key, api_sec)

        log = MarketMakerBotAutoTradeQueue.objects.create(
            bot_id=bot_id,
            price=price,
            quantity=quantity,
            side="ASK",
            status=status,
            candle=candle,
            exec_ref_price=exec_ref_price,
        )

        log.save()

    # bid
    else:
        exit_code = create_order(price, quantity, token, order, api_key, api_sec)

        log = MarketMakerBotAutoTradeQueue.objects.create(
            bot_id=bot_id,
            price=price,
            quantity=quantity,
            side="BID",
            status=status,
            candle=candle,
            exec_ref_price=exec_ref_price,
        )

        log.save()

    return {
        "name": "biconomy_auto_trade_order_open",
        "status": "success",
        "exit_code": exit_code,
        "info": {
            "exec_ref_price": exec_ref_price,
            "quantity": quantity,
            "price": price,
            "user_side_choice": user_side_choice,
            "token": token,
            "user_max_order_value": user_max_order_value,
            "bot_id": bot_id,
            "candle": candle,
            "operation_type": operation_type,
        },
    }


def biconomy_auto_trade_order_close(
        price, quantity, side, apikey, apisec, token
) -> dict:
    try:

        if side == "ASK":
            side = 2  # BID
            exit_code = create_order(price, quantity, token, side, apikey, apisec)

        elif side == "BID":
            side = 1  # ASK
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
            "error": f"{str(e)}",
        }


def biconomy_new_autotrade(candle: int):
    result = []

    bots = MarketMakerBot.objects.filter(
        status="START", trade_candle=candle, api_key__exchange__name="biconomy"
    )

    for data in bots:

        bot_id = data.id
        apikey = EncryptationTool.read(data.api_key.api_key)
        apisec = EncryptationTool.read(data.api_key.api_secret)
        user_side_choice = data.side
        user_max_order_value = data.trade_amount
        token = data.pair_token
        user_ref_price = data.user_ref_price
        side = data.side

        if user_ref_price == 0:
            exec_ref_price, ask, smallest_ask, highest_bid = check_ref_price(token)
        else:
            exec_ref_price = user_ref_price

        if side != 1 and side != 2:
            side = random.randint(1, 2)

        quantity, price = biconomy_reference_value(
            exec_ref_price, user_side_choice, user_max_order_value, token
        )

        biconomy_autotrade_open_result = biconomy_auto_trade_order_open(
            exec_ref_price,
            user_side_choice,
            token,
            user_max_order_value,
            apikey,
            apisec,
            bot_id,
            candle,
            side,
            status="NMOPN",
            quantity=quantity,
            price=price,
        )

        if side == 1:
            side = 2
        elif side == 2:
            side = 1
        else:
            raise ValueError(["at biconomy_new_autotrade invalid side option", side])

        biconomy_autotrade_close_result = biconomy_auto_trade_order_open(
            exec_ref_price,
            user_side_choice,
            token,
            user_max_order_value,
            apikey,
            apisec,
            bot_id,
            candle,
            side,
            status="NMCLO",
            quantity=quantity,
            price=price,
        )

        edata = {
            "autotrade_open": biconomy_autotrade_open_result,
            "autotrade_close": biconomy_autotrade_close_result,
            "info": {
                "exec_ref_price": exec_ref_price,
                "quantity": quantity,
                "price": price,
                "user_side_choice": user_side_choice,
                "user_max_order_value": user_max_order_value,
                "token": token,
                "side": data.side,
                "status": data.status,
                "bot_id": bot_id,
                "candle": candle,
            },
        }

        result.append(edata)

    return result


def biconomy_market_creator_open(geneses_bot) -> dict:
    user_order_size_bid = geneses_bot.user_order_size_bid
    user_order_size_ask = geneses_bot.user_order_size_ask
    token = geneses_bot.token
    apikey = EncryptationTool.read(geneses_bot.api_key.api_key)
    apisec = EncryptationTool.read(geneses_bot.api_key.api_secret)
    market_value = geneses_bot.market_value
    spread_distance = geneses_bot.spread_distance
    gid = geneses_bot.id

    try:
        price_bid = market_value * (1 - (spread_distance / 100.0))
        quantity_bid = user_order_size_bid / price_bid
        exit_code1 = f"The bid price will be {price_bid} and the bid quantity price will be {quantity_bid}"
        exit_code_bid = create_order(price_bid, quantity_bid, token, 2, apikey, apisec)

        GenesesQueue.objects.create(
            geneses_id=gid, cancel_code=exit_code_bid["result"]["id"], status="OPEN"
        )

        price_ask = market_value * ((spread_distance / 100.0) + 1.0)
        quantity_ask = user_order_size_ask / price_ask
        exit_code2 = f"The ask price will be {price_ask} and the ask quantity price will be {quantity_ask}"
        exit_code_ask = create_order(price_ask, quantity_ask, token, 1, apikey, apisec)

        GenesesQueue.objects.create(
            geneses_id=gid, cancel_code=exit_code_ask["result"]["id"], status="OPEN"
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
        return {
            "status": "error",
            "code": str(e),
        }


def biconomy_market_creator_close(geneses_bot) -> dict:
    responses = []

    api_key = EncryptationTool.read(geneses_bot.api_key.api_key)
    api_sec = EncryptationTool.read(geneses_bot.api_key.api_secret)
    gid_id = geneses_bot.id

    cancel_list = GenesesQueue.objects.filter(status="OPEN", geneses_id=gid_id)

    for reg in cancel_list:

        order_id = reg.cancel_code
        token = reg.geneses.token

        response_json = biconomy_cancel_one_order(api_key, api_sec, order_id, token)

        exit = {"code": 10, "message": "Order not found", "result": None}

        try:
            if response_json == exit:
                GenesesQueue.objects.filter(id=reg.id, geneses_id=gid_id).update(
                    status="FAIL"
                )
            else:
                GenesesQueue.objects.filter(id=reg.id, geneses_id=gid_id).update(
                    status="DONE"
                )

        except Exception as err:

            return {
                "status": f"fail to cancel order {reg.cancel_code}",
                "code": str(err),
            }

        responses.append(
            {
                "status": "success",
                "code": response_json["result"],
            }
        )

    return {"status": "success", "responses": responses}


def biconomy_order_limit_open(order_limit_cfg) -> dict:
    try:
        price = order_limit_cfg.price
        quantity = order_limit_cfg.quantity
        token = order_limit_cfg.pair_token
        side = order_limit_cfg.side
        api_key = EncryptationTool.read(order_limit_cfg.api_key.api_key)
        api_sec = EncryptationTool.read(order_limit_cfg.api_key.api_secret)
        order_limit_id = order_limit_cfg.id

        response = create_order(price, quantity, token, side, api_key, api_sec)
        order_id = response["result"]["id"]

        CancelOrderOrderLimit.objects.create(
            OrderLimitCfg_id=order_limit_id, cancel_order_id=order_id, order_status=True
        )

        return {
            "status": "success",
            "op": {
                "order_id": order_id,
            },
        }

    except Exception as err:

        return {
            "status": "error",
            "op": {
                "result": str(err)
            }
        }


def biconomy_order_limit_close(order_limit_cfg) -> dict:
    try:
        responses = []
        order_limit_cfg_id = order_limit_cfg.id

        cancel_list = CancelOrderOrderLimit.objects.filter(
            OrderLimitCfg_id=order_limit_cfg_id, order_status=True
        ).values("id", "OrderLimitCfg", "cancel_order_id")

        api_key = EncryptationTool.read(order_limit_cfg.api_key.api_key)
        api_sec = EncryptationTool.read(order_limit_cfg.api_key.api_secret)
        token = order_limit_cfg.pair_token

        for cfg in cancel_list:
            order_id = cfg["cancel_order_id"]

            response = biconomy_cancel_one_order(api_key, api_sec, order_id, token)
            responses.append(response)

            CancelOrderOrderLimit.objects.filter(
                id=cfg["id"], OrderLimitCfg=order_limit_cfg_id
            ).update(order_status=False)

        return {
            "status": "success",
            "op": {
                "result": responses,
            },
        }

    except Exception as err:

        return {
            "status": "error",
            "op": {
                "result": str(err)
            }
        }
