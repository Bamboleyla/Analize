import pandas as pd
import numpy as np


def _initialize_columns(data):
    """Initialize result columns with NaN values"""
    cols_to_init = [
        "BUY_PRICE",
        "SELL_PRICE",
        "POSITION",
        "COMMISSION",
        "BALANCE",
        "PROFIT",
    ]
    for col in cols_to_init:
        data[col] = np.nan


def calculate_method(data: pd.DataFrame, indicators: list[dict]) -> pd.DataFrame:
    _initialize_columns(data)

    grid_value = indicators[0]["value"]

    gc_high = f"GC_{grid_value}_HIGH"
    gc_low = f"GC_{grid_value}_LOW"
    gc_mid = f"GC_{grid_value}_MID"

    short_grids = [
        {
            "size": None,
            "price": None,
            "line_open": f"GC_{grid_value}_LEVEL_HIGH_{i}",
            "line_close": gc_mid if i == 0 else f"GC_{grid_value}_LEVEL_HIGH_{i-1}",
        }
        for i in range(len(indicators[0]["steps"]))
    ]
    long_grids = [
        {
            "size": None,
            "price": None,
            "line_open": f"GC_{grid_value}_LEVEL_LOW_{i}",
            "line_close": gc_mid if i == 0 else f"GC_{grid_value}_LEVEL_LOW_{i-1}",
        }
        for i in range(len(indicators[0]["steps"]))
    ]

    for index, row in data.iterrows():
        if index == 0:
            row["BALANCE"] = 0
            row["POSITION"] = 0
        else:
            data.loc[index, "BALANCE"] = data.loc[index - 1, "BALANCE"]
            data.loc[index, "POSITION"] = data.loc[index - 1, "POSITION"]

        direction = "DOWN" if row["CLOSE"] < row["OPEN"] else "UP"
        for line in long_grids:
            if (
                line["size"] is None
                and row["LOW"] < row[line["line_open"]]
                and row["HIGH"] > row[line["line_open"]]
            ):
                line["size"] = 1
                line["price"] = row[line["line_open"]]
                data.loc[index, "POSITION"] += 1
                data.loc[index, "BUY_PRICE"] = line["price"]
                tax = round(line["price"] * 0.0004, 2)
                data.loc[index, "COMMISSION"] = tax
                data.loc[index, "BALANCE"] = (
                    data.loc[index, "BALANCE"] - tax - line["price"]
                )
            elif (
                line["size"] is not None
                and row["HIGH"] > row[line["line_close"]]
                and row["LOW"] < row[line["line_close"]]
            ):
                sell_price = row[line["line_close"]]
                data.loc[index, "SELL_PRICE"] = sell_price
                tax = round(sell_price * 0.0004, 2)
                data.loc[index, "COMMISSION"] = tax
                data.loc[index, "BALANCE"] = (
                    data.loc[index, "BALANCE"] - tax + sell_price
                )
                data.loc[index, "PROFIT"] = round(
                    sell_price - line["price"] - (tax * 2), 2
                )
                line["size"] = None
                line["price"] = None
                data.loc[index, "POSITION"] -= 1
        for line in short_grids:
            if (
                line["size"] is None
                and row["LOW"] < row[line["line_open"]]
                and row["HIGH"] > row[line["line_open"]]
            ):
                line["size"] = 1
                line["price"] = row[line["line_open"]]
                data.loc[index, "POSITION"] -= 1
                data.loc[index, "SELL_PRICE"] = line["price"]
                tax = round(line["price"] * 0.0004, 2)
                data.loc[index, "COMMISSION"] = tax
                data.loc[index, "BALANCE"] = (
                    data.loc[index, "BALANCE"] - tax + line["price"]
                )
            elif (
                line["size"] is not None
                and row["HIGH"] > row[line["line_close"]]
                and row["LOW"] < row[line["line_close"]]
            ):
                sell_price = row[line["line_close"]]
                data.loc[index, "BUY_PRICE"] = sell_price
                tax = round(sell_price * 0.0004, 2)
                data.loc[index, "COMMISSION"] = tax
                data.loc[index, "BALANCE"] = (
                    data.loc[index, "BALANCE"] - tax - sell_price
                )
                data.loc[index, "PROFIT"] = round(
                    line["price"] - sell_price - (tax * 2), 2
                )
                line["size"] = None
                line["price"] = None
                data.loc[index, "POSITION"] += 1

    return data
