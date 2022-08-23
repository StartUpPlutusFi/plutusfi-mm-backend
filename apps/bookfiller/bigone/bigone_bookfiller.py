from apps.bot.ex.bigone import *


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
def book_generator(
    order_quantity, token, user_ref_price, user_max_order_value, side, apikey, apisec
):
    if user_ref_price is None:
        price = bookfiller_check_ref_price(token)
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
        create_order(price, quantity, side, token, apikey, apisec)
        order.append(x + 1)
    return {
        "order": order,
        "prices": prices,
        "quantitys": quantitys,
    }
