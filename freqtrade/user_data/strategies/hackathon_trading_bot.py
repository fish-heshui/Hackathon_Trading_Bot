from freqtrade.strategy.interface import IStrategy
from functools import reduce
from pandas import DataFrame, Series

# --------------------------------
import talib.abstract as ta
import pandas_ta as pta
import pandas as pd
import datetime
import freqtrade.vendor.qtpylib.indicators as qtpylib
from datetime import datetime
from freqtrade.persistence import Trade
from freqtrade.strategy import DecimalParameter, IntParameter
from roostoo_trade_client import RoostooAPIClient
import logging

ENABLE_DYNAMIC_POSITION = False
GLOBAL_DATA_CSV_PATH = "/home/fish/shared/Hackathon_Trading_Bot/freqtrade/user_data/strategies/global_m2_data.csv"
LIVE_TRADING = False
pd.options.mode.chained_assignment = None

# Strategy hyperparameters
entry_hyperparams = {
    "ema_period_entry": 12,
}

exit_hyperparams = {
    "ema_period_exit": 22,
    "exit_multiplier_1": 1.008,
    "exit_multiplier_2": 1.016,
}


def calculate_williams_percent_r(df: DataFrame, lookback_period: int = 14) -> Series:
    """
    Williams %R oscillator calculation
    Returns values between -100 (oversold) and 0 (overbought)
    """
    high_max = df["high"].rolling(center=False, window=lookback_period).max()
    low_min = df["low"].rolling(center=False, window=lookback_period).min()

    williams_r_values = Series(
        (high_max - df["close"]) / (high_max - low_min),
        name=f"Williams_R_{lookback_period}",
    )

    return williams_r_values * -100


