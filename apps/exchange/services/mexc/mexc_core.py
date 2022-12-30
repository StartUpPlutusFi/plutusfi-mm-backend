from datetime import datetime

from MexcClient.client import MexcClient
from MexcClient.Enums import EnumKlineInterval
from MexcClient.Enums.enums import EnumOrderSide, EnumOrderType
import requests
import random
import time
import numpy as np

from apps.autotrade.models.models import *
from apps.geneses.models.models import *
from apps.bookfiller.models.models import *
from apps.exchange.helper.crypto_utils import EncryptationTool
from apps.orderLimit.models.models import CancelOrderOrderLimit


def mexc_check_ref_price(token, api_key, api_sec) -> tuple[float, bool, float, float]:
    smallest_ask = 0.0
    highest_bid = 0.0
    ask = False
    client = MexcClient(api_key, api_sec)
    response_json = client.order_book_of_symbol(token)

    if not response_json['bids']:
        ref_price = float(response_json['asks'][0][0])
        ask = True
        return ref_price, ask, smallest_ask, highest_bid
    if not (response_json['asks']):
        ref_price = float(response_json['bids'][0][0])
        return ref_price, ask, smallest_ask, highest_bid
    ref_price = ((float(response_json['bids'][0][0]) + float(response_json['asks'][0][0])) / 2)
    smallest_ask = float(response_json['asks'][0][0])
    highest_bid = float(response_json['bids'][0][0])

    return ref_price, ask, smallest_ask, highest_bid


def mexc_create_order(price, quantity, token, side, api_key, api_sec) -> dict:
    try:
        client = MexcClient(api_key, api_sec)
        timestamp = datetime.now().timestamp()
        response = None
        if side == "BID":
            response = client.create_new_order(
                token,
                EnumOrderSide.BUY,
                EnumOrderType.LIMIT,
                int(timestamp),
                quantity=quantity,
                price=str(price),
            )
        if side == "ASK":
            response = client.create_new_order(
                token,
                EnumOrderSide.SELL,
                EnumOrderType.LIMIT,
                int(timestamp),
                quantity=quantity,
                price=str(price),
            )
        return {
            "status": "success",
            "response": response
        }
    except Exception as err:
        return {
            "status": "success",
            "local": "mexc_create_order",
            "response": str(err),
        }


def mexc_cancel_one_order(api_key, api_sec, order_id, token) -> dict:
    try:
        client = MexcClient(api_key, api_sec)
        timestamp = datetime.now().timestamp()
        response = client.cancel_order(
            symbol=token,
            order_id=order_id,
            timestamp=int(timestamp), )
        return {
            "status": "success",
            "response": response
        }
    except Exception as err:
        return {
            "status": "success",
            "loc": "mexc_cancel_one_order",
            "response": str(err),
        }


def mexc_cancel_all_orders(bookbot) -> dict:
    try:
        responses = []
        bot_id = bookbot.id

        cancel_list = CancelOrderBookBot.objects.filter(
            order_status=True, bot_id=bot_id
        ).values("id", "bot", "cancel_order_id")

        for bot in cancel_list:
            api_key = EncryptationTool.read(bookbot.api_key.api_key)
            secret_key = EncryptationTool.read(bookbot.api_key.api_secret)
            token = bookbot.pair_token
            order_id = bot["cancel_order_id"]
            response_json = mexc_cancel_one_order(
                api_key, secret_key, order_id, token
            )
            responses.append(response_json)

            CancelOrderBookBot.objects.filter(id=bot["id"], bot_id=bot_id).update(
                order_status=False
            )

        return {
            "status": "success",
            "response": responses,
            "bot_id": bot_id,
        }
    except Exception as err:
        return {
            "status": "success",
            "bot_id": bookbot.id,
            "loc": "mexc_cancel_all_orders",
            "response": str(err),
        }


