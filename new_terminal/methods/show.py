import pandas as pd
import finplot as fplt


def show_method(data: pd.DataFrame, config: dict) -> None:
    """Visualize trading data with indicators, actions, and signals using finplot"""
    # Check for required columns
    missing_columns = [
        col for col in config["required_columns"] if col not in data.columns
    ]
    if missing_columns:
        raise ValueError(f"There are no mandatory columns: {missing_columns}")

    # Create candlestick chart
    data.set_index("DATE", inplace=True)
    data.index = pd.to_datetime(data.index).tz_localize("Etc/GMT-5")
    fplt.candlestick_ochl(data[["OPEN", "CLOSE", "HIGH", "LOW"]])

    # Plot indicators
    for plot in config["plots"]:
        fplt.plot(
            data[plot["column"]],
            legend=plot["column"],
            color=plot["color"],
            width=plot["width"],
        )

    # Plot actions (points)
    for action in config["actions"]:
        col_data = data[action["column"]].dropna()
        if not col_data.empty:
            fplt.plot(
                col_data,
                legend=action["column"],
                color=action["color"],
                style=action["style"],
                width=action["width"],
            )

    # Plot signals (special markers)
    for signal in config["signals"]:
        col_data = data[signal["price_col"]].dropna()
        if not col_data.empty:
            fplt.plot(
                col_data + signal.get("offset", 0),
                legend=signal["legend"],
                color=signal["color"],
                style=signal["style"],
                width=signal["width"],
            )

    fplt.add_legend(config["legend"])
    fplt.show()
