from django.shortcuts import render

# Create your views here.
# BOOK ORDER CREATOR BASED ON REF_PRICE AND MINIMAL QUANTITY

# modulos
import jwt
import pandas as pd
from urllib.parse import urljoin, urlencode
import requests
import json

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


def check_ref_price(coin):
    ask = False
    BASE_URL =f'https://big.one/api/v3/asset_pairs/{coin}/depth'
    r = requests.get(BASE_URL)
    response_json = r.json()
    if not response_json['data']['bids']:
      ref_price = float(response_json['data']['asks'][0]['price'])
      ask = True
      print(f"There is no bids so the ref price value is the lowest ask: {ref_price}")
      return ref_price, ask
    if not response_json['data']['asks']:
      ref_price = float(response_json['data']['bids'][0]['price'])
      print(f"There is no asks so the ref price value is the highest bid: {ref_price}")
      return ref_price, ask
    ref_price = (float(response_json['data']['bids'][0]['price']) + float(response_json['data']['asks'][0]['price']))/2
    print (f"The ref price value is: {ref_price}")
    return ref_price, ask

def get_headers():
    headers = {
    'alg': 'HS256',
    'typ': 'JWT',
    }
    return headers

def get_apikey():

    API_KEY = '' #GET THE API KEY
    return API_KEY

def get_secretkey():

    SECRET_KEY = ''#GET THE SECRET KEY
    return SECRET_KEY

def create_order(price, quantity, side):
    params = {"asset_pair_name":coin,
              "side":side,
              "price":str(price),
              "amount":str(quantity), 
              "type":"LIMIT"
              }

    json_params = json.dumps(params, indent=4)
    r = requests.post(get_order_url(), headers=get_order_header_encoded(), data=json_params)
    response_json = r.json()
    print (response_json)


# Gets the price and quantity necessary to make an order from (reference price * 1.02)
def book_generator(limit_generator, coin, user_ref_price, user_max_order_value, side):
    price = 0.0
    if user_ref_price == 0:
      price, ask = check_ref_price(coin)
    else:
      price = user_ref_price
    multiplier = 1.02
    if side == "BID":
      multiplier = 0.98
    prices = []
    quantitys = []
    order = []
    for x in range(limit_generator):
        price = (multiplier * price)
        prices.append(price)
        quantity = user_max_order_value/price
        quantitys.append(quantity)
        ##create_order(price, quantity, side)
        order.append(x+1)
    return order, prices, quantitys


def get_budget(coin,side):
  BASE_URL = 'https://big.one/api/v3/viewer/accounts'
  r = requests.get(BASE_URL, headers=get_order_header_encoded())
  response_json = r.json()
  for x in response_json["data"]:
      if (float(x["asset_symbol"]) == "USDT" and side == "BID"):
          return x["balance"]
      if(float(x["asset_symbol"]) == coin and side == "ASK"):
          return x["balance"]




#mudar pra funçoes depois
if __name__ == '__main__':
    user_side_choice = 0
    user_max_order_value = 0
    while 12 > user_max_order_value:
        try:
            user_max_order_value= int(input("Please input a max value for the total order that is bigger than 12:  "))
        except ValueError:
            print("Invalid value")

    user_choice = 0
    while 1 > user_choice or user_choice > 3:
        try:
            user_choice= int(input("Please choose a coin (1 for AUV-USDT), (2 for GAMAO-USDT) and (3 for GRUSH-USDT):  "))
        except ValueError:
            print("Invalid value")
    if user_choice == 1:
      coin = "AUV-USDT"
    elif user_choice == 2:
      coin = "GAMAO-USDT"
    else:
      coin = "GRUSH-USDT"
    check_ref_price(coin)
    user_ref_price = float(input("Would you like to choose a ref_price? If yes input a value and if no just press enter: ") or "0")


   
    while 1 > user_side_choice or user_side_choice > 2:
        try:
            user_side_choice= int(input("Please choose a if you want to create a BID or an ASK book(1 for BID and 2 for ASK):  "))
        except ValueError:
            print("Invalid value")
    if user_side_choice == 1:
      side = "BID"
    else:
      side = "ASK"

    # Creates up to 50 orders based on the user input limited by the budget
    limit_generator = 0
    while 1 > limit_generator or 50 < limit_generator:
        try:
            limit_generator = int(input("Please input a value between 1 and 50 values you would like to add to the book:  "))
            # Checks if the total value of the orders does not exceed the budget
            ''' budget = get_budget()
            if (limit_generator * 10 > (budget * 0.95)):
                raise ValueError("Value bigger than budget") '''
        except ValueError:
            print("Invalid value")
    
    order,prices,quantitys = book_generator(limit_generator, coin, user_ref_price, user_max_order_value, side)
    # Shows the price and quantity of each order in a dataframe
    list_of_tuples = list(zip(order,prices,quantitys))
    list_of_tuples
    df = pd.DataFrame(list_of_tuples, columns= ['BidOrder','BidPrice', 'BidQtyMM'])
    print(df)


