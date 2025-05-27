"""
Show method for displaying financial data visualization.

This function creates a candlestick chart with additional plots, actions, and signals
based on the provided configuration.

Args:
    create_report: Callback function to generate a report from the data
    data (pd.DataFrame): DataFrame containing financial data with required columns
    config (dict): Configuration dictionary containing:
        - required_columns: List of mandatory column names
        - plots: List of plot configurations with column, color, and width
        - actions: List of action configurations with column, color, style, and width
        - signals: List of signal configurations with name, price column, offset, color, style, and legend

Raises:
    ValueError: If any required columns are missing from the DataFrame
"""

import pandas as pd
import finplot as fplt


def show_method(create_report, data: pd.DataFrame, config: dict) -> None:

    # checking the mandatory columns
    missing_columns = [
        col for col in config["required_columns"] if col not in data.columns
    ]
    if missing_columns:
        raise ValueError(f"There are no mandatory columns: {missing_columns}")

    create_report(data)  # create report

    # create candlestick
    data.set_index("DATE", inplace=True)
    data.index = pd.to_datetime(data.index).tz_localize("Etc/GMT-5")

    fplt.candlestick_ochl(data[["OPEN", "CLOSE", "HIGH", "LOW"]])

    # others plots
    for plot in config["plots"]:
        fplt.plot(
            data[plot["column"]],
            legend=plot["column"],
            color=plot["color"],
            width=plot["width"],
        )

    # actions
    for action in config["actions"]:
        fplt.plot(
            data[action["column"]],
            legend=action["column"],
            color=action["color"],
            style=action["style"],
            width=action["width"],
        )

    # signals
    for signal in config["signals"]:
        points = data.loc[data["SIGNAL"] == signal["name"], signal["price_col"]]
        if not points.empty:
            fplt.plot(
                points + signal["offset"],
                color=signal["color"],
                style=signal["style"],
                legend=signal["legend"],
                width=signal["width"],
            )

    fplt.add_legend(config["legend"])
    fplt.show()
