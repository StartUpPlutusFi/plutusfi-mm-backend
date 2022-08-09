import jwt
import requests
import random
import time


def ping():
    PING_URL = 'https://big.one/api/v3/ping'
    ping = requests.get(PING_URL)
    ping_json = ping.json()
    TIMESTAMP = ping_json["data"]["Timestamp"]
    return TIMESTAMP


def get_order_header_encoded():
    payload = {
        'type': 'OpenAPIV2',
        'sub': get_apikey(),
        'nonce': str(ping()),
        'recv_window': '50'
    }
    token = jwt.encode(
        headers=get_headers(),
        payload=payload,
        key=get_secretkey()
    )
    header_encoded = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    return header_encoded


def get_order_url():
    BASE_URL = 'https://big.one/api/v3/viewer/orders'
    return BASE_URL


def check_ref_price():
    smallest_ask = 0.0
    highest_bid = 0.0
    ask = False
    BASE_URL = f'https://big.one/api/v3/asset_pairs/{coin}/depth'
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
    print(f"The ref price value is: {ref_price}")
    print(
        f"The smallest ASK is {smallest_ask} and the highest BID is {highest_bid}")

    return ref_price, ask, smallest_ask, highest_bid


def get_headers():
    headers = {
        'alg': 'HS256',
        'typ': 'JWT',
    }
    return headers


def get_apikey():

    API_KEY = ''  # GET THE API KEY
    return API_KEY


def get_secretkey():

    SECRET_KEY = ''  # GET THE SECRET KEY
    return SECRET_KEY

def ref_value(user_ref_price, user_side_choice, user_max_order_value):
    ask = False
    smallest_ask = 0.0
    price = 0.0
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


def random_bid_ask_order(user_ref_price, user_side_choice, user_max_order_value):
    while True:
        order = random.randint(1, 2)

        if order == 1:
            quantity, price = ref_value(user_ref_price, user_side_choice, user_max_order_value)
            print(
                f"Creating an order with bid quantity: {quantity} bid price: {price}")
            #create_bid(price, quantity)
            time.sleep(10)
            print("Order created")
            print(
                f"Creating an order with ask quantity: {quantity} ask price: {price}")
            #create_ask(price, quantity)
            print("Order created")
        if order == 2:
            quantity, price = ref_value(user_ref_price, user_side_choice, user_max_order_value)
            print(
                f"Creating an order with ask quantity: {quantity} ask price: {price}")
            #create_ask(price, quantity)
            print("Order created")
            time.sleep(2)
            print(
                f"Creating an order with bid quantity: {quantity} bid price: {price}")
            #reate_bid(price, quantity)
            print("Order created")
        time.sleep(user_max_time*60)


if __name__ == '__main__':

    user_max_order_value = 12 # Order amont

    user_max_time = int(input(
        "Please input a max value of time in minutes for the app to redo the order:  "))

    user_choice = 0
    while 1 > user_choice or user_choice > 3:
        try:
            user_choice = int(input(
                "Please choose a coin (1 for AUV-USDT), (2 for GAMAO-USDT) and (3 for GRUSH-USDT):  "))
        except ValueError:
            print("Invalid value")
    if user_choice == 1:
        coin = "AUV-USDT"
    elif user_choice == 2:
        coin = "GAMAO-USDT"
    else:
        coin = "GRUSH-USDT"
    check_ref_price()
    user_ref_price = float(input(
        "Would you like to choose a ref_price? If yes input a value and if no just press enter: ") or "0")
    if user_ref_price == 0:
        while 1 > user_side_choice or user_side_choice > 3:
            try:
                user_side_choice = int(input(
                    "Choose a side for the orders to be made (1 for higher than the ref_priceup to the lowest ASK), (2 for lower than the ref_price up to the highest bid) or (3 for it to randomly pick):  "))
            except ValueError:
                print("Invalid value")

    

    random_bid_ask_order(user_ref_price, user_side_choice, user_max_order_value)