class Hackathon_Trading_Bot(IStrategy):
    dynamic_position_multiplier = 1
    position_data_table = None
    max_open_trades = 2
    if LIVE_TRADING:
        trading_api = RoostooAPIClient(max_trade=max_open_trades)

    INTERFACE_VERSION = 2

    @property
    def protections(self):
        return [
            {
                "method": "LowProfitPairs",
                "lookback_period_candles": 60,
                "trade_limit": 1,
                "stop_duration_candles": 60,
                "required_profit": -0.05,
            },
            {"method": "CooldownPeriod", "stop_duration_candles": 5},
        ]

    minimal_roi = {"0": 1}
    stoploss = -0.25

    # Entry parameters
    ema_candles_entry = IntParameter(5, 80, default=entry_hyperparams["ema_period_entry"], space="buy", optimize=True)

    # Exit parameters
    ema_candles_exit = IntParameter(5, 80, default=exit_hyperparams["ema_period_exit"], space="sell", optimize=True)
    exit_threshold_1 = DecimalParameter(0.95, 1.1, default=exit_hyperparams["exit_multiplier_1"], space="sell", optimize=True)
    exit_threshold_2 = DecimalParameter(0.99, 1.5, default=exit_hyperparams["exit_multiplier_2"], space="sell", optimize=True)

    trailing_stop = False
    trailing_stop_positive = 0.002
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    use_custom_stoploss = True

    order_types = {
        "entry": "limit",
        "exit": "limit",
        "emergency_exit": "market",
        "force_entry": "market",
        "force_exit": "market",
        "stoploss": "market",
        "stoploss_on_exchange": False,
        "stoploss_on_exchange_interval": 60,
        "stoploss_on_exchange_market_ratio": 0.99,
    }

    order_time_in_force = {"entry": "gtc", "exit": "gtc"}
    timeframe = "5m"
    process_only_new_candles = True
    startup_candle_count = 400

    def custom_stoploss(
        self, pair: str, trade: Trade, current_time: datetime, current_rate: float, current_profit: float, **kwargs
    ) -> float:
        if current_profit >= 0.05:
            return -0.002
        return None

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Price change percentage
        dataframe["price_change_pct"] = 100 / dataframe["open"] * dataframe["close"] - 100

        # Entry EMA calculation
        for period in self.ema_candles_entry.range:
            dataframe["ema_entry"] = ta.EMA(dataframe, timeperiod=period)

        # Exit EMA calculation
        for period in self.ema_candles_exit.range:
            dataframe["ema_exit"] = ta.EMA(dataframe, timeperiod=period)

        # Hull Moving Average
        dataframe["hull_ma_50"] = qtpylib.hull_moving_average(dataframe["close"], window=50)

        # MAMA/FAMA and KAMA indicators
        dataframe["hl2_price"] = (dataframe["high"] + dataframe["low"]) / 2
        dataframe["mama_line"], dataframe["fama_line"] = ta.MAMA(dataframe["hl2_price"], 0.25, 0.025)
        dataframe["mama_fama_diff"] = (dataframe["mama_line"] - dataframe["fama_line"]) / dataframe["hl2_price"]
        dataframe["kama_adaptive"] = ta.KAMA(dataframe["close"], 84)

        # Correlation Trend Indicator
        dataframe["cti_oscillator"] = pta.cti(dataframe["close"], length=20)

        # RSI variations
        dataframe["rsi_standard"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["rsi_fast"] = ta.RSI(dataframe, timeperiod=4)
        dataframe["rsi_slow"] = ta.RSI(dataframe, timeperiod=20)
        dataframe["rsi_long_84"] = ta.RSI(dataframe, timeperiod=84)
        dataframe["rsi_long_112"] = ta.RSI(dataframe, timeperiod=112)

        # Williams %R
        dataframe["williams_r_14"] = calculate_williams_percent_r(dataframe, 14)

        # Load position control data
        if ENABLE_DYNAMIC_POSITION:
            self.position_data_table = pd.read_csv(GLOBAL_DATA_CSV_PATH)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[:, "enter_tag"] = ""

        entry_condition = (
            (dataframe["kama_adaptive"] > dataframe["fama_line"])
            & (dataframe["fama_line"] > dataframe["mama_line"] * 0.981)
            & (dataframe["williams_r_14"] < -61.3)
            & (dataframe["mama_fama_diff"] < -0.025)
            & (dataframe["cti_oscillator"] < -0.715)
            & (dataframe["close"].rolling(48).max() >= dataframe["close"] * 1.05)
            & (dataframe["close"].rolling(288).max() >= dataframe["close"] * 1.125)
            & (dataframe["rsi_long_84"] < 60)
            & (dataframe["rsi_long_112"] < 60)
        )

        dataframe.loc[entry_condition, "enter_tag"] += "entry_signal"
        dataframe.loc[entry_condition, "enter_long"] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        exit_conditions = []
        dataframe.loc[:, "exit_tag"] = ""

        exit_signal = (
            (dataframe["close"] > dataframe["hull_ma_50"])
            & (dataframe["close"] > (dataframe["ema_exit"] * self.exit_threshold_2.value))
            & (dataframe["rsi_standard"] > 50)
            & (dataframe["volume"] > 0)
            & (dataframe["rsi_fast"] > dataframe["rsi_slow"])
        ) | (
            (dataframe["close"] < dataframe["hull_ma_50"])
            & (dataframe["close"] > (dataframe["ema_exit"] * self.exit_threshold_1.value))
            & (dataframe["volume"] > 0)
            & (dataframe["rsi_fast"] > dataframe["rsi_slow"])
        )

        exit_conditions.append(exit_signal)
        dataframe.loc[exit_signal, "exit_tag"] += "exit_signal"

        if exit_conditions:
            dataframe.loc[reduce(lambda x, y: x | y, exit_conditions), "exit_long"] = 1

        return dataframe

    def custom_stake_amount(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_stake: float,
        min_stake: float | None,
        max_stake: float,
        leverage: float,
        entry_tag: str | None,
        side: str,
        **kwargs,
    ) -> float:
        if ENABLE_DYNAMIC_POSITION:
            if self.position_data_table is None:
                print("Position data table not available")
                return proposed_stake

            date_str = current_time.strftime("%Y-%m-%d")
            if date_str in self.position_data_table["Date"].to_list():
                multiplier = self.position_data_table[self.position_data_table["Date"] == date_str]["PositionRatio"].values[0]
            else:
                multiplier = 1.0
            return proposed_stake * multiplier
        else:
            return proposed_stake

    def confirm_trade_entry(
        self,
        pair: str,
        order_type: str,
        amount: float,
        rate: float,
        time_in_force: str,
        current_time: datetime,
        entry_tag: str | None,
        side: str,
        **kwargs,
    ) -> bool:
        if LIVE_TRADING:
            position_multiplier = 1.0
            if ENABLE_DYNAMIC_POSITION:
                if self.position_data_table is None:
                    print("Position data table not available")
                else:
                    date_str = current_time.strftime("%Y-%m-%d")
                    if date_str in self.position_data_table["Date"].to_list():
                        position_multiplier = self.position_data_table[self.position_data_table["Date"] == date_str][
                            "PositionRatio"
                        ].values[0]

            self.trading_api.wrapped_buy(pair.replace("/USDT", "/USD"), position_multiplier)
            logging.info(f"Account Balance: {self.trading_api.get_balance()}")
        return True

    def confirm_trade_exit(
        self,
        pair: str,
        trade: Trade,
        order_type: str,
        amount: float,
        rate: float,
        time_in_force: str,
        exit_reason: str,
        current_time: datetime,
        **kwargs,
    ) -> bool:
        if LIVE_TRADING:
            self.trading_api.wrapped_sell(pair.replace("/USDT", "/USD"))
            logging.info(f"Account Balance: {self.trading_api.get_balance()}")
        return True
