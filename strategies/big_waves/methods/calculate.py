import pandas as pd
import numpy as np


def calculate_method(data: pd.DataFrame, indicators: list[dict]) -> pd.DataFrame:
    # Initialize columns
    _initialize_columns(data)

    # Vectorized time calculations
    data["DATE"] = pd.to_datetime(data["DATE"])
    times = data["DATE"].dt.time
    open_time = pd.Timestamp("07:00:00").time()
    close_time = pd.Timestamp("23:00:00").time()
    stop_time = pd.Timestamp("23:40:00").time()

    pc_period = indicators[0]["period"]
    st_period = indicators[1]["period"]
    st_multiplier = indicators[1]["multiplier"]

    # Generation of names of columns
    pc_low_col = f"PC_{pc_period}_LOW"
    pc_high_col = f"PC_{pc_period}_HIGH"
    st_lower_col = f"ST_LOWER_{st_period}_{st_multiplier}"

    prev_pc_low_col = f"prev_{pc_low_col}"
    prev_pc_high_col = f"prev_{pc_high_col}"
    prev_st_lower_col = f"prev_{st_lower_col}"

    data[prev_pc_low_col] = data[pc_low_col].shift(1)
    data[prev_pc_high_col] = data[pc_high_col].shift(1)
    data[prev_st_lower_col] = data[st_lower_col].shift(1)

    data["open_condition"] = (
        data[pc_low_col].notna()
        & data[st_lower_col].notna()
        & (data[pc_low_col] > data[st_lower_col])
        & (data["LOW"] < data[prev_pc_low_col])
    )
    data["improve_condition"] = data[pc_low_col].notna() & data[st_lower_col].notna()
    data["close_condition"] = (
        data[pc_high_col].notna()
        & data[st_lower_col].notna()
        & (data["HIGH"] > data[prev_pc_high_col])
    )
    data["stop_loss_condition"] = (
        data[prev_st_lower_col].notna() & data[st_lower_col].isna()
    )

    # Create and sort events
    events = _create_events(
        data,
        times,
        open_time,
        close_time,
        stop_time,
        prev_pc_low_col,
        prev_pc_high_col,
        prev_st_lower_col,
    )
    events.sort(key=lambda x: x["index"])

    # Process events
    position = 0
    position_prices = []
    position_average_price = 0
    best_price = 0
    last_event_index = None
    current_balance = 0  # Initialize cumulative balance
    trade_start_balance = 0  # Balance at trade opening
    in_trade = False  # Trade flag

    for event in events:
        idx = event["index"]
        if idx == last_event_index and event["type"] == "IMPROVE":
            continue

        # Initialize variables for balance changes and commissions
        delta_balance = 0
        commission_event = 0
        trade_profit = 0

        # Handle position opening
        if event["type"] == "BUY" and position == 0:
            (position, best_price, last_event_index, delta_balance, commission) = (
                _open_position(data, idx, event["price"], position_prices)
            )
            commission_event = commission
            in_trade = True

        # Handle position improvement
        elif event["type"] == "IMPROVE" and position > 0:
            (
                position,
                position_prices,
                best_price,
                last_event_index,
                delta_balance,
                commission,
            ) = _try_improve_position(data, idx, position, position_prices, best_price)
            commission_event = commission

        # Handle stop loss
        elif event["type"] == "STOP_LOSS" and position > 0:
            (
                position,
                position_prices,
                position_average_price,
                last_event_index,
                delta_balance,
                commission,
            ) = _close_position(data, idx, event["price"], position, "STOP_LOSS")
            commission_event = commission
            if position == 0 and in_trade:
                balance = round(current_balance + delta_balance, 2)
                trade_profit = balance - trade_start_balance
                trade_start_balance = balance
                in_trade = False

        # Handle position closing
        elif event["type"] in ["SELL", "CLOSE_TIME", "CLOSE_END"] and position > 0:
            (
                position,
                position_prices,
                position_average_price,
                last_event_index,
                delta_balance,
                commission,
            ) = _close_position(data, idx, event["price"], position, "LONG_SELL")
            commission_event = commission
            if position == 0 and in_trade:
                balance = round(current_balance + delta_balance, 2)
                trade_profit = balance - trade_start_balance
                trade_start_balance = balance
                in_trade = False

        # Update cumulative balance
        current_balance += delta_balance
        data.loc[idx, "BALANCE"] = round(current_balance, 2)
        data.loc[idx, "POSITION"] = position

        # Record trade profit
        if trade_profit != 0:
            data.loc[idx, "TRADE_PROFIT"] = round(trade_profit, 2)

        # Update commission
        if pd.isna(data.loc[idx, "COMMISSION"]):
            data.loc[idx, "COMMISSION"] = commission_event
        else:
            data.loc[idx, "COMMISSION"] += commission_event

    # Remove temporary columns
    columns_to_drop = [
        prev_pc_low_col,
        prev_pc_high_col,
        prev_st_lower_col,
        "open_condition",
        "improve_condition",
        "close_condition",
        "stop_loss_condition",
    ]
    data.drop(columns=columns_to_drop, inplace=True, errors="ignore")

    return data


