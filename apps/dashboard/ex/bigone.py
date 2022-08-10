import requests
import time
import random
import jwt
import json


def biconomy_configuration_set():

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-SITE-ID": "127",
    }

    API_KEY = "585f82c5-09cf-4288-a512-8bbe0f3067eb"
    SECRET_KEY = "594d28ac-b379-4418-b5af-1ca4e089c4fd"

    return {
        "base_url": "https://www.biconomy.com/api/v1/private/trade/limit",
        "api_key": API_KEY,
        "api_secret": SECRET_KEY,
        "headers": headers,
    }


def bigone_configuration_set():

    API_KEY = "7654e9c4-03ad-11ed-b82e-1a11d26d1a6a"
    SECRET_KEY = "3393DBF2490A73B14B5414DBCF6C9512A05F6D492A7CE1EB077D3EA139577303"

    header = {
        "alg": "HS256",
        "typ": "JWT",
    }

    payload = {
        "type": "OpenAPIV2",
        "sub": API_KEY,
        "nonce": str(time.time_ns()),
        "recv_window": "50",
    }

    JWT = jwt.encode(
        payload=payload,
        headers=header,
        key=SECRET_KEY,
        algorithm="HS256",
    )

    return {
        "base_url": "https://big.one/api/v3/",
        "api_key": API_KEY,
        "api_secret": SECRET_KEY,
        "headers": "headers",
        "jwt": JWT,
    }


def bigone_is_alive():

    cfg = bigone_configuration_set()
    url = "/ping"
    response = requests.get(f"{cfg['base_url']}{url}")
    return response.json()


def bigone_order_book(asset_pair_name="EOS-BTC"):

    cfg = bigone_configuration_set()
    url = f"/asset_pairs/{asset_pair_name}/depth"
    response = requests.get(f"{cfg['base_url']}{url}")
    return response.json()


def bigone_jwt_test():

    cfg = bigone_configuration_set()
    url = "/viewer/accounts"

    response = requests.get(
        f"{cfg['base_url']}{url}", headers={"Authorization": f"Bearer { cfg['jwt'] }"}
    )
    return {
        "code": response.status_code,
        "json": response.json(),
    }


def bigone_view_acount():

    cfg = bigone_configuration_set()
    url = "/viewer/accounts"

    response = requests.get(
        f"{cfg['base_url']}{url}", headers={"Authorization": f"Bearer { cfg['jwt'] }"}
    )
    return {
        "code": response.status_code,
        "json": response.json(),
    }

def ping():
    PING_URL = 'https://big.one/api/v3/ping'
    ping = requests.get(PING_URL)
    ping_json = ping.json()
    TIMESTAMP = ping_json["data"]["Timestamp"]
    return TIMESTAMP


def get_order_header_encoded(apikey, apisec):


    payload = {
        'type': 'OpenAPIV2',
        'sub': apikey,
        'nonce': str(ping()),
        'recv_window': '50'
    }
    token = jwt.encode(
        headers=get_headers(),
        payload=payload,
        key=apisec,
    )
    header_encoded = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    return header_encoded


def get_order_url():
    BASE_URL = 'https://big.one/api/v3/viewer/orders'
    return BASE_URL

def check_ref_price(token):
    smallest_ask = 0.0
    highest_bid = 0.0
    ask = False

    BASE_URL = f'https://big.one/api/v3/asset_pairs/{token}/depth'
    r = requests.get(BASE_URL)
    response_json = r.json()

    if not response_json['data']['bids']:
        ref_price = float(response_json['data']['asks'][0]['price'])
        ask = True
        print(
            f"There is no bids so the ref price value is the lowest ask: {ref_price}")
        return ref_price, ask, smallest_ask, highest_bid
    if not response_json['data']['asks']:
        ref_price = float(response_json['data']['bids'][0]['price'])
        print(
            f"There is no asks so the ref price value is the highest bid: {ref_price}")
        return ref_price, ask, smallest_ask, highest_bid
    ref_price = (float(response_json['data']['bids'][0]['price']) +
                 float(response_json['data']['asks'][0]['price']))/2
    smallest_ask = float(response_json['data']['asks'][0]['price'])
    highest_bid = float(response_json['data']['bids'][0]['price'])

    return ref_price, ask, smallest_ask, highest_bid


def get_headers():
    headers = {
        'alg': 'HS256',
        'typ': 'JWT',
    }
    return headers


def create_order(price, quantity, side, token, apikey, apisec):

    params = {
        "asset_pair_name": token,
        "side": side,
        "price": str(price),
        "amount": str(quantity),
        "type": "LIMIT",
    }

    json_params = json.dumps(params, indent=4)
    r = requests.post(
        get_order_url(), headers=get_order_header_encoded(apikey, apisec), data=json_params
    )
   
    return r.json()

def ref_value(user_ref_price, user_side_choice, user_max_order_value, token):
    ask = False
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
        ref_price = user_ref_price
        ask = False
        price = ref_price
    total_order = 0

    total_order = random.randint(12, user_max_order_value)
    print(f"Total order value in USDT: {total_order}")
    # Gets the price and quantity necessary to make an order from (reference price * 1.02) or * 0.98
    if ask or user_side_choice == 1 or random_operation == smallest_ask:
        price = 0.98 * price
    else:
        price = ((1.02) * price)
    print(f"Price {price}")
    quantity = total_order/price
    print(f"Quantity {quantity}")
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