import numpy as np
import pandas as pd


def calculate_method(data: pd.DataFrame, indicators: list[dict]) -> pd.DataFrame:
    """
    Calculate method for PriceChanel strategy.

    Strategy rules:
    - Period: indicators[0]["period"] (e.g. 40)
    - Entry condition: PC_HIGH was unchanged for at least 5 consecutive candles prior to current candle,
      and current candle HIGH > prev_PC_HIGH (breakout of upper channel).
    - Entry price: prev_PC_HIGH
    - Stop-Loss: PC_MID of entry candle
    - Take-Profit: Entry + 2 * (Entry - SL)
    - Maximum 1 open position at a time.
    """
    result_df = data.copy()

    period = indicators[0]["period"]
    pc_high_col = f"PC_{period}_HIGH"
    pc_mid_col = f"PC_{period}_MID"

    # Initialize strategy tracking columns
    result_df["BUY_PRICE"] = np.nan
    result_df["SELL_PRICE"] = np.nan  # TP exit
    result_df["SL_PRICE"] = np.nan    # SL exit
    result_df["CT_PRICE"] = np.nan    # Close time exit
    result_df["CE_PRICE"] = np.nan    # Close end exit

    result_df["TP_LEVEL"] = np.nan
    result_df["SL_LEVEL"] = np.nan

    result_df["POSITION"] = 0
    result_df["BALANCE"] = 0.0
    result_df["TRADE_PROFIT"] = np.nan

    pc_high_values = result_df[pc_high_col].values
    pc_mid_values = result_df[pc_mid_col].values
    high_values = result_df["HIGH"].values
    low_values = result_df["LOW"].values
    close_values = result_df["CLOSE"].values

    n_rows = len(result_df)

    position = 0
    entry_price = 0.0
    sl_price = 0.0
    tp_price = 0.0
    current_balance = 0.0

    buy_price_arr = [np.nan] * n_rows
    sell_price_arr = [np.nan] * n_rows
    sl_price_arr = [np.nan] * n_rows
    ce_price_arr = [np.nan] * n_rows
    tp_level_arr = [np.nan] * n_rows
    sl_level_arr = [np.nan] * n_rows
    position_arr = [0] * n_rows
    balance_arr = [0.0] * n_rows
    trade_profit_arr = [np.nan] * n_rows

    FLAT_CANDLES = 5

    last_exit_idx = -100

    for i in range(n_rows):
        # If we are currently in position
        if position == 1:
            tp_level_arr[i] = tp_price
            sl_level_arr[i] = sl_price
            position_arr[i] = 1
            balance_arr[i] = current_balance

            # Check exit conditions for candle i with static SL
            hit_sl = low_values[i] <= sl_price
            hit_tp = high_values[i] >= tp_price

            if hit_sl and hit_tp:
                # Both hit, SL priority
                exit_price = sl_price
                sl_price_arr[i] = exit_price
                profit = round(exit_price - entry_price, 2)
                current_balance = round(current_balance + profit, 2)
                trade_profit_arr[i] = profit
                balance_arr[i] = current_balance
                position = 0
                last_exit_idx = i
            elif hit_sl:
                exit_price = sl_price
                sl_price_arr[i] = exit_price
                profit = round(exit_price - entry_price, 2)
                current_balance = round(current_balance + profit, 2)
                trade_profit_arr[i] = profit
                balance_arr[i] = current_balance
                position = 0
                last_exit_idx = i
            elif hit_tp:
                exit_price = tp_price
                sell_price_arr[i] = exit_price
                profit = round(exit_price - entry_price, 2)
                current_balance = round(current_balance + profit, 2)
                trade_profit_arr[i] = profit
                balance_arr[i] = current_balance
                position = 0
                last_exit_idx = i

        # If we have no open position, check entry condition
        if position == 0:
            balance_arr[i] = current_balance
            # Must be at least FLAT_CANDLES after dataset start and after last position exit
            if i >= FLAT_CANDLES and (i - FLAT_CANDLES) >= last_exit_idx:
                prev_pc_high = pc_high_values[i - 1]
                # Check if PC_HIGH was constant for previous FLAT_CANDLES candles (i-FLAT_CANDLES to i-1)
                flat_slice = pc_high_values[i - FLAT_CANDLES : i]

                if not np.isnan(prev_pc_high) and not np.isnan(flat_slice).any():
                    is_flat = np.all(flat_slice == prev_pc_high)
                    # Check breakout on candle i
                    if is_flat and high_values[i] > prev_pc_high:
                        # Entry triggered!
                        position = 1
                        entry_price = prev_pc_high
                        sl_price = round(float(pc_mid_values[i]), 2)
                        sl_dist = entry_price - sl_price
                        tp_price = round(entry_price + 2.0 * sl_dist, 2)

                        buy_price_arr[i] = entry_price
                        tp_level_arr[i] = tp_price
                        sl_level_arr[i] = sl_price
                        position_arr[i] = 1

                        # Immediately check if candle i hits TP/SL after entry
                        hit_sl = low_values[i] <= sl_price
                        hit_tp = high_values[i] >= tp_price

                        if hit_sl and hit_tp:
                            exit_price = sl_price
                            sl_price_arr[i] = exit_price
                            profit = round(exit_price - entry_price, 2)
                            current_balance = round(current_balance + profit, 2)
                            trade_profit_arr[i] = profit
                            balance_arr[i] = current_balance
                            position = 0
                            last_exit_idx = i
                        elif hit_sl:
                            exit_price = sl_price
                            sl_price_arr[i] = exit_price
                            profit = round(exit_price - entry_price, 2)
                            current_balance = round(current_balance + profit, 2)
                            trade_profit_arr[i] = profit
                            balance_arr[i] = current_balance
                            position = 0
                            last_exit_idx = i
                        elif hit_tp:
                            exit_price = tp_price
                            sell_price_arr[i] = exit_price
                            profit = round(exit_price - entry_price, 2)
                            current_balance = round(current_balance + profit, 2)
                            trade_profit_arr[i] = profit
                            balance_arr[i] = current_balance
                            position = 0
                            last_exit_idx = i

    # If position is still open at the end of dataset, close at last candle CLOSE
    if position == 1:
        last_idx = n_rows - 1
        exit_price = round(float(close_values[last_idx]), 2)
        ce_price_arr[last_idx] = exit_price
        profit = round(exit_price - entry_price, 2)
        current_balance = round(current_balance + profit, 2)
        trade_profit_arr[last_idx] = profit
        balance_arr[last_idx] = current_balance
        position_arr[last_idx] = 0

    result_df["BUY_PRICE"] = buy_price_arr
    result_df["SELL_PRICE"] = sell_price_arr
    result_df["SL_PRICE"] = sl_price_arr
    result_df["CE_PRICE"] = ce_price_arr
    result_df["TP_LEVEL"] = tp_level_arr
    result_df["SL_LEVEL"] = sl_level_arr
    result_df["POSITION"] = position_arr
    result_df["BALANCE"] = balance_arr
    result_df["TRADE_PROFIT"] = trade_profit_arr

    return result_df

