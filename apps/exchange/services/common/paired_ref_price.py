import requests
import random
import json


def bit_pairing_value() -> float:
    response = requests.get('https://www.biconomy.com/api/v1/bit/price')
    paired_value = float(format(response.json(), ".18f"))
    paired_price = paired_value * random.uniform(0.99, 1.00)
    return paired_price


def paired_price_option_selector(option: int) -> float:
    if option == 1:
        return bit_pairing_value()
    else:
        return -1
