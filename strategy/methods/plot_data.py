def plot_data_method(self) -> dict:

    pc_period = self._config["indicators"][0]["period"]
    st_period = self._config["indicators"][1]["period"]
    st_multiplier = self._config["indicators"][1]["multiplier"]

    pc_high = f"PC_{pc_period}_HIGH"
    pc_low = f"PC_{pc_period}_LOW"
    pc_mid = f"PC_{pc_period}_MID"
    st_upper = f"ST_UPPER_{st_period}_{st_multiplier}"
    st_lower = f"ST_LOWER_{st_period}_{st_multiplier}"

    return {
        "legend": "PriceChanelGrid",
        "required_columns": [
            "OPEN",
            "CLOSE",
            "HIGH",
            "LOW",
            "DATE",
            pc_high,
            pc_low,
            pc_mid,
            st_upper,
            st_lower,
            # "BUY_PRICE",
            # "SELL_PRICE",
            # "SL_PRICE",
            # "CT_PRICE",
            # "CE_PRICE",
        ],
        "plots": [
            {"column": pc_high, "color": "#7B93FF", "width": 2},
            {"column": pc_low, "color": "#7B93FF", "width": 2},
            {"column": pc_mid, "color": "#BFFF2B", "width": 3},
            {"column": st_upper, "color": "#FA0000", "width": 3},
            {"column": st_lower, "color": "#006400", "width": 3},
        ],
        "actions": [
            # {"column": "BUY_PRICE", "color": "#000000", "style": "x", "width": 2},
            # {"column": "SELL_PRICE", "color": "#000000", "style": "x", "width": 2},
            # {"column": "SL_PRICE", "color": "#000000", "style": "x", "width": 2},
            # {"column": "CT_PRICE", "color": "#000000", "style": "x", "width": 2},
            # {"column": "CE_PRICE", "color": "#000000", "style": "x", "width": 2},
        ],
        "signals": [
            # {
            #     "name": "BUY",
            #     "price_col": "BUY_PRICE",
            #     "offset": -1,
            #     "color": "#4a6",
            #     "style": "^",
            #     "legend": "buy",
            #     "width": 2,
            # },
            # {
            #     "name": "SELL",
            #     "price_col": "SELL_PRICE",
            #     "offset": 1,
            #     "color": "#4a6",
            #     "style": "o",
            #     "legend": "sell",
            #     "width": 2,
            # },
            # {
            #     "name": "STOP_LOSS",
            #     "price_col": "SL_PRICE",
            #     "offset": 1,
            #     "color": "#FF5B5B",
            #     "style": "p",
            #     "legend": "stop loss",
            #     "width": 2,
            # },
            # {
            #     "name": "CLOSE_TIME",
            #     "price_col": "CT_PRICE",
            #     "offset": 1,
            #     "color": "#3C74BD",
            #     "style": "d",
            #     "legend": "close time",
            #     "width": 2,
            # },
            # {
            #     "name": "CLOSE_END",
            #     "price_col": "CE_PRICE",
            #     "offset": 1,
            #     "color": "#000000",
            #     "style": "*",
            #     "legend": "close end",
            #     "width": 2,
            # },
        ],
    }
