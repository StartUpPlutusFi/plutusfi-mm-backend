import random

from apps.dashboard.ex.bigone import *


def random_bid_ask_order(user_ref_price, user_side_choice, user_max_order_value, apikey, apisec, token):
    # if True:
    order = random.randint(1, 2)
    exit = []

    if order == 1:
        quantity, price = ref_value(
            user_ref_price, user_side_choice, user_max_order_value, token)

        exit.append(create_order(price, quantity, side="BID",
                    token=token, apikey=apikey,  apisec=apisec))
        time.sleep(10)
        exit.append(create_order(price, quantity, side="ASK",
                    token=token, apikey=apikey,  apisec=apisec))

    else:
        quantity, price = ref_value(
            user_ref_price, user_side_choice, user_max_order_value, token)

        exit.append(create_order(price, quantity, side="ASK",
                    token=token, apikey=apikey,  apisec=apisec))
        time.sleep(10)
        exit.append(create_order(price, quantity, side="BID",
                    token=token, apikey=apikey,  apisec=apisec))

    return exit
