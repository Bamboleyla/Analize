import pandas as pd
import numpy as np


class GridLine:
    __slots__ = ("size", "price", "open_arr", "close_arr")

    def __init__(self, open_arr: np.ndarray, close_arr: np.ndarray):
        self.size = None
        self.price = None
        self.open_arr = open_arr
        self.close_arr = close_arr


def calculate_method(data: pd.DataFrame, indicators: list[dict]) -> pd.DataFrame:
    grid_value = max(indicators[0]["steps"])
    gc_mid = f"GC_{grid_value}_MID"

    low_grids = [
        {
            "line_open": f"GC_{grid_value}_LEVEL_LOW_{i}",
            "line_close": gc_mid if i == 0 else f"GC_{grid_value}_LEVEL_LOW_{i-1}",
        }
        for i in range(len(indicators[0]["steps"]))
    ]
    high_grids = [
        {
            "line_open": gc_mid if i == 0 else f"GC_{grid_value}_LEVEL_HIGH_{i-1}",
            "line_close": f"GC_{grid_value}_LEVEL_HIGH_{i}",
        }
        for i in range(len(indicators[0]["steps"]))
    ]

    grids = high_grids + low_grids

    n = len(data)
    if n == 0:
        return data

    lows = data["LOW"].to_numpy()
    highs = data["HIGH"].to_numpy()
    opens = data["OPEN"].to_numpy()

    grid_lines = [
        GridLine(
            open_arr=data[line["line_open"]].to_numpy(),
            close_arr=data[line["line_close"]].to_numpy(),
        )
        for line in grids
    ]

    buy_prices = np.full(n, np.nan, dtype=np.float64)
    sell_prices = np.full(n, np.nan, dtype=np.float64)
    positions = np.zeros(n, dtype=np.float64)
    commissions = np.full(n, np.nan, dtype=np.float64)
    balances = np.zeros(n, dtype=np.float64)
    profits = np.full(n, np.nan, dtype=np.float64)

    curr_balance = 0.0
    curr_position = 0.0

    for i in range(n):
        low_i = lows[i]
        high_i = highs[i]
        open_i = opens[i]

        for line in grid_lines:
            line_open_val = line.open_arr[i]
            line_close_val = line.close_arr[i]

            if (
                line.size is None
                and low_i < line_open_val
                and high_i > line_open_val
            ):
                line.size = 1
                line.price = line_open_val
                curr_position += 1
                buy_prices[i] = line_open_val
                tax = round(line_open_val * 0.0004, 2)
                commissions[i] = tax
                curr_balance = curr_balance - tax - line_open_val
            elif line.size is not None and high_i > line_close_val:
                sell_price = line_close_val if low_i < line_close_val else open_i
                sell_prices[i] = sell_price
                tax = round(sell_price * 0.0004, 2)
                commissions[i] = tax
                curr_balance = curr_balance - tax + sell_price
                profits[i] = round(sell_price - line.price - (tax * 2), 2)
                line.size = None
                line.price = None
                curr_position -= 1

        balances[i] = curr_balance
        positions[i] = curr_position

    new_cols = pd.DataFrame(
        {
            "BUY_PRICE": buy_prices,
            "SELL_PRICE": sell_prices,
            "POSITION": positions,
            "COMMISSION": commissions,
            "BALANCE": balances,
            "PROFIT": profits,
        },
        index=data.index,
    )

    return pd.concat([data, new_cols], axis=1)
