# Create your views here.
# BOOK ORDER CREATOR BASED ON REF_PRICE AND MINIMAL QUANTITY

import jwt
import requests
import json


def ping():
    PING_URL = "https://big.one/api/v3/ping"
    ping = requests.get(PING_URL)
    ping_json = ping.json()
    TIMESTAMP = ping_json["data"]["Timestamp"]
    return TIMESTAMP


def get_order_header_encoded():
    payload = {
        "type": "OpenAPIV2",
        "sub": get_apikey(),
        "nonce": str(ping()),
        "recv_window": "50",
    }
    token = jwt.encode(headers=get_headers(), payload=payload, key=get_secretkey())
    header_encoded = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }
    return header_encoded


def get_order_url():
    BASE_URL = "https://big.one/api/v3/viewer/orders"
    return BASE_URL


def check_ref_price(coin):
    ask = False
    BASE_URL = f"https://big.one/api/v3/asset_pairs/{coin}/depth"
    r = requests.get(BASE_URL)
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


def get_headers():
    headers = {
        "alg": "HS256",
        "typ": "JWT",
    }
    return headers


def get_apikey():

    API_KEY = ""  # GET THE API KEY
    return API_KEY


def get_secretkey():

    SECRET_KEY = ""  # GET THE SECRET KEY
    return SECRET_KEY


def create_order(price, quantity, side, token):
    params = {
        "asset_pair_name": token,
        "side": side,
        "price": str(price),
        "amount": str(quantity),
        "type": "LIMIT",
    }

    json_params = json.dumps(params, indent=4)
    r = requests.post(
        get_order_url(), headers=get_order_header_encoded(), data=json_params
    )
   
    return r.json()


# Gets the price and quantity necessary to make an order from (reference price * 1.02)
def book_generator(order_quantity, token, user_ref_price, user_max_order_value, side):
    if user_ref_price == None:
        price = check_ref_price(token)
    else:
        price = user_ref_price
    multiplier = 1.02
    if side == "BID":
        multiplier = 0.98
    prices = []
    quantitys = []
    order = []
    for x in range(order_quantity):
        price = multiplier * price
        prices.append(price)
        quantity = user_max_order_value / price
        quantitys.append(quantity)
        # create_order(price, quantity, side, token)
        order.append(x + 1)
    return {
      "order": order,  
      "prices": prices,  
      "quantitys": quantitys, 
    }


def get_budget(coin, side):
    BASE_URL = "https://big.one/api/v3/viewer/accounts"
    r = requests.get(BASE_URL, headers=get_order_header_encoded())
    response_json = r.json()
    for x in response_json["data"]:
        if x["asset_symbol"] == "USDT" and side == "BID":
            return x["balance"]
        if x["asset_symbol"] == coin and side == "ASK":
            return x["balance"]


# mudar pra funçoes depois
def init():

    user_max_order_value = 0 #Order amount size 12 - ~
    token = "GAMAO-USDT" # token
    order_quantity = 2 # Order qunatity
    user_ref_price = check_ref_price(token) # Order user input 
    side = 'ASK' # 'BID'
    
    result = book_generator(
        order_quantity, token, user_ref_price, user_max_order_value, side
    )

    return result