def plot_data_method(self) -> dict:

    gc_steps = self._config["indicators"][0]["steps"]
    gc_value = max(gc_steps)

    pc_high = f"GC_{gc_value}_HIGH"
    pc_low = f"GC_{gc_value}_LOW"
    pc_mid = f"GC_{gc_value}_MID"

    # Базовые required_columns
    required_columns = [
        "OPEN",
        "CLOSE",
        "HIGH",
        "LOW",
        "DATE",
        pc_high,
        pc_low,
        pc_mid,
    ]

    # Базовые plots
    plots = [
        {"column": pc_high, "color": "#7B93FF", "width": 2},
        {"column": pc_low, "color": "#7B93FF", "width": 2},
        {"column": pc_mid, "color": "#BFFF2B", "width": 3},
    ]

    # Динамически добавляем колонки для каждого уровня steps
    for idx in enumerate(gc_steps):
        high_step_col = f"GC_{gc_value}_LEVEL_HIGH_{idx[0]}"
        low_step_col = f"GC_{gc_value}_LEVEL_LOW_{idx[0]}"

        # Добавляем в required_columns
        required_columns.extend([high_step_col, low_step_col])

        # Добавляем в plots с одинаковым цветом и шириной
        plots.extend(
            [
                {"column": high_step_col, "color": "#808080", "width": 2},
                {"column": low_step_col, "color": "#808080", "width": 2},
            ]
        )

    return {
        "legend": "MovingGrid",
        "required_columns": required_columns,
        "plots": plots,
        "actions": [
            {"column": "BUY_PRICE", "color": "#000000", "style": "x", "width": 2},
            {"column": "SELL_PRICE", "color": "#000000", "style": "x", "width": 2},
            # {"column": "SL_PRICE", "color": "#000000", "style": "x", "width": 2},
            # {"column": "CT_PRICE", "color": "#000000", "style": "x", "width": 2},
            # {"column": "CE_PRICE", "color": "#000000", "style": "x", "width": 2},
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
                "name": "SELL",
                "price_col": "SELL_PRICE",
                "offset": 1,
                "color": "#4a6",
                "style": "o",
                "legend": "sell",
                "width": 2,
            },
            # {
            #     "name": "STOP_LOSS",
            #     "price_col": "SL_PRICE",
            #     "offset": -1,
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
