import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
import numpy as np


def report_method(data: pd.DataFrame) -> None:
    """Generate a trading strategy performance report with visualizations"""
    data = data.copy()
    if "DATE" not in data.columns:
        data = data.reset_index()

    data["DATE"] = pd.to_datetime(data["DATE"])

    # Fill balance and position values
    data["BALANCE"] = data["BALANCE"].ffill().fillna(0)
    data["POSITION"] = data["POSITION"].ffill().fillna(0)

    # Determine profit column name (TRADE_PROFIT or PROFIT)
    if "TRADE_PROFIT" in data.columns:
        profit_col = "TRADE_PROFIT"
    elif "PROFIT" in data.columns:
        profit_col = "PROFIT"
    else:
        data["PROFIT"] = 0.0
        profit_col = "PROFIT"

    # Calculate strategy cumulative profit
    data["CUMULATIVE_PROFIT"] = data[profit_col].fillna(0).cumsum()

    # Create a temporary column for signal type
    data["SIGNAL_TYPE"] = None
    signal_mapping = [
        ("BUY_PRICE", "BUY"),
        ("SELL_PRICE", "SELL"),
        ("SL_PRICE", "STOP_LOSS"),
        ("CT_PRICE", "CLOSE_TIME"),
        ("CE_PRICE", "CLOSE_END"),
    ]
    for col, signal_name in signal_mapping:
        if col in data.columns:
            data.loc[data[col].notna(), "SIGNAL_TYPE"] = signal_name

    # Filter only rows with trades
    trades = data.dropna(subset=["SIGNAL_TYPE"]).copy()

    # Calculate buy-and-hold strategy return
    first_open = data["OPEN"].iloc[0]
    last_close = data["CLOSE"].iloc[-1]
    buy_hold_profit = last_close - first_open

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 7))

    # Trading strategy profit plot
    ax.step(
        data["DATE"],
        data["CUMULATIVE_PROFIT"],
        "b-",
        where="post",
        linewidth=2,
        label="Trading strategy",
    )

    # Fill for positive and negative values
    ax.fill_between(
        data["DATE"],
        data["CUMULATIVE_PROFIT"],
        0,
        where=(data["CUMULATIVE_PROFIT"] >= 0),
        facecolor="green",
        alpha=0.3,
        step="post",
    )
    ax.fill_between(
        data["DATE"],
        data["CUMULATIVE_PROFIT"],
        0,
        where=(data["CUMULATIVE_PROFIT"] <= 0),
        facecolor="red",
        alpha=0.3,
        step="post",
    )

    # Zero level line
    ax.axhline(0, color="black", linestyle="-", linewidth=1)

    # Buy-and-hold plot
    ax.plot(
        [data["DATE"].iloc[0], data["DATE"].iloc[-1]],
        [0, buy_hold_profit],
        "r--",
        linewidth=2,
        label="Buy & Hold (1 share)",
    )

    # Date format settings
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)

    # Axis and legend settings
    ax.set_xlabel("Date")
    ax.set_ylabel("Profit/Loss")
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    ax.legend()
    ax.grid(True)
    ax.set_title("Strategy Performance Comparison")

    plt.tight_layout()
    plt.show()

    # Signal statistics
    signal_counts = trades["SIGNAL_TYPE"].value_counts()

    # Calculate trade statistics
    trade_results = data.dropna(subset=[profit_col]).copy()
    profitable = (trade_results[profit_col] > 0).sum()
    unprofitable = (trade_results[profit_col] <= 0).sum()
    total_trades = profitable + unprofitable
    win_rate = (profitable / total_trades * 100) if total_trades > 0 else 0

    # Final balance (using cumulative profit)
    total_balance = data["CUMULATIVE_PROFIT"].iloc[-1]

    # Print statistics
    print("\nTrade Statistics:")
    print("=" * 40)
    print(f"Signal counts:")
    for signal, count in signal_counts.items():
        print(f"- {signal}: {count}")

    print("\nTrade Results:")
    print(f"- Profitable trades: {profitable}")
    print(f"- Unprofitable trades: {unprofitable}")
    print(f"- Win Rate: {win_rate:.2f}%")
    print(f"- Final balance: {total_balance:.2f}")
    print("=" * 40)