def _initialize_columns(data):
    """Initialize result columns with NaN values"""
    cols_to_init = [
        "BUY_PRICE",
        "SELL_PRICE",
        "SL_PRICE",
        "CT_PRICE",
        "CE_PRICE",
        "COMMISSION",
        "BALANCE",
        "POSITION",  # New column for position
        "TRADE_PROFIT",  # New column for trade profit
    ]
    for col in cols_to_init:
        data[col] = np.nan


def _create_events(
    data,
    times,
    open_time,
    close_time,
    stop_time,
    prev_pc_low_col,
    prev_pc_high_col,
    prev_st_lower_col,
):
    """Create all event types for processing"""
    events = []
    last_idx = data.index[-1]

    # Function to add events based on mask
    def add_events(mask, event_type, price_func=None):
        for idx in data.index[mask]:
            event = {"index": idx, "type": event_type}
            if price_func:
                event["price"] = price_func(idx)
            events.append(event)

    # Add BUY events
    buy_mask = (times > open_time) & (times < close_time) & data["open_condition"]
    add_events(buy_mask, "BUY", lambda idx: data.loc[idx, prev_pc_low_col])

    # Add IMPROVE events
    add_events(data["improve_condition"], "IMPROVE")

    # Add SELL events
    sell_mask = (times > open_time) & (times < stop_time) & data["close_condition"]
    add_events(sell_mask, "SELL", lambda idx: data.loc[idx, prev_pc_high_col])

    # Add STOP_LOSS events
    stop_loss_mask = data["stop_loss_condition"]
    add_events(
        stop_loss_mask, "STOP_LOSS", lambda idx: data.loc[idx, prev_st_lower_col]
    )

    # Add time-based closing events
    close_time_mask = times == stop_time
    add_events(close_time_mask, "CLOSE_TIME", lambda idx: data.loc[idx, "CLOSE"])

    # Add end-of-data closing event
    events.append(
        {
            "index": last_idx,
            "type": "CLOSE_END",
            "price": data.loc[last_idx, "CLOSE"],
        }
    )

    return events


def _open_position(data, idx, price, position_prices):
    """Open a new position and return balance change and commission"""
    commission = round(price * 0.0005, 2)
    data.loc[idx, "BUY_PRICE"] = price

    position_prices.append(price + commission)
    best_price = data.loc[idx, "LOW"]
    delta_balance = -price - commission
    return 1, best_price, idx, delta_balance, commission


def _close_position(data, idx, price, position, close_type):
    """Close a position and return balance change and commission"""
    commission = round(price * 0.0005 * position, 2)
    if close_type == "STOP_LOSS":
        data.loc[idx, "SL_PRICE"] = price
    elif close_type == "CLOSE_TIME":
        data.loc[idx, "CT_PRICE"] = price
    elif close_type == "CLOSE_END":
        data.loc[idx, "CE_PRICE"] = price
    else:  # LONG_SELL
        data.loc[idx, "SELL_PRICE"] = price

    delta_balance = price * position - commission
    return 0, [], 0, idx, delta_balance, commission


def _try_improve_position(data, idx, position, position_prices, best_price):
    """Attempt to improve position and return total balance changes and commissions"""
    total_delta = 0
    total_commission = 0
    last_event_index = idx

    if position > 1:
        for prev_price in position_prices[:-1]:
            price_with_comm = round(prev_price + prev_price * 0.001, 2)
            if data.loc[idx, "LOW"] <= price_with_comm <= data.loc[idx, "HIGH"]:
                data.loc[idx, "SELL_PRICE"] = price_with_comm
                commission_sell = round(price_with_comm * 0.0005, 2)
                total_delta += price_with_comm - commission_sell
                total_commission += commission_sell
                position -= 1
                position_prices.remove(prev_price)
                break

    if data.loc[idx, "LOW"] <= best_price <= data.loc[idx, "HIGH"]:
        data.loc[idx, "BUY_PRICE"] = best_price
        commission_buy = round(best_price * 0.0005, 2)
        total_delta += -best_price - commission_buy
        total_commission += commission_buy
        position_prices.append(best_price)
        position += 1
        best_price = data.loc[idx, "LOW"]
        last_event_index = idx

    return (
        position,
        position_prices,
        best_price,
        last_event_index,
        total_delta,
        total_commission,
    )
