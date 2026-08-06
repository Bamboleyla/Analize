def plot_data_method(self) -> dict:
    pc_period = self._config["indicators"][0]["period"]

    pc_high = f"PC_{pc_period}_HIGH"
    pc_low = f"PC_{pc_period}_LOW"
    pc_mid = f"PC_{pc_period}_MID"

    return {
        "legend": f"PriceChanel_{pc_period}",
        "required_columns": [
            "OPEN",
            "CLOSE",
            "HIGH",
            "LOW",
            "DATE",
            pc_high,
            pc_low,
            pc_mid,
            "BUY_PRICE",
            "SELL_PRICE",
            "SL_PRICE",
            "CE_PRICE",
            "TP_LEVEL",
            "SL_LEVEL",
        ],
        "plots": [
            {"column": pc_high, "color": "#7B93FF", "width": 2},
            {"column": pc_low, "color": "#7B93FF", "width": 2},
            {"column": pc_mid, "color": "#BFFF2B", "width": 3},
            {"column": "TP_LEVEL", "color": "#00E676", "width": 2},
            {"column": "SL_LEVEL", "color": "#FF5252", "width": 2},
        ],
        "actions": [
            {"column": "BUY_PRICE", "color": "#000000", "style": "x", "width": 2},
            {"column": "SELL_PRICE", "color": "#000000", "style": "x", "width": 2},
            {"column": "SL_PRICE", "color": "#000000", "style": "x", "width": 2},
            {"column": "CE_PRICE", "color": "#000000", "style": "x", "width": 2},
        ],
        "signals": [
            {
                "name": "BUY",
                "price_col": "BUY_PRICE",
                "offset": -1,
                "color": "#4a6",
                "style": "^",
                "legend": "buy",
                "width": 2,
            },
            {
                "name": "TAKE_PROFIT",
                "price_col": "SELL_PRICE",
                "offset": 1,
                "color": "#00E676",
                "style": "o",
                "legend": "take profit",
                "width": 2,
            },
            {
                "name": "STOP_LOSS",
                "price_col": "SL_PRICE",
                "offset": -1,
                "color": "#FF5252",
                "style": "p",
                "legend": "stop loss",
                "width": 2,
            },
            {
                "name": "CLOSE_END",
                "price_col": "CE_PRICE",
                "offset": 1,
                "color": "#000000",
                "style": "*",
                "legend": "close end",
                "width": 2,
            },
        ],
    }

