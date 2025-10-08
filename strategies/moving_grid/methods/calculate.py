import pandas as pd
import numpy as np


def _initialize_columns(data):
    """Initialize result columns with NaN values"""
    cols_to_init = [
        "BUY_PRICE",
        "SELL_PRICE",
        "COMMISSION",
        "BALANCE",
        "POSITION",
        "PROFIT",
    ]
    for col in cols_to_init:
        data[col] = np.nan


def calculate_method(data: pd.DataFrame, indicators: list[dict]) -> pd.DataFrame:
    _initialize_columns(data)

    global position

    grid_value = indicators[0]["value"]
    max_level = len(indicators[0]["steps"]) - 1

    gc_high = f"GC_{grid_value}_HIGH"
    gc_low = f"GC_{grid_value}_LOW"
    gc_mid = f"GC_{grid_value}_MID"

    level_open = 0
    level_open_high = f"GC_{grid_value}_LEVEL_HIGH_{level_open}"
    level_open_low = f"GC_{grid_value}_LEVEL_LOW_{level_open}"

    level_close = 0
    level_close_high = f"GC_{grid_value}_LEVEL_HIGH_{level_close}"
    level_close_low = f"GC_{grid_value}_LEVEL_LOW_{level_close}"

    position = {"direction": None, "size": None, "avarage_price": None}

    def calc_avarage_price(position, price):
        size = position["size"] if position["size"] > 0 else position["size"] * -1
        return round((position["avarage_price"] * size + price) / (size + 1), 2)

    def calc_sell_price():
        return (
            row[gc_mid]
            if position["size"] == -1 or position["size"] == 1
            else (
                row[level_close_high]
                if position["direction"] == "short"
                else row[level_close_low]
            )
        )

    def open_short(
        position: dict, level_open_high: str, level_open: int, level_close: int
    ):
        avarage_price = (
            row[level_open_high]
            if position["size"] is None
            else calc_avarage_price(position, row[level_open_high])
        )
        position = {
            "direction": "short",
            "size": -1 if position["size"] is None else position["size"] - 1,
            "avarage_price": avarage_price,
        }
        data.loc[index, "SELL_PRICE"] = row[level_open_high]
        tax = round(row[level_open_high] * 0.0005, 2)
        data.loc[index, "COMMISSION"] = tax
        data.loc[index, "BALANCE"] = (
            data.loc[index, "BALANCE"] - tax + row[level_open_high]
        )
        level_open += 1
        level_open_high = f"GC_{grid_value}_LEVEL_HIGH_{level_open if level_open < max_level else max_level}"
        level_close = 0 if position["size"] >= -2 else level_close + 1
        level_close_high = f"GC_{grid_value}_LEVEL_HIGH_{level_close if level_close < max_level else max_level}"
        return position, level_open, level_open_high, level_close, level_close_high

    def close_short(
        position: dict,
        level_close_high: str,
        level_open: int,
        level_close: int,
    ):
        sell_price = row[gc_mid] if position["size"] == -1 else row[level_close_high]
        data.loc[index, "BUY_PRICE"] = sell_price
        tax = round(sell_price * 0.0005, 2)
        data.loc[index, "COMMISSION"] = tax
        data.loc[index, "BALANCE"] = data.loc[index, "BALANCE"] - tax - sell_price

        data.loc[index, "PROFIT"] = round(
            position["avarage_price"] - sell_price - (tax * 2), 2
        )
        if position["size"] + 1 == 0:
            position = {"direction": None, "size": None, "avarage_price": None}
        else:
            position["size"] += 1
        level_open -= 1
        level_open_high = f"GC_{grid_value}_LEVEL_HIGH_{level_open if level_open < max_level else max_level}"
        level_close = (
            0 if position["size"] is None or position["size"] == 0 else level_close - 1
        )
        level_close_high = f"GC_{grid_value}_LEVEL_HIGH_{level_close}"
        return (
            position,
            level_open,
            level_open_high,
            level_close,
            level_close_high,
        )

    def open_long(
        position: dict, level_open_low: str, level_open: int, level_close: int
    ):
        avarage_price = (
            row[level_open_low]
            if position["size"] is None
            else calc_avarage_price(position, row[level_open_low])
        )
        position = {
            "direction": "long",
            "size": 1 if position["size"] is None else position["size"] + 1,
            "avarage_price": avarage_price,
        }
        data.loc[index, "BUY_PRICE"] = row[level_open_low]
        tax = round(row[level_open_low] * 0.0005, 2)
        data.loc[index, "COMMISSION"] = tax
        data.loc[index, "BALANCE"] = (
            data.loc[index, "BALANCE"] - tax - row[level_open_low]
        )
        level_open += 1
        level_open_low = f"GC_{grid_value}_LEVEL_LOW_{level_open if level_open <= max_level else max_level}"
        level_close = 0 if position["size"] <= 2 else level_close + 1
        level_close_low = f"GC_{grid_value}_LEVEL_LOW_{level_close if level_close < max_level else max_level}"
        return position, level_open, level_open_low, level_close, level_close_low

    def close_long(
        position: dict,
        level_close_low: str,
        level_open: int,
        level_close: int,
    ):
        sell_price = row[gc_mid] if position["size"] == 1 else row[level_close_low]
        data.loc[index, "SELL_PRICE"] = sell_price
        tax = round(sell_price * 0.0005, 2)
        data.loc[index, "COMMISSION"] = tax
        data.loc[index, "BALANCE"] = data.loc[index, "BALANCE"] - tax + sell_price

        data.loc[index, "PROFIT"] = round(
            sell_price - position["avarage_price"] - (tax * 2), 2
        )
        if position["size"] - 1 == 0:
            position = {"direction": None, "size": None, "avarage_price": None}
        else:
            position["size"] -= 1
        level_open -= 1
        level_open_low = f"GC_{grid_value}_LEVEL_LOW_{level_open if level_open <= max_level else max_level}"
        level_close = (
            0 if position["size"] is None or position["size"] == 0 else level_close - 1
        )
        level_close_low = f"GC_{grid_value}_LEVEL_LOW_{level_close}"
        return position, level_open, level_open_low, level_close, level_close_low

    for index, row in data.iterrows():
        while (
            position["size"] is not None
            and position["size"] < 0
            and row["LOW"] < calc_sell_price()
        ):
            (
                position,
                level_open,
                level_open_high,
                level_close,
                level_close_high,
            ) = close_short(position, level_close_high, level_open, level_close)

        while (
            position["size"] is not None
            and position["size"] > 0
            and row["HIGH"] > calc_sell_price()
        ):
            position, level_open, level_open_low, level_close, level_close_low = (
                close_long(position, level_close_low, level_open, level_close)
            )
        while row["HIGH"] > row[level_open_high] and (
            position["size"] is None or position["size"] >= -max_level
        ):
            (
                position,
                level_open,
                level_open_high,
                level_close,
                level_close_high,
            ) = open_short(position, level_open_high, level_open, level_close)

        while row["LOW"] < row[level_open_low] and (
            position["size"] is None or position["size"] <= max_level
        ):
            (
                position,
                level_open,
                level_open_low,
                level_close,
                level_close_low,
            ) = open_long(position, level_open_low, level_open, level_close)
    data.to_excel("result_grid.xlsx", index=False)
    return data
