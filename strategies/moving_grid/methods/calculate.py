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

    grid_value = max(indicators[0]["steps"])

    gc_mid = f"GC_{grid_value}_MID"

    low_grids = [
        {
            "size": None,
            "price": None,
            "line_open": f"GC_{grid_value}_LEVEL_LOW_{i}",
            "line_close": gc_mid if i == 0 else f"GC_{grid_value}_LEVEL_LOW_{i-1}",
        }
        for i in range(len(indicators[0]["steps"]))
    ]
    high_grids = [
        {
            "size": None,
            "price": None,
            "line_open": gc_mid if i == 0 else f"GC_{grid_value}_LEVEL_HIGH_{i-1}",
            "line_close": f"GC_{grid_value}_LEVEL_HIGH_{i}",
        }
        for i in range(len(indicators[0]["steps"]))
    ]

    grids = high_grids + low_grids

    for index, row in data.iterrows():
        if index == 0:
            data.loc[index, "BALANCE"] = 0
            data.loc[index, "POSITION"] = 0
        else:
            data.loc[index, "BALANCE"] = data.loc[index - 1, "BALANCE"]
            data.loc[index, "POSITION"] = data.loc[index - 1, "POSITION"]

        for line in grids:
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
            elif line["size"] is not None and row["HIGH"] > row[line["line_close"]]:
                sell_price = (
                    row[line["line_close"]]
                    if row["LOW"] < row[line["line_close"]]
                    else row["OPEN"]
                )
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
    return data
