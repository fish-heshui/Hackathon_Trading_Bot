# Roostoo Hackathon

## Introduction

We built our strategy based on the freqtrade trading framework and injected the Roostoo mock trading api into the framework. Thus, most code are for the freqtrade framework and the most import files are:

1. Strategy:  https://github.com/fish-heshui/Hackathon_Trading_Bot/blob/main/freqtrade/user_data/strategies/hackathon_trading_bot_v1.py
2. Wrapper for trading on roostoo: https://github.com/fish-heshui/Hackathon_Trading_Bot/blob/main/freqtrade/user_data/strategies/roostoo_trade_client.py
3. Some configuration of the strategy: https://github.com/fish-heshui/Hackathon_Trading_Bot/blob/main/freqtrade/user_data/config.json

## The core idea:

This strategy identifies pullbacks within broader uptrends based on multiple indicators—entering during oversold rebounds and exiting during strong market rallies. We employ trailing stop losses as profit-taking tools and standard stop losses for risk management. Below, I outline the strategy's core components through five key points: entry condition, exit condition, trailing_stop_loss, stop_loss and risk management.

### Entry condition:

```jsx
(dataframe["kama_adaptive"] > dataframe["fama_line"])
```

1.Filtering out noise and ensure the long-term trend is upward.

```jsx
dataframe["fama_line"] > dataframe["mama_line"] * 0.98
```

2.Used to filter strength, determining whether the trend is a strong uptrend rather than a weak trend or sideways movement. “0.98” can be changed to avoid misjudging trends due to short-term fluctuations

```jsx
& (dataframe["williams_r_14"] < -6.)
& (dataframe["mama_fama_diff"] < -0.025)
& (dataframe["cti_oscillator"] < -0.715)

```

3.Multiple indicators indicate that the market is currently in an oversold zone.

```jsx
& (dataframe["close"].rolling(48).max() >= dataframe["close"] * 1.05)
& (dataframe["close"].rolling(288).max() >= dataframe["close"] * 1.125)
& (dataframe["rsi_long_84"] < 60)
& (dataframe["rsi_long_112"] < 60)
```

4.Ensure that prices are falling from high levels, with room for a pullback and prevent being in a long-term overbought position

### Exit condition:

There are two types of exits: strong and weak. A strong exit occurs during a sudden surge, exiting between upward cycles. A weak exit happens when the overall market is declining or fluctuating, employing a conservative, gradual exit strategy.

```jsx
exit_signal = (
            (dataframe["close"] > dataframe["hull_ma_50"])
            & (dataframe["close"] > (dataframe["ema_exit"] * self.exit_threshold_2))
            & (dataframe["rsi_standard"] > 50)
            & (dataframe["volume"] > 0)
            & (dataframe["rsi_fast"] > dataframe["rsi_slow"])
        ) | (
            (dataframe["close"] < dataframe["hull_ma_50"])
            & (dataframe["close"] > (dataframe["ema_exit"] * self.exit_threshold_1))
            & (dataframe["volume"] > 0)
            & (dataframe["rsi_fast"] > dataframe["rsi_slow"])
        )
```

In actual backtesting, the firts exit pattern dominates the majority of cases.This is a trend-following exit system for strong uptrend markets.we used Hull Moving Average with 50-period and 22-period exponential moving averages and RSI to determine exit timing.

### Trailing_stop_loss(Primary profit-taking methods):

### Stop_loss:

We set the stop loss at 0.2. Setting it too low may trigger frequent stop losses, causing losses and leaving no room for price rebounds. Setting it too high risks triggering a single loss that results in significant loss in money.

### risk management:

1. Protection system:

```jsx
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
```

If the profit for a trading pair over the last 60 five-minute candlesticks is ≤ -5%, trading will be suspended for 60 candlesticks.
After any trade, we cool off for 5 five-minute candlesticks to prevent overtrading, giving the market time to digest.

1. Position management:

We have set our asset limit to 2, meaning each purchase requires half the capital. This results in larger profits and losses, so we aim to utilize on-chain data—such as Global Liquidity (M2)—to identify correlations with daily BTC price movements. This allows us to dynamically adjust positions: reducing exposure if indicators suggest prices will decline, and maintaining positions if they signal upward movement.

# How we implemented it

### 1. Global Liquidity (M2) on-chain data  scheduled for daily updates.

In the AWS linux environment, We utilize cron to manage and schedule data processing. Every day at UTC+2, a Python script is invoked to retrieve and process data, subsequently outputting usable signals.

```jsx
#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$HOME/scripts/m2-data-cleaning"  
LOG_DIR="$SCRIPT_DIR/../logs"
SCRIPT_NAME="m2_data_cleaning.py"
PYTHON_PATH="$HOME/miniconda3/envs/freqtrade/bin/python3"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/m2_cleaning_${TIMESTAMP}.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_dependencies() {
    if ! command -v $PYTHON_PATH &> /dev/null; then
        log "ERROR: Python3 not found at $PYTHON_PATH"
        exit 1
    fi

    if [ ! -f "$PROJECT_DIR/$SCRIPT_NAME" ]; then
        log "ERROR: Script $SCRIPT_NAME not found in $PROJECT_DIR"
        log "Expected path: $PROJECT_DIR/$SCRIPT_NAME"
        exit 1
    fi
}

main() {
    log "=== Starting M2 Data Cleaning ==="

    check_dependencies

    cd "$SCRIPT_DIR"

    log "Running: $PYTHON_PATH $SCRIPT_NAME"
    $PYTHON_PATH "$SCRIPT_NAME" >> "$LOG_FILE" 2>&1

    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        log "=== M2 Data Cleaning Completed Successfully ==="
    else
        log "=== M2 Data Cleaning Failed with exit code: $EXIT_CODE ==="
    fi

    exit $EXIT_CODE
}
main "$@"
```

```jsx
0 2 * * * /home/ssm-user/scripts/m2-data-cleaning/run_cleaning.sh
```
