import time
import hmac
import hashlib
import requests
import logging
import time
from typing import Literal


# --- API CLIENT ---
class RoostooAPIClient:
    API_BASE_URL = "https://mock-api.roostoo.com"
    API_KEY = "qZq5wGHqbuMy57a3XET1474Gh0ecThyfwDpInTJVTWdyfjC3nc8INgg0RVUPUvO5"
    SECRET_KEY = "hCptnFENrmd2ztKaGKOIN7ghFmoiEPr10ufQdI5pwEnNJoeJ4CHc1zDPJOw2VYol"

    def __init__(self, max_trade=5, api_key=API_KEY, secret_key=SECRET_KEY, base_url=API_BASE_URL):
        self.api_key = api_key
        self.secret_key = secret_key.encode()
        self.base_url = base_url
        self.max_trade = max_trade
        self.open_trade = 0
        logging.info(f"RoostooAPIClient initialized, account net value: {self.get_account_net_value()}")

    def _get_timestamp(self):
        return str(int(time.time() * 1000))

    def _sign(self, params: dict):
        sorted_items = sorted(params.items())
        query_string = "&".join([f"{key}={value}" for key, value in sorted_items])
        signature = hmac.new(self.secret_key, query_string.encode(), hashlib.sha256).hexdigest()
        return signature, query_string

    def _headers(self, params: dict, is_signed=False):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if is_signed:
            signature, _ = self._sign(params)
            headers["RST-API-KEY"] = self.api_key
            headers["MSG-SIGNATURE"] = signature
        return headers

    def _handle_response(self, response):
        if response.status_code != 200:
            logging.info(f"HTTP Error: {response.status_code} {response.text}")
            return None
        try:
            data = response.json()
        except Exception as e:
            logging.info(f"JSON decode error: {e}, Response: {response.text}")
            return None
        return data

    def list_of_coins(self):
        response = requests.get(self.base_url + "/v3/exchangeInfo")
        try:
            return [*self._handle_response(response)["TradePairs"]]
        except Exception as e:
            logging.info(f"Error in list_of_coins: {e}")
            return None

    def get_ticker(self, pair=None):
        try:
            url = f"{self.base_url}/v3/ticker"
            params = {"timestamp": self._get_timestamp()}
            if pair:
                params["pair"] = pair

            for i in range(5):
                headers = self._headers(params, is_signed=False)
                response = requests.get(url, params=params, headers=headers)
                response = self._handle_response(response)
                if response["Success"] or (response["Success"] == False and response["ErrMsg"] == "pair not found"):
                    return response
                else:
                    logging.info(response, "sleep for 1/15 second")
                    time.sleep(1 / 15)
            logging.info(f"Error in get_ticker: {e}")
            return None
        except Exception as e:
            logging.info(f"Error in get_ticker: {e}")
            return None

    def get_balance(self):
        try:
            params = {"timestamp": self._get_timestamp()}
            response = requests.get(f"{self.base_url}/v3/balance", params=params, headers=self._headers(params, is_signed=True))
            data = self._handle_response(response)
            return data if data else {"SpotWallet": {"USD": {"Free": -1}}}
        except Exception as e:
            logging.info(f"Error in get_balance: {e}")
            return None

    def place_order(self, coin, side: Literal["BUY", "SELL"], qty, price=None):
        try:
            params = {
                "timestamp": self._get_timestamp(),
                "pair": coin,
                "side": side,
                "quantity": qty,
                "type": "MARKET" if not price else "LIMIT",
            }
            if price:
                params["price"] = price
            response = requests.post(f"{self.base_url}/v3/place_order", data=params, headers=self._headers(params, is_signed=True))
            return self._handle_response(response)
        except Exception as e:
            logging.info(f"Error in place_order: {e}")
            return None

    def cancel_order(self, pair):
        try:
            params = {"timestamp": self._get_timestamp(), "pair": pair}
            response = requests.post(f"{self.base_url}/v3/cancel_order", data=params, headers=self._headers(params, is_signed=True))
            return self._handle_response(response)
        except Exception as e:
            logging.info(f"Error in cancel_order: {e}")
            return None

    def query_order(self, order_id=None, pair=None, offset=None, limit=None, pending_only=None):
        try:
            params = {"timestamp": self._get_timestamp()}

            if order_id:
                params["order_id"] = str(order_id)
            elif pair:
                params["pair"] = pair
                if offset is not None:
                    params["offset"] = str(offset)
                if limit is not None:
                    params["limit"] = str(limit)
                if pending_only is not None:
                    params["pending_only"] = "TRUE" if pending_only else "FALSE"

            response = requests.post(f"{self.base_url}/v3/query_order", data=params, headers=self._headers(params, is_signed=True))
            return self._handle_response(response)
        except Exception as e:
            logging.info(f"Error in query_order: {e}")
            return None

    def get_account_net_value(self, balance=None):
        if balance is None:
            balance = self.get_balance()
        if balance:
            total_value = balance["SpotWallet"]["USD"]["Free"]
            for coin, coin_balance in balance["SpotWallet"].items():
                if coin != "USD" and coin_balance["Free"] > 0:
                    ticker_data = self.get_ticker(f"{coin}/USD")
                    if ticker_data and "Data" in ticker_data and f"{coin}/USD" in ticker_data["Data"]:
                        coin_price = ticker_data["Data"][f"{coin}/USD"]["LastPrice"]
                        total_value += coin_balance["Free"] * coin_price
            return total_value
        return 0

    def wrapped_buy(self, coin, position_ratio):
        # position_ratio仓位控制

        if self.open_trade >= self.max_trade:
            logging.info("max trades reached")
            return None

        while True:
            balance = self.get_balance()
            if balance:
                break
            time.sleep(1 / 15)
        spots = balance["SpotWallet"]
        account_net_value = self.get_account_net_value(balance)
        usd_per_trade = account_net_value / self.max_trade

        usd_trade = min(usd_per_trade, spots["USD"]["Free"]) * position_ratio * 0.95  # 防止手续费不够
        coin_ticker = self.get_ticker(coin)

        if coin_ticker is None:
            logging.info(f"Error in get_ticker: {coin}, skipping buy")
            return None

        coin_price = coin_ticker["Data"][coin]["LastPrice"]
        coin_qty = round(usd_trade / coin_price, 3)
        if coin_qty <= 0:
            logging.info(f"not enough USD: {usd_trade} for {coin_qty} {coin}")
            return None

        # 解决部分币种的交易数量不能小数点之后位数过多
        for i in [2, 1, 0]:
            result = self.place_order(coin, "BUY", coin_qty)
            if not (result and result["ErrMsg"] == "quantity step size error"):
                break
            coin_qty = round(coin_qty, i)
            time.sleep(1 / 5)

        if result and result["Success"]:
            self.open_trade += 1
            logging.info(
                f"Placed {coin} BUY order for {coin_qty} ({usd_trade} USD) at {coin_price}, with postion control ratio: {position_ratio}"
            )
        else:
            logging.info(f"Buy {coin} failed")
        logging.info(result)

    def wrapped_sell(self, coin):
        while True:
            balance = self.get_balance()
            if balance:
                break
            time.sleep(1 / 15)
        spots = balance["SpotWallet"]
        coin_qty = spots[coin.replace("/USD", "")]["Free"] if coin.replace("/USD", "") in spots else 0
        if coin_qty <= 0:
            logging.info(f"No {coin} balance, skipping sell")
            return
        result = self.place_order(coin, "SELL", coin_qty)
        if result and result["Success"]:
            self.open_trade -= 1
            logging.info(f"Placed {coin} SELL order for {coin_qty}")
        else:
            logging.info(f"Sell {coin} failed")

        logging.info(result)


if __name__ == "__main__":
    client = RoostooAPIClient()
    client.wrapped_sell("BTC/USD")
    client.wrapped_sell("NEAR/USD")
    print(client.get_balance())
