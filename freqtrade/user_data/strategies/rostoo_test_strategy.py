# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from roostoo_trade_client import RoostooAPIClient  # roostoo
import logging  # roostoo
from freqtrade.persistence import Trade
import warnings, datetime

IS_LIVE_TRADING = True  # roostoo

from freqtrade.strategy import IStrategy
import talib.abstract as ta


class RoostooStrategy(IStrategy):
    """
    Simple MACD strategy for testing
    """

    INTERFACE_VERSION = 3
    can_short: bool = False
    minimal_roi = {"0": 0.05}
    stoploss = -0.1
    timeframe = "1m"
    process_only_new_candles = True
    use_exit_signal = True
    startup_candle_count: int = 30
    max_open_trades = 3

    lookback_period_candles = 50

    if IS_LIVE_TRADING:
        api_client = RoostooAPIClient(max_trade=3)  # roostoo

    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # MACD
        macd = ta.MACD(dataframe)
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # MACD crosses above signal line
                (dataframe["macd"] > dataframe["macdsignal"]*0.8)
                & (dataframe["macdhist"] > 0)
                & (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # MACD crosses below signal line
                (dataframe["macd"] < dataframe["macdsignal"]*1.2)
                & (dataframe["macdhist"] < 0)
                & (dataframe["volume"] > 0)
            ),
            "exit_long",
        ] = 1

        return dataframe

    # roostoo
    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                            time_in_force: str, current_time: datetime, entry_tag: str | None,
                            side: str, **kwargs) -> bool:
        # roostoo
        if IS_LIVE_TRADING:
            self.api_client.wrapped_buy(pair.replace("/USDT", "/USD"), 0.1)
            logging.info(f"balance: {self.api_client.get_balance()}")
        return True

    # roostoo
    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: datetime, **kwargs) -> bool:
        if IS_LIVE_TRADING:
            self.api_client.wrapped_sell(pair.replace("/USDT", "/USD"))
            logging.info(f"balance: {self.api_client.get_balance()}")
        return True
