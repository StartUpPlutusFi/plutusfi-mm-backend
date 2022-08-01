import requests
import time
import jwt


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