def mexc_book_generator(
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
            price, ask, smallest_ask, highest_bid = mexc_check_ref_price(token, api_key, api_sec)
        else:
            price = user_ref_price
        multiplier = 1.02
        if user_side_choice == "BID":
            multiplier = 0.98
        params = []
        response = []

        for x in range(limit_generator):
            price = multiplier * price
            quantity = user_max_order_value / price

            nprice = str("%.18f" % price)

            code = mexc_create_order(nprice, quantity, token, user_side_choice, api_key, api_sec)
            params.append({
                "price": nprice,
                "quantity": quantity,
                "token": token,
                "user_side_choice": user_side_choice
            })
            response.append(code)

            if "code" in code["response"]:
                if code["response"]["code"] == 700008:
                    return {
                        "status": "error",
                        "response": code["response"],
                        "params": params,
                    }

            CancelOrderBookBot.objects.create(
                bot_id=bookbot_id, cancel_order_id=code["response"]["orderId"], order_status=True
            )

        return {
            "status": "success",
            "response": response,
            "params": params,
        }

    except Exception as err:

        return {
            "status": "error",
            "local": "mexc_book_generator",
            "response": str(err),
            "p": user_ref_price
        }


def mexc_init_bookbot(data) -> dict:
    try:
        limit_generator = data.number_of_orders
        token = data.pair_token
        user_ref_price = data.user_ref_price
        user_max_order_value = data.order_size
        user_side_choice = data.side
        api_key = EncryptationTool.read(data.api_key.api_key)
        api_sec = EncryptationTool.read(data.api_key.api_secret)
        bookbot_id = data.id

        if user_side_choice != "ASK" and user_side_choice != "BID":
            raise ValueError("Invalid side, side must be ASK or BID strings")

        if user_ref_price == 0:
            user_ref_price, ask, smallest_ask, highest_bid = mexc_check_ref_price(token, api_key, api_sec)

        cancel_codes = mexc_book_generator(
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


def mexc_reference_value(
        user_ref_price: float, user_side_choice: int, user_max_order_value: int, token: str, api_key: str, api_sec: str
) -> tuple[float, float]:
    ask = False
    price, smallest_ask, highest_bid, random_operation = 0, 0, 0, 0

    if user_ref_price == 0:
        ref_price, ask, smallest_ask, highest_bid = mexc_check_ref_price(token, api_key, api_sec)
    else:
        ref_price = user_ref_price
        ask = False
        price = ref_price
    if smallest_ask > 0 and highest_bid > 0:
        if user_side_choice == 1:
            price = random.uniform(ref_price, smallest_ask)
        elif user_side_choice == 2:
            price = random.uniform(ref_price, highest_bid)
        else:
            random_list = [smallest_ask, highest_bid]
            random_operation = random.choice(random_list)
            price = random.uniform(ref_price, random_operation)
    else:
        price = ref_price

    total_order = random.randint(5, user_max_order_value)

    # Gets the price and quantity necessary to make an order from (reference price * 1.02) or * 0.98
    if ask or user_side_choice == 1 or random_operation == smallest_ask:
        price_mult = random.uniform(1.00, 0.98)
        price = price_mult * price
    else:
        price_mult = random.uniform(1.00, 1.02)
        price = price_mult * price
    quantity = total_order / price
    return quantity, price


def mexc_auto_trade_order_open(
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
        quantity, price = mexc_reference_value(
            exec_ref_price, user_side_choice, user_max_order_value, token
        )

    # ask
    if order == 1:
        exit_code = mexc_create_order(price, quantity, token, order, api_key, api_sec)

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
        exit_code = mexc_create_order(price, quantity, token, order, api_key, api_sec)

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


def mexc_auto_trade_order_close(
        price, quantity, side, apikey, apisec, token
) -> dict:
    try:

        if side == "ASK":
            exit_code = mexc_create_order(price, quantity, token, side, apikey, apisec)

        elif side == "BID":
            exit_code = mexc_create_order(price, quantity, token, side, apikey, apisec)
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


def mexc_new_autotrade(candle: int):
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
            exec_ref_price, ask, smallest_ask, highest_bid = mexc_check_ref_price(token, apikey, apisec)
        else:
            exec_ref_price = user_ref_price

        if side != 1 and side != 2:
            side = random.randint(1, 2)

        quantity, price = mexc_reference_value(
            exec_ref_price, user_side_choice, user_max_order_value, token, apikey, apisec
        )

        quantity = quantity * random.uniform(0.1, 0.99)

        biconomy_autotrade_open_result = mexc_auto_trade_order_open(
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

        biconomy_autotrade_close_result = mexc_auto_trade_order_open(
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


def mexc_market_creator_open(geneses_bot) -> dict:
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
        exit_code_bid = mexc_create_order(price_bid, quantity_bid, token, 2, apikey, apisec)

        GenesesQueue.objects.create(
            geneses_id=gid, cancel_code=exit_code_bid["orderId"], status="OPEN"
        )

        price_ask = market_value * ((spread_distance / 100.0) + 1.0)
        quantity_ask = user_order_size_ask / price_ask
        exit_code2 = f"The ask price will be {price_ask} and the ask quantity price will be {quantity_ask}"
        exit_code_ask = mexc_create_order(price_ask, quantity_ask, token, 1, apikey, apisec)

        GenesesQueue.objects.create(
            geneses_id=gid, cancel_code=exit_code_ask["orderId"], status="OPEN"
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


def mexc_market_creator_close(geneses_bot) -> dict:
    responses = []

    api_key = EncryptationTool.read(geneses_bot.api_key.api_key)
    api_sec = EncryptationTool.read(geneses_bot.api_key.api_secret)
    gid_id = geneses_bot.id

    cancel_list = GenesesQueue.objects.filter(status="OPEN", geneses_id=gid_id)

    for reg in cancel_list:

        order_id = reg.cancel_code
        token = reg.geneses.token

        response_json = mexc_cancel_one_order(api_key, api_sec, order_id, token)

        try:
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


def mexc_order_limit_open(order_limit_cfg) -> dict:
    try:
        price = order_limit_cfg.price
        quantity = order_limit_cfg.quantity
        token = order_limit_cfg.pair_token
        side = order_limit_cfg.side
        api_key = EncryptationTool.read(order_limit_cfg.api_key.api_key)
        api_sec = EncryptationTool.read(order_limit_cfg.api_key.api_secret)
        order_limit_id = order_limit_cfg.id

        response = mexc_create_order(price, quantity, token, side, api_key, api_sec)
        order_id = response["orderId"]

        CancelOrderOrderLimit.objects.create(
            OrderLimitCfg_id=order_limit_id, cancel_order_id=order_id, order_status=True
        )

        return {
            "status": "success",
            "operation_result": {
                "order_id": order_id,
            },
        }

    except Exception as err:

        return {
            "status": "error",
            "operation_result": {
                "result": str(err)
            }
        }


def mexc_order_limit_close(order_limit_cfg) -> dict:
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

            response = mexc_cancel_one_order(api_key, api_sec, order_id, token)
            responses.append(response)

            CancelOrderOrderLimit.objects.filter(
                id=cfg["id"], OrderLimitCfg=order_limit_cfg_id
            ).update(order_status=False)

        return {
            "status": "success",
            "operation_result": {
                "result": responses,
            },
        }

    except Exception as err:

        return {
            "status": "error",
            "operation_result": {
                "result": str(err)
            }
        }
